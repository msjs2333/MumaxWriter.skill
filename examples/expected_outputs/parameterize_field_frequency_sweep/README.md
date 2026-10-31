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

## Parameter changes and execution

Edit `BASE_PARAMS`, `FIELDS_MT` and `FREQUENCIES_GHZ`, then run the generator with `--output new_cases`. Geometry, all mesh axes, material, excitation amplitude/width and time settings are rendered from the same dictionary written to each `params.json`. The source spans the chosen number of x cells and all y/z cells; keep that width within the mesh. The helper refuses an existing case directory.

From each generated case directory, run `mumax3 -http= relax.mx3` and then `mumax3 -http= dynamics.mx3`. The second stage reads `relax.out/m_relaxed.ovf`; changing the output directory requires changing that input path too. Check the relaxed state before interpreting dynamics. This example defines independent field/frequency cases, not a hysteresis trajectory: every case starts its own relaxation. For a state-continuing field loop use the [installed hysteresis tutorial](../../../skills/mumax3/examples/hysteresis/README.md).
