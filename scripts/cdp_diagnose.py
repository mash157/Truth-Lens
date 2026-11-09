import asyncio
import json
import subprocess
import tempfile
import shutil
import os
import urllib.request
import websockets

DIAGNOSTIC_JS = """
(() => {
  const viewport = document.documentElement.clientWidth;

  const offenders = [...document.querySelectorAll('body *')]
    .map((el) => {
      const rect = el.getBoundingClientRect();
      const style = getComputedStyle(el);

      return {
        element: el.tagName.toLowerCase(),
        className: typeof el.className === 'string' ? el.className.trim() : (el.className?.baseVal || ''),
        id: el.id,
        left: Math.round(rect.left),
        right: Math.round(rect.right),
        width: Math.round(rect.width),
        scrollWidth: el.scrollWidth,
        position: style.position,
        transform: style.transform,
        overflowX: style.overflowX
      };
    })
    .filter((el) =>
      el.width > 0 &&
      (el.left < -1 || el.right > viewport + 1)
    );

  return {
    viewportWidth: viewport,
    documentWidth: document.documentElement.scrollWidth,
    bodyWidth: document.body.scrollWidth,
    horizontalOverflow: document.documentElement.scrollWidth > viewport,
    offenders: offenders.slice(0, 30)
  };
})()
"""

async def run_diagnostic():
    chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    temp_dir = tempfile.mkdtemp(prefix="chrome_overflow_")
    proc = subprocess.Popen([
        chrome,
        "--headless=new",
        "--remote-debugging-port=9222",
        f"--user-data-dir={temp_dir}",
        "--no-first-run",
        "--no-default-browser-check",
        "about:blank"
    ])
    
    try:
        await asyncio.sleep(2)
        req = urllib.request.urlopen("http://localhost:9222/json")
        targets = json.loads(req.read().decode('utf-8'))
        page_target = next(t for t in targets if t.get('type') == 'page')
        ws_url = page_target['webSocketDebuggerUrl']
        
        async with websockets.connect(ws_url) as ws:
            msg_id = 0
            async def send(method, params=None):
                nonlocal msg_id
                msg_id += 1
                await ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
                while True:
                    resp = json.loads(await ws.recv())
                    if resp.get('id') == msg_id:
                        return resp.get('result', {})
            
            # Enable Page & Runtime
            await send("Page.enable")
            await send("Runtime.enable")
            
            # Set viewport to 393x852 (exact iPhone 16 viewport from user screenshot!)
            print("=== TESTING AT 393x852 (USER SCREENSHOT VIEWPORT) ===")
            await send("Emulation.setDeviceMetricsOverride", {
                "width": 393,
                "height": 852,
                "deviceScaleFactor": 3,
                "mobile": True
            })
            
            # Navigate to Home
            await send("Page.navigate", {"url": "http://localhost:5173/"})
            await asyncio.sleep(2)
            
            eval_res = await send("Runtime.evaluate", {
                "expression": DIAGNOSTIC_JS,
                "returnByValue": True
            })
            
            data = eval_res.get('result', {}).get('value', {})
            print(json.dumps(data, indent=2))
            
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except:
            proc.kill()
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    asyncio.run(run_diagnostic())
