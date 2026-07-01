# Output Rules

This file controls the final Telegram output for the Morning Report.

## Final Output

The final answer must start directly with the report title:

```md
# Morning Report — ...
```

For test runs:

```md
# Morning Report — Test — ...
```

Do not write anything before the title.

If a manual test run already sent one short acknowledgement, the later final report message must still start directly with the report title.

Do not include internal logs such as:

- Topic Plan
- Source Plan
- search/fetch progress
- debug messages
- internal reasoning
- previous-run context

## Progress Messages

Do not expose workflow progress to the customer.

For scheduled/cron runs:

- send no acknowledgement or progress messages
- send only the final report and the optional `MEDIA:` directive

For manual test runs:

- at most one short acknowledgement is allowed before work begins
- after the acknowledgement, send no additional messages until the final report

Never send customer-visible phase messages such as:

- "Good, everything checks out"
- "Let me start building the report"
- "Now let me compose the report"
- "Audio generated successfully"
- "Let me record the run history"
- "Now delivering the test report"

After the final report is sent, do not send a second summary, recap, or delivery-status message unless the user explicitly asks. The report itself is the deliverable.

## Fresh Run

Treat every run as a fresh run.

Use only:

- workflow files read in the current run
- search/fetch results from the current run
- current topic configuration from `current-topics.md`

Do not reuse previous report conclusions unless the user explicitly asks.

## Source Rules

In the source table/list:

- URLs must be complete, including `https://`
- do not invent URLs
- do not use fetch-failed, search-result-only, social, or weak community sources as main evidence
- mention fetch failures only in sources or limitations

## Claim Rules

Do not make strong claims unless fetched sources support them.

If evidence is weak, use cautious wording in the configured report language.

## Failure Rules

If search or fetch fails:

- do not retry repeatedly
- use available sources
- mention the issue in limitations
- do not make the report longer to compensate

If audio generation fails:

- still send the text report
- do not claim an MP3 was delivered
- mention the audio failure briefly after the report or in delivery status
- keep any generated history manifest for troubleshooting

## Telegram Media

If audio summary is enabled and MP3 generation succeeds, the final Telegram output must include one standalone media directive after the text report:

```text
MEDIA:<absolute-mp3-path>
```

For the default audio command, use:

```text
MEDIA:/tmp/morning-report.mp3
```

Rules:

- put `MEDIA:` on its own line
- use the actual generated MP3 path
- do not wrap it in Markdown, quotes, or bullets
- do not include `MEDIA:` when audio is disabled or generation failed
- do not replace it with a sentence saying the file needs to be sent

## Telegram Style

Keep output easy to read:

- short paragraphs
- concise bullets
- simple Markdown
- compact source table/list
- limited emoji
- production report: max 900 words
- test report: max 500 words

## Final Check

Before sending, verify:

1. output starts with the title
2. configured report language is used
3. no internal logs or progress messages are included
4. URLs are complete
5. weak sources are not used as main evidence
6. limitations are included
7. audio content follows the configured audio preference
8. the full audio script is not included in the customer-facing text report unless requested
9. successful audio output includes a standalone `MEDIA:<path>` directive
10. no second summary or delivery-status message is sent after the report
