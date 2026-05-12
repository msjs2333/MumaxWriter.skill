# Prompt: Write A Vortex Relaxation Case

Use the `mumax3` skill to write an original vortex-state relaxation script for a generic circular disk.

Requirements:

- Disk diameter: 200 nm.
- Thickness: 10 nm.
- Mesh: 128 x 128 x 4.
- Material: `Msat = 800e3`, `Aex = 13e-12`, `alpha = 0.05`.
- Use `SetGeom(Cylinder(...))` or an equivalent disk geometry.
- Initialize with `Vortex(1, 1)` and relax.
- Save geometry and initial/relaxed magnetization.
- Add table diagnostics useful for checking relaxation quality.
- Mention how later vortex dynamics would normally be analyzed without inventing a mumax3 core-tracking API.
