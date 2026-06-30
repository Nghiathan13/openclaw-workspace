# Cron Setup

Use Docker Compose for OpenClaw cron commands in this VPS setup.

Default command prefix:

```bash
docker compose -f /home/ubuntu/openclaw/docker-compose.yml run --rm openclaw-cli
```

If the compose file path or CLI service name differs in the current runtime, use the actual configured value. Do not guess.

## Known Cron Commands

The operator reported these OpenClaw cron commands:

| Command | Purpose |
|---|---|
| `status` | Scheduler status |
| `list` | List jobs |
| `get` | Show one job as JSON |
| `show` | Show one job in formatted output |
| `add` | Add a new job |
| `edit` | Edit job fields through options |
| `disable` | Pause a job |
| `enable` | Re-enable a job |
| `rm` | Remove a job |
| `run` | Run a job immediately for debugging |
| `runs` | Show run history |

There is no standalone `wake` command. Wake is an `edit` option:

```bash
docker compose -f /home/ubuntu/openclaw/docker-compose.yml run --rm openclaw-cli cron edit <job-id> --wake now
docker compose -f /home/ubuntu/openclaw/docker-compose.yml run --rm openclaw-cli cron edit <job-id> --wake next-heartbeat
```

Do not use unknown command names such as `create`, `update`, `remove`, `pause`, or `delete`.

## Edit Options

The operator reported that `cron edit` supports these options:

- `--name`, `--cron`, `--tz`, `--every`, `--at`
- `--disable`, `--enable`, `--wake`
- `--model`, `--message`, `--system-event`
- `--channel`, `--to`, `--announce`, `--webhook`
- `--session`, `--session-key`
- `--tools`, `--thinking`, `--light-context`
- `--timeout-seconds`
- `--failure-alert` with sub-options
- `--delete-after-run`, `--keep-after-run`

Use `cron edit` for schedule patches when the target job is already verified.

## Inspect

Before adding, changing, disabling, enabling, removing, or resuming a schedule:

```bash
docker compose -f /home/ubuntu/openclaw/docker-compose.yml run --rm openclaw-cli cron status
docker compose -f /home/ubuntu/openclaw/docker-compose.yml run --rm openclaw-cli cron list
```

If a `Morning Report` schedule already exists, do not create a duplicate. Preserve/merge by default.

Use `cron get <job-id>` for machine-readable verification and `cron show <job-id>` for human-readable inspection:

```bash
docker compose -f /home/ubuntu/openclaw/docker-compose.yml run --rm openclaw-cli cron get <job-id>
docker compose -f /home/ubuntu/openclaw/docker-compose.yml run --rm openclaw-cli cron show <job-id>
```

## Cron Expression

Convert confirmed delivery time to cron format:

- `07:00` -> `0 7 * * *`
- `07:30` -> `30 7 * * *`

## Add

Use `cron add`, not `cron create`.

Before first use, inspect the current runtime's add syntax if exact flags are not already known:

```bash
docker compose -f /home/ubuntu/openclaw/docker-compose.yml run --rm openclaw-cli cron add --help
```

Required Morning Report values for a new job:

- name: `Morning Report`
- schedule: confirmed cron expression and timezone
- message/workflow points to `skills/morning-report/prompts/run-report.md`
- session: `isolated`
- channel: Telegram
- target: actual Telegram target, not a placeholder

Command shape, only if supported by the current CLI:

```bash
docker compose -f /home/ubuntu/openclaw/docker-compose.yml run --rm openclaw-cli cron add \
  --name "Morning Report" \
  --cron "<cron-expression>" \
  --tz "<timezone>" \
  --message "Read and execute skills/morning-report/prompts/run-report.md. Generate the Morning Report using the confirmed report language and deliver it through Telegram." \
  --session isolated \
  --announce \
  --channel telegram \
  --to "<telegram-target-id>"
```

Do not guess `<telegram-target-id>`. Use the actual Telegram target from the current OpenClaw runtime/session.

## Edit Or Reschedule

