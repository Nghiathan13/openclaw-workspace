# Morning Report Runner

File này chỉ dùng để điều phối workflow tạo Morning Information Report.

Đọc và thực thi các file dưới đây theo đúng thứ tự. Không bỏ qua file nào.

## Execution order

1. `/home/node/.openclaw/workspace/usecases/morning-report/01-topics.md`
2. `/home/node/.openclaw/workspace/usecases/morning-report/02-source-plan.md`
3. `/home/node/.openclaw/workspace/usecases/morning-report/03-search-rules.md`
4. `/home/node/.openclaw/workspace/usecases/morning-report/04-source-scoring.md`
5. `/home/node/.openclaw/workspace/usecases/morning-report/05-analysis-rules.md`
6. `/home/node/.openclaw/workspace/usecases/morning-report/06-report-format.md`
7. `/home/node/.openclaw/workspace/usecases/morning-report/07-output-rules.md`

## Final task

Sau khi đọc đủ các file trên, tạo một Morning Information Report bằng tiếng Việt cho Nghĩa.

Report phải tuân thủ toàn bộ quy tắc trong các file đã đọc.

## Conflict rule

Nếu có xung đột giữa các file, ưu tiên file có số thứ tự lớn hơn.

Ví dụ:

* `07-output-rules.md` được ưu tiên cao nhất về output cuối cùng.
* `06-report-format.md` quy định cấu trúc report.
* `05-analysis-rules.md` quy định cách phân tích.
* `04-source-scoring.md` quy định cách đánh giá nguồn.
* `03-search-rules.md` quy định cách search.
* `02-source-plan.md` quy định nguồn cần lấy.
* `01-topics.md` quy định cách chọn topic.
