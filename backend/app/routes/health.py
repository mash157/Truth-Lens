from fastapi import APIRouter
from backend.app.ml.model_loader import artifacts

router = APIRouter()


@router.get("/health")
def health_check():
    """
    Health-check endpoint for the TruthLens API.

    Intended for:
    - Backend health monitoring
    - Deployment health checks (e.g. Docker, cloud runtimes)
    - Uptime monitoring services (e.g. UptimeRobot)

    Returns HTTP 200 when the backend is reachable.
    The ``model_loaded`` field reflects the real current state of the
    loaded ML artifacts — it is never hardcoded.
    """
    # Attempt loading if not loaded yet (startup should have done this)
    model_loaded = artifacts.is_loaded
    if not model_loaded:
        model_loaded = artifacts.load()

    return {
        "status": "healthy",
        "service": "TruthLens API",
        "version": "1.0.0",
        "model_loaded": model_loaded,
        "model_error": artifacts.error_message if not model_loaded else None,
    }
