# Standard Problem 4: reversal and numerical comparison

This case implements **field 1** of [NIST muMAG Standard Problem 4](https://www.ctcms.nist.gov/~rdm/std4/spec4.html): a 500 x 125 x 3 nm Permalloy rectangle, `Msat=800 kA/m`, `Aex=13 pJ/m`, no crystalline anisotropy, damping 0.02, and applied flux density `(-24.6, 4.3, 0) mT`. It uses the compact S-state preparation in the [official MuMax3 example](https://mumax.github.io/examples.html): zero-field relaxation from `Uniform(1,0.1,0)`. Inspect `m_initial.ovf` to confirm the S-state; this is not a reproduction of the full saturation-and-ramp preparation suggested by NIST.

From this folder, with a fresh output name:

```text
mumax3 -http= -o sp4.out script.mx3
python ../../scripts/analyze_tutorial.py sp4 sp4.out
```

## Output contract and comparison

The self-contained input uses a 128 x 32 x 1 mesh and the engine default `GammaLL` (record the engine version when comparing trajectories). Fixed-step RK4 uses ten 0.1 ps integration steps per output sample. It records normalized average `mx,my,mz` every 1 ps from zero to 1 ns (1001 rows), applied field and energy in `table.txt`. It saves `m_initial.ovf`, `m_final.ovf`, and `m_crossing.ovf` at the first sampled `mx <= 0`, at most one sample after the true first crossing. Inspect the crossing field map to assess the reversal mechanism; a table alone cannot do this.

The analysis emits `analysis/curve.csv` (`t_s,mx,my,mz`) and `summary.json` with an interpolated first-crossing time, sampled snapshot time and table hash. It fails on incomplete/irregular time coverage, non-finite data, missing reversal or snapshot. **Passing these checks establishes output/reversal behavior only**, not agreement with SP4 reference solutions or equilibrium at the final time.

For quantitative comparison, obtain a documented field-1 solution from the [NIST solution collection](https://www.ctcms.nist.gov/~rdm/std4/results.html), convert its normalized components and time in seconds to `t_s,mx,my,mz` CSV, and preserve its source, mesh and preparation details. Then:

```text
python ../../scripts/analyze_tutorial.py sp4 sp4.out --reference-csv reference.csv --tolerance 0.03
```

The tool linearly interpolates a reference covering the whole interval and checks maximum absolute component error. `0.03` is an explicit tutorial comparison threshold, not an official NIST tolerance. It records the reference hash. Without that input, the summary explicitly says `reference_comparison: not_run`. A synthetic curve used in unit tests is not a benchmark reference.

## Modify and verify

- For mesh convergence, change `nx,ny` to `256,64` at fixed physical dimensions, and consider thickness resolution separately; compare both trajectories and crossing maps. A refinement that changes the reversal mechanism needs investigation even if average curves look close. Do not label the default mesh converged without this comparison.
- For integration convergence, halve `FixDt` and double the `Steps(10)` count per sample; `MaxErr` does not control a fixed timestep. For output-time resolution, halve `samplePeriod` while doubling `nSamples` to keep the observation window. Extend the window if equilibrium has not been reached.
- Field 2 is `(-35.5,-6.3,0) mT`; use a new independent run from the same prepared S-state, never the field-1 final state. Compare against a field-2 reference. Changing material or geometry creates a different problem and must not retain the SP4 benchmark label.
