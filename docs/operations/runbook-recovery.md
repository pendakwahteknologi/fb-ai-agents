# Runbook: recovery from incident

## Categories of incident

1. **Persona drift** — an agent posts a reply that violates voice or refusal rules.
2. **Content failure** — an agent posts a reply that is factually wrong, offensive, or harmful.
3. **Mass mis-classification** — the classifier routes many comments to the wrong agent.
4. **Burst publication** — the throttler fails and a Page replies too fast.
5. **Shadow-hide cluster** — many of an agent's recent replies have been hidden by Meta.

## Immediate actions, by category

### Persona drift / content failure

- Pause the affected agent.
- Delete the offending reply via the admin dashboard or scripted recovery tool.
- Capture the input comment, the classifier output, the routing decision, and the generated reply for the post-mortem.
- Determine whether the cause is the rule-set, the classifier prompt, the model, or the input. Fix at the cause layer.

### Mass mis-classification

- Pause the classifier (the system runs in pause-pending-review mode automatically when classifier confidence drops sustainedly).
- Sample twenty recent classifications. If more than three are wrong, we have a regression.
- Roll back to the previous classifier configuration. We never patch a live classifier; we revert.
- Investigate before reactivating.

### Burst publication

- Stop the service immediately.
- Run the bulk-cleanup tool against the affected Page to delete replies posted in the burst window.
- Investigate the throttler. The throttler is the most safety-critical component in the system; a regression there is a P0 incident.
- Do not restart until the root cause is identified and a regression test is added.

### Shadow-hide cluster

- Run the verification pass against the agent's last fifty replies.
- For each hidden reply, apply the remediation procedure.
- If remediation fails for more than a small fraction, the agent is in a Meta-side trust deficit. Pause the agent. Reduce its caps significantly when reactivated.

## Post-mortem

Every incident, regardless of category, gets a written post-mortem. Format:

- Timestamp
- Detected by (alert / human / external report)
- Category
- Description
- Root cause
- Fix
- Regression test added
- Lesson

The post-mortem log is internal. Lessons that generalise are added to the public war-stories collection in this repository.

## Communication

If the incident is publicly visible — that is, if a real person on Facebook saw the failure — we add a brief acknowledgement reply from a human operator on the affected thread. We do not silently delete and pretend it did not happen. The comment from the user is preserved; only the bot's reply is removed.

## Do not

- Do not roll forward to fix a live incident. Roll back, then fix, then roll forward in the next deploy window.
- Do not blame the model. Models do what we tell them. The fix is in the rule-set, the prompt, or the architecture.
- Do not skip the post-mortem because the fix was small. The post-mortem is the only mechanism that compounds learning across incidents.
