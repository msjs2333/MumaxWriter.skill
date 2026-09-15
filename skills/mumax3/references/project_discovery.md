# Project Discovery

Use this reference when changing or extending an existing mumax3 project.

## Read The Smallest Relevant Context

Start with the user's request, the affected `.mx3` source or template, and the task documentation that defines its active
parameters. Add only the records needed for the decision:

- status or a plot: the declared status, manifest, and relevant analysis or plot profile;
- a physics, protocol, or mesh change: the active source, parameter provenance, and applicable API reference;
- checkpoint reuse: the input identity plus its physical role, preparation protocol, material/geometry compatibility, and
  permitted downstream protocol;
- a scientific conclusion or child case: the evidence and decision criteria relevant to that conclusion.

Preserve unrelated work. Repository-local task instructions and current source override bundled examples.

## Resolve Conflicts Deliberately

Historical scripts and planning notes can explain a project, but are not automatically current inputs or evidence that a run
completed. When sources disagree, prefer the active task source and its case record, check the result summary where needed,
and report an unresolved conflict before changing physical behavior.

Do not infer a material model, mesh, field, initial state, or analysis convention from an older case merely because it is
nearby. Keep enough provenance to distinguish a byte-identical reused state from one that is also physically suitable for
the new protocol.

## Keep Project Context Project-Local

A project may maintain a short navigation document linking its active tasks, sources, results, and historical records. It
should help an agent find the relevant material, not require every request to load the entire project history. Keep detailed
storage, execution, and retention procedures with the project that uses them.
