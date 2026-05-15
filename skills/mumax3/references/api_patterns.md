# mumax3 API Patterns

Use this reference for common API combinations. It is not a full API list; check
`api_index.md`, `api_full.md`, or the official API page when an identifier is not
covered here.

Source baseline: official mumax3.12 API, <https://mumax.github.io/api.html>.

## Mesh And Periodic Boundaries

Prefer mesh dimensions that are powers of two, or at least products of small
prime factors such as 2, 3, 5, and 7. Keep cell sizes in SI units and derive
them from physical dimensions to avoid hidden unit conversions.

```go
nx := 256
ny := 128
nz := 1
Lx := 512e-9
Ly := 256e-9
Lz := 2e-9

SetGridSize(nx, ny, nz)
SetCellSize(Lx/nx, Ly/ny, Lz/nz)
```

Use `SetPBC(px, py, pz)` only when the model is physically periodic. A nonzero
value enables wrap-around in that direction and controls how many repeated
images the demag field sees; large values can make initialization slow.

```go
SetPBC(4, 4, 0) // thin-film periodicity in x and y
```

Cross-check identifiers: `SetGridSize`, `SetCellSize`, `SetMesh`, and `SetPBC`
are listed in `api_index.md#mesh-and-geometry` and
`api_full.md#mesh-size-and-geometry`.

## Shape Composition

Shapes are defined around the simulation-box center and use meters. Compose
simple shapes first, then call `SetGeom` once unless a deliberate resize or
geometry change is part of the experiment.

```go
disk := Circle(160e-9)
notch := Rect(30e-9, 80e-9).Transl(80e-9, 0, 0)
wire := Rect(800e-9, 120e-9)

SetGeom(wire.Sub(notch).Add(disk.Transl(-250e-9, 0, 0)))
SaveAs(geom, "geom.ovf")
```

Common shape methods: `Add`, `Sub`, `Intersect`, `Xor`, `Inverse`, `Transl`,
`RotX`, `RotY`, `RotZ`, `Scale`, and `Repeat`. Prefer named intermediate
shapes over deeply nested expressions when reviewing or parameterizing scripts.

Cross-check identifiers: `Rect`, `Circle`, `Cuboid`, `Cylinder`, range shapes,
and shape methods are listed in `api_index.md#mesh-and-geometry` and
`api_full.md#shapes`.

## Regions

Regions are mutually exclusive cell labels. Each cell belongs to exactly one
region, with region 0 as the default. Save `regions` when debugging spatial
assignment, especially after overlapping shape definitions or cell-level edits.

```go
core := Circle(80e-9)
rim := Circle(140e-9).Sub(core)

DefRegion(1, core)
DefRegion(2, rim)
SaveAs(regions, "regions.ovf")
```

Use `DefRegionCell` for sparse cell-index assignments, not for large masks that
are easier to express as shapes. Use `RedefRegion(old, new)` when remapping
existing labels is clearer than redefining shapes.

```go
DefRegionCell(3, 0, 0, 0)
RedefRegion(3, 2)
```

Cross-check identifiers: `DefRegion`, `DefRegionCell`, `RedefRegion`,
`regions`, and `NREGION` are listed in `api_index.md#regions` and
`api_full.md#material-regions`.

## Material And Quantity Region Values

Assigning a quantity directly sets it globally. Use `SetRegion` only for
region-specific values and keep region constants close to the region definition.

```go
Msat = 800e3
Aex = 13e-12
alpha = 0.01

Msat.SetRegion(1, 580e3)
alpha.SetRegion(2, 0.08)
```

Vector quantities also support region-specific assignment.

```go
anisU = Vector(0, 0, 1)
anisU.SetRegion(1, Vector(1, 0, 0))
B_ext.SetRegion(2, Vector(0, 5e-3, 0))
```

For magnetization, use `m.Set(...)` globally, `m.SetRegion(...)` by material
region, or `m.SetInShape(...)` for geometric seeds independent of region labels.

```go
m = Uniform(1, 0, 0)
m.SetRegion(1, Vortex(1, 1))
m.SetInShape(Circle(40e-9), Uniform(0, 0, 1))
```

Cross-check identifiers: material parameters and `m` methods are listed in
`api_index.md#magnetization-and-initial-states`,
`api_index.md#material-parameters`, and `api_full.md#material-parameters`.

## Relaxation And Dynamics

Use `Relax()` for robust relaxation from arbitrary or noisy starting states.
Turn off excitations first: temperature, current, and time-dependent fields
should not be active during relaxation. During `Relax()`, precession is disabled
and simulation time `t` does not advance.

```go
B_ext = Vector(0, 0, 0)
J = Vector(0, 0, 0)
Temp = 0
Relax()
SaveAs(m, "relaxed.ovf")
```

