# Lượt bổ sung ảnh theo nhóm — 2026-10-26

Repo sạch trên feat/refresh-ui, bắt đầu từ 11ce613. Không còn xung đột main. Stash e41598b từ lượt trước vẫn được giữ.

| Chỉ số | Trước | Sau |
| --- | ---: | ---: |
| Máy có ảnh | 67 | 69 |
| Đúng SKU/model | 67 | 67 |
| Đại diện cùng dòng | 0 | 2 |
| Chưa có ảnh | 158 | 156 |
| Tệp ảnh duy nhất | 67 | 66 |

Không thêm file ảnh: dùng lại đúng tệp WebP cho hai cấu hình chỉ khác RAM. 66 tệp phục vụ 69 máy, tổng 1.887.472 byte. Kiểm tra SHA-256 phát hiện hai tệp cũ của MRX33SA/A và MRX53SA/A giống hệt từng byte; gộp tệp MRX53 vào tệp MRX33, không thay đổi nội dung hiển thị hoặc bằng chứng nguồn độc lập. 67 máy có ảnh trước lượt này giữ nguyên trạng thái, quyền và hình nhìn thấy; chỉ một đường dẫn nội bộ đổi để loại trùng.

## Phạm vi và ưu tiên

Rà toàn bộ 158 máy thiếu, cả ứng viên khác mã có cùng tên thương mại/kích thước. Nhóm bảo thủ theo model/thế hệ và đường chéo màn hình để không gộp nhầm. 17 nhóm có ảnh đã tồn tại được đối chiếu thủ công. Sau đó tìm nguồn mới cho 3 nhóm (dưới trần20), tối đa3 website/nhóm. Không tìm dàn trải từng SKU, không mở lại nguồn đã sai chỉ vì chưa có ảnh.

UM3406HA được ưu tiên vì đang ở trang chủ; S5506MA và LOQ15IAX9 vì có hai cấu hình mỗi nhóm. Đã chạy 9 hồ sơ dự đoán theo phân vị giá, tối đa5 gợi ý/hồ sơ, để tham khảo thứ tự ưu tiên. Đây là mô phỏng, không phải thống kê sử dụng thật; không có mẫu xuất hiện lặp trong 45 gợi ý. Chi tiết đầu vào/kết quả nằm trong JSON review.

## Đối chiếu dùng lại ảnh

