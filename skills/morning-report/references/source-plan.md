# Source Plan

Choose source types for the selected topics.

## Current Mode

- Web is the primary source.
- Facebook and TikTok are available only through web search using `site:facebook.com` and `site:tiktok.com`.
- Do not claim direct Facebook/TikTok crawling.
- Treat Facebook/TikTok results as low-confidence social signals only.

## Source Types

### Web

Use for official docs, GitHub, vendor blogs, security research, technical blogs, and news.

Default quota: up to 5 web sources.

Default confidence:

- official / GitHub / vendor / security research: high
- news / technical blog: medium
- community/forum: low or medium depending on quality

### Facebook Site Search

Use only when the topic needs community reaction or social signals.

Query pattern:

```text
site:facebook.com <topic keywords>
```

Always mark as `low` confidence and `social_signal`.

### TikTok Site Search

Use only when the topic involves trends, viral content, video/social reaction, or market sentiment.

Query pattern:

```text
site:tiktok.com <topic keywords>
```

Always mark as `low` confidence and `social_signal`.

### RSS

Optional. Use only if a feed list or watcher exists in the runtime.

## Defaults By Topic Type

Technical/product/security topics:

```json
{"web": true, "facebook_site_search": false, "tiktok_site_search": false}
```

Social trend topics:

```json
{"web": true, "facebook_site_search": true, "tiktok_site_search": true}
```

Crypto/market topics:

```json
{"web": true, "facebook_site_search": true, "tiktok_site_search": true}
```

Do not use social signals as market conclusions.

## Source Plan Shape

```json
{
  "source_plan": [
    {
      "topic": "...",
      "source_mix": {
        "web": {"enabled": true, "quota": 5, "role": "primary"},
        "facebook_site_search": {"enabled": false, "quota": 5, "role": "social_signal", "confidence": "low"},
        "tiktok_site_search": {"enabled": false, "quota": 5, "role": "social_signal", "confidence": "low"},
        "rss": {"enabled": false, "quota": 5, "role": "optional"}
      },
      "reason": "..."
    }
  ]
}
```

Do not print the Source Plan in the final report.
