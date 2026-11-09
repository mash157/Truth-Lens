from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from backend.app.utils.logging_config import setup_logging
from backend.app.ml.model_loader import artifacts
from backend.app.routes import health, analysis, metrics, model, search


# --------------------------------------------------
# Setup Logging
# --------------------------------------------------

setup_logging()
logger = logging.getLogger(__name__)


# --------------------------------------------------
# FastAPI Application
# --------------------------------------------------

app = FastAPI(
    title="TruthLens API",
    description="Backend API for AI-Based Fake News Classification and Explainable Analysis",
    version="1.0.0"
)


# --------------------------------------------------
# CORS Configuration
# --------------------------------------------------

ALLOWED_ORIGINS = [
    # Production frontend
    "https://truth-lens-omega-nine.vercel.app",

    # Local development (Vite default + common fallback ports)
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:5175",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Startup Event
# --------------------------------------------------

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


# --------------------------------------------------
# Graceful Error Handling
# --------------------------------------------------

@app.exception_handler(Exception)
def general_exception_handler(request: Request, exc: Exception):
    logger.error(
        f"Unhandled server error: {str(exc)}",
        exc_info=True
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": (
                "An unexpected error occurred. "
                "Please contact the administrator or verify configuration."
            )
        }
    )


# --------------------------------------------------
# API Routers
# --------------------------------------------------

app.include_router(
    health.router,
    prefix="/api",
    tags=["health"]
)

app.include_router(
    analysis.router,
    prefix="/api",
    tags=["analysis"]
)

app.include_router(
    metrics.router,
    prefix="/api",
    tags=["metrics"]
)

app.include_router(
    model.router,
    prefix="/api",
    tags=["model"]
)

app.include_router(
    search.router,
    prefix="/api",
    tags=["search"]
)


# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------

@app.get("/")
def read_root():
    return {
        "app": "TruthLens",
        "description": (
            "AI-Based Fake News Classification "
            "and Explainable Analysis System"
        ),
        "version": "1.0.0",
        "health": "/api/health"
    }