# Mother_Doc Writing Rules

- Scope: `Octopus_OS/Mother_Doc/docs/**`.
- This family owns authored-doc tree shape, navigation shape, and docs-vs-container-root separation.
- `Octopus_OS/Mother_Doc/` is the code container root; authored docs live only under `docs/`.
- `graph/` is an asset root and must not be mixed into docs navigation.
- Every container doc directory must route authored content into:
  - `overview/` for human-observable summaries
  - `features/` for semantic feature coverage and unresolved requirements
  - `shared/` for API/event/shared-contract/cross-container dependency content
  - `common/` for stable abstract layers only
- Mother_Doc container writing must keep the core chain explicit:
  - `doc_code_authority`
  - `semantic_coverage_unit`
  - `mother_doc_container_architecture`
  - `os_graph_layer_model`
  - `cross_container_contract_baseline`
  - `evidence_minimum_witness`
- Those files are system-level authored contracts, not optional notes.
