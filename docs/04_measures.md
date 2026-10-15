# Phase 4 — 13 chỉ số đo gì (bảng `Measure`)

> Bảng này không chứa dữ liệu, chỉ chứa 13 công thức tính trên các dòng đang được chọn.
> Lịch chọn thời gian mặc định lọc theo ngày bán. Lọc theo ngày giao được kiểm riêng.
> Chi tiết công thức/query/số đối chiếu: `Log/phase4/evidence/run.json` và
> `Log/phase4/evidence/xcheck_p4.py`. Kết quả đã được Codex đối chiếu với CSV theo tháng, nhóm sản phẩm, nơi nhận và các ca lọc đã duyệt.
> Hai tên đã đổi theo hợp đồng (công thức giữ nguyên): Số mã đơn → **Số mã nhóm nguồn**,
> Trung vị số ngày bán đến giao → **Trung vị hiệu ngày nguồn**.
> H1 vẫn là giả định thực hành: đếm `Order_ID` như mã nhóm trong file, chưa xác nhận đó là đơn mua hàng thật.
> Chưa tính theo khách, giá trị đơn bình quân, doanh thu thuần, giao đúng hạn hay so với năm trước; chưa vẽ dashboard.

## 1. Danh sách 13 chỉ số

| Chỉ số | Đo gì | Toàn kỳ hoặc cách xem |
|---|---|---|
| Số dòng nguồn | Đếm dòng trong tập đang chọn; không phải số đơn | 9.705 |
| Lượng bán nguồn | Cộng cột Qty (đơn vị hàng chưa xác nhận) | 13.087 |
| Giá trị dòng nguồn | Cộng cột Line_Amount (số nguyên, không ký hiệu tiền, không gọi doanh thu thuần) | 8.787.091 |
| Số mã nhóm nguồn | Đếm mã Order_ID khác nhau, bỏ mã trống (file hiện không có trống); tính lại trên từng tập, không cộng dồn | 6.246 |
| Số dòng có cờ hợp lệ | Đếm dòng có Is_Returned bằng 0 hoặc 1 | 9.705 |
| Số dòng có cờ hoàn | Đếm dòng có Is_Returned bằng 1 | 574 |
| Tỷ lệ dòng có cờ hoàn | Dòng cờ 1 chia dòng có cờ hợp lệ | 5,91% |
| Số dòng đủ ngày | Đếm dòng đủ hai ngày và ngày giao không trước ngày bán | 9.705 |
| Trung vị hiệu ngày nguồn | Giá trị ở giữa của các hiệu ngày giao − ngày bán | 3 ngày |
| Tỷ trọng giá trị sản phẩm được chọn | Giá trị nhóm sản phẩm chia tổng các sản phẩm đang chọn | Xem từng nhóm; ví dụ ở mục 4 |
| Tỷ trọng giá trị nơi nhận được chọn | Giá trị nơi nhận chia tổng các nơi đang chọn | Xem từng nơi; ví dụ ở mục 4 |
| Giá trị nguồn tháng trước | Giá trị tháng liền trước, giữ lựa chọn sản phẩm/nơi nhận/cờ | Chọn đúng một tháng đầy đủ; ví dụ ở mục 5 |
| Thay đổi giá trị nguồn so tháng trước (%) | Chênh lệch tháng này so tháng trước chia giá trị tháng trước | Chọn đúng một tháng đầy đủ; ví dụ ở mục 5 |

Bốn chỉ số đầu đếm hoặc cộng trên các dòng đang chọn. Không có dòng → để trống. Các chỉ số sau dùng mẫu và điều kiện ở mục 2–5; không cộng tỷ lệ hoặc trung vị giữa các nhóm.

## 2. Hoàn trả — đếm theo cờ trên từng dòng

- Mẫu số (Số dòng có cờ hợp lệ): dòng có cờ 0 hoặc 1, tính trên đúng tập đang chọn
  (kể cả khi người xem đang lọc theo cờ). Toàn kỳ: 9.705.
- Tử số (Số dòng có cờ hoàn): dòng có cờ 1 trong tập đó. Toàn kỳ: 574.
  Tập có dòng nhưng không dòng cờ 1 nào → ghi 0 (ví dụ T6 + Fragrance);
  tập không có dòng → để trống.
