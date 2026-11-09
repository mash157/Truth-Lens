import os
import joblib
import json
import logging
from pathlib import Path
from backend.app.utils.config import (
    MODEL_PATH,
    VECTORIZER_PATH,
    MODEL_METADATA_PATH
)

logger = logging.getLogger(__name__)

class ModelArtifacts:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.metadata = None
        self._loaded = False
        self._error = None

    def load(self):
        """
        Loads model and vectorizer from the artifact folder.
        """
        if self._loaded:
            return True

        logger.info("Initializing Model Loader...")
        
        # Verify paths exist
        if not os.path.exists(MODEL_PATH):
            self._error = f"Model file not found at {MODEL_PATH}. Please run training first."
            logger.warning(self._error)
            return False
            
        if not os.path.exists(VECTORIZER_PATH):
            self._error = f"Vectorizer file not found at {VECTORIZER_PATH}. Please run training first."
            logger.warning(self._error)
            return False
            
        try:
            logger.info(f"Loading best model from {MODEL_PATH}...")
            self.model = joblib.load(MODEL_PATH)
            
            logger.info(f"Loading TF-IDF vectorizer from {VECTORIZER_PATH}...")
            self.vectorizer = joblib.load(VECTORIZER_PATH)
            
            if os.path.exists(MODEL_METADATA_PATH):
                logger.info(f"Loading model metadata from {MODEL_METADATA_PATH}...")
                with open(MODEL_METADATA_PATH, 'r') as f:
                    self.metadata = json.load(f)
            else:
                self.metadata = {"best_model_name": "Unknown Model"}
                
            self._loaded = True
            self._error = None
            logger.info("Model artifacts loaded successfully.")
            return True
            
        except Exception as e:
            self._error = f"Error loading artifacts: {str(e)}"
            logger.error(self._error)
            return False

    @property
    def is_loaded(self):
        return self._loaded

    @property
    def error_message(self):
        return self._error

# Global instance
artifacts = ModelArtifacts()
