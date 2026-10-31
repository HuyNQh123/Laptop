# Kiểm tra giao diện ảnh — 26/10/2026

Kiểm tra trên Flask/Jinja hiện có, SQLite chỉ đọc và mô hình đã lưu. Không huấn luyện lại.
Ảnh nguồn được xem trực quan trước khi duyệt; HTTP 200/phần mở rộng không được dùng làm
bằng chứng xác minh. Thống kê và lý do từng máy: [báo cáo ảnh](laptop-image-audit.md).

| Phần kiểm tra | Kết quả |
| --- | --- |
| Khóa tên laptop | 225 khóa duy nhất, phủ chính xác CSV, phát hiện cả khóa trùng sau chuẩn hóa |
| Ảnh tối ưu | Decode, SHA-256, kích thước/dung lượng, đường dẫn nằm trong thư mục ảnh; không upscale |
| Quyền và độ khớp | Hai trạng thái riêng; loại nguồn hạn chế, không tự gắn giấy phép mở; ảnh đại diện cần bằng chứng riêng |
| Các route | `/`, `/laptops`, `/compare`, `/predict`, `/analysis`, `/clustering` trả 200 với dữ liệu thật |
| Tìm kiếm và lọc trên trình duyệt | MacBook + Apple: 21 kết quả; sắp xếp giá; 10 máy/trang; trang 2 có 11–20/21 |
| So sánh thật | MLY03SA/A và MTL73SA/A hiển thị ảnh catalogue mới, thông số/chênh lệch và radar |
| Dự đoán thật | 9 thông số của MTL73: 38.260.000 ₫; 5 gợi ý, đầu tiên là MTL73 với đúng ảnh chung trong manifest |
| Preset | Nút Văn phòng điền đúng thông số tham khảo; các input vẫn sửa được |
| Ảnh thiếu | Có placeholder “Chưa có ảnh” và lý do; không dùng model khác |
| Ảnh lỗi | Fixture chỉ ở server preview trả ảnh 404: JS đổi sang placeholder, alt giữ tên máy, bỏ credit ảnh cũ |
| Responsive | Desktop 1440×1000: kho máy/so sánh; viewport 390×844: cả sáu trang, so sánh và gợi ý; không tràn ngang cấp trang |
| Hình học ảnh | Nền trắng, contain, tỷ lệ 4:3; ảnh 550/600/1000 px không bị phóng vượt kích thước thật |
| JavaScript | Không ghi nhận lỗi JS trong các luồng đã thử |

`python -m unittest discover -s tests -v`: **17/17 đạt**. Bao gồm bộ lọc kết hợp/nhanh,
sắp xếp số, phân trang không trùng/mất dòng, API nguồn/404, escape đầu vào, form lỗi,
so sánh lỗi, ràng buộc min/step, suy luận bằng mô hình thật và kiểm tra hash dữ liệu đầu vào.
Kiểm tra tự động ghi biểu đồ/CSV vào thư mục tạm. Đầu ra do trình duyệt tạo được khôi phục
trước commit; không đưa môi trường ảo, cache hoặc CSV/model sinh lại vào thay đổi.

## Ảnh chụp

- [Kho laptop desktop](screenshots/catalogue-desktop.png)
- [Kho laptop điện thoại](screenshots/catalogue-mobile.png)
- [So sánh desktop](screenshots/compare-desktop.png)
- [So sánh điện thoại](screenshots/compare-mobile.png)
- [Gợi ý sau dự đoán trên điện thoại](screenshots/recommendation-mobile.png)

Chưa kiểm tra MySQL thật, thiết bị iOS/Android thật, Safari/Firefox, chế độ tắt JavaScript.
Quyền tái sử dụng không được xác nhận chỉ vì nguồn công khai; trạng thái chưa công bố được
ghi rõ trong manifest. Module làm sạch dữ liệu giữ nguyên và còn cảnh báo deprecation pandas.

Đã kết hợp ba commit mới trên main đến a8075b8 vào nhánh giao diện, giải quyết hai template
xung đột và giữ nguyên 67 ảnh catalogue. Chi tiết kiểm tra sau kết hợp tại
[main-merge-review.md](main-merge-review.md). Chưa merge PR vào main.

Lượt bổ sung theo nhóm: 69 máy có ảnh (67 đúng model, 2 đại diện), 66 tệp dùng chung;
21 test đạt. Xem [targeted-image-pass.md](targeted-image-pass.md) để đọc kết quả hiện tại,
nguồn ứng viên và ảnh kiểm tra giao diện. Các số liệu phía trên mô tả lượt kiểm tra trước đó.
