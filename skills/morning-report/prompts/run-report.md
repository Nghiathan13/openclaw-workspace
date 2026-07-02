# Run Morning Report

Use this prompt to generate, preview, test, or scheduled-run the Morning Report.

Do not use this prompt for first-time setup or topic updates.

## Read First

- `USER.md`
- `skills/morning-report/state/current-topics.md` if it exists
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

If the helper reports missing required configuration, `state.exists: false`, or exits non-zero, stop. Do not search, fetch, analyze, or generate a report. Ask the operator/user to complete setup first.

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

## Customer-Visible Messaging

Keep report generation quiet.

- For scheduled/cron runs: do not send progress, acknowledgement, or status messages before the text report.
- For manual test runs: send at most one short acknowledgement before tool work begins, only if a response is needed to reassure the user. After that, send no customer-visible messages until the text report.
- Never send phase updates such as "everything checks out", "building the report", "composing the report", "preparing audio", "recording history", or "delivering to Telegram".
- Keep search plans, source plans, fetch progress, audio generation status, and history recording status internal unless there is a failure the user must know about.

## Workflow

Read these references in order:

1. `skills/morning-report/references/topic-router.md`
2. `skills/morning-report/references/source-plan.md`
3. `skills/morning-report/references/search-rules.md`
4. `skills/morning-report/references/source-scoring.md`
5. `skills/morning-report/references/analysis-rules.md`
6. `skills/morning-report/references/style-rules.md`
7. `skills/morning-report/references/report-format.md`
8. `skills/morning-report/references/audio-script.md` only if audio summary is enabled
9. `skills/morning-report/references/audio-runtime.md` only if audio summary is enabled
10. `skills/morning-report/references/report-history.md`
11. `skills/morning-report/references/output-rules.md`

Then generate a fresh Morning Information Report using only:

- configured topics
- configured report language
- canonical report style from `config_status.py` when available
- configured audio preference
- search/fetch results from this run

Do not reuse old conclusions, old sources, old report content, or hard-coded examples. Do not invent a report style outside `concise`, `deep_analysis`, or `opportunities_risks`.

## Delivery Order

The text report is the primary deliverable. Audio is optional follow-up media.

After the final text report is ready:

1. Save the exact text report to `/tmp/morning-report.md`.
2. Send the text report through Telegram immediately. The text report message must start directly with the report title.
3. Continue with audio only after the text report has been sent.

Do not wait for audio generation before sending the text report.

## Audio

If audio summary is enabled:

1. Prepare the audio script from the already-delivered report using `skills/morning-report/scripts/prepare_audio_script.py`.
2. Save only the audio script to `/tmp/morning-report-audio.txt`.
3. Run the audio helper dry-run from `skills/morning-report/references/audio-runtime.md`, passing the configured report language to `--lang`.
4. Run `skills/morning-report/scripts/generate_audio.py` following `skills/morning-report/references/audio-runtime.md`, passing the same configured report language to `--lang`.
5. When audio generation succeeds, send a second Telegram message containing only the standalone `MEDIA:<absolute-mp3-path>` directive so Telegram attaches the MP3.

Do not use the language model to write a separate audio script after the text report has been sent. The audio script must be derived from the delivered report by `prepare_audio_script.py`.

If any audio step fails after the text report was sent:

1. Do not retry repeatedly.
2. Do not emit a `MEDIA:` directive.
3. Send one short customer-visible notice in the configured report language saying that the text report was delivered but the audio summary could not be generated this time.
4. Record history with `--audio-status failed`.

Never use a language from a command example, previous manifest, topic language, user chat language, or VPS locale for audio. Audio must use the configured report language for this run.

Use the actual MP3 path returned by the audio manifest or helper output. For the default command, this is usually:

```text
MEDIA:/tmp/morning-report.mp3
```

Do not only write that the file "needs to be sent". The `MEDIA:` directive is the delivery instruction.

Do not include the full audio script in the customer-facing text report unless the user explicitly asks for it.

## History

After text delivery and any audio follow-up attempt, record the run with `skills/morning-report/scripts/record_report.py` following `skills/morning-report/references/report-history.md`.

Pass source URLs with `--source-url` and failed fetch URLs with `--failed-url` when available. Use `--audio-status generated`, `failed`, `disabled`, or `not_requested` according to the actual audio outcome. Use `--delivery-status sent` after the text report has been sent, even if audio generation later fails.

If report history recording fails, do not block text report delivery. Keep the customer-facing report clean and mention the history failure only to the operator when appropriate.

## Output

Follow `skills/morning-report/references/output-rules.md` exactly. The text report message must start directly with the report title. Do not send a second customer-facing summary after the report unless the user explicitly asks for one. The only allowed automatic follow-up messages are the audio `MEDIA:` directive or the short audio-failure notice described above.
