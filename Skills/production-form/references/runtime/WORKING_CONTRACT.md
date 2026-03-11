# Production-Form Working Contract

## Purpose
- This file is the markdown audit surface for `WORKING_CONTRACT.json`.
- The machine-readable contract remains the runtime rule source.

## Core Role
- Keep the current Octopus OS product-shaping task continuously available to AI.
- Preserve a local markdown design history during the temporary rapid-iteration phase.
- Provide a stable handoff layer between current product-form work and future GitHub-first iteration logging.

## Current Product Focus
- Brand: `Octopus OS`
- Engineering repository: `octopus-os-agent-console`
- Positioning: natural-language-driven multi-agent console
- Current phase: rapid local product shaping for a solo operator before the full public product form stabilizes
- Near-term direction: shape a self-contained AI collaboration stack instead of depending on opaque external skill bundles
- Install surface: command-line-first and one-line callable
- Host environment boundary: support only the author's current Codex CLI + VS Code workflow
- Runtime boundary: provision a dedicated install root and derive the Codex skills directory as `<install-root>/.codex/skills`
- Model boundary: support only `Codex + GPT-5.4 high reasoning effort`; other models are unsupported and untested
- Install deployment boundary: first install the latest Codex CLI into the dedicated install root, require a clean Codex skills root, require a GitHub skill repository binding, sync only real skill roots into `<install-root>/.codex/skills`, remove accidental root-level `AGENTS.md`, and mirror both root `AGENTS.md` and `Skills/AGENTS.md` into the sibling workspace

## Logging Rule
- Read the current product intent before making new product decisions.
- Read the latest local iteration log before extending an existing design line.
- Append a local log entry whenever a real product-shaping decision is made.
- Do not use the local log for trivial command noise.

## Future Switch
- This skill is intentionally temporary.
- When the product form is complete enough, the main iteration history can gradually move back to GitHub commits and release-facing logs.
