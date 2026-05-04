# Why the Reactions API broke us

## What happened

The original design called for agents to react to comments with the full set of Facebook reactions: Like, Love, Care, Haha, Wow, Sad, Angry. Different reactions would be selected based on classified comment sentiment, adding nuance to the engagement layer beyond replies.

The Reactions API requires App Review.

## Why it happened

Meta gates reaction-posting behind the `pages_manage_posts` permission at higher review tiers, depending on the exact endpoint and reaction type. App Review is an extensive process involving recorded screencasts, business verification, and policy review. We chose not to pursue it for our scope.

## What we learned

- **App Review is a major commitment.** It is not a forms exercise. It is closer in spirit to a regulatory submission.
- **Permission tiers are not always documented at the granularity required.** We discovered the gating empirically.
- **A planned feature can disappear quickly if the permission is not available, and the system must remain useful without it.**

## What we changed

- The reaction layer was reduced to Like-only, using the `/likes` endpoint, which works under our existing permissions.
- The classifier no longer outputs a reaction-type recommendation. It outputs a binary should-react decision.
- The persona reply engine compensates for the loss of reaction nuance by using reply tone more deliberately. A Care reaction is replaced by an empathetic short reply. A Haha reaction is replaced by a light reply. The texture is preserved at a different layer.
- The Reactions caps were raised slightly to compensate for the loss of expressive range. A Page that "Likes" a thoughtful comment is reading more meaning into a Like than a Page that has Care available, so we Like more selectively.

## What we did not change

- We did not pursue App Review. The cost-benefit did not justify it for the marginal gain of full reaction support.
- We did not abandon reactions altogether. Likes are still significant engagement signal.

## Outcome

The system operates with Like-only reactions. The user-visible impact is small. The architectural lesson — that any permission-gated feature can disappear and the system must degrade gracefully — has informed every subsequent design decision.

## The lesson, in one line

> Design every feature so that losing it gracefully is one of the supported states, not an emergency.
