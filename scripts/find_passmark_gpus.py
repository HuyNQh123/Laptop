import urllib.request
import ssl
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
headers = {'User-Agent': 'Mozilla/5.0'}

url = 'https://www.videocardbenchmark.net/gpu_list.php'
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, context=ctx, timeout=12) as r:
    html = r.read().decode('utf-8', errors='ignore')
    print('HTML length:', len(html))
    
    # Check for Iris in lines
    count = 0
    for line in html.splitlines():
        if 'Iris' in line or 'RTX 3050' in line or 'Apple' in line:
            print('Line:', line[:150])
            count += 1
            if count >= 10:
                break
