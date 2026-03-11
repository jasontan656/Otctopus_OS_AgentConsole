#!/usr/bin/env bash
set -euo pipefail

stage="${1:-}"
if [[ -z "$stage" ]]; then
  echo "USAGE: $0 <TURN_START|ROUTE|READ_EXEC|WRITE_EXEC|TURN_END>" >&2
  exit 2
fi

print_common_header() {
  local s="$1"
  echo "[STAGE_PRINT] stage=${s}"
}

case "$stage" in
  TURN_START)
    print_common_header "TURN_START"
    echo "[DO][Meta-mindchain] architect-first, assess whole-system impact and base-layer cleanliness before solution"
    echo "[DO][Meta-mindchain] if user request harms architecture stability, explicitly refuse and propose a cleaner path"
    echo "[DONT][Meta-mindchain] no local-only patching, no dead-code/compatibility-shell retention, no compliance on architecture-conflicting requests"
    echo "[DO][Meta-reasoningchain] use single-layer chain before advice: clarify/assumptions/evidence/alternatives/future/consequences/pilot"
    echo "[DONT][Meta-reasoningchain] unless NO_FUTURE_PROJECTION, do not skip full chain (especially evidence/future/rollback thresholds)"
    echo "[DO][Meta-prompt-write] if prompt/instruction text changes, run filter script and print structured intent block"
    echo "[DONT][Meta-prompt-write] no unstructured free-form prompt rewrite without mode decision"
    ;;
  ROUTE)
    print_common_header "ROUTE"
    echo "[DO][Routing] classify branch by disk-write intent (read-only vs non-read-only)"
    echo "[DONT][Routing] do not enter read-only branch if any create/modify/delete/move/rename may occur"
    echo "[DO][Meta-browser-operation] if browser task, choose exactly one mode: headless or headed"
    echo "[DONT][Meta-browser-operation] do not mix headless and headed workflows in same branch"
    ;;
  READ_EXEC)
    print_common_header "READ_EXEC"
    echo "[DO][Read-only] read/retrieve/analyze/report only"
    echo "[DONT][Read-only] no disk writes"
    echo "[DO][Meta-reasoningchain] keep claim/support/unknowns per step in single-layer reasoning outputs"
    echo "[DONT][Meta-keyword-first-edit] do not run edit flow in read-only branch"
    ;;
  WRITE_EXEC)
    print_common_header "WRITE_EXEC"
    echo "[DO][Meta-keyword-first-edit] replacement-first; print old->new->reason before additive edits"
    echo "[DONT][Meta-keyword-first-edit] no additive-first edits when replacement can satisfy intent"
    echo "[DO][Meta-refactor-behavior] define OEC (consumer/observables/invariants/witness) before refactor"
    echo "[DONT][Meta-refactor-behavior] do not change observable behavior unless in allowed_deltas"
    echo "[DO][Meta-github-operation] if this write turn touched Octopus_OS or octopus-os-agent-console, finish same-turn GitHub traceability before closing"
    echo "[DONT][Meta-github-operation] do not defer required repo traceability to a later turn"
    ;;
  TURN_END)
    print_common_header "TURN_END"
    echo "[DO][Closure] verify branch obligations and print completion evidence"
    echo "[DONT][Closure] do not skip required hooks"
    echo "[DO][Meta-github-operation] verify required commit-and-push traceability is complete for each affected repo"
    echo "[DONT][Meta-github-operation] do not close a write turn with missing required repo traceability"
    ;;
  *)
    echo "INVALID_STAGE: $stage" >&2
    exit 2
    ;;
esac
