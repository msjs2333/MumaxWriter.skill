# Micromagnetic Structure Patterns

Use this reference to choose a compact modeling pattern for common structures. It is not a physics handbook; verify material constants, mesh resolution, and boundary conditions against the user's model.

## Thin Film Or Nanostrip

- Use one or a few cells through thickness when the model is effectively two-dimensional.
- Prefer mesh dimensions with small prime factors for GPU performance.
- Start with `SetGeom(Rect(Lx, Ly))` or the full mesh box.
- Choose table quantities for averages and field saves for spatial analysis or state reuse.

## Material Heterostructure

- Define each material with `DefRegion(region, shape)` or `DefRegionCell`.
- Assign material quantities per region with `Msat.SetRegion`, `Aex.SetRegion`, `alpha.SetRegion`, anisotropy, DMI, or spin-torque parameters as needed.
- Save `regions` when inspecting or reusing a nontrivial region layout would help.
- Remember that each cell has one region; overlapping shapes require deliberate ordering.

## Domain Wall

- Use `TwoDomain(...)`, `m.SetInShape(...)`, or explicit left/right shapes to seed domains.
- Keep wall initialization separate from material regions.
- For propagation, use case-specific field or current parameters and table output that can locate the wall later.
- If using absorbing boundaries, reserve non-conflicting region IDs and document which cells are absorbers.

## Vortex

- Use disk or square geometry with `Circle`, `Cylinder`, `Square`, or `Rect`.
- Initialize with `Vortex(circulation, polarization)` when the built-in configuration matches the task.
- For core-motion studies, choose field snapshots or suitable table quantities for trajectory analysis.

## Skyrmion

- Use `NeelSkyrmion` or `BlochSkyrmion` only when compatible with the intended DMI and material model.
- Include DMI through `Dind` or `Dbulk` as appropriate.
- Relax before applying current or dynamic fields unless the user asks for a deliberately non-equilibrium initial condition.

## FMR And Spin Waves

- For response about equilibrium, prepare a relaxed static state; save it if needed for reuse or reference subtraction.
- Apply a small uniform or local time-dependent field with `B_ext` or `B_ext.Add(mask, expression)`.
- Keep the dynamic expression inline if it depends on `t`.
- Use time-resolved averages for global response, and field snapshots when spatial modes or propagation are needed. Choose sampling and duration for the requested frequency range and resolution.

## Periodic Systems

- Use `SetPBC(px, py, pz)` before or with mesh setup.
- Keep PBC counts modest unless the demag approximation requires more images.
- State which directions are periodic in comments and metadata.

