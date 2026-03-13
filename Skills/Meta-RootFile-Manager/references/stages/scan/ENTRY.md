---
doc_id: meta_rootfile_manager.references_stages_scan_entry
doc_type: topic_atom
topic: Scan Instruction
anchors:
- target: ../../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# Scan Instruction

> Active stage semantics. Executable scan tooling exists.

- Discover which files are under this skill's managed boundary.
- Load scan match rules from external rule assets instead of hardcoding all rules in code.
- Restrict the active result set to the exact governed source paths declared in the scan rule asset.
- Apply the disallowed list and exclude blacklisted domains such as `Octopus_OS`.
- Support both stdout output and json output.
- When json output is requested, tooling must write the result file into the corresponding `Codex_Skill_Runtime` folder.
- Run structure lint for every discovered managed file before declaring the scan successful.
