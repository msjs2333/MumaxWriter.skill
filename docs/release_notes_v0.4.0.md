# Release Notes: v0.4.0

Release date: 2026-10-31

## Paper to phenomenon

The skill now provides an optional [paper-reconstruction workflow](../skills/mumax3/references/paper_reconstruction.md): choose a target figure, recover a small model and preparation sequence, run, and adjust toward the observed shape and trend. Missing secondary parameters can use reasonable assumptions with brief notes. Quantitative comparison is available when useful; exploratory reconstruction is the default.

The installed [DMI edge-canting example](../skills/mumax3/examples/paper_edge_canting/README.md) follows Rohart & Thiaville (2013), Fig. 1. It includes original MuMax3 input, spatial OVF analysis, a plot from real simulation and a short result note. Increasing DMI increases the opposite edge tilts; reversing DMI reverses their directions. The example separates paper values from demonstration choices and explains the DMI sign convention.

The main skill adds one routing entry. Existing tutorial analysis retains its defaults, while the new spatial analyzer supports one-case pilots and small comparisons. English, Chinese and Japanese READMEs are updated. The skill continues to target MuMax3.

## Validation

Independent review and execution checked the feature commit. Checks covered 22 regressions, 11 real engine vet checks, resources and links. The unpacked skill's analysis CLI also handled one, two and three cases. An independent GPU run completed all four 128-cell preparations in 3.60 seconds and reproduced the edge-canting trend. The repository has no configured CI; these are local and independent execution results.

The example reconstructs the selected local-energy phenomenon without claiming a digitized-figure fit or full-dipolar reproduction. See its result note for model choices, measurements and the generated profile plot.
