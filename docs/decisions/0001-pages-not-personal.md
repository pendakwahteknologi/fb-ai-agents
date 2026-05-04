# ADR 0001: Pages, not personal accounts

## Status

Accepted. Non-negotiable.

## Context

The original design impulse was to give each persona a Facebook account that looked like a real human — a profile photo, a friends list, posts on a timeline. A persona "lives" more credibly on a personal account than on a Page.

## Decision

We use Facebook Pages exclusively. No personal accounts, ever, regardless of design pressure.

## Consequences

- Persona presence is shaped by what Pages can do, not by what people can do. Pages can comment, react, post, and message. Pages cannot, for example, send friend requests or join groups as a member in the same way a person can.
- Each persona is registered in the Business Portfolio and openly affiliated with Pendakwah Teknologi. There is no plausible deniability about the corporate parent. We accept this; it is the honest position.
- The "personhood" of each persona is carried entirely by voice, content, and consistency. Not by the credential type.

## Rationale

Meta's [Platform Terms](https://developers.facebook.com/terms) and [Community Standards](https://transparency.meta.com/policies/community-standards) explicitly forbid automation of personal accounts. The penalty for violation is account termination, often without warning, and often cascading to associated accounts.

The cost of a Page-only design is aesthetic. The cost of a personal-account design is existential.

We chose existence.

## Alternatives considered

- **Personal accounts with manual operation.** Rejected. Manual operation cannot scale to four personas across a 24/7 cycle.
- **Hybrid: personal accounts for "presence," Pages for actions.** Rejected. The personal accounts would still exist and would still violate ToS the moment they are tied to the same operational tooling.
- **A single Page operating all four personas via signed prefixes.** Rejected. Cross-Page spam classification is real. Distributing identities across Pages is a defence-in-depth measure as well as a UX choice.

## Notes

This ADR is the foundation of every other decision in this repository. If you are reading this and wondering whether the rule applies in your edge case: it does.
