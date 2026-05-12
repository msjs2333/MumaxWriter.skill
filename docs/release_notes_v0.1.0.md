# Release Notes: v0.1.0

Release date: 2026-05-12

## Scope

MumaxWriter.skill v0.1.0 provides a generic Codex skill for writing, reviewing, parameterizing, and maintaining mumax3 `.mx3` scripts.

Included:

- Runtime skill under `skills/mumax3/`.
- mumax3 syntax guardrails, anti-patterns, API references, modeling patterns, parameter sweep guidance, output reproducibility guidance, and compatibility notes.
- Runtime templates for minimal relaxation, region-aware relaxation, and local AC-field dynamics.
- Standard-library Python helper scripts for static warnings, template rendering, and case status collection.
- Evaluation prompts, expected outputs, template parameter examples, and manual evaluation checklist.
- Local release validation through `tests/validate_release.py`.

## Compatibility

- API references target the official mumax3.12 API page.
- Helper scripts use only the Python standard library and were validated with Python 3.13.
- `mumax3 -vet` checks are optional in the validator and run when mumax3 is available on `PATH`.

## Validation

The local release validation passed on 2026-05-12:

```powershell
python tests\validate_release.py
```

Validation covered:

- `SKILL.md` metadata checks.
- Python helper bytecode compilation.
- Template placeholder checks with tracked example params.
- Static checks on expected-output `.mx3` scripts.
- `mumax3 -vet` on expected-output `.mx3` scripts.
- Tracked sensitive-term scan.

## Known Limitations

- Static checks and `mumax3 -vet` do not prove physical correctness, numerical convergence, or publication readiness.
- `api_full.md` is kept as a sparse identifier/signature index with provenance; official mumax3 documentation remains the authority for detailed API semantics.
- Examples are generic smoke-test and evaluation artifacts, not calibrated physical studies.
- Advanced workflows such as domain-wall propagation, hysteresis standard problems, absorbing-boundary spin-wave guides, STT/SOT dynamics, and multilayer/RKKY examples remain future coverage.

