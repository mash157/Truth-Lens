import asyncio
import json
import urllib.request
import websockets
import subprocess
import tempfile
import shutil
import base64
import os

async def capture_screenshots():
    chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    temp_dir = tempfile.mkdtemp()
    out_dir = r'C:\Users\USER\Downloads\Truth-Lens-master\Truth-Lens-master\screenshots'
    os.makedirs(out_dir, exist_ok=True)
    
    proc = subprocess.Popen([
        chrome, '--headless=new', '--remote-debugging-port=9333',
        f'--user-data-dir={temp_dir}', '--no-first-run', '--no-default-browser-check',
        'http://localhost:5173/'
    ])
    try:
        await asyncio.sleep(2)
        version_info = json.loads(urllib.request.urlopen('http://localhost:9333/json/version').read().decode())
        browser_ws = version_info['webSocketDebuggerUrl']
        
        async with websockets.connect(browser_ws, max_size=10 * 1024 * 1024) as ws:
            msg_id = 0
            async def bsend(method, params=None):
                nonlocal msg_id
                msg_id += 1
                await ws.send(json.dumps({'id': msg_id, 'method': method, 'params': params or {}}))
                while True:
                    resp = json.loads(await ws.recv())
                    if resp.get('id') == msg_id: return resp.get('result', {})

            new_page = await bsend('Target.createTarget', {'url': 'http://localhost:5173/'})
            target_id = new_page['targetId']
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

            # 1. iPhone 16 (393x852) - Home Light Mode
            await psend('Emulation.setDeviceMetricsOverride', {'width': 393, 'height': 852, 'deviceScaleFactor': 3, 'mobile': True})
            await psend('Page.navigate', {'url': 'http://localhost:5173/'})
            await asyncio.sleep(1.5)
            shot = await psend('Page.captureScreenshot', {'format': 'png'})
            with open(os.path.join(out_dir, 'mobile-home-393px-light.png'), 'wb') as f:
                f.write(base64.b64decode(shot['data']))
            print('Saved mobile-home-393px-light.png')

            # 2. iPhone 16 (393x852) - Home Dark Mode
            await psend('Runtime.evaluate', {'expression': "document.documentElement.classList.add('dark')"})
            await asyncio.sleep(0.5)
            shot = await psend('Page.captureScreenshot', {'format': 'png'})
            with open(os.path.join(out_dir, 'mobile-home-393px-dark.png'), 'wb') as f:
                f.write(base64.b64decode(shot['data']))
            print('Saved mobile-home-393px-dark.png')

            # 3. 320px ultra-small viewport
            await psend('Runtime.evaluate', {'expression': "document.documentElement.classList.remove('dark')"})
            await psend('Emulation.setDeviceMetricsOverride', {'width': 320, 'height': 600, 'deviceScaleFactor': 2, 'mobile': True})
            await asyncio.sleep(0.5)
            shot = await psend('Page.captureScreenshot', {'format': 'png'})
            with open(os.path.join(out_dir, 'mobile-home-320px-light.png'), 'wb') as f:
                f.write(base64.b64decode(shot['data']))
            print('Saved mobile-home-320px-light.png')

            # 4. Desktop (1440x900)
            await psend('Emulation.setDeviceMetricsOverride', {'width': 1440, 'height': 900, 'deviceScaleFactor': 1, 'mobile': False})
            await psend('Page.navigate', {'url': 'http://localhost:5173/'})
            await asyncio.sleep(1.5)
            shot = await psend('Page.captureScreenshot', {'format': 'png'})
            with open(os.path.join(out_dir, 'desktop-home-1440px.png'), 'wb') as f:
                f.write(base64.b64decode(shot['data']))
            print('Saved desktop-home-1440px.png')

            # 5. Mobile Analyze Page (393x852)
            await psend('Emulation.setDeviceMetricsOverride', {'width': 393, 'height': 852, 'deviceScaleFactor': 3, 'mobile': True})
            await psend('Page.navigate', {'url': 'http://localhost:5173/analyze'})
            await asyncio.sleep(1.5)
            shot = await psend('Page.captureScreenshot', {'format': 'png'})
            with open(os.path.join(out_dir, 'mobile-analyze-393px.png'), 'wb') as f:
                f.write(base64.b64decode(shot['data']))
            print('Saved mobile-analyze-393px.png')

    finally:
        proc.terminate()
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == '__main__':
    asyncio.run(capture_screenshots())
