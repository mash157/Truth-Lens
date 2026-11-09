from fastapi import APIRouter, HTTPException, status
import os
import json
from backend.app.utils.config import MODEL_METADATA_PATH

router = APIRouter()

@router.get("/model-info")
def get_model_info():
    """
    Returns metadata about the selected best model and training configurations.
    """
    if not os.path.exists(MODEL_METADATA_PATH):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model metadata not found. Please run training first."
        )
    try:
        with open(MODEL_METADATA_PATH, 'r') as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error reading model metadata: {str(e)}"
        )
