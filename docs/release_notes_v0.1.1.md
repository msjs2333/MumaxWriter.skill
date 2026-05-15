# Release Notes: v0.1.1

Release date: 2026-05-15

## Scope

MumaxWriter.skill v0.1.1 is a citation and release metadata update for the generic `mumax3` Codex skill.

Included:

- Repository-level `CITATION.cff` metadata for GitHub citation support and Zenodo-ready software archiving.
- README citation guidance in English, Chinese, and Japanese.
- Release documentation describing the citation-only nature of this update.

## Compatibility

- No runtime skill behavior changed in this release.
- The installed skill path remains `skills/mumax3/`.
- The helper scripts, templates, references, and evaluation examples are unchanged from v0.1.0.

## Validation

This release should be validated from the repository root with:

```powershell
python tests\validate_release.py
```

When `cffconvert` is available locally, the citation metadata can also be validated with:

```powershell
cffconvert --validate -i CITATION.cff
```

## Zenodo Notes

This release is intended to be archived as a Zenodo software record through the GitHub-Zenodo integration. After Zenodo assigns a DOI, the DOI badge and DOI link can be added back to the README files.

## Known Limitations

- The citation author field currently uses the GitHub handle `msjs2333` as a placeholder.
- No DOI is embedded in the repository until Zenodo generates one.
- This metadata release does not change the physical validation status of the examples.
