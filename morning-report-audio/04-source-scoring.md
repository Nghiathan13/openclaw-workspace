# Source Scoring

File này quy định cách đánh giá độ tin cậy của nguồn cho Morning Information Report.

Topic đã được chọn ở `01-topics.md`.
Nguồn cần lấy đã được quyết định ở `02-source-plan.md`.
Cách search đã được quy định ở `03-search-rules.md`.

## Goal

Chấm điểm nguồn để quyết định:

* Nguồn nào được dùng làm luận cứ chính
* Nguồn nào chỉ dùng làm tín hiệu phụ
* Nguồn nào phải loại bỏ
* Report có đủ độ tin cậy hay không

## Source confidence levels

Mỗi nguồn phải được gán một trong ba mức:

* `high`
* `medium`
* `low`

## High confidence sources

Gán `high` nếu nguồn thuộc một trong các nhóm sau:

1. Official docs
2. Official release notes
3. GitHub repository chính thức
4. GitHub issue/discussion từ repo chính thức
5. Vendor blog chính thức
6. Security research từ tổ chức uy tín
7. API documentation chính thức

Ví dụ:

* docs chính thức của sản phẩm
* blog chính thức của công ty
* GitHub repo chính chủ
* báo cáo bảo mật từ vendor uy tín

Quy tắc:

* Có thể dùng làm luận cứ chính.
* Có thể dùng để kết luận nếu nội dung rõ ràng.
* Ưu tiên fetch các nguồn này trước.

## Medium confidence sources

Gán `medium` nếu nguồn thuộc một trong các nhóm sau:

1. News site công nghệ
2. Technical blog có nội dung rõ ràng
3. Bài phân tích có tác giả hoặc tổ chức cụ thể
4. Documentation không chính thức nhưng có chất lượng
5. Aggregator đáng tin nhưng không phải nguồn gốc

Quy tắc:

* Có thể dùng để hỗ trợ luận điểm.
* Không nên dùng làm kết luận duy nhất nếu không có nguồn high confidence.
* Nếu nội dung quan trọng, cần đối chiếu với ít nhất một nguồn khác.

## Low confidence sources

Gán `low` nếu nguồn thuộc một trong các nhóm sau:

1. Facebook site-search result
2. TikTok site-search result
3. X/Twitter/social post
4. Forum hoặc comment
5. Reddit/community discussion
6. Blog không rõ tác giả
7. SEO content yếu
8. Nguồn không fetch được nội dung chính
9. Nguồn có dấu hiệu quảng cáo, affiliate hoặc clickbait

Quy tắc:

* Không được dùng làm luận cứ chính.
* Chỉ dùng làm social signal hoặc tín hiệu phụ.
* Không dùng để kết luận chắc chắn.
* Nếu toàn bộ report chỉ có nguồn low confidence, phải ghi rõ report có độ tin cậy thấp.

## Fetch status rules

Mỗi nguồn cần có `fetch_status`:

* `fetched`
* `fetch_failed`
* `search_result_only`

### fetched

Nguồn đã được đọc nội dung chính.

Có thể dùng để phân tích nếu confidence đủ tốt.

### fetch_failed

Nguồn tìm thấy qua search nhưng không đọc được nội dung.

Quy tắc:

* Có thể liệt kê trong bảng nguồn.
* Không dùng làm luận cứ chính.
* Ghi chú rõ `fetch failed`.

### search_result_only

Nguồn chỉ có title/snippet từ search result.

Quy tắc:

* Chỉ dùng làm tín hiệu phụ.
* Không dùng để kết luận.
* Nếu là Facebook/TikTok, luôn đánh dấu `low confidence`.

## Scoring criteria

Khi đánh giá một nguồn, xem các yếu tố sau:

### 1. Authority

Nguồn có phải chính chủ không?

Điểm cao nếu là:

* official docs
* GitHub chính thức
* vendor blog
* security research
* API docs

### 2. Freshness

Nguồn có mới không?

Ưu tiên:

* trong 24 giờ gần đây
* trong 7 ngày gần đây
* trong 30 ngày gần đây

Nếu nguồn cũ nhưng vẫn là docs chính thức, vẫn có thể dùng.

### 3. Relevance

Nguồn có liên quan trực tiếp đến topic không?

Nguồn chỉ nhắc thoáng qua topic thì không nên dùng làm nguồn chính.

### 4. Evidence quality

Nguồn có dữ liệu, dẫn chứng, changelog, code, issue, thông báo chính thức không?

Nguồn chỉ nêu ý kiến chung thì giảm độ tin cậy.

### 5. Fetchability

Nếu không fetch được nội dung chính, không được xem là nguồn mạnh.

## Main evidence rules

Một nguồn chỉ được dùng làm luận cứ chính nếu:

* `confidence` là `high` hoặc `medium`
* `fetch_status` là `fetched`
* nội dung liên quan trực tiếp topic
* không chỉ là social signal

## Social signal rules

Facebook/TikTok site-search hiện tại luôn là:

```json
{
  "confidence": "low",
  "role": "social_signal"
}
```

Không được nói rằng đã crawl trực tiếp Facebook/TikTok.

Không dùng Facebook/TikTok site-search để kết luận sự thật.

Chỉ dùng để nói:

* có dấu hiệu thảo luận
* có tín hiệu cộng đồng
* có nội dung social liên quan

## Report confidence

Sau khi chấm điểm nguồn, đánh giá độ tin cậy tổng thể của report:

### High report confidence

Điều kiện:

* Có ít nhất 2 nguồn `high confidence`
* Có ít nhất 2 nguồn `fetched`
* Các nguồn không mâu thuẫn nghiêm trọng

### Medium report confidence

Điều kiện:

* Có ít nhất 1 nguồn `high confidence`, hoặc
* Có nhiều nguồn `medium confidence`
* Fetch thành công đủ để phân tích cơ bản

### Low report confidence

Điều kiện:

* Chỉ có nguồn social/community
* Chỉ có search snippets
* Fetch thành công dưới 2 nguồn
* Search bị rate-limit nhiều
* Nguồn mâu thuẫn nhưng không đủ dữ liệu đối chiếu

Nếu report confidence là `low`, phải ghi rõ trong phần hạn chế.

## Required source table fields

Trong report cuối, bảng nguồn phải có các cột:

| # | URL | Loại nguồn | Fetch status | Độ tin cậy | Vai trò | Ghi chú |
| - | --- | ---------- | ------------ | ---------- | ------- | ------- |

Vai trò có thể là:

* `main_evidence`
* `supporting_evidence`
* `social_signal`
* `background`
* `excluded`

## Exclusion rules

Loại bỏ hoặc không dùng nguồn nếu:

* URL không rõ ràng
* Nội dung không liên quan
* Có dấu hiệu spam/SEO/clickbait
* Không có thông tin mới
* Chỉ copy lại từ nguồn khác mà không thêm giá trị
* Nguồn social không thể kiểm chứng

Có thể nhắc ngắn trong phần hạn chế nếu nhiều nguồn bị loại.
