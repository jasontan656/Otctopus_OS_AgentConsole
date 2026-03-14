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
    echo "[DO][Meta-Architect-MindModel] architect-first, assess whole-system impact and base-layer cleanliness before solution"
    echo "[DO][Meta-Architect-MindModel] if user request harms architecture stability, explicitly refuse and propose a cleaner path"
    echo "[DONT][Meta-Architect-MindModel] no local-only patching, no dead-code/compatibility-shell retention, no compliance on architecture-conflicting requests"
    echo "[DO][Meta-Reasoning-Chain] use single-layer chain before advice: clarify/assumptions/evidence/alternatives/future/consequences/pilot"
    echo "[DONT][Meta-Reasoning-Chain] unless NO_FUTURE_PROJECTION, do not skip full chain (especially evidence/future/rollback thresholds)"
    echo "[DO][Meta-Enhance-Prompt] if prompt/instruction text changes, run filter script and print structured intent block"
    echo "[DONT][Meta-Enhance-Prompt] no unstructured free-form prompt rewrite without mode decision"
    ;;
  ROUTE)
    print_common_header "ROUTE"
    echo "[DO][Routing] classify branch by disk-write intent (read-only vs non-read-only)"
    echo "[DONT][Routing] do not enter read-only branch if any create/modify/delete/move/rename may occur"
    echo "[DO][Meta-Agent-Browser] if browser task, start from browser-total-entry and escalate agent-browser -> headless -> windows headed only when needed"
    echo "[DONT][Meta-Agent-Browser] do not mix multiple browser runtimes in one branch without an explicit fallback reason"
    ;;
  READ_EXEC)
    print_common_header "READ_EXEC"
    echo "[DO][Read-only] read/retrieve/analyze/report only"
    echo "[DONT][Read-only] no disk writes"
    echo "[DO][Meta-Reasoning-Chain] keep claim/support/unknowns per step in single-layer reasoning outputs"
    echo "[DO][Meta-keyword-first-edit] keep runtime hook active all time; in read-only branch use it only as a no-write classification and edit-blocking hook"
    ;;
  WRITE_EXEC)
    print_common_header "WRITE_EXEC"
    echo "[DO][Meta-keyword-first-edit] keep runtime hook active all time and enforce delete > replace > add before any write"
    echo "[DO][Meta-keyword-first-edit] print old->new->reason before additive edits"
    echo "[DONT][Meta-keyword-first-edit] no additive-first edits when replacement can satisfy intent, even while the runtime hook stays continuously active"
    echo "[DO][Meta-refactor-behavior] define OEC (consumer/observables/invariants/witness) before refactor"
    echo "[DONT][Meta-refactor-behavior] do not change observable behavior unless in allowed_deltas"
    echo "[DO][Meta-github-operation] if this write turn touched Octopus_OS or Otctopus_OS_AgentConsole, finish same-turn GitHub traceability before closing"
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
