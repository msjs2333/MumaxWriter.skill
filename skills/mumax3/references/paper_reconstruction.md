# From a paper to a reproduced phenomenon

Use this workflow when the task starts from a paper or a figure. Default to an **exploratory reconstruction**: make the main phenomenon and its trend appear in a small, understandable simulation. A useful first result is a working model and an explanation of what controls it. Use a quantitative comparison when the relevant parameters are available or the user asks for it.

## Read toward one observable

Start with the target figure, its caption, and the methods or supplementary passages that explain it. Identify what changes, what is measured, and the preparation sequence. For a broad request, choose one central effect that the available backend can model and proceed. If the paper is unavailable, work from the supplied excerpt and identify the missing source briefly.

Translate the target into an observable: edge canting needs a spatial magnetization profile; switching needs a time trace; a resonance needs a spectrum; texture motion needs positions over time. Match the axes and units before comparing shapes. An average can cancel the local effect you want to see.

## Build the smallest useful model

Recover geometry, energy terms, material scales, boundaries, and the order **prepare → relax → drive → observe**. A static equilibrium figure may need only preparation and relaxation. Map terms to supported MuMax3 quantities using the existing API references. Keep the mechanism responsible for the effect; simplify dimensions, geometry or the parameter range when they are not the target.

Use reported values where available. For a missing damping, mesh or drive duration, choose a reasonable starting value and state it briefly as an assumption. Derive useful scales such as `sqrt(A/K_eff)`, a precession period or a propagation time to choose cells and duration. A short note beside the parameters is usually enough; missing secondary details do not need a questionnaire before the first run. Ask only when a choice changes the target itself or the required physics has no suitable implementation.

Reuse a nearby script or template, then change the model and protocol deliberately. Check SI units and order of magnitude, energy/sign conventions, and whether the saved quantity is actually the plotted observable. For example, do not add full demagnetization while keeping a reported effective anisotropy that already includes its local contribution.

## Run, inspect, adjust

Start with one small case and a useful control, such as removing or reversing the driving interaction. Use native continuation if the effect depends on its previous state; reset the initial state for independent comparisons. Save just the trace or field maps needed for the target, and extract the observable with a short analysis step.

Look first for the effect's existence, direction, spatial or temporal shape, and response to a control parameter. If it is absent, check preparation and relaxation, field/current direction, boundary conditions, and whether averaging hid it. If the shape is right but the scale differs, adjust the most relevant parameter or observation window. Change one physical explanation at a time with a few small runs, rather than launching a broad search.

For an exploratory result, explain the observed trend without imposing a universal error threshold or a full convergence campaign. If a quantitative question emerges, use the available paper values and compare that observable more closely; refine the mesh, timestep or preparation where it could explain the discrepancy.

## Keep a short result note

Four lines in the answer or example README are sufficient:

- **Target/source:** paper section or figure and the chosen phenomenon.
- **Model:** reported parameters plus the few assumptions or simplifications used.
- **Run/result:** what actually ran, the observed feature and a useful number or plot.
- **Next adjustment:** the most informative change, if the result still differs.

Keep assumed values distinct from reported ones, and actual simulation output distinct from an analytic sketch or synthetic test. See the [DMI edge-canting example](../examples/paper_edge_canting/README.md) for a complete paper-to-script-to-profile reconstruction.
