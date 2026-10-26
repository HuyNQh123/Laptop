# Khởi động trên Render

## Cấu hình service sau khi bản sửa được duyệt và push

- Repository: `HuyNQh123/Laptop`; branch: `feat/refresh-ui`.
- Runtime: Python; Root Directory: để trống (thư mục chứa `app.py`).
- Build Command:

```sh
pip install -r requirements.txt && MPLCONFIGDIR="$PWD/.mpl-cache" MPLBACKEND=Agg python -c "import matplotlib.font_manager"
```

- Start Command:

```sh
gunicorn --config gunicorn.conf.py app:app
```

- Health Check Path: `/` (kiểm tra được cả dữ liệu trang chủ).
- Environment: `DATABASE_BACKEND=sqlite` cho Render demo để dùng đúng
  `data/laptops.db` được đóng gói từ Git, bao gồm 1.125 nguồn đã audit.
  Không đặt biến này thì cơ chế cũ vẫn là tự thử MySQL rồi fallback SQLite.
- Dùng `PORT` Render cung cấp, thường là `10000`. Không cần gán cổng 5001.
- Không thêm `--preload`, `--daemon`, nhiều worker hoặc tăng `--timeout` để chữa lỗi khởi động.
  Kiểm tra cả `GUNICORN_CMD_ARGS` nếu đã đặt: tham số dòng lệnh có thể ghi đè file cấu hình.
- Nếu đã đặt `MPLCONFIGDIR` trong Environment, bỏ thiết lập cũ hoặc đặt đúng đường dẫn
  tuyệt đối tới `.mpl-cache` trong Root Directory, để build và runtime dùng cùng cache.
  Không nhập `$PWD` vào giá trị Environment và mong dashboard tự mở rộng biến.

`gunicorn.conf.py` bind `0.0.0.0:<PORT>`, dùng một worker để tránh nhân bộ nhớ của các
thư viện phân tích, không preload app, ghi access/error log ra stdout/stderr.
Timeout giữ mặc định Gunicorn. `.mpl-cache/` đã nằm trong `.gitignore`.
Build tạo trước cache font; runtime vẫn có thể tự tạo nếu cache không được mang sang
hoặc đường dẫn cấu hình khác. Thư mục cache phải ghi được.

## Những gì code thực sự chạy lúc import

Trước bản sửa, chuỗi import là `app` → `data_cleaning` (Pandas/NumPy) và
`data_analysis` → Matplotlib/Pyplot/Seaborn; `radar_chart` cũng nạp Pyplot.
Backend `Agg` đã được chọn đúng, nhưng không ngăn bước dò font/tạo font cache.

Bản sửa chỉ nạp các thư viện đó khi mở thống kê, so sánh hoặc phân cụm; radar chỉ
được nạp khi gửi cặp máy hợp lệ. Trang chủ, kho máy và API nguồn không cần chúng.
Không huấn luyện mô hình, chạy EDA, phân cụm, vẽ biểu đồ hoặc nạp CSV lúc import
`app.py`. Phần dự đoán vốn đã import trong route; cơ chế nạp mô hình giữ nguyên.

Import vẫn gọi `get_database_uri()`: với `DATABASE_BACKEND=sqlite` trả ngay URI
của file SQLite trong repo, không dò MySQL. Với chế độ mặc định `auto`, thử MySQL (`connect_timeout=2`), gửi
`CREATE DATABASE IF NOT EXISTS`, rồi chọn SQLite nếu lỗi. Đây là I/O lúc khởi động;
thời gian DNS/đọc phản hồi SQL không được bảo đảm bởi riêng connect timeout.
Cơ chế `auto` và kết nối MySQL được giữ nguyên; demo có thể chọn SQLite tường minh
như trên. Không chạy `init_db.py` hoặc tạo lại dữ liệu trong build/start.

`app.run(debug=True, port=5001)` chỉ chạy khi gọi `python app.py`, không chạy khi
Gunicorn import `app:app`; thay cổng ở dòng đó không sửa được bind của Gunicorn.

## Kết quả thử nghiệm local

