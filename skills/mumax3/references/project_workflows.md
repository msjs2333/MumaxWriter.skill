# Project Workflow Patterns

Use this reference for multi-stage or multi-case simulation projects.

## Task Interface

Prefer one user-facing Python entry point per task and keep reusable implementation in a package module. Common commands are:

- `doctor`: verify the mumax3 executable, input checkpoints, storage, and optional dependencies.
- `prepare --dry-run`: show planned cases without writing.
- `prepare`: render scripts, manifests, signatures, and input records.
- `run` and `run-one`: execute resumably and isolate one case when needed.
- `postprocess` and `postprocess-one`: derive results without rerunning dynamics.
- `status` and `eta`: report current state and evidence-based timing estimates.
- `classify`: record a human scientific review separately from automated metrics.
- `summary`: aggregate only fresh and compatible analyses.

Not every task needs every command, but its public contract and resume behavior should be explicit.

## Signatures And Checkpoints

Record canonical hashes for:

- the physical case configuration;
- the rendered template or template version;
- every reused OVF input;
- the dynamic output frame manifest;
- the analysis configuration.

Reject or mark stale outputs when the recorded input hash or signature no longer matches. A matching filename alone is not
proof of provenance. For nonlinear checkpoints, verify a known SHA256 before reuse.

## Resume And Failure Handling

- Default to resuming complete, signature-matching stages.
- Do not overwrite a complete case without explicit force.
- Archive partial or incompatible outputs before retrying.
- Distinguish execution failure, incomplete output, stale analysis, and pending manual review.
- Record elapsed time per physical and analysis stage so ETA can use observed medians.
- Support configurable run, result, checkpoint, and executable paths when cases may move between machines.

## Regions, Masks, And Staged Drives

Each cell has one region label. A later `DefRegion` can replace an earlier absorber or material region, so inspect overlap
deliberately. Save `regions` for nontrivial layouts. When independent spatial fields must overlap, consider an OVF mask,
`LoadFile`, or a custom quantity instead of forcing every property through the same region map.

For local anisotropy, spin-current, or field schedules:

- save the mask and initial state;
- keep ramp, hold, switch-off, and recovery phases explicit;
- use `RemoveExtraTerms()` before rebuilding staged extra fields;
- document whether `J` is a charge-current density or an effective spin-current input;
- validate `FixedLayer`, `FixedLayerPosition`, thickness, polarization, and torque-disable flags against the installed version.

## Analysis And Human Review

Crop absorbers and source near fields before comparing propagation or focusing metrics. Record static references, frame
manifests, units, and analysis signatures. For topology-rich dynamics, keep net charge, absolute charge, signed density,
connected regions, contact frames, and full-field animations available.

Automated core pairing can fail under strong waves, deformation, or multiple structures. Do not turn a tracking gap directly
into a scientific label such as annihilation. Keep automated state, analysis freshness, and human classification separate.

## Tests

Use fast tests for case planning, signatures, dry-run behavior, resume logic, path overrides, and failure degradation. Mark
real subprocesses, full plotting, GIF encoding, large OVF processing, and real mumax3 runs as integration tests. Tests must use
temporary roots and must not depend on a project's live `runs/` or `results/`.
