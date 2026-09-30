# Laptop Analysis & Price Prediction System

Hệ thống web toàn diện bằng Python phục vụ việc quản lý, phân tích thống kê, phân cụm bằng Machine Learning, so sánh trực quan và dự đoán giá laptop dựa trên cấu hình phần cứng.

---

## 🚀 Các tính năng chính

1. **Laptop Dataset (`/laptops`)**:
   - Quản lý và duyệt toàn bộ dữ liệu 250 laptop đã qua quy trình làm sạch (Data Cleaning), chuẩn hóa kiểu dữ liệu và xử lý giá trị khuyết thiếu.
   - Hỗ trợ tìm kiếm thời gian thực, sắp xếp và phân trang.

2. **Statistical Analysis & Visualization (`/analysis`)**:
   - Báo cáo chỉ số thống kê tổng quan: Mean, Median, Standard Deviation của giá cả và cấu hình.
   - Bảng phân tích chi tiết theo từng thương hiệu (ASUS, Acer, Dell, HP, Lenovo, MSI, Apple...).
   - Danh sách Top 3 / Bottom 3 theo Giá, CPU, GPU và Top 5 Best Sellers bán chạy nhất.
   - Biểu đồ phân phối trực quan: Histogram giá, Histogram CPU, Scatter Plots tương quan (RAM vs Price, GPU vs Price, CPU vs Price).

3. **K-Means Clustering & PCA Visualization (`/clustering`)**:
   - Áp dụng `StandardScaler` và thuật toán K-Means không giám sát (Unsupervised Learning).
   - Tự động tìm số cụm tối ưu ($K$) bằng phương pháp Elbow Method và Silhouette Score.
   - Giảm chiều dữ liệu từ đa chiều xuống 2D (PC1, PC2) bằng Principal Component Analysis (PCA) và trực quan hóa các phân khúc laptop (Gaming, Budget/Office, Mainstream, High-End...).

4. **Laptop Comparison & Radar Chart (`/compare`)**:
   - So sánh trực tiếp 2 mẫu laptop bất kỳ theo các thuộc tính tự chọn (CPU, GPU, RAM, Ổ cứng, Pin, Màn hình, Giá...).
   - Chuẩn hóa Min-Max Scaling [0, 1] trên toàn bộ thị trường để vẽ biểu đồ mạng nhện (Radar Chart) đa chiều.

5. **Laptop Price Prediction (`/predict`)**:
   - Huấn luyện và đánh giá so sánh 2 mô hình học máy: **Linear Regression** (với `StandardScaler` Pipeline) và **Random Forest Regressor**.
   - Dự đoán giá bán laptop tức thời dựa trên 9 thông số kỹ thuật đầu vào với cơ chế kiểm tra và xử lý lỗi chặt chẽ (Validation).

---

## 🛠️ Công nghệ sử dụng

- **Ngôn ngữ**: Python 3.x
- **Web Framework**: Flask 3.x
- **Xử lý dữ liệu & ML**: Pandas, NumPy, Scikit-Learn, Joblib
- **Trực quan hóa**: Matplotlib, Seaborn
- **Frontend**: HTML5, CSS3, Bootstrap 5, DataTables, JavaScript

---

## 📂 Cấu trúc thư mục dự án

```text
Laptop/
│
├── data/
│   ├── laptops.csv              # File dữ liệu laptop gốc
│   ├── laptops_clustered.csv    # Dữ liệu laptop sau khi gán nhãn K-Means
│   ├── laptops_pca.csv          # Tọa độ 2D sau khi chạy PCA
│   └── results2.csv             # Kết quả phân tích thống kê theo hãng
│
├── models/
│   └── laptop_price_model.pkl   # Mô hình ML đã train được đóng gói
│
├── src/
│   ├── data_cleaning.py         # Module đọc và làm sạch dữ liệu
│   ├── data_analysis.py         # Module phân tích thống kê & sinh biểu đồ
│   ├── clustering.py            # Module phân cụm K-Means
│   ├── pca_analysis.py          # Module giảm chiều PCA & vẽ đồ thị 2D
│   ├── radar_chart.py           # Module chuẩn hóa & vẽ Radar Chart so sánh
│   └── price_prediction.py      # Module huấn luyện & dự đoán giá laptop
│
├── static/
│   ├── charts/                  # Chứa toàn bộ các biểu đồ đã sinh ra (.png)
│   └── css/
│       └── style.css            # File định dạng CSS tùy biến
│
├── templates/
│   ├── base.html                # Template khung sườn & Navbar chung
│   ├── index.html               # Trang chủ giới thiệu hệ thống
│   ├── laptops.html             # Trang danh sách Dataset
│   ├── analysis.html            # Trang Dashboard phân tích thống kê
│   ├── clustering.html          # Trang K-Means & PCA
│   ├── compare.html             # Trang so sánh 2 laptop & Radar Chart
│   └── predict.html             # Trang nhập cấu hình dự đoán giá
│
├── generate_dataset.py          # Script sinh dữ liệu laptop mẫu
├── app.py                       # File chạy chính của ứng dụng Flask
├── requirements.txt             # Danh sách các thư viện cần thiết
└── README.md                    # Hướng dẫn chi tiết dự án
```

---

## ⚙️ Hướng dẫn cài đặt và chạy hệ thống

### 1. Tạo và kích hoạt môi trường ảo (Virtual Environment)
```powershell
# Tạo virtual environment
python -m venv .venv

# Kích hoạt trên Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# Kích hoạt trên Command Prompt (cmd)
.\.venv\Scripts\activate.bat

# Kích hoạt trên Linux/macOS
source .venv/bin/activate
```

### 2. Cài đặt các thư viện cần thiết
```powershell
pip install -r requirements.txt
```

### 3. (Tùy chọn) Chạy kiểm thử từng module độc lập
```powershell
# Test Data Cleaning
python -m src.data_cleaning

# Test Phân tích & Sinh biểu đồ
python -m src.data_analysis

# Test K-Means Clustering
python -m src.clustering

# Test PCA 2D Visualization
python -m src.pca_analysis

# Test Radar Chart So sánh
python -m src.radar_chart

# Test Huấn luyện mô hình Dự đoán giá
python -m src.price_prediction
```

### 4. Khởi động Web Server
```powershell
python app.py
```

Mở trình duyệt web và truy cập địa chỉ:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**
