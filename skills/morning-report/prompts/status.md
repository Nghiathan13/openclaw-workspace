# Morning Report Status

Use this prompt when the user asks what is configured, what topics are tracked, whether Morning Report is enabled, whether cron exists, or why a report/audio did not run.

## Read First

Run:

```bash
python3 skills/morning-report/scripts/config_status.py
```

Use the JSON output as the source of truth for Morning Report state.

If scheduler details matter, also read:

- `skills/morning-report/references/cron.md`

If report or audio troubleshooting matters, run:

```bash
python3 skills/morning-report/scripts/history_status.py --limit 1
```

Use the helper output instead of manually guessing latest history files.

## Behavior

Report current state only. Do not edit files or scheduler configuration unless the user clearly asks for a change.

Do not assume cron, Telegram target, TTS, audio delivery, or fallback model/provider status. State `unknown` or `not verified` when the information is not present or was not verified in the current runtime.

## Status Checklist

Summarize these fields when available:

- setup/lifecycle status
- active topics
- optional topics
- delivery time
- timezone
- report style
- report language
- audio summary preference
- delivery channel
- user preference status from `USER.md`
- cron/scheduler status, only if inspected or already present in reliable context
- latest report run status, only if inspected from history helper
- latest audio run status, only if inspected from history helper
- latest audit event, only if inspected from history helper

If setup/lifecycle status is `paused` or `disabled`, state that Morning Report will not generate scheduled reports until it is resumed/re-enabled. Do not describe this as incomplete setup.

If `warnings` are present in the helper output, mention them briefly.

## Output

Use the user's language. Keep the answer concise and operational.

If setup is incomplete, point the user to setup:

`skills/morning-report/prompts/setup.md`

If the user wants to change topics, route to:

`skills/morning-report/prompts/update-topics.md`

If the user wants a manual test run, route to:

`skills/morning-report/prompts/run-report.md`
