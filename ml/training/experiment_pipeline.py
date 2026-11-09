"""
TruthLens Comprehensive ML Experiment Pipeline (Optimized, Staged)

Implements all experiments efficiently:
- Word TF-IDF configs
- Character TF-IDF
- Word + Character combined
- Model comparison
- SVM hyperparameter tuning
- 5-fold cross-validation
- Confidence calibration
- Uncertainty detection
- External dataset evaluation

The pipeline is split into independently runnable, checkpointed STAGES so long
runs can be resumed without repeating completed work. State is stored in
ml/results/pipeline_state.json.

Usage:
    python -m ml.training.experiment_pipeline --stage exp1      # baseline
    python -m ml.training.experiment_pipeline --stage exp2      # word configs
    python -m ml.training.experiment_pipeline --stage exp3      # char TF-IDF
    python -m ml.training.experiment_pipeline --stage exp4      # word+char
    python -m ml.training.experiment_pipeline --stage exp5      # model comparison
    python -m ml.training.experiment_pipeline --stage exp6      # SVM tuning
    python -m ml.training.experiment_pipeline --stage cv1..cv5  # CV folds
    python -m ml.training.experiment_pipeline --stage final     # final model+artifacts
    python -m ml.training.experiment_pipeline --stage status    # show progress
    python -m ml.training.experiment_pipeline --stage reset     # clear state

NO Serper / web calls happen anywhere in this pipeline.
"""

import os
import sys
import json
import time
import argparse
import joblib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix,
    classification_report,
)
from scipy.sparse import hstack

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ml.config import (
    TRAIN_DATA_PATH,
    VAL_DATA_PATH,
    TEST_DATA_PATH,
    ARTIFACTS_DIR,
    RESULTS_DIR,
    RANDOM_STATE
)
from ml.preprocessing.clean_text import combine_headline_and_body


class CombinedVectorizer:
    """Memory-efficient combined word + character TF-IDF transformer."""

    def __init__(self, word_params=None, char_params=None):
        self.word_params = word_params or {}
        self.char_params = char_params or {}
        self.word_vectorizer = None
        self.char_vectorizer = None
        self._fitted = False

    def fit(self, X, y=None):
        self.word_vectorizer = TfidfVectorizer(**self.word_params)
        self.char_vectorizer = TfidfVectorizer(**self.char_params)
        self.word_vectorizer.fit(X)
        self.char_vectorizer.fit(X)
        self._fitted = True
        return self

    def fit_transform(self, X, y=None):
        self.fit(X, y)
        return self.transform(X)

    def transform(self, X):
        X_word = self.word_vectorizer.transform(X)
        X_char = self.char_vectorizer.transform(X)
        return hstack([X_word, X_char])

    def get_feature_names_out(self):
        word_names = self.word_vectorizer.get_feature_names_out()
        char_names = self.char_vectorizer.get_feature_names_out()
        return np.concatenate([
            np.array([f"word_{n}" for n in word_names]),
            np.array([f"char_{n}" for n in char_names])
        ])


def train_and_evaluate(name, vectorizer, model, X_train, y_train, X_val, y_val, X_test=None, y_test=None):
    """Train, evaluate, and return results."""
    t0 = time.time()
    X_tr_vec = vectorizer.fit_transform(X_train)
    X_va_vec = vectorizer.transform(X_val)
    model.fit(X_tr_vec, y_train)

    preds_val = model.predict(X_va_vec)
    acc_v = accuracy_score(y_val, preds_val)
    p_v, r_v, f1_v, _ = precision_recall_fscore_support(y_val, preds_val, average='binary')

    res = {
        "name": name,
        "val_accuracy": round(float(acc_v), 4),
        "val_precision": round(float(p_v), 4),
        "val_recall": round(float(r_v), 4),
        "val_f1": round(float(f1_v), 4),
        "time_s": round(time.time() - t0, 1)
    }

    if X_test is not None and y_test is not None:
        X_te_vec = vectorizer.transform(X_test)
        preds_te = model.predict(X_te_vec)
        acc_t = accuracy_score(y_test, preds_te)
        p_t, r_t, f1_t, _ = precision_recall_fscore_support(y_test, preds_te, average='binary')
        res["test_accuracy"] = round(float(acc_t), 4)
        res["test_precision"] = round(float(p_t), 4)
        res["test_recall"] = round(float(r_t), 4)
        res["test_f1"] = round(float(f1_t), 4)

    return res, model, vectorizer


