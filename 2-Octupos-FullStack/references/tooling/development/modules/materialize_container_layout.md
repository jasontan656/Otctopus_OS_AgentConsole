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
