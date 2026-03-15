---
doc_id: dev_projectstructure_constitution.references_runtime_contracts_skill_runtime_contract
doc_type: topic_atom
topic: Dev-ProjectStructure-Constitution Runtime Contract
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# Dev-ProjectStructure-Constitution Runtime Contract

- Primary runtime entry: `./.venv_backend_skills/bin/python Skills/Dev-ProjectStructure-Constitution/scripts/Cli_Toolbox.py contract --json`
- CLI JSON is the primary runtime source.
- `SKILL.md` remains a facade and narrative mirror.
- `Development_Docs/`、`Client_Applications/`、`Foundation_Bundle/`、and `Deploy_Guide/` are the authoritative top-level roots for the current `Octopus_OS` structure.
- `Mother_Doc/`, `Octopus_Hub/`, `System_Manifests/`, `Capability_Modules/`, `Integration_Adapters/`, `Infra_Contracts/`, and `Deploy/` are no longer authoritative top-level roots in `Octopus_OS`.
- Project-wide development documentation, architecture notes, evidence, current frontend product mother_doc, and graph/runtime indexes should live in `Development_Docs/`, `README.md`, or an owning object's `Development_Docs/`.
- The single frontend implementation root lives directly in `Client_Applications/`; `Client_Applications/Unified_Portal/` and `Client_Applications/*/Development_Docs/` are no longer valid for the current Octopus_OS phase.
- All backend modules, adapters, and infrastructure contracts should converge under `Foundation_Bundle/`; deployment scripts, gatekeeping, and CI should converge under `Deploy_Guide/`.
- Object roots express object identity only; project-structure governance must not pre-create abstract role directories such as `Common/` and `Core/` unless a downstream domain contract explicitly reintroduces them for a real internal architecture reason.
- At project-structure level, each service/module object root may pre-create only one fixed child directory: `Development_Docs/`.
- `Assets/` and `Channels/` are no longer valid default object-level child directories in the Octopus_OS structure constitution.
- `Foundation_Bundle` capability directories use `Auth/`, `Payload/`, `Persistence/`, `Event_Task/`, `Cache/`, `Session_Context/`, `Policy_Enforcement/`, `Storage_Access/`, and `Audit_Observe/`; `*_Runtime` is no longer a valid object-level path suffix.
