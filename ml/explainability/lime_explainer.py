import os
import sys
import numpy as np
import joblib

# Add parent directory to path to ensure ml package is importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def explain_prediction(text: str, model, vectorizer, model_name: str, max_features: int = 10):
    """
    Computes local feature contribution explanation for an individual text input.
    """
    if not text.strip():
        return {
            "prediction": "AMBIGUOUS",
            "confidence": 0.50,
            "supporting_features": [],
            "opposing_features": []
        }
        
    # 1. Transform input text using vectorizer
    x_vec = vectorizer.transform([text])
    feature_names = vectorizer.get_feature_names_out()
    
    # 2. Extract active features (words present in input text)
    non_zero_indices = x_vec.nonzero()[1]
    tfidf_values = x_vec.toarray()[0]
    
    # 3. Extract model weights
    weights = None
    intercept = 0.0
    
    if hasattr(model, "calibrated_classifiers_"):
        # Calibrated SVM
        coefs = []
        for clf in model.calibrated_classifiers_:
            base_est = getattr(clf, "estimator", None) or getattr(clf, "base_estimator", None)
            if base_est and hasattr(base_est, "coef_"):
                coefs.append(base_est.coef_[0])
            elif hasattr(clf, "coef_"):
                coefs.append(clf.coef_[0])
        if coefs:
            weights = np.mean(coefs, axis=0)
        # intercept
        intercepts = []
        for clf in model.calibrated_classifiers_:
            base_est = getattr(clf, "estimator", None) or getattr(clf, "base_estimator", None)
            if base_est and hasattr(base_est, "intercept_"):
                intercepts.append(base_est.intercept_[0])
        if intercepts:
            intercept = float(np.mean(intercepts))
    elif hasattr(model, "coef_"):
        # Logistic Regression
        weights = model.coef_[0]
        intercept = float(model.intercept_[0])
    elif model_name == "Multinomial Naive Bayes" and hasattr(model, "feature_log_prob_"):
        # Naive Bayes
        weights = model.feature_log_prob_[1] - model.feature_log_prob_[0]
        intercept = float(model.class_log_prior_[1] - model.class_log_prior_[0])
        
    # Calculate predicted class and confidence
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(x_vec)[0]
        pred_class = int(np.argmax(probs))
        confidence = float(probs[pred_class])
    else:
        # Fallback if no probabilities (e.g. raw SVM)
        dec = model.decision_function(x_vec)[0]
        # Sigmoid calibration
        prob_1 = 1 / (1 + np.exp(-dec))
        pred_class = 1 if prob_1 >= 0.5 else 0
        confidence = float(prob_1 if pred_class == 1 else 1 - prob_1)
        
    predicted_label = "LIKELY_FAKE" if pred_class == 1 else "LIKELY_GENUINE"
    
    # 4. Compute individual contributions
    contributions = []
    if weights is not None:
        for idx in non_zero_indices:
            word = feature_names[idx]
            tfidf_val = tfidf_values[idx]
            weight = weights[idx]
            contrib = weight * tfidf_val
            
            contributions.append({
                "word": word,
                "weight": float(contrib),
                "tfidf": float(tfidf_val),
                "model_coef": float(weight)
            })
            
    # 5. Split into supporting and opposing features
    # Supporting features: push in the direction of the prediction
    # If prediction is LIKELY_FAKE (class 1), supporting features are those with positive contribution.
    # If prediction is LIKELY_GENUINE (class 0), supporting features are those with negative contribution.
    supporting = []
    opposing = []
    
    for c in contributions:
        # If predicted Fake (1), positive contribution supports, negative opposes
        # If predicted Genuine (0), negative contribution supports, positive opposes
        is_positive = c["weight"] > 0
        if pred_class == 1:
            if is_positive:
                supporting.append(c)
            else:
                opposing.append(c)
        else:
            if not is_positive:
                # Supporting class 0 means pushing negative. Let's flip weight sign for UI representation
                # so that weights shown in charts are positive magnitude values
                c_copy = c.copy()
                c_copy["weight"] = abs(c["weight"])
                supporting.append(c_copy)
            else:
                c_copy = c.copy()
                c_copy["weight"] = abs(c["weight"])
                opposing.append(c_copy)
                
    # Sort supporting and opposing by absolute contribution weight descending
    supporting = sorted(supporting, key=lambda x: abs(x["weight"]), reverse=True)[:max_features]
    opposing = sorted(opposing, key=lambda x: abs(x["weight"]), reverse=True)[:max_features]
    
    return {
        "prediction": predicted_label,
        "confidence": confidence,
        "model_name": model_name,
        "supporting_features": supporting,
        "opposing_features": opposing
    }
