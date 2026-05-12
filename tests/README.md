# Release Validation

Run the local release-candidate checks from the repository root:

```powershell
python tests\validate_release.py
```

The validator uses only the Python standard library. It checks helper script compilation, basic skill metadata, template parameter examples, static warnings for expected-output `.mx3` files, optional `mumax3 -vet`, and a small tracked-file sensitive-term scan.

