#!/usr/bin/env python3
"""
End-to-end test for frontend Serper integration.
Tests that the backend endpoints work correctly for the frontend.
"""

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from backend.app.main import app
import backend.app.utils.config as config_module

client = TestClient(app)
results = []

def test(name, passed, detail=""):
    status = "[PASS]" if passed else "[FAIL]"
    results.append({"name": name, "passed": passed, "detail": detail})
    print(f"  {status}  {name}")
    if detail:
        print(f"         {detail}")

print("=" * 60)
print("  FRONTEND SERPER INTEGRATION TEST")
print("=" * 60)

# 1. Analyze endpoint (ML) works
print("\n>> [1] ML Analysis endpoint")
resp = client.post("/api/analyze", json={
    "title": "UN calls for humanitarian pause in Yemen",
    "text": "The United Nations called for a humanitarian pause in Yemen after fighting escalated in the capital."
})
test("ML analyze responds", resp.status_code in [200, 503], f"HTTP {resp.status_code}")

# 2. Search endpoint works
print("\n>> [2] Search endpoint (Serper)")
resp = client.post("/api/search", json={"query": "Reuters technology news", "num_results": 5})
test("Search responds", resp.status_code == 200, f"HTTP {resp.status_code}")
body = resp.json()
test("Search returns results", len(body.get("results", [])) >= 1, f"Count: {len(body.get('results', []))}")

# 3. Verify response format matches frontend expectations
print("\n>> [3] Response format validation")
if resp.status_code == 200:
    for r in body.get("results", []):
        test("Result has 'title'", "title" in r and len(r["title"]) > 0)
        test("Result has 'link'", "link" in r and len(r["link"]) > 0)
        test("Result has 'snippet'", "snippet" in r and len(r["snippet"]) > 0)
        test("Result has 'position'", "position" in r)
        break  # Just check first result

# 4. API key not in search response
print("\n>> [4] Security checks")
resp_text = json.dumps(body)
test("API key NOT in response", config_module.SERPER_API_KEY not in resp_text)

# 5. Empty key returns 503
print("\n>> [5] Error handling")
original = config_module.SERPER_API_KEY
config_module.SERPER_API_KEY = ""
resp = client.post("/api/search", json={"query": "test", "num_results": 3})
test("Empty key returns 503", resp.status_code == 503, f"HTTP {resp.status_code}")
config_module.SERPER_API_KEY = original

# 6. Dashboard endpoints work
print("\n>> [6] Dashboard endpoints")
resp = client.get("/api/metrics")
test("Metrics endpoint", resp.status_code == 200, f"HTTP {resp.status_code}")

resp = client.get("/api/model-info")
test("Model info endpoint", resp.status_code == 200, f"HTTP {resp.status_code}")

resp = client.get("/api/feature-importance")
test("Feature importance endpoint", resp.status_code == 200, f"HTTP {resp.status_code}")

# 7. Health endpoint
print("\n>> [7] Health endpoint")
resp = client.get("/api/health")
test("Health endpoint", resp.status_code == 200, f"HTTP {resp.status_code}")

# Summary
print("\n" + "=" * 60)
passed = sum(1 for r in results if r["passed"])
failed = sum(1 for r in results if not r["passed"])
total = len(results)
print(f"  Total: {total}  |  Passed: {passed}  |  Failed: {failed}")
if failed > 0:
    print("\n  Failed:")
    for r in results:
        if not r["passed"]:
            print(f"    [FAIL] {r['name']} -- {r['detail']}")
    sys.exit(1)
else:
    print("\n  ALL TESTS PASSED")
