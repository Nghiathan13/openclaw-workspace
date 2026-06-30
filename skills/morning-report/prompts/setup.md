# Morning Report Setup

Use this prompt for one-time setup of the Morning Report workflow.

Use `skills/morning-report/prompts/update-settings.md` for later changes to delivery time, timezone, report style, report language, audio preference, or multiple configuration fields.

Do not use this prompt to generate the daily report. Daily report generation is handled by `skills/morning-report/prompts/run-report.md`.

## Read First

- `USER.md`
- `IDENTITY.md`
- `SOUL.md`
- `skills/morning-report/state/current-topics.md`
- `skills/morning-report/references/policy.md`
- `skills/morning-report/references/cron.md`

Run before asking setup questions:

```bash
python3 skills/morning-report/scripts/config_status.py
```

Use existing values from the helper output when they are already clear.

## Collect

Collect and confirm these values:

1. Daily topics to follow
2. Morning delivery time
3. Timezone
4. Report style
5. Report language
6. Audio summary preference

Ask only for missing values. Use the user's language. Do not ask the customer to edit files, code, Docker, or VPS settings.

## Confirm Before Changes

Before changing files or cron, summarize the full resulting configuration:

- Topics
- Delivery time
- Timezone
- Report style
- Report language
- Audio summary
- Delivery channel: Telegram

For changed fields, show `current -> requested` when there is an existing saved value. For unchanged fields, still show the resulting value. Do not use vague phrases like "other settings stay the same."

If the user sends another configuration change instead of confirming, merge it into the pending setup summary and ask for confirmation again. A new configuration request is not confirmation.

Continue only after the user clearly confirms the latest full summary.

## Save After Confirmation

After confirmation, save the confirmed setup with the helper script. Example command shape:

```bash
python3 skills/morning-report/scripts/update_config.py setup \
  --topic "<topic>" \
  --delivery-time "<delivery-time>" \
  --timezone "<timezone>" \
  --report-style "<report-style>" \
  --report-language "<report-language>" \
  --audio-summary "<audio-summary>" \
  --delivery-channel "Telegram" \
  --user-status "preferences_saved_schedule_pending"
```

Repeat `--topic` for multiple active topics. Use `--optional-topic` only for optional topics explicitly provided by the user.

Do not manually rewrite `skills/morning-report/state/current-topics.md` or `USER.md` unless the helper is unavailable. Preserve unrelated content.

Set `--user-status enabled` only after cron is configured and verified. If preferences are saved but cron is not enabled, keep `preferences_saved_schedule_pending`.

## Schedule

Configure or update cron using `skills/morning-report/references/cron.md`.

If the runtime supports model/provider fallback, preserve or configure fallback internally using `skills/morning-report/references/policy.md`.

Do not mention fallback model/provider details to the customer unless the operator explicitly asks.

## Completion

Setup is complete only when:

- the user confirmed the setup
- `python3 skills/morning-report/scripts/config_status.py --check` succeeds
- `USER.md` was updated through the helper
- cron was configured and verified
- the user received final confirmation

Do not delete reusable skill prompts.

## Final Confirmation

Send final confirmation only when setup is complete. Adapt to the user's language:

```text
Done. Morning Report is enabled.

- Topics:
- Delivery time:
- Timezone:
- Report style:
- Report language:
- Audio summary:
- Delivery channel: Telegram

The Morning Report schedule has been configured and verified.
The first report will be sent at the next scheduled run.

You can change the topics anytime by messaging me naturally.
```

If preferences were saved but cron was not enabled, do not use the final confirmation above. Clearly state what is still missing.
