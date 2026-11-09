import os
import sys
import pandas as pd
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score

# Add parent directory to path to ensure ml package is importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ml.config import (
    TRAIN_DATA_PATH,
    VAL_DATA_PATH,
    RESULTS_DIR,
    TFIDF_MAX_FEATURES,
    TFIDF_MIN_DF,
    TFIDF_MAX_DF,
    TFIDF_NGRAM_RANGE,
    TFIDF_SUBLINEAR_TF,
    RANDOM_STATE
)

def tune_hyperparameters():
    print("Running hyperparameter tuning for Logistic Regression...")
    train_df = pd.read_csv(TRAIN_DATA_PATH)
    val_df = pd.read_csv(VAL_DATA_PATH)
    
    # Clean nans
    train_df['combined_text'] = train_df['combined_text'].fillna("")
    val_df['combined_text'] = val_df['combined_text'].fillna("")
    
    # Use a 20% sample of the training data for faster grid search
    train_sample = train_df.sample(frac=0.2, random_state=RANDOM_STATE)
    X_train_sub = train_sample['combined_text']
    y_train_sub = train_sample['label']
    
    X_val = val_df['combined_text']
    y_val = val_df['label']
    
    # Fit vectorizer
    vectorizer = TfidfVectorizer(
        max_features=TFIDF_MAX_FEATURES,
        min_df=TFIDF_MIN_DF,
        max_df=TFIDF_MAX_DF,
        ngram_range=TFIDF_NGRAM_RANGE,
        sublinear_tf=TFIDF_SUBLINEAR_TF
    )
    X_train_vec = vectorizer.fit_transform(X_train_sub)
    X_val_vec = vectorizer.transform(X_val)
    
    c_values = [0.1, 1.0, 10.0]
    best_c = 1.0
    best_f1 = 0
    tuning_log = []
    
    for c in c_values:
        print(f"Testing C={c}...")
        model = LogisticRegression(C=c, max_iter=1000, random_state=RANDOM_STATE)
        model.fit(X_train_vec, y_train_sub)
        
        preds = model.predict(X_val_vec)
        f1 = f1_score(y_val, preds)
        print(f"  F1-Score: {f1:.4f}")
        
        tuning_log.append({"C": c, "F1-Score": float(round(f1, 4))})
        
        if f1 > best_f1:
            best_f1 = f1
            best_c = c
            
    print(f"Optimal C selected: {best_c} with F1-Score: {best_f1:.4f}")
    
    # Save tuning log
    tuning_file = RESULTS_DIR / "hyperparameter_tuning.json"
    with open(tuning_file, 'w') as f:
        json.dump({
            "model": "Logistic Regression",
            "tuning_parameters": "C (regularization strength)",
            "results": tuning_log,
            "best_C": best_c
        }, f, indent=4)
        
    print(f"Tuning results saved to {tuning_file}")

if __name__ == "__main__":
    tune_hyperparameters()
