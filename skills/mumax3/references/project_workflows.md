# Project Workflow Patterns

Use this reference for multi-stage or multi-case simulation projects.

## Task Interface

Prefer one user-facing Python entry point per task and keep reusable implementation in a package module. Common commands are:

- `doctor`: verify the mumax3 executable, input checkpoints, storage, and optional dependencies.
- `prepare --dry-run`: show planned cases without writing.
- `prepare`: render scripts, manifests, signatures, and input records.
- `run` and `run-one`: execute resumably and isolate one case when needed.
- `start`: launch a background operation only after its lock, running state, process identity, logs, and monitor handoff are durable.
- `postprocess` and `postprocess-one`: derive results without rerunning dynamics.
- `status` and `eta`: report compact current state and evidence-based timing estimates.
- `monitor --until-terminal --emit-on-change`: follow the local handoff without repeatedly loading large records.
- `cancel`: record the request and terminate the declared process tree while preserving partial-output evidence.
- `classify`: record a human scientific review separately from automated metrics.
- `summary`: aggregate only fresh and compatible analyses.

Not every task needs every command, but its public contract and resume behavior should be explicit.

## State Safety Primitives

Make state and manifest safety a dependency of background work, not an optional later optimization.

- Write JSON through a same-directory unique temporary file, flush and close it, then atomically replace the destination.
  Keep a backup only when the previous file is known to be valid.
- A resilient reader must distinguish `ok`, `missing`, `corrupt`, `recovered_from_backup`, and `schema_invalid`. Do not catch
  arbitrary errors and return an empty object that can be mistaken for "not prepared".
- Acquire a writer lock atomically for the exact mutable resource. Record host, PID, process-start identity, nonce, command,
  resource, and input signature so PID reuse and conflicting inputs are detectable.
- Do not delete a lock merely because it is old. Automatic stale takeover is safe only when the same-host owner identity is
  proven dead; cross-host or insufficient evidence requires an explicit user-approved takeover path.

Separate resource keys for simulation/case output, analysis products, and render/manifest publication allow unrelated work to
proceed while retaining one writer per mutable resource. Readers do not acquire a writer lock.

## State Model And Terminal Semantics

Keep these axes separate in storage and status output:

- `execution_state`: prepared, queued, running, completed, failed, or cancelled;
- `output_completeness`: complete, complete with declared gaps, incomplete, or reconciliation required;
- `analysis_state` and freshness: absent, running, fresh, stale, partial, or failed;
- `automatic_gate_state`: contract findings that may control an authorized workflow;
- `manual_classification`: a separately owned human scientific conclusion.

Tracker or component-pairing output belongs to `tracker_status`; it must not write a physical conclusion such as annihilation,
successful reset, or topology loss. Terminal status takes precedence over ETA: completed work reports zero remaining time,
while scientific-gate failure, execution failure, cancellation, and stale input remain distinct states and exit codes.

Each coarse scan, confirmation, hold, analysis, and render operation needs its own operation ID, start time, elapsed time, and
terminal record. Do not reuse an old operation start time for a later phase.

## Decision Contracts And Ancestor Gates

A decision that can launch descendants or support a scientific label must be versioned and declare:

- required quantities and vector components;
- the complete frame/time window and critical frames;
- thresholds, permitted warnings, and hard-stop findings;
- input frame-manifest SHA256 and analysis signature;
- required evidence products and whether partial analysis is allowed.

For orientation, reset, and switching decisions, inspect every required frame in the decision window and all required
magnetization components (`mx`, `my`, and `mz` when orientation is at issue). A final frame, a single display component, or an
early good interval cannot replace the declared window.

Write a compact gate summary per stage while retaining the full timeline as a product. Before preparing a child, validate the
complete ancestor chain. Missing, stale, hard-failed, or contract-disallowed warning summaries fail closed. A task may stop
descendant progression after a hard finding, but partial evidence must remain marked incomplete and must not become a human
classification.

Automated gates may drive only transitions authorized by the versioned contract. Human classifications and overrides remain
separate, retain the original automatic evidence, and are never overwritten by tracker, gate, resume, or cleanup code.

## Background Handoff And Monitoring

