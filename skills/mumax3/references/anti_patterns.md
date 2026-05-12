# mumax3 Anti-Patterns

Use this reference when reviewing scripts or when an implementation starts to look like normal Go instead of mumax3 input syntax.

## Full Go Constructs

Do not generate or keep these in `.mx3` scripts:

- `package` or `import`.
- `func` declarations or custom Go helper functions.
- `type`, structs, interfaces, methods, goroutines, channels, `select`, `defer`, `goto`, labels, or maps.
- `switch`, `range`, `return`, `break`, and `continue`.
- Multi-return idioms such as `x, err := ...`.

mumax3 parses a Go-like subset and then interprets only supported statements and expressions. A fragment that is valid Go may still be invalid mumax3 script.

## Go Standard Library Misuse

Avoid package selectors such as:

- `fmt.Println(...)`
- `math.Sin(...)`, `math.Pow(...)`
- `os.MkdirAll(...)`, `filepath.Join(...)`
- `strings.Contains(...)`
- `strconv.ParseFloat(...)`

Use exposed mumax3 functions directly instead: `Print`, `Sprintf`, `sin`, `pow`, `sqrt`, `Vector`, `SaveAs`, `TableAdd`, and so on. Use Python for filesystem work, CSV/JSON parsing, path joins, plotting, or batch orchestration.

## Invented API Names

Do not invent convenience APIs such as:

- `SetMaterial(...)`
- `SetExternalField(...)`
- `SetOutput(...)`
- `SetDampingRegion(...)`
- `RunSimulation(...)`
- `CreateMask(...)`

Check `api_index.md` first. If absent there, check `api_full.md` or the official API page before using a name.

## Arithmetic And Assignment Traps

- Use `pow(x, y)` for powers. In Go-like syntax `^` is not exponentiation.
- Prefer single assignment: `x := 1`, not `x, y := 1, 2`.
- Avoid `%` unless confirmed for the exact mumax3 version; prefer `mod(x, y)` or `remainder(x, y)` when a floating remainder is intended.
- Do not store time-dependent expressions in ordinary variables unless one-time evaluation is intended.

Correct dynamic field pattern:

```go
B_ext.Add(mask, h0*sin(2*pi*f*t))
```

Risky if a dynamic value was intended:

```go
value := h0*sin(2*pi*f*t)
B_ext.Add(mask, value)
```

## Region And Output Traps

- Regions are mutually exclusive cell labels. Later region definitions can overwrite earlier intent.
- Save `regions` when debugging spatial assignments.
- Do not assume output files land in the working directory; mumax3 creates an output directory for a script run.
- Include at least one final `Save`/`SaveAs` or an autosave/table schedule for scripts meant to produce data.

