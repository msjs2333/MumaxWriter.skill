# Parameter Sweep Guidance

Choose native MuMax3 loops for sequential parameter steps, such as a hysteresis sweep that continues from the previous state. External tools such as Python are useful for independent cases, parallel execution, fitting, and plotting; they are not required for every scan.

## Plan And Execute

Define the parameters, units, case-selection rule, and expected analysis before generating a sweep. Begin with a small pilot
when it can expose rendering, resource, or interpretation problems cheaply. Render each case's `.mx3` script from its chosen
parameters when generating independent cases, capture useful engine logs, and make rerun behavior explicit rather than silently overwriting completed outputs.

Use the case record and output/sampling guidance in `output_and_reproducibility.md` instead of maintaining a second required
layout or metadata list. Isolate cases so their scripts and MuMax3 output directories cannot collide.

## Analyze For The Structure And Question

Select measurements that match both the simulated structure and the scientific question. Crop absorbers or source near fields
when they would bias a propagation or focusing metric, and retain the static reference and time window needed to interpret
dynamic quantities.

Examples include wall position for domain walls; core or texture trajectories for vortices and skyrmions; reference-relative
dynamic components, spectra, mode maps, or propagation metrics for FMR and spin waves; and magnetization curves for
hysteresis. These are options, not a mandatory evidence checklist. Save derived values with units and enough input provenance
to reproduce the comparison.

## Python Tools

`numpy`, `pandas`, `scipy`, and `matplotlib` cover many sweeps. `scikit-image` can help with contours; Ubermag,
`discretisedfield`, and `micromagneticdata` can be useful for notebooks and field data. Choose libraries for the analysis
need without rewriting an established MuMax3 workflow unnecessarily.
