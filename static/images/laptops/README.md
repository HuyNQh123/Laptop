# Ảnh sản phẩm catalogue

Bảng ánh xạ và bằng chứng: `data/laptop_images.json`. Số liệu: `data/image_audit_summary.json`.
Báo cáo từng máy còn thiếu: `docs/laptop-image-audit.md`. Hai ảnh chụp có bối cảnh cũ đã bỏ.

Chỉ dùng ảnh một máy đầy đủ thân/màn hình, nền trắng hoặc trong suốt, chính diện hoặc 3/4.
Loại ảnh người dùng trong phòng/trên bàn, collage, banner, quà tặng, phụ kiện và ảnh chưa
xác nhận model/thế hệ/kích thước/màu. Không dùng AI, không sửa dữ liệu gốc để khớp ảnh.

## Thêm hoặc thay ảnh

1. Tìm trang hãng/nhà bán lẻ bằng SKU, không đoán URL. Mở trang và đối chiếu URL cuối,
   tiêu đề, model, thế hệ, kích thước, màu. Đọc gallery/Product JSON-LD, srcset hoặc og:image
   gắn với chính sản phẩm đó; tránh ảnh liên quan, logo và placeholder.
2. Xem trực quan ảnh gốc. Đọc chính sách ảnh nếu nguồn có liên kết riêng. Có hạn chế rõ ràng
   thì ghi lại và tìm nguồn khác. Chính sách HACOM: https://hacom.vn/ban-quyen-hinh-anh;
   các ảnh từ nguồn này đã bị loại, không suy diễn CC BY từ danh sách loại license trong chính sách.
3. Tách độ khớp model và quyền sử dụng. `rights_status: not_declared` có nghĩa trang chưa
   công bố giấy phép, **không xác nhận đã được cấp phép**. Không gắn nhãn CC/public domain.
   Lưu thông báo copyright/phạm vi kiểm tra. `restricted` không được hiển thị.
4. Giữ bản tải gốc ngoài Git. Chạy optimizer (công cụ không tự xác minh hoặc duyệt ảnh):

   ```powershell
   python tools/optimize_product_image.py C:/path/original.png stable-model-key.webp
   ```

5. Cập nhật đúng khóa tên đầy đủ đã kiểm tra duy nhất; không ghép bằng vị trí dòng hoặc ID DB.
   Ghi `source_url`, `resolved_source_url`, `source_title`, `source_name`, `image_url` quan sát
   thực tế, `matched_model`, `gallery_binding`, `model_evidence`, `checked_date`, `visual_checked`,
   `image_type: catalogue`, `match_level`, `rights_status`, `rights_note`, `rights_notices`,
   `alt`, kích thước gốc/tối ưu, SHA-256 và đường dẫn cục bộ.
6. Chỉ dùng `exact_model` sau đối chiếu mã máy. `same_series_representative` yêu cầu xác nhận
   cùng ngoại hình và chỉ khác RAM/SSD; giao diện ghi “Ảnh đại diện cùng dòng máy”.
   Không đủ bằng chứng thì giữ placeholder “Chưa có ảnh”.
7. Cập nhật số liệu, chạy:

   ```powershell
   python tools/check_product_images.py
   python tools/image_audit_report.py
   python -m unittest discover -s tests -v
   ```

Ảnh WebP tối đa 1000×1000 px và 150 KB, thu nhỏ theo tỷ lệ, không upscale/crop.
Vùng trong suốt đặt trên nền trắng. Thành phần dùng chung cho kho máy, so sánh và gợi ý
sử dụng contain, giới hạn theo kích thước ảnh thật, alt có tên máy, lazy loading và fallback.

Khóa JSON trùng (kể cả hoa/thường, khoảng trắng, Unicode tương đương) bị từ chối.
Ảnh chưa duyệt hoặc nằm ngoài thư mục này không được dùng làm ảnh sản phẩm.