# ---------------------------------------------------------------------------
# Resumable staging helpers
# ---------------------------------------------------------------------------

STATE_PATH = RESULTS_DIR / "pipeline_state.json"
N_CV_FOLDS = 5


def _load_state():
    if STATE_PATH.exists():
        with open(STATE_PATH) as f:
            return json.load(f)
    return {}


def _save_state(state):
    with open(STATE_PATH, 'w') as f:
        json.dump(state, f, indent=2)


def _upsert_exp(state, result):
    exps = [e for e in state.get("experiments", []) if e.get("name") != result["name"]]
    exps.append(result)
    state["experiments"] = exps


def _load_splits():
    train_df = pd.read_csv(TRAIN_DATA_PATH)
    val_df = pd.read_csv(VAL_DATA_PATH)
    test_df = pd.read_csv(TEST_DATA_PATH)
    for d in [train_df, val_df, test_df]:
        d['combined_text'] = d['combined_text'].fillna("")
    return (
        train_df['combined_text'], train_df['label'],
        val_df['combined_text'], val_df['label'],
        test_df['combined_text'], test_df['label'],
    )


def _calibrated_svm(c=1.0, class_weight=None, cv=3):
    return CalibratedClassifierCV(
        estimator=LinearSVC(C=c, class_weight=class_weight,
                            random_state=RANDOM_STATE, dual=False),
        cv=cv, n_jobs=-1
    )


class CrossValidateConfig:
    """Stratified k-fold CV helpers (fold-wise for resumable staging)."""

    @staticmethod
    def run_fold(fold_i, word_cfg, model_c, model_class_weight, X, y):
        skf = StratifiedKFold(n_splits=N_CV_FOLDS, shuffle=True,
                              random_state=RANDOM_STATE)
        train_idx, val_idx = list(skf.split(X, y))[fold_i]
        X_tr, X_va = X.iloc[train_idx], X.iloc[val_idx]
        y_tr, y_va = y.iloc[train_idx], y.iloc[val_idx]

        vec = TfidfVectorizer(**word_cfg)
        X_tr_vec = vec.fit_transform(X_tr)
        X_va_vec = vec.transform(X_va)
        mdl = _calibrated_svm(model_c, model_class_weight)
        mdl.fit(X_tr_vec, y_tr)

        preds = mdl.predict(X_va_vec)
        acc = accuracy_score(y_va, preds)
        p, r, f1, _ = precision_recall_fscore_support(y_va, preds, average='binary')
        print(f"    Fold {fold_i + 1}: Acc={acc:.4f} F1={f1:.4f}")
        return {"accuracy": acc, "precision": p, "recall": r, "f1": f1}

    @staticmethod
    def aggregate(folds):
        summary = {}
        for m in ["accuracy", "precision", "recall", "f1"]:
            vals = [f[m] for f in folds]
            summary[f"mean_{m}"] = round(float(np.mean(vals)), 4)
            summary[f"std_{m}"] = round(float(np.std(vals)), 4)
        return summary


