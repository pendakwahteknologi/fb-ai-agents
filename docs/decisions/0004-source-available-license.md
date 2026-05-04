# ADR 0004: Source-available, non-commercial license

## Status

Accepted.

## Context

This repository is published as a documentation artefact. It contains architecture, operational runbooks, decision records, and skeleton interfaces. It does not contain the intelligence layer (prompts, persona rule-sets, throttling constants, classifier weights, recovery heuristics).

The choice of license shapes both the legal and the cultural framing of what we are doing.

## Decision

We use the [PolyForm Noncommercial License 1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0).

## Consequences

- Anyone may read, study, and modify the contents of this repository for non-commercial purposes.
- Charitable, educational, public-research, and government use is explicitly permitted.
- Commercial use requires a separate agreement with Pendakwah Teknologi.
- Derivative commercial products are not permitted under this license.

## Rationale

We want this repository to be a learning resource. We want to share the architecture, the operational discipline, and the lessons. We want students, researchers, and small civic-tech projects to read it and benefit.

We do not want a competitor to clone the repository, fill in the gaps with three months of work, and sell the result as a product. The License floor protects against the latter while the openness ceiling permits the former.

The PolyForm Project licenses are well-drafted, plain-English, and recognised as source-available standards. PolyForm Noncommercial 1.0.0 is the right point on the spectrum for our intent.

## Alternatives considered

- **MIT or Apache 2.0.** Rejected. Permits competitive commercial cloning, which is the exact outcome we want to prevent.
- **GPL or AGPL.** Rejected. Copyleft is misaligned with our intent — we are not trying to force derivative works open; we are trying to prevent commercial exploitation of our materials.
- **Proprietary, all-rights-reserved.** Rejected. Conflicts with the goal of being a public learning resource.
- **Business Source License (BUSL).** Considered. Has a time-based commercial conversion clause that does not match our intent.

## Notes

The intelligence layer is not in this repository and is not under this license. It is held privately by Pendakwah Teknologi and is licensed only via direct commercial agreement.
