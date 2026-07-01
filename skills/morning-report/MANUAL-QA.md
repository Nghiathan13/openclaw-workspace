# Manual QA Checklist

Run this checklist after major Morning Report prompt or script changes. Pair it with:

```bash
python3 -m unittest discover skills/morning-report/tests
python3 skills/morning-report/scripts/preflight.py --compact
```

## Router And Status

- [ ] Ask what topics Morning Report is tracking. The agent routes to `prompts/status.md`.
- [ ] The response lists active topics, delivery time, timezone, style, report language, audio preference, and delivery channel.
- [ ] The agent does not edit files or scheduler state for a status-only request.
- [ ] Unknown cron, Telegram, TTS, or fallback status is stated as unknown or not verified.

## Setup

- [ ] Start from `Status: not_configured` in `state/current-topics.md`.
- [ ] `scripts/preflight.py --compact` reports runtime readiness without changing report configuration.
- [ ] Ask the agent to set up Morning Report. It asks only for missing required values.
- [ ] The setup question uses the user's language.
- [ ] Before saving, the agent summarizes the full resulting configuration: topics, delivery time, timezone, style, language, audio, and Telegram.
- [ ] If the user sends another configuration change instead of confirming, the agent merges the change and asks for confirmation again.
- [ ] After clear confirmation, the agent saves via `scripts/update_config.py`, syncs `USER.md`, then verifies with `scripts/config_status.py --check`.
- [ ] The agent claims Morning Report is enabled only after cron/scheduler is configured and verified.

## Topic And Settings Updates

- [ ] Replacing topics requires confirmation and shows `current -> requested`.
- [ ] The confirmation lists all resulting settings; it does not say only "other settings stay the same."
- [ ] Adding or removing a topic uses `scripts/update_config.py ... --sync-user`.
- [ ] Removing the final active topic is blocked; the agent asks whether to replace it or disable Morning Report explicitly.
- [ ] If the user changes delivery time or timezone, the agent routes to `prompts/update-settings.md`.
- [ ] Time or timezone changes update and verify cron before the agent says the schedule is enabled.
- [ ] Internal fallback model/provider details are not mentioned to the customer.

## Pause, Disable, And Resume

- [ ] Disable Morning Report after confirmation. Topics and preferences remain saved.
- [ ] If cron disable cannot be verified, the agent says scheduler status is not verified.
- [ ] While status is `disabled` or `paused`, manual/scheduled report runs stop before search or generation.
- [ ] Resume/re-enable only after `cron enable` or `cron add` is verified active.
- [ ] After resume, status returns to `configured` and `USER.md` status returns to `enabled`.

## Manual Report Run

- [ ] A manual run starts with `scripts/config_status.py --check`.
- [ ] If required config is missing, the agent stops before search or report generation.
- [ ] A scheduled/cron run sends no progress or acknowledgement messages before the final report.
- [ ] A manual test run sends at most one short acknowledgement before work begins.
- [ ] The agent does not send phase updates such as search progress, composing, audio success, history recording, or delivery status.
- [ ] The report uses only configured topics, configured language, configured style, and fresh sources from the current run.
- [ ] The final customer-facing Telegram text starts directly with the report title.
- [ ] The agent does not send a second summary or recap after the final report unless the user explicitly asks.
- [ ] After generation, the agent records history with `scripts/record_report.py`.

## Audio

- [ ] If audio is disabled, no audio script or MP3 is generated.
- [ ] If audio is enabled, the agent creates a clean spoken script and runs `scripts/generate_audio.py`.
- [ ] If audio generation succeeds, the final Telegram output includes a standalone `MEDIA:<mp3-path>` line.
- [ ] The Telegram chat receives an attached/playable MP3, not just a text path.
- [ ] Text report delivery still happens if audio generation fails.
- [ ] Audio success or failure is reflected in report history.
- [ ] The full audio script is not included in the customer-facing text report unless explicitly requested.

## Artifacts

- [ ] `state/audit.log` gains an event after setup, topic updates, settings updates, or report recording.
- [ ] `state/report-history/` stores the report and manifest for completed or prepared runs.
- [ ] `state/audio-history/` stores audio chunks, MP3, and manifest only when audio generation runs.
- [ ] Runtime artifacts remain ignored by git.
