# Run Morning Report

Use this prompt to generate, preview, test, or scheduled-run the Morning Report.

Do not use this prompt for first-time setup or topic updates.

## Read First

- `USER.md`
- `skills/morning-report/state/current-topics.md`
- `skills/morning-report/references/policy.md`
- `skills/morning-report/references/report-history.md`

Run the status helper before starting search:

```bash
python3 skills/morning-report/scripts/config_status.py
```

If `state.setup_status` is `paused` or `disabled`, stop. Do not search, fetch, analyze, generate, or send a report. For scheduled runs, stay quiet unless the runtime requires a status response. For manual runs, say Morning Report is paused/disabled and can be resumed on request.

If status is not paused/disabled, verify runnable configuration:

```bash
python3 skills/morning-report/scripts/config_status.py --check
```

If the helper reports missing required configuration or exits non-zero, stop. Do not search, fetch, analyze, or generate a report. Ask the operator/user to complete setup first.

## Required State

Run only when status shows:

- `configured: true`
- at least one active topic
- delivery time
- timezone
- report style
- report language
- audio summary preference
- delivery channel

Use only configured values. Do not invent missing values.

## Workflow

Read these references in order:

1. `skills/morning-report/references/topic-router.md`
2. `skills/morning-report/references/source-plan.md`
3. `skills/morning-report/references/search-rules.md`
4. `skills/morning-report/references/source-scoring.md`
5. `skills/morning-report/references/analysis-rules.md`
6. `skills/morning-report/references/report-format.md`
7. `skills/morning-report/references/audio-script.md` only if audio summary is enabled
8. `skills/morning-report/references/audio-runtime.md` only if audio summary is enabled
9. `skills/morning-report/references/report-history.md`
10. `skills/morning-report/references/output-rules.md`

Then generate a fresh Morning Information Report using only:

- configured topics
- configured report language
- configured report style
- configured audio preference
- search/fetch results from this run

Do not reuse old conclusions, old sources, old report content, or hard-coded examples.

## Audio

If audio summary is enabled:

1. Generate a clean spoken audio script from the final report.
2. Save only the audio script to a temporary text file.
3. Run `skills/morning-report/scripts/generate_audio.py` following `skills/morning-report/references/audio-runtime.md`.
4. Send the text report through Telegram.
5. When audio generation succeeds, append a standalone `MEDIA:<absolute-mp3-path>` line to the final Telegram output so Telegram attaches the MP3.

Use the actual MP3 path returned by the audio manifest or helper output. For the default command, this is usually:

```text
MEDIA:/tmp/morning-report.mp3
```

Do not only write that the file "needs to be sent". The `MEDIA:` directive is the delivery instruction.

If audio generation fails, still send the text report. Do not claim audio was delivered. Mention the audio failure briefly after the report or in the delivery status.

Do not include the full audio script in the customer-facing text report unless the user explicitly asks for it.

## History

After generating the final customer-facing report, save the report text to a temporary Markdown file and record the run with `skills/morning-report/scripts/record_report.py` following `skills/morning-report/references/report-history.md`.

Pass source URLs with `--source-url` and failed fetch URLs with `--failed-url` when available. Use `--audio-status generated`, `failed`, `disabled`, or `not_requested` according to the actual audio outcome. Use `--delivery-status sent` only after the text report and required `MEDIA:` directive were emitted for Telegram delivery; otherwise use `prepared`, `failed`, or `not_recorded`.

If report history recording fails, do not block text report delivery. Keep the customer-facing report clean and mention the history failure only to the operator when appropriate.

## Output

Follow `skills/morning-report/references/output-rules.md` exactly. The final Telegram text output must start directly with the report title.
