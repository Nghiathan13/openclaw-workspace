# Report Format

Create a Telegram-friendly Morning Information Report using the canonical report style from `style-rules.md`.

Use the configured report language from `current-topics.md` for all user-facing report text and section headings.

## Length

- Production report: max 900 words
- Test report: max 500 words
- Audio script, when enabled: 3-5 minutes or about 450-750 words
- `concise` reports should be shorter: target 250-500 words

If evidence is weak, keep the report shorter.

## Title

Use the style-specific title from `style-rules.md`. Use the date format natural for the configured report language.

## Required Sections

Use the style-specific structure from `style-rules.md`. Do not mix sections from different styles unless needed for source accountability or limitations.

## Source Accountability

Every report must make source quality visible.

For `concise` reports:

- include source URLs or source notes inside relevant bullets
- avoid a large source table unless evidence is complex

For `deep_analysis` reports:

- use the `Source check` section

For `opportunities_risks` reports:

- include evidence/confidence inside each opportunity or risk when useful

When a dedicated source list is used, each source should include:

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

## Relevance And Actions

Connect findings to the configured topics and the current user's use case.

Avoid generic advice. Make each point practical.

Include small actions when useful and when the selected style calls for them.

For `opportunities_risks`, actions must follow from the listed trigger, condition, risk, or watch signal.

## Audio Script

Do not create or include a separate audio script in the customer-facing report.

When audio summary is enabled, runtime audio text is derived after text delivery by `scripts/prepare_audio_script.py` from the delivered report.

For audio-friendly reports:

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
