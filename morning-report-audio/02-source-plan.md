# Source Plan

File này quy định cách chọn nguồn dữ liệu cho Morning Information Report.

Không hard-code topic trong file này. Topic đã được chọn ở `01-topics.md`.

## Goal

Sau khi có Topic Plan từ `01-topics.md`, hãy tạo Source Plan để quyết định cần lấy dữ liệu từ nguồn nào.

## Current mode

Hiện tại chưa có API chính thức cho Facebook và TikTok.

Vì vậy:

* `web` là nguồn chính.
* `facebook` chỉ dùng bằng `site:facebook.com` qua web search.
* `tiktok` chỉ dùng bằng `site:tiktok.com` qua web search.
* Không được nói rằng đã crawl trực tiếp Facebook hoặc TikTok.
* Không được xem Facebook/TikTok site-search result là bằng chứng chính.
* Facebook/TikTok hiện chỉ là `social_signal` và luôn đánh dấu `low confidence`.

## Source types

### 1. Web

Vai trò: nguồn chính.

Dùng cho:

* official docs
* GitHub
* vendor blog
* technical blog
* security research
* news site

Quota mặc định:

* tối đa 5 nguồn web

Độ tin cậy mặc định:

* official / GitHub / vendor / security research: `high`
* news / technical blog: `medium`
* community / forum: `low` hoặc `medium` tùy nội dung

### 2. Facebook site search

Vai trò: tín hiệu social phụ.

Cách lấy hiện tại:

```text
site:facebook.com <topic keywords>
```

Quota mặc định:

* tối đa 5 nguồn nếu tìm được

Quy tắc:

* Chỉ dùng nếu topic cần phản ứng cộng đồng hoặc social signal.
* Luôn đánh dấu `low confidence`.
* Không dùng làm luận cứ chính.
* Nếu không tìm được đủ 5 nguồn thì ghi rõ số nguồn thực tế.
* Không bịa thêm nguồn.
* Không nói là đã crawl Facebook trực tiếp.

### 3. TikTok site search

Vai trò: tín hiệu social/video trend phụ.

Cách lấy hiện tại:

```text
site:tiktok.com <topic keywords>
```

Quota mặc định:

* tối đa 5 nguồn nếu tìm được

Quy tắc:

* Chỉ dùng nếu topic liên quan trend, viral, video content, phản ứng cộng đồng hoặc social signal.
* Luôn đánh dấu `low confidence`.
* Không dùng làm luận cứ chính.
* Nếu không tìm được đủ 5 nguồn thì ghi rõ số nguồn thực tế.
* Không bịa thêm nguồn.
* Không nói là đã crawl TikTok trực tiếp.

### 4. RSS

Vai trò: optional.

Chỉ dùng sau này nếu có Content Watcher hoặc danh sách RSS cố định.

Hiện tại không bắt buộc.

## Default source quota

Cố gắng lấy:

* `web`: tối đa 5 nguồn
* `facebook_site_search`: tối đa 5 nguồn nếu phù hợp
* `tiktok_site_search`: tối đa 5 nguồn nếu phù hợp
* `rss`: optional

Nếu không đủ nguồn, phải ghi rõ:

* nguồn nào lấy đủ
* nguồn nào thiếu
* lý do thiếu nếu biết

Không được bịa URL, số lượng nguồn hoặc nội dung nguồn.

## Source selection rules

### Technical / product / security topics

Ví dụ:

* OpenClaw
* ClawHub
* AI agent security
* DeepSeek API
* Cursor / Cline / Codex
* Telegram bot automation

Ưu tiên:

1. Web official/vendor/GitHub/security research
2. Facebook/TikTok chỉ dùng nếu có social discussion đáng chú ý

Mặc định:

```json
{
  "web": true,
  "facebook_site_search": false,
  "tiktok_site_search": false
}
```

### Social trend topics

Ví dụ:

* AI coding trend trên TikTok
* cộng đồng phản ứng với một công cụ mới
* viral chatbot workflow
* trend crypto trên social

Ưu tiên:

1. Web để xác minh thông tin chính
2. Facebook site search để lấy social signal
3. TikTok site search để lấy video/social trend

Mặc định:

```json
{
  "web": true,
  "facebook_site_search": true,
  "tiktok_site_search": true
}
```

### Crypto / market topics

Ưu tiên:

1. Web/news/vendor để lấy thông tin chính
2. Facebook/TikTok chỉ dùng để xem tâm lý thị trường

Không dùng social signal để kết luận thị trường.

Mặc định:

```json
{
  "web": true,
  "facebook_site_search": true,
  "tiktok_site_search": true
}
```

## Required Source Plan

Trước khi search, tự tạo kế hoạch dạng:

```json
{
  "source_plan": [
    {
      "topic": "...",
      "source_mix": {
        "web": {
          "enabled": true,
          "quota": 5,
          "role": "primary"
        },
        "facebook_site_search": {
          "enabled": true,
          "quota": 5,
          "role": "social_signal",
          "confidence": "low"
        },
        "tiktok_site_search": {
          "enabled": true,
          "quota": 5,
          "role": "social_signal",
          "confidence": "low"
        },
        "rss": {
          "enabled": false,
          "quota": 5,
          "role": "optional"
        }
      },
      "reason": "..."
    }
  ]
}
```

Không cần in Source Plan ra report cuối cùng, nhưng phải dùng nó để quyết định search.

## Future upgrade

Khi có API chính thức cho Facebook hoặc TikTok, có thể đổi:

* `facebook_site_search` → `facebook_api`
* `tiktok_site_search` → `tiktok_api`

Khi đó mới được xem Facebook/TikTok là nguồn thu thập trực tiếp.

Trước khi có API, mọi kết quả Facebook/TikTok đều là site-search fallback và phải đánh dấu `low confidence`.
