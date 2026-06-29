# Output Rules

File này quy định output cuối cùng của Morning Information Report.

Mục tiêu là đảm bảo kết quả gửi về Telegram sạch, không có log nội bộ, không có reasoning thừa, không dùng context cũ.

## Final answer boundary

Output cuối cùng phải bắt đầu trực tiếp bằng title:

```md
# Morning Report — ...
```

Nếu là bản test:

```md
# Morning Report — Test — ...
```

Không viết bất kỳ dòng nào trước title.

Không in:

* Topic Plan
* Source Plan
* Search log
* Fetch log
* Debug log
* Reasoning nội bộ
* "Đang thực thi"
* "Đã đọc file"
* "Đã có context từ lần chạy trước"

## Fresh run rule

Mỗi lần chạy phải được xem là một fresh run.

Không dùng kết luận, nguồn, hoặc context từ lần chạy trước, trừ khi Nghĩa yêu cầu rõ ràng.

Chỉ dùng:

* các file workflow đã đọc trong lần chạy hiện tại
* kết quả search/fetch trong lần chạy hiện tại
* topic hiện tại từ `current-topics.md`

## URL rule

Trong bảng nguồn, URL phải là URL đầy đủ.

Đúng:

```text
https://github.com/NVIDIA/NemoClaw
```

Sai:

```text
github.com/NVIDIA/NemoClaw
```

Không bịa URL. Nếu chỉ có domain hoặc URL không đầy đủ, không đưa vào bảng nguồn chính.

## Claim wording rule

Không dùng claim quá mạnh nếu nguồn không chứng minh rõ.

Tránh các cụm:

* "hoàn toàn mới"
* "chắc chắn"
* "production-ready"
* "official partnership"
* "đã xác nhận"
* "đột phá"
* "cách mạng"

Chỉ dùng các cụm đó nếu nguồn đã đọc nói rõ.

Nếu chưa chắc, viết nhẹ hơn:

* "có dấu hiệu"
* "nguồn gần đây cho thấy"
* "cần kiểm chứng thêm"
* "chưa đủ dữ liệu để kết luận chắc chắn"

## Source usage rule

Không dùng nguồn sau làm luận cứ chính:

* fetch failed
* search result only
* Facebook site-search
* TikTok site-search
* social signal
* community source yếu

Các nguồn đó chỉ được dùng làm tín hiệu phụ hoặc ghi trong phần hạn chế.

## Rate-limit rule

Nếu `web_search` bị rate-limit:

* không retry nhiều lần
* dùng kết quả đã có
* ghi rõ trong phần `## 7. Hạn chế`
* không làm report dài thêm để bù thiếu dữ liệu

## Telegram readability rule

Report phải dễ đọc trên Telegram.

Yêu cầu:

* đoạn ngắn
* bullet ngắn
* bảng không quá dài
* không dùng markdown phức tạp
* không dùng quá nhiều emoji
* không viết quá 900 từ cho production
* không viết quá 500 từ cho bản test

## Final check

Trước khi trả lời, tự kiểm tra:

1. Output có bắt đầu bằng title không?
2. Có log nội bộ trước title không?
3. URL đã đầy đủ chưa?
4. Có dùng nguồn fetch fail làm kết luận không?
5. Có ghi hạn chế nếu search/fetch lỗi không?
6. Có giữ đúng format trong `06-report-format.md` không?
