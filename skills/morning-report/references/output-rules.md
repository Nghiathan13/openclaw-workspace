# Output Rules

This file controls the customer-visible Telegram output for the Morning Report.

## Text Report Message

The text report message must start directly with the report title:

```md
# <style-specific title> — ...
```

For test runs:

```md
# <style-specific title> — Test — ...
```

The allowed title meaning comes from `style-rules.md`: Morning Brief, Morning Analysis, or Opportunities & Risks. Translate the title naturally when the configured report language is not English.

Do not write anything before the title.

If a manual test run already sent one short acknowledgement, the later text report message must still start directly with the report title.

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
- send the text report first
- then send only the optional audio `MEDIA:` directive or the short audio-failure notice

For manual test runs:

- at most one short acknowledgement is allowed before work begins
- after the acknowledgement, send no additional messages until the text report

Never send customer-visible phase messages such as:

- "Good, everything checks out"
- "Let me start building the report"
- "Now let me compose the report"
- "Audio generated successfully"
- "Let me record the run history"
- "Now delivering the test report"

After the text report is sent, do not send a second summary, recap, or delivery-status message unless the user explicitly asks. The only automatic follow-up messages allowed are:

- a standalone `MEDIA:<path>` directive when audio succeeds
- one short audio-failure notice when audio was requested but could not be generated

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
- send one short audio-failure notice after the report
- keep any generated history manifest for troubleshooting

## Telegram Media

If audio summary is enabled and MP3 generation succeeds, send one standalone media directive after the text report:

```text
MEDIA:<absolute-mp3-path>
```

For the default audio command, use:

```text
MEDIA:/tmp/morning-report.mp3
```

Rules:

- put `MEDIA:` on its own line
- send it after the text report message
- use the actual generated MP3 path
- do not wrap it in Markdown, quotes, or bullets
- do not include `MEDIA:` when audio is disabled or generation failed
- do not replace it with a sentence saying the file needs to be sent

## Audio Failure Notice

If audio was requested but failed after the text report was delivered, send one short notice in the configured report language.

Example in English:

```text
Audio summary could not be generated this time. The text report above was delivered successfully.
```

Do not include logs, stack traces, provider details, file paths, or retry plans in the customer-facing notice.

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

1. text report starts with the title
2. configured report language is used
3. output structure matches the canonical report style
4. no internal logs or progress messages are included
5. URLs are complete
6. weak sources are not used as main evidence
7. limitations are included
8. audio content follows the configured audio preference
9. the full audio script is not included in the customer-facing text report unless requested
10. text report is sent before audio generation or audio delivery
11. successful audio output is sent as a standalone `MEDIA:<path>` directive after the text report
12. audio failure sends one short notice, not a second report summary
