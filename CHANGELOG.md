# Changelog

## 0.1.1 - 2026-05-15

Citation and release metadata update for the generic `mumax3` Codex skill.

### Added

- Added repository-level `CITATION.cff` metadata for GitHub citation support and Zenodo-ready software archiving.
- Added README citation guidance in English, Chinese, and Japanese.
- Added release notes for the citation-only `v0.1.1` metadata release.

### Changed

- Documented that DOI badge and DOI links should be added after Zenodo generates the software DOI.

## 0.1.0 - 2026-05-12

Initial public release of the generic `mumax3` Codex skill.

### Added

- Generic `skills/mumax3` runtime skill with concise `SKILL.md` guidance.
- mumax3 references for syntax guardrails, anti-patterns, API index, API patterns, structures, parameter sweeps, output reproducibility, compatibility notes, and full API fallback.
- Runtime templates for minimal relaxation, region-aware thin-film relaxation, and local AC-field dynamics.
- Helper scripts for static `.mx3` warnings, deterministic template rendering, and conservative case status collection.
- Evaluation prompts and expected outputs for representative mumax3 workflows.
- Third-party source notes, troubleshooting notes, release notes, template parameter examples, and local release validation script.

### Changed

- Reduced tracked compatibility notes to generic environment assumptions instead of detailed machine hardware.
- Expanded example catalog coverage to show which prompts have expected outputs and which remain future coverage.

### Known Gaps

- `api_full.md` is kept as a sparse identifier/signature index with provenance. The official mumax3 API remains authoritative for detailed semantics.
- The examples are smoke-test and evaluation artifacts, not physically validated studies.

