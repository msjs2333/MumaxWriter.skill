# Project Discovery

Use this reference before changing an existing mumax3 repository.

## Start From The Requested Intent

Choose the smallest authoritative context that can answer the request without weakening scientific gates.

| Intent | Read first | Do not load by default |
|---|---|---|
| Status, ETA, monitor, cancel | Current operation state, compact handoff, declared log tail | API catalog, geometry history, OVF files, complete timelines |
| Plot, GIF, summary | Exact input/product manifest and selected analysis/plot profile | Full simulation API or unrelated project history |
| Physics or protocol change | Complete active project context, active template/source, API references | Historical defaults that are not active inputs |
| Checkpoint reuse or scan | Parent manifest/SHA256, initial-state role, allowed protocol, output profile | Absolute path or mtime as identity |
| Descendant preparation/classification | Decision contract, fresh gate summaries, complete ancestor chain | Final-frame-only or single-component substitutes |

If the narrow context is missing, corrupt, stale, or internally inconsistent, stop and expand deliberately. Do not silently
replace missing evidence with generic examples.

## Discovery Order

1. Inspect the repository status and preserve unrelated or uncommitted work.
2. Read the existing `.mx3` scripts and templates that implement the requested behavior.
3. Read the root README, task-specific documentation, result summaries, and test guidance.
4. If `docs/mumax3_reference/current_project_context.md` exists, read it completely.
5. Confirm parameter values against source code, generated manifests, and current result records rather than relying on old examples.

Steps 2-5 are required before changing physics, protocols, checkpoints, or analysis definitions. Pure read-only status and
product-layout work may follow the intent table instead, provided it does not make a scientific decision.

Bundled templates are generic examples. They never override a repository's current model.

## Historical And Current Models

Projects often retain an early baseline alongside newer production geometries. Keep both traceable, but label them explicitly.
Do not promote a historical mesh, material value, field, source position, or frequency to a current default merely because it
appears in an older script or document.

When sources disagree:

1. Prefer the active task source and rendered case manifest.
2. Use current result summaries to verify what actually ran.
3. Treat planning documents as intent, not evidence of completed dynamics.
4. Report unresolved conflicts before changing physical behavior.

## Project Context Contract

A project-local context should remain concise and contain:

- current and historical model boundaries;
- authoritative source and documentation links;
- active, completed, and archived task status;
- checkpoint identity and hash requirements;
- project-specific analysis and human-review constraints;
- facts that must not be inferred across different material or topology models.

Prefer a compact active summary that links to historical records. Routine monitors should consume a small, schema-versioned
handoff rather than this complete context. Plot-only work should consume exact manifests and profiles rather than discover
inputs by scanning large output trees.

Keep literature reviews and large result tables in their original project documents and link to them rather than duplicating
them into the skill.
