# Install And Cleanup Model

## Goal

The public trial surface must eventually support:

- one-command install
- clean-root validation before install
- one-command cleanup
- no accidental deletion of unrelated user files

## Current Trial Warning

The install flow is currently for local trial only.

Users should be warned that:

- the repository is changing extremely quickly
- the product is still structurally unstable
- installable does not mean stable
- each install may reflect a build that is superseded again within 10 to 15 minutes
- the product currently supports Codex only
- the current supported host environment is the author's Codex CLI + VS Code workflow only
- the product currently supports only GPT-5.4 with high reasoning effort
- other models are unsupported, untested, and may not behave equivalently
- no other environment adapters are planned at the current phase
- a dedicated GitHub repository binding is mandatory for Octopus OS to drive its future Git workflow
- operators should use a fresh GitHub account, or back up and clear the current account before binding it to this machine flow

## Current Install Surface

Octopus OS currently exposes two installation modes, but both of them remain directory-level installs.

Mode 1: direct one-line install:

```bash
python3 product_tools/octopus_os_agent_console.py install --runtime-target codex-gpt-5.4-high --install-root ~/Octopus_Runtime/codex-home --github-skill-repo git@github.com:YOUR_ACCOUNT/octopus-os-skills.git --github-auth-mode ssh --acknowledge-github-control-risk
```

Mode 2: attach an already available Codex CLI:

1. open Codex inside the repository source directory
2. ask Codex to follow the repository installation instructions and install into a dedicated target path
3. after installation, use the returned launch command to start Codex against the target-directory `console/` workspace

`wizard` may still exist as a guided TUI, but the canonical product artifact remains the same in both modes: a dedicated install root with a fixed internal Octopus OS directory layout.

## Hard Install Gate

Install must refuse to continue unless all conditions are true:

1. the operator explicitly targets `codex-gpt-5.4-high`
2. the dedicated install root can host a Codex home at `<install-root>/.codex`
3. the target Codex skills root is still clean, meaning it contains no previously installed user skills and at most Codex initial `.system` entries
4. a GitHub skill repository binding is provided
5. the GitHub control risk warning is acknowledged

If any condition fails, install should stop instead of trying to adapt to another runtime layout or another model stack.

## No System-Level Install

Octopus OS does not provide a system-level Codex installation mode.

Even when the operator already has a usable Codex CLI, that binary is only treated as an attach target for driving the dedicated Octopus OS runtime under the chosen install root.

The supported end state is still:

1. a dedicated directory-level Codex install root
2. a dedicated directory-level Codex skills root under that install root
3. a target-directory `console/` workspace mirror
4. target-directory runtime roots for skill runtime and skill results
5. a target-directory `Octopus_OS/` folder

## Minimum Model

The installer has to manage six targets at the same time:

1. a dedicated Codex install root such as `~/Octopus_Runtime/codex-home`
2. the derived Codex skills directory at `<install-root>/.codex/skills`
3. a `console/` workspace directory inside the target root, such as `~/Octopus_Runtime/codex-home/console`
4. a skill runtime directory at `<install-root>/Codex_Skill_Runtime`
5. a skill result directory at `<install-root>/Codex_Skills_Result`
6. an Octopus OS directory at `<install-root>/Octopus_OS`

The install surface now resolves the Codex CLI in this order:

- use `--codex-cli-bin` in attach mode when it is explicitly provided
- otherwise attach to `codex` when it already exists on `PATH`
- otherwise install the latest Codex CLI into the chosen install root

The two targets have different contents by design:

- the dedicated install root receives the latest Codex CLI package only when attach mode cannot be used
- when target-local Codex installation is required, npm cache/log/userconfig traces must stay under `<install-root>/.product_runtime/` instead of leaking into the operator home
- `<install-root>/.codex/skills` receives only syncable skill roots and `.system/`
- the target-directory `console/` workspace receives the full product mirror, including the repository root `AGENTS.md` and `Skills/AGENTS.md`
- `<install-root>/Codex_Skill_Runtime` and `<install-root>/Codex_Skills_Result` are created as governed runtime/result containers
- `<install-root>/Octopus_OS` is created as part of the installed baseline layout
- accidental root-level files such as `<install-root>/.codex/skills/AGENTS.md` must be removed instead of preserved
- the target-directory `console/` workspace also stores the GitHub repository binding metadata used by Octopus OS

## Required Output Before Install

- which skills will be synced
- whether the dedicated Codex skills root is still clean
- which Codex CLI strategy will be used and which binary path will launch the runtime
- where the workspace will be created
- which GitHub repository binding will be written
- which objects cleanup will remove or restore

## Cleanup Must Be Manifest-Driven

Cleanup must never guess which files "probably belong to Octopus OS".

It must rely on an install-time manifest that records:

- install session id
- install root
- codex root
- workspace root
- codex CLI install details
- target-local Codex CLI filesystem entries created during install
- installed skill list
- GitHub repository binding details
- overwritten skill backups if any legacy state had to be preserved

When install had to place Codex CLI artifacts into the target root, uninstall should consume that manifest and remove those recorded artifacts as part of the rollback instead of leaving `bin/`, `lib/`, or other target-local Codex remnants behind.

## Current Implementation Status

The repository already contains a product installer entrypoint at `product_tools/octopus_os_agent_console.py`.

Current capabilities:

- `plan`
- `install`
- `uninstall`
- `wizard`

Current behavior already includes:

- skill root discovery
- attach to an already available Codex CLI when possible
- dedicated Codex CLI installation into the chosen install root as a fallback
- clean-root validation before skill sync
- workspace mirror creation
- target-directory creation of `Codex_Skill_Runtime`, `Codex_Skills_Result`, and `Octopus_OS`
- root `AGENTS.md` and `Skills/AGENTS.md` deployment into the workspace mirror
- GitHub repository binding capture in the workspace runtime area
- cleanup of forbidden root-level files accidentally present in `<install-root>/.codex/skills`
- manifest persistence
- manifest-driven uninstall
- a bilingual terminal wizard for end users
- explicit warning surfaces for the current unstable phase should remain part of the install experience

Future enhancements can still add:

- finer conflict detection
- user modification detection
- rollback audit output
