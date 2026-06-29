# Analysis Rules

File này quy định cách phân tích, đối chiếu và tổng hợp nguồn cho Morning Information Report.

Topic đã được chọn ở `01-topics.md`.
Nguồn đã được chọn ở `02-source-plan.md`.
Search đã được thực hiện theo `03-search-rules.md`.
Nguồn đã được chấm điểm theo `04-source-scoring.md`.

## Goal

Tạo phần phân tích ngắn, rõ, có căn cứ, không phóng đại và không bịa kết luận.

## Analysis order

Phân tích theo thứ tự sau:

1. Xác định nguồn chính
2. Tóm tắt thông tin chính từ từng nguồn
3. Tìm điểm giống nhau giữa các nguồn
4. Tìm điểm khác nhau hoặc mâu thuẫn
5. Đánh giá độ tin cậy tổng thể
6. Rút ra ý nghĩa thực tế với Nghĩa
7. Đề xuất hành động hôm nay

## Main evidence first

Chỉ dùng nguồn làm luận cứ chính nếu nguồn đó thỏa điều kiện:

* `confidence` là `high` hoặc `medium`
* `fetch_status` là `fetched`
* nội dung liên quan trực tiếp topic
* không phải social signal

Nguồn `low confidence`, Facebook, TikTok, social, forum, search snippet hoặc fetch failed chỉ được dùng làm tín hiệu phụ.

## Cross-check rules

Khi có nhiều nguồn, phải kiểm tra:

1. Các nguồn có đang nói cùng một sự kiện không?
2. Nguồn nào là nguồn gốc?
3. Nguồn nào chỉ trích dẫn lại?
4. Có mâu thuẫn về ngày tháng, số liệu, claim hoặc kết luận không?
5. Có nguồn official/vendor xác nhận không?

Nếu có mâu thuẫn:

* Không chọn kết luận chắc chắn nếu chưa đủ dữ liệu.
* Nêu rõ mâu thuẫn.
* Ưu tiên nguồn official, GitHub, vendor, security research.
* Đánh dấu phần đó là `needs verification` nếu cần.

## Claim strength

Mỗi nhận định quan trọng phải thuộc một trong ba mức:

### Strong claim

Chỉ dùng khi:

* Có nguồn high confidence
* Fetch thành công
* Nội dung rõ ràng
* Không có mâu thuẫn lớn

Cách viết:

* "Nguồn official cho biết..."
* "Báo cáo security research xác nhận..."
* "GitHub release notes ghi..."

### Medium claim

Dùng khi:

* Có nguồn medium hoặc nhiều nguồn hỗ trợ
* Chưa có nguồn official
* Nội dung hợp lý nhưng cần kiểm chứng thêm

Cách viết:

* "Có dấu hiệu..."
* "Một số nguồn cho thấy..."
* "Khả năng cao..."

### Weak claim

Dùng khi:

* Chỉ có social signal
* Chỉ có search snippet
* Fetch fail
* Nguồn low confidence

Cách viết:

* "Chỉ nên xem là tín hiệu phụ..."
* "Chưa đủ dữ liệu để kết luận..."
* "Cần kiểm chứng thêm..."

Không được viết weak claim như sự thật chắc chắn.

## Comparison rules

Trong phần phân tích, luôn cố gắng so sánh:

### Điểm giống nhau

Các nguồn cùng xác nhận điều gì?

Ví dụ:

* cùng nói về một bản cập nhật
* cùng nhắc một rủi ro bảo mật
* cùng phản ánh một xu hướng
* cùng liên quan đến topic Nghĩa đang theo dõi

### Điểm khác nhau

Các nguồn khác nhau ở đâu?

Ví dụ:

* official docs nói kỹ thuật, news nói tác động
* vendor blog tập trung tính năng, community tập trung lỗi
* social nói phản ứng người dùng, web nói thông tin chính thức

### Mâu thuẫn

Có claim nào trái nhau không?

Nếu có, phải ghi rõ:

* nguồn A nói gì
* nguồn B nói gì
* nguồn nào đáng tin hơn
* kết luận hiện tại nên thận trọng ở đâu

## Relevance to Nghĩa

Sau khi phân tích nguồn, phải rút ra ý nghĩa thực tế với Nghĩa.

Ưu tiên liên hệ đến:

* OpenClaw setup
* Telegram bot automation
* Cron/report workflow
* AI agent security
* ClawHub skills
* DeepSeek/API/model choice
* Web app/SaaS/project cá nhân
* Việc nên học hoặc test tiếp hôm nay

Không viết chung chung kiểu:

* "Điều này rất quan trọng"
* "Bạn nên cập nhật xu hướng"
* "Công nghệ đang phát triển nhanh"

Phải viết cụ thể.

Ví dụ tốt:

* "Nếu Nghĩa đang cài skill từ ClawHub, nên audit publisher và đọc `setup.sh` trước khi chạy."
* "Nếu report bị fetch fail nhiều, nên thêm Firecrawl làm fallback."
* "Nếu dùng Brave Search free tier, nên giảm search budget để tránh 429."

## Action rules

Phần hành động hôm nay phải có đúng 3 việc.

Mỗi việc phải:

* cụ thể
* nhỏ
* làm được trong ngày
* liên quan đến topic report
* không quá chung chung

Format:

1. Việc cần làm

   * Lý do ngắn
   * Kết quả mong muốn

Ví dụ:

1. Audit các skill đã cài trong OpenClaw

   * Lý do: giảm rủi ro supply chain
   * Kết quả: biết skill nào an toàn, skill nào cần gỡ

## Do not overreach

Không được:

* bịa dữ liệu
* bịa số liệu
* bịa nguồn
* suy luận quá xa từ social signal
* lấy fetch failed source làm kết luận
* viết như đã crawl Facebook/TikTok trực tiếp
* nói chắc chắn khi nguồn yếu
* dùng nhiều từ hype như "đột phá", "cách mạng", "siêu mạnh" nếu nguồn không chứng minh

## Required analysis output

Trong report cuối phải có phần:

### Phân tích chính

Gồm:

* Điểm giống nhau giữa các nguồn
* Điểm khác nhau hoặc mâu thuẫn
* Kết luận đáng tin nhất
* Phần cần kiểm chứng thêm nếu có

### Ý nghĩa với Nghĩa

Gồm:

* Tác động thực tế
* Việc nên chú ý
* Rủi ro hoặc cơ hội

### Việc nên làm hôm nay

Đúng 3 việc cụ thể.
