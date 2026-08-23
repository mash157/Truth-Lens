import sys
import os

# Add parent directory to path to ensure app can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.explainer import ExplainerService

def test_explainer_with_empty_text():
    result = ExplainerService.explain("", "LIKELY_FAKE")
    assert "supporting_features" in result
    assert "opposing_features" in result
    assert len(result["supporting_features"]) == 0
    assert len(result["opposing_features"]) == 0