- Tỷ lệ = tử / mẫu: toàn kỳ 574/9.705 ≈ 5,91%; lọc cờ 0 → 0%, lọc cờ 1 → 100%.
  Đây là tỷ lệ dòng mang cờ, chưa phải tỷ lệ đơn/hàng hoàn.

## 3. Giao hàng — hiệu ngày giao trừ ngày bán, tính từng dòng

- Mẫu (Số dòng đủ ngày): dòng có đủ 2 ngày và ngày giao không trước ngày bán,
  đếm trên đúng tập đang lọc (không quay về toàn kỳ). Toàn kỳ: 9.705.
- Trung vị hiệu ngày nguồn: xếp mọi hiệu ngày (giao − bán) của mẫu từ nhỏ đến lớn
  rồi lấy giá trị ở giữa; nhóm chẵn dòng thì lấy trung bình 2 giá trị giữa
  (ví dụ T5 + Fragrance = 3,5 ngày). Toàn kỳ: 3 ngày.
  Đây là con số ở giữa của các dòng trong file, chưa phải thời gian xử lý đơn,
  cam kết thời gian giao hay đánh giá giao đúng hạn. Không mẫu → để trống.

## 4. Đóng góp — phần của tổng giá trị đang chọn

- Tử = giá trị của nhóm đang xét; mẫu = giá trị của toàn bộ phạm vi đang chọn
  (bỏ nhóm sản phẩm hoặc nơi nhận của ô hiện tại, giữ phạm vi người xem đã chọn và các bộ lọc khác).
- Ví dụ: chọn {Skincare, Makeup} → mẫu 5.066.802, Skincare 53,83% + Makeup 46,17% = 100%.
  Chọn {Skincare, Makeup} trong tháng 6 tại {Delhi, Mumbai} → mẫu 101.734,
  Skincare 60,72% + Makeup 39,28% = 100% — mẫu vẫn giữ lọc tháng và nơi nhận.
  Với nơi nhận, chọn Delhi + Mumbai ở tháng 6: tổng 169.651; mỗi nơi được chia cho tổng này.
- Trục vẽ phải lấy từ đúng bảng đã chọn (sản phẩm từ DimProduct, nơi nhận từ
  DimDestination). Mẫu bằng 0 hoặc trống → để trống. Tương tác chọn nhóm lớn nhất và chọn trực tiếp trên biểu đồ sẽ kiểm khi có dashboard.

## 5. So tháng — tháng này với tháng lịch liền trước

- Chỉ tính khi tập chọn là đúng 1 tháng lịch đầy đủ (đủ số ngày trên lịch,
  ví dụ tháng 2 phải có đủ 28 ngày) và cả hai tháng đều có dòng.
  Thiếu 1 ngày giữa tháng (tháng 2 thiếu 15/02 còn 27 ngày) → tháng trước và %
  đều trống. Nhiều tháng, 2 ngày rời rạc, tháng 1, tháng 8 → trống.
- Tháng 2 so tháng 1: 1.031.819 so 968.478 (+6,54%); giữ lọc Category thì so
  đúng Category đó (Skincare tháng 2 lấy tháng 1 Skincare = 302.899);
  giữ lọc nơi nhận/cờ thì so đúng tập đó (Delhi cờ 0: tháng 3 = 87.557,
  tháng 2 = 90.763). Không gọi đây là tăng trưởng doanh nghiệp thật.
- Mẫu số phần trăm bằng 0 → để trống (file hiện chưa có ca này nên chưa thử
  trực tiếp, mới kiểm điều kiện trong công thức).

## 6. Lọc ngày ghi thẳng trên dòng

- Lọc trực tiếp cột ngày trên bảng dòng vẫn giữ đúng tập cho mẫu và trung vị:
  ngày bán 15/06 → 49 dòng mẫu, trung vị 3; ngày bán 18/06 → 43 dòng, trung vị 4;
  ngày giao 15/06 → 43 dòng, trung vị 4; ngày giao 18/06 → 55 dòng, trung vị 3.
