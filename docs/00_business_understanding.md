# Phase 0 — Nile Sales cần phân tích điều gì?

Lượt chạy lại ngày 13/10/2026 · DAFlowAuto 1.2 · **Đã được người dùng duyệt ngày 13/10/2026; định nghĩa chưa rõ vẫn chưa được xác nhận.**

## 1. Bài toán và người sử dụng

Cần hiểu kết quả bán hàng trong file Nile Sales: tháng nào biến động, nhóm sản phẩm/nơi nhận nào đóng góp và điểm nào cần tìm hiểu về cờ hoàn, ngày bán–giao. Kết quả giúp chọn **một việc ưu tiên cần xác minh**, trước khi đưa ra hành động kinh doanh.

Người đọc đề xuất: người phụ trách bán hàng/vận hành. Chưa có người cụ thể, mục tiêu cải thiện bằng số hoặc thời hạn được xác nhận. Không tự đặt cam kết tăng bán hàng, giảm hoàn hoặc hiệu quả đã đạt.

## 2. Nguồn và phạm vi

- Nguồn: [Nile_Sales_YTD.xlsx](../data/Nile_Sales_YTD.xlsx), đã được đọc lại trong lượt này.
- Có 7 sheet mang tên các tháng 1–7/2025; cùng 18 cột và tổng 9.705 dòng có dữ liệu dưới tiêu đề. Đây là đếm đầu vào, chưa kết luận các dòng đều hợp lệ hoặc đủ mọi giao dịch.
- Có các cột ngày bán/giao, sản phẩm, lượng/giá/giá trị, nơi gửi/nhận, mã đơn/khách và cờ hoàn. Phạm vi ngày thực tế, giá trị thiếu và độ nhất quán sẽ được kiểm ở Phase 1.
- Một dòng tạm hiểu là một dòng ghi sản phẩm bán. Cách hiểu này cần kiểm với mã đơn/SKU; mã nguồn chưa được xác nhận là đơn hàng hợp lệ hay khóa duy nhất.
- Truy nguồn bằng tệp + sheet + số dòng Excel. Không lấy dữ liệu làm sạch/model/kết luận cũ thay cho việc thực hiện lại.

## 3. Bốn câu hỏi và cách dùng kết quả

| Cần biết gì? | Đo bằng gì? | Kết quả hỗ trợ quyết định gì? |
|---|---|---|
| Lượng và giá trị bán thay đổi thế nào theo tháng? | Tổng Qty, tổng Line_Amount; số dòng/mã đơn và độ phủ kỳ | Chọn tháng cần tìm hiểu biến động; chưa suy nguyên nhân tăng/giảm |
| Sản phẩm và nơi nhận nào đóng góp chính? | Giá trị và tỷ trọng theo Category/SKU/To_Location, kèm quy mô | Chọn nhóm ưu tiên xem xét; chưa quyết định mua thêm hàng khi thiếu tồn kho/lợi nhuận |
| Dòng có cờ hoàn tập trung ở đâu? | Số dòng cờ 1, tỷ lệ trên dòng có cờ 0 hoặc 1, kèm số mẫu | Chọn nhóm cần xác minh cờ hoàn; chưa gọi là tỷ lệ đơn hoàn hay tiền hoàn |
| Khoảng ngày bán–giao khác nhau thế nào? | Hiệu Delivery_Date−Sales_Date ở dòng đủ ngày hợp lệ; số mẫu, trung vị và phân phối | Chọn nhóm/tuyến cần tìm hiểu; chưa đánh giá giao đúng hạn |

## 4. Cách đo ban đầu và giới hạn

| Chỉ số | Cách tính dự kiến | Cách đọc đúng |
|---|---|---|
| Giá trị dòng nguồn | Cộng Line_Amount trong phạm vi đã chọn | Đơn vị tiền chưa rõ; chưa là doanh thu thuần |
| Lượng bán nguồn | Cộng Qty | Đơn vị hàng chưa rõ; chưa tự trừ hoàn |
| Số mã đơn nguồn | Đếm Order_ID khác nhau, không đếm mã thiếu | Không lấy làm mẫu số giá trị đơn bình quân khi nghĩa/khóa đơn chưa rõ |
| Tỷ trọng nhóm | Giá trị nhóm / tổng cùng kỳ và bộ lọc | Không lấy tổng Top N làm toàn bộ; không cộng tỷ lệ khác mẫu số |
| Tỷ lệ dòng cờ 1 | Dòng cờ 1 / dòng có cờ 0 hoặc 1 | Báo riêng cờ thiếu/khác; không đổi thành tỷ lệ đơn hoặc hàng hoàn |
| Khoảng ngày bán–giao | Hiệu hai ngày; trung vị là mức ở giữa các dòng đủ ngày hợp lệ | Kèm số mẫu/phân phối; không cộng trung vị nhóm; chưa là giao đúng hạn |

Kỳ bán chọn theo Sales_Date. So tháng chỉ sau khi kiểm độ phủ; tháng đầu thiếu kỳ trước thì để trống. Không có nguồn năm trước để so cùng kỳ năm trước. Dữ liệu thiếu/sai phải được báo, không tự đổi thành 0 hoặc loại dòng để làm đẹp số.

## 5. Điều chưa rõ cần xác nhận

| Cần xác nhận với chủ dữ liệu | Khi chưa có trả lời |
|---|---|
| Tiền tệ, thuế/chiết khấu trong giá trị; nguồn đã trừ hoàn chưa? | Chỉ báo giá trị nguồn; không tính doanh thu thuần/tiền hoàn |
| Cờ hoàn nghĩa gì, hoàn cả dòng hay một phần, ngày hoàn là ngày nào? | Chỉ mô tả cờ theo dòng; chưa nhận nguyên nhân hoặc tỷ lệ đơn hoàn |
| Một mã đơn gắn với khách/SKU như thế nào; một dòng thực sự đại diện gì? | Phase 1 kiểm; hoãn giá trị đơn bình quân và các chỉ số khách hàng |
| Ngày giao là thực tế hay dự kiến; hạn giao chuẩn là gì? | Chỉ mô tả hiệu hai ngày ghi trong nguồn |
| File trích xuất khi nào, đủ giao dịch trong kỳ chưa? | Không coi ngày cuối dữ liệu là ngày trích xuất; không nhận toàn doanh nghiệp tăng trưởng |

Các điểm chưa rõ được giữ để hỏi/xác minh; việc kiểm dữ liệu độc lập vẫn thực hiện được sau khi duyệt Phase 1. Chưa cần tự điền đáp án để tiếp tục.

## 6. Bạn duyệt gì ở Phase 0?

Duyệt mục tiêu, người đọc đề xuất, bốn câu hỏi và giới hạn cách đo ở trên; có thể yêu cầu sửa câu hỏi hoặc xác nhận định nghĩa. Duyệt Phase 0 **không xác nhận chất lượng dữ liệu, các chỉ số đã tính hay những phase sau đã chạy**.

Bước tiếp là worker kiểm dữ liệu ở Phase 1 theo [PLAN, mục 4](../Plan/PLAN.md#4-kế-hoạch-phase-1--đã-được-duyệt-và-giao-triển-khai). Tôi review kết quả trước khi trình bạn duyệt tiếp. Giữ ngoại lệ đã chốt: không làm PDF/TEX, không mặc định thêm SQL/kho dữ liệu/ML hoặc publish.
