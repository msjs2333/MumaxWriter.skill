# Runnable mumax3 Examples

These examples are intentionally generic and original to this repository. They are smoke-test style starting points, not calibrated physical studies.

## Minimal Thin-Film Relaxation

```go
// Output and mesh.
OutputFormat = OVF2_TEXT
nx := 128
ny := 64
nz := 1
Lx := 512e-9
Ly := 256e-9
Lz := 2e-9
SetGridSize(nx, ny, nz)
SetCellSize(Lx/nx, Ly/ny, Lz/nz)

// Geometry and material.
SetGeom(Rect(Lx, Ly))
Msat = 800e3
Aex = 13e-12
alpha = 0.02

// Initial state, output, and run stage.
m = Uniform(1, 0, 0)
TableAdd(m)
TableAutoSave(1e-12)
Relax()
SaveAs(m, "m_relaxed.ovf")
TableSave()
```

## Region-Based Bilayer Strip

```go
OutputFormat = OVF2_TEXT
nx := 128
ny := 64
nz := 2
Lx := 384e-9
Ly := 192e-9
Lz := 2e-9
SetGridSize(nx, ny, nz)
SetCellSize(Lx/nx, Ly/ny, Lz/nz)

SetGeom(Rect(Lx, Ly))
DefRegion(1, Layer(0))
DefRegion(2, Layer(1))
SaveAs(regions, "regions.ovf")

Msat.SetRegion(1, 800e3)
Msat.SetRegion(2, 650e3)
Aex.SetRegion(1, 13e-12)
Aex.SetRegion(2, 10e-12)
alpha.SetRegion(1, 0.02)
alpha.SetRegion(2, 0.03)

m = Uniform(1, 0, 0)
TableAdd(m.Region(1))
TableAdd(m.Region(2))
TableAutoSave(2e-12)
Relax()
SaveAs(m, "m_bilayer_relaxed.ovf")
```

## Local AC Field Dynamics

```go
OutputFormat = OVF2_TEXT
nx := 256
ny := 64
nz := 1
Lx := 768e-9
Ly := 192e-9
Lz := 2e-9
SetGridSize(nx, ny, nz)
SetCellSize(Lx/nx, Ly/ny, Lz/nz)
SetGeom(Rect(Lx, Ly))

Msat = 800e3
Aex = 13e-12
alpha = 0.01
m = Uniform(1, 0, 0)
Relax()
SaveAs(m, "m_static.ovf")

mask := NewVectorMask(nx, ny, nz)
for i:=0; i<8; i++{
    for j:=0; j<ny; j++{
        mask.SetVector(i, j, 0, Vector(0, 1, 0))
    }
}

h0 := 1e-3
f := 5e9
B_ext.Add(mask, h0*sin(2*pi*f*t))
TableAdd(m)
TableAutoSave(5e-12)
AutoSave(m, 20e-12)
Run(2e-9)
SaveAs(m, "m_dynamic_final.ovf")
```

## Review Notes

- Keep dimensions and parameters explicit near the top.
- Use SI units.
- Save `regions` when region layout matters.
- Use direct time-dependent expressions in API calls that accept functions.
- Put production parameter sweeps in Python orchestration instead of embedding many cases in one `.mx3`.
