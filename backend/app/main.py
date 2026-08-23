from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from backend.app.utils.logging_config import setup_logging
from backend.app.ml.model_loader import artifacts
from backend.app.routes import health, analysis, metrics, model

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="TruthLens API",
    description="Backend API for AI-Based Fake News Classification and Explainable Analysis",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, restrict to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup Event
@app.on_event("startup")
def startup_event():
    logger.info("Application starting up...")
    # Load model artifacts once at startup
    loaded = artifacts.load()
    if loaded:
        logger.info("Successfully loaded ML models on startup.")
    else:
        logger.warning(
            "Failed to load ML models on startup. "
            "Please ensure model has been trained by running scripts/train.py"
        )

# Graceful Error Handling
@app.exception_handler(Exception)
def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled server error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please contact the administrator or verify configuration."
        }
    )

# Include Routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(analysis.router, prefix="/api", tags=["analysis"])
app.include_router(metrics.router, prefix="/api", tags=["metrics"])
app.include_router(model.router, prefix="/api", tags=["model"])

@app.get("/")
def read_root():
    return {
        "app": "TruthLens",
        "description": "AI-Based Fake News Classification and Explainable Analysis System",
        "version": "1.0.0",
        "health": "/api/health"
    }
