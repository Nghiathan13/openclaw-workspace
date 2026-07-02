# Audio Script Rules

Use this file only when audio summary is enabled in `current-topics.md`.

## Duration

Target 3-5 minutes, about 450-750 words depending on the configured report language.

If evidence is weak, stay closer to 3 minutes and state limitations clearly.

At runtime, derive the audio script from the already-delivered text report with `scripts/prepare_audio_script.py`. Do not ask the language model to create a separate audio script after text delivery.

Before generating MP3, validate the script with `generate_audio.py --dry-run`. If the helper reports `length_ok: false` during a scheduled run, do not block the delivered text report. Continue unless the script is empty or invalid.

## Content

The script should include:

1. brief opening with date and topics
2. 3-5 key points
3. practical relevance
4. 3 small actions, when useful
5. limitations or uncertainty

## Style

- natural spoken language
- calm and clear
- no tables
- no long URLs
- no debug logs
- no internal reasoning
- no direct Facebook/TikTok crawling claims
- no hype unless sources justify it

## TTS Handoff

The script must be clean enough to send directly to TTS.

Do not include API keys, voice IDs, file paths, provider logs, or runtime details.
