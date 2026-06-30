# Report History

Use this reference when generating a Morning Report or troubleshooting a previous run.

## Runtime

After each generated Morning Report, record the run with:

```bash
python3 skills/morning-report/scripts/record_report.py   --report-file /tmp/morning-report.md   --audio-status "<not_requested|disabled|generated|failed>"   --delivery-status "<prepared|sent|failed|not_recorded>"
```

Add `--source-url` for fetched source URLs and `--failed-url` for failed fetches when available.

If audio was generated, also pass:

```bash
--audio-script-file /tmp/morning-report-audio.txt --audio-file /tmp/morning-report.mp3 --audio-manifest <path-to-audio-manifest.json>
```

## History Layout

Report history is stored under:

```text
skills/morning-report/state/report-history/YYYY-MM-DD/<run-id>/
```

Each run directory may contain:

- `report.md`
- `audio-script.txt`
- `morning-report.mp3`
- `audio-manifest.json`
- `manifest.json`

## Audit Log

`record_report.py` appends a `report_recorded` event to:

```text
skills/morning-report/state/audit.log
```

Configuration helper scripts may also append setup or settings events.

## Status Helper

To inspect the latest report/audio/audit status, run:

```bash
python3 skills/morning-report/scripts/history_status.py --limit 1
```

## Failure Handling

If recording history fails, do not block delivery of the text report. Mention the history recording failure only to the operator, not as part of the customer-facing report.
