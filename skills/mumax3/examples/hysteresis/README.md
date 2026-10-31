# Continuous hysteresis: state history matters

This one-cell, zero-temperature uniaxial macrospin teaches continuation through metastable states. Demagnetization is disabled; `Ku1=50 kJ/m3`, `Msat=800 kA/m`, easy axis x give `B_k=2 Ku1/Msat=0.125 T`. A fixed 1 mT transverse field avoids exactly antiparallel zero torque. Sweep x from +0.2 to -0.2 T and back in 10 mT steps, carrying `m` between steps. Reinitializing `m` inside the loop changes the experiment.

The [official MuMax3 hysteresis example](https://mumax.github.io/examples.html#Hysteresis) illustrates state continuation. This macrospin uses `Relax()` at every field step: energy minimization alone can stall near an unstable stationary state during reversal. `Minimize()` remains useful for neighboring states when its convergence is checked. This is an independently written macrospin model, not that example's film or its numerical reference curve. API units and anisotropy are documented in the [official API](https://mumax.github.io/api.html).

From this folder, with a fresh output name:

```text
mumax3 -http= -o hysteresis.out script.mx3
python ../../scripts/analyze_tutorial.py hysteresis hysteresis.out
```

The engine needs compatible NVIDIA/CUDA support. An existing output directory should be retained; use a new `-o` path rather than adding a force-clean option.

## Output and acceptance

- Input: self-contained `script.mx3`; no external checkpoint or data file.
- Output: `m_initial.ovf`, `m_final.ovf`, and 81 rows in `table.txt`, with normalized magnetization, actual applied field, branch identifier and model constants. `t` need not increase during minimization: the independent variable is field and branch.
- Analysis: `analysis/curve.csv` preserves acquisition order; `summary.json` records both linearly interpolated `mx=0` crossing fields, the comparison value and the input-table hash.
- For energy density `E=-Ku1 mx^2-Msat(Bx mx+By my)`, loss of a metastable minimum yields the Stoner-Wohlfarth astroid. With fixed `By`, the predicted switching magnitude is `B_k [1-(|By|/B_k)^(2/3)]^(3/2)`, about 0.1176 T here. This analytic value is derived for this macrospin energy, not a fitted reference from the simulation.
- The checker requires complete ordered branches, saturation at the extremes, opposite switching signs, and each crossing within two field steps of that value. Missing reversal, truncated branches or non-finite data fail. These are tutorial tolerances, not universal accuracy targets.

## Modify and verify

Change `fieldLimit` or `nIntervals` at the top; the script derives `fieldStep` and records it in the table. Halve the step and compare switching estimates (the uncertainty should shrink with the bracket). Change `Ku1`/`Msat` and retain `fieldLimit > B_k > |By| > 0`; the analysis uses the recorded `B_k`. Keep the transverse field small. Enabling demagnetization, adding cells or changing anisotropy invalidates this analytic contract and requires a new reference model. Independent parameter grids should instead restart each case from its specified preparation state.
