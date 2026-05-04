# Runbook: anti-spam block (error 368)

## Symptom

A persona Page suddenly stops being able to post comments. The Graph API returns error code 368, sometimes with sub-codes. Existing replies remain visible. Reactions may continue to work for a short window before they too are blocked.

## Triage

1. Check the Page health endpoint. The affected Page should already be marked blocked by the throttler. If it is not, the detector is broken and is itself an incident.
2. Check the activity log for the burst that triggered the block. There will be one. Anti-spam blocks are caused.
3. Determine whether the burst was a configuration regression, a real spike in incoming comments, or an operator action.

## Containment

- The throttler will already have transitioned the Page to a blocked state with a 24-hour TTL.
- The router will exclude the Page from selection for the duration.
- Where a fallback path exists for the affected agent, it will engage automatically. Where it does not, the agent is silent for the cooldown.
- Do not attempt to manually clear the block flag before the cooldown expires. The block is server-side, not client-side. Local clearing only causes more 368 errors and extends the cooldown.

## Recovery

- After 24 hours, the Page is moved to a probationary state. Caps are reduced. Jitter is widened.
- Operators monitor the first hour of probation closely. If a second 368 occurs in probation, the cooldown is extended and the Page moves into deep cooldown (typically 72 hours).
- After a clean probation hour, the Page returns to standard operating limits.

## Root cause analysis

Every 368 event requires a written post-mortem in the internal log. The post-mortem must answer:

- What was the burst pattern?
- Why was the throttler not stricter?
- Was the trigger a configuration change, a model output change, or an upstream comment volume change?
- What change is being made to prevent recurrence?

## Do not

- Do not switch to a different Page to "work around" the block. Cross-Page substitution under the same persona is a separate ToS violation.
- Do not delete and recreate the Page. The IP and admin signal carry over, and the Page is now also new — a worse position.
- Do not appeal the block via Meta support. There is nothing to appeal; the block is automatic and time-bounded.

## Reference

The detection mechanism, the exact cooldown durations, and the probationary cap reductions are tuned values. They are not in this repository.
