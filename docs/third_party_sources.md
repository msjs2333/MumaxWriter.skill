# Third-Party Sources And Provenance

This repository uses external projects as documentation and coverage references. The tracked examples and templates are intended to be original repository content unless a file explicitly says otherwise.

## Reference Sources

- mumax3 homepage: https://mumax.github.io/
- mumax3 examples: https://mumax.github.io/examples.html
- mumax3 API: https://mumax.github.io/api.html
- mumax3 repository: https://github.com/mumax/3
- Ubermag documentation: https://ubermag.github.io/documentation/index.html
- Fidimag user guide: https://fidimag.readthedocs.io/en/latest/user_guide/index.html
- OOMMF user guide: https://math.nist.gov/oommf/doc/userguide21a1/userguide-xml/userguide.html
- MicroMagnetic.jl documentation: https://magneticsimulation.github.io/MicroMagnetic.jl/stable/
- OpenAI skills catalog: https://github.com/openai/skills

## Repository Policy

- Use external projects to decide coverage, terminology, validation expectations, and documentation structure.
- Prefer original `.mx3` examples written for this repository.
- Do not copy third-party example scripts into this Apache-2.0 repository unless license compatibility, attribution, and required notices are reviewed explicitly.
- Keep any downloaded external caches outside the public release snapshot.

## `api_full.md` Provenance

`skills/mumax3/references/api_full.md` is a structured fallback reference derived from the official mumax3.12 API page. It is useful for review tasks and disputed identifiers.

For `v0.1.0`, `api_full.md` is kept in the repository as a sparse identifier/signature index with clear provenance. It is not a replacement for official mumax3 API documentation.

Future versions may replace it with a generator or a smaller original summary if maintenance or licensing requirements change.

## Paper reconstruction example

The [edge-canting example](../skills/mumax3/examples/paper_edge_canting/README.md) uses physical parameters and the selected phenomenon from Rohart & Thiaville, Phys. Rev. B 88, 184422 (2013), [public full text](https://arxiv.org/html/1310.0666v1), Sections II and III A / Fig. 1. The repository supplies its own MuMax3 implementation, analysis and plot generation; it does not redistribute the article, its figures or other authors' code. See the example for parameter choices and the mapping to MuMax3's DMI convention.
