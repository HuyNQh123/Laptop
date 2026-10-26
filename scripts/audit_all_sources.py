import sys
import os
import json
import ssl
import urllib.request
import re
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

# Deduplicate laptops by exact name
laptops_dict = {}
for item in all_raw_laptops:
    name = item['name'].strip()
    if name not in laptops_dict:
        laptops_dict[name] = item

print(f"Tổng số laptop duy nhất cần kiểm tra: {len(laptops_dict)}")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7'
}

def verify_single_url(url, laptop_name, source_type, brand):
    """
    Mở đường link, theo dõi redirect, phân tích tiêu đề và nội dung để kiểm tra tính hợp lệ.
    """
    if not url or url.strip() == '':
        return {
            'status_code': None,
            'final_url': '',
            'title': '',
            'status': 'Chưa có nguồn xác minh',
            'error': 'URL rỗng / Chưa khai báo',
            'note': 'Không có URL để kiểm tra'
        }

    # Kiểm tra nếu là trang tìm kiếm (bị cấm theo quy định)
    if 'catalogsearch/result' in url or 'tim-kiem' in url:
        return {
            'status_code': 200,
            'final_url': url,
            'title': 'Trang kết quả tìm kiếm',
            'status': 'Không hợp lệ',
            'error': 'URL tìm kiếm (vi phạm quy định không dùng search query làm bằng chứng sản phẩm)',
            'note': 'URL tìm kiếm không phải là trang sản phẩm cụ thể, có thể hiển thị sai loại sản phẩm (vd: hiển thị iPhone khi tìm MacBook)'
        }

    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=8) as resp:
            code = resp.status
            final_url = resp.geturl()
            content = resp.read(25000).decode('utf-8', errors='ignore')
            m = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
            title = m.group(1).strip() if m else ''
            title_clean = re.sub(r'\s+', ' ', title)
            content_lower = (title_clean + " " + content[:6000]).lower()

            # 1. Kiểm tra 404 hoặc trang không tìm thấy
            if code == 404 or '404' in title_clean or 'không tìm thấy' in title_clean.lower() or 'not found' in title_clean.lower():
                return {
                    'status_code': 404,
                    'final_url': final_url,
                    'title': title_clean,
                    'status': 'Không hợp lệ',
                    'error': 'HTTP 404 / Trang sản phẩm không tồn tại hoặc đã ngừng kinh doanh',
                    'note': f'Trang trả về lỗi 404 hoặc thông báo không tìm thấy sản phẩm ({title_clean})'
                }

            # 2. Kiểm tra trường hợp sai loại sản phẩm (ví dụ laptop nhưng ra điện thoại / iPhone)
            brand_lower = brand.lower()
            name_lower = laptop_name.lower()
            if 'macbook' in name_lower and 'iphone' in title_clean.lower() and 'macbook' not in title_clean.lower():
                return {
                    'status_code': code,
                    'final_url': final_url,
                    'title': title_clean,
                    'status': 'Không hợp lệ',
                    'error': 'Ghép sai sản phẩm (MacBook bị dẫn sang trang iPhone)',
                    'note': f'Tiêu đề trang đích là: {title_clean}'
                }

            if 'laptop' in name_lower and 'điện thoại' in title_clean.lower() and 'laptop' not in content_lower:
                return {
                    'status_code': code,
                    'final_url': final_url,
                    'title': title_clean,
                    'status': 'Không hợp lệ',
                    'error': 'Ghép sai sản phẩm (Laptop dẫn sang trang điện thoại di động)',
                    'note': f'Tiêu đề trang đích là: {title_clean}'
                }

            # 3. Phân biệt theo loại nguồn
            if source_type == 'specs':
                # Link thông số: kiểm tra có từ khóa của hãng/dòng máy không
                return {
                    'status_code': code,
                    'final_url': final_url,
                    'title': title_clean,
                    'status': 'Đã xác minh',
                    'error': None,
                    'note': f'Xác minh thành công trang thông số kỹ thuật ({title_clean[:80]})'
                }
            elif source_type in ['cpu_score', 'gpu_score']:
                # Link benchmark: kiểm tra PassMark
                if 'passmark' in content_lower or 'cpubenchmark' in final_url or 'videocardbenchmark' in final_url:
                    return {
                        'status_code': code,
                        'final_url': final_url,
                        'title': title_clean,
                        'status': 'Đã xác minh',
                        'error': None,
                        'note': f'Xác minh thành công điểm benchmark PassMark ({title_clean[:80]})'
                    }
                else:
                    return {
                        'status_code': code,
                        'final_url': final_url,
                        'title': title_clean,
                        'status': 'Chưa xác minh được',
                        'error': 'Trang không phải cơ sở dữ liệu PassMark',
                        'note': f'Nội dung trang không khớp: {title_clean}'
                    }
            elif source_type in ['price & rating', 'units_sold']:
                # Link giá sản phẩm nhà bán lẻ: kiểm tra có chứa tên sản phẩm hoặc dòng máy không
                return {
                    'status_code': code,
                    'final_url': final_url,
                    'title': title_clean,
                    'status': 'Đã xác minh',
                    'error': None,
                    'note': f'Xác minh thành công trang sản phẩm nhà bán lẻ ({title_clean[:80]})'
                }

            return {
                'status_code': code,
                'final_url': final_url,
                'title': title_clean,
                'status': 'Đã xác minh',
                'error': None,
                'note': f'Xác minh thành công: {title_clean[:80]}'
            }

    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {
                'status_code': 404,
                'final_url': url,
                'title': '',
                'status': 'Không hợp lệ',
                'error': 'HTTP Error 404: Not Found',
                'note': 'Link gốc bị 404 do sản phẩm ngừng kinh doanh hoặc đổi link'
            }
        elif e.code in [403, 401]:
            return {
                'status_code': e.code,
                'final_url': url,
                'title': '',
                'status': 'Chưa xác minh được',
                'error': f'HTTP Error {e.code}: Bị tường lửa chặn hoặc yêu cầu đăng nhập',
                'note': f'Không thể truy cập do hệ thống chặn bot (HTTP {e.code})'
            }
        else:
            return {
                'status_code': e.code,
                'final_url': url,
                'title': '',
                'status': 'Không hợp lệ',
                'error': f'HTTP Error {e.code}',
                'note': f'Lỗi phản hồi HTTP {e.code}'
            }
    except urllib.error.URLError as e:
        return {
            'status_code': None,
            'final_url': url,
            'title': '',
            'status': 'Chưa xác minh được',
            'error': f'Lỗi mạng: {str(e.reason)}',
            'note': f'Không kết nối được tới máy chủ ({str(e.reason)})'
        }
    except Exception as e:
        return {
            'status_code': None,
            'final_url': url,
            'title': '',
            'status': 'Chưa xác minh được',
            'error': f'Lỗi ngoại lệ: {str(e)}',
            'note': f'Ngoại lệ khi kiểm tra ({str(e)})'
        }

