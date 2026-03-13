# Third-Party Components

## GitNexus-Derived Core In `Meta-code-graph-base`

The `Meta-code-graph-base` skill includes a vendored and modified upstream core at:

- `Skills/Meta-code-graph-base/assets/gitnexus_core`

That directory is derived from the `gitnexus/` core in the upstream `GitNexus` project:

- Upstream project: `GitNexus`
- Upstream repository path used for comparison: `Human_Work_Zone/GitNexus/gitnexus`
- Current purpose in Octopus OS: local code-graph engine core used by `Meta-code-graph-base`

## Current Integration Shape

The Octopus OS skill does not present `gitnexus_core` as an original implementation.
It is a governed migration of the upstream engine with local wrapping and product-specific trimming.

The current integration keeps the upstream parsing and graph engine as the base, while Octopus OS adds or changes:

- local runtime routing into a caller-provided graph runtime root
- a Python wrapper entrypoint in `scripts/meta_code_graph_base.py`
- local resource URIs, map output, and wiki bundle output
- removal of the upstream web, plugin, eval, setup, serve, and MCP transport shell from the skill surface

## License And Notice Boundary

The repository root is MIT-licensed for original repository content, but that does not replace separate notices carried by embedded third-party components.

For the vendored `gitnexus_core` directory:

- upstream license: `PolyForm Noncommercial 1.0.0`
- required attribution notice is preserved in the vendored directory notice file
- distribution and modification of that component must follow its upstream license terms

See:

- `Skills/Meta-code-graph-base/assets/gitnexus_core/LICENSE`
- `Skills/Meta-code-graph-base/assets/gitnexus_core/NOTICE`

## Repository-Level Clarification

When this repository is published or shared, `Meta-code-graph-base` should be understood as including migrated and modified core code from `GitNexus`, not as a fully independent clean-room implementation of the code-graph engine.
