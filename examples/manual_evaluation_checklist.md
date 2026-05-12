# Manual Evaluation Checklist

Use this checklist when running the prompts in `examples/prompts/` against the `mumax3` skill. The checklist is intentionally manual because the goal is to judge agent behavior, not only static syntax.

## Before Running

- Confirm the evaluator has read `skills/mumax3/SKILL.md`.
- For ordinary script generation, allow use of `references/api_index.md`, `references/api_patterns.md`, `references/structures.md`, and `references/output_and_reproducibility.md`.
- For parameter sweeps, allow `references/parameter_sweep.md`.
- For disputed or advanced identifiers, require checking `references/api_full.md` or the official mumax3 API.

## Script Quality

- Uses mumax3 script syntax, not full Go.
- Avoids `package`, `import`, `func`, `return`, Go standard library selectors, multiple assignment, and invented helper APIs.
- Uses SI units and names physical dimensions clearly.
- Keeps mesh, geometry, material, initial state, fields, output, and run stages easy to identify.
- Assigns time-dependent fields inline to `B_ext` or `B_ext.Add(...)` when the expression depends on `t`.
- Saves enough spatial and table output for the requested workflow.

## Reproducibility

- Records case parameters, units, generated script paths, expected output directories, and log paths.
- Uses stable filenames inside isolated case directories.
- Explains mumax3 `.out` output behavior when relevant.
- Uses Python for batch orchestration instead of embedding a full sweep inside one `.mx3`.

## Physics And Scope

- States assumptions and production-use checks for material constants, mesh resolution, damping, boundary conditions, and excitation amplitude.
- Does not claim physical validation from syntax checks alone.
- Credits external projects only as inspiration sources and does not copy third-party code.
- Separates optional advanced stages, such as current-driven skyrmion motion, from the base relaxation script.

## Local Checks

- Run `python skills/mumax3/scripts/check_mx3_static.py <script.mx3>` on generated scripts when local Python is available.
- If mumax3 is installed, run `mumax3 -vet <script.mx3>`.
- For dynamic examples, inspect table and autosave cadence against the highest excitation frequency.
