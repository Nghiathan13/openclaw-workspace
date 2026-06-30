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

Write the clean spoken script to a temporary text file, then run:

```bash
python3 skills/morning-report/scripts/generate_audio.py \
  --text-file /tmp/morning-report-audio.txt \
  --output /tmp/morning-report.mp3 \
  --lang vi \
  --chunk-limit 180
```

Use the configured report language for `--lang`. The helper accepts common names such as `Vietnamese` or `English`, and also accepts codes such as `vi` or `en`.

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

When audio generation succeeds and the delivery channel is Telegram, attach the MP3 by adding a standalone media directive to the final output:

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

- still send the text Morning Report
- do not claim audio was delivered
- do not emit a `MEDIA:` directive for a missing or failed MP3
- mention briefly that audio generation failed
- preserve the history manifest if one was created
