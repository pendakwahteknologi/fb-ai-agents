# `src/` — interfaces only

This directory contains the **type signatures and module shapes** of the production system. It does not contain implementations.

The intelligence layer — the classifier prompt, the persona rule-sets, the throttling constants, the routing priority weights, the recovery heuristics, the verification logic — is held privately by Pendakwah Teknologi and is not open-sourced.

## Why

We share the architecture because the architecture compounds learning across the field. We do not share the intelligence layer because the intelligence layer is the product.

A determined engineer could rebuild a worse version of this system from public documentation in three months. Building one that does not get its Pages banned in the first hour is a different problem.

## What you will find

Each file in `interfaces/` declares the public surface of one component:

- [`classifier.py`](interfaces/classifier.py) — the categorisation step
- [`router.py`](interfaces/router.py) — comment-to-agent routing
- [`throttler.py`](interfaces/throttler.py) — human-pace pacing and backoff
- [`poster.py`](interfaces/poster.py) — outbound Graph API calls
- [`state_store.py`](interfaces/state_store.py) — atomic persistence

The signatures are real. They reflect the actual production interfaces. The bodies are not here.

## How to use this

If you want to understand the shape of the system: read the interfaces.

If you want to use the system: [talk to us](../README.md#contact).
