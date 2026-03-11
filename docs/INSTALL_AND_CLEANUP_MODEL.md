# Install And Cleanup Model

## Goal

The public trial surface must eventually support:

- one-command install
- overwrite warnings before install
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

## Current Install Surface

The intended public trial install surface is command-line-first and one-line callable:

```bash
python3 product_tools/octopus_os_agent_console.py install --runtime-target codex-gpt-5.4-high --codex-root ~/.codex/skills --workspace-root ~/Octopus_OS_Agent_Console && codex -C ~/Octopus_OS_Agent_Console -m gpt-5.4 -c 'model_reasoning_effort="high"'
```

`wizard` may still exist as a guided TUI, but the canonical install path is the single-line CLI entry above.

## Hard Install Gate

Install must refuse to continue unless both conditions are true:

1. the target skills root matches a Codex-style directory shape such as `.../.codex/skills`
2. the operator explicitly targets `codex-gpt-5.4-high`

If either condition fails, install should stop instead of trying to adapt to another runtime layout or another model stack.

## Minimum Model

The installer has to manage two targets at the same time:

1. `~/.codex/skills`
2. a user-selected Octopus OS workspace directory

The two targets have different contents by design:

- `~/.codex/skills` receives only syncable skill roots and `.system/`
- the workspace receives the full product mirror, including the repository root `AGENTS.md` and `Skills/AGENTS.md`
- accidental root-level files such as `~/.codex/skills/AGENTS.md` must be removed instead of preserved

## Required Output Before Install

- which skills will be synced
- which same-name skills will be overwritten
- where the workspace will be created
- which objects cleanup will remove or restore

## Cleanup Must Be Manifest-Driven

Cleanup must never guess which files "probably belong to Octopus OS".

It must rely on an install-time manifest that records:

- install session id
- codex root
- workspace root
- installed skill list
- overwritten skill backups

## Current Implementation Status

The repository already contains a product installer entrypoint at `product_tools/octopus_os_agent_console.py`.

Current capabilities:

- `plan`
- `install`
- `uninstall`
- `wizard`

Current behavior already includes:

- skill root discovery
- overwrite warnings
- workspace mirror creation
- root `AGENTS.md` and `Skills/AGENTS.md` deployment into the workspace mirror
- cleanup of forbidden root-level files accidentally present in `~/.codex/skills`
- manifest persistence
- manifest-driven uninstall
- a bilingual terminal wizard for end users
- explicit warning surfaces for the current unstable phase should remain part of the install experience

Future enhancements can still add:

- finer conflict detection
- user modification detection
- rollback audit output
