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

async def run():
    chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    temp_dir = tempfile.mkdtemp()
    proc = subprocess.Popen([
        chrome, '--headless=new', '--remote-debugging-port=9222',
        f'--user-data-dir={temp_dir}', '--no-first-run', '--no-default-browser-check',
        '--disable-extensions', 'http://localhost:5173/'
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
            
            widths = [320, 360, 375, 390, 393, 414, 430]
            routes = ['/', '/analyze', '/dashboard', '/research', '/how-it-works', '/model']
            
            summary = {}
            for r in routes:
                summary[r] = {}
                await send('Page.navigate', {'url': f'http://localhost:5173{r}'})
                await asyncio.sleep(1.2)
                for w in widths:
                    await send('Emulation.setDeviceMetricsOverride', {'width': w, 'height': 852, 'deviceScaleFactor': 3, 'mobile': True})
                    await asyncio.sleep(0.3)
                    res = await send('Runtime.evaluate', {'expression': DIAGNOSTIC_JS, 'returnByValue': True})
                    val = res.get('result', {}).get('value', {})
                    dw = val.get('documentWidth')
                    vp = val.get('viewportWidth')
                    passed = (dw == vp)
                    offenders_count = len(val.get('offenders', []))
                    summary[r][w] = {
                        'passed': passed,
                        'doc': dw,
                        'vp': vp,
                        'offenders': offenders_count
                    }
                    print(f"Route {r} @ {w}px -> passed: {passed}, docWidth: {dw}, viewport: {vp}, offenders: {offenders_count}")
                    
            print("\nFINAL SUMMARY:")
            print(json.dumps(summary, indent=2))
    finally:
        proc.terminate()
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == '__main__':
    asyncio.run(run())