Use `Minimize()` for faster energy minimization when the state is already near a
minimum, such as consecutive field steps in a hysteresis loop. It is less robust
than `Relax()` for random or far-from-equilibrium initial states.

```go
B := -50e-3
for i:=0; i<=20; i++{
    B_ext = Vector(B, 0, 0)
    Minimize()
    TableSave()
    B += 5e-3
}
```

Use `Run(duration)` for time dynamics. Use `RunWhile(condition)` only when the
stopping condition is itself part of the model, such as switching or a moving
feature crossing a threshold.

```go
TableAutoSave(2e-12)
AutoSave(m, 50e-12)
Run(2e-9)

mx := m.Comp(0)
RunWhile(mx.Average() < 0)
```

Cross-check identifiers: `Relax`, `Minimize`, `Run`, `RunWhile`, `Steps`, and
time quantities are listed in `api_index.md#running-and-solver-control` and
`api_full.md#running`.

## Solver Control

The default adaptive solver is usually appropriate. Only set solver controls
when the task needs a fixed-step method, tighter error control, or a documented
reproduction of a previous run.

```go
MaxErr = 1e-6
MinDt = 1e-16
MaxDt = 1e-12
Run(1e-9)
```

Use `SetSolver(4)` with `FixDt` for fixed-step RK4-style runs. Use Euler
(`SetSolver(1)`) only for debugging or exceptional cases because it requires
`FixDt` and ignores other accuracy settings.

```go
SetSolver(4)
FixDt = 1e-15
Run(200e-12)
FixDt = 0
SetSolver(5)
```

Cross-check identifiers: `SetSolver`, `FixDt`, `MaxErr`, `MinDt`, `MaxDt`,
`Headroom`, `LastErr`, and `dt` are listed in
`api_index.md#running-and-solver-control` and `api_full.md#running`.

## Loading And Output

Use `m.LoadFile(path)` to load a magnetization state into `m`. Use top-level
`LoadFile(path)` when an API expects a `Slice`, such as mask or custom quantity
work.

```go
m.LoadFile("relaxed.ovf")
mask := LoadFile("source_mask.ovf")
```

Use `Save` for conventional auto-named field output and `SaveAs` when later
automation expects a stable filename. Use `AutoSave` for spatial snapshots and
`TableAutoSave` for time series. `table.txt` includes time and average
magnetization by default; add other quantities explicitly.

```go
OutputFormat = OVF2_BINARY

TableAdd(B_ext)
TableAdd(E_total)
TableAdd(MaxAngle)
TableAdd(torque)
TableAutoSave(5e-12)

AutoSave(m, 100e-12)
SaveAs(m, "m_final.ovf")
SaveAs(B_eff, "B_eff_final.ovf")
```

`TableAdd` and `TableAddVar` are column-registration calls. Put them before the
run or sweep loop, then use `TableSave()` inside the loop to append rows. If a
derived value changes at each sweep point and is awkward to express as a
mumax3 scalar function, save the underlying quantities and compute the derived
column in Python.

Recommended field-loop pattern:

```go
TableAdd(B_ext)
TableAdd(E_total)

for i:=0; i<=20; i++{
    B_ext = Vector(-50e-3 + i*5e-3, 0, 0)
    Minimize()
    TableSave()
}
```

Risky pattern:

```go
for i:=0; i<=20; i++{
    h := -50e-3 + i*5e-3
    B_ext = Vector(h, 0, 0)
    Minimize()
    TableAddVar(h, "H", "T")
    TableSave()
}
```

For region-specific output, call `.Region(region)` on quantities that support
it, or `.Comp(component)` for vector components.

```go
TableAdd(m.Region(1))
SaveAs(m.Comp(2), "mz_final.ovf")
```

Cross-check identifiers: `LoadFile`, `Save`, `SaveAs`, `AutoSave`, `TableAdd`,
`TableAddVar`, `TableAutoSave`, and output quantities are listed in
`api_index.md#scheduling-and-saving`, `api_index.md#output-quantities`,
`api_full.md#scheduling-output`, and `api_full.md#output-quantities`.

## Common Quantities To Monitor

Use a small, purposeful output set instead of saving every quantity.

- `m`: magnetization state; save as OVF and table-average when dynamics matter.
- `B_eff`: effective field; useful for diagnostics after relaxation.
- `E_total`: scalar energy; useful in minimization and hysteresis checks.
- `MaxAngle`: neighbor-spin angle; useful for mesh-quality and convergence
  diagnostics.
- `torque` or `maxTorque`: useful for relaxation quality, but interpret in the
  context of solver settings and model scale.

```go
TableAdd(E_total)
TableAdd(MaxAngle)
TableAdd(torque)
TableAutoSave(10e-12)
```

Check `api_full.md#output-quantities` before using less common quantities such
as `LLtorque`, `STTorque`, `Edens_*`, or extension-provided diagnostics.

