# Nile Sales — phân tích dữ liệu bán hàng

Phân tích bộ dữ liệu thực hành **tháng 1–7/2025** bằng Python và Power BI: từ hiểu/làm sạch dữ liệu, model và 13 công thức đến dashboard ba trang và báo cáo kinh doanh.

![Dashboard Tổng quan Nile Sales](reports/phase5b/page_01.png)

## Xem sản phẩm

- [Báo cáo kinh doanh PDF — 6 trang](reports/06_business_report.pdf) · [nguồn TEX](reports/06_business_report.tex).
- [Dashboard Power BI](pbi/NileSales.pbip): Tổng quan; Sản phẩm và nơi nhận; Cờ nguồn và hiệu ngày.
- [Ảnh và cách đọc ba trang](docs/05b_dashboard_build.md) · [Phát hiện và giới hạn](docs/04b_findings.md).

## Điều phân tích cho thấy

| Quy mô tháng 1–7/2025 | Kết quả |
|---|---:|
| Dòng nguồn | 9.705 |
| Lượng ghi nhận | 13.087 |
| Tổng giá trị dòng nguồn | 8.787.091, chưa xác nhận tiền tệ |
| Sản phẩm / nhóm / nơi nhận | 50 / 5 / 28 |

- Giá trị tháng 7 đạt **1.744.028**, tăng **22,72%** so tháng 6; lượng chỉ tăng **5,87%**. Chia theo số ngày lịch, giá trị vẫn tăng **18,76%**. Đây là biến động trong file, chưa chứng minh tăng trưởng toàn doanh nghiệp hoặc nguyên nhân.
- Hai mã Makeup **BPC-1041/BPC-1048** đóng góp **94.461**, tương đương **29,26% phần tăng ròng tháng 7**. Đề xuất rà lượng, giá ghi nhận và cơ cấu nơi nhận của hai mã trước; chưa phải hành động đã triển khai.
- Cờ 1 xuất hiện trên **574/9.705 dòng (5,91%)**; trung vị hiệu ngày nguồn là **3 ngày**. Chưa đủ định nghĩa để gọi là đơn hoàn thực tế, tiền hoàn hoặc giao đúng hạn.

## Hiểu đúng dữ liệu và phạm vi

Nguồn là workbook thực hành từ [video Goodly trên YouTube](https://www.youtube.com/watch?v=1AavSLWhh-E), không có quyền truy cập hệ thống gốc để xác nhận cách tạo file. Repo ghi nguồn tham khảo; không tự coi dữ liệu là giao dịch doanh nghiệp thật hay dữ liệu mô phỏng đã xác minh.

`Order_ID` được đọc là **mã nhóm nguồn**, chưa là đơn mua hàng thật: 3.459/6.246 mã nhóm có hai Customer_ID. H1 được dùng như giả định thực hành, không phải nguyên nhân đã chứng minh; giữ các dòng và mã gốc. Không tính giá trị đơn bình quân, giữ chân khách, doanh thu thuần hoặc lợi nhuận khi thiếu định nghĩa/dữ liệu. [Doc hiểu dữ liệu](docs/01_data_understanding.md) giữ bằng chứng và các giả thuyết.

Nguồn, CSV chuẩn hóa và các bảng tổng hợp được giữ để đối chiếu. Không sửa ngoại lệ hoặc gán lại khách để làm đẹp số. Phạm vi là Excel → Python → Power BI; không có triển khai SQL/DW/ML hoặc bằng chứng hiệu quả vận hành đã đạt.

## Mở trên máy khác

1. Clone repo; giữ `pbi/NileSales.Report` và `pbi/NileSales.SemanticModel` bên cạnh `NileSales.pbip`.
2. Mở PBIP bằng Power BI Desktop hỗ trợ định dạng dự án. Trước Refresh, vào **Transform data**, chọn query `FactSalesLine`, sửa đường dẫn `File.Contents(...)` trong **Advanced Editor** tới `data/processed/nile_sales_clean.csv` trên máy của bạn. Model hiện dùng đường dẫn tuyệt đối, chưa có parameter DataFolder.
3. Sau Refresh, đối chiếu các tổng **8.787.091 / 13.087 / 9.705 / 6.246** và kỳ nguồn trước khi dùng các bộ lọc.

Nguồn Excel ở `data/Nile_Sales_YTD.xlsx`; notebook 01/02 ở `notebooks/` giải thích hiểu và làm sạch dữ liệu. Scripts có kiểm số/hash của bản đã chốt; không cần chạy generator để mở dashboard, vì có thể ghi đè bố cục hiện hành. Việc Refresh trên máy khác chưa được kiểm trong lần đóng gói này.

## Cấu trúc phần công khai

| Thư mục | Nội dung |
|---|---|
| data | Workbook, CSV chuẩn hóa và cờ rà soát có dấu vết nguồn |
| notebooks | Hiểu và làm sạch dữ liệu, code kèm giải thích/biểu đồ |
| docs | Bài toán, định nghĩa, phát hiện, thiết kế và giới hạn |
| pbi | PBIP, report và semantic model |
| reports | Bảng tổng hợp, ảnh dashboard, báo cáo TEX/PDF |
| scripts | Phân tích, vẽ và các phép kiểm của dự án |

Hồ sơ điều phối `Plan/`, `Log/`, hướng dẫn agent và bản sao lưu giữ cục bộ. Tham chiếu tới chúng trong tài liệu là dấu vết kiểm nội bộ, không phải tài liệu công khai hoặc chứng nhận chạy trên máy khác. File hướng dẫn kết nối của bên thứ ba và cache/build phụ không nằm trong repo.

## Trạng thái kiểm

Đã đối chiếu các tổng/nhóm/DAX, render ba trang, lưu–đóng–mở lại và review báo cáo PDF sáu trang. Hình thức 5B đã được người dùng chấp nhận để tiếp tục. **QA thao tác đầy đủ chưa nghiệm thu:** lọc đồng bộ/nhiều lựa chọn/rỗng, chọn biểu đồ, hover, điều hướng và reset; chưa chứng minh ClearAllSlicers xóa mọi lựa chọn trên hình. Không gọi toàn bộ chức năng đã hoàn tất chỉ từ ảnh hoặc báo cáo.
