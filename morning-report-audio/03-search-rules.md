# Search Rules

File này quy định cách search thông tin cho Morning Information Report.

Topic đã được chọn ở `01-topics.md`.
Nguồn cần lấy đã được quyết định ở `02-source-plan.md`.

## Goal

Search đủ thông tin để tạo report, nhưng không search quá nhiều, không gây rate-limit, không lấy nguồn yếu làm kết luận chính.

## Search budget

Mỗi lần chạy report:

* Gọi `web_search` tối đa 3 lần.
* Gọi `web_fetch` tối đa 5 URL.
* Nếu bị rate-limit, không retry quá 1 lần.
* Nếu vẫn bị rate-limit, dùng kết quả đã có và ghi rõ hạn chế.

## Search order

Thực hiện search theo thứ tự:

1. Search web chính trước.
2. Fetch các nguồn web quan trọng nhất.
3. Nếu Source Plan bật Facebook site search, search `site:facebook.com`.
4. Nếu Source Plan bật TikTok site search, search `site:tiktok.com`.
5. Chỉ fetch social URL nếu URL có vẻ đọc được và thật sự cần thiết.

## Web search query rules

Với mỗi topic chính, tạo query ngắn, rõ, ưu tiên tiếng Anh.

Ví dụ:

```text
OpenClaw security ClawHub skills
OpenClaw Telegram bot cron jobs
DeepSeek API coding agent
Cursor Cline AI coding tools update
```

Nếu topic liên quan Việt Nam hoặc thị trường Việt Nam, dùng thêm tiếng Việt.

Ví dụ:

```text
crypto Việt Nam hôm nay
AI coding tool Việt Nam
```

## Official source priority

Khi search web, ưu tiên theo thứ tự:

1. Official docs
2. GitHub repository / GitHub issue / release notes
3. Vendor blog
4. Security research
5. Technical blog
6. News site
7. Community/forum/social

Không dùng community/social làm kết luận chính nếu chưa có nguồn web đáng tin xác nhận.

## Facebook site search

Chỉ dùng khi Source Plan bật `facebook_site_search`.

Query format:

```text
site:facebook.com <topic keywords>
```

Ví dụ:

```text
site:facebook.com OpenClaw AI agent
site:facebook.com DeepSeek API
site:facebook.com crypto market Vietnam
```

Quy tắc:

* Facebook site search chỉ là social signal.
* Luôn đánh dấu `low confidence`.
* Không xem là crawl trực tiếp Facebook.
* Không dùng làm bằng chứng chính.
* Nếu không đủ 5 nguồn, ghi rõ số nguồn thực tế.

## TikTok site search

Chỉ dùng khi Source Plan bật `tiktok_site_search`.

Query format:

```text
site:tiktok.com <topic keywords>
```

Ví dụ:

```text
site:tiktok.com AI coding tools
site:tiktok.com DeepSeek API
site:tiktok.com crypto market
```

Quy tắc:

* TikTok site search chỉ là social/video signal.
* Luôn đánh dấu `low confidence`.
* Không xem là crawl trực tiếp TikTok.
* Không dùng làm bằng chứng chính.
* Nếu không đủ 5 nguồn, ghi rõ số nguồn thực tế.

## Fetch rules

Sau khi có search results:

1. Chỉ `web_fetch` URL có khả năng chứa nội dung chính.
2. Ưu tiên fetch:

   * official docs
   * GitHub
   * vendor blog
   * security research
   * news article quan trọng
3. Không fetch quá 5 URL.
4. Nếu fetch fail:

   * vẫn có thể liệt kê URL trong nguồn đã tìm thấy
   * phải ghi `fetch failed`
   * không dùng nguồn đó làm luận cứ chính

## Query refinement

Nếu search lần đầu quá rộng, refine query bằng cách thêm:

* năm hiện tại
* tên sản phẩm
* keyword `release`, `security`, `update`, `API`, `pricing`, `docs`
* tên nguồn nếu cần, ví dụ `GitHub`, `docs`, `blog`

Ví dụ:

```text
OpenClaw ClawHub security 2026
DeepSeek API pricing coding agent
Cursor Cline comparison update
```

## Stop rules

Dừng search khi đã có:

* ít nhất 3 nguồn web đáng tin, hoặc
* 5 nguồn tổng hợp đủ tốt, hoặc
* đã chạm search budget, hoặc
* gặp rate-limit

Không cố search thêm nếu thông tin đã đủ để tạo report ngắn.

## Failure handling

Nếu không tìm được nguồn tốt:

* Không bịa nguồn.
* Không bịa kết luận.
* Viết rõ: "Không tìm được nguồn đủ tin cậy cho topic này."
* Đề xuất topic khác hoặc hành động khác cho hôm nay.

Nếu chỉ có nguồn social:

* Report phải đánh dấu `low confidence`.
* Không đưa ra kết luận chắc chắn.

Nếu chỉ fetch thành công dưới 2 nguồn:

* Report phải có phần "Hạn chế".
* Không viết như report hoàn chỉnh.
