# Source Scoring

Score every source before using it in the report.

## Confidence

Use one of:

- `high`
- `medium`
- `low`

High confidence:

- official docs
- official release notes
- official GitHub repository/issues/discussions
- vendor blog
- reputable security research
- official API documentation

Medium confidence:

- reputable news sites
- technical blogs with clear authorship
- analysis from identifiable organizations/authors
- high-quality unofficial documentation
- reliable aggregators

Low confidence:

- Facebook/TikTok/site-search social results
- social posts
- forums/comments
- weak community sources
- unclear authorship
- SEO/clickbait pages
- sources that cannot be fetched

## Fetch Status

Use one of:

- `fetched`
- `fetch_failed`
- `search_result_only`

Only `fetched` sources can support main analysis.

## Roles

Use one of:

- `main_evidence`
- `supporting_evidence`
- `social_signal`
- `background`
- `excluded`

A source can be `main_evidence` only if:

- confidence is `high` or `medium`
- fetch status is `fetched`
- content is directly relevant
- it is not a social signal

## Report Confidence

High:

- at least 2 high-confidence sources
- at least 2 fetched sources
- no major unresolved conflict

Medium:

- at least 1 high-confidence source, or multiple medium-confidence sources
- enough fetched content for basic analysis

Low:

- only social/community/search snippets
- fewer than 2 fetched sources
- repeated rate limits
- unresolved source conflicts

If confidence is low, state it in limitations.

## Source Table Fields

Final report source table/list must include:

- URL
- source type
- fetch status
- confidence
- role
- note

Do not invent URLs or source details.
