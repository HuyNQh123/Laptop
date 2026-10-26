# Kiểm tra ảnh catalogue — 2026-10-26

Danh sách 225 laptop, 225 khóa tên duy nhất. Nhóm thử 13 mẫu đã được xem ảnh và kiểm tra trên web trước khi mở rộng; 11 mẫu còn sử dụng được sau khi thay/loại nguồn có hạn chế.

| Kết quả | Số laptop |
| --- | ---: |
| Ảnh đúng mã model trên trang nguồn | 67 |
| Ảnh đại diện cùng dòng đã xác nhận | 2 |
| Chưa có ảnh | 156 |

Đã tìm nguồn mới cho toàn bộ 225 tên, tìm lại các mã còn thiếu bằng SKU ngắn, và thử mở 181 trang sản phẩm (có thể lặp URL giữa cấu hình). Không kết luận mã chưa xác minh là không có ảnh trên mạng.

Ảnh WebP: 1,887,472 byte; tối đa 1000×1000 px, thu nhỏ theo tỷ lệ, không upscale/crop/AI. Hai ảnh chụp có bối cảnh cũ đã được thay bằng ảnh catalogue cho đúng MLY03SA/A và MTL73SA/A.

Có 66 tệp ảnh duy nhất phục vụ 69 máy. Xem lượt đối chiếu cùng ngoại hình tại [targeted-image-pass.md](targeted-image-pass.md).

## Quyền sử dụng

Độ khớp model và quyền sử dụng là hai trường riêng. Các ảnh đang hiển thị có nguồn sản phẩm, nhưng trang nguồn không công bố giấy phép tái sử dụng/mở. `not_declared` không phải xác nhận được cấp phép; không gắn nhãn CC/public domain. Thông báo copyright được giữ trong `rights_notices`. Các nguồn ghi All rights reserved đã bị loại; MRX33SA/A dùng nguồn An Khang thay thế, MQKP3SA/A còn thiếu ảnh. Toàn bộ ảnh lấy từ HACOM bị loại sau khi đọc chính sách ảnh riêng tại https://hacom.vn/ban-quyen-hinh-anh. Các nguồn bị loại và nguồn thay thế nằm trong source_rejections. Phạm vi kiểm tra gồm nội dung công khai trên trang sản phẩm và chính sách riêng đã mở; không suy diễn quyền từ HTTP 200.

## Các trường hợp dữ liệu cần nhóm đối chiếu

Giữ nguyên CSV, cơ sở dữ liệu, giá và đặc trưng ML. Một số SKU có cấu hình khác CSV; ảnh đối chiếu theo SKU, dòng, thế hệ và ngoại hình, không dùng ảnh để sửa dữ liệu. Những tên biến thể mâu thuẫn (HP dv2075TU/dv2073TU, Acer 59G4/36PN) tiếp tục thiếu ảnh.

- ASUS Zenbook 14 OLED UX3405MA-PP152W: Mã SKU trên trang khớp tên dữ liệu, nhưng cấu hình CPU/RAM hoặc SSD trên trang khác CSV. Ảnh lấy theo SKU và ngoại hình; không sửa dữ liệu hay đặc trưng ML.
- ASUS Zenbook 14 OLED UX3405MA-PP151W: Mã SKU trên trang khớp tên dữ liệu, nhưng cấu hình CPU/RAM hoặc SSD trên trang khác CSV. Ảnh lấy theo SKU và ngoại hình; không sửa dữ liệu hay đặc trưng ML.
- ASUS Vivobook 15 X1504ZA-NJ582W: Mã SKU trên trang khớp tên dữ liệu, nhưng cấu hình CPU/RAM hoặc SSD trên trang khác CSV. Ảnh lấy theo SKU và ngoại hình; không sửa dữ liệu hay đặc trưng ML.
- ASUS Vivobook Go 14 E1404FA-NK177W: Mã SKU trên trang khớp tên dữ liệu, nhưng cấu hình CPU/RAM hoặc SSD trên trang khác CSV. Ảnh lấy theo SKU và ngoại hình; không sửa dữ liệu hay đặc trưng ML.
- HP Victus 16-s0078AX 8C5N7PA: Mã SKU trên trang khớp tên dữ liệu, nhưng cấu hình CPU/RAM hoặc SSD trên trang khác CSV. Ảnh lấy theo SKU và ngoại hình; không sửa dữ liệu hay đặc trưng ML.