class ExperimentStages:
    """Individual experiment stages. Each stage is independently runnable and
    its result is checkpointed so long runs can resume."""

    @staticmethod
    def exp1_baseline():
        state = _load_state()
        X_train, y_train, X_val, y_val, X_test, y_test = _load_splits()
        vec = TfidfVectorizer(max_features=10000, min_df=2, max_df=0.95,
                              ngram_range=(1, 2), sublinear_tf=True)
        mod = _calibrated_svm()
        r, _, _ = train_and_evaluate("Baseline 10k (1,2)", vec, mod,
                                     X_train, y_train, X_val, y_val, X_test, y_test)
        _upsert_exp(state, r)
        print(f"Exp1 baseline: Val F1={r['val_f1']:.4f} Test F1={r.get('test_f1', '?')}")
        _save_state(state)

    @staticmethod
    def exp2_word_configs():
        state = _load_state()
        X_train, y_train, X_val, y_val, _, _ = _load_splits()
        word_cfgs = [
            ("20k (1,2)", dict(max_features=20000, min_df=2, max_df=0.95,
                               ngram_range=(1, 2), sublinear_tf=True)),
            ("30k (1,2) df3", dict(max_features=30000, min_df=3, max_df=0.90,
                                   ngram_range=(1, 2), sublinear_tf=True)),
            ("20k (1,3)", dict(max_features=20000, min_df=2, max_df=0.95,
                               ngram_range=(1, 3), sublinear_tf=True)),
        ]
        best_word_f1, best_word_cfg = 0, None
        for label, cfg in word_cfgs:
            vec = TfidfVectorizer(**cfg)
            mod = _calibrated_svm()
            r, _, _ = train_and_evaluate(f"Word {label}", vec, mod,
                                         X_train, y_train, X_val, y_val)
            _upsert_exp(state, r)
            print(f"  {label}: Val F1={r['val_f1']:.4f}")
            if r['val_f1'] > best_word_f1:
                best_word_f1, best_word_cfg = r['val_f1'], cfg
        state["best_word_f1"] = best_word_f1
        state["best_word_cfg"] = best_word_cfg
        print(f"Best word config: F1={best_word_f1:.4f} cfg={best_word_cfg}")
        _save_state(state)

    @staticmethod
    def exp3_char():
        state = _load_state()
        X_train, y_train, X_val, y_val, _, _ = _load_splits()
        char_cfg = dict(analyzer="char", ngram_range=(3, 5), max_features=30000,
                        min_df=2, max_df=0.95, sublinear_tf=True)
        vec = TfidfVectorizer(**char_cfg)
        mod = _calibrated_svm()
        r, _, _ = train_and_evaluate("Char (3,5) 30k", vec, mod,
                                     X_train, y_train, X_val, y_val)
        _upsert_exp(state, r)
        print(f"Exp3 char TF-IDF: Val F1={r['val_f1']:.4f}")
        _save_state(state)

    @staticmethod
    def exp4_combined():
        state = _load_state()
        assert state.get("best_word_cfg"), "Run exp2 first"
        X_train, y_train, X_val, y_val, _, _ = _load_splits()
        wc = state["best_word_cfg"]
        combined = CombinedVectorizer(
            word_params=wc,
            char_params=dict(analyzer="char", ngram_range=(3, 5), max_features=15000,
                             min_df=2, max_df=0.95, sublinear_tf=True)
        )
        mod = _calibrated_svm()
        r, _, _ = train_and_evaluate("Combined Word+Char", combined, mod,
                                     X_train, y_train, X_val, y_val)
        _upsert_exp(state, r)
        print(f"Exp4 combined: Val F1={r['val_f1']:.4f}")
        _save_state(state)

    @staticmethod
    def exp5_model_comparison():
        state = _load_state()
        assert state.get("best_word_cfg"), "Run exp2 first"
        X_train, y_train, X_val, y_val, _, _ = _load_splits()
        cfg = state["best_word_cfg"]
        models = {
            "LogisticRegression": lambda: LogisticRegression(
                max_iter=1000, random_state=RANDOM_STATE, C=10.0, n_jobs=-1),
            "MultinomialNB": lambda: MultinomialNB(alpha=1.0),
            "LinearSVM_Calibrated": lambda: _calibrated_svm(),
        }
        best_model_name, best_model_f1 = None, 0
        for name, mf in models.items():
            vec = TfidfVectorizer(**cfg)
            mod = mf()
            r, _, _ = train_and_evaluate(f"BestWord+{name}", vec, mod,
                                         X_train, y_train, X_val, y_val)
            _upsert_exp(state, r)
            print(f"  {name}: Val F1={r['val_f1']:.4f}")
            if r['val_f1'] > best_model_f1:
                best_model_f1, best_model_name = r['val_f1'], name
        state["best_model_name"] = best_model_name
        print(f"Best comparison model on val: {best_model_name} F1={best_model_f1:.4f}")
        _save_state(state)

    @staticmethod
    def exp6_svm_tuning():
        state = _load_state()
        assert state.get("best_word_cfg"), "Run exp2 first"
        X_train, y_train, X_val, y_val, _, _ = _load_splits()
        cfg = state["best_word_cfg"]
        c_vals = [0.1, 0.5, 1, 2, 5, 10]
        class_weights = [None, "balanced"]
        best_svm_f1, best_svm_c, best_svm_cw = 0, 1, None
        best_svm_val_metrics = None
        tuning_log = []

        tuning_vec = TfidfVectorizer(**cfg)
        X_train_tune = tuning_vec.fit_transform(X_train)
        X_val_tune = tuning_vec.transform(X_val)

        for cw in class_weights:
            for c in c_vals:
                t0 = time.time()
                mod = _calibrated_svm(c, cw)
                mod.fit(X_train_tune, y_train)
                preds_val = mod.predict(X_val_tune)
                acc_v = accuracy_score(y_val, preds_val)
                p_v, r_v, f1_v, _ = precision_recall_fscore_support(
                    y_val, preds_val, average='binary')
                elapsed = round(time.time() - t0, 1)
                r = {"name": f"SVM C={c} cw={cw}",
                     "val_accuracy": round(float(acc_v), 4),
                     "val_precision": round(float(p_v), 4),
                     "val_recall": round(float(r_v), 4),
                     "val_f1": round(float(f1_v), 4),
                     "time_s": elapsed}
                _upsert_exp(state, r)
                tuning_log.append({"C": c, "class_weight": str(cw),
                                   "val_f1": r['val_f1']})
                print(f"  C={c} cw={cw}: Val F1={r['val_f1']:.4f} ({elapsed}s)")
                if r['val_f1'] > best_svm_f1:
                    best_svm_f1 = r['val_f1']
                    best_svm_c, best_svm_cw = c, cw
                    best_svm_val_metrics = {
                        "accuracy": r["val_accuracy"], "precision": r["val_precision"],
                        "recall": r["val_recall"], "f1_score": r["val_f1"]
                    }

        print(f"Best SVM: C={best_svm_c} cw={best_svm_cw} F1={best_svm_f1:.4f}")
        state["best_svm"] = {"C": best_svm_c, "class_weight": str(best_svm_cw),
                             "val_f1": round(best_svm_f1, 4)}
        state["best_svm_val_metrics"] = best_svm_val_metrics
        state["tuning_log"] = tuning_log
        with open(RESULTS_DIR / "svm_tuning.json", 'w') as f:
            json.dump({"best_C": best_svm_c, "best_class_weight": best_svm_cw,
                       "best_val_f1": round(best_svm_f1, 4), "results": tuning_log},
                      f, indent=4)
        _save_state(state)


