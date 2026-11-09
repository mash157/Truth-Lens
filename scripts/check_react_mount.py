import asyncio
import json
import urllib.request
import websockets
import subprocess
import tempfile
import shutil

CHECK_DOM = """
(() => {
  return {
    url: window.location.href,
    title: document.title,
    heroDisclaimerText: document.querySelector('.hero-disclaimer')?.innerText,
    heroDisclaimerRect: document.querySelector('.hero-disclaimer')?.getBoundingClientRect()
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
            await send('Emulation.setDeviceMetricsOverride', {'width': 393, 'height': 852, 'deviceScaleFactor': 3, 'mobile': True})
            await send('Page.navigate', {'url': 'http://localhost:5173/'})
            # wait 3 seconds for React to mount
            await asyncio.sleep(3)
            res = await send('Runtime.evaluate', {'expression': CHECK_DOM, 'returnByValue': True})
            print(json.dumps(res.get('result', {}).get('value', {}), indent=2))
    finally:
        proc.terminate()
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == '__main__':
    asyncio.run(main())
