import numpy as np
from backend.app.ml.model_loader import artifacts

class ExplainerService:
    @staticmethod
    def explain(combined_text: str, pred_class_label: str, max_features: int = 10):
        """
        Extracts word-level feature contributions for the prediction of a given text.
        """
        # Ensure model and vectorizer are loaded
        if not artifacts.is_loaded:
            return {
                "supporting_features": [],
                "opposing_features": []
            }
            
        model = artifacts.model
        vectorizer = artifacts.vectorizer
        model_name = artifacts.metadata.get("best_model_name", "")
        
        # 1. Transform text to TF-IDF vector
        x_vec = vectorizer.transform([combined_text])
        feature_names = vectorizer.get_feature_names_out()
        
        # 2. Extract active features (words present in text)
        non_zero_indices = x_vec.nonzero()[1]
        tfidf_values = x_vec.toarray()[0]
        
        # 3. Extract model weights
        weights = None
        
        # Handle CalibratedClassifierCV
        if hasattr(model, "calibrated_classifiers_"):
            coefs = []
            for clf in model.calibrated_classifiers_:
                base_est = getattr(clf, "estimator", None) or getattr(clf, "base_estimator", None)
                if base_est and hasattr(base_est, "coef_"):
                    coefs.append(base_est.coef_[0])
                elif hasattr(clf, "coef_"):
                    coefs.append(clf.coef_[0])
            if coefs:
                weights = np.mean(coefs, axis=0)
        elif hasattr(model, "coef_"):
            weights = model.coef_[0]
        elif model_name == "Multinomial Naive Bayes" and hasattr(model, "feature_log_prob_"):
            # MNB contribution is log probability difference
            weights = model.feature_log_prob_[1] - model.feature_log_prob_[0]
            
        pred_class = 1 if pred_class_label == "LIKELY_FAKE" else 0
        
        contributions = []
        if weights is not None:
            for idx in non_zero_indices:
                word = feature_names[idx]
                tfidf_val = tfidf_values[idx]
                weight = weights[idx]
                contrib = weight * tfidf_val
                
                # Keep only features with non-zero contribution
                if abs(contrib) > 1e-6:
                    contributions.append({
                        "word": word,
                        "weight": float(contrib),
                        "tfidf": float(tfidf_val),
                        "model_coef": float(weight)
                    })
                    
        # Split into supporting and opposing
        supporting = []
        opposing = []
        
        for c in contributions:
            # For class 1 (Fake): positive weight supports, negative opposes
            # For class 0 (Genuine): negative weight supports, positive opposes
            is_positive = c["weight"] > 0
            if pred_class == 1:
                if is_positive:
                    supporting.append({
                        "word": c["word"],
                        "weight": float(abs(c["weight"])),
                        "tfidf": c["tfidf"],
                        "model_coef": c["model_coef"]
                    })
                else:
                    opposing.append({
                        "word": c["word"],
                        "weight": float(abs(c["weight"])),
                        "tfidf": c["tfidf"],
                        "model_coef": c["model_coef"]
                    })
            else:
                if not is_positive:
                    supporting.append({
                        "word": c["word"],
                        "weight": float(abs(c["weight"])),
                        "tfidf": c["tfidf"],
                        "model_coef": c["model_coef"]
                    })
                else:
                    opposing.append({
                        "word": c["word"],
                        "weight": float(abs(c["weight"])),
                        "tfidf": c["tfidf"],
                        "model_coef": c["model_coef"]
                    })
                    
        # Sort by absolute weight descending
        supporting = sorted(supporting, key=lambda x: x["weight"], reverse=True)[:max_features]
        opposing = sorted(opposing, key=lambda x: x["weight"], reverse=True)[:max_features]
        
        return {
            "supporting_features": supporting,
            "opposing_features": opposing
        }
