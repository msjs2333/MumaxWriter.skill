---
name: mumax3
description: Use when writing, reviewing, parameterizing, debugging, or orchestrating mumax3 .mx3 simulations, including micromagnetic geometry, domain walls, vortices, skyrmions, spin waves, regions, masks, anisotropy modulation, spin torque, OVF/table output, checkpoint reuse, parameter scans, and Python-based batch workflows.
metadata:
  short-description: Write and parameterize mumax3 scripts
---

# mumax3 Skill

Use this skill to produce reliable mumax3 `.mx3` scripts and surrounding automation. Keep mumax3 as the simulation backend; use Python for orchestration, validation, fitting, and plotting when the task exceeds one simulation.

## Core Workflow

1. Read existing `.mx3` scripts before editing.
2. Preserve physical behavior unless the user explicitly requests a model change.
3. Use mumax3 syntax and API, not full Go and not invented helper APIs.
4. Keep simulation parameters centralized near the top of the script or in a Python case/config layer.
5. Structure scripts in this order: output settings, mesh, geometry, material, initial state/load state, fields, regions/damping, output schedule, run/save.
6. Add concise comments for geometry, material parameters, fields, source masks, output, and run stages.
7. For parameter sweeps, prefer Python-generated `.mx3` files over complex control logic inside mumax3.
8. Record parameters, generated scripts, input hashes, case signatures, logs, output paths, and analysis provenance.
9. Keep simulation completion, analysis completion, and scientific classification as separate states.

## Safety Invariants

These invariants apply to orchestration, analysis, reuse, and cleanup. Project-local automation may strengthen them but must
not weaken them.

1. **Single writer:** only one writer may mutate a declared output resource at a time. Use separate resource locks for
   simulation, analysis, and render/manifest work; a GPU capacity lease is not a writer lock.
2. **SHA256 lineage:** bind reused inputs, generated scripts, frame manifests, and derived products to content hashes.
   Filenames, absolute paths, and modification times are not scientific identity.
3. **All-vector decision gates:** orientation, reset, switching, and descendant decisions must evaluate every required frame
   in the declared decision window with all required vector components, including `mx`, `my`, and `mz` when magnetization
   orientation is at issue. A final frame or one display component cannot hide an intermediate failure.
4. **Manual/automatic separation:** automated execution, evidence, tracker, and gate state must not create or overwrite a
   human scientific classification. A tracking gap is not by itself a physical conclusion.

## Syntax Guardrails

mumax3 uses a limited Go-like script language. Do not generate full Go.

Allowed/common:

- `:=` for new variables, `=` for existing variables.
- Single assignment only; avoid multiple assignment.
- `if` / `else` and basic `for init; cond; post {}` loops.
- Function and method calls such as `SetGridSize(...)`, `m.LoadFile(...)`, `Msat.SetRegion(...)`.
- `+`, `-`, `*`, `/`, comparisons, `&&`, `||`, `!`, `++`, `--`, `+=`, `-=`.
- `//` comments.

Avoid:

- `package`, `import`, `func` declarations, structs, interfaces, goroutines, channels.
- `switch`, `range`, `return`, `break`, `continue`, `defer`, `goto`.
- Go package selectors such as `fmt.`, `math.`, `os.`, `strings.`, or custom Go functions.
- `%`, bitwise operators, shifts, multiple assignment, and unsupported compound assignment.
- `^` for powers; use `pow(x, y)`.

Read `references/language_subset.md` when validating syntax. Read `references/anti_patterns.md` when checking Go/mumax3 boundary mistakes.

## Reference Selection

- Pure `status`, ETA, monitor, or cancel work: read `references/project_workflows.md` and the current operation/handoff only.
  Do not load the API catalog, geometry history, or large field outputs unless the status evidence is insufficient.
- Plot, GIF, or summary-only work: read `references/output_and_reproducibility.md`, the exact input manifest, and the selected
  analysis/plot profile. Read model references only when a plotted quantity or scientific purpose is unresolved.
- Geometry, material, initial-state, field, source, torque, or protocol changes: read
  `references/project_discovery.md`, the complete active project context, the active source/template, and the applicable API
  references. Verify parent SHA256, initial-state role, and allowed field protocol before reuse.
