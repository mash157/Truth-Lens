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
        chrome, '--headless=new', '--remote-debugging-port=9333',
        f'--user-data-dir={temp_dir}', '--no-first-run', '--no-default-browser-check',
        'http://localhost:5173/'
    ])
    try:
        await asyncio.sleep(2)
        version_info = json.loads(urllib.request.urlopen('http://localhost:9333/json/version').read().decode())
        browser_ws = version_info['webSocketDebuggerUrl']
        
        async with websockets.connect(browser_ws) as ws:
            msg_id = 0
            async def bsend(method, params=None):
                nonlocal msg_id
                msg_id += 1
                await ws.send(json.dumps({'id': msg_id, 'method': method, 'params': params or {}}))
                while True:
                    resp = json.loads(await ws.recv())
                    if resp.get('id') == msg_id: return resp.get('result', {})

            # Create target page
            new_page = await bsend('Target.createTarget', {'url': 'http://localhost:5173/'})
            target_id = new_page['targetId']
            
            # Attach to target
            attached = await bsend('Target.attachToTarget', {'targetId': target_id, 'flatten': True})
            session_id = attached['sessionId']
            
            async def psend(method, params=None):
                nonlocal msg_id
                msg_id += 1
                await ws.send(json.dumps({'id': msg_id, 'sessionId': session_id, 'method': method, 'params': params or {}}))
                while True:
                    resp = json.loads(await ws.recv())
                    if resp.get('id') == msg_id: return resp.get('result', {})

            await psend('Page.enable')
            await psend('Runtime.enable')

            widths = [320, 360, 375, 390, 393, 414, 430]
            routes = ['/', '/analyze', '/dashboard', '/research', '/how-it-works', '/model']

            results = {}
            for r in routes:
                results[r] = {}
                await psend('Page.navigate', {'url': f'http://localhost:5173{r}'})
                await asyncio.sleep(1.2)
                for w in widths:
                    await psend('Emulation.setDeviceMetricsOverride', {'width': w, 'height': 852, 'deviceScaleFactor': 3, 'mobile': True})
                    await asyncio.sleep(0.3)
                    res = await psend('Runtime.evaluate', {'expression': DIAGNOSTIC_JS, 'returnByValue': True})
                    val = res.get('result', {}).get('value', {})
                    dw = val.get('documentWidth')
                    vp = val.get('viewportWidth')
                    passed = (dw == vp)
                    offenders_count = len(val.get('offenders', []))
                    results[r][w] = {
                        'viewport': vp,
                        'document': dw,
                        'body': val.get('bodyWidth'),
                        'passed': passed,
                        'offenders': offenders_count
                    }
                    print(f"[{'PASS' if passed else 'FAIL'}] {r:14} {w}px -> doc={dw}, vp={vp}, offenders={offenders_count}")
                    if offenders_count > 0:
                        for off in val.get('offenders', []):
                            print(f"      OFFENDER: <{off['element']} class='{off['className']}'> left={off['left']}, right={off['right']}")

            print("\nSUMMARY TABLE:")
            print(json.dumps(results, indent=2))
    finally:
        proc.terminate()
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == '__main__':
    asyncio.run(run())
