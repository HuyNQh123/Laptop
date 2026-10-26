"""Render existing verification evidence; this tool never verifies or fetches images."""
import json
from collections import Counter
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.product_images import load_manifest

LABELS={
    'not_found':'Chưa tìm được nguồn/ảnh catalogue đủ chuẩn',
    'model_mismatch':'Sai hoặc mâu thuẫn model',
    'access_blocked':'Bị chặn truy cập (403/429)',
    'download_error':'Lỗi tải/giải mã ảnh hoặc ảnh quá nhỏ',
    'source_unavailable':'Lỗi truy cập nguồn (SSL/timeout/404)',
    'rights_restricted':'Nguồn có hạn chế quyền sử dụng',
}
def report():
    manifest=load_manifest()
    summary=json.loads((ROOT/'data/image_audit_summary.json').read_text(encoding='utf-8'))
    missing={n:e for n,e in manifest.items() if e['verification_status']!='verified'}
    verified={n:e for n,e in manifest.items() if e['verification_status']=='verified'}
    lines=['# Kiểm tra ảnh catalogue — '+summary['audit_date'],'',
           f"Danh sách {len(manifest)} laptop, {len(manifest)} khóa tên duy nhất. Nhóm thử {summary['pilot_count']} mẫu đã được xem ảnh và kiểm tra trên web trước khi mở rộng; {summary['pilot_verified']} mẫu còn sử dụng được sau khi thay/loại nguồn có hạn chế.",'',
           '| Kết quả | Số laptop |','| --- | ---: |',
           f"| Ảnh đúng mã model trên trang nguồn | {summary['exact_model']} |",
           f"| Ảnh đại diện cùng dòng đã xác nhận | {summary['same_series_representative']} |",
           f"| Chưa có ảnh | {len(missing)} |",'',
           f"Đã tìm nguồn mới cho toàn bộ {len(manifest)} tên, tìm lại các mã còn thiếu bằng SKU ngắn, và thử mở {summary['product_pages_attempted']} trang sản phẩm (có thể lặp URL giữa cấu hình). Không kết luận mã chưa xác minh là không có ảnh trên mạng.",'',
           f"Ảnh WebP: {summary['optimized_total_bytes']:,} byte; tối đa 1000×1000 px, thu nhỏ theo tỷ lệ, không upscale/crop/AI. Hai ảnh chụp có bối cảnh cũ đã được thay bằng ảnh catalogue cho đúng MLY03SA/A và MTL73SA/A.",'',
           f"Có {summary['unique_image_files']} tệp ảnh duy nhất phục vụ {summary['verified']} máy. Xem lượt đối chiếu cùng ngoại hình tại [targeted-image-pass.md](targeted-image-pass.md).",'',
           '## Quyền sử dụng','',
           'Độ khớp model và quyền sử dụng là hai trường riêng. Các ảnh đang hiển thị có nguồn sản phẩm, nhưng trang nguồn không công bố giấy phép tái sử dụng/mở. `not_declared` không phải xác nhận được cấp phép; không gắn nhãn CC/public domain. Thông báo copyright được giữ trong `rights_notices`. Các nguồn ghi All rights reserved đã bị loại; MRX33SA/A dùng nguồn An Khang thay thế, MQKP3SA/A còn thiếu ảnh. Toàn bộ ảnh lấy từ HACOM bị loại sau khi đọc chính sách ảnh riêng tại https://hacom.vn/ban-quyen-hinh-anh. Các nguồn bị loại và nguồn thay thế nằm trong source_rejections. Phạm vi kiểm tra gồm nội dung công khai trên trang sản phẩm và chính sách riêng đã mở; không suy diễn quyền từ HTTP 200.','',
           '## Các trường hợp dữ liệu cần nhóm đối chiếu','',
           'Giữ nguyên CSV, cơ sở dữ liệu, giá và đặc trưng ML. Một số SKU có cấu hình khác CSV; ảnh đối chiếu theo SKU, dòng, thế hệ và ngoại hình, không dùng ảnh để sửa dữ liệu. Những tên biến thể mâu thuẫn (HP dv2075TU/dv2073TU, Acer 59G4/36PN) tiếp tục thiếu ảnh.','']
    for name,e in verified.items():
        if e.get('data_conflict_note'):lines.append('- '+name+': '+e['data_conflict_note'])
    lines+=['','## Ảnh đại diện dùng chung','','| Laptop | Model ảnh nguồn | Tệp dùng chung | Bằng chứng |','| --- | --- | --- | --- |']
    for name,e in verified.items():
        if e['match_level']=='same_series_representative':
            lines.append('| '+name+' | '+e['representative_source_key']+' | '+e['path']+' | '+e['representative_evidence'].replace('|','/')+' |')
    lines+=['','## Nguyên nhân còn thiếu','','| Nguyên nhân chính | Số laptop |','| --- | ---: |']
    counts=Counter(e['missing_reason'] for e in missing.values())
    for reason,label in LABELS.items():lines.append(f'| {label} | {counts[reason]} |')
    lines+=['','Mỗi máy có một nguyên nhân chính; toàn bộ lần thử, chuyển hướng, mã HTTP và lỗi cụ thể nằm trong `data/laptop_images.json`. Ảnh banner/ghép/nền trang trí bị loại được ghi rõ trong ghi chú.','','| Laptop | Nguyên nhân | Ghi chú |','| --- | --- | --- |']
    for name,e in missing.items():lines.append('| '+name+' | '+LABELS.get(e['missing_reason'],e['missing_reason'])+' | '+e['note'].replace('|','/')+' |')
    dest=ROOT/'docs/laptop-image-audit.md';dest.parent.mkdir(exist_ok=True)
    dest.write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
    print(dest)
if __name__=='__main__':report()
