# project_baseline

<!-- octopus:status:start -->
## Document Status
doc_path: Mother_Doc/project_baseline/README.md
doc_role: scope_purpose
doc_lifecycle_state: modified
doc_requires_development: true
doc_sync_status: modified
last_updated_stage: mother_doc
change_detection_mode: block_registry

## Block Registry
- block_id: primary
  lifecycle_state: modified
  requires_development: true
  sync_status: modified
  last_updated_stage: mother_doc
<!-- octopus:status:end -->

This directory is the always-load project baseline for Octopus OS.

## 1. Purpose

- It sits above concrete container scopes.
- Read this scope before deciding which containers are affected by the current requirement.
- It carries the project-wide operating model, current development baseline, impact pruning rule, and dynamic growth rule.

## 2. Reading Order

- Read `project_baseline.md` for the scope entity.
- Read the leaf baseline documents in this directory before entering `Admin_UI`, `Mother_Doc`, or any other container scope.
- Return to the peer `AGENTS.md` when you need the next exact file path.

## 3. Maintenance Rule

- If the current project objective, likely impact surface, or dynamic growth rule changes, this directory must be updated first.
- Container-local docs come after the project baseline, not before it.
