# Release Validation

Collector regressions use synthetic cases to distinguish missing/corrupt metadata and comparable/unverified analysis signatures. They do not require research outputs or validate scientific classification. Reference removal is checked through current links, not fixed document names.

Run the release checks from the repository root.  The default remains the full
release candidate check:

```powershell
python tests\validate_release.py
```

For a documentation-only change, use:

```powershell
python tests\validate_release.py --scope docs
```

For helper-script changes, use:

```powershell
python tests\validate_release.py --scope helpers
```

`docs` checks skill metadata, local reference links, and literal local home paths in Git-tracked maintained files (or explicit maintained roots when Git is unavailable), including the top-level English, Chinese, and Japanese READMEs. `helpers` additionally syntax-checks helper scripts in memory and runs the helper regression suite once. `full` additionally validates templates, expected-output static warnings, and `mumax3 -vet`. If `mumax3` is not on `PATH`, the full check reports that `-vet` was skipped; that result is not a full acceptance.


## Workflow validation evidence

CPU regressions change generator parameters, check all six generated cases against their JSON and tracked representative, protect existing case files, and test analysis against synthetic valid/corrupt signals. Synthetic reference comparisons do not establish physics. The full check vets all ten concrete example scripts; ordinary MuMax3 `-vet` initializes CUDA and compiles scripts, without evaluating simulation or input-file loads.

The three installed tutorial scripts were also executed with MuMax3 3.12 (commit `6e5c98bb`, CUDA 12.9) on an NVIDIA RTX 5060 Laptop GPU on 2026-10-31. Each execution had a 60-second timeout and a fresh output directory. All exited successfully and their native tables passed the tutorial analyzer:

| Case | Engine time | Observable | Scope |
| --- | --- | --- | --- |
| Continuous hysteresis | 12.9 s | Switching at -0.114994 / +0.114994 T; analytic magnitude 0.117576 T, tolerance 0.02 T | Macrospin branch ordering and switching |
| SP4 field 1 | 26.8 s | First `mx=0` at 0.138675 ns; sampled snapshot at 0.139 ns | Output/reversal only; independent reference comparison not run |
| Pulsed FMR | 16.6 s | Peak 2.798601 GHz; analytic 2.800051 GHz, tolerance 0.2 GHz | Isotropic macrospin frequency |

No mesh/timestep convergence study or independent SP4 solution comparison was performed. Snapshot checks in the analyzer inspect existence and OVF header, not the complete spatial field. The guides define further checks; these results do not claim those checks were run.
