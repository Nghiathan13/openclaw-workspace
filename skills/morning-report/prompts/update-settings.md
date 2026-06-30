# Morning Report Settings Updates

Use this prompt when the user wants to change Morning Report delivery time, timezone, report style, report language, audio summary preference, delivery channel, lifecycle status, or multiple Morning Report configuration fields in one conversation.

Also use this prompt when the user adds a settings change while another Morning Report configuration change is still pending confirmation.

## Read First

Run:

```bash
python3 skills/morning-report/scripts/config_status.py
```

Use the JSON output as the source of truth for saved configuration. Use conversation history only for unconfirmed pending changes.

Read:

- `skills/morning-report/references/policy.md`
- `skills/morning-report/references/cron.md` if delivery time, timezone, pause, disable, or resume may change scheduler state

If required setup is missing, ask the user/operator to complete setup first.

## Supported Intents

- Change delivery time
- Change timezone
- Change report style
- Change report language
- Enable or disable audio summary
- Pause, disable, resume, or re-enable Morning Report delivery
- Change multiple Morning Report settings together
- Merge a new settings request with a pending topic/settings change

## Rules

- Do not invent missing values.
- Preserve saved values unless the user explicitly changes them.
- A new configuration request is not confirmation for a previous pending change.
- If a change is pending and the user sends another configuration change, merge the requested changes and ask for confirmation again.
- Do not update files, cron, scheduler, or runtime settings until the user clearly confirms the latest full summary.
- Do not mention internal model/provider fallback details.
- Do not remove saved topics or preferences when pausing or disabling Morning Report.
- Treat pause/disable/resume as scheduler lifecycle changes. Inspect scheduler state before changing it, and verify any scheduler change before claiming it succeeded.
- If a temporary pause is requested, ask for the exact resume date/time/timezone unless it is already explicit. Only claim automatic resume if a verified scheduler/cron mechanism exists for it.

## Confirmation Before Edit

Before changing files, cron, or scheduler, summarize the full resulting configuration:

- Topics
- Delivery time
- Timezone
- Report style
- Report language
- Audio summary
- Delivery channel
- Morning Report status when lifecycle status changes

For every changed field, show `current -> requested`. For every unchanged field, show the resulting value. Do not use vague phrases like "other settings stay the same."

Ask the user to confirm whether to apply the full configuration.

## Save After Confirmation

For lifecycle changes only, use `skills/morning-report/scripts/update_config.py set-status` after confirmation. Preserve topics and preferences.

Command patterns:

```bash
python3 skills/morning-report/scripts/update_config.py set-status --status disabled --sync-user
python3 skills/morning-report/scripts/update_config.py set-status --status paused --sync-user
python3 skills/morning-report/scripts/update_config.py set-status --status configured --sync-user
```

Use `disabled` when the user wants Morning Report turned off indefinitely. Use `paused` when the user wants a temporary or explicit pause. Use `configured` only when resuming/re-enabling and the required configuration plus scheduler state are verified.

For delivery preference changes, save the full resulting configuration with `skills/morning-report/scripts/update_config.py setup`. Include current saved values for fields that were not changed.

Command shape:

```bash
python3 skills/morning-report/scripts/update_config.py setup \
  --topic "<resulting-active-topic>" \
  --delivery-time "<resulting-delivery-time>" \
  --timezone "<resulting-timezone>" \
  --report-style "<resulting-report-style>" \
  --report-language "<resulting-report-language>" \
  --audio-summary "<resulting-audio-summary>" \
  --delivery-channel "Telegram" \
  --user-status "preferences_saved_schedule_pending"
```

Repeat `--topic` for every resulting active topic. Use `--optional-topic` only for optional topics explicitly provided by the user.

Choose `--user-status` carefully:

- Use `enabled` when the existing schedule remains valid.
- Use `disabled` when Morning Report is intentionally turned off.
- Use `paused` when Morning Report is intentionally paused.
- Use `preferences_saved_schedule_pending` only while a required cron/scheduler change has not been verified.
- If delivery time or timezone changed, save preferences as pending if needed, edit the schedule with `cron edit` using `skills/morning-report/references/cron.md`, verify it, then save the same resulting configuration again with `--user-status "enabled"`.

For pause/disable:

- Inspect scheduler state using `skills/morning-report/references/cron.md`.
- If the user confirms pause/disable and the `Morning Report` job is verified, disable the job with `cron disable <job-id>`.
- If scheduler disable is unavailable or cannot be verified, still set lifecycle status to `paused` or `disabled`; the run workflow will stop before report generation. Do not claim the cron job itself was disabled unless verified.
- Do not use `cron rm` for ordinary pause/disable when `cron disable` is available.

For resume/re-enable:

- If a valid disabled Morning Report job exists, enable it with `cron enable <job-id>`.
- If no valid job exists, add a new Morning Report job using `skills/morning-report/references/cron.md`.
- Set status to `configured` only after scheduler verification succeeds.

After saving and any required cron add/edit/disable/enable/rm operation, run:

```bash
python3 skills/morning-report/scripts/config_status.py
```

Use `--check` only when the expected final status is runnable/configured. For `paused` or `disabled`, `--check` is expected to fail because reports should not run.

If the check fails unexpectedly or cron verification fails, explain what is still missing instead of claiming the update is complete.

## Final Response

After the confirmed update is saved and verified, tell the user:

- the configuration was updated
- the full resulting configuration
- whether cron/schedule was updated and verified, or not verified
- when the change will apply

Do not mention internal model/provider fallback details.
