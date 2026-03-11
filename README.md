# Octopus OS

Octopus OS is a natural-language-driven multi-agent console.

It is being shaped for a solo operator building a complete AI collaboration stack from the ground up: development, deployment, operations, market work, workflow orchestration, multi-agent collaboration, and natural-language-driven execution.

This repository is the product foundation for Octopus OS. It has two responsibilities at the same time:

- Public product surface: positioning, installation model, workspace mirror, and product-facing documentation.
- Internal skill source of truth: the skill core still evolves here first and can still be pushed into `~/.codex/skills`.

## Current Status

- Stage: Alpha
- Intended use: learning, testing, and trial runs
- Not recommended yet for critical production workflows
- Supported runtime: Codex only
- Supported host environment: Codex CLI in the author's current Codex CLI + VS Code workflow only
- Supported model profile: GPT-5.4 with high reasoning effort only
- Other models are unsupported, untested, and may behave differently
- No other environment adapters are planned at the current phase
- A dedicated GitHub repository binding is required for Octopus OS skill evolution and Git automation
- The repository currently changes at a very high pace, often every 10 to 15 minutes
- Commit-by-commit reading is not a meaningful way to learn the system yet; use the higher-level product documents instead

## How To Read This Repository

This is not just a generic skill mirror.

A better model is:

- `Skills/`: the execution core of Octopus OS and the only syncable skill container
- `skill-mirror-to-codex`: the internal bridge that pushes skill roots into `~/.codex/skills`
- `docs/` and `product_tools/`: product surfaces that must stay outside the codex installation directory
- Git history: an externalized product iteration log

## Hard Boundaries

- Product-facing files may evolve here, but they must not pollute `~/.codex/skills`
- Skill roots must remain pushable through `skill-mirror-to-codex`
- Install and cleanup must stay manifest-driven instead of using guess-based deletion
- Installation now targets a dedicated Codex install root instead of reusing an arbitrary existing `~/.codex/skills`
- The target Codex skills directory must be clean before Octopus OS is installed; only Codex initial `.system` entries are allowed
- A dedicated GitHub skill repository binding is mandatory during installation
- Octopus OS provides directory-level installation only and does not provide system-level Codex installation
- The long-term target is a self-contained stack of skills and workflows owned by the product itself, reducing dependence on third-party skill installs and keeping AI behavior explicit, safe, and controllable

## Installation Modes

Mode 1: direct command-line install into a dedicated target path.

```bash
python3 product_tools/octopus_os_agent_console.py install --runtime-target codex-gpt-5.4-high --install-root ~/Octopus_Runtime/codex-home --github-skill-repo git@github.com:YOUR_ACCOUNT/octopus-os-skills.git --github-auth-mode ssh --acknowledge-github-control-risk && HOME=~/Octopus_Runtime/codex-home ~/Octopus_Runtime/codex-home/bin/codex -C ~/Octopus_Runtime/octopus-os-agent-console -m gpt-5.4 -c 'model_reasoning_effort="high"'
```

Mode 2: use an already system-installed Codex CLI only as the bootstrap tool.

1. Clone or pull this repository into a source directory.
2. Open Codex in that source directory.
3. Ask Codex to run the guided installation flow into your chosen dedicated target path.
4. After installation, enter the dedicated target path and use the directory-level Codex CLI from there.

The second mode still produces a directory-level Octopus OS runtime. It does not convert Octopus OS into a system-level install.

The installer will refuse to continue if:

- the runtime target is not explicitly acknowledged as `codex-gpt-5.4-high`
- the dedicated Codex skills root is not clean
- a GitHub skill repository binding is not provided
- the GitHub control risk warning is not explicitly acknowledged

Install behavior is intentionally narrow:

- it installs the latest Codex CLI into the dedicated install root by using the official npm package
- it uses that install root as the Codex home boundary and syncs only real skill roots into `<install-root>/.codex/skills`
- it removes any accidental root-level `<install-root>/.codex/skills/AGENTS.md`
- it creates a sibling `octopus-os-agent-console` workspace mirror, including the repository root `AGENTS.md` and `Skills/AGENTS.md`
- it captures a GitHub skill repository binding so Octopus OS can later drive its Git workflow
- it then launches a new Codex CLI session against the sibling workspace so the installed skill ecosystem is active immediately
- it does not write a system-level Codex installation for the user

GitHub binding warning:

- this machine flow is intentionally GitHub-controlling
- use a fresh GitHub account for Octopus OS, or fully back up and clear the existing account before binding it

## Entry Documents

- `docs/PRODUCT_IDENTITY.md`
- `docs/OPERATOR_AND_SECURITY_MODEL.md`
- `docs/SYNC_BOUNDARY.md`
- `docs/INSTALL_AND_CLEANUP_MODEL.md`
- `docs/PRODUCT_ITERATION_LOGGING.md`

## Directory Transition

The product engineering name is now `octopus-os-agent-console`.
Internally, this repository still acts as the governed source that maps syncable skill roots from `Skills/` into `~/.codex/skills`.

## Repository Layout

- `Skills/`: all skill roots, including `.system/`
- `docs/`: public product documentation
- `product_tools/`: installer and product-side utilities
- repository root: normal product repository entry files such as `README.md`, `AGENTS.md`, and future code or release metadata
