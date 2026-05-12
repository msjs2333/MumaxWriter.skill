# Prompt: Write A Minimal Thin-Film Relaxation

Use the `mumax3` skill to write a minimal, runnable mumax3 relaxation case for a generic thin film.

Requirements:

- Create a single `.mx3` script.
- Use SI units and explicit mesh, geometry, material, initial state, output, and run sections.
- Model a 512 nm x 256 nm x 2 nm rectangular film with a 128 x 64 x 1 mesh.
- Use `Msat = 800e3`, `Aex = 13e-12`, and `alpha = 0.02`.
- Start from uniform magnetization along +x.
- Save the initial and relaxed magnetization as OVF files.
- Add table output for average magnetization, total energy, and `MaxAngle`.
- Do not use Go imports, helper functions, or invented APIs.
- Include a short note explaining the expected mumax3 output directory and the files needed for reproducibility.

Evaluation focus:

- The script is valid mumax3-style input rather than full Go.
- Parameters are centralized near the top.
- Output filenames are stable inside the case output directory.
- The answer mentions the generated script and minimal metadata needed to rerun it.
