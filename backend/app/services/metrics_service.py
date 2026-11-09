import json
import os
from fastapi import HTTPException, status
from backend.app.utils.config import (
    DATASET_STATS_PATH,
    METRICS_PATH,
    MODEL_COMPARISON_PATH,
    FEATURE_IMPORTANCE_PATH
)

class MetricsService:
    @staticmethod
    def get_dataset_statistics():
        if not os.path.exists(DATASET_STATS_PATH):
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Dataset statistics not available. Please run data preparation first."
            )
        try:
            with open(DATASET_STATS_PATH, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error reading dataset statistics: {str(e)}"
            )

    @staticmethod
    def get_model_evaluation_metrics():
        if not os.path.exists(METRICS_PATH):
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Model evaluation metrics not available. Please run training and evaluation first."
            )
        try:
            with open(METRICS_PATH, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error reading model evaluation metrics: {str(e)}"
            )

    @staticmethod
    def get_model_comparison():
        if not os.path.exists(MODEL_COMPARISON_PATH):
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Model comparison data not available. Please run training first."
            )
        try:
            with open(MODEL_COMPARISON_PATH, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error reading model comparison: {str(e)}"
            )

    @staticmethod
    def get_feature_importances():
        if not os.path.exists(FEATURE_IMPORTANCE_PATH):
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Global feature importances not available. Please run training first."
            )
        try:
            with open(FEATURE_IMPORTANCE_PATH, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error reading feature importances: {str(e)}"
            )
