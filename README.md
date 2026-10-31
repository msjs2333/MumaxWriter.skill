# MumaxWriter.skill

[English](README.md) | [中文](README.zh-CN.md) | [日本語](README.ja.md)

A Codex skill project for helping AI agents write, review, parameterize, and maintain mumax3 `.mx3` simulation code.

This repository contains a MuMax3 agent skill, reusable worked examples, and separate evaluation prompts.

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
        installation.md
        worked_workflows.md
        case_status.md
      examples/
        hysteresis/
        standard_problem4/
        fmr/
      scripts/
        check_mx3_static.py
        render_template.py
        collect_case_status.py
        analyze_tutorial.py
        sync_local_skill.py
  docs/
    release_notes_v0.1.0.md
    release_notes_v0.2.0.md
    release_notes_v0.3.0.md
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
- Keep concise principles for coordinating writers, traceable inputs, adequate evidence, and separation of automatic findings from human interpretation.
- Leave task schemas, background scheduling, storage/release protocols and agent assignments to project guidance; load technical references only for the requested work.

## Installation For Local Use

Copy the skill folder into your Codex skills directory:

```powershell
Copy-Item -Recurse .\skills\mumax3 C:\Users\<you>\.codex\skills\mumax3
```

Then invoke it explicitly with:

```text
Use $mumax3 to write or review this mumax3 script.
```

For an existing installation, preview and apply an exact, backed-up synchronization:

```powershell
python skills\mumax3\scripts\sync_local_skill.py --dry-run
python skills\mumax3\scripts\sync_local_skill.py --apply
```

The apply operation backs up the current `.../skills/mumax3` tree before replacing it and verifies source/target hashes.

## Install From Codex Marketplace

Install the standalone skill from GitHub with:

```powershell
npx codex-marketplace add msjs2333/MumaxWriter.skill/skills/mumax3 --skill
```

Then invoke it explicitly with:

```text
Use $mumax3 to write or review this mumax3 script.
```

MuMax3 simulator setup is separate from skill installation. See the short [installation guide](skills/mumax3/references/installation.md) for environment checks, official binaries, WSL/source-build options, and agent-assisted setup.

## Quick Example

```text
Use $mumax3 to write a minimal mumax3 thin-film relaxation script with SI units, table output, and a final OVF save.
```

Sequential scans can use native MuMax3 loops; independent cases may use Python orchestration. The optional `collect_case_status.py` expects a documented case layout, not arbitrary `.out` directories; see its `--help` and the output reference.

## Local Validation

Run local validation from the repository root:

```powershell
python tests\validate_release.py
# Documentation-only change:
python tests\validate_release.py --scope docs
# Helper change (includes helper tests once):
python tests\validate_release.py --scope helpers
```

The validator uses only the Python standard library. The default full scope checks metadata/links, maintained-file privacy terms, helper behavior, templates, static warnings and available engine vet. Missing engine checks are reported as skipped, not passed. Documentation scopes do not run simulations or helper suites. Exact prose and project-name blacklists are not test contracts.

## Current Status

The current release is `v0.3.0`. It includes installed [worked workflows](skills/mumax3/references/worked_workflows.md) for continuous hysteresis, field-1 Standard Problem 4 and pulsed macrospin FMR, with table analysis and explicit acceptance limits. Evaluation prompts remain under `examples/prompts/`; copying `skills/mumax3/` includes the teaching cases and analysis tool.

These contracts are generic guidance and a validation surface. A research repository must implement and test the applicable
state, lock, decision, output, and retention behavior locally; this skill update does not claim to migrate project task code
or project data.

The examples and static checks are intended for skill validation and script hygiene. They do not prove physical correctness, numerical convergence, or publication readiness.

Start with the relevant project instructions and active task source; do not require a particular project-context filename or read unrelated history in full.

## Future Roadmap

Planned directions for later releases:

- Evaluate optional Python-side data handling workflows, including possible use of the Ubermag ecosystem and related analysis tools.
- Add mumax+ compatibility, with the long-term direction of making mumax+ the primary target while keeping mumax3 support.
- Provide assisted migration workflows from existing mumax3 `.mx3` scripts to mumax+, including API mapping notes, behavior differences, and validation checklists.
- Expand postprocessing examples for OVF/table output, spectra, mode maps, texture tracking, and sweep summaries.

## Documentation

- [Release notes v0.3.0](docs/release_notes_v0.3.0.md): parameter consistency, installed modeling/analysis cases and validation scope.
- [Release notes v0.2.0](docs/release_notes_v0.2.0.md): MuMax3 setup guidance and skill maintenance updates.
- [Release notes v0.1.0](docs/release_notes_v0.1.0.md): initial public snapshot scope, compatibility, validation status, and known limitations.
- [Example catalog](examples/catalog/README.md): prompts, expected outputs, and coverage map.
- [Third-party sources](docs/third_party_sources.md): external source and provenance notes.
- [Troubleshooting](docs/troubleshooting.md): common local validation and mumax3 issues.

## License

Licensed under the [Apache License 2.0](LICENSE).