## Time-Dependent Inputs

When an API accepts a function, mumax3 can implicitly re-evaluate an expression
over time. Do not store a time-dependent expression in an ordinary variable
unless a one-time evaluation is intended.

Correct dynamic assignment:

```go
f := 10e9
h0 := 1e-3
B_ext = Vector(0, h0*sin(2*pi*f*t), 0)
```

Risky if the intent was dynamic:

```go
drive := h0*sin(2*pi*f*t)
B_ext = Vector(0, drive, 0)
```

For localized excitation, combine a mask with a scalar time function.

```go
source := NewVectorMask(nx, ny, nz)
for i:=0; i<nx; i++{
    for j:=0; j<ny; j++{
        if i < 8 {
            source.SetVector(i, j, 0, Vector(0, 0, 1))
        }
    }
}
B_ext.Add(source, h0*sin(2*pi*f*t))
```

Use `B_ext.RemoveExtraTerms()` before replacing added excitation terms in staged
runs.

Cross-check identifiers: `B_ext`, `NewVectorMask`, `NewScalarMask`,
`Vector`, `sin`, `pi`, and `t` are listed in `api_index.md#fields-and-excitation`
and `api_full.md#excitation`.

## Spin Currents

Spin-current scripts are advanced enough to require official-API confirmation.
Keep torque model choices explicit. For Zhang-Li-style current-driven dynamics,
set `J`, `Pol`, and `xi`, and disable the Slonczewski torque if it should not
contribute.

```go
DisableSlonczewskiTorque = true
J = Vector(1e12, 0, 0)
Pol = 0.6
xi = 0.05
Run(1e-9)
```

For Slonczewski torque, define the fixed layer and geometry assumptions
explicitly.

```go
DisableZhangLiTorque = true
J = Vector(0, 0, 8e11)
Pol = 0.5
FixedLayer = Vector(0, 0, 1)
FixedLayerPosition = FIXEDLAYER_TOP
FreeLayerThickness = 1.2e-9
Lambda = 1
EpsilonPrime = 0.02
```

Cross-check in `api_full.md#spin-currents` and the official API before using
spin-torque parameters.

## Moving Window

Use moving-window helpers only for models where the physical feature can leave
the simulation box, such as domain walls or bubbles. Add `TotalShift` to the
table so downstream analysis can reconstruct absolute position.

```go
ext_centerWall(0)
ext_rmSurfaceCharge(0, -1, 1)
TableAdd(TotalShift)
Run(5e-9)
```

The default inserted edge magnetization is usually sufficient. Override
`ShiftMagL`, `ShiftMagR`, `ShiftGeom`, `ShiftM`, or `ShiftRegions` only when the
boundary behavior is part of the intended model.

Cross-check in `api_full.md#moving-simulation-window` and the official API.
Extension APIs can be version-sensitive.

## Custom Quantities

Custom quantities combine existing quantities point-wise. They are useful for
diagnostics, derived fields, or saved postprocessing inputs. Keep the expression
short and verify component/scalar dimensions before using it in analysis.

```go
mx := m.Comp(0)
my := m.Comp(1)
mxy2 := Add(Mul(mx, mx), Mul(my, my))
SaveAs(mxy2, "mxy2.ovf")
```

For finite-difference expressions, make the stencil and cell-size assumptions
visible in variable names and comments. Prefer built-in extension quantities
when they exactly match the needed diagnostic.

Cross-check in `api_full.md#custom-quantities` and the official API.

## Custom Effective Fields

Custom field and energy terms directly affect dynamics and should be treated as
model changes, not output conveniences. Define both the field term and matching
energy density when energy accounting matters, then add diagnostics for
`B_custom`, `E_custom`, or `Edens_custom`.

```go
Ms := 800e3
K := 2e5
u := ConstVector(0, 0, 1)

anisField := Mul(Const(2*K/Ms), Mul(Dot(u, m), u))
anisEdens := Mul(Const(-0.5*Ms), Dot(anisField, m))

AddFieldTerm(anisField)
AddEdensTerm(anisEdens)
TableAdd(E_custom)
```

Call `RemoveCustomFields()` or `RemoveCustomEnergies()` before replacing custom
terms in staged scripts.

Cross-check in `api_full.md#custom-effective-field-terms` and the official API.

## Magnetic Force Microscopy

MFM output is a derived image-style diagnostic for 2D magnetization. Set the
lift height explicitly and save `MFM` under a name that records that choice.

```go
MFMLift = 50e-9
SaveAs(MFM, "mfm_lift_50nm.ovf")
```

Use `MFMDipole` only when the tip model needs a finite vertically magnetized
section instead of the default point-monopole approximation.

Cross-check in `api_full.md#magnetic-force-microscopy` and the official API.
