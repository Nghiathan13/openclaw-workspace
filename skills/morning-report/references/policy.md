# Morning Report Policy

Use these rules for setup and daily report runs.

## Do Not Assume

Do not invent or guess:

- topics
- delivery time
- timezone
- report style
- report language
- audio preference
- Telegram target
- cron status
- TTS availability
- fallback model/provider status

## Setup Safety

- Do not run the report while `current-topics.md` contains `Status: not_configured`.
- Do not ask the user to edit code, files, VPS, or Docker.
- Do not claim cron is enabled unless it was configured and verified.
- Do not claim audio is available unless TTS is available.
- Do not delete reusable skill prompts. Update runtime state through helper scripts after confirmed setup.

## Customer Confirmation

Before saving any Morning Report setup or configuration change, show the full resulting configuration:

- Topics
- Delivery time
- Timezone
- Report style
- Report language
- Audio summary
- Delivery channel

For changed fields, show `current -> requested`. For unchanged fields, still show the resulting value. Do not replace unchanged fields with vague phrases like "other settings stay the same."

If there is an unconfirmed pending change and the user sends another configuration change instead of a clear confirmation, do not apply anything yet. Merge the new request into the pending change summary and ask for confirmation again using the full resulting configuration.

A new configuration request is not confirmation. Continue only after the user clearly confirms the latest full summary.

## Runtime Fallback

If runtime model/provider fallback is available, preserve or configure it internally.

- Do not hard-code a provider or model name.
- Prefer an existing working fallback.
- If no fallback exists, choose only from models/providers actually available in the runtime.
- Do not block setup solely because fallback is unavailable.
- Do not mention fallback details to the customer unless the operator asks.

## Language

Use the user's language during setup. Use the configured report language during report generation.

Do not hard-code user name, country, language, or topics.
