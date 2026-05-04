# Runbook: token rotation

## When to rotate

- A token is suspected of having leaked.
- An admin role on the Page or Business Portfolio has changed.
- A periodic rotation is due (we rotate annually as a matter of hygiene, even though the long-lived flow does not strictly require it).
- The `/debug_token` endpoint reports a state inconsistent with our records.

## Pre-flight

1. Confirm the operator performing the rotation has Admin (not Editor) role on every Page involved.
2. Confirm 2FA is enabled on the operator's personal Facebook account.
3. Confirm the Business Portfolio is in good standing.
4. Notify the on-call operator that a rotation window is opening.

## Procedure

1. Generate a new short-lived User Access Token via the Graph API Explorer with the required permission set.
2. Exchange the short-lived User Access Token for a long-lived User Access Token using the standard endpoint.
3. From the long-lived User Access Token, fetch the Page Access Token for each persona Page. For Pages held inside a Business Portfolio, this requires `business_management` permission and a different code path than Pages held personally.
4. Verify each new Page Access Token via `/debug_token`. Confirm the `expires_at` field is `0` (never expires) and the scopes are correct.
5. Update the secrets store with the new tokens. Atomic write only.
6. Restart the service. Monitor the readiness endpoint until all agents return healthy.
7. Watch the activity log for the first ten minutes. If anything looks wrong, roll back to the previous token set.

## Verification

- Health endpoint reports all agents healthy.
- A test comment flows end-to-end and produces a reply within expected latency.
- No `OAuthException` errors in the log.
- Page health states are unchanged.

## Rollback

- Restore the previous token set from the previous-version secrets snapshot.
- Restart the service.
- Investigate the failure before attempting another rotation.

## Do not

- Do not commit tokens to git. Never. Logs auto-redact, but git does not.
- Do not store tokens in a shared chat, screenshot, or third-party clipboard manager.
- Do not generate tokens on a machine that is not the production secret-management host.

## Reference

The exact token-fetch scripts and the Business Portfolio fallback path are not published. The procedure above is the operator-facing description.
