# Prompt: Parameterize A Field/Frequency Sweep

Use the `mumax3` skill to design a small field/frequency sweep workflow around native mumax3 scripts.

Scenario:

- Generic thin film, 768 nm x 192 nm x 2 nm.
- Mesh: 256 x 64 x 1.
- Material: `Msat = 800e3`, `Aex = 13e-12`, `alpha = 0.01`.
- Static field values: -5 mT, 0 mT, +5 mT along +x.
- Excitation frequencies: 5 GHz and 10 GHz.
- Excitation amplitude: 1 mT along +y, localized to the first 8 x-cells.
- Relax each case before dynamics.
- Run dynamics for 2 ns.

Requirements:

- Use Python to generate one case directory per field/frequency pair.
- Each case must contain `params.json`, `relax.mx3`, `dynamics.mx3`, `logs/`, and an output location.
- The generated `.mx3` scripts must keep mesh/material/output sections explicit.
- `dynamics.mx3` must load the relaxed state from the corresponding `relax.mx3` output.
- Save time-resolved table output and magnetization snapshots.
- Do not hard-code all cases manually inside one `.mx3` file.
- Include enough metadata to reproduce or audit each case.

Evaluation focus:

- The workflow separates Python orchestration from mumax3 simulation logic.
- Case names include key scanned parameters without relying on global output filenames.
- The dynamic excitation keeps the `sin(2*pi*f*t)` expression in the mumax3 assignment.
