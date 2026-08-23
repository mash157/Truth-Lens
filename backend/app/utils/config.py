import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
BACKEND_DIR = BASE_DIR / "backend"

# Server configuration
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# ML Artifact paths
MODEL_PATH = Path(os.getenv("MODEL_PATH", str(BASE_DIR / "ml" / "artifacts" / "best_model.joblib")))
VECTORIZER_PATH = Path(os.getenv("VECTORIZER_PATH", str(BASE_DIR / "ml" / "artifacts" / "tfidf_vectorizer.joblib")))
FEATURE_NAMES_PATH = Path(os.getenv("FEATURE_NAMES_PATH", str(BASE_DIR / "ml" / "artifacts" / "feature_names.joblib")))
MODEL_METADATA_PATH = Path(os.getenv("MODEL_METADATA_PATH", str(BASE_DIR / "ml" / "artifacts" / "model_metadata.json")))

# ML Result paths
DATASET_STATS_PATH = BASE_DIR / "ml" / "results" / "dataset_statistics.json"
METRICS_PATH = BASE_DIR / "ml" / "results" / "metrics.json"
MODEL_COMPARISON_PATH = BASE_DIR / "ml" / "results" / "model_comparison.json"
FEATURE_IMPORTANCE_PATH = BASE_DIR / "ml" / "results" / "feature_importance.json"
CONFUSION_MATRIX_PATH = BASE_DIR / "ml" / "results" / "confusion_matrix.png"

# Serper API (Google Search)
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")
SERPER_API_URL = "https://google.serper.dev/search"
