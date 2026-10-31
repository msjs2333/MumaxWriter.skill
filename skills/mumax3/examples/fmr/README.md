# Pulsed macrospin FMR: simulation to spectrum

This is an isotropic, single-cell frequency check, not a thin-film Kittel or propagating-wave model. Demagnetization and anisotropy are disabled. A 0.1 T z bias prepares `m=(0,0,1)`; a 1 mT transverse pulse lasts 50 ps, then the free response is recorded for 10 ns at 5 ps cadence. During observation, fixed-step RK4 takes ten 0.5 ps integration steps per saved sample. Damping is 0.01 and `GammaLL=1.7595e11 rad/(T s)`.

These model choices make the expected frequency analytically identifiable: the Gilbert equation for a uniform spin in constant field gives `f = GammaLL*B/(2*pi*(1+alpha^2))`, about 2.800 GHz. Use the [official MuMax3 API](https://mumax.github.io/api.html) for `GammaLL` units, dynamic fields, solver and demagnetization controls. The script and analysis are independently written; the analytic frequency is not estimated from a stored simulation fixture.

From this folder, with a fresh output name:

```text
mumax3 -http= -o fmr.out script.mx3
python ../../scripts/analyze_tutorial.py fmr fmr.out
```

## Output and acceptance

- Input: `script.mx3`, including all model/pulse/sampling constants.
- Output: initial/final magnetization OVFs and 2001 table rows **after the pulse**, from 50 ps to 10.05 ns. The table records the actual bias, damping, gyromagnetic ratio, pulse duration, sample interval and observation duration used by the script.
- Analysis: subtract the mean from `mx,my`, apply a Hann window, and calculate positive-frequency DFT power of both transverse components. `analysis/spectrum.csv` contains frequency in Hz and arbitrary power; `summary.json` records the measured peak, analytic value, bin width, tolerance and table hash. Plot the CSV to inspect the full spectrum, not only the largest bin.
- Missing/irregular samples, non-finite values, no transverse signal, insufficient cycles/samples or a peak beyond `max(2/T, 2% of f)` fail. The default bin width is approximately 0.1 GHz. This finite-window tolerance checks the frequency, not linewidth, absolute susceptibility or damping fits.

## Modify and verify

Change the bias and expect frequency to scale linearly; metadata and analytic comparison follow the script's table columns. Ensure at least ten cycles and ten samples per expected period. Change `nSamples` at fixed `samplePeriod` to improve frequency resolution; decreasing the sampling interval alone does not improve `1/T`. Halve pulse amplitude and verify an unchanged peak in the small-angle regime. The standard-library DFT is limited to 10000 saved rows (`nSamples <= 9999`, including the initial row); use an FFT implementation for larger studies.

Adding anisotropy, demagnetization or spatial modes changes the dispersion: replace this analytic test with the applicable model instead of loosening its tolerance. Noise or truncated traces used in unit tests validate the analysis code only. Engine execution, analytic agreement, timestep convergence and model applicability are separate claims.
