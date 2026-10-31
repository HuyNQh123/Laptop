# Kết hợp main vào feat/refresh-ui — 2026-10-26

## Trạng thái và bảo toàn thay đổi

- Nhánh trước merge: `feat/refresh-ui`, a9005c6; main mới nhất đã fetch: a8075b8.
- Lưu 4 file chưa commit trong stash `e41598b4788027caed05a3799c58e2bb8ac25c4a`
  (`pre-main-merge: preserve local generated outputs 2026-10-26`):
  `data/laptops_clustered.csv`, `data/laptops_pca.csv`, `data/results2.csv`,
  `static/charts/pca_clusters.png`. Stash được giữ lại, không áp lại đầu ra cũ vào main mới.
- Đã đọc thay đổi liên quan từ 9a1c593 (nguồn đối chiếu), b408bbb (thống kê),
  a8075b8 (NUMERIC_COLS cho phân cụm), cùng các template/backend của hai nhánh.
- Merge thông thường, không rebase/force-push; không merge PR vào main.

## Cách kết hợp

- `templates/laptops.html`: giữ form GET, thẻ catalogue dùng component chung, toàn bộ ID
  cho tìm kiếm AJAX, bộ lọc, sort, phân trang và số máy/trang. Đưa ý nghĩa trạng thái/ghi chú
  nguồn mới của main vào luồng hộp nguồn hiện có, thay vì mang lại bảng DataTables/modal cũ.
- `static/js/ui.js`: hiển thị note, ngày, trạng thái bằng textContent; chỉ mở liên kết ở trạng thái
  Verified/Đã xác minh hoặc Chưa xác minh được. Trạng thái chưa xác minh có nhãn riêng;
  trạng thái không có nguồn không hiện liên kết. Giữ kiểm tra giao thức URL và fallback ảnh.
- `templates/analysis.html`: dùng `stats`, `top_bottom`, `leaders`, `evaluation`, `num_cols`,
  `col_labels`, `brands`, `best_value_laptops`, `top_selling`, `laptops` từ backend mới của main.
  Bỏ biến cũ không còn được truyền như total_laptops, med_price, top_cpu, brand_stats.
  Giữ phong cách sáng của nhánh giao diện; đưa đủ 9 tiêu chí cao/thấp, thống kê nhóm,
  trung bình/trung vị/độ phân tán/số mẫu, xếp hạng hãng, P/P và số lượng bán của main vào các section.
  Các mục dùng anchor/details native, hoạt động bằng bàn phím và không cần JS để xem dữ liệu.
- `static/js/analysis.js`: tìm thông số/hãng, phối hợp lọc hãng, số dòng và trạng thái rỗng.
  Tìm tiếng Việt có hoặc không dấu. Tải CSV dùng url_for('download_results').
- `static/css/style.css`: điều hướng thống kê, khoảng cách details và bộ lọc responsive.
- `app.py`: kiểm tra bản tự kết hợp; giữ context mới, `/stats`, `/download/results` của main
  cùng catalog_context/product_view, xác thực form và ảnh gợi ý của nhánh giao diện.
- Giữ nguyên src/data_analysis.py, dữ liệu nguồn, script audit, CSV/biểu đồ đã commit của main.
  Không đổi model, 9 đặc trưng dự đoán, training CSV hoặc DB. Không huấn luyện lại.

## Kiểm tra thực tế

- 17 test hồi quy hiện có đạt; 2 test tích hợp mới đạt: StrictUndefined cho `/analysis`,
  `/stats`, catalog có filter/sort/page và kiểm tra CSV download/schema/context/19 đường dẫn biểu đồ.
- Dự đoán và so sánh POST bằng model hiện có; form hợp lệ/không hợp lệ, ảnh gợi ý/so sánh,
  phân cụm, 6 route hiện có đều qua kiểm tra tự động.
- Test dùng SQLite chỉ đọc, model sao chép và đầu ra tạm; chặn huấn luyện, so hash đầu vào.
  Khi thử trình duyệt đồng thời với test, guard hash phát hiện CSV thống kê bị web ghi lại;
  đã phục hồi đầu ra, tách hai lượt kiểm tra và chạy lại hai test tích hợp thành công.
- check_product_images.py đạt: 225 khóa duy nhất, 67 đúng model, 0 đại diện cùng dòng,
  158 thiếu ảnh. Manifest, ảnh và quy trình catalogue không thay đổi.
- Web chạy tại 127.0.0.1:5000 với SQLite chỉ đọc; desktop 1440×1000 và màn hình nhỏ 390×844.
- Kho: tìm MacBook, lọc Apple, sort giá tăng, 10 máy/trang; 21 kết quả; trang 2 là 11–20/21,
  10 giá tăng đúng thứ tự. Hộp nguồn mở/đóng, hiện note/ngày/status/link; ảnh thật và placeholder
  hiển thị nhất quán với contain, tên/alt và thông tin nguồn.
- Thống kê: 225 mẫu/9 hãng, giá trung bình 32.526.444 ₫, trung vị 25.990.000 ₫.
  Lọc Apple + “gia” có đúng 1 dòng giá; truy vấn không khớp có thông báo rỗng.
  Mở biểu đồ phần cứng thành công; bảng rộng cuộn trong vùng riêng, không tràn toàn trang.
- Không có lỗi console trình duyệt. Không còn marker xung đột trong mã ứng dụng/template/test.
- Phục hồi file sinh ra khi chạy web từ baseline sau kết hợp, không đưa chúng vào commit.
  Các CSV và PNG nhập từ main là thay đổi đã commit upstream, không phải đầu ra QA mới.
- Chưa kiểm tra MySQL thật, thiết bị điện thoại thật, Safari/Firefox; nguồn dữ liệu được kiểm tra
  bằng SQLite sẵn có, không chạy lại script nhập CSV nguồn vào DB. Cảnh báo deprecation pandas còn tồn tại.

## Ảnh chụp sau kết hợp

- [Kho desktop](screenshots/merge-catalogue-desktop.png)
- [Kho điện thoại](screenshots/merge-catalogue-mobile.png)
- [Lọc thống kê desktop](screenshots/merge-statistics-desktop.png)
- [Lọc thống kê điện thoại](screenshots/merge-analysis-mobile.png)
