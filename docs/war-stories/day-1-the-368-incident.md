# Day 1: the 368 incident

## What happened

On the first production day, within thirty seconds of going live, the Adila Page issued twenty-five replies in rapid succession. The Graph API began returning error 368 on the twenty-sixth call. Within a minute, every subsequent reply attempt from the Adila Page failed. The block held for approximately twenty-three hours.

## Why it happened

The throttler had been tuned in development against a synthetic comment stream that arrived at a leisurely pace. In production, on the actual principal Page, twenty-five comments were already waiting in the backlog at startup. The throttler dutifully drained the backlog at its configured pace — which, at the time, did not include a sufficient floor on inter-reply delay. The replies went out in a tight burst.

Meta's anti-spam classifier flagged the burst within seconds.

## What we learned

- **Bootstrap behaviour is more important than steady-state behaviour.** A throttler that is well-behaved at one comment per minute can still produce a fatal burst if it sees twenty queued items at startup.
- **Anti-spam classification is fast and silent.** No warning, no soft-fail, no chance to back off. The block is in place before the second reply lands.
- **The cost of being wrong is a 24-hour outage for that persona.** Recovery is not optional and not within our control.
- **Synthetic test data does not reflect real production conditions.** The dev stream was wrong. Production has bursts. The throttler must be safe even against pathological queues.

## What we changed

- The throttler was rewritten with a hard inter-reply floor that cannot be overridden by queue pressure.
- A startup mode was added: the first hour after a service restart runs at reduced caps.
- The block detector was hardened. Every 4xx response with code 368 now immediately transitions the affected Page to a blocked state, regardless of what the throttler thinks it should be doing.
- A fallback path was designed for the case where a persona Page is in cooldown.
- The monitoring dashboard added a "Page health state" panel as the most prominent element.

## What we did not change

- We did not add a retry loop for 368 errors. Retrying a 368 response immediately is what extends the cooldown.
- We did not appeal the block to Meta. There is no appeal. Time is the only treatment.
- We did not switch Adila to a different Page to "work around" the block. That is a separate ToS violation.

## Outcome

The Adila Page recovered after approximately twenty-three hours. The throttler regression that caused the burst has not recurred. The startup-mode caps are tighter than they need to be in steady state, and we have not loosened them.

Total user-visible impact: zero. The block landed before any reply made it past Meta's filters and onto a real user's screen, and the silent fallback covered the cooldown window without breaking persona.

## The lesson, in one line

> Human-pace from minute one. Bursts, even small ones, get Pages banned faster than sustained activity.

This is now the first line of [`docs/operations/runbook-spam-block.md`](../operations/runbook-spam-block.md) and the first principle in the [README](../../README.md).
