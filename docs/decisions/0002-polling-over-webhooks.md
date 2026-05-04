# ADR 0002: Polling over webhooks

## Status

Accepted.

## Context

Meta provides a [Webhooks for Pages](https://developers.facebook.com/docs/graph-api/webhooks) capability. In principle, a webhook-driven system would be lower-latency, lower-quota, and more elegant than polling.

## Decision

We use polling.

## Consequences

- Slightly higher API quota usage.
- Slightly higher reply latency (bounded by the poll interval).
- No webhook receiver endpoint to expose, harden, and operate.
- No need to manage webhook subscription state, verification challenges, or HMAC signature validation under load.

## Rationale

Three reasons.

**First, the poll interval is a feature.** It naturally absorbs comment bursts. A webhook firehose during a viral post would overwhelm our throttler before it could intervene; the poll loop pulls work at our pace, not Meta's.

**Second, our latency budget is generous.** A comment that gets a reply within two to ten minutes is indistinguishable, to a human reader, from one that gets a reply within ten seconds. We are not building a real-time chat product. We are building a steady, persistent presence.

**Third, polling is simpler.** A webhook endpoint is a public attack surface. It must be authenticated, rate-limited, validated, and operated under stricter security posture than an outbound-only client. The simplicity of polling is itself the argument.

## Alternatives considered

- **Webhooks only.** Rejected for the reasons above.
- **Hybrid: webhooks for low-latency, polling for backfill.** Considered. Rejected as premature optimisation. Will be revisited if the source Page sees comment volumes that exceed what the polling cadence can drain in real time.

## Notes

The poll interval, jitter, and per-post comment-fetch depth are tuned values and are not in this repository.
