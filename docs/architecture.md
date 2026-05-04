# Architecture

This document describes the system in prose. It is intentionally implementation-light. It will tell you **what** every component does and **why** it exists. It will not tell you **how** we made it work in production. That is the proprietary layer.

## System overview

The system is a long-running service that observes a single source Facebook Page (the **principal Page**), classifies incoming public comments, routes each comment to the appropriate persona agent, generates a reply in that persona's voice, and posts the reply via that persona's own Facebook Page identity. It maintains health state for each persona Page, throttles aggressively against Meta's anti-spam systems, and recovers gracefully when blocks occur.

It is not a chatbot. There is no user-facing input field. The "users" are members of the public commenting on the principal Page; they never know they are interacting with a coordinated multi-agent system unless we choose to tell them.

## Components

### Ingestion loop

Polls the principal Page on a randomised interval. For each post within a configurable horizon, fetches comments and replies. Deduplicates against the processed-state store. Constructs a work queue ordered by priority.

Polling cadence, horizon depth, and prioritisation weights are tuned values. They are not in this repository.

### Classifier

A language-model-driven categorisation step. Each new comment is classified into one of several categories: general inquiry, abusive content, dismissive trolling, unsupported assertion, help-seeking, refuse-and-deflect, or no-action. The classifier also extracts mention targets, language, and a confidence score.

The classifier is the first defence against prompt injection. Comments are treated as data, not instructions. The system prompt that achieves this robustness is not published.

### Router

Maps a classified comment to a specific persona agent. Routing is not a one-to-one mapping from category to agent. It depends on:

- whether the comment names a specific agent
- the health status of each persona Page (live, throttled, blocked, recovering)
- whether the comment sits in a thread an agent has already engaged
- whether the comment is on the principal Page's most recent post
- a configurable priority matrix

When the preferred agent's Page is in cooldown, the router may select a fallback path. The fallback path preserves persona attribution while continuing engagement. The mechanism is not described here.

### Persona reply engine

For each routed comment, the engine assembles a context window containing the comment text, the parent post, any preceding thread, and the persona's rule-set. The rule-set defines voice, tone, allowed topics, refusal categories, length constraints, formatting constraints, and identity-opacity rules. The reply is generated, validated, and either accepted or rejected.

The rule-sets are the brand. They are not published.

### Throttler

Enforces human-pace timing. Replies and reactions are paced with randomised jitter inside calibrated bands. Per-Page hourly caps are enforced. A skip rate introduces natural variance — not every commentable comment is commented on. When error 368 or related anti-spam responses are observed, the affected Page is moved to a degraded state and a recovery timer is started.

The exact bands, caps, skip rates, and backoff curves are tuned values. They are not in this repository.

### Poster

Issues the actual Graph API call to publish a reply, post a reaction, or take any other state-changing action on Facebook. The Poster uses the persona Page's own access token, ensuring the published artefact appears under that persona's identity. It is the only component that holds write tokens. It enforces rate limits at the call site as a last line of defence.

### Verification layer

After a successful publish, a separate pass verifies the reply is actually visible. Meta occasionally shadow-hides bot replies without notification. The verification layer detects this and applies remediation. The remediation method is not described here.

### State store

All persistent state is kept in atomic JSON files in a local data directory. Atomic write (temp file plus rename) is mandatory; we have lost data to non-atomic writes and will not lose it again. Persisted state includes:

- processed comment IDs (capped, with recency eviction)
- threads where any agent has previously replied
- per-Page health and cooldown timers
- baseline snapshots used by certain modes

The state store is intentionally simple. There is no database. Boring infrastructure is a feature.

### Observability

The service exposes health, readiness, and metrics endpoints. An activity endpoint provides a recent log for human review. Per-agent counters track replies, refusals, errors, and rate-limit events. The logger redacts access tokens at write time; we do not rely on operators to keep tokens out of logs.

## Data flow, end to end

1. The ingestion loop wakes, polls the principal Page, and discovers a new comment.
2. The comment is deduplicated against the state store. If new, it enters the work queue.
3. The classifier categorises the comment and returns a routing hint.
4. The router selects a persona agent, considering health, priority, and fallback rules.
5. The persona reply engine generates a candidate reply using the agent's rule-set.
6. The throttler waits the appropriate jittered interval.
7. The Poster publishes the reply via the persona's Page token.
8. The verification layer confirms visibility.
9. The state store records the comment as processed and the thread as engaged.
10. Metrics are updated. The loop continues.

## Failure modes and how the system handles them

**Anti-spam block (error 368)** — The Page is marked blocked with a 24-hour TTL. The router excludes it. Where appropriate, a fallback path continues engagement under different attribution. After TTL expiry, the Page is probationally returned to service with reduced caps.

**Token expiry** — Tokens obtained via the long-lived flow do not expire under normal conditions, but they can be invalidated. The system detects the failure mode and surfaces an alert. There is no auto-renewal; renewal is a deliberate human operation.

**Rate limit (error 4 / 17 / 32)** — The throttler observes the response, increases its backoff, and reduces caps for the remainder of the hour.

**Shadow-hide** — Detected by the verification layer. Remediation is applied. If it fails, the agent backs off and surfaces an alert.

**Prompt injection in a comment** — The classifier rejects the comment to a refuse-and-deflect category. The persona reply engine's rule-set provides a second layer of defence. We have not yet observed an injection that survived both layers.

**Crash mid-write** — Atomic writes ensure the state file on disk is always either the previous version or the new version, never partial. On restart, the service replays from the last-known-good state.

**Network partition** — The polling loop tolerates failure. Queued work is preserved. No external state is lost because all state is local.

## What is intentionally absent from this document

- The classifier's prompt
- The persona rule-sets
- The throttling constants
- The dismissive-troll detection patterns
- The fallback attribution mechanism
- The shadow-hide remediation procedure
- The prompt-injection defence specifics

These are the moat. The architecture is open. The intelligence layer is not.
