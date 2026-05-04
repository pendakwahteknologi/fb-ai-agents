# Monitoring

## What we watch

### Per-service

- Liveness (is the process running)
- Readiness (is the process able to accept work)
- Polling loop heartbeat (is ingestion happening)
- Outbound API error rate, by error code

### Per-agent

- Replies issued, by hour
- Reactions issued, by hour
- Refusals, by category
- Classifier confidence distribution
- Page health state (live / throttled / blocked / recovering)
- Cooldown timer remaining
- Shadow-hide rate

### Per-Page

- Cumulative replies in the trailing hour
- Cumulative reactions in the trailing hour
- Cumulative skipped opportunities
- Time since last 368 event
- Time since last successful reply

## Alerts

Alerts are noisy if poorly tuned. Ours are tuned to fire only on conditions that require human action within an hour.

- Any Page enters `blocked` state.
- Classifier confidence drops below threshold for a sustained window.
- Outbound 4xx error rate exceeds threshold for a sustained window.
- Polling heartbeat misses more than two intervals.
- Shadow-hide rate exceeds threshold for any agent.
- Disk usage on the host exceeds threshold.

Alerts that have fired in the last quarter are reviewed monthly. False positives are tuned away. Real positives become test cases.

## Dashboards

There is a single operational dashboard. It shows, at a glance:

- per-agent reply count for the day
- per-Page health state and cooldown remaining
- outbound error counts by code
- the last twenty activity-log entries

If you cannot understand the system's state from this dashboard within thirty seconds, the dashboard is broken. We do not add fields to feel comprehensive; we add fields when an incident showed us a missing signal.

## Logs

- Every reply is logged with: timestamp, comment ID, classifier output, routing decision, agent ID, latency, success or failure, and (if failure) error code.
- Every refusal is logged with: timestamp, comment ID, refusal category.
- Every error is logged with: timestamp, error code, context, and a redacted token if relevant.
- All logs auto-redact tokens at write time.

Logs are retained for thirty days online and ninety days in cold storage. Beyond ninety days, only aggregate counters are retained.

## What is intentionally absent from this document

The exact thresholds, the alerting tool, and the dashboard implementation are operator-specific and not published. The principles are universal; the values are not.
