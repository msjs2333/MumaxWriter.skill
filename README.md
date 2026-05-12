# MumaxWriter.skill

[English](README.md) | [中文](README.zh-CN.md) | [日本語](README.ja.md)

A Codex skill project for helping AI agents write, review, parameterize, and maintain mumax3 `.mx3` simulation code.

This repository contains a cleaned generic `mumax3` skill. Project-specific research material has been removed from the public snapshot; the installed skill path is kept generic for broader reuse.

## Repository Layout

```text
MumaxWriter.skill/
  README.md
  README.zh-CN.md
  README.ja.md
  examples/
    prompts/
    expected_outputs/
    catalog/
    manual_evaluation_checklist.md
  skills/
    mumax3/
      SKILL.md
      agents/
        openai.yaml
      assets/
        templates/
          minimal_relax.mx3.template
          thin_film_with_region.mx3.template
          local_ac_field.mx3.template
      references/
        language_subset.md
        anti_patterns.md
        api_index.md
        api_patterns.md
        api_full.md
        examples.md
        structures.md
        parameter_sweep.md
        output_and_reproducibility.md
        compatibility_notes.md
      scripts/
        check_mx3_static.py
        render_template.py
        collect_case_status.py
  docs/
    release_notes_v0.1.0.md
    third_party_sources.md
    troubleshooting.md
  tests/
    validate_release.py
```

## What The Skill Does

The `mumax3` skill helps an AI agent:

- Write valid mumax3 `.mx3` scripts instead of full Go code.
- Review scripts for common mumax3 syntax and API mistakes.
- Parameterize mumax3 scripts for batch simulations.
- Structure scripts around mesh, geometry, materials, initial states, fields, damping, output, and run stages.
- Decide when to use Python to generate scripts, run mumax3, organize outputs, fit results, and plot figures.

## Installation For Local Use

Copy the skill folder into your Codex skills directory:

```powershell
Copy-Item -Recurse .\skills\mumax3 C:\Users\<you>\.codex\skills\mumax3
```

Then invoke it explicitly with:

```text
Use $mumax3 to write or review this mumax3 script.
```

## Quick Example

```text
Use $mumax3 to write a minimal mumax3 thin-film relaxation script with SI units, table output, and a final OVF save.
```

For parameter sweeps, ask the skill to keep Python responsible for case generation, metadata, logs, and postprocessing while keeping each simulation in native mumax3 `.mx3` scripts.

## Local Validation

Run local validation from the repository root:

```powershell
python tests\validate_release.py
```

The validator uses only the Python standard library. It compiles helper scripts, checks template parameter examples, runs conservative static checks on expected-output `.mx3` files, and runs `mumax3 -vet` when mumax3 is available on `PATH`.

## Current Status

This is the `v0.1.0` public snapshot. It includes generic mumax3 templates, expanded API pattern references, deterministic helper scripts, and a repository-level evaluation surface under `examples/`.

The examples and static checks are intended for skill validation and script hygiene. They do not prove physical correctness, numerical convergence, or publication readiness.

## Future Roadmap

Planned directions for later releases:

- Evaluate optional Python-side data handling workflows, including possible use of the Ubermag ecosystem and related analysis tools.
- Add mumax+ compatibility, with the long-term direction of making mumax+ the primary target while keeping mumax3 support.
- Provide assisted migration workflows from existing mumax3 `.mx3` scripts to mumax+, including API mapping notes, behavior differences, and validation checklists.
- Expand postprocessing examples for OVF/table output, spectra, mode maps, texture tracking, and sweep summaries.

## Documentation

- [Release notes](docs/release_notes_v0.1.0.md): scope, compatibility, validation status, and known limitations.
- [Example catalog](examples/catalog/README.md): prompts, expected outputs, and coverage map.
- [Third-party sources](docs/third_party_sources.md): external source and provenance notes.
- [Troubleshooting](docs/troubleshooting.md): common local validation and mumax3 issues.

## License

Licensed under the [Apache License 2.0](LICENSE).
