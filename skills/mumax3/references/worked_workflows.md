# Worked workflows

Choose a case by the decision it teaches. All files below are included when installing the `mumax3` skill; repository-level prompts remain separate evaluation material.

| Question | Worked case | Evidence and limit |
| --- | --- | --- |
| Must each parameter step inherit the previous state? | [Continuous hysteresis](../examples/hysteresis/README.md) | Branch ordering and switching fields against a macrospin energy model; not an independent-case grid. |
| Does a transient simulation reproduce a specified problem? | [Standard Problem 4](../examples/standard_problem4/README.md) | Reversal trajectory and first-crossing field snapshot; reference comparison and mesh convergence are separate checks. |
| How do outputs become an observable? | [Pulsed macrospin FMR](../examples/fmr/README.md) | Time sampling, windowed spectrum and analytic frequency; not a spatial spin-wave model. |

For a paper-driven task, start with [paper reconstruction](paper_reconstruction.md) and its [DMI edge-canting case](../examples/paper_edge_canting/README.md). That case uses a separate spatial-profile analyzer and a short result note, without a reproduction score.

Read the selected case's assumptions and acceptance criteria before adapting it. Keep the initial state/protocol when comparing runs; change mesh at fixed physical dimensions for convergence, and change observation time at fixed cadence for frequency resolution. Parameter changes can invalidate an analytic comparison even if the script still runs.

The companion `scripts/analyze_tutorial.py` reads native MuMax3 tables, verifies the documented output contract, and writes CSV plus a JSON summary. Analysis-specific scalar parameters are recorded by the `.mx3` into table columns, rather than separately copied into analysis defaults. Preserve the input script and engine version for the full model and solver settings. OVF checks establish file presence and header only; open the field maps separately to assess their contents. Its checks are deliberately specific to these three cases. Do not use a passing tutorial check as acceptance of an unrelated research model.

Run cases in a new scratch directory. Scripts write `m_initial.ovf`, `m_final.ovf` and `table.txt`; SP4 also saves the first sampled reversal state. Read each README for commands and additional conditions. The analysis requires Python 3.10+ with the standard library. The actual engine, including ordinary `-vet`, initializes CUDA; CPU-only tests check generation and synthetic analysis without claiming an engine run.
