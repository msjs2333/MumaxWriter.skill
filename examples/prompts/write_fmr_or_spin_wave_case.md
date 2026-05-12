# Prompt: Write An FMR Or Spin-Wave Dynamics Case

Use the `mumax3` skill to write a compact dynamic script for either FMR or spin-wave propagation in a generic thin film.

Choose one path and state the choice:

- FMR: relax a uniform thin film under a static bias field, then apply a small uniform sinusoidal transverse field.
- Spin wave: relax a thin strip, then apply a small localized sinusoidal source field near one end.

Requirements:

- Build and save a relaxed static state before dynamics.
- Use a small excitation amplitude, for example 0.5 mT to 1 mT.
- Keep any `t`-dependent expression inline in `B_ext` or `B_ext.Add(...)`.
- Save table output at an interval that can resolve the chosen frequency.
- Save magnetization snapshots for postprocessing.
- Include a short note on Nyquist/time-resolution expectations and which outputs a Python analysis stage would consume.
- Do not use ordinary Go imports or custom functions.
