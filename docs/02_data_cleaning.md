# Phase 2 — Chuẩn hóa dữ liệu (lượt chạy lại)

> Notebook: [02_clean_data.ipynb](../notebooks/02_clean_data.ipynb) (kernel sạch, exit 0).
> Nguồn: `data/Nile_Sales_YTD.xlsx` SHA `fae7a695…6d4fc0bd8` (đầu–cuối bằng nhau).
> H1 là giả định thực hành đã chọn, chưa xác nhận nguyên nhân thật. Giữ mọi dòng/mã khách; `Order_ID` được dùng như mã nhóm nguồn, chưa nhận là đơn kinh doanh.

## 1. Đã đổi gì, vì sao

Chỉ chuẩn hóa kiểu/định dạng: ngày sang ISO `YYYY-MM-DD` (giờ gốc toàn 00:00, đã đếm);
số nguyên giữ chính xác; chuỗi/mã/nhãn giữ nguyên giá trị (không trim/gộp/sửa).
Không làm tròn, null→0, trừ hoàn, bỏ dòng/outlier, chọn khách hay tạo khóa.

## 2. Trước–sau (18 → 21 cột, giữ 9.705 dòng)

| | Trước (Excel) | Sau ([nile_sales_clean.csv](../data/processed/nile_sales_clean.csv)) |
|---|---|---|
| Cột | 18 cột nguồn | 18 nguồn + 3 truy nguồn (`__source_file__`, `__sheet__`, `__excel_row__`) |
| Dòng | 9.705 | 9.705 (không thêm/bớt) |
| Qty / giá trị | 13.087 / 8.787.091 | bằng nhau (delta 0, cả theo tháng/nhóm/nơi nhận) |
| Dòng có `Is_Returned=1` / tổng dòng | 574 / 9.705 | bằng nhau |
| Ô khác định dạng ngày | — | 0 (đọc lại khớp từng ô; lượt đọc Excel độc lập khớp 174.690 ô) |

## 3. Bảng cờ xem xét

[nile_sales_review_flags.csv](../data/processed/nile_sales_review_flags.csv)
(6.918 dòng thuộc 3.459 mã nhóm đa khách): mã nhóm/khách, truy nguồn, số mã khách, lý do
`ORDER_MULTIPLE_CUSTOMER_IDS`. Cờ là điều cần xác minh, không phải lỗi;
không dùng loại dòng khỏi CSV chính. Không lẫn với cờ hoàn.

## 4. Dùng được và hoãn lại

Dùng được: tổng số lượng (`Qty`) và giá trị ghi nhận (`Line_Amount`) theo tháng/nhóm sản phẩm/nơi nhận để mô tả file. Dữ liệu có ba cột truy nguồn giúp mở đúng dòng Excel khi cần kiểm. `Is_Returned` vẫn là cờ trên từng dòng; không tự trừ số tiền hoặc gọi là tỷ lệ đơn hoàn.

Hoãn phân tích khách mua lại/giá trị khách, giá trị đơn bình quân (AOV), doanh thu thuần và giao đúng hạn vì thiếu định nghĩa cần thiết. Riêng AOV cần xác nhận `Order_ID` đại diện một đơn kinh doanh và cách tính giá trị đơn; nhiều mã khách trong nhóm không tự làm sai phép cộng theo nhóm.
