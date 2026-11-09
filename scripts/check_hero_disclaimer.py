import asyncio
import json
import urllib.request
import websockets
import subprocess
import tempfile
import shutil

JS = """
(() => {
  const el = document.querySelector('.hero-disclaimer');
  if (!el) return null;
  const rect = el.getBoundingClientRect();
  return {
    rect: {
      left: Math.round(rect.left),
      right: Math.round(rect.right),
      width: Math.round(rect.width)
    },
    scrollWidth: el.scrollWidth,
    clientWidth: el.clientWidth,
    viewport: document.documentElement.clientWidth,
    whiteSpace: getComputedStyle(el).whiteSpace
  };
})()
"""

async def main():
    chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    temp_dir = tempfile.mkdtemp()
    proc = subprocess.Popen([
        chrome, '--headless=new', '--remote-debugging-port=9222',
        f'--user-data-dir={temp_dir}', '--no-first-run', '--no-default-browser-check', 'about:blank'
    ])
    try:
        await asyncio.sleep(2)
        req = urllib.request.urlopen('http://localhost:9222/json')
        targets = json.loads(req.read().decode('utf-8'))
        ws_url = targets[0]['webSocketDebuggerUrl']
        async with websockets.connect(ws_url) as ws:
            msg_id = 0
            async def send(method, params=None):
                nonlocal msg_id
                msg_id += 1
                await ws.send(json.dumps({'id': msg_id, 'method': method, 'params': params or {}}))
                while True:
                    resp = json.loads(await ws.recv())
                    if resp.get('id') == msg_id: return resp.get('result', {})
            await send('Page.enable')
            await send('Runtime.enable')
            
            for w in [320, 360, 375, 390, 393, 414, 430]:
                await send('Emulation.setDeviceMetricsOverride', {'width': w, 'height': 852, 'deviceScaleFactor': 3, 'mobile': True})
                await send('Page.navigate', {'url': 'http://localhost:5173/'})
                await asyncio.sleep(1)
                res = await send('Runtime.evaluate', {'expression': JS, 'returnByValue': True})
                val = res.get('result', {}).get('value', {})
                print(f"Viewport {w}: {val}")
    finally:
        proc.terminate()
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == '__main__':
    asyncio.run(main())
