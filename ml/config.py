import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = BASE_DIR / "dataset"
RAW_DATA_PATH = DATASET_DIR / "raw" / "WELFake_Dataset.csv"
PROCESSED_DATA_DIR = DATASET_DIR / "processed"
TRAIN_DATA_PATH = PROCESSED_DATA_DIR / "train.csv"
VAL_DATA_PATH = PROCESSED_DATA_DIR / "validation.csv"
TEST_DATA_PATH = PROCESSED_DATA_DIR / "test.csv"

ARTIFACTS_DIR = BASE_DIR / "ml" / "artifacts"
RESULTS_DIR = BASE_DIR / "ml" / "results"

# Create directories if they do not exist
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Training configurations
RANDOM_STATE = 42
TEST_SIZE = 0.15
VAL_SIZE = 0.15  # Out of the remaining 85% train + val

# TF-IDF vectorizer parameters
TFIDF_MAX_FEATURES = 10000  # Reasonable size for performance and presentation
TFIDF_MIN_DF = 2
TFIDF_MAX_DF = 0.95
TFIDF_NGRAM_RANGE = (1, 2)  # Unigrams & bigrams
TFIDF_SUBLINEAR_TF = True
