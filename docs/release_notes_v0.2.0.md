# Release Notes: v0.2.0

Release date: 2026-10-30

## Changes

- Add a concise, separate MuMax3 installation guide covering NVIDIA GPU/driver checks, official binaries, WSL 2, source-build requirements and agent-assisted installation. The main skill loads it only for setup or missing-engine tasks.
- Remove repository citation metadata and software-archiving preparation from the current documentation; simplify the English, Chinese and Japanese READMEs.
- Include the previously unreleased workflow simplification, optional case-status helper fixes, backed-up local skill synchronization and scoped release validation. See [CHANGELOG.md](../CHANGELOG.md) for details.

## Compatibility

The skill remains at `skills/mumax3/` and targets native MuMax3 `.mx3` scripts. MuMax+ support remains a future direction. Existing templates and helper interfaces remain compatible. Installing the skill does not install MuMax3 or authorize system changes.

## Validation

The full `python tests/validate_release.py` check passed: metadata and reference links, maintained-file scan, helper regression tests, three templates, static checks and `mumax3 -vet` on all seven expected-output scripts. Static checks and engine vet do not establish physical correctness or numerical convergence.
