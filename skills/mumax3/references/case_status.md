# Optional case-status collector

Use `scripts/collect_case_status.py` only for directories containing `params.json` or a top-level `.mx3`, with nested `*.out` outputs. It reports file presence and recorded metadata; it neither executes MuMax3 nor proves completion, convergence or physical validity. Existing project status tools take precedence.

The collector accepts these optional records; none is required for ordinary scripts:

| Record | Fields interpreted |
| --- | --- |
| `params.json` | `case_id`, `status`, `error_message`; `configuration_signature` / `config_signature` / `case_signature`; `checkpoint_sha256` / `static_input_sha256` / `input_sha256`; `dynamic_signature` |
| `run_record.json` | `status` |
| `analysis_record.json` | `analysis_signature` / `signature`, `dynamic_signature` |
| `manual_review.json` | `status` / `classification`, `dynamic_signature`, `analysis_signature` |
| `manifest.json` or `case_manifest.json` | Presence and JSON validity only, at case or selected root level |

`--result-root` places analysis/review lookup under a parallel case tree; otherwise those records live in each case directory. Missing optional records are allowed; malformed ones are reported. Unrelated fields are ignored. Older stage-numbered signatures are no longer aliases: map them explicitly to the appropriate generic field when adopting this collector. Do not assume a stage number has the same meaning across projects.

`analysis_fresh` means comparable recorded dynamic signatures agree, not that data hashes were recomputed or the analysis is correct. No comparable signature means `analysis_unverified`. `derived_status` remains separate from recorded run/review status. A plain `.out` directory without source/params is not discovered. Custom output paths require a project-specific adapter rather than a mandatory new directory layout.