A successful background `start` commits, in order: the resource lock, running state, process identity, stdout/stderr paths,
and `monitor_handoff.json`. If any element is missing, `start` fails instead of returning an unmonitorable success.

The handoff should contain a schema version, task/case/operation identity, parent and child PIDs with process-start identity,
repo-relative state/log paths, terminal states, suggested polling interval, stall threshold, and a read-only path allowlist.
Routine monitoring reads the compact status, emits on change, and tails only the declared log amount. It does not read OVF
frames, full timelines, or complete case records.

Local deterministic monitoring is the baseline. Delegating polling to another model or service is an optional consumer of the
same handoff, not a prerequisite for safe execution.

## Cancellation And ETA

Cancellation records request time, worker acknowledgement, terminate/kill escalation, process-tree cleanup, and the observed
partial output. Use distinct outcomes such as `cancelled_by_user`, `engine_error`, `gpu_error`, and `incomplete_timeline`.
Cancelled samples do not enter ETA calibration and are not retried automatically.

ETA groups observations by operation/phase and relevant environment factors such as mesh, demagnetization setting, GPU,
mumax3 version, host, and output profile. Dynamic case generation must expose a projected-case function. Record estimates as
estimates, retain measured elapsed time, and avoid universal seed multipliers or response-time constants.

## Signatures And Checkpoints

Record canonical hashes for:

- the physical case configuration;
- the rendered template or template version;
- every reused OVF input;
- the dynamic output frame manifest;
- the analysis configuration.

Persist repository objects as repository ID plus repository-relative path plus SHA256. Absolute/logical/physical paths are
diagnostic observations, not identity, and mtime may only shortlist candidates. Separate simulation, analysis, and plot source
signatures and list shared dependencies explicitly.

For reused initial states, record the physical role, preparation field/protocol, material and geometry identity, source task,
and allowed downstream field protocols. Matching SHA256 proves content identity, not physical suitability.

Reject or mark stale outputs when the recorded input hash or signature no longer matches. A matching filename alone is not
proof of provenance. For nonlinear checkpoints, verify a known SHA256 before reuse.

## Resume And Failure Handling

- Default to resuming complete, signature-matching stages.
- Do not overwrite a complete case without explicit force.
- Archive partial or incompatible outputs before retrying.
- Distinguish execution failure, incomplete output, stale analysis, and pending manual review.
- Record elapsed time per physical and analysis stage so ETA can use observed medians.
- Support configurable run, result, checkpoint, and executable paths when cases may move between machines.

## Doctor And Resource Scheduling

Keep `doctor` import-light: standard library plus a minimal shared preflight module at process start, with plotting, fitting,
and task-heavy imports delayed until their subcommands. It should still report Python, mumax3, GPU, path/write permission,
parent input, lock, and protocol-derived disk capacity when an unrelated optional dependency is broken.

Provide `prepare --dry-run`, a minimal smoke case, conservative static checking, and `mumax3 -vet` for new entry points. These
checks establish syntax and environment readiness; they do not prove physics or numerical convergence.

A GPU lease is capacity scheduling, separate from writer ownership. Only mumax3 or an actual CUDA phase requests a lease for
the selected device. CPU plotting and image encoding do not occupy it. Device reserve, slots, and queue policy come from the
task and mesh estimate, not one project-global lock or one universal free-memory threshold.

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

When human review is delayed until the end of a chain, intermediate records say `pending_manual_review`; they do not contain
provisional human labels. Automatic evidence may continue only where the decision contract explicitly permits it.

## Tests

Use fast tests for case planning, signatures, dry-run behavior, resume logic, path overrides, and failure degradation. Mark
real subprocesses, full plotting, GIF encoding, large OVF processing, and real mumax3 runs as integration tests. Tests must use
temporary roots and must not depend on a project's live `runs/` or `results/`.

Add fault-injection tests for truncated JSON, invalid backup/schema, concurrent writers, PID reuse, live/stale/cross-host lock
owners, half-committed starts, user cancellation, and terminal-state/ETA consistency. Add scientific contract tests where an
intermediate vector failure, missing ancestor, stale manifest, or tracker gap must not launch a descendant or write a human
classification.