| Nhóm | Quyết định / lý do |
| --- | --- |
| Apple MacBook Air 13 M2 (2022) · 13.6 inch | Không ghép MLY03 Silver sang MLXW3 Space Grey; Z15S chưa đủ đối chiếu màu/SKU. Không đổi ảnh Silver đã có. |
| Apple MacBook Air 15 M3 (2024) · 15.3 inch | MRYM3 Space Grey; MXD43 có nguồn chỉ Midnight, BTO Z1BR chưa xác nhận màu. Không ghép theo tên Air 15 M3. |
| Dell Gaming G15 5530 · 15.6 inch | CPU/GPU và lựa chọn màu/đèn bàn phím khác; trang Dell MY đã bỏ sản phẩm, không lấy ảnh Alienware liên quan. |
| Lenovo IdeaPad 1 15AMN7 · 15.6 inch | PSREF liệt kê Cloud Grey/Abyss Blue/Sand và nhiều CPU. Chưa đối chiếu được màu của hai MTM 82VG003E/GVN. |
| ASUS TUF Gaming F15 FX506HF · 15.6 inch | Đã xác nhận cùng FX506HF, 15.6 inch, Graphite Black, i5-11400H/RTX2050; khác RAM 8/16GB. Dùng lại ảnh HN014W. |
| ASUS Vivobook 15 OLED A1505VA · 15.6 inch | A1505VA khác CPU; trang ASUS tìm được A1505ZA thế hệ 12 không khớp VA thế hệ 13. Không dùng trang khác thế hệ làm bằng chứng. |
| ASUS Vivobook 15 X1504ZA · 15.6 inch | Cùng X1504ZA nhưng có nhiều màu; chưa xác nhận màu NJ581W với ảnh NJ517W/NJ582W. Không suy diễn màu theo tiền tố SKU. |
| ASUS Vivobook 16 M1605YA · 16 inch | M1605YA có Indie Black/Cool Silver; MB117W chưa có bằng chứng màu/ngoại hình theo SKU. Giữ placeholder. |
| Acer Aspire 7 Gaming A715-76G · 15.6 inch | A715-76G hai mã NH.QGESV/NH.QMFSV và GPU2050/3050 khác; chưa có bằng chứng đủ về thân/màu theo hai mã. |
| Apple MacBook Air 13 M1 (2020) · 13.3 inch | Đã xác nhận M1 2020, 13.3 inch, Space Grey, 8CPU/7GPU, cùng SSD256GB, khác RAM8/16GB. Dùng lại ảnh MGN63. |
| Apple MacBook Air 13 M3 (2024) · 13.6 inch | MRXN3 là Space Grey theo trang nhà bán hàng; MXCV3 là Midnight theo ảnh/nguồn đã có. Không ghép dù cùng 13.6 inch/M3. |
| Apple MacBook Pro 14 M3 (2023) · 14.2 inch | Z1C80001Y BTO chưa xác nhận được cấu hình/màu với MTL73; không coi cùng tên Pro14 M3 là bằng chứng đủ. |
| Apple MacBook Pro 14 M3 Pro (2023) · 14.2 inch | Z1AU0009U chưa xác nhận màu/BTO; khác bin CPU/GPU với MRX33. Không ghép từ Pro14 M3 thường hoặc Pro16. |
| Dell Inspiron 14 5430 · 14 inch | 5430 có nhiều CPU/màu; chưa đối chiếu được mã71015634 với ảnh71015633. Không ghép chỉ từ tên Inspiron14. |
| Dell Inspiron 15 3530 · 15.6 inch | Dell thông số 3530 có hai thân plastic/aluminum, khác kích thước/USB-C. Chưa xác nhận đủ hai mã71011772/775 dùng cùng thân/màu. |
| Dell XPS 15 9530 · 15.6 inch | XPS9530 có GPU4050/4060; thiếu bằng chứng ngoại hình/màu theo mã71015715, nên không tự ghép ảnh71015716. |
| HP ProBook 450 G10 · 15.6 inch | ProBook450 G10 có Pike Silver plastic/aluminum và tùy chọn camera; chưa xác nhận thân của873D4PA so với873D1PA. |

Hai máy được gắn nhãn “Ảnh đại diện cùng dòng”, alt/title nêu model ảnh nguồn. JSON lưu model nguồn, các máy dùng chung, đời máy, thân, màn hình, màu, khác biệt, URL bằng chứng và ngày kiểm tra. Không gán ảnh theo số dòng.

## Nguồn mới và ứng viên cần đối chiếu

### ASUS Zenbook 14 OLED UM3406HA | 14 inch

Mẫu thứ ba trên trang chủ đang thiếu ảnh; tách khỏi UX3405MA/UM3406KA.

Ảnh hãng thumbnail nhỏ và quyền cần thỏa thuận; nguồn thay thế chưa xác nhận/404.

