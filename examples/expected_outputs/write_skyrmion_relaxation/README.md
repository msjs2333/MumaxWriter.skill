# Expected Output: DMI Skyrmion Relaxation

This expected output illustrates the desired structure for `examples/prompts/write_skyrmion_relaxation.md`.

Files:

- `params.json`: case metadata and requested material/geometry values.
- `script.mx3`: original generic mumax3 script for an interfacial-DMI skyrmion relaxation smoke test.

Manual checks:

```powershell
python skills\mumax3\scripts\check_mx3_static.py examples\expected_outputs\write_skyrmion_relaxation\script.mx3
mumax3 -vet examples\expected_outputs\write_skyrmion_relaxation\script.mx3
```

Production use requires checking material constants, DMI sign convention, anisotropy, mesh resolution, boundary conditions, and whether the seeded skyrmion is stable for the intended system.

