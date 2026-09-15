# Release Validation

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

`docs` checks skill metadata, local reference links, and sensitive terms in Git-tracked maintained files (or explicit maintained roots when Git is unavailable), including the top-level English, Chinese, and Japanese READMEs. `helpers` additionally syntax-checks helper scripts in memory and runs the helper regression suite once. `full` additionally validates templates, expected-output static warnings, and `mumax3 -vet`. If `mumax3` is not on `PATH`, the full check reports that `-vet` was skipped; that result is not a full acceptance.