## Ảnh đại diện dùng chung

| Laptop | Model ảnh nguồn | Tệp dùng chung | Bằng chứng |
| --- | --- | --- | --- |
| Apple MacBook Air 13 M1 (2020) 16GB 256GB Z124000DE | Apple MacBook Air 13 M1 (2020) 8GB 256GB MGN63SA/A | images/laptops/346564c20846a678.webp | Apple Support M1 2020 xác nhận màn hình 13.3 inch, cùng kích thước vỏ và tùy chọn RAM 8/16GB. Trang Tân Hưng Phát ghi đúng Z124000DE, 16GB/256GB, M1 8CPU/7GPU, màu Xám; nguồn MGN63 đang có ghi Space Grey. Đã xem lại ảnh catalogue nguồn, cùng thân nhôm hình nêm M1, không dùng ảnh Air M2/M3 hay Pro. |
| ASUS TUF Gaming F15 FX506HF-HN017W | ASUS TUF Gaming F15 FX506HF-HN014W | images/laptops/616dfc4fb10503be.webp | ASUS techspec xác nhận FX506HF thuộc TUF F15 FX506, 15.6 inch. SP-One URL kết thúc HN014W nhưng tiêu đề và cấu hình thực tế là HN017W, RAM 16GB, i5-11400H/RTX2050, Graphite Black. Nguồn Laptopnew của HN014W ghi RAM 8GB và màu Xám Đen (Grey). Đối chiếu cùng FX506HF/thế hệ/kích thước, chỉ khác RAM; đã xem lại ảnh nguyên máy nền trắng. |

## Nguyên nhân còn thiếu

| Nguyên nhân chính | Số laptop |
| --- | ---: |
| Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | 135 |
| Sai hoặc mâu thuẫn model | 5 |
| Bị chặn truy cập (403/429) | 3 |
| Lỗi tải/giải mã ảnh hoặc ảnh quá nhỏ | 0 |
| Lỗi truy cập nguồn (SSL/timeout/404) | 3 |
| Nguồn có hạn chế quyền sử dụng | 10 |

Mỗi máy có một nguyên nhân chính; toàn bộ lần thử, chuyển hướng, mã HTTP và lỗi cụ thể nằm trong `data/laptop_images.json`. Ảnh banner/ghép/nền trang trí bị loại được ghi rõ trong ghi chú.

