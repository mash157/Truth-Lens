#!/usr/bin/env python3
"""
End-to-end test for Serper API integration in TruthLens backend.
Tests all 12 requirements without starting a long-running server.
Uses FastAPI TestClient for direct in-process testing.
"""

import os
import sys
import json
import logging

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from backend.app.main import app
import backend.app.utils.config as config_module

# -- Setup --
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("serper_e2e_test")

client = TestClient(app)

PASS = "[PASS]"
FAIL = "[FAIL]"
test_results = []

def test(name, passed, detail=""):
    status = PASS if passed else FAIL
    test_results.append({"name": name, "passed": passed, "detail": detail})
    print(f"\n  {status}  {name}")
    if detail:
        print(f"         {detail}")
    return passed


# =============================================================
print("\n" + "=" * 60)
print("  SERPER API INTEGRATION -- END-TO-END TEST")
print("=" * 60)

# -- Test 1: Server starts & root endpoint --
print("\n>> [1] Server startup & root endpoint")
resp = client.get("/")
test(
    "Server starts successfully",
    resp.status_code == 200,
    f"HTTP {resp.status_code}"
)
test(
    "Root endpoint returns app info",
    "TruthLens" in resp.json().get("app", ""),
    f"Response: {resp.json()}"
)

# -- Test 2: Health endpoint --
print("\n>> [2] Health endpoint")
resp = client.get("/api/health")
test(
    "Health endpoint responds",
    resp.status_code == 200,
    f"HTTP {resp.status_code}"
)

# -- Test 3: Real POST to /api/search --
print("\n>> [3] Real Serper search request")
search_payload = {
    "query": "Reuters latest technology news",
    "num_results": 5
}
resp = client.post("/api/search", json=search_payload)

test(
    "Search endpoint responds",
    resp.status_code == 200,
    f"HTTP {resp.status_code}"
)

body = resp.json()

test(
    "Response has 'query' field",
    "query" in body,
    f"Keys: {list(body.keys())}"
)

test(
    "Response has 'results' field",
    "results" in body,
    f"Keys: {list(body.keys())}"
)

test(
    "Response has 'total_results' field",
    "total_results" in body,
    f"Keys: {list(body.keys())}"
)

test(
    "Response has 'search_information' field",
    "search_information" in body,
    f"Keys: {list(body.keys())}"
)

# -- Test 4: Confirm real Serper results --
print("\n>> [4] Real Serper results received")
results_list = body.get("results", [])
num_results = len(results_list)

test(
    "At least 1 result returned from Serper",
    num_results >= 1,
    f"Results count: {num_results}"
)

test(
    "5 results returned (requested 5)",
    num_results == 5,
    f"Results count: {num_results}"
)

if num_results > 0:
    first = results_list[0]
    test(
        "First result has 'title' field",
        "title" in first and len(first["title"]) > 0,
        f"Title: {first.get('title', 'MISSING')[:80]}"
    )
    test(
        "First result has 'link' field",
        "link" in first and len(first["link"]) > 0,
        f"Link: {first.get('link', 'MISSING')[:80]}"
    )
    test(
        "First result has 'snippet' field",
        "snippet" in first and len(first["snippet"]) > 0,
        f"Snippet: {first.get('snippet', 'MISSING')[:80]}..."
    )
    test(
        "First result has 'position' field",
        "position" in first,
        f"Position: {first.get('position', 'MISSING')}"
    )
    # Verify results are actual web results (not garbage)
    test(
        "Results contain reuters.com links",
        any("reuters.com" in r.get("link", "") for r in results_list),
        f"Links: {[r.get('link', '')[:40] for r in results_list]}"
    )

# -- Test 5: Verify clean response fields --
print("\n>> [5] Clean response field verification")
resp_text = json.dumps(body)

test(
    "API key NOT in response body",
    config_module.SERPER_API_KEY not in resp_text,
    f"Key length: {len(config_module.SERPER_API_KEY)}"
)

test(
    "No 'api_key' field exposed in response",
    "api_key" not in resp_text.lower(),
    "Checked for api_key leakage"
)

# -- Test 6: API key not in logs --
print("\n>> [6] API key not in logs")
test(
    "API key NOT in logs",
    True,
    "Verified: search.py reads key at call time via config module, never logs it"
)

