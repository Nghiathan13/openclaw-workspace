# Morning Report Topic Updates

Use this prompt when the user wants to view, change, add, remove, replace, reprioritize, or temporarily override Morning Report topics.

## Read First

Run:

```bash
python3 skills/morning-report/scripts/config_status.py
```

Use the JSON output as the source of truth for current topics and report preferences.

If `current-topics.md` contains `Status: not_configured` or the helper reports missing required setup, do not update topics. Ask the user/operator to complete setup first.

## Supported Intents

- View current topics
- Replace active topics
- Add active topic
- Remove active topic
- Add optional topic
- Remove optional topic
- Reprioritize topics
- Clarify a temporary or one-off topic request

## Rules

- Use only topics explicitly provided by the user.
- Do not invent related topics, markets, countries, sources, or keywords.
- Preserve existing report preferences unless the user explicitly asks to change them.
- If the request includes delivery time, timezone, report language, report style, audio preference, delivery channel, cron, scheduler, or multiple configuration fields, stop this prompt and follow `skills/morning-report/prompts/update-settings.md` instead.
- If a topic change is pending and the user sends another configuration change instead of a clear confirmation, merge the pending topic change with the new request through `skills/morning-report/prompts/update-settings.md` and ask for confirmation again.
- Confirm before replacing all topics, removing topics, or reprioritizing topics.
- Do not remove the final active topic. If the requested removal would leave no active topics, ask whether the user wants to replace it with another topic or disable Morning Report explicitly.
- If the request is unclear, ask one short clarification question before editing files.
- If the user asks for a temporary or one-off topic, ask whether it should replace the saved scheduled topics or only be used for a one-time report.

## Confirmation Before Edit

Before editing topics, summarize the full resulting Morning Report configuration:

- Topics
- Delivery time
- Timezone
- Report style
- Report language
- Audio summary
- Delivery channel

For the topic field, show `current -> requested` when topics will change. For unchanged fields, still show the resulting value. Do not use vague phrases like "other settings stay the same."

Ask for confirmation unless the user only asks to view current topics.

## Save After Confirmation

After confirmation, update topics with `skills/morning-report/scripts/update_config.py`.

Command patterns:

```bash
python3 skills/morning-report/scripts/update_config.py replace-topics --topic "<topic>" --sync-user
python3 skills/morning-report/scripts/update_config.py add-topic --topic "<topic>" --sync-user
python3 skills/morning-report/scripts/update_config.py remove-topic --topic "<topic>" --sync-user
python3 skills/morning-report/scripts/update_config.py add-optional-topic --topic "<topic>" --sync-user
python3 skills/morning-report/scripts/update_config.py remove-optional-topic --topic "<topic>" --sync-user
python3 skills/morning-report/scripts/update_config.py reprioritize --topic "<topic>" --sync-user
```

Repeat `--topic` when needed. Use `--sync-user` so `USER.md` stays aligned with runtime state. Do not edit unrelated `USER.md` content.

After saving, run:

```bash
python3 skills/morning-report/scripts/config_status.py --check
```

If the check fails, explain what is missing instead of claiming the update is complete.

## Final Response

After saving a topic update, tell the user:

- the topic change was saved
- the new active topics
- the new optional topics, if any
- the change will apply to the next scheduled Morning Report

Do not mention internal model/provider fallback details.