class FinalStage:
    """Phases 8-11 + artifact generation using the validated best config."""

    @staticmethod
    def run():
        state = _load_state()
        assert state.get("best_svm"), "Run exp6 first"
        assert len(state.get("cv_folds", {})) == N_CV_FOLDS, \
            f"Run all {N_CV_FOLDS} CV folds first"

        X_train, y_train, X_val, y_val, X_test, y_test = _load_splits()
        cfg = state["best_word_cfg"]
        best_svm = state["best_svm"]
        best_c = best_svm["C"]
        best_cw = None if best_svm["class_weight"] == "None" else best_svm["class_weight"]

        # ---- Phase 8-9: Final Model on train+val, evaluate ONCE on test ----
        print("\n--- Final Model Training + Calibration ---")
        final_vec = TfidfVectorizer(**cfg)
        X_all_train = pd.concat([X_train, X_val], ignore_index=True)
        y_all_train = pd.concat([y_train, y_val], ignore_index=True)
        X_all_vec = final_vec.fit_transform(X_all_train)

        final_svc = LinearSVC(C=best_c, class_weight=best_cw,
                              random_state=RANDOM_STATE, dual=False)
        final_model = CalibratedClassifierCV(estimator=final_svc, cv=5,
                                             method='sigmoid', n_jobs=-1)
        final_model.fit(X_all_vec, y_all_train)

        X_test_vec = final_vec.transform(X_test)
        test_preds = final_model.predict(X_test_vec)
        test_acc = accuracy_score(y_test, test_preds)
        test_p, test_r, test_f1, _ = precision_recall_fscore_support(
            y_test, test_preds, average='binary')
        cm = confusion_matrix(y_test, test_preds)
        print(f"FINAL TEST: Acc={test_acc:.4f} Prec={test_p:.4f} "
              f"Rec={test_r:.4f} F1={test_f1:.4f}")
        print(f"Confusion Matrix:\n{cm}")

        # ---- Phase 10: Uncertainty Detection ----
        # Threshold selected with a TRAIN-fitted model evaluated on the
        # held-out VALIDATION set (never the test set).
        print("\n--- Uncertainty Threshold Selection (validation set) ---")
        tune_vec = TfidfVectorizer(**cfg)
        X_train_tune = tune_vec.fit_transform(X_train)
        X_val_tune = tune_vec.transform(X_val)
        thresh_model = _calibrated_svm(best_c, best_cw)
        thresh_model.fit(X_train_tune, y_train)
        val_probs = thresh_model.predict_proba(X_val_tune)
        val_max_probs = val_probs.max(axis=1)
        val_preds = thresh_model.predict(X_val_tune)

        thresholds = [0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80]
        best_thresh, best_score = 0.55, 0
        print("  Threshold | Coverage | Accuracy | Score")
        for t in thresholds:
            mask = val_max_probs >= t
            if mask.sum() == 0:
                continue
            acc = accuracy_score(y_val[mask], val_preds[mask])
            cov = mask.sum() / len(y_val)
            score = acc * cov
            print(f"    {t:.2f}     | {cov:.3f}    | {acc:.4f}  | {score:.4f}")
            if score > best_score:
                best_score, best_thresh = score, t
        print(f"Selected threshold: {best_thresh}")

        test_probs = final_model.predict_proba(X_test_vec)
        test_max_probs = test_probs.max(axis=1)
        certain_mask = test_max_probs >= best_thresh
        n_certain = int(certain_mask.sum())
        n_uncertain = len(y_test) - n_certain
        certain_acc = accuracy_score(y_test[certain_mask], test_preds[certain_mask]) \
            if n_certain > 0 else 0
        print(f"Test: Certain={n_certain}, Uncertain={n_uncertain}, "
              f"Certain accuracy={certain_acc:.4f}")

        # ---- Phase 9: Calibration diagnostic (test set, reporting only) ----
        # Sigmoid calibration is fitted by CalibratedClassifierCV on training
        # folds only; this reliability diagram is computed on the untouched
        # test set purely as reporting and never used to fit anything.
        print("\n--- Calibration Diagnostic (test set, reporting only) ---")
        prob_fake = test_probs[:, 1]
        bin_edges = np.linspace(0, 1, 11)
        cal_data = []
        for i in range(10):
            mask = (prob_fake >= bin_edges[i]) & (prob_fake < bin_edges[i + 1])
            if mask.sum() > 0:
                cal_data.append({
                    "bin_start": round(float(bin_edges[i]), 2),
                    "bin_end": round(float(bin_edges[i + 1]), 2),
                    "mean_predicted": round(float(prob_fake[mask].mean()), 4),
                    "mean_observed": round(float(y_test.iloc[mask].mean()), 4),
                    "count": int(mask.sum())
                })
        for b in cal_data:
            print(f"  [{b['bin_start']:.1f}-{b['bin_end']:.1f}] "
                  f"predicted={b['mean_predicted']:.3f} "
                  f"observed={b['mean_observed']:.3f} n={b['count']}")

        # ---- Phase 11: External Dataset Evaluation ----
        print("\n--- External Dataset Evaluation ---")
        ext_dir = Path(__file__).resolve().parent.parent.parent / "dataset" / "external"
        ext_path = ext_dir / "external_dataset.csv"
        ext_dir.mkdir(parents=True, exist_ok=True)
        ext_results = None
        if ext_path.exists():
            ext_df = pd.read_csv(ext_path)
            if all(c in ext_df.columns for c in ['title', 'text', 'label']):
                ext_df['combined_text'] = ext_df.apply(
                    lambda r: combine_headline_and_body(r['title'], r['text']), axis=1)
                X_ext_vec = final_vec.transform(ext_df['combined_text'])
                ext_preds = final_model.predict(X_ext_vec)
                ea = accuracy_score(ext_df['label'], ext_preds)
                ep, er, ef, _ = precision_recall_fscore_support(
                    ext_df['label'], ext_preds, average='binary')
                ext_results = {"accuracy": round(float(ea), 4),
                               "precision": round(float(ep), 4),
                               "recall": round(float(er), 4),
                               "f1_score": round(float(ef), 4),
                               "dataset_size": len(ext_df)}
                print(f"External: Acc={ea:.4f} F1={ef:.4f} (n={len(ext_df)})")
            else:
                print("External dataset missing required columns (title, text, label)")
        else:
            print("No external dataset found.")
            print("To evaluate generalization later, provide:")
            print(f"  {ext_path}")
            print("with columns: title,text,label (never used for training).")

        # ---- Phase 22-23: Save Artifacts ----
        print("\n--- Saving Artifacts ---")
        joblib.dump(final_model, ARTIFACTS_DIR / "best_model.joblib")
        joblib.dump(final_vec, ARTIFACTS_DIR / "tfidf_vectorizer.joblib")
        feature_names = final_vec.get_feature_names_out()
        joblib.dump(feature_names, ARTIFACTS_DIR / "feature_names.joblib")
        joblib.dump({
            "total_features": len(feature_names),
            "has_character_features": False,
        }, ARTIFACTS_DIR / "feature_info.joblib")

        cv_results = CrossValidateConfig.aggregate(list(state["cv_folds"].values()))
        metadata = {
            "best_model_name": "Linear SVM (Calibrated)",
            "vectorizer_type": "TfidfVectorizer (word-level)",
            "tfidf_config": cfg,
            "ngram_range": str(cfg.get("ngram_range", (1, 2))),
            "max_features": cfg.get("max_features", 20000),
            "C": best_c,
            "class_weight": str(best_cw),
            "calibration_method": "sigmoid (5-fold internal CV)",
            "confidence_meaning": (
                "Calibrated probability from CalibratedClassifierCV sigmoid scaling; "
                "approximates P(predicted class is correct given the model's "
                "training distribution). It is NOT a measure of factual truth."
            ),
            "calibration_note": (
                "Calibration is fitted inside CalibratedClassifierCV on training "
                "folds only. calibration_data is a diagnostic reliability diagram "
                "evaluated on the held-out test set and fits nothing."
            ),
            "uncertainty_threshold": float(best_thresh),
            "uncertainty_policy": (
                "max calibrated class probability < threshold -> UNCERTAIN. "
                "UNCERTAIN means low model confidence, not that news is fake."
            ),
            "random_state": RANDOM_STATE,
            "validation_metrics": state.get("best_svm_val_metrics"),
            "validation_metrics_note": (
                "From the best TRAIN-fitted tuned model evaluated on the held-out "
                "validation set. The deployed final model is refit on train+val."
            ),
            "test_metrics": {"accuracy": round(float(test_acc), 4),
                             "precision": round(float(test_p), 4),
                             "recall": round(float(test_r), 4),
                             "f1_score": round(float(test_f1), 4)},
            "cross_validation": cv_results,
            "calibration_data": cal_data,
            "uncertainty_analysis": {
                "threshold": float(best_thresh),
                "test_certain_count": n_certain,
                "test_uncertain_count": n_uncertain,
                "test_certain_accuracy": round(float(certain_acc), 4)
            }
        }
        if ext_results:
            metadata["external_dataset_results"] = ext_results

        with open(ARTIFACTS_DIR / "model_metadata.json", 'w') as f:
            json.dump(metadata, f, indent=4)

        # Experiment comparison table
        exps_clean = [{k: v for k, v in e.items() if k != 'time_s'}
                      for e in state.get("experiments", [])]
        comp_df = pd.DataFrame(exps_clean)
        comp_df.to_csv(RESULTS_DIR / "model_comparison.csv", index=False)
        with open(RESULTS_DIR / "model_comparison.json", 'w') as f:
            json.dump(exps_clean, f, indent=4)
        with open(RESULTS_DIR / "all_experiments.json", 'w') as f:
            json.dump(state.get("experiments", []), f, indent=4)
        with open(RESULTS_DIR / "cross_validation.json", 'w') as f:
            json.dump(cv_results, f, indent=4)
        with open(RESULTS_DIR / "calibration_data.json", 'w') as f:
            json.dump(cal_data, f, indent=4)

        metrics = {
            "model_name": "Linear SVM (Calibrated)",
            "accuracy": round(float(test_acc), 4),
            "precision": round(float(test_p), 4),
            "recall": round(float(test_r), 4),
            "f1_score": round(float(test_f1), 4),
            "confusion_matrix": {"true_negative": int(cm[0, 0]),
                                 "false_positive": int(cm[0, 1]),
                                 "false_negative": int(cm[1, 0]),
                                 "true_positive": int(cm[1, 1])},
            "classification_report": classification_report(
                y_test, test_preds, output_dict=True)
        }
        with open(RESULTS_DIR / "metrics.json", 'w') as f:
            json.dump(metrics, f, indent=4)

        # Confusion matrix plot
        plt.figure(figsize=(6, 5))
        plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
        plt.title(f'Confusion Matrix - Final SVM (C={best_c})', fontsize=11, pad=15)
        plt.colorbar()
        tick_marks = np.arange(2)
        plt.xticks(tick_marks, ['Genuine', 'Fake'])
        plt.yticks(tick_marks, ['Genuine', 'Fake'])
        thresh_val = cm.max() / 2.
        for i, j in np.ndindex(cm.shape):
            plt.text(j, i, format(cm[i, j], 'd'), horizontalalignment="center",
                     color="white" if cm[i, j] > thresh_val else "black",
                     fontsize=14, weight='bold')
        plt.ylabel('Actual', fontsize=10, labelpad=10)
        plt.xlabel('Predicted', fontsize=10, labelpad=10)
        plt.tight_layout()
        plt.savefig(RESULTS_DIR / "confusion_matrix.png", dpi=300)
        plt.close()

        # Global feature importance from averaged fold coefficients
        coefs = []
        for clf in getattr(final_model, "calibrated_classifiers_", []):
            base_est = getattr(clf, "estimator", None) or getattr(clf, "base_estimator", None)
            if base_est is not None and hasattr(base_est, "coef_"):
                coefs.append(base_est.coef_[0])
        avg_coef = np.mean(coefs, axis=0) if coefs else None
        if avg_coef is not None:
            imp_df = pd.DataFrame({"feature": feature_names, "coefficient": avg_coef}) \
                .sort_values("coefficient", ascending=False)
            imp_df.to_csv(RESULTS_DIR / "feature_importance.csv", index=False)
            with open(RESULTS_DIR / "feature_importance.json", 'w') as f:
                json.dump({
                    "model_name": "Linear SVM (Calibrated)",
                    "top_fake_features": imp_df.head(20).to_dict("records"),
                    "top_genuine_features": imp_df.tail(20).iloc[::-1].to_dict("records")
                }, f, indent=4)

        print("\n" + "=" * 70)
        print("  FINAL STAGE COMPLETE")
        print(f"  Best Model : Linear SVM (Calibrated, C={best_c}, cw={best_cw})")
        print(f"  Best TF-IDF: {cfg}")
        print(f"  Test       : Acc={test_acc:.4f} F1={test_f1:.4f}")
        cv = cv_results
        print(f"  5-fold CV  : Acc {cv['mean_accuracy']:.4f} ± {cv['std_accuracy']:.4f} | "
              f"F1 {cv['mean_f1']:.4f} ± {cv['std_f1']:.4f}")
        print(f"  Uncertainty threshold: {best_thresh}")
        print("=" * 70)


