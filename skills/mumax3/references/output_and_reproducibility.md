# Output And Reproducibility

Use this reference for run folder design, output conventions, and metadata. For parameter sweeps, combine it with `parameter_sweep.md`.

## Recommended Run Layout

```text
runs/
  case_0001/
    params.json
    script.mx3
    logs/
      mumax3.stdout.txt
      mumax3.stderr.txt
    out/
    notes.md
results/
  tables/
  fields/
  figures/
```

Keep one generated `.mx3` script per simulation case. Do not overwrite a completed case unless the user explicitly requests rerun behavior.

## Minimum Per-Case Metadata

Record enough to regenerate the case:

- Case ID and creation timestamp.
- Input parameter values and units.
- Mesh size, cell size, geometry, and region mapping.
- Material parameters and initial state source.
- Field/current/excitation schedule.
- Output schedule and expected output files.
- mumax3 command, working directory, stdout/stderr log paths, and status.

## mumax3 Output Conventions

- `Save(quantity)` writes a space-dependent quantity with an automatic name.
- `SaveAs(quantity, "name.ovf")` writes a space-dependent quantity with a chosen name.
- `AutoSave(quantity, period)` writes snapshots periodically.
- `TableAdd(quantity)` adds table columns; `TableAutoSave(period)` schedules table output.
- `TableSave()` appends a table row immediately.
- `Snapshot`/`SnapshotAs` writes images when image output is desired.

For scripts with region logic, `SaveAs(regions, "regions.ovf")` is a useful debug artifact.

## File Naming

- Include key scanned parameters in case IDs or folder names, not every output filename.
- Prefer stable filenames inside a case folder: `m_initial.ovf`, `m_relaxed.ovf`, `m_final.ovf`, `regions.ovf`.
- Avoid fixed filenames across a sweep unless each run has an isolated working directory.

## Logs And Postprocessing

- Capture stdout and stderr from the native `mumax3` process.
- Store generated scripts next to parameters, not only templates.
- Keep analysis scripts separate from raw simulation outputs.
- Write derived tables with explicit units in column names or metadata.

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
