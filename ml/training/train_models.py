import os
import sys
import pandas as pd
import joblib
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

# Add parent directory to path to ensure ml package is importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ml.config import (
    TRAIN_DATA_PATH,
    VAL_DATA_PATH,
    ARTIFACTS_DIR,
    RESULTS_DIR,
    TFIDF_MAX_FEATURES,
    TFIDF_MIN_DF,
    TFIDF_MAX_DF,
    TFIDF_NGRAM_RANGE,
    TFIDF_SUBLINEAR_TF,
    RANDOM_STATE
)

def train_and_evaluate():
    print("Loading train and validation datasets...")
    train_df = pd.read_csv(TRAIN_DATA_PATH)
    val_df = pd.read_csv(VAL_DATA_PATH)
    
    # Fill any potential nans
    train_df['combined_text'] = train_df['combined_text'].fillna("")
    val_df['combined_text'] = val_df['combined_text'].fillna("")
    
    X_train = train_df['combined_text']
    y_train = train_df['label']
    
    X_val = val_df['combined_text']
    y_val = val_df['label']
    
    print(f"Train size: {len(X_train)}, Val size: {len(X_val)}")
    
    # 1. TF-IDF Vectorization
    print("Fitting TF-IDF Vectorizer...")
    vectorizer = TfidfVectorizer(
        max_features=TFIDF_MAX_FEATURES,
        min_df=TFIDF_MIN_DF,
        max_df=TFIDF_MAX_DF,
        ngram_range=TFIDF_NGRAM_RANGE,
        sublinear_tf=TFIDF_SUBLINEAR_TF
    )
    
    X_train_vec = vectorizer.fit_transform(X_train)
    X_val_vec = vectorizer.transform(X_val)
    print(f"TF-IDF Matrix shape: {X_train_vec.shape}")
    
    # Save vectorizer and feature names
    vectorizer_path = ARTIFACTS_DIR / "tfidf_vectorizer.joblib"
    feature_names_path = ARTIFACTS_DIR / "feature_names.joblib"
    joblib.dump(vectorizer, vectorizer_path)
    joblib.dump(vectorizer.get_feature_names_out(), feature_names_path)
    print(f"Saved vectorizer and feature names to {ARTIFACTS_DIR}")
    
    # 2. Define Models
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=RANDOM_STATE),
        "Multinomial Naive Bayes": MultinomialNB(),
        "Linear SVM": CalibratedClassifierCV(
            estimator=LinearSVC(random_state=RANDOM_STATE, dual=False)
        )
    }
    
    comparison_results = []
    trained_models = {}
    
    # 3. Train and Evaluate
    for name, model in models.items():
        print(f"Training {name}...")
        model.fit(X_train_vec, y_train)
        trained_models[name] = model
        
        # Predict on validation data
        preds = model.predict(X_val_vec)
        
        # Evaluate
        accuracy = accuracy_score(y_val, preds)
        precision, recall, f1, _ = precision_recall_fscore_support(y_val, preds, average='binary')
        
        print(f"{name} validation results:")
        print(f"  Accuracy:  {accuracy:.4f}")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall:    {recall:.4f}")
        print(f"  F1-Score:  {f1:.4f}\n")
        
        comparison_results.append({
            "Model": name,
            "Accuracy": float(round(accuracy, 4)),
            "Precision": float(round(precision, 4)),
            "Recall": float(round(recall, 4)),
            "F1_Score": float(round(f1, 4))
        })
        
        # Save each trained model to artifacts temporarily
        model_filename = name.lower().replace(" ", "_") + ".joblib"
        joblib.dump(model, ARTIFACTS_DIR / model_filename)
        
    # Save comparison to CSV
    comp_df = pd.DataFrame(comparison_results)
    comparison_csv_path = RESULTS_DIR / "model_comparison.csv"
    comp_df.to_csv(comparison_csv_path, index=False)
    print(f"Saved model comparison table to {comparison_csv_path}")
    
    # Save comparison details as json for easier reading in UI if needed
    with open(RESULTS_DIR / "model_comparison.json", 'w') as f:
        json.dump(comparison_results, f, indent=4)
        
    return trained_models, comparison_results

if __name__ == "__main__":
    train_and_evaluate()
