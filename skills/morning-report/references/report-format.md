# Report Format

Create a concise Telegram-friendly Morning Information Report.

Use the configured report language from `current-topics.md` for all user-facing report text and section headings.

## Length

- Production report: max 900 words
- Test report: max 500 words
- Audio script, when enabled: 3-5 minutes or about 450-750 words

If evidence is weak, keep the report shorter.

## Title

Start with:

```md
# Morning Report — <date>
```

For test runs:

```md
# Morning Report — Test — <date>
```

Use the date format natural for the configured report language.

## Required Sections

The report must include these sections in this order. Translate headings into the configured report language.

1. Quick Summary
2. Sources Used
3. Main Analysis
4. Relevance To You
5. Actions For Today
6. Audio Script, only if audio summary is enabled
7. Limitations

If audio summary is disabled, omit the Audio Script section or state briefly that audio was not requested, depending on the output rules/runtime requirement.

## Quick Summary

Write 3-5 concise bullets.

Each bullet should include:

- the key information
- why it matters
- no more than 2 lines

Do not include unverified weak/social claims in the quick summary.

## Sources Used

Use a compact table or bullet list suitable for Telegram.

Each source must include:

- URL
- source type
- fetch status
- confidence
- role
- note

Allowed source types:

- official
- GitHub
- vendor
- security research
- technical blog
- news
- community
- social
- unknown

Allowed fetch status values:

- fetched
- fetch_failed
- search_result_only

Allowed confidence values:

- high
- medium
- low

Allowed roles:

- main_evidence
- supporting_evidence
- social_signal
- background
- excluded

## Main Analysis

Include:

- agreements across sources
- differences or conflicts
- most reliable conclusion
- what still needs verification

Use only fetched high/medium-confidence sources as main evidence.

## Relevance To You

Connect findings to the configured topics and the current user's use case.

Avoid generic advice. Make each point practical.

## Actions For Today

Include exactly 3 small actions when useful.

Format:

```md
1. Action
   - Reason:
   - Expected result:
```

## Audio Script

Create only when audio summary is enabled. This script is for TTS handoff, not for the customer-facing text report unless the user explicitly asks to see it.

Requirements:

- natural spoken style
- no tables
- no bullet lists
- no hype
- mention uncertainty when evidence is weak
- suitable for direct TTS input

## Limitations

Always include limitations.

Mention any of:

- search rate limits
- fetch failures
- only social evidence
- fewer than 2 fetched sources
- insufficient high-confidence sources
- Facebook/TikTok used only as site-search fallback

If there are no major limitations, say so briefly in the configured report language.

## Style

- concise
- factual
- non-promotional
- simple Markdown
- limited emoji
- no invented numbers, dates, URLs, or source claims
