import sys
import os
import pytest
from fastapi import HTTPException

# Add parent directory to path to ensure app can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.predictor import PredictorService

def test_predictor_empty_input():
    with pytest.raises(HTTPException) as excinfo:
        PredictorService.predict("", "    ")
    assert excinfo.value.status_code == 422
