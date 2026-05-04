# Production report

This document summarises observed system behaviour during the first production weeks. Numbers are rounded and reported in ranges rather than exact values. The intent is to convey order of magnitude, not to publish a tuning sheet.

## Operating window

- Source Page: Pendakwah Teknologi
- Active personas: Adila, Hakimah
- Personas in preparation: Aqilah, Hidayah
- Cadence: continuous, 24/7

## Volume

- Comments observed per day: low hundreds, peaking on viral-post days into low thousands
- Comments engaged with: a curated subset, governed by routing priority and skip rate
- Replies issued per day: tens to low hundreds
- Reactions issued per day: roughly twice the reply volume

## Latency

- Comment-to-reply median: in the single-digit minutes
- Comment-to-reply 95th percentile: in the low double-digit minutes
- This latency is by design. Faster replies feel non-human and trigger anti-spam classification.

## Reliability

- Anti-spam blocks observed in steady state: rare, contained when they occur, fully recovered within their cooldown window
- Shadow-hide events: a small ongoing background rate, detected and remediated automatically
- Unrecovered failures requiring human intervention: zero to date

## Classifier behaviour

- Confidence distribution skews high; low-confidence classifications are routed to a refuse-and-deflect category
- Mis-classification rate, sampled weekly, is low single-digit percent
- Prompt injection attempts: several per week, all caught at the classifier layer

## Persona engagement quality

- Voice consistency, sampled by human review: high
- Refusal compliance: 100% on tested categories
- DM-redirect violations: zero
- Off-brand replies requiring deletion: a small handful, each generating a post-mortem and a rule-set adjustment

## What we are not publishing

- The exact numerical values for the ranges above
- The classifier confidence threshold
- The skip rate
- The reply caps
- The reaction caps
- Per-agent reply distributions
- Cost-per-reply economics

These are tuning sheets and competitive information.

## What this report is for

This report exists to demonstrate that the system is real, operating, and observable. The architecture documented in this repository corresponds to a production system, not a paper design. The discipline described in the operational runbooks corresponds to actual incidents and actual recoveries.

If you want the numbers behind the ranges, [talk to us](../../README.md#contact).
