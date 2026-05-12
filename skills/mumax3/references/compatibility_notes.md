# Compatibility Notes

Use this reference when a task touches advanced mumax3 features, version-sensitive behavior, or Python workflow boundaries.

## Version Baseline

Runtime references in this skill target the official mumax3.12 API page. For older installations, confirm identifiers against the matching official API version before using advanced features.

Official API: <https://mumax.github.io/api.html>

## Verified Environment

On 2026-05-12, the Phase 2 smoke examples and release-candidate expected-output scripts were checked in a Windows environment with:

- `mumax3.exe` from `mumax3.12_windows_cuda12.9`.
- `mumax3 -vet` accepted the tracked expected-output scripts used by the release validation.
- Earlier short smoke runs produced expected `*.ovf`, `table.txt`, `log.txt`, and `references.bib` outputs.

mumax3 reported a non-fatal CPU-info probe error in this environment, while GPU execution and output generation succeeded.

## Script Language Boundary

mumax3 input syntax is Go-like and case-insensitive for API identifiers, but it is not a full Go runtime. Keep filesystem operations, JSON/CSV parsing, plotting, optimization loops, and multiprocessing in Python.

## Advanced Features

Check `api_full.md` and official docs before using:

- Spin currents and torque parameters.
- Moving window controls.
- Custom quantities and custom effective field terms.
- MFM helpers.
- Slicing/cropping helpers beyond simple `SaveAs`.
- Thermal noise and random seeding.
- Magnetoelastic or extension APIs.

## Python Ecosystem Boundary

Default backend should remain native mumax3 execution. Python can orchestrate cases and analyze results. Ubermag, `discretisedfield`, `micromagneticdata`, or notebooks may help with data handling, but do not rewrite a native mumax3 workflow into another framework unless the user asks or a pilot proves feature coverage.

## Output Formats

OVF output is the default field-data path for downstream analysis. Table output is appropriate for scalar or region-averaged time series. Confirm conversion tools and file readers before promising a specific postprocessing pipeline.
