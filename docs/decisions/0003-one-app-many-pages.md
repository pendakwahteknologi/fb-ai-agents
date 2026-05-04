# ADR 0003: One Meta App, many Pages

## Status

Accepted.

## Context

The system involves four persona Pages and one principal Page. A natural design instinct is to register a separate Meta App per persona, on the theory that App-level rate limits or App-level reputation might benefit from isolation.

## Decision

We use a single Meta App for all five Pages.

## Consequences

- All Pages share the same App-level rate budget.
- All Pages share the same App-level reputation. A reputational hit on one Page propagates to the App.
- Token issuance, permission management, and developer-side configuration is centralised.
- Operationally far simpler.

## Rationale

App-level rate limits, in our measured experience, are not the binding constraint. Per-Page rate limits and per-Page anti-spam classification dominate. Multiple Apps would not help.

App-level reputation is real but weak. Per-Page behaviour is what determines whether a Page is throttled, hidden, or blocked. We invest in per-Page hygiene rather than App diversification.

A single App means a single set of secrets, a single review surface (if we ever pursue App Review for additional permissions), and a single OAuth flow for token issuance. The simplicity is worth the lack of isolation.

## Alternatives considered

- **One App per persona.** Rejected. Operationally complex. No measured benefit.
- **Two Apps, separating principal Page from persona Pages.** Considered. Rejected as a premature isolation that would not actually isolate the failure modes we worry about.

## Notes

If we ever pursue App Review (for example, to obtain Reactions API access at scale), we will revisit this decision. Today, we do not need it.
