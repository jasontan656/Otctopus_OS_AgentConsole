# materialize_container_layout

## Purpose

- Materialize the container directory under `Octopus_OS/`.
- Materialize the same-named document directory under `Octopus_OS/Mother_Doc/`.

## Boundary

- The tool does not infer project semantics.
- AI must decide the container set before calling the tool.

## Naming Guardrails

- Container names must be readable and filesystem-safe.
- Avoid `Shared_*`, `Business_*`, and `Runtime_*`.
- `Mother_Doc` is a special self-reference case: workspace path stays `Octopus_OS/Mother_Doc/`, while the document entry is `Octopus_OS/Mother_Doc/Mother_Doc/`.
