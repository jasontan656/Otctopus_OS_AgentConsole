# materialize_container_layout

## Purpose

- Materialize the container directory under `Octopus_OS/`.
- Materialize the same-named document directory under `Octopus_OS/Mother_Doc/`.
- Materialize the stable `common/` abstraction layer for the container family.

## Boundary

- The tool does not infer project semantics.
- AI must decide the container set before calling the tool.

## Behavior

- `Mother_Doc` is a special self-reference case: workspace path stays `Octopus_OS/Mother_Doc/`, while the authored entry lives at `Octopus_OS/Mother_Doc/Mother_Doc/`.
- Every authored container entry gets `README.md + common/`.
- `common/` is split into `architecture/`, `stack/`, `naming/`, `contracts/`, and `operations/`.
- The exact markdown files are selected from one of five container families:
  - `Mother_Doc`
  - `UI`
  - `Gateway`
  - `Service`
  - `Data_Infra`

## Naming Guardrails

- Container names must be readable and filesystem-safe.
- Avoid `Shared_*`, `Business_*`, and `Runtime_*`.
- Preferred stage-1 suffixes are `_UI`, `_Gateway`, `_Service`, `_DB`, `_Cache`, `_Broker`, and `_Storage`.
