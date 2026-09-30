import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    """Set background color for a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def create_document():
    doc = docx.Document()
    
    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(51, 51, 51)
    
    # Title
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_run = title_p.add_run("BÁO CÁO TOÀN DIỆN VÀ TÀI LIỆU KỸ THUẬT\nHỆ THỐNG PHÂN TÍCH & DỰ ĐOÁN GIÁ LAPTOP\n(LAPTOP ANALYSIS & PRICE PREDICTION SYSTEM)")
    title_run.font.size = Pt(16)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(13, 110, 253) # Primary Blue
    
    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_run = sub_p.add_run("Tổng hợp chi tiết 8 bước phát triển (STEP 1 - STEP 8), vai trò từng tập tin, kiến trúc hệ thống và giải thích thuật toán")
    sub_run.font.size = Pt(11)
    sub_run.font.italic = True
    sub_run.font.color.rgb = RGBColor(108, 117, 125)
    
    doc.add_paragraph("-" * 80)
    
    # ==========================================
    # PHẦN 1: TỔNG QUAN DỰ ÁN
    # ==========================================
    h1 = doc.add_heading("PHẦN 1: TỔNG QUAN DỰ ÁN & CÔNG NGHỆ SỬ DỤNG", level=1)
    h1.runs[0].font.color.rgb = RGBColor(13, 110, 253)
    
    doc.add_paragraph(
        "Hệ thống 'Laptop Analysis & Price Prediction System' là một ứng dụng Web hoàn chỉnh được xây dựng trên nền tảng Python (Flask). "
        "Dự án kết hợp chặt chẽ giữa Khoa học dữ liệu (Data Science), Học máy (Machine Learning) và Phát triển ứng dụng Web, "
        "nhằm giải quyết bài toán quản lý, phân tích chuyên sâu cấu hình laptop trên thị trường, tự động phân nhóm sản phẩm và dự đoán giá thành dựa trên thông số phần cứng."
    )
    
    p = doc.add_paragraph()
    p.add_run("Các công nghệ cốt lõi bao gồm:\n").bold = True
    techs = [
        ("Python 3.x", "Ngôn ngữ lập trình chính cho toàn bộ backend, xử lý dữ liệu và mô hình AI."),
        ("Flask", "Web Framework vi mô nhẹ, linh hoạt, dễ mở rộng để xây dựng API và render giao diện HTML."),
        ("Pandas & NumPy", "Thư viện nền tảng để đọc, làm sạch dữ liệu bảng, tính toán thống kê và biến đổi ma trận số học."),
        ("Scikit-Learn", "Thư viện Machine Learning chuẩn mực phục vụ: StandardScaler, KMeans, PCA, Linear Regression, Random Forest, Pipeline, Train/Test Split và Metrics."),
        ("Matplotlib & Seaborn", "Thư viện vẽ và kết xuất biểu đồ tĩnh (Histogram, Scatter plot, Polar Radar chart) dưới dạng hình ảnh PNG."),
        ("Joblib", "Đóng gói, tuần tự hóa (serialize) và lưu trữ mô hình Machine Learning đã huấn luyện thành file binary (.pkl)."),
        ("Bootstrap 5 & DataTables", "Framework giao diện hiện đại, responsive, kết hợp thư viện bảng động để tìm kiếm và phân trang mượt mà.")
    ]
    for tech, desc in techs:
        p_item = doc.add_paragraph(style='List Bullet')
        p_item.add_run(f"{tech}: ").bold = True
        p_item.add_run(desc)
        
    doc.add_paragraph()

    # ==========================================
    # PHẦN 2: CHI TIẾT TỪNG BƯỚC PHÁT TRIỂN (STEP 1 - STEP 8)
    # ==========================================
    h1 = doc.add_heading("PHẦN 2: CHI TIẾT CÁC BƯỚC XÂY DỰNG (STEP 1 ĐẾN STEP 8)", level=1)
    h1.runs[0].font.color.rgb = RGBColor(13, 110, 253)
    
    steps = [
        {
            "num": "STEP 1",
            "name": "Khởi tạo Môi trường & Khung xương Website (Project Setup)",
            "purpose": "Thiết lập nền móng dự án, cô lập môi trường thực thi (Virtual Environment), cấu hình quản lý dependencies và dựng bộ khung website Flask với cấu trúc thừa kế giao diện (Template Inheritance).",
            "files": [
                (".venv/ (Virtual Environment)", "Thư mục môi trường ảo Python cô lập, giúp cài đặt đúng phiên bản thư viện mà không xung đột với hệ thống toàn cục của máy tính."),
                ("requirements.txt", "Tập tin khai báo danh sách tất cả các thư viện bên ngoài cần thiết (Flask, pandas, scikit-learn...). Giúp việc cài đặt lại môi trường chỉ bằng một lệnh duy nhất: pip install -r requirements.txt."),
                ("app.py", "Tập tin điều phối trung tâm của ứng dụng Flask. Khởi tạo Flask App, định tuyến URL (Routing) và lắng nghe các request từ client."),
                ("templates/base.html", "Khung xương HTML mẫu (Master Layout). Chứa thanh điều hướng chung (Navbar), nhúng CSS/JS Bootstrap và định nghĩa các khối {% block content %} để các trang con kế thừa."),
                ("templates/index.html", "Trang chủ (Home Page) kế thừa từ base.html, hiển thị lời chào và tổng quan ban đầu."),
                ("static/css/style.css", "Tập tin CSS tùy chỉnh để định dạng màu sắc, bo góc thẻ card và các hiệu ứng hover mượt mà.")
            ],
            "impact": "Tạo ra một website hoạt động được ở mức cơ sở tại địa chỉ http://127.0.0.1:5000, sẵn sàng cho việc tích hợp dữ liệu và các module khoa học dữ liệu tiếp theo."
        },
        {
            "num": "STEP 2",
            "name": "Tạo Dataset & Xây dựng Pipeline Làm sạch Dữ liệu (Data Cleaning)",
            "purpose": "Chuẩn bị nguồn dữ liệu laptop và xây dựng quy trình tiền xử lý dữ liệu tự động, loại bỏ dữ liệu rác, chuẩn hóa định dạng văn bản và xử lý dữ liệu khuyết thiếu trước khi đưa vào phân tích và học máy.",
            "files": [
                ("generate_dataset.py", "Script sinh dữ liệu mô phỏng gồm 255 laptop thuộc nhiều hãng (ASUS, Dell, Apple, HP...) với các thông số: CPU/GPU Score, RAM, Storage, Screen, Pin, Giá, Số lượng bán. Cố ý chèn 5 dòng trùng lặp và 11 giá trị rỗng ở cột giá để kiểm tra tính năng lọc."),
                ("data/laptops.csv", "Tập tin dữ liệu thô (Raw Data) lưu trữ toàn bộ mẫu laptop dạng bảng CSV."),
                ("src/data_cleaning.py", "Module xử lý dữ liệu chuyên biệt gồm các hàm: load_data(), remove_duplicates() (xóa trùng), normalize_brand() (chuẩn hóa tên hãng), convert_numeric_columns() (chuyển đổi đơn vị '16GB' -> 16 dạng số) và handle_missing_values() (điền giá trị khuyết thiếu bằng Median cho cột số và Mode/Unknown cho chuỗi)."),
                ("templates/laptops.html", "Giao diện hiển thị bảng dữ liệu laptop đã qua làm sạch dưới dạng bảng Bootstrap trực quan.")
            ],
            "impact": "Tạo ra route /laptops. Giúp hệ thống sở hữu tập dữ liệu sạch (250 dòng hoàn chỉnh, không còn NaN hay duplicate), bảo đảm tính chính xác tuyệt đối cho các thuật toán AI phía sau."
        },
        {
            "num": "STEP 3",
            "name": "Phân tích Thống kê & Trực quan hóa Dữ liệu (EDA & Visualization)",
            "purpose": "Khai phá dữ liệu (Exploratory Data Analysis - EDA), tính toán các chỉ số thống kê mô tả (Mean, Median, Std), phân nhóm theo thương hiệu, xếp hạng Top/Bottom/Best Sellers và vẽ biểu đồ phân tích xu hướng giá.",
            "files": [
                ("src/data_analysis.py", "Module tính toán thống kê và vẽ biểu đồ. Sử dụng Pandas groupby('brand') để tính toán đa chỉ số; hàm get_top_bottom() để lọc top cao nhất/thấp nhất; hàm create_charts() dùng Matplotlib/Seaborn vẽ 6 biểu đồ phân phối và tương quan, lưu vào static/charts/."),
                ("data/results2.csv", "File CSV kết xuất lưu trữ bảng thống kê tổng hợp theo từng hãng để phục vụ báo cáo."),
                ("static/charts/*.png", "Thư mục lưu trữ các hình ảnh biểu đồ: price_histogram.png, cpu_score_histogram.png, avg_price_by_brand.png, ram_vs_price.png, cpu_vs_price.png, gpu_vs_price.png."),
                ("templates/analysis.html", "Giao diện Dashboard phân tích tổng thể: hiển thị các chỉ số Mean/Median/Std, Top/Bottom 3 của Giá/CPU/GPU, Top 5 Laptop bán chạy nhất (Best Sellers), bảng phân tích hãng và lưới hiển thị 6 biểu đồ.")
            ],
            "impact": "Tạo ra route /analysis. Cung cấp cái nhìn sâu sắc, toàn diện về thị trường laptop giúp người dùng hiểu được tương quan giữa cấu hình và giá trị sản phẩm."
        },
        {
            "num": "STEP 4",
            "name": "Phân cụm Laptop bằng Thuật toán K-Means (Unsupervised Learning)",
            "purpose": "Sử dụng thuật toán học máy không giám sát K-Means để tự động phân chia 250 laptop thành các nhóm (cụm) có cấu hình và đặc tính tương đồng nhau mà không cần nhãn định sẵn.",
            "files": [
                ("src/clustering.py", "Module xử lý phân cụm. Áp dụng StandardScaler để đưa các thuộc tính có thang đo khác nhau (RAM 8-64GB vs Giá 10-60 triệu) về cùng phân phối chuẩn (Mean=0, Std=1). Dùng vòng lặp thử K=2..8, vẽ biểu đồ Elbow (Inertia) và Silhouette Score để tự động tìm ra Best K (K=2). Tự động gán nhãn phân khúc (Gaming, Budget, Mainstream, Premium) dựa trên giá trị trung bình của từng cụm."),
                ("data/laptops_clustered.csv", "Tập tin lưu trữ dữ liệu laptop đã được bổ sung thêm cột 'cluster' (nhãn cụm phân loại)."),
                ("static/charts/elbow_method.png", "Biểu đồ đường gấp khúc Elbow minh họa mức giảm quán tính (Inertia) theo số cụm K."),
                ("static/charts/silhouette_score.png", "Biểu đồ đánh giá chất lượng phân cụm Silhouette Score cho từng K."),
                ("templates/clustering.html", "Giao diện hiển thị số cụm tối ưu, điểm Silhouette, các thẻ chi tiết đặc điểm từng cụm, các biểu đồ Elbow/Silhouette và bảng dữ liệu laptop kèm bộ lọc (Filter) theo Cluster.")
            ],
            "impact": "Tạo ra route /clustering. Giúp hệ thống tự động nhận diện phân khúc thị trường (nhóm Laptop văn phòng giá rẻ vs nhóm Laptop Gaming hiệu năng cao) một cách khách quan."
        },
        {
            "num": "STEP 5",
            "name": "Giảm chiều Dữ liệu & Trực quan hóa 2D bằng PCA (PCA Visualization)",
            "purpose": "Áp dụng kỹ thuật Giảm chiều dữ liệu Principal Component Analysis (PCA) để nén không gian dữ liệu 9 chiều cấu hình xuống không gian 2 chiều (PC1, PC2) nhằm vẽ các cụm laptop lên mặt phẳng 2D.",
            "files": [
                ("src/pca_analysis.py", "Module thực hiện PCA(n_components=2). Tính toán lượng phương sai giải thích được (Explained Variance Ratio: PC1 ~56.68%, PC2 ~10.82%, Tổng ~67.50%). Vẽ biểu đồ phân tán (Scatter plot) phân biệt màu sắc giữa các cluster."),
                ("data/laptops_pca.csv", "Tập tin CSV lưu tọa độ 2D của từng mẫu laptop: name, brand, PC1, PC2, cluster."),
                ("static/charts/pca_clusters.png", "Biểu đồ Scatter plot 2D thể hiện ranh giới phân tách rõ ràng giữa các phân khúc laptop.")
            ],
            "impact": "Tích hợp biểu đồ PCA lên phần đầu của trang /clustering, giúp người dùng trực quan hóa được dữ liệu đa chiều phức tạp ngay trên màn hình phẳng 2D."
        },
        {
            "num": "STEP 6",
            "name": "So sánh 2 Laptop & Biểu đồ Mạng nhện (Radar Chart Comparison)",
            "purpose": "Cung cấp công cụ so sánh trực tiếp 2 mẫu laptop bất kỳ theo các tiêu chí phần cứng tùy chọn (CPU, GPU, RAM, Ổ cứng, Pin, Màn hình, Giá...) dưới dạng biểu đồ mạng nhện đa chiều.",
            "files": [
                ("src/radar_chart.py", "Module chuẩn hóa dữ liệu theo công thức Min-Max Scaling [0, 1] trên toàn bộ 250 laptop trong dataset, sau đó sử dụng hệ tọa độ cực (Polar Coordinates trong Matplotlib) để vẽ 2 đa giác khép kín đại diện cho 2 máy, lưu vào static/charts/radar_comparison.png."),
                ("templates/compare.html", "Giao diện so sánh với 2 Dropdown chọn Laptop 1 và Laptop 2, danh sách Checkbox chọn các thuộc tính so sánh, bảng đối chiếu thông số thật (có đơn vị VND, GB, Hz, kg, Wh...) và hình ảnh Radar Chart kết quả.")
            ],
            "impact": "Tạo ra route /compare. Giúp người mua hàng dễ dàng đặt 2 mẫu laptop lên bàn cân để so sánh toàn diện ưu nhược điểm của từng máy."
        },
        {
            "num": "STEP 7",
            "name": "Xây dựng Mô hình Dự đoán Giá Laptop bằng Machine Learning (Price Prediction)",
            "purpose": "Ứng dụng học máy có giám sát (Supervised Regression) để học mối tương quan giữa 9 thông số kỹ thuật và giá thành laptop, từ đó dự đoán chính xác giá bán của một chiếc laptop có cấu hình bất kỳ.",
            "files": [
                ("src/price_prediction.py", "Module xây dựng Scikit-Learn Pipeline, chia tập Train (80% = 200 mẫu) và Test (20% = 50 mẫu). Huấn luyện đồng thời 2 mô hình: Linear Regression (với StandardScaler) và Random Forest Regressor (100 cây). Đánh giá qua MAE, RMSE và R² Score. Tự động chọn mô hình tốt nhất (Linear Regression với R²=0.7000) và đóng gói bằng Joblib vào models/laptop_price_model.pkl. Cung cấp hàm predict_laptop_price() dự đoán trực tiếp mà không cần train lại."),
                ("models/laptop_price_model.pkl", "File mô hình ML đã đóng gói kèm Pipeline tiền xử lý."),
                ("templates/predict.html", "Giao diện Form nhập liệu thông số cấu hình, thẻ hiển thị chỉ số đánh giá mô hình (MAE, RMSE, R² Score) và khu vực hiển thị giá ước tính định dạng tiền VND.")
            ],
            "impact": "Tạo ra route /predict (hỗ trợ cả GET và POST) với cơ chế kiểm tra dữ liệu đầu vào (Validation: kiểm tra số âm, bỏ trống, giá trị phi lý), giúp người dùng định giá được chiếc laptop theo cấu hình mong muốn."
        },
        {
            "num": "STEP 8",
            "name": "Tích hợp Toàn diện, Nâng cấp Giao diện & Kiểm thử (Final Integration & Testing)",
            "purpose": "Đồng bộ hóa toàn bộ 6 phân hệ của website, nâng cấp giao diện chuẩn Bootstrap 5, bổ sung tìm kiếm/phân trang DataTables, viết tài liệu README.md và kiểm thử tự động toàn diện.",
            "files": [
                ("templates/index.html (Nâng cấp)", "Bổ sung Hero Banner giới thiệu, 4 thẻ Card số liệu động thực tế và 6 thẻ tính năng dẫn trực tiếp tới từng phân hệ."),
                ("templates/laptops.html (Nâng cấp)", "Tích hợp thư viện DataTables hỗ trợ tìm kiếm theo từ khóa thời gian thực, sắp xếp cột tăng/giảm và phân trang 15 dòng/trang."),
                ("templates/base.html (Nâng cấp)", "Đồng bộ thanh menu Navbar với đầy đủ 6 liên kết: Home, Laptops, Analysis, Clustering, Compare, Price Prediction."),
                ("README.md", "Tài liệu kỹ thuật Markdown chuẩn quốc tế tóm tắt dự án, kiến trúc, công nghệ và lệnh vận hành."),
                ("generate_report_docx.py", "Script tự động kết xuất tài liệu báo cáo toàn diện ra tập tin Microsoft Word (.docx).")
            ],
            "impact": "Hoàn thiện hệ thống thành một sản phẩm Web Data Science & AI hoàn chỉnh, chạy ổn định, không lỗi, giao diện thân thiện và sẵn sàng để demo hoặc phát triển tiếp."
        }
    ]
    
    for step in steps:
        doc.add_heading(f"{step['num']}: {step['name']}", level=2)
        
        p_pur = doc.add_paragraph()
        p_pur.add_run("Mục tiêu & Tác dụng trong Web: ").bold = True
        p_pur.add_run(step["purpose"])
        
        doc.add_paragraph().add_run("Chi tiết vai trò của từng tập tin:").bold = True
        for fname, fdesc in step["files"]:
            p_f = doc.add_paragraph(style='List Bullet')
            p_f.add_run(f"• {fname}: ").bold = True
            p_f.add_run(fdesc)
            
        p_imp = doc.add_paragraph()
        p_imp.add_run("Kết quả đạt được: ").bold = True
        p_imp.add_run(step["impact"])
        doc.add_paragraph()

    # ==========================================
    # PHẦN 3: CHI TIẾT CÁC PHÂN HỆ TRONG WEBSITE
    # ==========================================
    h1 = doc.add_heading("PHẦN 3: KIẾN TRÚC & CHI TIẾT CÁC HỆ THỐNG CON TRONG WEBSITE", level=1)
    h1.runs[0].font.color.rgb = RGBColor(13, 110, 253)
    
    doc.add_paragraph(
        "Website được thiết kế theo mô hình phân tầng Modular Architecture, tách biệt rõ ràng giữa tầng Giao diện (Presentation Layer - HTML/Jinja2), "
        "tầng Điều phối (Routing/Controller Layer - Flask app.py) và tầng Xử lý nghiệp vụ & Machine Learning (Business & ML Layer - src/)."
    )
    
    modules = [
        ("1. Phân hệ Quản lý & Khám phá Dữ liệu (Dataset Management)",
         "URL: /laptops\n"
         "Nhiệm vụ: Trình bày tập dữ liệu 250 laptop đã được làm sạch hoàn chỉnh. Hệ thống tích hợp bảng tương tác DataTables cho phép người dùng tìm kiếm tức thì theo tên máy, hãng sản xuất hoặc lọc nhanh các dòng máy theo RAM/Ổ cứng/Màn hình mà không cần tải lại trang."),
         
        ("2. Phân hệ Thống kê & Báo cáo Thị trường (Statistical Dashboard)",
         "URL: /analysis\n"
         "Nhiệm vụ: Cung cấp bức tranh toàn cảnh về thị trường laptop. Phân hệ tự động tính toán các đại lượng thống kê mô tả (Mean, Median, Standard Deviation) cho giá bán; phân loại top 3 laptop có giá/CPU/GPU cao nhất và thấp nhất; vinh danh 5 mẫu laptop bán chạy nhất; tổng hợp bảng so sánh tương quan giữa các thương hiệu và hiển thị 6 biểu đồ trực quan."),
         
        ("3. Phân hệ Phân khúc Thông minh (K-Means & PCA Clustering System)",
         "URL: /clustering\n"
         "Nhiệm vụ: Ứng dụng AI học máy không giám sát để tự động phân nhóm laptop theo độ tương đồng cấu hình. Hệ thống kết hợp 2 kỹ thuật đỉnh cao:\n"
         "• K-Means: Tìm số cụm tối ưu qua phân tích điểm Silhouette Score và Elbow Method, sau đó tự động phân loại laptop thành các phân khúc thị trường (Budget/Office vs Gaming/High-Performance).\n"
         "• PCA 2D Visualization: Nén dữ liệu đa chiều xuống 2 trục tọa độ chính (PC1 giải thích 56.68%, PC2 giải thích 10.82% phương sai) để vẽ biểu đồ phân tán trực quan hóa ranh giới các cụm."),
         
        ("4. Phân hệ So sánh & Đánh giá Đa chiều (Laptop Comparison & Radar Chart)",
         "URL: /compare\n"
         "Nhiệm vụ: Hỗ trợ người dùng lựa chọn 2 laptop bất kỳ và tích chọn các tiêu chí muốn so sánh. Hệ thống áp dụng Min-Max Scaling trên toàn bộ thị trường để đưa các chỉ số về thang đo chuẩn [0, 1], sau đó vẽ biểu đồ mạng nhện Radar Chart đa giác khép kín kèm bảng đối chiếu thông số thật, giúp nhận diện rõ điểm mạnh/yếu của từng model."),
         
        ("5. Phân hệ Trí tuệ Nhân tạo Dự đoán Giá (Price Prediction System)",
         "URL: /predict\n"
         "Nhiệm vụ: Ứng dụng mô hình học máy Linear Regression (được chuẩn hóa qua StandardScaler Pipeline, đạt R² = 0.7000) để ước tính giá trị thị trường của một cấu hình laptop bất kỳ. Hệ thống tích hợp cơ chế Validation nghiêm ngặt, ngăn chặn các giá trị số âm, giá trị rỗng hoặc thông số phi thực tế trước khi tính toán.")
    ]
    
    for mtitle, mdesc in modules:
        doc.add_heading(mtitle, level=2)
        doc.add_paragraph(mdesc)

    # ==========================================
    # PHẦN 4: HƯỚNG DẪN CÀI ĐẶT VÀ VẬN HÀNH
    # ==========================================
    h1 = doc.add_heading("PHẦN 4: HƯỚNG DẪN KHỞI CHẠY & VẬN HÀNH HỆ THỐNG", level=1)
    h1.runs[0].font.color.rgb = RGBColor(13, 110, 253)
    
    doc.add_paragraph("Để triển khai và chạy thử nghiệm hệ thống trên máy tính cá nhân, thực hiện tuần tự các bước sau:")
    
    steps_guide = [
        ("Bước 1: Mở Terminal tại thư mục dự án và kích hoạt môi trường ảo", ".\\.venv\\Scripts\\Activate.ps1 (trên Windows PowerShell) hoặc source .venv/bin/activate (trên Linux/macOS)."),
        ("Bước 2: Cài đặt toàn bộ thư viện cần thiết", "pip install -r requirements.txt"),
        ("Bước 3: (Tùy chọn) Chạy kiểm thử độc lập các module", "python -m src.data_cleaning\npython -m src.data_analysis\npython -m src.clustering\npython -m src.pca_analysis\npython -m src.radar_chart\npython -m src.price_prediction"),
        ("Bước 4: Khởi động Web Server", "python app.py"),
        ("Bước 5: Mở trình duyệt và truy cập hệ thống", "Mở trình duyệt web và điều hướng tới: http://127.0.0.1:5000")
    ]
    
    for sname, scmd in steps_guide:
        p_step = doc.add_paragraph()
        p_step.add_run(f"{sname}:\n").bold = True
        p_step.add_run(scmd)

    # Lưu tập tin
    output_filename = "Bao_Cao_Chi_Tiet_Project_Laptop.docx"
    doc.save(output_filename)
    print(f"Đã tạo thành công file Word: {output_filename}")

if __name__ == '__main__':
    create_document()