- Descendant preparation or scientific classification: read the versioned decision contract, fresh gate summaries, and the
  complete ancestor chain. Missing or stale required evidence fails closed.
- Long background work: read `references/project_workflows.md` for the local handoff/monitor contract. Keep monitoring input
  compact; do not send OVF data, full timelines, or complete case records through routine polling.

Technical references:

- Normal script generation: read `references/api_index.md` first, then `references/api_patterns.md`.
- Syntax uncertainty: read `references/language_subset.md` and `references/anti_patterns.md`.
- Existing-script review or disputed identifiers: check `references/api_full.md`.
- Runnable examples: read `references/examples.md`.
- Structure-specific modeling: read `references/structures.md`.
- Repository-specific work: read `references/project_discovery.md`, then any discovered project context.
- Batch runs, output folders, OVF/table/log handling, metadata, cold copies, retention, or release: read
  `references/output_and_reproducibility.md`.
- Task CLIs, signatures, resume behavior, ETA, manual review, and test layering: read `references/project_workflows.md`.
- Advanced features or version-sensitive behavior: read `references/compatibility_notes.md` and the official mumax3 API.
- Parameter scans, fitting, optimization, or plotting: read `references/parameter_sweep.md`.

Do not invent mumax3 APIs. If a needed identifier is absent from `api_index.md`, confirm it in `api_full.md` or the official API before using it.

Before declaring a short variable with `:=`, check whether the name is a mumax3 built-in identifier. Constants and quantities such as `mu0`/`Mu0`, `pi`, `t`, `m`, `Msat`, `B_ext`, and `OutputFormat` are provided by mumax3 and should not be redeclared.

## Project Discovery

Before changing an existing repository, inspect its scripts, templates, root documentation, and current task records. If
`docs/mumax3_reference/current_project_context.md` exists, read it completely before changing geometry, materials, initial
states, fields, sources, torque, scans, checkpoints, or postprocessing. Treat that project-local file and the source scripts
it links as authoritative over bundled examples or remembered defaults.

For status/ETA/cancel and presentation-only work, load only the compact current-operation record, exact product manifest, and
the relevant profile. Do not bulk-read large outputs or historical context merely because the repository contains them.

## Static Review Helper

When reviewing generated or user-provided scripts, run `scripts/check_mx3_static.py path/to/file.mx3` if local tools are available. Treat its output as conservative warnings only; it does not prove mumax3 semantics.

## Deterministic Helpers

Use `scripts/render_template.py` to render `assets/templates/*.mx3.template` files from JSON or `KEY=VALUE` pairs. Use `scripts/collect_case_status.py` to summarize case folders, metadata, logs, and output files. These helpers report file/template status only; they do not validate physical correctness.

Use `scripts/sync_local_skill.py` to compare or safely synchronize this maintained skill into a local Codex skills directory.
Run it with `--dry-run` first; applying a sync creates a timestamped backup before replacing the target tree.

## Review Checklist

Before finalizing `.mx3` code:

- Mesh dimensions and cell sizes match the intended physical model.
- Geometry dimensions use SI units.
- Region indices do not conflict unintentionally.
- Material parameters are assigned globally or with `SetRegion` on supported quantities.
- Time-dependent fields are assigned directly to quantities that accept functions.
- Absorbing boundary regions do not overwrite important physical regions without intent.
- Output filenames include key parameters or are placed in case-specific directories.
- Scripts needed by later stages save the expected OVF files.
- Reused OVF inputs match the recorded geometry, mesh, and SHA256.
- Reused initial states have a compatible physical role and field protocol; SHA256 alone is not a physical validity gate.
- Decision plots contain every quantity required by their versioned decision contract and cover its complete frame window.
- Local anisotropy or torque masks do not silently overwrite absorber regions or other material assignments.
- Batch-generation code records signatures, parameters, inputs, logs, and analysis provenance.
- Data considered for release is sealed against new writers, references, profiles, and manual-evidence changes.
- A cold copy is bound to stable volume/snapshot identity and verified recovery; a drive letter or mirrored path is not proof.
- Automated topology or connected-component metrics remain supporting evidence when strong deformation or multiple textures make pairing ambiguous.

