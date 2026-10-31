# Changelog

## Unreleased

- Fixed the field/frequency generator so geometry, mesh, material, drive and sampling settings in `params.json` actually determine both scripts. Existing case directories are refused.
- Added installed continuous-hysteresis, SP4 field-1 and pulsed-macrospin FMR tutorials, with observable extraction, explicit acceptance limits and independent evaluation prompts.
- Added parameter-change regressions and synthetic analysis failure tests; documented actual engine runs separately from benchmark acceptance.
- Unified continuation-versus-independent-sweep guidance and documented the optional collector schema. Removed project-specific signature aliases and obsolete maintenance audits containing private paths and research-template names.

## 0.2.0 - 2026-10-30

### Installation and documentation

- Added a separate MuMax3 installation reference covering environment checks, official binaries, WSL 2, source builds and authorized agent assistance; the main skill links to it only when needed.
- Removed repository citation metadata and software-archiving preparation from the current documentation.
- Updated the English, Chinese and Japanese READMEs.
- Included the previously unreleased skill and helper improvements below.

### Third-round generalization (2026-09-15)

- Made native sequential scans and external case orchestration explicit alternatives; choose tables, fields and checkpoints from the scientific question rather than a universal output recipe.
- Kept concise coordination, traceability, evidence and human/automatic principles without requiring project schemas or ancestor tracking. Merged useful input-reuse guidance into the output reference and removed `project_discovery.md` and `project_workflows.md`.
- Retained the layout-specific status collector as optional compatibility tooling, not a default workflow. Invalid optional metadata is reported; analysis without comparable provenance is unverified rather than fresh. Zero discovered cases produces a diagnostic on stderr; CSV columns remain compatible.
- Preserved static checking, templates, installation backup/hash checks and existing project runtime protections.

### Second-round simplification (2026-09-15)

- Shortened the entry point and four workflow/output references; read task-specific context instead of a mandatory full project history.
- Kept writer coordination, SHA256 traceability, sufficient vector evidence and human/automatic separation as concise, scoped principles. Removed mandatory project state schemas, ancestor pipelines and cold-storage/release procedures from generic guidance.
- Kept API references, templates and runtime helpers compatible; directory layouts and metadata are examples, not a required framework.
- Replaced wording/project-name assertions with scoped metadata/link and existing helper behavior checks; added docs/helpers/full validation scopes, retaining a full default and explicit engine-skip reporting.

The earlier entries below describe the first-round development history; the second-round notes supersede its mandatory workflow/wording surface.

### Added

- Added repository-local project-context discovery without embedding private or fast-changing model defaults in the generic skill.
- Added task workflow guidance for signatures, checkpoint hashes, resume behavior, ETA, path overrides, manual review, and layered tests.
- Added a backed-up, hash-verified local skill synchronization helper and helper regression tests.
- Added four explicit workflow invariants: one writer per mutable resource, SHA256 lineage, all-vector/all-frame decision gates,
  and separation of automatic state from human scientific classification.
- Added intent-based reference routing for compact status/monitor work, product-only plotting, physics changes, descendant
  preparation, and long background operations.
- Added contracts for resilient state I/O, owner-identified locks, ancestor gates, local handoffs, cancellation typing,
  operation ETA, minimal-import doctor checks, and GPU capacity leases.
- Added output-directory/timeline reconciliation, repository-relative identity, initial-state roles, output/plot profiles,
  product DAGs, protocol-derived capacity estimates, and verified retention/release guidance.
- Added release checks for required safety contracts, local reference links, and exclusion of project-specific literals.
- Added generic cold-volume guidance for sealed datasets, immutable backup snapshots, candidate-scoped apply-time hashing,
  durable release/recovery transactions, independent backup GC, archive recovery semantics, and copy-count risk.

### Changed

- Expanded region, local anisotropy, spin-current mask, and staged-drive guidance.
- Made static mesh/output checks case-insensitive and limited protected-name warnings to core mumax3 quantities and constants.
- Extended case-status collection with manifest, provenance, analysis-freshness, and manual-review fields.
- Expanded helper regression coverage from implementation helpers to the generic workflow and reproducibility contract surface.

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

