import sys
import os
import json
import ssl
import urllib.request
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding='utf-8')

import laptops_asus_lenovo
import laptops_dell_hp
import laptops_acer_apple_msi_others
import laptops_batch2
import laptops_batch3
import laptops_batch4
from benchmark_data import CPU_BENCHMARKS, GPU_BENCHMARKS

all_raw_laptops = (
    laptops_asus_lenovo.ASUS_LAPTOPS +
    laptops_asus_lenovo.LENOVO_LAPTOPS +
    laptops_dell_hp.DELL_LAPTOPS +
    laptops_dell_hp.HP_LAPTOPS +
    laptops_acer_apple_msi_others.ACER_LAPTOPS +
    laptops_acer_apple_msi_others.APPLE_LAPTOPS +
    laptops_acer_apple_msi_others.MSI_LAPTOPS +
    laptops_acer_apple_msi_others.OTHERS_LAPTOPS +
    laptops_batch2.BATCH2_LAPTOPS +
    laptops_batch3.BATCH3_LAPTOPS +
    laptops_batch4.BATCH4_LAPTOPS
)

# Deduplicate by name
unique_laptops = {}
for item in all_raw_laptops:
    name = item['name'].strip()
    if name not in unique_laptops:
        unique_laptops[name] = item

print(f"Tổng số laptop duy nhất: {len(unique_laptops)}")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7'
}

def test_url(url, expected_keywords=[], forbidden_keywords=[]):
    if not url:
        return {
            'status_code': None,
            'final_url': '',
            'title': '',
            'error': 'URL rỗng',
            'is_valid': False,
            'reason': 'Chưa có URL'
        }
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            code = resp.status
            final_url = resp.geturl()
            content = resp.read(30000).decode('utf-8', errors='ignore')
            m = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
            title = m.group(1).strip() if m else ''
            title_clean = re.sub(r'\s+', ' ', title)
            
            # Check forbidden keywords (e.g. phone keywords on laptop pages)
            content_lower = (title_clean + " " + content[:5000]).lower()
            for fb in forbidden_keywords:
                if fb.lower() in content_lower and not any(k.lower() in content_lower for k in expected_keywords):
                    return {
                        'status_code': code,
                        'final_url': final_url,
                        'title': title_clean,
                        'error': None,
                        'is_valid': False,
                        'reason': f"Phát hiện nội dung sai loại sản phẩm ({fb})"
                    }
            
            # Check if 404 in title or 404 code
            if '404' in title_clean or 'không tìm thấy' in title_clean.lower() or 'not found' in title_clean.lower():
                return {
                    'status_code': 404,
                    'final_url': final_url,
                    'title': title_clean,
                    'error': '404 in page title',
                    'is_valid': False,
                    'reason': 'Trang báo lỗi 404 / Không tìm thấy sản phẩm'
                }

            return {
                'status_code': code,
                'final_url': final_url,
                'title': title_clean,
                'error': None,
                'is_valid': True,
                'reason': 'Hợp lệ'
            }
    except urllib.error.HTTPError as e:
        return {
            'status_code': e.code,
            'final_url': url,
            'title': '',
            'error': f'HTTP Error {e.code}',
            'is_valid': False,
            'reason': f'Lỗi HTTP {e.code}'
        }
    except urllib.error.URLError as e:
        return {
            'status_code': None,
            'final_url': url,
            'title': '',
            'error': str(e.reason),
            'is_valid': False,
            'reason': f'Lỗi kết nối ({e.reason})'
        }
    except Exception as e:
        return {
            'status_code': None,
            'final_url': url,
            'title': '',
            'error': str(e),
            'is_valid': False,
            'reason': f'Lỗi kiểm tra ({str(e)})'
        }

if __name__ == '__main__':
    # Test sample
    print("Testing sample verification...")
    res = test_url('https://cellphones.com.vn/macbook-air-2020-m1.html', expected_keywords=['macbook'], forbidden_keywords=['iphone'])
    print(res)
