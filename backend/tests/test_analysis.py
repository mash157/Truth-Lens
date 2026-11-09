import sys
import os
from fastapi.testclient import TestClient

# Add parent directory to path to ensure app can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

client = TestClient(app)

def test_get_sample_articles():
    response = client.get("/api/sample-articles")
    assert response.status_code == 200
    articles = response.json()
    assert len(articles) == 3
    assert articles[0]["title"] is not None
    assert "DEMO ARTICLE" in articles[0]["label"]

def test_analyze_endpoint_validation():
    # Test invalid short text
    response = client.post(
        "/api/analyze",
        json={"title": "Short title", "text": "too short"}
    )
    assert response.status_code == 422
