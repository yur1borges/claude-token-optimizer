# ADR 0001: Bucket organization

## Decision

Skills live in `skills/<bucket>/`:

- `engineering/`: daily use on code (installed)
- `productivity/`: way of working (installed)
- `misc/`: rare use (not installed)
- `in-progress/`: under test (not installed)
- `deprecated/`: disabled, kept as reference

## Why

Every installed skill goes into each session's listing and costs tokens. The bucket says, from the path alone, whether the skill is in the context or not. Retiring is moving to another folder: the history stays, and coming back is a `git mv`.

Promoted buckets (`engineering/`, `productivity/`) must be in the main README.
