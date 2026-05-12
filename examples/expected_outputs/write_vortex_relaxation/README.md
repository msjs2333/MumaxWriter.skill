# Expected Output: Vortex Relaxation

This expected output illustrates the desired structure for `examples/prompts/write_vortex_relaxation.md`.

Files:

- `params.json`: case metadata and requested material/geometry values.
- `script.mx3`: original generic mumax3 vortex-state relaxation script.

Manual checks:

```powershell
python skills\mumax3\scripts\check_mx3_static.py examples\expected_outputs\write_vortex_relaxation\script.mx3
mumax3 -vet examples\expected_outputs\write_vortex_relaxation\script.mx3
```

Later vortex dynamics should be analyzed in Python from magnetization snapshots or OVF/table output. Do not invent a built-in mumax3 core-tracking API.

