#!/usr/bin/env python3
"""
Simulates browser requests to verify the frontend-backend connection.
Tests exactly what the browser would send via Vite proxy.
"""

import sys
import os
import json
import time
import threading
import subprocess

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import httpx

BACKEND = "http://127.0.0.1:8000"
results = []

def test(name, passed, detail=""):
    status = "[PASS]" if passed else "[FAIL]"
    results.append({"name": name, "passed": passed, "detail": detail})
    print(f"  {status}  {name}")
    if detail:
        print(f"         {detail}")

print("=" * 60)
print("  BROWSER CONNECTION SIMULATION TEST")
print("=" * 60)

# Test 1: Backend is reachable
print("\n>> [1] Backend health check")
try:
    resp = httpx.get(f"{BACKEND}/api/health", timeout=5)
    test("Backend is reachable", resp.status_code == 200, f"HTTP {resp.status_code}")
    data = resp.json()
    test("Model is loaded", data.get("model_loaded") == True, f"model_loaded: {data.get('model_loaded')}")
except Exception as e:
    test("Backend is reachable", False, str(e))
    print("\n  Cannot continue without backend. Please start: python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000")
    sys.exit(1)

# Test 2: Analyze with exact browser-like request (what Vite proxy would forward)
print("\n>> [2] POST /api/analyze (simulating browser via Vite proxy)")
headers = {
    "Content-Type": "application/json",
    "Origin": "http://localhost:5173",  # What Vite dev server would send
    "Referer": "http://localhost:5173/analyze",
}
payload = {
    "title": "China says resolutely opposes deployment of THAAD in South Korea",
    "text": "BEIJING (Reuters) - China said on Friday it resolutely opposes deployment of a U.S. anti-missile defense system in South Korea."
}
try:
    resp = httpx.post(f"{BACKEND}/api/analyze", json=payload, headers=headers, timeout=30)
    test("POST /api/analyze succeeds", resp.status_code == 200, f"HTTP {resp.status_code}")
    data = resp.json()
    test("Has prediction field", "prediction" in data, f"prediction: {data.get('prediction')}")
    test("Prediction is LIKELY_GENUINE", data.get("prediction") == "LIKELY_GENUINE", f"prediction: {data.get('prediction')}")
    test("Has confidence field", "confidence" in data, f"confidence: {data.get('confidence')}")
    test("Confidence ~99.78%", abs(data.get("confidence", 0) - 0.9978) < 0.01, f"confidence: {data.get('confidence')}")
except Exception as e:
    test("POST /api/analyze succeeds", False, str(e))

# Test 3: CORS headers check
print("\n>> [3] CORS preflight check")
try:
    resp = httpx.options(
        f"{BACKEND}/api/analyze",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type",
        },
        timeout=5,
    )
    allow_origin = resp.headers.get("access-control-allow-origin", "")
    test("CORS allows localhost:5173", "localhost:5173" in allow_origin, f"Access-Control-Allow-Origin: {allow_origin}")
except Exception as e:
    test("CORS preflight check", False, str(e))

# Test 4: Dashboard endpoints
print("\n>> [4] Dashboard API endpoints")
for endpoint in ["/api/metrics", "/api/model-info", "/api/feature-importance"]:
    try:
        resp = httpx.get(f"{BACKEND}{endpoint}", timeout=5)
        test(f"GET {endpoint}", resp.status_code == 200, f"HTTP {resp.status_code}")
    except Exception as e:
        test(f"GET {endpoint}", False, str(e))

# Test 5: Search endpoint (Serper)
print("\n>> [5] Search endpoint (Serper)")
try:
    resp = httpx.post(
        f"{BACKEND}/api/search",
        json={"query": "Reuters technology news", "num_results": 5},
        headers={"Content-Type": "application/json"},
        timeout=15,
    )
    test("POST /api/search succeeds", resp.status_code == 200, f"HTTP {resp.status_code}")
    data = resp.json()
    test("Search returns results", len(data.get("results", [])) >= 1, f"Count: {len(data.get('results', []))}")
except Exception as e:
    test("POST /api/search succeeds", False, str(e))

# Test 6: Confusion matrix image
print("\n>> [6] Confusion matrix image")
try:
    resp = httpx.get(f"{BACKEND}/api/metrics/confusion-matrix", timeout=5)
    test("GET confusion matrix", resp.status_code == 200, f"HTTP {resp.status_code}, content-type: {resp.headers.get('content-type', 'unknown')}")
except Exception as e:
    test("GET confusion matrix", False, str(e))

# Test 7: Root endpoint
print("\n>> [7] Root endpoint")
try:
    resp = httpx.get(f"{BACKEND}/", timeout=5)
    test("GET /", resp.status_code == 200, f"HTTP {resp.status_code}")
except Exception as e:
    test("GET /", False, str(e))

# Test 8: API key security
print("\n>> [8] Security")
from backend.app.utils.config import SERPER_API_KEY
try:
    resp = httpx.post(
        f"{BACKEND}/api/search",
        json={"query": "test", "num_results": 3},
        timeout=15,
    )
    resp_text = resp.text
    test("API key not in response", SERPER_API_KEY not in resp_text)
except Exception as e:
    test("API key check", False, str(e))

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
    print("\n  Backend endpoints verified and ready for browser connection.")
