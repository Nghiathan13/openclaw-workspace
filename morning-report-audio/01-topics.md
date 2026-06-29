# Topic Router

File này quy định cách đọc, chuẩn hóa và chọn topic cho Morning Information Report.

Không hard-code danh sách topic cố định trong file này.

## Input

Đọc topic hiện tại từ file:

`/home/node/.openclaw/workspace/usecases/morning-report/topics/current-topics.md`

## Task

Sau khi đọc `current-topics.md`, hãy tạo Topic Plan trước khi search.

Topic Plan phải gồm:

1. `selected_topics`
   - Chọn tối đa 2 topic chính để search sâu.
   - Có thể chọn thêm tối đa 1 topic phụ nếu có tin rất đáng chú ý.

2. `normalized_keywords`
   - Chuyển topic của user thành keyword search rõ ràng.
   - Bao gồm cả tiếng Anh và tiếng Việt nếu cần.

3. `search_intent`
   - Phân loại topic thuộc nhóm nào:
     - official_update
     - security
     - technical_guide
     - product_update
     - market_news
     - social_signal
     - general_news

4. `priority`
   - high
   - medium
   - low

5. `reason`
   - Giải thích ngắn vì sao chọn topic đó.

## Topic selection rules

1. Ưu tiên topic trong mục `User priority`.
2. Không search toàn bộ topic cùng lúc.
3. Chỉ chọn topic có khả năng có thông tin mới hoặc hữu ích.
4. Nếu topic quá rộng, thu hẹp lại trước khi search.
5. Nếu topic thuộc `Optional topics`, chỉ chọn nếu có tin lớn hoặc liên quan trực tiếp.
6. Nếu không có topic rõ ràng, mặc định ưu tiên:
   - OpenClaw
   - Telegram bot automation
   - AI coding tools

## Output before searching

Trước khi gọi `web_search`, phải tự tạo kế hoạch dạng:

```json
{
  "selected_topics": [
    {
      "topic": "...",
      "priority": "high",
      "search_intent": "...",
      "keywords": ["...", "..."],
      "reason": "..."
    }
  ]
}