Python 3.12 trên Windows, subprocess mới, `-X importtime`, cùng repo/database,
cache font riêng; số đo là local, không đại diện tốc độ máy Render:

| Lần import | Trước | Sau |
| --- | ---: | ---: |
| Cache font rỗng | 20,191 giây | 1,278 giây |
| Lần tiếp theo | 4,635 giây | 1,299 giây |

Trước: nạp Pandas/NumPy/Pyplot/Seaborn và tạo `fontlist`.
Sau: không nạp các thư viện này, không tạo cache, `/` và `/laptops` đều HTTP 200.
Bước dò database local riêng mất khoảng 0,263 giây, chọn SQLite.

Test hồi quy chặn hoàn toàn import các thư viện khoa học trong subprocess:
bản cũ thất bại; bản sửa phục vụ được `/`, `/laptops`, `/api/laptop-sources/1`.
Test cấu hình kiểm tra cổng PORT tùy chỉnh, cổng mặc định, một worker và không preload.
Bộ kiểm thử đầy đủ: 26 tests đạt, gồm GET thống kê, phục vụ/giải mã PNG biểu đồ,
POST so sánh tạo radar hợp lệ và POST dự đoán/gợi ý bằng model có sẵn.
Test subprocess tạo cache với `MPLCONFIGDIR=<Root Directory>/.mpl-cache`, sau đó
nạp `gunicorn.conf.py` trong tiến trình mới trước khi import Matplotlib: đường dẫn
runtime trùng build, backend Agg, nội dung và mtime của cache font không đổi.
HTTP local `/` và kho máy có bộ lọc trả 200;
`netstat` xác nhận socket thử nghiệm `0.0.0.0:5012` ở trạng thái LISTENING,
không tạo thư mục font cache. Server thử nghiệm đã dừng sau kiểm tra.

Lệnh `python -m gunicorn --check-config` trên Windows dừng ở lỗi thiếu `fcntl`.
Môi trường này không có Linux/WSL hoạt động để chạy Gunicorn thật. Thử HTTP local
và bộ kiểm thử Flask không thay thế việc xác nhận tiến trình Gunicorn trên Render.

## Phân biệt cảnh báo với nguyên nhân triển khai

`Matplotlib is building the font cache` là thông báo khởi tạo, không tự nó chứng
minh deadlock. `No open ports detected` chỉ nói lần quét chưa thấy cổng phù hợp.
Đặc biệt Gunicorn thường bind socket trước khi import app trong worker; với preload
thì thứ tự khác. Gunicorn hiện đại còn tự đọc PORT cho bind mặc định, nên không thể
kết luận lệnh `gunicorn app` tự nó sai cổng chỉ từ hai dòng log trên.

Chưa có toàn bộ log, Start Command và biến môi trường thực tế của service để kết
luận nguyên nhân duy nhất của lần deploy quá 10 phút. Nếu vẫn lỗi sau khi duyệt:

1. Xác nhận deploy đang dùng commit mới chứa bản sửa, không còn `bf23777`.
2. Kiểm tra `Listening at: http://0.0.0.0:10000` (hoặc PORT thực tế),
   `Booting worker`, rồi access log của health check `/` trả 200.
3. Nếu không có `Listening at`, đối chiếu Start Command, Root Directory,
   PORT và `GUNICORN_CMD_ARGS`; không chỉ tăng timeout.
4. Nếu đã listen nhưng worker không sẵn sàng, đọc traceback/worker timeout,
   tín hiệu SIGKILL/OOM và memory metrics; kiểm tra database nếu stack đang chờ MySQL.
5. Nếu cache font chậm ở build, log sẽ chỉ rõ build chưa hoàn tất; kiểm tra quyền
   ghi/cache path và bước warm cache, không đợi port của web trong giai đoạn build.

Tham khảo: [Render port binding](https://render.com/docs/web-services#port-binding),
[Gunicorn settings](https://docs.gunicorn.org/en/stable/settings.html),
[Matplotlib cache variables](https://matplotlib.org/stable/install/environment_variables_faq.html).