If a `Morning Report` job already exists and the delivery time, timezone, workflow message, channel, model, or session settings must change:

1. Inspect the job with `cron get <job-id>`.
2. Verify it is the `Morning Report` job and points to `skills/morning-report/prompts/run-report.md`.
3. Patch only the required fields with `cron edit <job-id> ...`.
4. Verify the edited job with `cron get <job-id>` or `cron show <job-id>`.

Example command shape:

```bash
docker compose -f /home/ubuntu/openclaw/docker-compose.yml run --rm openclaw-cli cron edit <job-id> \
  --cron "<cron-expression>" \
  --tz "<timezone>"
```

Do not remove and re-add a schedule when `cron edit` can safely patch it.

## Disable Or Enable

Use `cron disable <job-id>` to pause a verified job. Use `cron enable <job-id>` to re-enable it.

Equivalent edit options may also exist, but prefer the dedicated commands when available:

```bash
docker compose -f /home/ubuntu/openclaw/docker-compose.yml run --rm openclaw-cli cron disable <job-id>
docker compose -f /home/ubuntu/openclaw/docker-compose.yml run --rm openclaw-cli cron enable <job-id>
```

Before disabling or enabling:

- verify the job with `cron get <job-id>`
- verify it is the `Morning Report` job
- verify the workflow points to `skills/morning-report/prompts/run-report.md`
- preserve saved topics and preferences in `skills/morning-report/state/current-topics.md`

## Remove

Use `cron rm <job-id>` only after the user/operator clearly confirms permanent removal, replacement cleanup, or a reset.

Do not use `rm` for ordinary topic changes or temporary pause/disable when `cron disable` is available.

Before removing:

- verify the job with `cron get <job-id>`
- verify it is the `Morning Report` job
- verify the workflow points to `skills/morning-report/prompts/run-report.md`
- preserve saved topics and preferences in `skills/morning-report/state/current-topics.md`

## Verify

After adding, editing, disabling, enabling, removing, or replacing a schedule:

```bash
docker compose -f /home/ubuntu/openclaw/docker-compose.yml run --rm openclaw-cli cron list
docker compose -f /home/ubuntu/openclaw/docker-compose.yml run --rm openclaw-cli cron get <job-id>
docker compose -f /home/ubuntu/openclaw/docker-compose.yml run --rm openclaw-cli cron runs --id <job-id>
```

For active schedules, treat cron setup as successful only after verification shows:

- job name: `Morning Report`
- confirmed cron expression
- confirmed timezone
- `isolated` session mode
- workflow/message points to `skills/morning-report/prompts/run-report.md`
- Telegram delivery is enabled
- Telegram target is real, not a placeholder
- job is enabled

For disabled schedules, treat pause/disable as successful only after verification shows the `Morning Report` job exists and is disabled.

For removed schedules, treat removal as successful only after verification shows the old job is no longer listed or no longer retrievable as an active job.

## Pause, Disable, Or Resume

For pause/disable:

1. Confirm the user's intent.
2. Inspect scheduler state.
3. Verify the target job is exactly `Morning Report`.
4. Disable the cron job with `cron disable <job-id>`.
5. Verify the job is disabled.
6. Set Morning Report lifecycle status to `paused` or `disabled` with `scripts/update_config.py set-status`.

If `cron disable` is unavailable or cannot be verified:

- still set Morning Report lifecycle status to `paused` or `disabled`
- do not claim that the cron job itself was disabled
- the run workflow must stop before report generation while status is `paused` or `disabled`

For resume/re-enable:

1. Inspect scheduler state.
2. If the existing `Morning Report` job exists, enable it with `cron enable <job-id>`.
3. If no valid job exists, add a new `Morning Report` job using the saved delivery time/timezone and verified Telegram target.
4. Verify the active schedule with `cron list` and `cron get <job-id>`.
5. Set lifecycle status back to `configured` only after scheduler verification succeeds.

For temporary pause with automatic resume, use only verified runtime support. The reported `wake` capability is an `edit` option, not a standalone command.