- [UM3406HA / Jade Black / 14 inch](https://www.asus.com/laptops/for-home/zenbook/asus-zenbook-14-oled-um3406/techspec/) — opened; quyền: restricted_without_written_agreement. Trang chung gồm HA/KA/GA; không dùng ảnh KA/GA. CPU hãng8840HS khác CSV8845HS; không sửa dữ liệu.
- [UM3406HA-QL020W](https://business.currys.co.uk/catalogue/computing/laptops/windows-laptop/asus-zenbook-14-oled-um3406ha-ql020w-ai-ready-14-amd-ryzen-7-8840hs-16-gb-ram-1-tb-ssd/P306304P) — opened; quyền: not_declared. Khác hậu tố KD083W; chưa đủ kiểm chứng cấu hình/màu.
- [Nguồn](https://www.laptopmart.ae/products/asus-zenbook-14-oled-um3406) — http_404.

### ASUS Vivobook S 15 S5506MA | 15.6 inch

Hai cấu hình Ultra5/Ultra7 trong cùng mã S5506MA; ưu tiên hiệu quả theo nhóm.

Hãng cần thỏa thuận quyền ảnh; màu/SKU nguồn thay thế chưa đủ đối chiếu, nguồn thứ ba chuyển danh mục.

- [S5506 / Mist Blue](https://www.asus.com/us/laptops/for-home/vivobook/asus-vivobook-s-15-oled-s5506/) — opened; quyền: restricted_without_written_agreement. Có cả banner nhiều máy ở trang; chỉ lưu ứng viên gallery, chưa xác nhận màu MA022W/MA023W.
- [S5506MA-MA005W / Blue](https://business.currys.co.uk/catalogue/computing/laptops/windows-laptop/asus-vivobook-s-15-oled-s5506ma-15-6-laptop-intel-core-ultra-7-1-tb-ssd-blue/N661372W) — opened; quyền: not_declared. Màu Blue được nêu; chưa đối chiếu được với hậu tố022/023 trong dữ liệu.
- [Nguồn](https://www.expert-technomarkt.de/Notebooks/Asus-Vivobook-S15-S5506MA-MA005W-Quad-HD-Notebook-39%2C6-cm-15.6-Zoll-2880-x-1620-Pixel-16-GB-Ram-1-TB-SSD-Windows-11-Home-Intel-Core-i7-max.-4%2C8-GHz-Silber-Silber.17040248024.html) — redirect_to_category. Không lấy ảnh sản phẩm liên quan ở trang danh mục.

### Lenovo LOQ 15IAX9 | 15.6 inch

Hai cấu hình 83GS001RVN/UVN, cùng model/thế hệ và kích thước; không dùng ảnh LOQ15IAX9E/IRX9.

Trang hãng chưa có gallery packshot kiểm chứng/quyền; nguồn bán hàng trả placeholder và có mâu thuẫn cấu hình.

- [15IAX9](https://www.lenovo.com/us/en/p/laptops/loq-laptops/loq-15-series/lenovo-loq-15iax9/len101q0006) — opened_partial; quyền: requires_scope_review. PSREF xác nhận Luna Grey/15.6; điều khoản không cấp giấy phép bản quyền, chưa xác nhận quyền tái phân phối ảnh.
- [83GS001RVN / Luna Grey](https://cellphones.com.vn/laptop-lenovo-loq-15iax9-83gs001rvn.html) — opened; quyền: not_declared. Ảnh chính hiện là placeholder; không lấy ảnh bài đánh giá. Trang ghi12450HX/RTX3050/12GB, CSV ghi12450H/RTX2050; giữ nguyên dữ liệu.

Ảnh ASUS S5506 Mist Blue là ứng viên gallery có URL quan sát thực tế trong JSON. Chưa tải vào static: điều kiện ASUS không tự cấp quyền ảnh; còn thiếu đối chiếu màu hai SKU. Lenovo cần kiểm tra quyền/phạm vi gallery; CellphoneS trả placeholder, không lấy ảnh người dùng/review. Không kết luận trên Internet không có ảnh.

Điều khoản đã đọc: [ASUS](https://www.asus.com/terms_of_use_notice_privacy_policy/official-site/), [Apple](https://www.apple.com/legal/intellectual-property/guidelinesfor3rdparties.html), [Lenovo](https://www.lenovo.com/us/en/legal/). Không suy ra giấy phép mở từ nguồn công khai. Ảnh retailer hiện có vẫn not_declared; hai lần dùng chung kế thừa đúng trạng thái này, không được gọi là đã cấp phép.

## Kiểm tra giao diện và mã nguồn

- 21 test hồi quy/tích hợp đạt, gồm render catalogue/so sánh/gợi ý với nhãn đại diện và alt có model ảnh nguồn.
  Sau bước gộp file giống hệt, chạy lại các kiểm tra manifest, checksum, số file và quyền sử dụng.
- Desktop 1440×1000: hai cấu hình M1 hiện cùng tệp ảnh, cấu hình 16GB có nhãn đại diện;
  bản M2 chưa phù hợp vẫn dùng placeholder.
- Mobile 390×844: kho, so sánh M1/TUF và gợi ý đều hiện đầy đủ máy, object-fit contain,
  không tràn ngang toàn trang, không có lỗi console. Dự đoán thật với cấu hình HN017W trả
  16.490.000 ₫, 5 gợi ý; HN017W đứng đầu, cùng tệp ảnh và nhãn đại diện. Không dùng fixture cho kiểm tra trực quan này.
- Test chặn huấn luyện lại và so hash đầu vào; file radar phát sinh từ so sánh đã phục hồi,
  không đưa DB/CSV huấn luyện/model/biểu đồ/venv/cache vào commit.
- Chưa kiểm tra MySQL thật, thiết bị điện thoại thật và Safari/Firefox. Không xác nhận đã có giấy phép
  cho các ảnh not_declared; nguồn mới còn thiếu quyền hoặc bằng chứng được giữ ở trạng thái ứng viên.

File thay đổi: manifest/summary, inventory và hồ sơ review JSON; module metadata và component ảnh;
hai công cụ kiểm tra/báo cáo, công cụ nhóm model mới; tests, tài liệu và bốn ảnh QA.
Xóa một WebP cũ trùng byte; không thêm ảnh mới hoặc thay dữ liệu laptop.

- [Kho desktop](screenshots/shared-catalogue-desktop.png)
- [Kho điện thoại](screenshots/shared-catalogue-mobile.png)
- [So sánh điện thoại](screenshots/shared-compare-mobile.png)
- [Gợi ý sau dự đoán điện thoại](screenshots/shared-recommendation-mobile.png)

## Danh sách nhóm chưa có ảnh

Bảng dưới bao phủ đủ156 máy còn thiếu. Cột lý do giữ hồ sơ trước đây nếu chưa có phát hiện mới. Danh sách tên đầy đủ, nguồn cũ và ứng viên khác mã nằm trong data/image_family_inventory.json; nguồn/URL ảnh mới và trạng thái quyền nằm trong data/image_targeted_review.json.

| Nhóm | Máy thiếu | Lý do |
| --- | ---: | --- |
| Apple MacBook Air 13 M2 (2022) · 13.6 inch · 2 | Không ghép MLY03 Silver sang MLXW3 Space Grey; Z15S chưa đủ đối chiếu màu/SKU. Không đổi ảnh Silver đã có. |
| Apple MacBook Air 15 M3 (2024) · 15.3 inch · 2 | MRYM3 Space Grey; MXD43 có nguồn chỉ Midnight, BTO Z1BR chưa xác nhận màu. Không ghép theo tên Air 15 M3. |
| Dell Gaming G15 5530 · 15.6 inch · 2 | CPU/GPU và lựa chọn màu/đèn bàn phím khác; trang Dell MY đã bỏ sản phẩm, không lấy ảnh Alienware liên quan. |
| Lenovo IdeaPad 1 15AMN7 · 15.6 inch · 2 | PSREF liệt kê Cloud Grey/Abyss Blue/Sand và nhiều CPU. Chưa đối chiếu được màu của hai MTM 82VG003E/GVN. |
| ASUS Vivobook 15 OLED A1505VA · 15.6 inch · 1 | A1505VA khác CPU; trang ASUS tìm được A1505ZA thế hệ 12 không khớp VA thế hệ 13. Không dùng trang khác thế hệ làm bằng chứng. |
| ASUS Vivobook 15 X1504ZA · 15.6 inch · 1 | Cùng X1504ZA nhưng có nhiều màu; chưa xác nhận màu NJ581W với ảnh NJ517W/NJ582W. Không suy diễn màu theo tiền tố SKU. |
| ASUS Vivobook 16 M1605YA · 16 inch · 1 | M1605YA có Indie Black/Cool Silver; MB117W chưa có bằng chứng màu/ngoại hình theo SKU. Giữ placeholder. |
| Acer Aspire 7 Gaming A715-76G · 15.6 inch · 1 | A715-76G hai mã NH.QGESV/NH.QMFSV và GPU2050/3050 khác; chưa có bằng chứng đủ về thân/màu theo hai mã. |
| Apple MacBook Air 13 M3 (2024) · 13.6 inch · 1 | MRXN3 là Space Grey theo trang nhà bán hàng; MXCV3 là Midnight theo ảnh/nguồn đã có. Không ghép dù cùng 13.6 inch/M3. |
| Apple MacBook Pro 14 M3 (2023) · 14.2 inch · 1 | Z1C80001Y BTO chưa xác nhận được cấu hình/màu với MTL73; không coi cùng tên Pro14 M3 là bằng chứng đủ. |
| Apple MacBook Pro 14 M3 Pro (2023) · 14.2 inch · 1 | Z1AU0009U chưa xác nhận màu/BTO; khác bin CPU/GPU với MRX33. Không ghép từ Pro14 M3 thường hoặc Pro16. |
| Dell Inspiron 14 5430 · 14 inch · 1 | 5430 có nhiều CPU/màu; chưa đối chiếu được mã71015634 với ảnh71015633. Không ghép chỉ từ tên Inspiron14. |
| Dell Inspiron 15 3530 · 15.6 inch · 1 | Dell thông số 3530 có hai thân plastic/aluminum, khác kích thước/USB-C. Chưa xác nhận đủ hai mã71011772/775 dùng cùng thân/màu. |
| Dell XPS 15 9530 · 15.6 inch · 1 | XPS9530 có GPU4050/4060; thiếu bằng chứng ngoại hình/màu theo mã71015715, nên không tự ghép ảnh71015716. |
| HP ProBook 450 G10 · 15.6 inch · 1 | ProBook450 G10 có Pike Silver plastic/aluminum và tùy chọn camera; chưa xác nhận thân của873D4PA so với873D1PA. |
| ASUS Vivobook Pro 15 OLED N6506MV · 15.6 inch · 2 | not_found: 1, model_mismatch: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| ASUS Vivobook S 15 S5506MA · 15.6 inch · 2 | Hãng cần thỏa thuận quyền ảnh; màu/SKU nguồn thay thế chưa đủ đối chiếu, nguồn thứ ba chuyển danh mục. |
| Acer Nitro V 15 ANV15-51 · 15.6 inch · 2 | model_mismatch: 1, not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Acer Predator Helios 16 PH16-71 · 16 inch · 2 | not_found: 2; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Apple MacBook Pro 16 M3 Max (2023) · 16.2 inch · 2 | not_found: 2; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Apple MacBook Pro 16 M3 Pro (2023) · 16.2 inch · 2 | source_unavailable: 1, model_mismatch: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Dell Inspiron 14 5440 · 14 inch · 2 | not_found: 2; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Dell Latitude 3440 · 14 inch · 2 | not_found: 2; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| HP 15s-fq5228TU · 15.6 inch · 2 | not_found: 2; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Lenovo LOQ 15IAX9 · 15.6 inch · 2 | Trang hãng chưa có gallery packshot kiểm chứng/quyền; nguồn bán hàng trả placeholder và có mâu thuẫn cấu hình. |
| Lenovo LOQ 15IRX9 · 15.6 inch · 2 | not_found: 2; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| ASUS ExpertBook B1 B1402CBA · 14 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| ASUS ExpertBook B2 B2402CBA · 14 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| ASUS ExpertBook B5 B5402CBA · 14 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| ASUS ProArt P16 H7606WI · 16 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| ASUS ROG Flow X13 GV302XA · 13.4 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| ASUS ROG Strix G16 G614JIR · 16 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| ASUS ROG Strix G16 G614JV · 16 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| ASUS ROG Strix SCAR 16 G634JYR · 16 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| ASUS ROG Zephyrus G14 GA403UI · 14 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| ASUS ROG Zephyrus G16 GU605MI · 16 inch · 1 | access_blocked: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| ASUS TUF Gaming A15 FA506NC · 15.6 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| ASUS TUF Gaming A16 FA617NSR · 16 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| ASUS TUF Gaming A17 FA707NU · 17.3 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| ASUS TUF Gaming F15 FX507ZC4 · 15.6 inch · 1 | rights_restricted: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| ASUS TUF Gaming F16 FX607JU · 16 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| ASUS Vivobook 14X K3405VC · 14 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| ASUS Vivobook 16X K3605VC · 16 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| ASUS Vivobook S 14 OLED M5406UA · 14 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| ASUS Zenbook 14 OLED UM3406HA · 14 inch · 1 | Ảnh hãng thumbnail nhỏ và quyền cần thỏa thuận; nguồn thay thế chưa xác nhận/404. |
| ASUS Zenbook Duo UX8406MA · 14 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| ASUS Zenbook S 13 OLED UX5304MA · 13.3 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Acer Aspire 5 A514-56P · 14 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Acer Aspire 5 A515-58M · 15.6 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Acer Aspire Lite AL14-51M · 14 inch · 1 | model_mismatch: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Acer Nitro 16 Phoenix AN16-41 · 16 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Acer Nitro 5 Tiger AN515-58 · 15.6 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Acer Predator Helios Neo 16 PHN16-71 · 16 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Acer Predator Helios Neo 16 PHN16-72 · 16 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Acer Swift 14 SF14-71T · 14 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Acer Swift 3 SF314-512 · 14 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Acer Swift Go 14 SFG14-41 · 14 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Acer Swift Go 14 SFG14-71 · 14 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Acer Swift Go 14 SFG14-73 · 14 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Acer Swift Go 16 SFG16-71 · 16 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Acer Swift X SFX14-41G · 14 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Apple MacBook Air 15 M2 (2023) · 15.3 inch · 1 | rights_restricted: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Apple MacBook Pro 14 M2 Pro (2023) · 14.2 inch · 1 | rights_restricted: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Dell Gaming G16 7630 · 16 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Dell Inspiron 16 5630 · 16 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Dell Inspiron 16 Plus 7630 · 16 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Dell Latitude 3540 · 15.6 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Dell Latitude 5440 · 14 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Dell Precision 3581 · 15.6 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Dell XPS 13 9340 · 13.4 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Dell XPS 14 9440 · 14.5 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Dell XPS 16 9640 · 16.3 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Gigabyte AORUS 15 BKF · 15.6 inch · 1 | rights_restricted: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Gigabyte AORUS 16X AKG · 16 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Gigabyte AORUS 17 BSF · 17.3 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Gigabyte G5 KF · 15.6 inch · 1 | rights_restricted: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| HP 14s-em0086AU · 14 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| HP Elite Dragonfly G4 · 13.5 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| HP EliteBook 840 G10 · 14 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| HP Envy 16-h1023TX · 16 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| HP Envy x360 14-fa0045AU · 14 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| HP OMEN 16-wf0055TX · 16.1 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| HP OMEN 16-xf0071AX · 16.1 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| HP OMEN Transcend 14-fb0089TX · 14 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| HP Pavilion 14-dv2075TU · 14 inch · 1 | model_mismatch: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| HP Pavilion 15-eg3093TU · 15.6 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| HP Pavilion 15-eg3095TU · 15.6 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| HP Pavilion 15-eg3097TU · 15.6 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| HP Pavilion Plus 14-ew0014TU · 14 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| HP ProBook 440 G10 · 14 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| HP Spectre x360 14-eu0051TU · 14 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| HP Victus 15-fa1089TX · 15.6 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| HP Victus 15-fa1139TX · 15.6 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| HP Victus 15-fb1022AX · 15.6 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| HP Victus 16-r1014TX · 16.1 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| LG Gram 14 2023 14Z90R · 14 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| LG Gram 14 2024 14Z90S · 14 inch · 1 | rights_restricted: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| LG Gram 16 2023 16Z90R · 16 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| LG Gram 16 2024 16Z90S · 16 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| LG Gram 17 2023 17Z90R · 17 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| LG Gram Pro 16 2024 16Z90SP · 16 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Lenovo IdeaPad Slim 3 14IRH8 · 14 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Lenovo IdeaPad Slim 3 15ABR8 · 15.6 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Lenovo IdeaPad Slim 3 15IAH8 · 15.6 inch · 1 | source_unavailable: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Lenovo IdeaPad Slim 5 14IMH9 · 14 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Lenovo LOQ 15AHP9 · 15.6 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Lenovo LOQ 15APH8 · 15.6 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Lenovo Legion 7 16IRX9 · 16 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Lenovo Legion Pro 7 16IRX9 · 16 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Lenovo Legion Slim 5 16AHP9 · 16 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Lenovo ThinkBook 14 G6 IRL · 14 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Lenovo ThinkBook 14 G6+ IMH · 14 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Lenovo ThinkBook 16 G6 ABP · 16 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Lenovo ThinkBook 16 G6 IRL · 16 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Lenovo ThinkPad E14 Gen 5 · 14 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Lenovo ThinkPad E16 Gen 1 · 16 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Lenovo ThinkPad L14 Gen 4 · 14 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Lenovo ThinkPad L15 Gen 4 · 15.6 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Lenovo ThinkPad P16s Gen 2 · 16 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Lenovo ThinkPad T14 Gen 4 · 14 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Lenovo ThinkPad T14s Gen 4 · 14 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Lenovo ThinkPad X1 Carbon Gen 11 · 14 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Lenovo ThinkPad X1 Carbon Gen 12 · 14 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| Lenovo Yoga Pro 7 14AHP9 · 14.5 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| MSI Bravo 15 C7UDX · 15.6 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| MSI Bravo 15 C7VFK · 15.6 inch · 1 | rights_restricted: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| MSI Crosshair 16 HX D14VFKG · 16 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| MSI Cyborg 15 A13VF · 15.6 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| MSI Katana 15 B13VEK · 15.6 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| MSI Katana A15 AI B8VF · 15.6 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| MSI Modern 14 C12M · 14 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| MSI Prestige 13 Evo A13M · 13.3 inch · 1 | rights_restricted: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| MSI Prestige 16 AI Evo B1MG · 16 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| MSI Pulse 16 AI C1VGKG · 16 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| MSI Raider GE68 HX 13VG · 16 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| MSI Stealth 14 Studio A13VE · 14 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| MSI Stealth 16 Studio A13VG · 16 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| MSI Sword 16 HX B14VFK · 16 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| MSI Thin GF63 12VE · 15.6 inch · 1 | source_unavailable: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| MSI Titan 18 HX A14VIG · 18 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
| MSI Vector 16 HX A13VHG · 16 inch · 1 | not_found: 1; chưa có ảnh cùng model/thế hệ/kích thước/màu đủ bằng chứng trong kho hiện tại. Không mở nguồn mới ngoài ba nhóm đã chọn. |
