# Install And Cleanup Model

## Goal

The public trial surface must eventually support:

- one-command install
- overwrite warnings before install
- one-command cleanup
- no accidental deletion of unrelated user files

## Minimum Model

The installer has to manage two targets at the same time:

1. `~/.codex/skills`
2. a user-selected Octopus OS workspace directory

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
- manifest persistence
- manifest-driven uninstall
- a bilingual terminal wizard for end users

Future enhancements can still add:

- finer conflict detection
- user modification detection
- rollback audit output
