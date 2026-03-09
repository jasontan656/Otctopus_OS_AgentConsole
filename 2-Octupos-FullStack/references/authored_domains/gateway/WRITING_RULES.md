# Gateway Writing Rules

- Gateway docs own routing, upstream, auth-forwarding, and traffic-boundary updates.
- Do not normalize gateway authored-doc updates into generic service rules.
- Gateway writing updates must stay aligned with route prefixes and upstream aliases in the same container common layer.
- Gateway container docs must explicitly split authored content into `overview/`, `features/`, `shared/`, and `common/`.
- `shared/` is mandatory for gateway API surfaces, upstream bindings, and cross-container traffic contracts.
