# Audio Runtime

Use this reference only when Morning Report audio summary is enabled.

## Runtime

The MVP audio runtime uses Google TTS through `skills/morning-report/scripts/generate_audio.py`.

This avoids asking the language model to perform fragile audio operations. The helper handles:

- text normalization
- sentence-aware chunking
- Google TTS requests
- MP3 chunk storage
- MP3 merge
- runtime history manifest

## Limits

Google TTS has a practical request limit of about 200 characters per call. Use a safe default of 180 characters per chunk.

Do not send the full 3-5 minute script in one request.

## Command

Derive the clean spoken script from the already-delivered text report. Do not ask the language model to write a second audio script after the text report has been sent.

```bash
python3 skills/morning-report/scripts/prepare_audio_script.py \
  --report-file /tmp/morning-report.md \
  --output /tmp/morning-report-audio.txt \
  --max-words 750
```

Then validate chunking and target duration without calling TTS:

```bash
python3 skills/morning-report/scripts/generate_audio.py \
  --text-file /tmp/morning-report-audio.txt \
  --lang "<configured-report-language>" \
  --chunk-limit 180 \
  --dry-run
```

The dry-run JSON includes:

- `word_count`
- `estimated_minutes`
- `length_ok`
- `length_warnings`
- `chunk_count`

If `length_ok` is false, do not block the already-delivered text report. For scheduled runs, continue with TTS unless the audio script is empty or invalid. For manual operator testing, mention the length warning only if the operator asks.

Then run:

```bash
python3 skills/morning-report/scripts/generate_audio.py \
  --text-file /tmp/morning-report-audio.txt \
  --output /tmp/morning-report.mp3 \
  --lang "<configured-report-language>" \
  --chunk-limit 180
```

Replace `<configured-report-language>` with the configured `Report language` from `skills/morning-report/state/current-topics.md` or `config_status.py`.

Do not copy a language from examples, previous runs, topic names, user chat language, or the VPS locale. The audio language must follow the configured report language for this run.

The helper accepts common English language names and language codes, such as `English`, `en`, `Japanese`, or `ja`.

## History

Audio history is stored under:

```text
skills/morning-report/state/audio-history/YYYY-MM-DD/<run-id>/
```

Each run directory contains:

- `audio-script.txt`
- `chunks/`
- `morning-report.mp3`
- `manifest.json`
- `ffmpeg-list.txt` when ffmpeg merge is used

Do not manually edit history files during normal report generation. Use `manifest.json` for troubleshooting.

## Telegram Delivery

When audio generation succeeds and the delivery channel is Telegram, attach the MP3 by sending a standalone media directive after the text report message:

```text
MEDIA:<absolute-mp3-path>
```

For the default command, use:

```text
MEDIA:/tmp/morning-report.mp3
```

Use the actual MP3 path from the helper output or `manifest.json` if it differs. Do not wrap the directive in backticks, bullets, quotes, or explanatory text. Do not replace it with a sentence like "file needs to be sent"; Telegram needs the `MEDIA:` line.

## Merge

The helper uses `ffmpeg` concat when available. If `ffmpeg` is unavailable, it falls back to binary MP3 append for MVP compatibility.

## Failure Handling

Audio generation is optional relative to the text report.

If audio generation fails:

- keep the already-sent text Morning Report as successful delivery
- do not claim audio was delivered
- do not emit a `MEDIA:` directive for a missing or failed MP3
- send one short customer-visible notice in the configured report language that audio generation failed this time
- preserve the history manifest if one was created