| Laptop | Nguyên nhân | Ghi chú |
| --- | --- | --- |
| ASUS Zenbook 14 OLED UM3406HA-KD083W | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| ASUS Zenbook S 13 OLED UX5304MA-NQ047W | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| ASUS Zenbook Duo UX8406MA-PZ141W | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| ASUS Vivobook 14X K3405VC-KM083W | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| ASUS Vivobook 16X K3605VC-MB083W | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| ASUS Vivobook Pro 15 OLED N6506MV-MA025W | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| ASUS Vivobook S 14 OLED M5406UA-PP046W | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| ASUS TUF Gaming F15 FX507ZC4-HN095W | Nguồn có hạn chế quyền sử dụng | Nguồn ảnh đã đối chiếu có hạn chế sử dụng rõ ràng; chưa xác minh được ảnh đạt chuẩn từ nguồn thay thế. Giữ Chưa có ảnh. |
| ASUS TUF Gaming A15 FA506NC-HN012W | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| ASUS TUF Gaming F16 FX607JU-N3133W | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| ASUS ROG Strix G16 G614JV-N3090W | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| ASUS ROG Strix G16 G614JIR-N4011W | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| ASUS ROG Zephyrus G14 GA403UI-QS038W | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| ASUS ROG Zephyrus G16 GU605MI-QR038W | Bị chặn truy cập (403/429) | Nguồn mới trả HTTP 403/429; chưa truy cập được gallery để xác minh ảnh. Không kết luận trên mạng không có ảnh. |
| ASUS ROG Strix SCAR 16 G634JYR-RA067W | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| ASUS ROG Flow X13 GV302XA-MU009W | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| ASUS ExpertBook B1 B1402CBA-NK3154W | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| ASUS ExpertBook B5 B5402CBA-KI0244W | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| ASUS Vivobook 15 OLED A1505VA-L1357W | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| ASUS ProArt P16 H7606WI-ME048W | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| ASUS TUF Gaming A16 FA617NSR-RL058W | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Lenovo IdeaPad Slim 3 15IAH8 83ER000EVN | Lỗi truy cập nguồn (SSL/timeout/404) | Nguồn mới lỗi truy cập hoặc không cung cấp được ảnh gallery đủ độ nét; xem chi tiết lần thử. |
| Lenovo IdeaPad Slim 5 14IMH9 83DA001SVN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Lenovo LOQ 15IAX9 83GS001RVN | Nguồn có hạn chế quyền sử dụng | Nguồn ảnh đã đối chiếu có hạn chế sử dụng rõ ràng; chưa xác minh được ảnh đạt chuẩn từ nguồn thay thế. Giữ Chưa có ảnh. |
| Lenovo LOQ 15IAX9 83GS001UVN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Lenovo LOQ 15IRX9 83DV003UVN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Lenovo LOQ 15AHP9 83DX003CVN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Lenovo Legion Pro 7 16IRX9 83DE001RVN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Lenovo ThinkBook 14 G6+ IMH 21KW003KVN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Lenovo ThinkBook 16 G6 IRL 21KH0065VN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Lenovo ThinkPad E14 Gen 5 21JK0067VN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Lenovo ThinkPad E16 Gen 1 21JN0069VN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Lenovo ThinkPad T14 Gen 4 21HD0050VN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Lenovo ThinkPad X1 Carbon Gen 11 21HM000EVN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Dell Inspiron 14 5430 71015634 | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Dell Inspiron 16 5630 71011408 | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Dell Inspiron 16 Plus 7630 71011409 | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Dell Latitude 3440 71015637 | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Dell Latitude 5440 71015638 | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Dell XPS 13 9340 71034448 | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Dell XPS 14 9440 71034449 | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Dell XPS 16 9640 71034450 | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Dell Gaming G15 5530 i5 13450HX RTX 3050 | Bị chặn truy cập (403/429) | Nguồn mới trả HTTP 403/429; chưa truy cập được gallery để xác minh ảnh. Không kết luận trên mạng không có ảnh. |
| Dell Gaming G15 5530 i7 13650HX RTX 4050 | Bị chặn truy cập (403/429) | Nguồn mới trả HTTP 403/429; chưa truy cập được gallery để xác minh ảnh. Không kết luận trên mạng không có ảnh. |
| HP 14s-em0086AU 8R447PA | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| HP 15s-fq5228TU 8U236PA | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| HP Pavilion 14-dv2075TU 7C0P2PA | Sai hoặc mâu thuẫn model | Trang có mã 7C0P2PA nhưng ghi dv2073TU, khác tên dv2075TU trong dữ liệu; chưa xác nhận được biến thể. |
| HP Pavilion 15-eg3093TU 8U232PA | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| HP Pavilion Plus 14-ew0014TU 8C593PA | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| HP Envy x360 14-fa0045AU A19AFPA | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| HP Spectre x360 14-eu0051TU 9Y355PA | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| HP ProBook 440 G10 873A7PA | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| HP EliteBook 840 G10 873J2PA | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| HP Victus 15-fa1089TX 896X7PA | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| HP Victus 15-fa1139TX 9E394PA | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| HP OMEN 16-wf0055TX 81S89PA | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| HP OMEN Transcend 14-fb0089TX 9Z861PA | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Acer Aspire 5 A514-56P-5026 NX.KHRSV.002 | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Acer Aspire Lite AL14-51M-59G4 NX.KTWSV.001 | Sai hoặc mâu thuẫn model | Trang có mã NX.KTWSV.001 nhưng là 36PN, không phải 59G4 trong dữ liệu; không ghép ảnh theo mã linh kiện mâu thuẫn. |
| Acer Swift Go 14 SFG14-71-59W6 NX.KF5SV.004 | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Acer Swift Go 14 SFG14-73-718T NX.KSLSV.001 | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Acer Nitro 5 Tiger AN515-58-577Z NH.QFHSV.00C | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Acer Nitro V 15 ANV15-51-57B2 NH.QNASV.001 | Sai hoặc mâu thuẫn model | Trang tìm được chuyển hướng hoặc không xác nhận đúng mã model; không lấy ảnh sản phẩm khác. |
| Acer Nitro V 15 ANV15-51-58H9 NH.QNASV.003 | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Acer Nitro 16 Phoenix AN16-41-R5M4 NH.QLKSV.001 | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Acer Predator Helios Neo 16 PHN16-71-779X NH.QLUSV.007 | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Acer Predator Helios 16 PH16-71-948L NH.QJSSV.002 | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Apple MacBook Air 13 M2 (2022) 8GB 256GB MLXW3SA/A | Nguồn có hạn chế quyền sử dụng | Nguồn ảnh đã đối chiếu có hạn chế sử dụng rõ ràng; chưa xác minh được ảnh đạt chuẩn từ nguồn thay thế. Giữ Chưa có ảnh. |
| Apple MacBook Air 13 M2 (2022) 16GB 512GB Z15S00036 | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Apple MacBook Air 15 M2 (2023) 8GB 256GB MQKP3SA/A | Nguồn có hạn chế quyền sử dụng | Ảnh đúng SKU từ HugoTech bị loại vì trang ghi All rights reserved. Chưa có ảnh từ nguồn thay thế phù hợp. |
| Apple MacBook Air 13 M3 (2024) 8GB 256GB MRXN3SA/A | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Apple MacBook Air 15 M3 (2024) 16GB 512GB MXD43SA/A | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Apple MacBook Pro 16 M3 Pro (2023) 18GB 512GB MRW13SA/A | Lỗi truy cập nguồn (SSL/timeout/404) | Nguồn mới lỗi truy cập hoặc không cung cấp được ảnh gallery đủ độ nét; xem chi tiết lần thử. |
| Apple MacBook Pro 16 M3 Max (2023) 36GB 1TB MUW63SA/A | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| MSI Prestige 13 Evo A13M-081VN | Nguồn có hạn chế quyền sử dụng | Nguồn ảnh đã đối chiếu có hạn chế sử dụng rõ ràng; chưa xác minh được ảnh đạt chuẩn từ nguồn thay thế. Giữ Chưa có ảnh. |
| MSI Prestige 16 AI Evo B1MG-007VN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| MSI Katana A15 AI B8VF-400VN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| MSI Stealth 16 Studio A13VG-080VN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| MSI Raider GE68 HX 13VG-095VN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| MSI Titan 18 HX A14VIG-072VN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| LG Gram 14 2023 14Z90R-G.AH75A5 | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Ảnh gallery tải được có nền trang trí, chữ quảng cáo, giải thưởng hoặc ghép góc máy; chưa tìm được ảnh đơn máy nền trắng đạt chuẩn. Nguồn LG có lần trả 403; không kết luận không có ảnh trên mạng. |
| LG Gram 16 2023 16Z90R-G.AH76A5 | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Ảnh gallery tải được có nền trang trí, chữ quảng cáo, giải thưởng hoặc ghép góc máy; chưa tìm được ảnh đơn máy nền trắng đạt chuẩn. Nguồn LG có lần trả 403; không kết luận không có ảnh trên mạng. |
| LG Gram Pro 16 2024 16Z90SP-G.AH78A5 | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Gigabyte G5 KF-E3VN333SH | Nguồn có hạn chế quyền sử dụng | Nguồn ảnh đã đối chiếu có hạn chế sử dụng rõ ràng; chưa xác minh được ảnh đạt chuẩn từ nguồn thay thế. Giữ Chưa có ảnh. |
| Gigabyte AORUS 16X AKG-53VN854SH | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| ASUS Vivobook 15 X1504ZA-NJ581W | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| ASUS Vivobook S 15 S5506MA-MA022W | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| ASUS Vivobook S 15 S5506MA-MA023W | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Lenovo IdeaPad 1 15AMN7 82VG003EVN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Lenovo IdeaPad 1 15AMN7 82VG003GVN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Lenovo IdeaPad Slim 3 14IRH8 83EL0020VN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Lenovo IdeaPad Slim 3 15ABR8 82XM001LVN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Lenovo ThinkBook 14 G6 IRL 21KG0064VN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Lenovo ThinkBook 16 G6 ABP 21KK005DVN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Lenovo LOQ 15IRX9 83DV003TVN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Lenovo Legion Slim 5 16AHP9 83DH003HVN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Dell Inspiron 14 5440 71034827 | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Dell Inspiron 14 5440 71034828 | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Dell Inspiron 15 3530 71011772 | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Dell Gaming G16 7630 71015718 | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| HP 15s-fq5228TU 8U235PA | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| HP Pavilion 15-eg3095TU 8U234PA | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| HP Pavilion 15-eg3097TU 8U235PA | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| HP Victus 15-fb1022AX 94F90PA | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| HP Victus 16-r1014TX 9I344PA | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Acer Aspire 5 A515-58M-79R7 NX.KHHSV.002 | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Acer Aspire 7 Gaming A715-76G-5132 NH.QGESV.008 | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Acer Predator Helios Neo 16 PHN16-72-78F1 NH.QNNSV.004 | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Apple MacBook Pro 14 M3 (2023) 16GB 512GB Z1C80001Y | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Apple MacBook Pro 14 M3 Pro (2023) 36GB 1TB Z1AU0009U | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Apple MacBook Pro 16 M3 Pro (2023) 36GB 512GB MRW23SA/A | Sai hoặc mâu thuẫn model | Trang tìm được chuyển hướng hoặc không xác nhận đúng mã model; không lấy ảnh sản phẩm khác. |
| Apple MacBook Pro 16 M3 Max (2023) 48GB 1TB MUW73SA/A | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| MSI Thin GF63 12VE-460VN | Lỗi truy cập nguồn (SSL/timeout/404) | Nguồn mới lỗi truy cập hoặc không cung cấp được ảnh gallery đủ độ nét; xem chi tiết lần thử. |
| MSI Cyborg 15 A13VF-862VN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| MSI Katana 15 B13VEK-2083VN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| MSI Sword 16 HX B14VFK-045VN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| MSI Bravo 15 C7UDX-407VN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| MSI Bravo 15 C7VFK-275VN | Nguồn có hạn chế quyền sử dụng | Nguồn ảnh đã đối chiếu có hạn chế sử dụng rõ ràng; chưa xác minh được ảnh đạt chuẩn từ nguồn thay thế. Giữ Chưa có ảnh. |
| ASUS Vivobook 16 M1605YA-MB117W | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| ASUS Vivobook Pro 15 OLED N6506MV-MA089W | Sai hoặc mâu thuẫn model | Ứng viên từ trang tổng hợp có ảnh chưa đối chiếu được với ngoại hình Pro 15 OLED N6506MV; không dùng. |
| ASUS ExpertBook B2 B2402CBA-KI0631W | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Lenovo ThinkPad L14 Gen 4 21H10034VN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Lenovo ThinkPad L15 Gen 4 21H30035VN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Lenovo ThinkPad T14s Gen 4 21F6005BVN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Lenovo ThinkPad P16s Gen 2 21HK003EVN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Lenovo Yoga Pro 7 14AHP9 83E3001QVN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Lenovo LOQ 15APH8 82XT0049VN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Dell Latitude 3440 71015636 | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Dell Latitude 3540 71015639 | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Dell XPS 15 9530 71015715 | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| HP ProBook 450 G10 873D4PA | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| HP OMEN 16-xf0071AX 8W947PA | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Acer Swift Go 14 SFG14-41-R5G1 NX.KG1SV.002 | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Acer Swift Go 16 SFG16-71-7440 NX.KFTSV.002 | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Acer Predator Helios 16 PH16-71-72BF NH.QJRSV.002 | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Apple MacBook Pro 14 M2 Pro (2023) 16GB 512GB MPHE3SA/A | Nguồn có hạn chế quyền sử dụng | Nguồn ảnh đã đối chiếu có hạn chế sử dụng rõ ràng; chưa xác minh được ảnh đạt chuẩn từ nguồn thay thế. Giữ Chưa có ảnh. |
| MSI Modern 14 C12M-047VN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| MSI Stealth 14 Studio A13VE-041VN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| LG Gram 17 2023 17Z90R-G.AH78A5 | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Ảnh gallery tải được có nền trang trí, chữ quảng cáo, giải thưởng hoặc ghép góc máy; chưa tìm được ảnh đơn máy nền trắng đạt chuẩn. Nguồn LG có lần trả 403; không kết luận không có ảnh trên mạng. |
| Gigabyte AORUS 15 BKF-73VN754SH | Nguồn có hạn chế quyền sử dụng | Nguồn ảnh đã đối chiếu có hạn chế sử dụng rõ ràng; chưa xác minh được ảnh đạt chuẩn từ nguồn thay thế. Giữ Chưa có ảnh. |
| Lenovo ThinkPad X1 Carbon Gen 12 21KC0050VN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Lenovo Legion 7 16IRX9 83FD003AVN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| ASUS TUF Gaming A17 FA707NU-HX034W | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Dell Precision 3581 71015640 | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| HP Envy 16-h1023TX 8C5N6PA | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| HP Elite Dragonfly G4 873K5PA | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Acer Swift 3 SF314-512-56SR NX.K0FSV.001 | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Acer Swift X SFX14-41G-R1S6 NX.AU5SV.00B | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Acer Swift 14 SF14-71T-71FE NX.K54SV.001 | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Apple MacBook Air 15 M3 (2024) 24GB 512GB Z1BR0006H | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| MSI Pulse 16 AI C1VGKG-018VN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| MSI Crosshair 16 HX D14VFKG-044VN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| MSI Vector 16 HX A13VHG-489VN | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| LG Gram 14 2024 14Z90S-G.AH55A5 | Nguồn có hạn chế quyền sử dụng | Nguồn ảnh đã đối chiếu có hạn chế sử dụng rõ ràng; chưa xác minh được ảnh đạt chuẩn từ nguồn thay thế. Giữ Chưa có ảnh. |
| LG Gram 16 2024 16Z90S-G.AH75A5 | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
| Gigabyte AORUS 17 BSF-73VN654SH | Chưa tìm được nguồn/ảnh catalogue đủ chuẩn | Lượt tìm mới chưa tìm được trang/ảnh catalogue xác nhận đúng mã model; tiếp tục hiển thị Chưa có ảnh. |
