# IMPACT_SELECTION_BASELINE

- Start from `default_all_relevant`, not from a guessed short list.
- The first pass must assume the current user requirement can touch all project containers, shared contracts, and evidence surfaces.
- Then prune by ranking `highest_probability_unrelated -> next_highest_probability_unrelated`.
- Do not exclude a container or domain unless there is a readable semantic reason for exclusion.
- For UI-facing requests, do not stop at the UI container; evaluate backend services, API gateway, data, shared contracts, graph consumption, and observability before pruning.
