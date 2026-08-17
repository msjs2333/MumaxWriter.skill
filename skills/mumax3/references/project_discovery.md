# Project Discovery

Use this reference before changing an existing mumax3 repository.

## Discovery Order

1. Inspect the repository status and preserve unrelated or uncommitted work.
2. Read the existing `.mx3` scripts and templates that implement the requested behavior.
3. Read the root README, task-specific documentation, result summaries, and test guidance.
4. If `docs/mumax3_reference/current_project_context.md` exists, read it completely.
5. Confirm parameter values against source code, generated manifests, and current result records rather than relying on old examples.

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

Keep literature reviews and large result tables in their original project documents and link to them rather than duplicating
them into the skill.

