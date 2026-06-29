# Morning Report Setup

This file is a one-time setup wizard for the Morning Report + Audio use case.

Read and follow this file only when the operator explicitly asks you to read `morning-report-audio/setup.md`.

Do not use this file to generate a daily report. Daily report generation is handled by `morning-report-audio/00-run.md`.

## Goal

Set up the user to receive a Morning Report through Telegram.

After setup is complete, the workspace must have enough configuration to:

- Follow the topics confirmed by the user
- Send the report in the morning at the confirmed delivery time
- Use Telegram as the delivery channel
- Generate an audio summary according to the current workflow and available TTS runtime

Do not ask the user to edit files or code.

## Before Asking The User

Read the existing context before asking setup questions:

- `USER.md`
- `IDENTITY.md`
- `SOUL.md`
- `morning-report-audio/topics/current-topics.md`

Use only information that is already present in those files or information the user has provided in the current conversation.

Do not assume:

- topics to follow
- delivery time
- timezone if it is not already known
- report style
- audio preference
- cron/scheduler status
- TTS availability

If `morning-report-audio/topics/current-topics.md` contains `Status: not_configured`, do not run the report. Complete setup first.

## Required Setup Information

Before enabling the report, make sure the following information is known:

1. Daily topics to follow
2. Morning delivery time
3. Timezone
4. Report style
5. Audio summary preference

If any item is already clear from `USER.md` or the current conversation, do not ask for it again. Still include it in the setup summary so the user can confirm it.

If any required item is missing, ask the user in one concise message. Use the same language the user is using.

Vietnamese template:

```text
Để thiết lập Morning Report, tôi cần xác nhận vài thông tin:

1. Chủ đề bạn muốn theo dõi hằng ngày là gì?
2. Bạn muốn nhận report lúc mấy giờ mỗi sáng?
3. Timezone cần dùng là gì?
4. Bạn muốn report theo phong cách nào: ngắn gọn, phân tích sâu, hay tập trung cơ hội/rủi ro?
5. Bạn có muốn nhận bản audio summary nếu hệ thống tạo audio khả dụng không?
```

Do not ask extra setup questions in the same message unless the user's previous answer was unclear.

## After The User Answers

Do not update files or configure the scheduler immediately.

First, summarize the setup you understood and ask for confirmation.

Vietnamese template:

```text
Tôi hiểu cấu hình Morning Report như sau:

- Topic theo dõi:
- Giờ gửi:
- Timezone:
- Phong cách report:
- Audio summary:
- Kênh gửi: Telegram

Bạn xác nhận cấu hình này đúng chưa? Sau khi bạn xác nhận, tôi sẽ lưu cấu hình và thiết lập lịch gửi hằng ngày nếu runtime hiện tại hỗ trợ scheduler/cron.
```

Continue only after the user clearly confirms.

## Files To Update After Confirmation

After the user confirms, update the files below. Preserve unrelated content and do not remove other information.

### 1. `morning-report-audio/topics/current-topics.md`

Update this file from `not_configured` to the confirmed setup.

Use this structure:

```md
# Current Topics

## Setup status

Status: configured

## Active topics

1. ...

## Optional topics

Only add optional topics if the user explicitly provided secondary or optional topics.
If the user did not provide optional topics, write: `None provided.`

## User priority

List the highest-priority topics first.
Use only topics the user provided or confirmed.

## Report preferences

- Delivery time:
- Timezone:
- Report style:
- Audio summary:
- Delivery channel: Telegram
```

Do not add sample topics. Do not add optional topics unless the user explicitly provided them.

### 2. `USER.md`

Add or update this section:

```md
## Morning Report Preferences

- Status:
- Topics:
- Delivery time:
- Timezone:
- Report style:
- Audio summary:
- Delivery channel: Telegram
```

Set `Status` to `enabled` only after scheduler/cron setup succeeds.

If preferences are saved but scheduler/cron setup is not complete, set `Status: preferences_saved_schedule_pending`.

## Scheduler/Cron Setup

Morning Report requires a reliable daily delivery time, so prefer scheduled task/cron over heartbeat.

Before changing scheduler configuration, inspect the existing state and preserve/merge by default, following `AGENTS.md`.

### OpenClaw Cron Template

Use this template only if the current runtime provides the OpenClaw cron CLI or an equivalent scheduled task capability.

Before creating a new schedule, inspect existing schedules:

