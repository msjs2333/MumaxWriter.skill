# Example And Evaluation Catalog

This catalog maps repository-level evaluation prompts to expected outputs and external inspiration sources. External projects are used for task coverage and validation expectations only; the repository examples are original unless a file explicitly says otherwise.

## Source Inspiration

- mumax3 official examples and API: compact runnable `.mx3` scripts, standard problems, hysteresis-style sweeps, output scheduling, and official identifier checks.
- Fidimag documentation: task families such as domain walls, skyrmions, FMR, spin waves, and postprocessing.
- MicroMagnetic.jl documentation: vortex dynamics, skyrmions, standard problems, and dynamic susceptibility as coverage targets.
- Ubermag documentation: separation of model definition, backend execution, and data analysis.
- OOMMF user guide: reproducibility, problem specification discipline, OVF/table-oriented output, and batch workflows.

## Coverage Map

| Structure or workflow family | Prompt | Expected output | Notes |
| --- | --- | --- | --- |
| Minimal thin-film relaxation | [`write_minimal_relax.md`](../prompts/write_minimal_relax.md) | [`write_minimal_relax/`](../expected_outputs/write_minimal_relax/) | Core smoke test for script organization, outputs, and metadata. |
| Broken syntax/API review | [`review_broken_script.md`](../prompts/review_broken_script.md) | [`review_broken_script/`](../expected_outputs/review_broken_script/) | Evaluates Go/mumax3 boundary guardrails and corrected script quality. |
| Field/frequency sweep | [`parameterize_field_frequency_sweep.md`](../prompts/parameterize_field_frequency_sweep.md) | [`parameterize_field_frequency_sweep/`](../expected_outputs/parameterize_field_frequency_sweep/) | Evaluates Python orchestration, case metadata, and dynamic-field syntax. |
| Skyrmion with DMI | [`write_skyrmion_relaxation.md`](../prompts/write_skyrmion_relaxation.md) | [`write_skyrmion_relaxation/`](../expected_outputs/write_skyrmion_relaxation/) | Evaluates DMI setup, skyrmion seed, relaxation diagnostics, and caution around material assumptions. |
| Vortex relaxation | [`write_vortex_relaxation.md`](../prompts/write_vortex_relaxation.md) | [`write_vortex_relaxation/`](../expected_outputs/write_vortex_relaxation/) | Evaluates disk geometry, vortex initialization, and output for later dynamics analysis. |
| FMR or spin wave dynamics | [`write_fmr_or_spin_wave_case.md`](../prompts/write_fmr_or_spin_wave_case.md) | [`write_fmr_or_spin_wave_case/`](../expected_outputs/write_fmr_or_spin_wave_case/) | Evaluates relaxed-state staging, inline time-dependent excitation, output cadence, and Python-side analysis expectations. |

## Template Parameter Examples

Tracked parameter examples for runtime templates live under [`../template_params/`](../template_params/):

- `minimal_relax.params.example.json`
- `thin_film_with_region.params.example.json`
- `local_ac_field.params.example.json`

## Gap List For Later Phases

- Hysteresis or Standard Problem style field sweep.
- Domain wall relaxation and propagation.
- Periodic-boundary thin film.
- Region-based material heterostructure beyond runtime templates.
- Absorbing-boundary spin-wave guide.
- Geometry and shape-composition cases.
- Grains/disorder, moving-window dynamics, STT/SOT, SAF/RKKY multilayers, and MFM outputs.
