# Prompt: Write A DMI Skyrmion Relaxation Case

Use the `mumax3` skill to write an original skyrmion relaxation script for a generic ultrathin ferromagnetic film with interfacial DMI.

Requirements:

- Use a 256 nm x 256 nm x 1 nm film with a 128 x 128 x 1 mesh.
- Set `Msat = 580e3`, `Aex = 15e-12`, `Ku1 = 0.8e6`, `anisU = Vector(0, 0, 1)`, `Dind = 3e-3`, and `alpha = 0.3`.
- Seed a Neel skyrmion centered in the film and relax it.
- Save initial and relaxed magnetization, plus table diagnostics including `E_total` and `MaxAngle`.
- Explain which parts should be verified against the intended material system before production use.
- Do not copy a third-party skyrmion example.

Optional extension:

- Add a short second stage showing how current-driven motion could be added using `J`, `Pol`, and `xi`, but keep it clearly separated from the relaxation stage.
