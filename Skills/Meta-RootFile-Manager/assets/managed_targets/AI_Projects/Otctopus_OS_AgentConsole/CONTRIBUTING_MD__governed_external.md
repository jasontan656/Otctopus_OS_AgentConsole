---
doc_id: meta_rootfile_manager.assets_managed_targets_ai_projects_otctopus_os_agentconsole_contributing_md_governed_external
doc_type: topic_atom
topic: Contributing
anchors:
- target: ../../../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# Contributing

## Current Project State

Octopus OS is currently maintained as an AI-first project by the repository owner.

The development direction is not planned through a public roadmap-first process. It is driven by real usage, breakpoints, operating pain, and iteration pressure discovered during the author's own use of the system.

Because of that, this repository is not currently open to collaborative development.

## What Is Not Accepted Right Now

- pull requests for direct code changes
- collaborative feature branch development
- external refactors submitted as implementation proposals
- attempts to normalize the project toward generic multi-maintainer open-source workflows before the internal product shape is complete

## What Is Welcome Right Now

- product suggestions
- bug reports
- safety concerns
- documentation clarity issues
- operator experience feedback
- release-readiness feedback

Use the repository issue area for those suggestions.

## Why External Code Contribution Is Closed For Now

- the repository is still in a product-shaping phase
- the architecture is still changing very quickly
- a large portion of the development loop is AI-maintained and AI-operated
- the current internal workflow is intentionally optimized for rapid solo iteration, not for multi-maintainer coordination

When the internal development phase is considered complete enough, this policy may change and external contribution rules can be opened in a future revision of this file.

## Before Opening Any Suggestion

- read [README.md](README.md)
- read [SECURITY.md](SECURITY.md)
- do not paste secrets, keys, or private infrastructure details
- keep suggestions focused on observable behavior, operator workflow, or release quality
