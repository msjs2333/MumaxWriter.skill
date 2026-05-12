# mumax3 Script Language Subset

mumax3 scripts are parsed with Go syntax but compiled by a small interpreter. A syntactically valid Go fragment may still be rejected by mumax3.

## Supported Basics

- Case-insensitive API identifiers: `msat`, `Msat`, and `MSAT` refer to the same API object.
- Variables: `x := ...` declares a new variable; `x = ...` assigns an existing variable.
- Basic literals: integers, floats, strings, booleans through predefined `true` and `false`.
- Blocks introduce scope.

## Supported Statements

- Empty statements.
- Expression statements: `Print(x)`, `Save(m)`.
- Single assignment: `=`, `:=`, `+=`, `-=`.
- Increment/decrement: `i++`, `i--`.
- `if` / `else`.
- Basic `for` loops, including omitted init/condition/post.

Avoid `switch`, `select`, `range`, `return`, `defer`, `go`, `break`, `continue`, labels, and declarations.

## Supported Expressions

- Identifiers.
- Basic literals.
- Binary expressions: `+`, `-`, `*`, `/`, comparisons, `&&`, `||`.
- Unary expressions: `-x`, `!ok`.
- Function calls and method calls.
- Parenthesized expressions.
- Index expressions for slices/arrays.

Use `pow(x, y)` for powers. Use `mod` or `remainder` for remainder-like operations.

## Time-Dependent Values

If an API accepts a function, mumax3 may implicitly convert an expression into a re-evaluated function. Do not store time-dependent expressions in ordinary variables unless a one-time evaluation is intended.

Correct for dynamic material/field inputs:

```go
B_ext.Add(mask, h0*sin(2*pi*f*t))
```

Potentially static if evaluated first:

```go
value := sin(2*pi*f*t)
B_ext.Add(mask, h0*value)
```
