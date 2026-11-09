import asyncio
import json
import urllib.request
import websockets
import subprocess
import tempfile
import shutil

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
    offenders: offenders
  };
})()
"""

async def main():
    chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    temp_dir = tempfile.mkdtemp(prefix="chrome_diag_")
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
            
            await send("Page.enable")
            await send("Runtime.enable")
            await send("Emulation.setDeviceMetricsOverride", {
                "width": 393,
                "height": 852,
                "deviceScaleFactor": 3,
                "mobile": True
            })
            
            routes = ['/', '/analyze', '/dashboard', '/research', '/how-it-works', '/model']
            for r in routes:
                await send("Page.navigate", {"url": f"http://localhost:5173{r}"})
                await asyncio.sleep(1.5)
                res = await send("Runtime.evaluate", {"expression": DIAGNOSTIC_JS, "returnByValue": True})
                val = res.get('result', {}).get('value', {})
                print(f"=== ROUTE: {r} ===")
                print(f"viewport: {val.get('viewportWidth')}, docWidth: {val.get('documentWidth')}, bodyWidth: {val.get('bodyWidth')}, overflow: {val.get('horizontalOverflow')}")
                offenders = val.get('offenders', [])
                print(f"Offenders count: {len(offenders)}")
                for o in offenders:
                    print(f"  <{o['element']} class='{o['className']}' id='{o['id']}'> left={o['left']} right={o['right']} width={o['width']} pos={o['position']}")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except:
            proc.kill()
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    asyncio.run(main())
