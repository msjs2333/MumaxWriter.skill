---
name: mumax3
description: Write, review, debug, and parameterize MuMax3 .mx3 simulations, including geometry, materials, fields, initial states, OVF output, and Python batch workflows.
metadata:
  short-description: Write and parameterize mumax3 scripts
---

# mumax3

Use native MuMax3 for `.mx3` simulations. Python can handle case generation, analysis and plotting when useful; keep existing workflows unless the request calls for a change.

## Start with the requested work

Read the target script and relevant task instructions. Use current source and input records to resolve parameters; generic examples and historical plans are not evidence of what ran. Do not load an entire project history for a local edit.

- **Edit or generate a script:** check the identifiers and patterns you need in [api_index.md](references/api_index.md) and [api_patterns.md](references/api_patterns.md), not both files in full by default.
- **Syntax uncertainty:** use [language_subset.md](references/language_subset.md) and [anti_patterns.md](references/anti_patterns.md). MuMax3 is Go-like, not full Go. Do not redeclare built-ins such as `mu0`, `t`, `m`, or `B_ext`.
- **Missing/disputed API:** search [api_full.md](references/api_full.md); consult [compatibility_notes.md](references/compatibility_notes.md) and the official API for version-sensitive behavior. Do not invent identifiers.
- **Model-specific help:** choose [structures.md](references/structures.md) or [examples.md](references/examples.md).
- **Output or sampling design:** use [output_and_reproducibility.md](references/output_and_reproducibility.md).
- **Batch or staged execution:** use [parameter_sweep.md](references/parameter_sweep.md) or [project_workflows.md](references/project_workflows.md) when designing that workflow, not for each status query.
- **Unfamiliar repository:** [project_discovery.md](references/project_discovery.md) gives a short discovery approach.

For status/ETA, read the task's compact state and supported entry point. For presentation-only changes, use the exact plot inputs or cache and plotting code. Expand context only when the requested decision needs it.

## Scientific and execution principles

- **Single writer:** coordinate concurrent changes to the same output; independent outputs need not serialize. Use the project's existing mechanism when present.
- **SHA256 lineage:** keep critical reused inputs and scientific derivatives traceable to their actual content. Apply hash checks where reuse, publication, or data release requires them; a matching hash alone does not establish physical compatibility.
- **Full-vector evidence when needed:** orientation or switching decisions require adequate vector evidence over the relevant window. The scientific question determines components, sampling and thresholds; a display image need not show every component. Automatic gates and ancestor checks apply when the task's decision depends on them, not to every script or plot.
- **Human/automatic separation:** distinguish simulation completion, analysis findings and human scientific conclusions. Automated metrics do not silently overwrite a human classification; missing tracking evidence is not itself a physical conclusion.

## Check the changed behavior

For physical edits, check SI units, mesh/cell size, geometry and region assignments, field/mask interactions, and required outputs. Reused states should fit the mesh, geometry and physical role of the new stage. Scope the checks to what changed.

`scripts/check_mx3_static.py path/to/file.mx3` provides conservative warnings, not proof of valid physics. Use engine `mumax3 -vet` when syntax/API changes warrant it; report unavailable checks. Numerical convergence and scientific acceptance require task-appropriate evidence, not a blanket checklist.

## Helpers

- `scripts/render_template.py`: render `assets/templates/*.mx3.template` using JSON or `KEY=VALUE` parameters.
- `scripts/collect_case_status.py`: report file/metadata status; inspect `--help` and the task's conventions before using it. It does not validate physics.
- `scripts/sync_local_skill.py`: maintenance only; preview with `--dry-run` before an authorized `--apply`, which backs up the prior installation.

Project-specific state schemas, monitoring schedules, storage/prune protocols, and agent assignments belong in project guidance, not in this skill's default workflow.

