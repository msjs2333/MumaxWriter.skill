# Troubleshooting

## Skill Is Not Triggering

- Confirm `skills/mumax3` was copied into the active Codex skills directory.
- Invoke it explicitly with: `Use $mumax3 to write or review this mumax3 script.`
- Check that `skills/mumax3/SKILL.md` exists and starts with valid YAML frontmatter.

## Python Helper Fails

- Use Python 3.10 or newer.
- Run helper scripts from the repository root when using relative paths.
- The bundled helper scripts use only the Python standard library.

## `quick_validate.py` Fails With Missing `yaml`

The system `skill-creator` validator may require PyYAML. This repository's `tests/validate_release.py` avoids that dependency and performs the release-candidate checks used by this project.

## `mumax3 -vet` Is Not Available

- Install mumax3 and make sure `mumax3` is on `PATH`.
- If `mumax3` is unavailable, `tests/validate_release.py` skips `-vet` checks and still runs Python, template, and static checks.
- Passing `-vet` does not prove physical correctness; it only catches parser/API issues that mumax3 can detect without running the simulation.

## Output Directory Already Exists

mumax3 writes outputs into a script-specific `.out` directory. If rerunning manually, either remove the old output directory, choose a new script name, or use the appropriate mumax3 command-line option only when overwriting is intentional.

## Paths With Spaces

Prefer running commands from the repository root and quote paths when invoking mumax3 or Python manually. Keep generated case folders simple and avoid spaces in sweep case IDs.

## Physical Validation

The skill can help write syntactically valid scripts and reproducible case layouts. It does not validate whether a material model, mesh resolution, boundary condition, or excitation amplitude is physically appropriate for a publication-quality study.

