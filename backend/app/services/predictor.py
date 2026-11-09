import numpy as np
from fastapi import HTTPException, status
from backend.app.ml.model_loader import artifacts
from backend.app.ml.preprocessing import combine_headline_and_body

class PredictorService:
    @staticmethod
    def predict(title: str, text: str):
        # 1. Ensure artifacts are loaded
        if not artifacts.is_loaded:
            success = artifacts.load()
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail={
                        "error": "Model Not Trained",
                        "message": "The TruthLens classification models are not trained yet. "
                                   "Please run 'python scripts/train.py' in the terminal to train the models first."
                    }
                )
        
        # 2. Preprocess and combine input
        combined_text = combine_headline_and_body(title, text)
        if not combined_text.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Input text contains no usable word features after preprocessing."
            )
            
        model = artifacts.model
        vectorizer = artifacts.vectorizer
        model_name = artifacts.metadata.get("best_model_name", "Classification Model")
        uncertainty_threshold = artifacts.metadata.get("uncertainty_threshold", 0.55)
        
        # 3. Vectorize text
        vec_text = vectorizer.transform([combined_text])
        
        # 4. Predict
        preds = model.predict(vec_text)
        pred_class = int(preds[0])
        
        # 5. Determine calibrated probabilities and confidence
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(vec_text)[0]
            confidence = float(probs[pred_class])
            max_prob = float(max(probs))
        else:
            # Fallback sigmoid calibration
            dec = model.decision_function(vec_text)[0]
            prob_1 = 1 / (1 + np.exp(-dec))
            confidence = float(prob_1 if pred_class == 1 else 1 - prob_1)
            max_prob = confidence
        
        # 6. Uncertainty detection
        is_uncertain = max_prob < uncertainty_threshold
        
        if is_uncertain:
            prediction_label = "UNCERTAIN"
        else:
            prediction_label = "LIKELY_FAKE" if pred_class == 1 else "LIKELY_GENUINE"
        
        return {
            "prediction": prediction_label,
            "confidence": confidence,
            "model_name": model_name,
            "combined_text": combined_text,
            "uncertainty": is_uncertain,
            "max_probability": max_prob
        }
