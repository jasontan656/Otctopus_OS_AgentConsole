# Mother_Doc

<!-- octopus:status:start -->
## Document Status
doc_path: README.md
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

`docs/` is the authored-document mirror root inside the `Mother_Doc` container for `Octopus_OS`.

## Core Positioning

- It is the sole authored-document root for `Octopus_OS`.
- The `Octopus_OS/Mother_Doc/` container root itself is reserved for code/runtime assets and does not act as the docs root.
- It mirrors the deployed container set 1:1 through same-named container directories.
- Its directory tree is also the future Admin Panel visualization tree.
- Runtime consumers must use the document access API defined by the `Mother_Doc` container; direct file reads are not the consumption model.
- Each container entry must first expose a stable abstraction layer under `common/`.
- Every non-`AGENTS.md` document carries `Document Status + Block Registry` so document-side changes can be detected mechanically.
- `Mother_Doc/common/development_logs/` carries implementation batches and deployment checkpoints as the internal delivery timeline inside the docs tree.
- The delivery timeline is designed to close with Git / GitHub: the local log keeps the summary, and Git history carries the concrete file/code changes.

## Entry Shape

- `README.md`: mirror-root explanation.
- `AGENTS.md`: mirror-root recursive index; this file class exists only inside `docs/`.
- `Mother_Doc.md`: scope-entity document for the root `Mother_Doc` directory itself.
- same-named container directories: the primary authored-document entry shape.
- `Mother_Doc/Mother_Doc/README.md`: the self-description purpose doc for the `Mother_Doc` container itself.
- `Mother_Doc/Mother_Doc/AGENTS.md`: the self-description recursive index for the `Mother_Doc` container itself.

## Container Mirror Directories

- `Mother_Doc/`
- `User_UI/`
- `Admin_UI/`
- `API_Gateway/`
- `Identity_Service/`
- `Account_Service/`
- `Order_Service/`
- `Payment_Service/`
- `Notification_Service/`
- `File_Service/`
- `AI_Service/`
- `Postgres_DB/`
- `Redis_Cache/`
- `MQ_Broker/`
- `Object_Storage/`

These names mirror the workspace container directories 1:1.

Boundary rule:

- `AGENTS.md` only exists in `Octopus_OS/Mother_Doc/docs/**`.
- Actual workspace containers such as `Octopus_OS/User_UI/` or `Octopus_OS/Order_Service/` do not carry `AGENTS.md`.

Special case:

- `Mother_Doc/Mother_Doc/` is the authored documentation node for the `Octopus_OS/Mother_Doc/` container itself.
- Read this file first for root purpose, then use the peer `AGENTS.md` to choose the next scope, and use `Mother_Doc.md` to understand the root directory as an authored object.
