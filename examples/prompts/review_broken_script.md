# Prompt: Review A Broken mumax3 Script

Use the `mumax3` skill to review the following `.mx3` script. Identify likely syntax/API problems, explain why they are risky in mumax3, and provide a corrected compact script.

```go
package main

import "math"

func drive(f float64) float64 {
    return math.Sin(2 * math.Pi * f * t)
}

nx, ny := 128, 64
SetGridSize(nx, ny, 1)
SetCellSize(4e-9, 4e-9, 2e-9)
SetGeom(Rect(512e-9, 256e-9))

Msat = 800e3
Aex = 13e-12
alpha = 0.01
Ku1 = 2^5

m = Uniform(1, 0, 0)
Relax()

h := drive(10e9)
B_ext = Vector(0, h, 0)
Run(2e-9)
```

Requirements:

- Do not merely rewrite it as ordinary Go.
- Use mumax3 built-ins directly.
- Replace the power expression with valid mumax3 syntax.
- Keep the time-dependent field expression inline where it is assigned.
- Add at least one table or spatial output.
- Mention that a local static checker can provide conservative warnings but does not prove physical correctness.
