# Output And Reproducibility

Use this reference for run folder design, output conventions, and metadata. For parameter sweeps, combine it with `parameter_sweep.md`.

## Recommended Run Layout

```text
runs/
  case_0001/
    params.json
    script.mx3
    run_record.json
    frame_manifest.json
    logs/
      mumax3.stdout.txt
      mumax3.stderr.txt
    script.out/
    notes.md
results/
  case_0001/
    metrics/
    arrays/
    figures/
    gif/
    product_manifest.json
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
- Versioned output and sampling profile, including quantities, cadence, critical times, and minimum observation windows.
- mumax3 binary/version, command, working directory, requested/resolved output directory, stdout/stderr paths, and return code.
- Repository ID plus repository-relative source/input paths and SHA256; absolute observed paths only for diagnostics.
- Initial-state physical role, preparation protocol, and allowed downstream protocol.
- Separate execution, output-completeness, analysis-freshness, automatic-gate, and manual-classification state.

## Output Directory Contract

Make one launcher-owned output directory part of the case contract.

- Prefer passing mumax3 `-o <stage>.out` when the installed version supports it, and record the exact command and resolved path.
- Without `-o`, isolate the working directory and accept only the single candidate derived by the installed mumax3 version
  from the input script stem. A script named `stage.mx3` conventionally produces `stage.out`; do not look only for
  `stage.mx3.out` or guess among multiple directories.
- A zero mumax3 return code with no uniquely reconciled output directory is
  `execution_succeeded_reconciliation_required`. Do not convert it to ordinary failure or automatically rerun it.
- `-f` can clean an existing output directory; never add it to resumable automation unless explicit overwrite policy,
  provenance checks, and user intent permit removal of the old output.

The run record stores the requested path, discovered candidates, resolved path, return code, command, working directory, and
reconciliation finding. Output discovery is not a scientific-completeness check.

## mumax3 Output Conventions

- `Save(quantity)` writes a space-dependent quantity with an automatic name.
- `SaveAs(quantity, "name.ovf")` writes a space-dependent quantity with a chosen name.
- `AutoSave(quantity, period)` writes snapshots periodically.
- `TableAdd(quantity)` adds table columns; `TableAutoSave(period)` schedules table output.
- `TableSave()` appends a table row immediately.
- `Snapshot`/`SnapshotAs` writes images when image output is desired.

For scripts with region logic, `SaveAs(regions, "regions.ovf")` is a useful debug artifact.

## Timeline And Completion Contract

Define expected output from the versioned profile before launch. Reconcile at least:

- expected and observed frame identities/times;
- first, last, and protocol-critical frames;
- monotonic physical time;
- missing and duplicate frames;
- maximum observed interval and any allowed gap policy;
- expected tables, named checkpoints, and final explicit saves.

Report `complete`, `complete_with_gaps`, `incomplete`, or `reconciliation_required` with the evidence. A percentage of expected
frame count is not enough to declare completeness, because missing switch or endpoint frames may be scientifically decisive.
Keep the original frame manifest content-addressed and immutable; later availability/retention records refer to it rather than
rewriting it.

## Content Identity And Source Signatures

Persist file identity as repository ID, repository-relative path, and SHA256. Logical, physical, and observed absolute paths
help diagnose relocation but do not enter scientific identity. Modification time may shortlist files for hashing; it cannot
make an analysis fresh or stale by itself.

Bind at least the case configuration, rendered script/template, mumax3 binary/version, every reused input, frame manifest,
analysis configuration/code, plot profile, and derived product manifest. Keep simulation, analysis, and plot source signatures
separate, with shared dependencies explicitly listed.

SHA256 proves which bytes were used, not whether they were physically valid. A reused initial state also needs a compatible
role, preparation field/protocol, material/geometry identity, source task, and allowed downstream protocol.

## File Naming

- Include key scanned parameters in case IDs or folder names, not every output filename.
- Prefer stable filenames inside a case folder: `m_initial.ovf`, `m_relaxed.ovf`, `m_final.ovf`, `regions.ovf`.
- Avoid fixed filenames across a sweep unless each run has an isolated working directory.

## Output And Sampling Profiles

Use a versioned output profile per scientific role and protocol. It declares:

- quantities and vector dimensions to save in each phase;
- autosave/table cadence plus explicit critical saves;
- protocol duration, minimum observation window, critical times, and expected frame count;
- output format and a conservative bytes-per-frame estimate;
- downstream decision/analysis requirements and retention class.

Cadence is a sampling contract, not a universal number. Periodic or lock-in analysis must state required samples per cycle,
phase coverage, and minimum cycles/windows; same-phase once-per-cycle samples cannot recover a complex response.

Before launch, estimate `estimated_new`, `peak`, and `free_after_run` from grid, vector dimension, format, frame plan, remaining
cases, tables, derived products, concurrent writers, and temporary force/archive copies. Margin is profile/task policy. Do not
reuse one fixed free-space threshold or one peak multiplier across different protocols.

## Analysis Products And Plot Profiles

Represent postprocessing as a dependency graph with independently signed nodes such as metrics, arrays, figures, GIF,
summary, manifest, and validation. Publish new products atomically and commit the product manifest last, so interruption leaves
the previous complete product set authoritative.

Expose product-scoped rebuilds such as `--only`, `--changed`, and `--validate` where appropriate. A layout-, label-, or
overlay-only cache hit should perform zero OVF reads; record read calls and bytes when measuring this property.

A purpose-specific plot profile declares required and optional quantities, display order, units, normalization, shared scale,
colormap, overlays, and its signature. At minimum, distinguish presentation/position plots from orientation, topology, and
other decision evidence. Do not impose one fixed component order on every plot. An unknown decision purpose fails closed until
all decision-required quantities are present; an unknown presentation purpose asks the user to choose.

## Logs And Postprocessing

- Capture stdout and stderr from the native `mumax3` process.
- Store generated scripts next to parameters, not only templates.
- Keep analysis scripts separate from raw simulation outputs.
- Write derived tables with explicit units in column names or metadata.

## Retention And Safe Release

Classify raw and derived objects at least as reference, precious, evidence, or scratch. Pin initial states, ancestor
checkpoints, named endpoints, decision windows, manual evidence, GIF/source frames, and documented references unless a
versioned profile proves a different safe set.

A retention plan is read-only and content-addressed. It lists the original frame-manifest SHA256, candidate relative paths and
SHA256, byte counts, reference closure, keep/release reasons, lost reanalysis capability, archive target, recovery procedure,
and plan expiration conditions. Derive the keep set from output, decision, and plot profiles rather than a universal
"first frames plus periodic sample" rule.

Never rewrite the original frame manifest after releasing frames. Write separate retention/release manifests and an explicit
raw-frame availability state. Before deleting a source, reject active writers, copy/archive to the approved destination,
verify every SHA256 (and archive integrity where applicable), test the recovery path, and obtain confirmation for the exact
plan SHA and file list. Any failure preserves the source. Unknown references fail closed to pinned; probability is not a safe
garbage-collection rule.

Treat backup availability as necessary but not sufficient for release. Make a dataset eligible only after it is explicitly
`sealed_for_retention`: simulation, analysis, profiles, reference closure, and manual-evidence inputs are stable and no related
writer is active. Reopening the dataset, adding a reference, or changing a profile/classification expires prior coverage and
retention plans.

Identify a mounted cold volume by a persistent volume/backup-set identity, physical-device evidence, and an immutable snapshot
manifest SHA256. A drive letter, mount path, matching filename, size, or modification time is not backup identity. Compare
ordinary files by repository-relative path plus SHA256. For archives, distinguish byte-exact container recovery from expanded
member equivalence; the latter requires a complete normalized member set and per-member SHA256 and cannot promise identical
archive bytes.

Keep copy-only synchronization and source release as separate plans, transactions, locks, and user confirmations. Publish
backup snapshots immutably; never propagate a source deletion into the backup as part of prune. Backup-side garbage collection
needs its own content-addressed plan and authorization. If the source release leaves one physical copy, report that it is now
the sole archive rather than a redundant backup; require policy or exact-plan acceptance appropriate to the retention class.

Re-discover the bound volume and re-hash every release candidate at apply time. A hash cache may use size, mtime, or stable file
IDs only to shortlist routine scrub work, never as deletion proof. Run periodic content scrubs, mark damaged or incomplete
snapshots degraded, and exclude them from recovery coverage. Preserve compact snapshot roots, transfer/recovery audits, release
manifests, and authorization records independently from the large cold volume.

Limit each destructive plan by declared dataset, file count, and bytes. Budget enough independent temporary space for the
release batch, archive expansion, recovery copy, journal, and protocol margin; reduce the batch instead of replacing complete
recovery validation with sampling. Reject case-folding, Unicode-normalization, reserved-name, path-traversal, duplicate-member,
and link/reparse-point ambiguities rather than silently renaming objects.

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
