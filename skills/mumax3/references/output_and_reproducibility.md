# Output And Reproducibility

Use this reference for case outputs, sampling, and derived products. For sweep generation and analysis choices, also read
`parameter_sweep.md`.

## Case Records

Give each simulation case an isolated working/output location and keep its generated `.mx3` script with the parameters needed
to reproduce it. Record, as applicable, the parameter values and units, mesh/geometry/regions, material and drive schedule,
initial-state role and provenance, output/sampling profile, MuMax3 version and command, and the status of execution and
analysis. A project may choose its own directory and manifest format; avoid duplicating the same metadata in several places.

Keep source and input provenance sufficient to reproduce or assess reuse. Content hashes identify bytes, while physical role,
preparation protocol, and material/geometry compatibility establish whether an initial state is appropriate for a new case.

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

Define expected outputs before launch: relevant quantities, cadence, explicit critical saves, time window, and tables or
checkpoints. Reconcile observed frames and times against that plan, including critical protocol times, monotonic time, and
material gaps or duplicates. A frame-count percentage alone does not establish scientific completeness.

Choose cadence from the analysis goal. Periodic or phase-sensitive analysis needs enough samples, phase coverage, and windows
to support the intended inference; one fixed cadence or component set does not fit every problem. Estimate output size from
the grid, quantities, frame plan, and product needs before a large run, using margins appropriate to the task.

## File Naming

- Include key scanned parameters in case IDs or folder names, not every output filename.
- Prefer stable filenames inside a case folder: `m_initial.ovf`, `m_relaxed.ovf`, `m_final.ovf`, `regions.ovf`.
- Avoid fixed filenames across a sweep unless each run has an isolated working directory.

## Analysis Products And Plot Profiles

Keep analysis and plot inputs distinguishable from raw simulation outputs. A derived metric, array, figure, animation, or
summary should declare the inputs and configuration on which it depends, so a presentation-only change can rebuild without
rerunning dynamics. Plot profiles should state purpose, units, normalization, and required evidence; presentation plots and
scientific decision evidence need not use the same quantities or display order.

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

Collect conservative case status rows from a sweep directory:

```powershell
python skills\mumax3\scripts\collect_case_status.py runs\field_frequency_sweep --recursive --csv results\case_status.csv
```

The helper scripts only inspect template placeholders, metadata, logs, and output files. They do not prove that a simulation is physically correct or numerically converged.