```bash
openclaw cron list
```

If a Morning Report schedule already exists, do not create a duplicate. Preserve/merge the existing schedule by default. Only replace or update it when the user/operator has clearly confirmed the change and the runtime provides the required command.

Cron expression rule:

- Convert the confirmed delivery time to standard cron format: `<minute> <hour> * * *`
- Example: `07:00` becomes `0 7 * * *`
- Example: `07:30` becomes `30 7 * * *`

Command shape:

```bash
openclaw cron create "<cron-expression>" \
  "Read and execute morning-report-audio/00-run.md. Generate the Morning Report in Vietnamese and deliver it through Telegram." \
  --name "Morning Report" \
  --tz "<timezone>" \
  --session isolated \
  --announce \
  --channel telegram \
  --to "<telegram-target-id>"
```

Example for `07:00` with `Asia/Ho_Chi_Minh` timezone:

```bash
openclaw cron create "0 7 * * *" \
  "Read and execute morning-report-audio/00-run.md. Generate the Morning Report in Vietnamese and deliver it through Telegram." \
  --name "Morning Report" \
  --tz "Asia/Ho_Chi_Minh" \
  --session isolated \
  --announce \
  --channel telegram \
  --to "<telegram-target-id>"
```

Do not guess `<telegram-target-id>`. Use only the actual Telegram target from the current OpenClaw runtime/session. If the target cannot be determined, stop and explain what is missing.

After creating the schedule, verify it:

```bash
openclaw cron list
openclaw cron get <job-id>
openclaw cron runs --id <job-id>
```

Only treat scheduler setup as successful after verification shows the Morning Report schedule exists with the confirmed time, timezone, isolated session, Telegram delivery, and the correct workflow instruction.

If the current runtime provides a tool to create a scheduled task/cron:

- Create a daily schedule using the delivery time and timezone confirmed by the user
- The schedule must run the workflow in `morning-report-audio/00-run.md`
- The output must be delivered through Telegram
- Confirm `enabled` only if scheduler/cron configuration succeeds

If the current runtime does not provide scheduler/cron setup capability:

- Still save preferences in `USER.md` and `morning-report-audio/topics/current-topics.md`
- Set `Status: preferences_saved_schedule_pending` in `USER.md`
- Tell the user that preferences were saved but automatic scheduling has not been enabled yet
- Do not delete this setup file

Do not claim scheduler/cron is enabled unless it was actually configured successfully.

## Audio Setup

Only confirm audio summary availability if the runtime/TTS tool is actually available.

If TTS is not available:

- Save the user's audio preference
- Do not say that an audio file will definitely be sent
- Say that audio will be used when audio generation is available

Do not claim ElevenLabs, TTS, voice ID, or audio delivery is ready unless there is evidence from the current runtime/configuration.

## Completion Rules

Consider setup complete only when all of the following are true:

- The user confirmed the setup
- `morning-report-audio/topics/current-topics.md` was updated
- `USER.md` was updated
- Scheduler/cron was configured successfully
- The user received final confirmation that Morning Report is enabled

After and only after all completion requirements are met, delete this file:

`morning-report-audio/setup.md`

If any step is incomplete, keep this file so setup can continue later.

## Final Confirmation

Send this final confirmation only when setup is actually complete, including scheduler/cron:

```text
Đã xong. Morning Report đã được bật.

Tôi sẽ theo dõi các topic bạn đã chọn và gửi report mỗi sáng qua Telegram theo giờ đã cấu hình.

Nếu audio generation khả dụng, tôi cũng sẽ gửi kèm bản audio summary theo cấu hình đã xác nhận.

Bạn có thể đổi topic bất kỳ lúc nào bằng cách nhắn tự nhiên, ví dụ:
"Đổi topic Morning Report sang crypto và thị trường tài chính."
```

If preferences were saved but scheduler/cron was not enabled, do not use the final confirmation above. Clearly state what is still missing instead.

## Safety Rules

- Do not assume missing information.
- Do not invent topics, delivery time, timezone, cron status, TTS status, or audio capability.
- Do not run the daily report while `current-topics.md` still contains `Status: not_configured`.
- Do not edit `00-run.md` or other workflow rule files during setup unless the operator explicitly asks.
- Do not delete this file until setup fully satisfies the Completion Rules.
- Do not ask the user to touch code, files, VPS, or Docker.
