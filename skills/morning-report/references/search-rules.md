# Search Rules

Search enough to produce a useful short report without over-querying or relying on weak sources.

## Budget

Per report run:

- `web_search`: max 3 calls
- `web_fetch`: max 5 URLs
- Rate-limit retry: max 1 retry

If still rate-limited, use available results and mention the limitation.

## Order

1. Search primary web sources first.
2. Fetch the strongest web sources.
3. If enabled, search Facebook site results.
4. If enabled, search TikTok site results.
5. Fetch social URLs only when readable and necessary.

## Query Rules

- Keep queries short and specific.
- Prefer English keywords for global topics.
- Add local-language keywords only when the configured topic or market requires them.
- Add current year, product name, `release`, `security`, `update`, `API`, `pricing`, `docs`, or source names when refinement is needed.

## Source Priority

Prefer sources in this order:

1. Official docs
2. GitHub repository / issue / release notes
3. Vendor blog
4. Security research
5. Technical blog
6. News site
7. Community/forum/social

Do not use community or social sources as main evidence unless a reliable source supports the claim.

## Stop Rules

Stop searching when one condition is met:

- at least 3 reliable web sources are available
- 5 total useful sources are available
- the search budget is reached
- rate-limit blocks further search

## Failure Rules

If reliable sources are not found:

- do not invent sources or conclusions
- say evidence is insufficient
- add the issue to limitations

If fewer than 2 sources were fetched successfully, keep the report cautious and include limitations.
