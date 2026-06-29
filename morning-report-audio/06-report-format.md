# Report Format

File này quy định format đầu ra cuối cùng cho Morning Information Report.

Report phải viết bằng tiếng Việt, ngắn gọn, dễ đọc trên Telegram.

## Output length

Mặc định:

* Report chính: tối đa 900 từ
* Nếu là bản test: tối đa 500 từ
* Audio script: 1–2 phút đọc

Không viết quá dài nếu nguồn không đủ mạnh.

## Report title

Tiêu đề bắt buộc:

```md
# Morning Report — <ngày/tháng/năm>
```

Ví dụ:

```md
# Morning Report — 29/06/2026
```

Nếu là bản test:

```md
# Morning Report — Test — <ngày/tháng/năm>
```

## Required sections

Report cuối phải có đúng các phần sau, theo thứ tự.

---

## 1. Tóm tắt nhanh

Viết 3–5 bullet.

Mỗi bullet phải gồm:

* thông tin chính
* vì sao đáng chú ý
* không quá 2 dòng

Không đưa nguồn yếu vào tóm tắt nếu chưa được xác minh.

Format:

```md
## 1. Tóm tắt nhanh

- ...
- ...
- ...
```

---

## 2. Nguồn đã dùng

Tạo bảng nguồn.

Bảng bắt buộc có các cột:

```md
| # | URL | Loại nguồn | Fetch status | Độ tin cậy | Vai trò | Ghi chú |
|---|-----|------------|--------------|------------|--------|--------|
```

Giá trị hợp lệ:

### Loại nguồn

* official
* GitHub
* vendor
* security research
* technical blog
* news
* community
* social
* unknown

### Fetch status

* fetched
* fetch_failed
* search_result_only

### Độ tin cậy

* high
* medium
* low

### Vai trò

* main_evidence
* supporting_evidence
* social_signal
* background
* excluded

Quy tắc:

* URL phải là URL thật đã tìm được.
* Không bịa URL.
* Nếu fetch fail, ghi rõ `fetch_failed`.
* Nếu Facebook/TikTok lấy qua site search, ghi `social_signal` và `low`.

---

## 3. Phân tích chính

Phần này phải ngắn, có căn cứ.

Bắt buộc gồm 4 ý:

```md
## 3. Phân tích chính

**Điểm giống nhau:**
- ...

**Điểm khác nhau hoặc mâu thuẫn:**
- ...

**Kết luận đáng tin nhất:**
- ...

**Cần kiểm chứng thêm:**
- ...
```

Quy tắc:

* Chỉ dùng nguồn `fetched` và `high/medium` làm luận cứ chính.
* Không dùng nguồn `fetch_failed` làm kết luận.
* Không dùng Facebook/TikTok site-search làm kết luận chính.
* Nếu không có mâu thuẫn, ghi: `Chưa thấy mâu thuẫn rõ từ các nguồn đã đọc.`
* Nếu dữ liệu yếu, ghi rõ: `Dữ liệu chưa đủ mạnh để kết luận chắc chắn.`

---

## 4. Ý nghĩa với Nghĩa

Phần này phải liên hệ trực tiếp đến việc Nghĩa đang làm.

Ưu tiên liên hệ đến:

* OpenClaw setup
* Telegram bot automation
* cron/report workflow
* AI agent security
* ClawHub skills
* DeepSeek/API/model choice
* web app/SaaS/project cá nhân

Format:

```md
## 4. Ý nghĩa với Nghĩa

- ...
- ...
- ...
```

Không viết chung chung. Mỗi ý phải có tác động thực tế.

---

## 5. Việc nên làm hôm nay

Đưa đúng 3 việc.

Mỗi việc gồm:

* việc cần làm
* lý do ngắn
* kết quả mong muốn

Format:

```md
## 5. Việc nên làm hôm nay

1. ...
   - Lý do: ...
   - Kết quả: ...

2. ...
   - Lý do: ...
   - Kết quả: ...

3. ...
   - Lý do: ...
   - Kết quả: ...
```

Quy tắc:

* Việc phải nhỏ và làm được trong ngày.
* Không đưa việc quá lớn như "xây toàn bộ hệ thống".
* Ưu tiên việc liên quan đến topic report.

---

## 6. Bản đọc audio ngắn

Viết đoạn script tự nhiên, dễ đọc thành audio.

Format:

```md
## 6. Bản đọc audio ngắn

<đoạn script>
```

Yêu cầu:

* 1–2 phút đọc
* không dùng bảng
* không dùng bullet
* văn phong tự nhiên
* không hype
* nêu rõ nếu nguồn chưa chắc chắn

---

## 7. Hạn chế

Luôn có phần hạn chế ở cuối.

Format:

```md
## 7. Hạn chế

- ...
- ...
```

Bắt buộc ghi nếu có:

* search bị rate-limit
* fetch fail
* chỉ có nguồn social
* dưới 2 nguồn fetch thành công
* không đủ nguồn high confidence
* Facebook/TikTok chỉ là site-search fallback

Nếu không có hạn chế đáng kể, ghi:

```md
Không có hạn chế lớn trong lần chạy này.
```

## Style rules

* Viết ngắn gọn.
* Không dùng văn phong quảng cáo.
* Không dùng từ quá mạnh nếu nguồn chưa đủ.
* Không bịa số liệu, ngày tháng, URL.
* Không nói chắc khi chỉ có nguồn yếu.
* Không dùng quá nhiều emoji.
* Không dùng markdown quá phức tạp vì report gửi qua Telegram.
