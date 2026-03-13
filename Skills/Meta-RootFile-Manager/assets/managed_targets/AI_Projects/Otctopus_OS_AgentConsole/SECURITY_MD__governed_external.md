---
doc_id: meta_rootfile_manager.assets_managed_targets_ai_projects_otctopus_os_agentconsole_security_md_governed_external
doc_type: topic_atom
topic: Security Policy
anchors:
- target: ../../../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# Security Policy

## Current Risk Posture

Octopus OS is not a low-permission automation tool.

At the current phase, the intended operating model assumes:

- autonomous AI execution with no approval step during task flow
- full danger access to the working environment
- complete tool access for the AI operator
- a WSL2 Linux-only operating assumption
- no tested or supported adapters for macOS, native Windows, containers, or other environments

If that operating model is unacceptable for your machine or your project, do not install Octopus OS.

## Installation Boundary

The current installation model is directory-level, not system-level.

That reduces blast radius compared with system-wide installation, but it does not make the project low-risk.

The installed runtime can still:

- change AI behavior
- change AI decision patterns
- change tool usage patterns
- alter how the AI plans and executes work

Because of that, first-time use is not recommended on top of an existing live project that you care about.

Use a fresh dedicated target path first.

## Runtime Requirements

The currently intended runtime is:

- Codex CLI
- GPT-5.4 with high reasoning effort
- WSL2 Linux
- full tool access
- no-approval command execution

Other models, other environments, and reduced-permission sandboxes are not claimed to be equivalent.

## GitHub Risk Boundary

Octopus OS may be configured to let AI drive GitHub operations.

That means:

- a fresh GitHub account is strongly recommended
- if you do not use a fresh account, back up and clear the existing account state before binding it
- never bind an account that still contains assets you are not prepared to expose to an AI-driven workflow

## Reporting Security Issues

This repository does not currently publish a private security reporting channel.

For now:

- use the repository issue area
- redact secrets, keys, tokens, internal addresses, and private infrastructure details
- report the smallest reproducible description that is still useful

If a private reporting path is introduced later, this file should be updated.
