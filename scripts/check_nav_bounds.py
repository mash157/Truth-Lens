import asyncio
import json
import urllib.request
import websockets
import subprocess
import tempfile
import shutil

JS = """
(() => {
  const brand = document.querySelector('.brand');
  const toggle = document.querySelector('.theme-toggle');
  const menuBtn = document.querySelector('.menu-button');
  const navMobile = document.querySelector('.nav-mobile');
  const navInner = document.querySelector('.nav-inner');
  const siteNav = document.querySelector('.site-nav');
  return {
    viewport: document.documentElement.clientWidth,
    siteNavRect: siteNav ? siteNav.getBoundingClientRect() : null,
    navInnerRect: navInner ? navInner.getBoundingClientRect() : null,
    brandRect: brand ? brand.getBoundingClientRect() : null,
    toggleRect: toggle ? toggle.getBoundingClientRect() : null,
    menuBtnRect: menuBtn ? menuBtn.getBoundingClientRect() : null,
    navMobileRect: navMobile ? navMobile.getBoundingClientRect() : null,
  };
})()
"""

async def main():
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
            for w in [320, 360, 375, 393]:
                await send('Emulation.setDeviceMetricsOverride', {'width': w, 'height': 852, 'deviceScaleFactor': 3, 'mobile': True})
                await asyncio.sleep(0.5)
                res = await send('Runtime.evaluate', {'expression': JS, 'returnByValue': True})
                val = res.get('result', {}).get('value', {})
                print(f"=== Viewport {w} ===")
                print(f"  brand right: {val['brandRect']['right']}")
                print(f"  toggle left: {val['toggleRect']['left']}, right: {val['toggleRect']['right']}")
                print(f"  menuBtn right: {val['menuBtnRect']['right']}")
    finally:
        proc.terminate()
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == '__main__':
    asyncio.run(main())
