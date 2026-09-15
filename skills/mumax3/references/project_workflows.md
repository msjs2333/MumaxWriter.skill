# Project Workflow Patterns

Use this reference for multi-stage or multi-case simulation projects.

## Stages And Reuse

Make the inputs, generated scripts, outputs, and result of each meaningful stage identifiable. A task may offer separate
prepare, run, postprocess, status, or summary commands, but its public behavior and rerun policy should be clear. Preserve a
completed case unless the requested rerun policy permits replacement.

When stages or people can write the same mutable output, coordinate a single writer and leave readers able to distinguish
missing, incomplete, and completed results. The choice of lock, process tracking, storage layout, cancellation, monitoring,
or recovery mechanism belongs to the project.

For a reused initial state, record both content provenance and the physical role: its preparation field/protocol,
material/geometry identity, source task, and allowed downstream use. A matching hash or filename alone does not establish
physical suitability.

## Evidence And Review

State the scientific question before choosing frames, vector components, thresholds, windows, or analyses. Sampling and
evidence must be sufficient for that question: a display image or final frame can be useful, but is not automatically enough
for a switching, orientation, topology, or time-dependent conclusion.

Keep automated measurements, their freshness/limitations, and human scientific classifications distinct. A tracker gap or
partial analysis is evidence to investigate, not by itself a physical label. Where an automated result controls a later
stage, document the applicable criteria and retain the supporting evidence; apply checks to the relevant dependencies rather
than requiring an unrelated full project history.

## Verification

Use a dry run, small smoke case, static checks, or `mumax3 -vet` when they address the change. They establish rendering and
environment readiness, not physical correctness or numerical convergence. Test planning, reuse, and postprocessing with
temporary data; reserve real engines, large OVF processing, and full plots for integration checks when warranted.

## Regions, Masks, And Staged Drives

Each cell has one region label. A later `DefRegion` can replace an earlier absorber or material region, so inspect overlap
deliberately. Save `regions` when it will help diagnose a nontrivial layout or support later reuse. When independent spatial
fields must overlap, consider an OVF mask, `LoadFile`, or a custom quantity instead of forcing every property through the same
region map.

For local anisotropy, spin-current, or field schedules:

- save the mask or initial state when it supports debugging, reuse, or the planned analysis;
- keep ramp, hold, switch-off, and recovery phases explicit;
- use `RemoveExtraTerms()` before rebuilding staged extra fields;
- document whether `J` is a charge-current density or an effective spin-current input;
- validate `FixedLayer`, `FixedLayerPosition`, thickness, polarization, and torque-disable flags against the installed version.