def run_cv_fold_stage(fold_i):
    state = _load_state()
    assert state.get("best_word_cfg") and state.get("best_svm"), "Run exp2/exp6 first"
    X_train, y_train, X_val, y_val, _, _ = _load_splits()
    cfg = state["best_word_cfg"]
    best_svm = state["best_svm"]
    best_cw = None if best_svm["class_weight"] == "None" else best_svm["class_weight"]

    full_df = pd.concat([pd.read_csv(TRAIN_DATA_PATH), pd.read_csv(VAL_DATA_PATH)],
                        ignore_index=True)
    full_df['combined_text'] = full_df['combined_text'].fillna("")
    X_full, y_full = full_df['combined_text'], full_df['label']

    print(f"CV fold {fold_i + 1}/{N_CV_FOLDS}")
    fold_res = CrossValidateConfig.run_fold(fold_i, cfg, best_svm["C"], best_cw,
                                            X_full, y_full)
    folds = state.setdefault("cv_folds", {})
    folds[str(fold_i)] = fold_res
    _save_state(state)


def run_status():
    state = _load_state()
    print("Pipeline state:", STATE_PATH)
    print(f"  Experiments recorded : {len(state.get('experiments', []))}")
    print(f"  best_word_cfg        : {state.get('best_word_cfg')}")
    print(f"  best_svm             : {state.get('best_svm')}")
    print(f"  CV folds done        : {sorted(state.get('cv_folds', {}).keys())}")
    print(f"  Final artifacts      : {(ARTIFACTS_DIR / 'model_metadata.json').exists()}")


