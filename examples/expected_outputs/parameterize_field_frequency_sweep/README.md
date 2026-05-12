# Expected Output: Field/Frequency Sweep

This expected output illustrates the expected structure for `examples/prompts/parameterize_field_frequency_sweep.md`. The workflow uses Python for case generation and native mumax3 for simulation.

Expected response shape:

- Explain why Python owns the sweep and mumax3 owns each simulation.
- Generate one case directory per field/frequency pair.
- Write `params.json`, `relax.mx3`, `dynamics.mx3`, and `logs/` under each case.
- Keep static field, excitation frequency, and output paths visible in metadata.

Files:

- `generate_field_frequency_sweep.py`: sample generator for six cases.
- `case_0001_field_m005mT_freq_005GHz/`: representative generated case.

Manual checks:

- `python skills/mumax3/scripts/check_mx3_static.py examples/expected_outputs/parameterize_field_frequency_sweep/case_0001_field_m005mT_freq_005GHz/relax.mx3 examples/expected_outputs/parameterize_field_frequency_sweep/case_0001_field_m005mT_freq_005GHz/dynamics.mx3`
- If mumax3 is installed, run `mumax3 -vet relax.mx3` and `mumax3 -vet dynamics.mx3` inside a generated case directory.
