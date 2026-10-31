# Release Notes: v0.3.0

Release date: 2026-10-31

## Changes

- Fix the field/frequency generator so geometry, mesh, material, drive and sampling parameters actually determine both generated scripts and agree with `params.json`. The excitation covers all z layers; generation refuses existing case directories.
- Include continuous hysteresis, Standard Problem 4 field-1 reversal and pulsed macrospin FMR teaching workflows in the installed skill. Each has runnable input, output contracts, observable extraction, references, acceptance limits and parameter-change guidance. Independent evaluation prompts remain outside the installed skill.
- Use one consistent rule for scans: native state continuation for hysteresis, independent preparation and external orchestration for independent cases. The main skill adds only a short route to the detailed guides.
- Remove obsolete maintenance audits containing private local paths and research-template names. Update the English, Chinese and Japanese READMEs and document the optional case-status collector's boundaries.

## Compatibility

The skill remains at `skills/mumax3/` and targets MuMax3 `.mx3`, not MuMax+. Existing templates, installation guidance, license and third-party sources remain. Installing a skill does not install an engine or authorize system changes.

The optional collector retains its CSV columns and generic signature fields, but no longer interprets stage-numbered signature or `h0_sha256` aliases. Map legacy records explicitly to the documented [generic schema](../skills/mumax3/references/case_status.md). The sweep generator now rejects an existing case directory instead of overwriting files.

## Validation and limits

Local validation passed 18 CPU regressions, all ten concrete scripts through real MuMax3 `-vet`, and three rendered templates through `-vet`. Skill metadata, local documentation links and installable package contents were also checked. These are local checks; the repository has no configured CI workflow. Synthetic analysis tests and compilation do not establish physical correctness.

The three new tutorials also completed bounded GPU runs with MuMax3 3.12 (commit `6e5c98bb`, CUDA 12.9) on an RTX 5060 Laptop GPU, and their native tables passed the tutorial analyzer:

| Case | Observed result | Comparison or scope |
| --- | --- | --- |
| Continuous hysteresis | Switching at approximately -0.114994 / +0.114994 T | Analytic magnitude 0.117576 T, within the declared 0.02 T tolerance |
| Pulsed macrospin FMR | Peak 2.798601 GHz | Analytic 2.800051 GHz, within the declared 0.2 GHz tolerance |
| SP4 field 1 | First `mx=0` at 0.138675 ns; sampled snapshot at 0.139 ns | Output and reversal checks only |

SP4 independent-reference comparison and mesh/timestep convergence studies were not performed. OVF checks establish file presence and header, not the correctness of the full spatial field. The tutorials define further acceptance checks without claiming they were run. See [validation details](../tests/README.md).
