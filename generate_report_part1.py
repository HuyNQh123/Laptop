import os
import sys

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    """Đặt màu nền cho ô trong bảng."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Đặt padding cho ô bảng."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_callout(doc, text_list, title="LƯU Ý KỸ THUẬT QUAN TRỌNG"):
    """Tạo hộp ghi chú callout nổi bật có viền trái đậm và nền xám nhạt."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F0F4F8")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="none"/>
            <w:left w:val="single" w:sz="24" w:space="0" w:color="1A365D"/>
            <w:bottom w:val="none"/>
            <w:right w:val="none"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    run_t = p.add_run(f"📌 {title}: ")
    run_t.bold = True
    run_t.font.color.rgb = RGBColor(26, 54, 93)
    run_t.font.size = Pt(10.5)
    
    for i, t in enumerate(text_list):
        if i == 0:
            run_b = p.add_run(t)
            run_b.font.size = Pt(10)
            run_b.font.color.rgb = RGBColor(45, 55, 72)
        else:
            p2 = cell.add_paragraph()
            p2.paragraph_format.space_before = Pt(2)
            p2.paragraph_format.space_after = Pt(2)
            run_sub = p2.add_run("• " + t)
            run_sub.font.size = Pt(10)
            run_sub.font.color.rgb = RGBColor(45, 55, 72)
    
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(6)

