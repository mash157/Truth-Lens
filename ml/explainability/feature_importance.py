import os
import sys
import joblib
import pandas as pd
import json

# Add parent directory to path to ensure ml package is importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ml.config import ARTIFACTS_DIR, RESULTS_DIR

def extract_global_feature_importance():
    print("Extracting global feature importance from the best model...")
    
    # Load model and vectorizer
    best_model_path = ARTIFACTS_DIR / "best_model.joblib"
    feature_names_path = ARTIFACTS_DIR / "feature_names.joblib"
    metadata_path = ARTIFACTS_DIR / "model_metadata.json"
    
    if not (best_model_path.exists() and feature_names_path.exists()):
        raise FileNotFoundError("Best model or feature names joblib not found.")
        
    model = joblib.load(best_model_path)
    feature_names = joblib.load(feature_names_path)
    
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
        
    model_name = metadata.get("best_model_name", "")
    print(f"Model: {model_name}")
    
    # Extract coefficients
    # CalibratedClassifierCV wraps the base estimator. Let's handle both calibrated and uncalibrated models.
    if hasattr(model, "calibrated_classifiers_"):
        # Calibrated SVM: average coefficients across base estimators
        coefs = []
        for clf in model.calibrated_classifiers_:
            # clf.base_estimator is the LinearSVC (in sklearn it can be base_estimator or estimator)
            base_est = getattr(clf, "estimator", None) or getattr(clf, "base_estimator", None)
            if base_est and hasattr(base_est, "coef_"):
                coefs.append(base_est.coef_[0])
            elif hasattr(clf, "coef_"):
                coefs.append(clf.coef_[0])
        if coefs:
            import numpy as np
            coef = np.mean(coefs, axis=0)
        else:
            print("Warning: Could not extract coefficients from calibrated model base estimators.")
            coef = None
    elif hasattr(model, "coef_"):
        # For standard Logistic Regression or Multinomial NB
        coef = model.coef_[0]
    else:
        print("Warning: Model does not have coefficients (e.g. not linear).")
        coef = None
        
    if coef is not None:
        # Create a DataFrame mapping features to coefficients
        # 1 = Fake (positive coefficient means word is associated with Fake)
        # 0 = Genuine (negative coefficient means word is associated with Genuine)
        importance_df = pd.DataFrame({
            "feature": feature_names,
            "coefficient": coef
        })
        
        # Sort by coefficient
        importance_df = importance_df.sort_values(by="coefficient", ascending=False)
        
        # Save to CSV
        importance_csv_path = RESULTS_DIR / "feature_importance.csv"
        importance_df.to_csv(importance_csv_path, index=False)
        print(f"Saved {len(importance_df)} feature importances to {importance_csv_path}")
        
        # Save top 20 fake and top 20 genuine features to a JSON for dashboard quick access
        top_fake = importance_df.head(20).to_dict(orient="records")
        top_genuine = importance_df.tail(20).iloc[::-1].to_dict(orient="records") # reverse so most negative is first
        
        importance_json_path = RESULTS_DIR / "feature_importance.json"
        with open(importance_json_path, 'w') as f:
            json.dump({
                "model_name": model_name,
                "top_fake_features": top_fake,
                "top_genuine_features": top_genuine
            }, f, indent=4)
            
        print(f"Saved top importances summary to {importance_json_path}")
    else:
        # Naive Bayes handles feature importance through feature log probability
        if model_name == "Multinomial Naive Bayes":
            # coef_ in MultinomialNB represents log(P(x_i | y_c))
            # Let's extract difference in log probability between classes
            # class 0 = Genuine, class 1 = Fake
            if hasattr(model, "feature_log_prob_"):
                log_prob_diff = model.feature_log_prob_[1] - model.feature_log_prob_[0]
                importance_df = pd.DataFrame({
                    "feature": feature_names,
                    "coefficient": log_prob_diff
                }).sort_values(by="coefficient", ascending=False)
                
                importance_csv_path = RESULTS_DIR / "feature_importance.csv"
                importance_df.to_csv(importance_csv_path, index=False)
                
                top_fake = importance_df.head(20).to_dict(orient="records")
                top_genuine = importance_df.tail(20).iloc[::-1].to_dict(orient="records")
                
                with open(RESULTS_DIR / "feature_importance.json", 'w') as f:
                    json.dump({
                        "model_name": model_name,
                        "top_fake_features": top_fake,
                        "top_genuine_features": top_genuine
                    }, f, indent=4)
                print("Extracted MultinomialNB log probability difference as feature importance.")
            else:
                print("Could not extract feature log probabilities from MultinomialNB.")
        else:
            print("No feature importance extracted.")

if __name__ == "__main__":
    extract_global_feature_importance()