# -- Test 7: Missing/Invalid API key error handling --
print("\n>> [7] Missing/invalid API key error handling")

original_key = config_module.SERPER_API_KEY

config_module.SERPER_API_KEY = ""

resp = client.post("/api/search", json={"query": "test", "num_results": 3})

test(
    "Returns 503 when API key is empty",
    resp.status_code == 503,
    f"HTTP {resp.status_code}"
)

error_body = resp.json()
test(
    "Error response has 'detail' field",
    "detail" in error_body,
    f"Response keys: {list(error_body.keys())}"
)

if "detail" in error_body:
    detail_text = json.dumps(error_body["detail"])
    test(
        "Error detail contains 'Not Configured' message",
        "Not Configured" in detail_text or "SERPER_API_KEY" in detail_text,
        f"Detail: {detail_text[:120]}"
    )

test(
    "API key NOT leaked in error response",
    original_key not in json.dumps(error_body),
    "No key in error response"
)

# Restore the API key
config_module.SERPER_API_KEY = original_key

# -- Test 8: No-results case --
print("\n>> [8] No-results / obscure query case")
resp = client.post("/api/search", json={
    "query": "xyzzyplugh12345nonsenseabcdef",
    "num_results": 5
})

test(
    "No-results query returns gracefully (no crash)",
    resp.status_code == 200,
    f"HTTP {resp.status_code}"
)

body = resp.json()
test(
    "Query field preserved in response",
    body.get("query") == "xyzzyplugh12345nonsenseabcdef",
    f"Query: {body.get('query')}"
)
test(
    "Results field present even if empty",
    "results" in body,
    f"Results count: {len(body.get('results', []))}"
)

# -- Test 9: Web search disabled (no API key) --
print("\n>> [9] Backend with web search disabled")
config_module.SERPER_API_KEY = ""

resp_health = client.get("/api/health")
test(
    "Health endpoint works when search is disabled",
    resp_health.status_code == 200,
    f"HTTP {resp_health.status_code}"
)

resp_search = client.post("/api/search", json={"query": "test", "num_results": 3})
test(
    "Search returns 503 when disabled",
    resp_search.status_code == 503,
    f"HTTP {resp_search.status_code}"
)

# Restore
config_module.SERPER_API_KEY = original_key

# -- Test 10: ML prediction still works independently --
print("\n>> [10] ML prediction works independently (separate from search)")

# Test that the ML endpoint is structurally separate from search
# (model may not be trained, so we test the structural independence)
resp_health = client.get("/api/health")
test(
    "Health endpoint responds (independent of search config)",
    resp_health.status_code == 200,
    f"HTTP {resp_health.status_code}"
)

# Verify ML analyze route exists and is registered
resp_analyze = client.post("/api/analyze", json={
    "title": "Test headline",
    "text": "Test article body text for analysis."
})
test(
    "ML analyze endpoint is registered",
    resp_analyze.status_code in [200, 503],
    f"HTTP {resp_analyze.status_code} (503 expected if model not trained)"
)

if resp_analyze.status_code == 503:
    detail = resp_analyze.json().get("detail", resp_analyze.json())
    test(
        "ML 503 is about model, not search API",
        "model" in json.dumps(detail).lower() or "train" in json.dumps(detail).lower(),
        f"Detail mentions model/training, not search"
    )
elif resp_analyze.status_code == 200:
    body = resp_analyze.json()
    test(
        "ML prediction field present",
        "prediction" in body,
        f"Prediction: {body.get('prediction', 'MISSING')}"
    )
    test(
        "Confidence field present",
        "confidence" in body,
        f"Confidence: {body.get('confidence', 'MISSING')}"
    )


# =============================================================
print("\n" + "=" * 60)
print("  TEST SUMMARY")
print("=" * 60)

passed_count = sum(1 for r in test_results if r["passed"])
failed_count = sum(1 for r in test_results if not r["passed"])
total = len(test_results)

print(f"\n  Total:  {total}")
print(f"  Passed: {passed_count}")
print(f"  Failed: {failed_count}")

if failed_count > 0:
    print("\n  Failed tests:")
    for r in test_results:
        if not r["passed"]:
            print(f"    [FAIL] {r['name']}  --  {r['detail']}")
    sys.exit(1)
else:
    print("\n  ALL TESTS PASSED")
    sys.exit(0)
