# Expected Output: Minimal Thin-Film Relaxation

This expected output illustrates the level of structure and script quality desired for `examples/prompts/write_minimal_relax.md`. It is original repository content and is not copied from third-party examples.

Expected response shape:

- A short explanation of the case assumptions.
- A generated `.mx3` script.
- Minimal metadata identifying the mesh, geometry, material, initial state, and expected files.
- A note that mumax3 writes script output into a script-specific `.out` directory.

Files:

- `script.mx3`: compact runnable mumax3 script.
- `params.json`: minimal reproducibility metadata for the case.

Manual checks:

- `python skills/mumax3/scripts/check_mx3_static.py examples/expected_outputs/write_minimal_relax/script.mx3`
- If mumax3 is installed, run `mumax3 -vet script.mx3` from this directory.
