from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from backend.app.services.metrics_service import MetricsService
from backend.app.utils.config import CONFUSION_MATRIX_PATH

router = APIRouter()

@router.get("/metrics")
def get_dashboard_metrics():
    """
    Returns general evaluation metrics, dataset statistics, and model comparisons.
    """
    try:
        dataset_stats = MetricsService.get_dataset_statistics()
    except Exception:
        dataset_stats = None
        
    try:
        eval_metrics = MetricsService.get_model_evaluation_metrics()
    except Exception:
        eval_metrics = None
        
    try:
        model_comparison = MetricsService.get_model_comparison()
    except Exception:
        model_comparison = None
        
    return {
        "dataset_statistics": dataset_stats,
        "evaluation_metrics": eval_metrics,
        "model_comparison": model_comparison
    }

@router.get("/metrics/confusion-matrix")
def get_confusion_matrix_image():
    """
    Serves the confusion matrix plot image.
    """
    import os
    if not os.path.exists(CONFUSION_MATRIX_PATH):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Confusion matrix image not available. Please run training first."
        )
    return FileResponse(CONFUSION_MATRIX_PATH, media_type="image/png")

@router.get("/feature-importance")
def get_global_feature_importance():
    """
    Returns global feature importance coefficients.
    """
    return MetricsService.get_feature_importances()