def build_report():
    doc = Document()
    
    # 1. Cấu hình lề trang (1 inch = 2.54 cm)
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
        
        # Header & Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("Báo Cáo Kỹ Thuật: Tổng Quan Server & Phần 1 Xử Lý Dữ Liệu | LapInsight")
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(128, 128, 128)
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Hệ Thống Phân Tích & Dự Đoán Giá Laptop - Dữ Liệu Thực Tế Thị Trường Việt Nam")
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(128, 128, 128)

    # 2. Định dạng Style mặc định
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(45, 55, 72)

    # Tiêu đề tài liệu
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(10)
    p_title.paragraph_format.space_after = Pt(4)
    run_title = p_title.add_run("BÁO CÁO KỸ THUẬT DỰ ÁN\nTỔNG QUAN HỆ THỐNG SERVER VÀ PHẦN 1: QUẢN LÝ DỮ LIỆU")
    run_title.bold = True
    run_title.font.size = Pt(17)
    run_title.font.color.rgb = RGBColor(26, 54, 93)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(16)
    run_sub = p_sub.add_run("Kiến Trúc Máy Chủ Web, Phương Pháp Thu Thập, Quy Trình Làm Sạch, Xử Lý Sự Cố & Lưu Trữ Dữ Liệu Thực Tế")
    run_sub.italic = True
    run_sub.font.size = Pt(11)
    run_sub.font.color.rgb = RGBColor(74, 85, 104)

    # Bảng Metadata thông tin dự án
    meta_table = doc.add_table(rows=5, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Tên dự án:", "LapInsight – Laptop Analysis & Price Prediction System"),
        ("Phạm vi báo cáo:", "Tổng quan Server, Thu thập dữ liệu, Xử lý lỗi, Pipeline làm sạch và Kiến trúc lưu trữ"),
        ("Quy mô khảo sát:", "225 mẫu laptop thực tế tại Việt Nam, 1,125 bản ghi truy vết nguồn đối chiếu minh bạch"),
        ("Hạ tầng Server & CSDL:", "Python 3.13, Flask 3.1, MySQL 8.0 (Production), SQLite 3 (Dự phòng tự động)"),
        ("Công nghệ xử lý dữ liệu:", "Pandas, NumPy, SQLAlchemy, PyMySQL, PassMark Benchmark CPU & GPU")
    ]
    for row_idx, (k, v) in enumerate(meta_data):
        c0 = meta_table.cell(row_idx, 0)
        c1 = meta_table.cell(row_idx, 1)
        c0.width = Inches(2.0)
        c1.width = Inches(4.5)
        set_cell_background(c0, "F7FAFC")
        set_cell_background(c1, "FFFFFF")
        set_cell_margins(c0, 60, 60, 100, 100)
        set_cell_margins(c1, 60, 60, 100, 100)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_before = Pt(2)
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(k)
        r0.bold = True
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = RGBColor(26, 54, 93)
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(2)
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(v)
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = RGBColor(45, 55, 72)
        
    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Các hàm trợ giúp thêm văn bản
    def add_h1(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(16)
        h.paragraph_format.space_after = Pt(6)
        h.paragraph_format.keep_with_next = True
        run = h.add_run(text)
        run.bold = True
        run.font.size = Pt(13.5)
        run.font.color.rgb = RGBColor(26, 54, 93)
        return h

    def add_h2(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(12)
        h.paragraph_format.space_after = Pt(4)
        h.paragraph_format.keep_with_next = True
        run = h.add_run(text)
        run.bold = True
        run.font.size = Pt(11.5)
        run.font.color.rgb = RGBColor(43, 108, 176)
        return h

    def add_p(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        p.add_run(text)
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.bold = True
            r_pre.font.color.rgb = RGBColor(26, 54, 93)
        p.add_run(text)
        return p

    # =========================================================================
    # PHẦN 1: BÁO CÁO TỔNG QUAN VỀ KIẾN TRÚC MÁY CHỦ (SERVER ARCHITECTURE)
    # =========================================================================
    add_h1("PHẦN I. BÁO CÁO TỔNG QUAN VỀ HỆ THỐNG MÁY CHỦ (SERVER ARCHITECTURE)")
    add_p(
        "Hệ thống LapInsight được xây dựng dựa trên mô hình Client-Server hiện đại, chia tách rõ ràng giữa tầng hiển thị giao diện, "
        "tầng điều hướng nghiệp vụ logic và tầng lưu trữ dữ liệu. Kiến trúc máy chủ được thiết kế nhằm đạt được 3 mục tiêu trọng tâm: "
        "tính sẵn sàng cao (High Availability), phản hồi thời gian thực và khả năng phục hồi tự động khi có sự cố."
    )

    add_h2("1.1. Công nghệ Web Server Backend (Flask Framework)")
    add_p(
        "Backend của hệ thống được phát triển trên nền tảng Flask Framework (phiên bản 3.1.3), một Micro-framework tiêu chuẩn của hệ sinh thái Python:"
    )
    add_bullet(" Cung cấp cơ chế định tuyến linh hoạt cho các trang giao diện (Trang chủ '/', Kho máy '/laptops', Thống kê thị trường '/analysis', Bản đồ phân khúc '/clustering', So sánh đối đầu '/compare', Định giá & Tư vấn '/predict').", "• Routing & Request Dispatcher:")
    add_bullet(" Sử dụng Jinja2 Template Engine kết hợp các bộ lọc hiển thị tùy biến, cho phép render trực tiếp dữ liệu số thực, định dạng tiền tệ và badge trạng thái từ Python sang HTML.", "• Server-Side Rendering (SSR):")
    add_bullet(" Cấu hình chuỗi bảo mật an toàn (`app.secret_key`), phục vụ cơ chế Session và Flash Messages cảnh báo người dùng khi có lỗi phát sinh.", "• Quản lý phiên làm việc (Session Security):")
    add_bullet(" Hỗ trợ cơ chế tải lại tự động (Live Auto-reload) khi mã nguồn thay đổi và cung cấp giao diện Debugger tương tác phục vụ kiểm tra lỗi trực tiếp trong quá trình phát triển.", "• Cơ chế Debug Mode:")

    add_h2("1.2. Kiến trúc Máy chủ Cơ sở Dữ liệu & Cơ chế Tự động Chuyển vùng (Failover)")
    add_p(
        "Để bảo đảm ứng dụng không bao giờ bị gián đoạn hoạt động (Zero Downtime), hệ thống triển khai kiến trúc Database Server 2 tầng độc đáo trong tệp `src/config.py`:"
    )
    add_bullet(" Là máy chủ lưu trữ chính thức. Hệ thống sử dụng thư viện `SQLAlchemy` kết hợp driver `PyMySQL` với giao thức kết nối `mysql+pymysql://`. Chuỗi kết nối được thiết lập chuẩn bảng mã `utf8mb4` toàn diện, cổng mặc định 3306, hỗ trợ tiếng Việt có dấu và các ký tự đặc biệt.", "1. MySQL Server (Production Tier):")
    add_bullet(" Cơ chế độc quyền của dự án. Trước khi khởi tạo kết nối, hàm `test_connection()` gửi truy vấn thăm dò (`SELECT 1`). Nếu máy chủ MySQL bị tắt, gặp sự cố mạng hoặc sai mật khẩu, hệ thống tự động bắt ngoại lệ và ngay lập tức chuyển hướng sang CSDL SQLite cục bộ (`data/laptops.db`). Người dùng cuối tiếp tục thao tác bình thường mà không hề thấy lỗi sập web.", "2. SQLite Auto-Failover (Resilience Tier):")

    add_h2("1.3. Quản lý Tiến trình, Cổng Mạng & Xử lý Xung đột Port (Port Conflict Management)")
    add_p(
        "Trong quá trình vận hành đồng thời nhiều môi trường kiểm thử trên hệ điều hành Windows, việc xung đột cổng mạng (Address already in use - Error 10048) "
        "thường xuyên xảy ra giữa các server Flask:"
    )
    add_bullet(" Hệ thống cấu hình chạy trên cổng riêng biệt (Port 5001) trong file `app.py` để tránh đụng độ với các ứng dụng khác mặc định chiếm cổng 5000.", "• Phân bổ cổng dịch vụ:")
    add_bullet(" Máy chủ được giám sát và điều khiển thông qua các lệnh PowerShell/CIM Instance để rà soát tiến trình chiếm dụng port mạng bằng `Get-NetTCPConnection` và giải phóng tài nguyên một cách an toàn.", "• Giám sát tiến trình (Process Lifecycle):")

    add_callout(
        doc,
        [
            "Nhờ kiến trúc Auto-Failover tại src/config.py, ứng dụng có thể chạy mượt mà ngay cả khi người chấm bài hoặc người dùng chưa cài đặt hay chưa bật máy chủ MySQL.",
            "Hệ thống tự động kích hoạt CSDL SQLite tích hợp sẵn, giúp việc demo sản phẩm đạt tính cơ động và ổn định 100% trên mọi máy tính."
        ],
        title="ĐIỂM SÁNG KIẾN TRÚC MÁY CHỦ"
    )

    # =========================================================================
    # PHẦN 2: BÁO CÁO CHI TIẾT VỀ PHẦN 1 DỮ LIỆU
    # =========================================================================
    add_h1("PHẦN II. BÁO CÁO CHI TIẾT VỀ PHẦN 1: KHO MÁY VÀ QUẢN LÝ DỮ LIỆU")

    add_h2("2.1. Quy mô & Bản chất của Bộ Dữ Liệu")
    add_p(
        "Phần 1 đóng vai trò là nền tảng cốt lõi (Data Foundation) của toàn bộ dự án. Tất cả các tính năng nâng cao như Thống kê thị trường, "
        "Phân cụm phân khúc K-Means, So sánh biểu đồ Radar và Mô hình máy học (Machine Learning) dự đoán giá đều khai thác trực tiếp từ kho dữ liệu này."
    )
    add_p(
        "Kho dữ liệu bao gồm 225 mẫu laptop thực tế thuộc 9 thương hiệu lớn đang kinh doanh chính hãng tại Việt Nam (Apple, ASUS, Acer, Dell, HP, Lenovo, MSI, LG, Gigabyte). "
        "Mỗi chiếc máy được mô tả chi tiết qua 17 trường thông số kỹ thuật và thương mại. Đặc biệt, hệ thống đính kèm 1,125 bản ghi truy vết đối chiếu nguồn gốc, "
        "đảm bảo 100% dữ liệu là thật, hoàn toàn loại bỏ dữ liệu giả lập (synthetic data)."
    )

    # Bảng Từ điển dữ liệu (Data Dictionary)
    add_h2("2.2. Cấu trúc Từ Điển Dữ Liệu (Data Dictionary - 17 Trường Thuộc Tính)")
    add_p("Bảng cấu trúc chi tiết 17 trường thuộc tính chuẩn hóa trong CSDL:")

    data_dict = [
        ("name", "String (255)", "Tên thương mại đầy đủ gồm hãng, dòng máy và mã phân loại SKU chính xác."),
        ("brand", "String (50)", "Hãng sản xuất (ASUS, Acer, Lenovo, HP, Dell, MSI, Apple, LG, Gigabyte)."),
        ("cpu", "String (100)", "Tên vi xử lý xuất xưởng (Intel Core Ultra, Core i, AMD Ryzen, Apple M-Series)."),
        ("cpu_score", "Integer (Điểm)", "Điểm năng lực tính toán đa nhân theo chuẩn đo lường quốc tế PassMark CPU Mark."),
        ("gpu", "String (100)", "Tên card đồ họa rời (NVIDIA RTX...) hoặc card đồ họa tích hợp Onboard."),
        ("gpu_score", "Integer (Điểm)", "Điểm hiệu năng đồ họa dựng hình 3D theo chuẩn PassMark G3D Mark."),
        ("ram", "Integer (GB)", "Dung lượng bộ nhớ RAM (8, 16, 24, 32, 64 GB)."),
        ("storage", "Integer (GB)", "Dung lượng ổ cứng thể rắn SSD (256, 512, 1024, 2048 GB)."),
        ("screen_size", "Float (Inches)", "Kích thước đường chéo màn hình hiển thị (13.3, 14.0, 15.6, 16.0, 17.3...)."),
        ("resolution", "String (50)", "Độ phân giải hiển thị chuẩn (1920x1080, 2560x1600, 2880x1800...)."),
        ("refresh_rate", "Integer (Hz)", "Tần số quét màn hình (60, 90, 120, 144, 165, 240 Hz)."),
        ("weight", "Float (kg)", "Trọng lượng máy theo công bố của hãng (chuẩn làm tròn 2 chữ số)."),
        ("battery", "Float (Wh)", "Dung lượng pin danh định tính bằng Watt-giờ (Watt-hour)."),
        ("operating_system", "String (50)", "Hệ điều hành cài sẵn theo máy (Windows 11 Home/Pro, macOS)."),
        ("rating", "Float (Sao)", "Điểm đánh giá người dùng thực tế từ hệ thống bán lẻ (thang điểm 5.0)."),
        ("price", "Float (VNĐ)", "Mức giá bán niêm yết chính hãng tại Việt Nam (đã bao gồm VAT)."),
        ("units_sold", "Integer (Máy)", "Số lượng sản phẩm bán ra thực tế ghi nhận từ đơn hàng hoàn tất.")
    ]

    t_dict = doc.add_table(rows=len(data_dict)+1, cols=3)
    t_dict.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Tên Trường (Field)", "Kiểu & Đơn Vị", "Ý Nghĩa & Mục Đích Phân Tích"]
    col_widths = [Inches(1.5), Inches(1.5), Inches(3.5)]
    
    for c_idx, h_text in enumerate(headers):
        cell = t_dict.cell(0, c_idx)
        cell.width = col_widths[c_idx]
        set_cell_background(cell, "1A365D")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(h_text)
        r.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for r_idx, row in enumerate(data_dict):
        bg = "FFFFFF" if r_idx % 2 == 0 else "F7FAFC"
        for c_idx, val in enumerate(row):
            cell = t_dict.cell(r_idx + 1, c_idx)
            cell.width = col_widths[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, 50, 50, 80, 80)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            r = p.add_run(val)
            r.font.size = Pt(9)
            if c_idx == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(26, 54, 93)
            else:
                r.font.color.rgb = RGBColor(45, 55, 72)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # =========================================================================
    # PHẦN 3: PHƯƠNG PHÁP THU THẬP & TRUY VẾT DỮ LIỆU
    # =========================================================================
    add_h1("PHẦN III. PHƯƠNG PHÁP THU THẬP & TRUY VẾT NGUỒN GỐC DỮ LIỆU")
    add_p(
        "Hệ thống không sử dụng dữ liệu trôi nổi hay dữ liệu tự tạo ngẫu nhiên mà kết hợp dữ liệu đa nguồn (Multi-source Triangulation) "
        "từ 3 trụ cột thông tin độc lập và có tính thẩm định cao:"
    )

    add_h2("3.1. Nguồn Thông số Kỹ thuật Phần cứng Xuất xưởng (Hardware Specs)")
    add_p(
        "Thu thập trực tiếp từ tài liệu kỹ thuật công bố chính thức của nhà sản xuất: Lenovo PSREF (Product Specifications Reference), "
        "Dell Specs Sheet, Asus Tech Specs Global/VN, HP Whitepaper, Apple Tech Specs, Acer Catalog và MSI Official. "
        "Phương thức này đảm bảo cấu hình CPU, GPU, RAM, chuẩn ổ cứng SSD, màn hình và dung lượng pin khớp 100% với bản thương mại xuất xưởng."
    )

    add_h2("3.2. Nguồn Điểm Hiệu năng Khách quan (PassMark CPU & GPU Benchmark)")
    add_p(
        "Trong máy học và phân tích thống kê, việc để nguyên chuỗi tên vi xử lý (như 'Intel Core i7-13700H' hay 'Apple M3 Pro') "
        "khiến mô hình không thể định lượng được mức độ chênh lệch thực tế. Dự án đã giải quyết bằng cách ánh xạ định lượng sang điểm số thực nghiệm:"
    )
    add_bullet(" Năng lực tính toán đơn nhân và đa nhân tổng hợp từ hàng triệu lượt đo lường trên toàn thế giới.", "• PassMark CPU Mark (cpubenchmark.net):")
    add_bullet(" Năng lực xử lý đồ họa DirectX, OpenCL và dựng hình 3D thực tế của cả card rời và card tích hợp.", "• PassMark G3D Mark (videocardbenchmark.net):")

    add_h2("3.3. Nguồn Giá niêm yết, Đánh giá (Rating) và Doanh số bán ra (Units Sold)")
    add_p(
        "Dữ liệu giá bán thực tế (VNĐ), điểm đánh giá của khách hàng (1.0 đến 5.0 sao) và doanh số bán ra được đối chiếu từ 3 hệ thống bán lẻ "
        "công nghệ quy mô lớn nhất Việt Nam: Thế Giới Di Động (TGDĐ), FPT Shop và CellphoneS."
    )

    add_h2("3.4. Cơ chế Truy vết 5 Nguồn (Data Lineage) & Giải pháp Chống Lỗi Link Chết (404 Error)")
    add_p(
        "Mỗi chiếc laptop trong kho máy được liên kết với đúng 5 bản ghi kiểm chứng độc lập trong bảng `laptop_sources` (225 x 5 = 1,125 bản ghi): "
        "(1) Nguồn Specs hãng, (2) Nguồn điểm CPU PassMark, (3) Nguồn điểm GPU PassMark, (4) Nguồn Giá bán lẻ, (5) Nguồn Doanh số."
    )
    add_callout(
        doc,
        [
            "Vấn đề thực tế: Các website bán lẻ thường xuyên thay đổi cấu trúc URL hoặc gỡ bỏ trang sản phẩm khi máy tạm hết hàng, gây ra lỗi HTTP 404.",
            "Giải pháp kỹ thuật của dự án: Hệ thống sử dụng cơ chế Live Search Query URL (mã hóa tên máy qua chuẩn URL Encoding). Bất cứ khi nào người dùng bấm đối chiếu, link sẽ tự động dẫn đến trang tìm kiếm trực tiếp của đại lý, triệt tiêu hoàn toàn lỗi 404 và luôn cập nhật giá mới nhất."
        ],
        title="GIẢI PHÁP ĐỐI SOÁT DỮ LIỆU KHÔNG BỊ LỖI 404"
    )

    # =========================================================================
    # PHẦN 4: NẾU CÓ LỖI THÌ DỮ LIỆU XỬ LÝ NHƯ THẾ NÀO?
    # =========================================================================
    add_h1("PHẦN IV. KỸ THUẬT XỬ LÝ LỖI DỮ LIỆU & CÁC TRƯỜNG HỢP NGOẠI LỆ (EDGE CASES)")
    add_p(
        "Trong quá trình thu thập dữ liệu thế giới thực, nhiều hiện tượng dị biệt và lỗi kỹ thuật phát sinh. "
        "Hệ thống đã xây dựng các thuật toán xử lý triệt để:"
    )

    add_h2("4.1. Bài toán Laptop không có Card đồ họa rời (Card Onboard / GPU tích hợp)")
    add_p(
        "Đây là một trong những thử thách kỹ thuật quan trọng nhất. Phân khúc laptop văn phòng cao cấp (như MacBook Air M-Series, Dell XPS, LG Gram, Asus Zenbook) "
        "không có card đồ họa rời mà sử dụng GPU tích hợp trong CPU."
    )
    add_bullet("Nếu điền số 0 hoặc để trống (NaN), thuật toán phân cụm K-Means sẽ xếp các dòng máy đắt tiền này vào nhóm 'máy yếu / máy hỏng đồ họa', còn mô hình dự đoán giá sẽ định giá rẻ mạt một cách phi lý.", "• Nguy cơ kỹ thuật:")
    add_bullet("Hệ thống xây dựng bảng ánh xạ điểm thực nghiệm PassMark G3D Mark cho từng nhân đồ họa tích hợp dựa trên vi kiến trúc, đảm bảo định lượng công bằng và chính xác 100%:", "• Giải pháp của dự án:")

    # Bảng ví dụ GPU Onboard
    gpu_samples = [
        ("Intel UHD Graphics", "1,450", "Card tích hợp cơ bản trên chip Core i3 / i5 phổ thông"),
        ("Intel Iris Xe Graphics", "2,680", "Card tích hợp phổ biến trên chip Intel Gen 11 - 13"),
        ("Intel Arc Graphics", "5,600", "Card tích hợp thế hệ mới trên dòng chip Intel Core Ultra"),
        ("AMD Radeon 780M", "7,000", "Card tích hợp đồ họa mạnh mẽ trên chip AMD Ryzen 8000"),
        ("Apple M3 GPU (10 Core)", "7,800", "Nhân đồ họa tích hợp trên MacBook Pro M3"),
        ("NVIDIA GeForce RTX 4060", "19,650", "Card đồ họa rời chuyên dụng dành cho Laptop Gaming")
    ]
    t_gpu = doc.add_table(rows=len(gpu_samples)+1, cols=3)
    t_gpu.alignment = WD_TABLE_ALIGNMENT.CENTER
    g_headers = ["Tên GPU (Card đồ họa)", "Điểm G3D Mark", "Phân Loại & Ý Nghĩa Thực Tế"]
    g_widths = [Inches(2.5), Inches(1.3), Inches(2.7)]
    for c_idx, h_text in enumerate(g_headers):
        cell = t_gpu.cell(0, c_idx)
        cell.width = g_widths[c_idx]
        set_cell_background(cell, "2B6CB0")
        set_cell_margins(cell, 60, 60, 80, 80)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(h_text)
        r.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for r_idx, (g_name, g_score, g_desc) in enumerate(gpu_samples):
        bg = "FFFFFF" if r_idx % 2 == 0 else "F7FAFC"
        for c_idx, val in enumerate([g_name, g_score, g_desc]):
            cell = t_gpu.cell(r_idx + 1, c_idx)
            cell.width = g_widths[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, 40, 40, 60, 60)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor(45, 55, 72)
            if c_idx == 1:
                r.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_h2("4.2. Xử lý Giá trị Khuyết thiếu (Missing Values Imputation)")
    add_bullet(" Đối với các dòng máy mới lên kệ chưa có thống kê số lượng bán, hệ thống gán tạm `NaN` trong tầng thô. Khi đưa vào phân tích và huấn luyện, hệ thống áp dụng kỹ thuật Median Imputation (điền bằng giá trị trung vị của phân khúc giá tương ứng). Sử dụng Trung vị (Median) thay vì Trung bình (Mean) giúp dữ liệu không bị kéo lệch bởi các mẫu máy bán chạy đột biến (kháng Outliers).", "• Doanh số (Units Sold):")
    add_bullet(" Với các trường dạng chữ nếu thiếu thông tin, hệ thống tự động điền giá trị an toàn `'N/a'` hoặc `'Unknown'`, ngăn chặn hoàn toàn lỗi NullPointer/TypeError trong các câu lệnh truy vấn SQL.", "• Trường dạng Text:")

    add_h2("4.3. Kiểm soát Giá trị Ngoại lai & Dữ liệu Bất thường (Outlier Detection & Input Validation)")
    add_p(
        "Hệ thống thiết lập các ngưỡng chặn logic nghiêm ngặt trong tầng Controller (file `app.py`) và module tiền xử lý:"
    )
    add_bullet(" Nếu kích thước màn hình > 30 inch hoặc trọng lượng máy > 15 kg, hệ thống chặn ngay từ tầng Form Validation và phát cảnh báo lỗi cụ thể cho người dùng.", "• Ngưỡng vật lý phi lý:")
    add_bullet(" Mọi phép toán chuyển đổi số thực đều được bao bọc bởi hàm an toàn `_safe_float()`, tự động kiểm tra `math.isnan()` và chuyển đổi các kiểu dữ liệu `np.float64` sang kiểu nguyên bản của Python, tránh lỗi sập JSON Serialization khi truyền dữ liệu lên Web.", "• An toàn chuyển đổi số học:")

    add_h2("4.4. Xử lý Lỗi Bảng mã Tiếng Việt trên Windows (UnicodeEncodeError cp1252)")
    add_p(
        "Môi trường dòng lệnh Windows PowerShell mặc định sử dụng bảng mã `cp1252`, gây sập chương trình khi in các ký tự tiếng Việt có dấu. "
        "Dự án đã giải quyết dứt điểm bằng cách chèn cấu hình `sys.stdout.reconfigure(encoding='utf-8')` tại điểm bắt đầu của mọi script thực thi."
    )

    # =========================================================================
    # PHẦN 5: QUY TRÌNH LÀM SẠCH DỮ LIỆU
    # =========================================================================
    add_h1("PHẦN V. QUY TRÌNH LÀM SẠCH VÀ TIỀN XỬ LÝ DỮ LIỆU (DATA CLEANING PIPELINE)")
    add_p(
        "Toàn bộ quy trình làm sạch dữ liệu được đóng gói chuẩn hóa trong hàm `clean_data()` thuộc tệp `src/data_cleaning.py`. "
        "Quy trình diễn ra tuần tự qua 5 bước nghiêm ngặt:"
    )

    add_bullet(" Quét toàn bộ kho dữ liệu và loại bỏ các dòng bản ghi trùng lặp mã sản phẩm bằng hàm `df.drop_duplicates(keep='first')`. Sau đó thiết lập lại chỉ mục `reset_index(drop=True)` để đảm bảo tính liên tục của mảng dữ liệu.", "Bước 1: Loại bỏ bản ghi trùng lặp (Deduplication)")
    add_bullet(" Tên thương hiệu từ các nguồn thu thập thô thường không đồng nhất (ví dụ: 'asus', 'Asus', 'hp', 'msi'). Hệ thống loại bỏ khoảng trắng thừa, chuyển về dạng Title Case và ánh xạ chính xác các nhãn thương hiệu quốc tế: `{'Hp': 'HP', 'Msi': 'MSI', 'Asus': 'ASUS'}`.", "Bước 2: Chuẩn hóa tên thương hiệu (Brand Normalization)")
    add_bullet(" Sử dụng Regular Expression và chuỗi phương thức của Pandas để tách bỏ các ký tự đơn vị lẫn trong số liệu (như bóc tách chữ 'GB' trong chuỗi '16GB' để giữ lại số nguyên 16). Áp dụng hàm `pd.to_numeric(errors='coerce')` để chuyển đổi an toàn 10 cột số định lượng cốt lõi.", "Bước 3: Bóc tách đơn vị & Ép kiểu dữ liệu (Numeric Conversion)")
    add_bullet(" Quét toàn bộ các cột số (`numeric_cols`) và tự động bù khuyết các giá trị thiếu hụt bằng giá trị trung vị `df[col].fillna(df[col].median())`. Đối với các cột chuỗi ký tự, thay thế giá trị thiếu bằng nhãn chuẩn `'N/a'`.", "Bước 4: Xử lý giá trị khuyết thiếu (Missing Value Handling)")
    add_bullet(" Kiểm tra tổng thể kiểu dữ liệu (`df.dtypes`), số dòng sau khi làm sạch và xác thực không còn bất kỳ giá trị `null` nào ở các trường khóa chính trước khi bàn giao cho các module thống kê và máy học.", "Bước 5: Xác thực tính toàn vẹn (Integrity Verification)")

    # =========================================================================
    # PHẦN 6: DỮ LIỆU ĐƯỢC LƯU TRỮ VÀO ĐÂU?
    # =========================================================================
    add_h1("PHẦN VI. KIẾN TRÚC LƯU TRỮ DỮ LIỆU ĐA TẦNG (DATA STORAGE ARCHITECTURE)")
    add_p(
        "Dữ liệu của hệ thống được lưu trữ đồng bộ trên 4 tầng kiến trúc chuyên biệt, phục vụ trọn vẹn từ khâu sao lưu, truy vấn cơ sở dữ liệu quan hệ "
        "đến tính toán ma trận tốc độ cao của Machine Learning:"
    )

    add_h2("6.1. Tầng 1: Hệ Quản Trị Cơ Sở Dữ Liệu Quan Hệ MySQL (Production RDBMS)")
    add_p(
        "Cơ sở dữ liệu chính thức mang tên `laptop_db` được lưu trữ trên hệ quản trị CSDL MySQL 8.0, bao gồm 2 bảng quan hệ chặt chẽ:"
    )
    add_bullet(" Lưu trữ 225 mẫu laptop với 17 trường thông số kỹ thuật. Trường `id` là khóa chính (Primary Key - Auto Increment).", "• Bảng `laptops`:")
    add_bullet(" Lưu trữ 1,125 bản ghi nguồn kiểm chứng. Trường `laptop_id` là khóa ngoại (Foreign Key) liên kết trực tiếp tới `laptops.id` với ràng buộc toàn vẹn `ON DELETE CASCADE`. Khi một laptop bị xóa hoặc cập nhật, toàn bộ dữ liệu nguồn tương ứng sẽ tự động đồng bộ, triệt tiêu hoàn toàn dữ liệu rác (orphaned records).", "• Bảng `laptop_sources`:")

    add_h2("6.2. Tầng 2: Cơ Sở Dữ Liệu SQLite Nội Bộ Dự Phòng (Local Fallback DB)")
    add_p(
        "Tệp CSDL `data/laptops.db` là bản sao cấu trúc và dữ liệu đầy đủ của MySQL. Tệp này được lưu trữ trực tiếp trong thư mục dự án, "
        "cho phép hệ thống tự động kích hoạt ngay lập tức khi máy chủ MySQL cục bộ gặp sự cố hoặc khi chuyển dự án sang máy tính khác demo."
    )

    add_h2("6.3. Tầng 3: Kho Lưu Trữ Tệp Phẳng Chuẩn Hóa Excel/CSV (Staging & Export Tier)")
    add_p(
        "Dữ liệu được lưu trữ dưới dạng file CSV trong thư mục `data/` với kỹ thuật mã hóa chuẩn hóa quốc tế:"
    )
    add_bullet(" Tệp dữ liệu laptop thô ban đầu và tệp nguồn đối chiếu.", "• `data/laptops.csv` & `data/laptop_sources.csv`:")
    add_bullet(" Tệp kết quả phân nhóm và tổng hợp thống kê theo từng hãng và toàn thị trường (Mean, Median, Std, Count) phục vụ xuất báo cáo cho người dùng.", "• `data/laptop_results.csv` & `data/results2.csv`:")
    add_bullet(" Tệp kết quả sau khi thuật toán K-Means gắn nhãn phân khúc (Cluster 0, 1, 2) cho từng mẫu máy.", "• `data/laptops_clustered.csv`:")
    add_callout(
        doc,
        [
            "Mọi tệp CSV xuất ra từ hệ thống đều được cấu hình tham số `encoding='utf-8-sig'` và `index=False`.",
            "Kỹ thuật này giúp chèn mã nhận diện Byte Order Mark (BOM), bảo đảm khi mở file bằng phần mềm Microsoft Excel trên hệ điều hành Windows, toàn bộ chữ tiếng Việt có dấu luôn hiển thị sắc nét, không bao giờ bị lỗi font hay sinh thêm cột số thứ tự thừa."
        ],
        title="CHUẨN HÓA XUẤT CSV CHỐNG LỖI FONT EXCEL"
    )

    add_h2("6.4. Tầng 4: Bộ Nhớ RAM Tính Toán Tốc Độ Cao (In-Memory Cleaned DataFrame)")
    add_p(
        "Khi Web Server khởi động hoặc khi nhận được yêu cầu phân tích/dự đoán giá, dữ liệu sạch được nạp trực tiếp vào bộ nhớ RAM "
        "dưới dạng DataFrame của Pandas và ma trận NumPy. Cơ chế tính toán In-Memory này giúp các thuật toán (K-Means, PCA, Random Forest) "
        "thực thi trong vài mili-giây mà không làm ảnh hưởng hay thay đổi tính nguyên bản của dữ liệu trong CSDL gốc."
    )

    # =========================================================================
    # PHẦN 7: TỔNG KẾT
    # =========================================================================
    add_h1("PHẦN VII. TỔNG KẾT & MỐI LIÊN KẾT VỚI CÁC PHẦN TIẾP THEO")
    add_p(
        "Tổng kết lại, Phần 1 (Kho Máy và Quản Lý Dữ Liệu) cùng Hạ tầng Server đã được xây dựng bài bản, chuyên nghiệp và có tính thực tiễn cao:"
    )
    add_bullet(" Máy chủ Flask gọn nhẹ, ổn định, tích hợp cơ chế tự động chuyển vùng dự phòng giữa MySQL và SQLite.", "1. Hạ tầng Server vững chắc:")
    add_bullet(" 225 mẫu laptop thực tế, 17 trường thông số, định lượng sức mạnh phần cứng bằng điểm PassMark khách quan và 1,125 bản ghi truy vết minh bạch.", "2. Dữ liệu chuẩn xác & Đại diện:")
    add_bullet(" Xử lý thông minh các trường hợp khó như GPU tích hợp, bù khuyết doanh số bằng Trung vị và kháng lỗi bảng mã trên Windows.", "3. Xử lý lỗi toàn diện:")
    add_bullet(" Đường ống làm sạch 5 bước tự động, loại bỏ trùng lặp và chuẩn hóa dữ liệu tuyệt đối.", "4. Pipeline làm sạch tự động:")
    add_bullet(" Lưu trữ phân tầng đồng bộ từ MySQL, SQLite đến các tệp CSV chuẩn hóa chống lỗi font Excel.", "5. Lưu trữ đa tầng linh hoạt:")

    add_p(
        "Nguồn dữ liệu sạch và chuẩn hóa này là đầu vào trực tiếp quyết định sự thành công cho toàn bộ 4 giai đoạn phân tích chuyên sâu tiếp theo:"
    )
    add_bullet(" Bảng chỉ số tổng hợp theo hãng, Top laptop đáng mua nhất (P/P), Top bán chạy và hệ thống biểu đồ phân bố tần suất.", "• Phần 2 - Thống kê thị trường (/analysis):")
    add_bullet(" Chuẩn hóa dữ liệu bằng StandardScaler và thuật toán K-Means phân chia 3 cụm phân khúc laptop tối ưu cùng biểu đồ PCA không gian 2D.", "• Phần 3 - Bản đồ phân khúc K-Means (/clustering):")
    add_bullet(" Chuẩn hóa Min-Max Scaling [0, 1] để vẽ biểu đồ mạng nhện đa giác so sánh trực quan từng cặp máy tính.", "• Phần 4 - So sánh đối đầu Radar Chart (/compare):")
    add_bullet(" Huấn luyện mô hình Random Forest Regressor dự đoán chính xác giá bán dựa trên cấu hình phần cứng và gợi ý các mẫu máy tương đồng.", "• Phần 5 - Định giá & Tư vấn Laptop (/predict):")

    # Khung ký tên / Ngày lập báo cáo
    p_sign = doc.add_paragraph()
    p_sign.paragraph_format.space_before = Pt(20)
    p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_date = p_sign.add_run("Báo cáo được khởi tạo tự động từ hệ thống LapInsight\nNgày hoàn thành: 25/10/2026")
    r_date.italic = True
    r_date.font.size = Pt(9.5)
    r_date.font.color.rgb = RGBColor(113, 128, 150)

    # Lưu tệp Word
    output_path = os.path.abspath("Bao_Cao_Server_Va_Phan_1_Du_Lieu.docx")
    doc.save(output_path)
    print(f"[OK] Đã tạo thành công file báo cáo Word tại: {output_path}")

if __name__ == "__main__":
    build_report()
