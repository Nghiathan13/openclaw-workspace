# Topic Router

Select the topics for the current Morning Report run.

## Read First

- `skills/morning-report/state/current-topics.md`
- `skills/morning-report/references/policy.md`

If `current-topics.md` contains `Status: not_configured`, stop. Do not select fallback topics.

## Task

Create an internal Topic Plan before search.

Use only configured topics from `current-topics.md`:

- Prefer `User priority`
- Select up to 2 active topics for deeper search
- Add at most 1 optional topic only if it is highly relevant or likely to have major news
- If a topic is too broad, narrow it for search without changing the saved topic

## Topic Plan Shape

```json
{
  "selected_topics": [
    {
      "topic": "...",
      "priority": "high | medium | low",
      "search_intent": "official_update | security | technical_guide | product_update | market_news | social_signal | general_news",
      "keywords": ["..."],
      "reason": "..."
    }
  ]
}
```

Do not print the Topic Plan in the final report.
