# Expected Output: Broken Script Review

This expected output illustrates the desired response shape for `examples/prompts/review_broken_script.md`.

The answer should:

- Identify full Go constructs that mumax3 scripts do not support: `package`, `import`, `func`, and `return`.
- Replace `math.Sin` and `math.Pi` with mumax3 built-ins `sin` and `pi`.
- Replace `2^5` with `pow(2, 5)`.
- Avoid storing a time-dependent expression in a normal variable before assignment.
- Add output through `TableAdd`, `TableAutoSave`, `SaveAs`, or equivalent calls.
- State that static checking and `mumax3 -vet` are syntax/API checks, not physical validation.

Files:

- `corrected.mx3`: compact corrected script suitable for static checking and `mumax3 -vet`.
- `review.md`: concise review notes and validation caveats.

