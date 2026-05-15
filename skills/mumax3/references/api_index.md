# mumax3 API Index

Use this compact whitelist for normal script generation. It covers common, high-frequency identifiers only. If a needed identifier is not listed, check `api_full.md` or the official mumax3 API before using it.

Source baseline: official mumax3.12 API, <https://mumax.github.io/api.html>.

## Syntax And Constants

- `true`, `false`
- `pi`, `inf`
- `mu0`/`Mu0`, `GammaLL`, `t`, `step`
- Math functions: `abs`, `ceil`, `floor`, `exp`, `log`, `log10`, `max`, `min`, `mod`, `pow`, `remainder`, `sin`, `cos`, `tan`, `sqrt`, `sinc`, `rand`, `randNorm`, `randSeed`
- Formatting/printing: `Print`, `Printf`, `Sprintf`

These names are built into mumax3. Use them directly; do not redeclare them with
`:=`. Identifier lookup is case-insensitive in mumax3 scripts, so `mu0`, `Mu0`,
and `MU0` refer to the same built-in constant. For less common names, search
`api_full.md` before choosing a local variable name.

## Mesh And Geometry

- `SetGridSize(nx, ny, nz)`
- `SetCellSize(dx, dy, dz)`
- `SetMesh(nx, ny, nz, dx, dy, dz, pbcx, pbcy, pbcz)`
- `SetPBC(nx, ny, nz)`
- `SetGeom(shape)`
- `EdgeSmooth`

Common shapes:

- `Rect(x, y)`, `Square(size)`
- `Circle(diameter)`, `Ellipse(x, y)`
- `Cuboid(x, y, z)`, `Cylinder(diameter, height)`, `Ellipsoid(x, y, z)`
- `XRange(x1, x2)`, `YRange(y1, y2)`, `ZRange(z1, z2)`, `Layer(k)`, `Layers(k1, k2)`
- `Universe()`, `ImageShape(path)`, `Cell(i, j, k)`

Common shape methods:

- `Add`, `Sub`, `Intersect`, `Xor`, `Inverse`
- `Transl`, `RotX`, `RotY`, `RotZ`, `Scale`, `Repeat`

## Regions

- `DefRegion(region, shape)`
- `DefRegionCell(region, i, j, k)`
- `RedefRegion(old, new)`
- `regions`
- `NREGION`

Quantity region methods commonly used in scripts:

- `SetRegion(region, valueOrFunction)`
- `Region(region)`
- `GetRegion(region)`

## Magnetization And Initial States

- `m`
- `Uniform(mx, my, mz)`
- `RandomMag()`, `RandomMagSeed(seed)`
- `Vortex(circulation, polarization)`, `VortexWall(mxLeft, mxRight, circulation, polarization)`
- `NeelSkyrmion(charge, polarization)`, `BlochSkyrmion(charge, polarization)`
- `TwoDomain(...)`
- `m.Set(config)`, `m.SetRegion(region, config)`, `m.SetInShape(shape, config)`, `m.LoadFile(path)`

## Material Parameters

Common scalar parameters:

- `Msat`, `Aex`, `alpha`
- `Ku1`, `Ku2`, `Kc1`, `Kc2`, `Kc3`
- `Dind`, `Dbulk`
- `Temp`

Common vector parameters:

- `anisU`, `anisC1`, `anisC2`

Spin-torque/current parameters:

- `J`, `Pol`, `xi`, `Lambda`, `EpsilonPrime`, `FixedLayer`, `FreeLayerThickness`, `DisableZhangLiTorque`, `DisableSlonczewskiTorque`

## Fields And Excitation

- `B_ext`, `B_ext.Add(mask, value)`, `B_ext.RemoveExtraTerms()`
- `Vector(x, y, z)`
- `NewVectorMask(nx, ny, nz)`, `NewScalarMask(nx, ny, nz)`, `NewSlice(ncomp, nx, ny, nz)`
- `LoadFile(path)`

## Output Quantities

Common spatial or table quantities:

- `m`, `B_ext`, `B_eff`, `B_demag`, `B_exch`, `B_anis`, `B_therm`, `torque`
- `E_total`, `E_demag`, `E_exch`, `E_anis`, `E_Zeeman`, `E_therm`
- `MaxAngle`, `LastErr`, `NEval`, `NSteps`, `dt`, `t`
- `Average(quantity)`, `Min(quantity)`, `Max(quantity)`, `Sum(quantity)`, `Crop(...)`

## Scheduling And Saving

- `Save(quantity)`, `SaveAs(quantity, path)`
- `AutoSave(quantity, period)`
- `TableAdd(quantity)`, `TableAddVar(value, name, unit)`
- `TableAutoSave(period)`, `TableSave()`, `TablePrint(...)`
- `Snapshot(quantity)`, `SnapshotAs(quantity, path)`
- `OutputFormat`, `TableAdd`, `TableAutoSave`

Add table columns once during setup. `TableAdd` and `TableAddVar` define table
columns; `TableSave` writes a row. Avoid calling `TableAddVar` inside a field
loop to record changing values. Prefer table columns for existing quantities
such as `B_ext` and `m`, or postprocess derived quantities in Python.

## Running And Solver Control

- `Relax()`, `Minimize()`
- `Run(seconds)`, `RunWhile(condition)`
- `SetSolver(id)`
- `FixDt`, `MinDt`, `MaxDt`, `MaxErr`, `Headroom`
- `RelaxTorqueThreshold`, `RelaxWallClockTime`

