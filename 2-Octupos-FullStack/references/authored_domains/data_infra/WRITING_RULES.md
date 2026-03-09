# Data Infra Writing Rules

- Data/infra family owns resource, namespace, ownership-boundary, and client-boundary authored-doc updates.
- Do not normalize these rules into generic service rules.
- Data/infra docs must preserve explicit resource ownership and access-policy boundaries.
- Data/infra container docs must explicitly split authored content into `overview/`, `features/`, `shared/`, and `common/`.
- `shared/` carries access policy, client boundary, and cross-container dependency material; `features/` carries concrete operational capabilities and outstanding rollout questions.
