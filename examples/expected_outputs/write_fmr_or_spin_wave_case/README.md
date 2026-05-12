# Expected Output: Spin-Wave Dynamics Case

This expected output chooses the spin-wave path from `examples/prompts/write_fmr_or_spin_wave_case.md`.

Files:

- `params.json`: case metadata for the static and dynamic stages.
- `script.mx3`: compact original mumax3 script with static relaxation followed by a localized sinusoidal excitation.

Manual checks:

```powershell
python skills\mumax3\scripts\check_mx3_static.py examples\expected_outputs\write_fmr_or_spin_wave_case\script.mx3
mumax3 -vet examples\expected_outputs\write_fmr_or_spin_wave_case\script.mx3
```

The table period is `5e-12`, giving a 200 GHz sample rate, which resolves a 5 GHz drive under the Nyquist criterion. Python postprocessing would consume `table.txt`, autosaved magnetization snapshots, and the final OVF state.

