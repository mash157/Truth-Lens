import asyncio
import json
import urllib.request
import websockets
import subprocess
import tempfile
import shutil

TEST_JS = """
(() => {
  // Check if any element or container can be scrolled
  window.scrollTo(200, 0);
  const scrolledWindow = window.scrollX || document.documentElement.scrollLeft || document.body.scrollLeft;
  window.scrollTo(0, 0);
  
  // Find all scrollable containers in the DOM
  const scrollableContainers = [];
  document.querySelectorAll('*').forEach(el => {
    if (el.scrollWidth > el.clientWidth && el.clientWidth > 0) {
      const style = getComputedStyle(el);
      scrollableContainers.push({
        tag: el.tagName.toLowerCase(),
        className: typeof el.className === 'string' ? el.className.trim() : '',
        id: el.id,
        clientWidth: el.clientWidth,
        scrollWidth: el.scrollWidth,
        overflowX: style.overflowX
      });
    }
  });

  return {
    windowInnerWidth: window.innerWidth,
    docClientW: document.documentElement.clientWidth,
    docScrollW: document.documentElement.scrollWidth,
    bodyClientW: document.body.clientWidth,
    bodyScrollW: document.body.scrollWidth,
    scrolledWindow,
    scrollableContainers
  };
})()
"""

async def main():
    chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    temp_dir = tempfile.mkdtemp(prefix="chrome_test_")
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
            
            await send("Page.navigate", {"url": "http://localhost:5173/"})
            await asyncio.sleep(2)
            res = await send("Runtime.evaluate", {"expression": TEST_JS, "returnByValue": True})
            print(json.dumps(res.get('result', {}).get('value', {}), indent=2))
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except:
            proc.kill()
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    asyncio.run(main())
