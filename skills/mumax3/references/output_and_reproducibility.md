# Output And Reproducibility

Use this reference when choosing outputs, sampling, or reused inputs. For scans, see `parameter_sweep.md`.

## Case Records

Keep the `.mx3` source and inputs needed to reproduce the result. Independent cases need non-colliding outputs, not a prescribed directory or manifest schema. A self-contained script can hold its own parameters; generated cases may benefit from a separate parameter record and engine version/command.

For checkpoint reuse, identify the actual input and its physical role: preparation field/protocol, material, geometry and mesh compatibility. A relaxed state may stay in memory when stages share one script; saving a checkpoint is useful for later reuse or analysis, not a mandatory stage boundary.

SHA256 can verify reused content or cache identity when needed by the task. It cannot establish physical suitability. If a downstream decision relies on an earlier result, check the relevant evidence and acceptance criteria; project contracts may require ancestry checks, but ordinary scripts need no ancestor registry.

## Output Directories

When a launcher, shared workspace, or multiple cases make output paths ambiguous, record the intended path and keep cases
isolated. Prefer `mumax3 -o <stage>.out` when the installed version supports it. Without `-o`, a script named `stage.mx3`
conventionally produces `stage.out`; reconcile the actual directory rather than guessing from similarly named paths.

If the engine exits successfully but its output location is not yet confirmed, record that uncertainty and investigate before
deciding whether to rerun. Record the command, working directory, output location, and return code to the degree needed to
reproduce or diagnose the case. Output discovery is not a scientific-completeness check. `-f` can clean an existing output
directory, so use it only when the requested overwrite policy permits removal of the old output.

## mumax3 Output Conventions

- `Save(quantity)` writes a space-dependent quantity with an automatic name.
- `SaveAs(quantity, "name.ovf")` writes a space-dependent quantity with a chosen name.
- `AutoSave(quantity, period)` writes snapshots periodically.
- `TableAdd(quantity)` adds table columns; `TableAutoSave(period)` schedules table output.
- `TableSave()` appends a table row immediately.
- `Snapshot`/`SnapshotAs` writes images when image output is desired.

For scripts with region logic, `SaveAs(regions, "regions.ovf")` is a useful debug artifact.

## Sampling And Completion

Select quantities, cadence and time window for the intended measurement. A global response can use averaged tables; spatial modes or texture motion may need fields. When a conclusion relies on a time sequence, check its relevant window for gaps or missing critical times. A frame-count percentage alone does not establish scientific completeness.

Choose cadence from the analysis goal. Periodic or phase-sensitive analysis needs enough samples, phase coverage, and windows
to support the intended inference; one fixed cadence or component set does not fit every problem. Estimate output size from
the grid, quantities, frame plan, and product needs before a large run, using margins appropriate to the task.

## Optional Naming Convention

- Include key scanned parameters in case IDs or folder names, not every output filename.
- Prefer stable filenames inside a case folder: `m_initial.ovf`, `m_relaxed.ovf`, `m_final.ovf`, `regions.ovf`.
- Avoid fixed filenames across a sweep unless each run has an isolated working directory.

## Derived Products

Keep analysis inputs and relevant settings identifiable so a presentation change need not rerun dynamics. Repeated plotting can use a profile for units and normalization; a one-off plot needs no profile framework. Display choices and scientific evidence need not use the same quantities or order.

## Logs And Postprocessing

- Capture stdout and stderr from the native `mumax3` process.
- Store generated scripts next to parameters, not only templates.
- Keep analysis scripts separate from raw simulation outputs.
- Write derived tables with explicit units in column names or metadata.

Project-specific backup, retention, release, and storage procedures belong in that project's documentation.

## Helper Script Invocations

Render a repository template after listing the required placeholders:

```powershell
python skills\mumax3\scripts\render_template.py skills\mumax3\assets\templates\minimal_relax.mx3.template --list
python skills\mumax3\scripts\render_template.py skills\mumax3\assets\templates\minimal_relax.mx3.template --params params.json --output script.mx3
```

Optional layout-specific status collector (not a general MuMax output scanner):

```powershell
python skills\mumax3\scripts\collect_case_status.py runs\field_frequency_sweep --recursive --csv results\case_status.csv
```

The collector discovers cases containing `params.json` or a top-level `.mx3`, and expects nested `*.out` outputs. `--result-root` supports its conventional analysis/manual-review JSON records; inspect `--help` before adopting those conventions. A standalone `.out` without source/params is not discovered. Reported freshness compares recorded signatures, not actual physics or file hashes. Use an existing task's status command when available.