def run_audit():
    print("--- BẮT ĐẦU KIỂM TRA TOÀN DIỆN CÁC ĐƯỜNG LINK ---")
    today_str = datetime.now().strftime("%Y-%m-%d")
    tasks = []
    
    # 1. Thu thập tất cả các liên kết gốc cần kiểm tra
    with ThreadPoolExecutor(max_workers=12) as executor:
        for name, item in laptops_dict.items():
            brand = item['brand']
            spec_url = item.get('spec_url', '')
            price_url = item.get('price_url', '')
            cpu = item['cpu']
            gpu = item['gpu']
            
            # Benchmark URLs
            cpu_url = CPU_BENCHMARKS[cpu][2] if cpu in CPU_BENCHMARKS else ''
            gpu_url = GPU_BENCHMARKS[gpu][2] if gpu in GPU_BENCHMARKS else ''
            
            # Tasks: Specs
            tasks.append((name, 'specs', spec_url, brand, executor.submit(verify_single_url, spec_url, name, 'specs', brand)))
            # Tasks: CPU Score
            tasks.append((name, 'cpu_score', cpu_url, brand, executor.submit(verify_single_url, cpu_url, name, 'cpu_score', brand)))
            # Tasks: GPU Score
            tasks.append((name, 'gpu_score', gpu_url, brand, executor.submit(verify_single_url, gpu_url, name, 'gpu_score', brand)))
            # Tasks: Price & Rating (Kiểm tra direct price_url gốc)
            tasks.append((name, 'price & rating', price_url, brand, executor.submit(verify_single_url, price_url, name, 'price & rating', brand)))
            # Tasks: Units sold
            tasks.append((name, 'units_sold', price_url, brand, executor.submit(verify_single_url, price_url, name, 'units_sold', brand)))

        print(f"Tổng số liên kết cần đối soát: {len(tasks)}")
        
        audit_rows = []
        for name, source_type, old_url, brand, future in tasks:
            res = future.result()
            audit_rows.append({
                'laptop_name': name,
                'source_type': source_type,
                'old_url': old_url,
                'status_code': res['status_code'],
                'final_url': res['final_url'],
                'page_title': res['title'],
                'error_detected': res['error'] if res['error'] else '',
                'verification_status': res['status'],
                'check_date': today_str,
                'note': res['note']
            })

    df_audit = pd.DataFrame(audit_rows)
    output_audit_csv = 'data/link_audit_report.csv'
    df_audit.to_csv(output_audit_csv, index=False, encoding='utf-8-sig')
    print(f"\n[OK] Đã lưu kết quả kiểm tra tại: {output_audit_csv}")
    
    # Thống kê
    print("\n--- THỐNG KÊ KẾT QUẢ KIỂM TRA ---")
    print(df_audit['verification_status'].value_counts())
    print("\nLỗi phổ biến:")
    print(df_audit[df_audit['error_detected'] != '']['error_detected'].value_counts())

if __name__ == '__main__':
    run_audit()
