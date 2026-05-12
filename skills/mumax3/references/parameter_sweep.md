# Parameter Sweep Guidance

Use Python for case generation, execution, analysis, fitting, and plotting. Use mumax3 only for the simulation itself.

## Recommended Case Layout

```text
runs/
  case_0001_field_010mT_freq_010GHz/
    params.json
    relax.mx3
    dynamics.mx3
    logs/
    out/
results/
  metrics/
  tables/
  figures/
```

## Minimum Metadata

Each case should record:

- `case_id`
- geometry parameters, for example `length_nm`, `width_nm`, feature sizes, and source position
- material parameters, for example `Msat`, `Aex`, anisotropy, DMI, damping, and region assignments
- field and excitation parameters, for example `B_mT`, `frequency_GHz`, `amplitude_mT`, and run time
- mesh and cell size
- simulation time and time step
- generated script paths
- output paths
- status and error message if failed

## Execution Strategy

1. Generate a small pilot grid first.
2. Render `.mx3` scripts from templates.
3. Run `mumax3` with subprocess calls.
4. Capture stdout/stderr logs.
5. Mark case status in a manifest file.
6. Avoid overwriting completed cases unless explicitly requested.

## Analysis Strategy

Use analysis steps that match the simulated structure. Keep the workflow explicit and case-specific.

Common options:

- Load final or time-resolved magnetization from OVF output.
- Crop boundary or absorber regions before extracting metrics.
- Compute scalar summaries such as average magnetization, maximum angle, energy terms, switching field, resonance peak, mode amplitude, or texture position.
- Save extracted quantities as CSV or Parquet.

Structure-specific examples:

- Domain walls: extract a wall centerline using a zero crossing or peak transverse component.
- Vortices/skyrmions: track core or topological texture position over time.
- FMR/spin waves: compute dynamic components relative to a static reference, spectra, spatial mode maps, and propagation metrics.
- Hysteresis: extract magnetization curves, coercive fields, and remanence.

## Recommended Python Libraries

- `numpy` for arrays.
- `pandas` for manifests and tabular results.
- `scipy` for fitting and optimization.
- `matplotlib` for figures.
- `scikit-image` for contours if using image-like field slices.
- `ubermag`/`discretisedfield`/`micromagneticdata` may help with field data, but native mumax3 execution should remain the default backend.

## Technology Choice

Default: Python + native mumax3.

Rationale:

- Keeps current `.mx3` scripts usable.
- Avoids loss of mumax3-specific API coverage.
- Python has stronger tools for fitting, plotting, and data management.

Use Ubermag/mumax3c selectively for notebooks and data handling. Do not rewrite the whole workflow into Ubermag unless a pilot demonstrates it supports all required mumax3 features.