def main():
    parser = argparse.ArgumentParser(description="TruthLens staged ML pipeline")
    parser.add_argument("--stage", required=True,
                        help="exp1..exp6 | cv1..cv5 | final | status | reset")
    args = parser.parse_args()
    stage = args.stage.lower()

    t0 = time.time()
    if stage == "reset":
        if STATE_PATH.exists():
            STATE_PATH.unlink()
        print("State cleared.")
    elif stage == "status":
        run_status()
    elif stage == "exp1":
        ExperimentStages.exp1_baseline()
    elif stage == "exp2":
        ExperimentStages.exp2_word_configs()
    elif stage == "exp3":
        ExperimentStages.exp3_char()
    elif stage == "exp4":
        ExperimentStages.exp4_combined()
    elif stage == "exp5":
        ExperimentStages.exp5_model_comparison()
    elif stage == "exp6":
        ExperimentStages.exp6_svm_tuning()
    elif stage.startswith("cv"):
        idx = int(stage[2:]) - 1
        if not 0 <= idx < N_CV_FOLDS:
            raise SystemExit(f"cv index must be 1..{N_CV_FOLDS}")
        run_cv_fold_stage(idx)
    elif stage == "final":
        FinalStage.run()
    else:
        raise SystemExit(f"Unknown stage: {args.stage}")

    print(f"[stage '{stage}' done in {time.time() - t0:.1f}s]")


if __name__ == "__main__":
    main()
