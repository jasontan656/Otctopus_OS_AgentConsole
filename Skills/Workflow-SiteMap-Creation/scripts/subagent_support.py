from __future__ import annotations

import json
import os
import shlex
import time
from pathlib import Path

from cli_support import (
    BACKEND_PYTHON,
    JsonObject,
    REPO_ROOT,
    RESULT_ROOT,
    RUNTASK_CLI,
    SKILL_ROOT,
    SUBAGENT_RUN_ROOT,
    read_yaml,
    write_yaml,
    relpath,
    run_command,
    summarize_completed_process,
    write_json,
    write_text,
)


CODEX_BIN = os.environ.get("WORKFLOW_SITEMAP_CREATION_CODEX_BIN", "codex")
TMUX_BIN = os.environ.get("WORKFLOW_SITEMAP_CREATION_TMUX_BIN", "tmux")
RUNSTATE_TEMPLATE_ROOT = SKILL_ROOT / "references" / "runstates" / "templates"
SUBAGENT_PROMPT_TEMPLATE_PATH = SKILL_ROOT / "references" / "runtime_contracts" / "BACKGROUND_SUBAGENT_PROMPT_TEMPLATE.txt"


def _slug(text: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "_" for ch in text).strip("_") or "workflow_sitemap_creation"


def _subagent_prompt(factory_payload: JsonObject, enhanced_intent: JsonObject, workspace_root: str, task_runtime_file: str) -> str:
    final_intent = str(enhanced_intent["final_intent_output"]).strip()
    factory_excerpt = str(factory_payload.get("source_excerpt", "")).strip()
    template = SUBAGENT_PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")
    return template.format(
        final_intent=final_intent,
        skill_root=SKILL_ROOT,
        workspace_root=workspace_root,
        task_runtime_file=task_runtime_file,
        factory_excerpt=factory_excerpt,
        repo_root=REPO_ROOT,
    ).strip() + "\n"


def scaffold_runtask(factory_payload: dict[str, object], workspace_root: str | None = None) -> dict[str, object]:
    task_name = f"workflow_sitemap_creation_{factory_payload['source_digest'][:12]}"
    runtime_contract = run_command([str(BACKEND_PYTHON), str(RUNTASK_CLI), "runtime-contract", "--json"], cwd=REPO_ROOT)
    reading_chain = run_command(
        [str(BACKEND_PYTHON), str(RUNTASK_CLI), "read-contract-context", "--entry", "analysis_loop", "--json"],
        cwd=REPO_ROOT,
    )
    task_runtime_args = [str(BACKEND_PYTHON), str(RUNTASK_CLI), "task-runtime-scaffold", "--task-name", task_name, "--json"]
    workspace_scaffold_args = [str(BACKEND_PYTHON), str(RUNTASK_CLI), "workspace-scaffold", "--json"]
    if workspace_root:
        task_runtime_args.extend(["--workspace-root", workspace_root])
        workspace_scaffold_args.extend(["--workspace-root", workspace_root])
    task_runtime = run_command(task_runtime_args, cwd=REPO_ROOT)
    task_runtime_payload = json.loads(task_runtime.stdout)
    resolved_workspace_root = str(task_runtime_payload["workspace_root"])
    workspace_scaffold_args.extend(["--workspace-root", resolved_workspace_root, "--force"])
    workspace_scaffold = run_command(workspace_scaffold_args, cwd=REPO_ROOT)
    return {
        "status": "pass",
        "runtime_contract": summarize_completed_process(runtime_contract),
        "reading_chain": summarize_completed_process(reading_chain),
        "task_runtime": json.loads(task_runtime.stdout),
        "workspace_scaffold": json.loads(workspace_scaffold.stdout),
        "workspace_root": resolved_workspace_root,
        "task_runtime_file": str(task_runtime_payload["task_runtime_file"]),
        "task_id": str(task_runtime_payload["task_id"]),
    }


def _run_shell_escaped(command: str) -> str:
    return shlex.quote(command)


def _thread_id_from_log(log_path: Path) -> str:
    if not log_path.exists():
        return ""
    for line in log_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if payload.get("type") == "thread.started":
            return str(payload.get("thread_id", ""))
    return ""


def _tail_lines(path: Path, limit: int = 20) -> list[str]:
    if not path.exists():
        return []
    return path.read_text(encoding="utf-8").splitlines()[-limit:]


def _run_root(run_id: str) -> Path:
    return SUBAGENT_RUN_ROOT / run_id


def _runtime_writeback(run_root: Path, relative_path: str, payload: dict[str, object]) -> str:
    target = run_root / relative_path
    write_json(target, payload)
    return str(target)


def _runtime_checklist_path(run_root: Path, checklist_name: str) -> Path:
    return run_root / f"{checklist_name}.yaml"


def _initialize_runtime_checklists(run_root: Path) -> None:
    workflow_template = read_yaml(RUNSTATE_TEMPLATE_ROOT / "workflow_runtime_checklist.yaml")
    stage_template = read_yaml(RUNSTATE_TEMPLATE_ROOT / "stage_runtime_checklist.yaml")
    write_yaml(_runtime_checklist_path(run_root, "workflow_runtime_checklist"), workflow_template)
    write_yaml(_runtime_checklist_path(run_root, "stage_runtime_checklist"), stage_template)


def _update_checklist(
    path: Path,
    *,
    status: str | None = None,
    current_step: str | None = None,
    previous_output_ref: str | None = None,
    writeback_ref: str | None = None,
    step_id: str | None = None,
    step_status: str | None = None,
    step_notes: str | None = None,
    produced_output_ref: str | None = None,
) -> None:
    payload = read_yaml(path)
    if status is not None:
        payload["status"] = status
    if current_step is not None:
        payload["current_step"] = current_step
    if previous_output_ref is not None:
        payload["previous_output_ref"] = previous_output_ref
    if writeback_ref is not None:
        payload["writeback_ref"] = writeback_ref
    items = payload.get("items")
    if step_id and isinstance(items, list):
        for item in items:
            if not isinstance(item, dict) or item.get("step_id") != step_id:
                continue
            if step_status is not None:
                item["status"] = step_status
            if step_notes is not None:
                item["notes"] = step_notes
            if produced_output_ref is not None:
                item["produced_output_ref"] = produced_output_ref
            if writeback_ref is not None:
                item["writeback_ref"] = writeback_ref
            break
    write_yaml(path, payload)


def _tmux_session_exists(session_name: str) -> bool:
    completed = run_command([TMUX_BIN, "has-session", "-t", session_name], cwd=REPO_ROOT, check=False)
    return completed.returncode == 0


def launch_and_wait_subagent(
    factory_payload: dict[str, object],
    enhanced_intent: dict[str, object],
    runtask_payload: dict[str, object],
    *,
    poll_interval_seconds: int = 5,
    idle_timeout_seconds: int = 600,
    extra_add_dirs: list[str] | None = None,
) -> dict[str, object]:
    run_id = f"{runtask_payload['task_id']}_{int(time.time())}"
    run_root = SUBAGENT_RUN_ROOT / run_id
    run_root.mkdir(parents=True, exist_ok=True)
    _initialize_runtime_checklists(run_root)
    prompt_path = run_root / "subagent_prompt.txt"
    log_path = run_root / "subagent_events.jsonl"
    last_message_path = run_root / "last_message.txt"
    exit_code_path = run_root / "exit_code.txt"
    completed_flag = run_root / "completed_at.txt"
    metadata_path = run_root / "metadata.json"
    session_name = f"wsc_{_slug(run_id)[:40]}"
    write_text(
        prompt_path,
        _subagent_prompt(
            factory_payload,
            enhanced_intent,
            str(runtask_payload["workspace_root"]),
            str(runtask_payload["task_runtime_file"]),
        ),
    )
    add_dir_flags = []
    for extra in extra_add_dirs or []:
        add_dir_flags.extend(["--add-dir", extra])
    codex_command = (
        f"cd {shlex.quote(str(REPO_ROOT))} && "
        f"stdbuf -oL -eL {shlex.quote(CODEX_BIN)} exec "
        f"-m gpt-5.4 "
        f"--config reasoning_effort='\"high\"' "
        f"--dangerously-bypass-approvals-and-sandbox "
        f"-C {shlex.quote(str(REPO_ROOT))} "
        f"--json "
        f"-o {shlex.quote(str(last_message_path))} "
        f"{' '.join(shlex.quote(flag) for flag in add_dir_flags)} "
        f"- < {shlex.quote(str(prompt_path))} 2>&1 | tee {shlex.quote(str(log_path))}; "
        f"status=${{PIPESTATUS[0]}}; "
        f"printf '%s' \"$status\" > {shlex.quote(str(exit_code_path))}; "
        f"date --iso-8601=seconds > {shlex.quote(str(completed_flag))}; "
        f"while true; do sleep 3600; done"
    )
    metadata = {
        "run_id": run_id,
        "session_name": session_name,
        "prompt_path": str(prompt_path),
        "log_path": str(log_path),
        "last_message_path": str(last_message_path),
        "exit_code_path": str(exit_code_path),
        "completed_flag": str(completed_flag),
        "poll_interval_seconds": poll_interval_seconds,
        "idle_timeout_seconds": idle_timeout_seconds,
        "workspace_root": str(runtask_payload["workspace_root"]),
        "task_runtime_file": str(runtask_payload["task_runtime_file"]),
    }
    write_json(metadata_path, metadata)
    factory_writeback = _runtime_writeback(run_root, "runtime/factory_payload.json", factory_payload)
    _update_checklist(
        _runtime_checklist_path(run_root, "workflow_runtime_checklist"),
        status="in_progress",
        current_step="intent_enhance",
        previous_output_ref="factory_payload",
        writeback_ref=relpath(Path(factory_writeback), run_root),
        step_id="factory_intake",
        step_status="completed",
        step_notes="factory payload persisted before Meta-Enhance-Prompt handoff",
        produced_output_ref="factory_payload",
    )
    intent_writeback_path = run_root / "runtime" / "enhanced_intent.txt"
    write_text(intent_writeback_path, str(enhanced_intent["final_intent_output"]).strip() + "\n")
    _update_checklist(
        _runtime_checklist_path(run_root, "workflow_runtime_checklist"),
        status="in_progress",
        current_step="runtask_subagent_launch",
        previous_output_ref="enhanced_intent",
        writeback_ref=relpath(intent_writeback_path, run_root),
        step_id="intent_enhance",
        step_status="completed",
        step_notes="enhanced INTENT persisted for subagent launch",
        produced_output_ref="enhanced_intent",
    )

    run_command([TMUX_BIN, "new-session", "-d", "-s", session_name, f"bash -lc {_run_shell_escaped(codex_command)}"], cwd=REPO_ROOT)
    launch_writeback = _runtime_writeback(
        run_root,
        "runtime/subagent_launch.json",
        {
            "run_id": run_id,
            "session_name": session_name,
            "prompt_path": str(prompt_path),
            "task_runtime_file": str(runtask_payload["task_runtime_file"]),
            "workspace_root": str(runtask_payload["workspace_root"]),
        },
    )
    _update_checklist(
        _runtime_checklist_path(run_root, "workflow_runtime_checklist"),
        status="in_progress",
        current_step="runtask_subagent_poll",
        previous_output_ref="tmux_session_id",
        writeback_ref=relpath(Path(launch_writeback), run_root),
        step_id="runtask_subagent_launch",
        step_status="completed",
        step_notes="tmux session launched for background subagent",
        produced_output_ref=session_name,
    )

    last_change_at = time.time()
    last_size = log_path.stat().st_size if log_path.exists() else 0
    status = "running"
    failure_reason = ""
    poll_count = 0
    polling_samples: list[dict[str, object]] = []
    while True:
        time.sleep(poll_interval_seconds)
        poll_count += 1
        current_exists = _tmux_session_exists(session_name)
        current_size = log_path.stat().st_size if log_path.exists() else 0
        if current_size != last_size:
            last_size = current_size
            last_change_at = time.time()
        polling_samples.append(
            {
                "poll_index": poll_count,
                "session_exists": current_exists,
                "log_size": current_size,
                "seconds_since_last_change": round(time.time() - last_change_at, 3),
            }
        )
        polling_samples = polling_samples[-20:]
        if exit_code_path.exists():
            exit_code = exit_code_path.read_text(encoding="utf-8").strip() or "1"
            status = "pass" if exit_code == "0" else "fail"
            break
        if not current_exists:
            status = "fail"
            failure_reason = "tmux_session_disappeared_before_exit_code"
            break
        if time.time() - last_change_at >= idle_timeout_seconds:
            status = "fail"
            failure_reason = "idle_timeout_without_new_output"
            break

    polling_summary = {
        "poll_count": poll_count,
        "poll_interval_seconds": poll_interval_seconds,
        "idle_timeout_seconds": idle_timeout_seconds,
        "samples_tail": polling_samples,
        "last_log_size": last_size,
        "seconds_since_last_change": round(time.time() - last_change_at, 3),
        "status": status,
        "failure_reason": failure_reason,
    }
    polling_writeback = _runtime_writeback(run_root, "runtime/subagent_polling.json", polling_summary)
    freshness_writeback = _runtime_writeback(
        run_root,
        "runtime/tmux_freshness.json",
        {
            "session_name": session_name,
            "last_log_size": last_size,
            "seconds_since_last_change": round(time.time() - last_change_at, 3),
            "status": "pass" if status == "pass" else "fail",
        },
    )
    _update_checklist(
        _runtime_checklist_path(run_root, "workflow_runtime_checklist"),
        status="in_progress",
        current_step="runtask_subagent_finalize",
        previous_output_ref="subagent_progress",
        writeback_ref=relpath(Path(polling_writeback), run_root),
        step_id="runtask_subagent_poll",
        step_status="completed" if status == "pass" else "failed",
        step_notes="tmux polling summary persisted",
        produced_output_ref="subagent_progress",
    )
    _update_checklist(
        _runtime_checklist_path(run_root, "stage_runtime_checklist"),
        status="in_progress",
        current_step="verify_runtask_stage_evidence",
        previous_output_ref="tmux_session_id",
        writeback_ref=relpath(Path(freshness_writeback), run_root),
        step_id="verify_tmux_output_freshness",
        step_status="completed" if status == "pass" else "failed",
        step_notes="tmux freshness evidence persisted",
        produced_output_ref="freshness_snapshot",
    )

    session_existed_before_kill = _tmux_session_exists(session_name)
    kill_invoked = False
    if session_existed_before_kill:
        kill_invoked = True
        run_command([TMUX_BIN, "kill-session", "-t", session_name], cwd=REPO_ROOT, check=False)
    session_exists_after_kill = _tmux_session_exists(session_name)
    manual_termination = {
        "required": True,
        "kill_invoked": kill_invoked,
        "session_existed_before_kill": session_existed_before_kill,
        "session_exists_after_kill": session_exists_after_kill,
        "status": "pass" if not session_exists_after_kill else "fail",
    }
    manual_termination_writeback = _runtime_writeback(run_root, "runtime/process_termination_check.json", manual_termination)

    final_tail = _tail_lines(log_path)
    finalize_payload = {
        "status": status,
        "failure_reason": failure_reason,
        "thread_id": _thread_id_from_log(log_path),
        "final_log_tail": final_tail,
        "manual_termination": manual_termination,
    }
    finalize_writeback = _runtime_writeback(run_root, "runtime/subagent_finalize.json", finalize_payload)
    _update_checklist(
        _runtime_checklist_path(run_root, "workflow_runtime_checklist"),
        status="completed" if status == "pass" else "failed",
        current_step="done" if status == "pass" else "failed",
        previous_output_ref="runtask_evidence_summary",
        writeback_ref=relpath(Path(finalize_writeback), run_root),
        step_id="runtask_subagent_finalize",
        step_status="completed" if status == "pass" else "failed",
        step_notes="subagent finalized and tmux session manually terminated",
        produced_output_ref="runtask_evidence_summary",
    )
    _update_checklist(
        _runtime_checklist_path(run_root, "stage_runtime_checklist"),
        status="completed" if manual_termination["status"] == "pass" else "failed",
        current_step="done" if manual_termination["status"] == "pass" else "failed",
        previous_output_ref="subagent_finalize",
        writeback_ref=relpath(Path(manual_termination_writeback), run_root),
        step_id="verify_manual_termination",
        step_status="completed" if manual_termination["status"] == "pass" else "failed",
        step_notes="manual termination evidence persisted",
        produced_output_ref="process_termination_check",
    )
    result = {
        "status": status,
        "failure_reason": failure_reason,
        "run_id": run_id,
        "session_name": session_name,
        "thread_id": _thread_id_from_log(log_path),
        "workspace_root": str(runtask_payload["workspace_root"]),
        "task_runtime_file": str(runtask_payload["task_runtime_file"]),
        "log_path": str(log_path),
        "last_message_path": str(last_message_path),
        "exit_code_path": str(exit_code_path),
        "completed_flag": str(completed_flag),
        "final_log_tail": final_tail,
        "last_message": last_message_path.read_text(encoding="utf-8").strip() if last_message_path.exists() else "",
        "polling_summary": polling_summary,
        "manual_termination": manual_termination,
        "workflow_runtime_checklist": str(_runtime_checklist_path(run_root, "workflow_runtime_checklist")),
        "stage_runtime_checklist": str(_runtime_checklist_path(run_root, "stage_runtime_checklist")),
    }
    write_json(run_root / "result.json", result)
    return result


def latest_subagent_status(run_id: str | None = None) -> dict[str, object]:
    if not SUBAGENT_RUN_ROOT.exists():
        return {"status": "fail", "reason": "no_subagent_runs"}
    if run_id:
        target_root = SUBAGENT_RUN_ROOT / run_id
    else:
        candidates = sorted((path for path in SUBAGENT_RUN_ROOT.iterdir() if path.is_dir()), key=lambda path: path.stat().st_mtime, reverse=True)
        if not candidates:
            return {"status": "fail", "reason": "no_subagent_runs"}
        target_root = candidates[0]
    result_path = target_root / "result.json"
    metadata_path = target_root / "metadata.json"
    metadata = read_yaml(metadata_path) if metadata_path.exists() else {}
    payload = read_yaml(result_path) if result_path.exists() else {}
    if not payload:
        payload = {
            "status": "running" if metadata else "fail",
            "run_id": target_root.name,
            "session_name": metadata.get("session_name", ""),
            "log_path": metadata.get("log_path", ""),
            "last_message_path": metadata.get("last_message_path", ""),
        }
    payload["run_root"] = str(target_root)
    return payload


def runtask_validation_summary(runtask_payload: dict[str, object]) -> dict[str, object]:
    workspace_root = str(runtask_payload["workspace_root"])
    workspace_path = Path(workspace_root)
    all_lint = run_command(
        [str(BACKEND_PYTHON), str(RUNTASK_CLI), "stage-lint", "--workspace-root", workspace_root, "--stage", "all", "--json"],
        cwd=REPO_ROOT,
        check=False,
    )
    validation_lint = run_command(
        [str(BACKEND_PYTHON), str(RUNTASK_CLI), "stage-lint", "--workspace-root", workspace_root, "--stage", "validation", "--json"],
        cwd=REPO_ROOT,
        check=False,
    )
    task_runtime_path = Path(runtask_payload["task_runtime_file"])
    stage_object_paths = {
        "workspace_manifest": workspace_path / "workspace_manifest.yaml",
        "evidence_registry": workspace_path / "research" / "evidence_registry.yaml",
        "architect_assessment": workspace_path / "architect" / "assessment.yaml",
        "preview_projection": workspace_path / "preview" / "projection.yaml",
        "design_decisions": workspace_path / "design" / "decisions.yaml",
        "impact_map": workspace_path / "impact" / "impact_map.yaml",
        "milestone_packages": workspace_path / "plan" / "milestone_packages.yaml",
        "implementation_ledger": workspace_path / "implementation" / "turn_ledger.yaml",
    }
    stage_artifact_paths = {
        "research": workspace_path / "research" / "001_research_report.md",
        "architect": workspace_path / "architect" / "001_architecture_assessment_report.md",
        "preview": workspace_path / "preview" / "001_future_shape_preview.md",
        "design": workspace_path / "design" / "001_design_strategy.md",
        "impact": workspace_path / "impact" / "001_impact_investigation.md",
        "validation": workspace_path / "validation" / "001_acceptance_report.md",
        "final_delivery": workspace_path / "final_delivery" / "001_final_delivery_brief.md",
    }
    return {
        "status": "pass" if all_lint.returncode == 0 and validation_lint.returncode == 0 else "fail",
        "all_stage_lint": json.loads(all_lint.stdout) if all_lint.stdout.strip() else summarize_completed_process(all_lint),
        "validation_stage_lint": json.loads(validation_lint.stdout) if validation_lint.stdout.strip() else summarize_completed_process(validation_lint),
        "workspace_manifest": read_yaml(stage_object_paths["workspace_manifest"]),
        "implementation_ledger": read_yaml(stage_object_paths["implementation_ledger"]),
        "design_decisions": read_yaml(stage_object_paths["design_decisions"]),
        "task_runtime": read_yaml(task_runtime_path),
        "stage_object_paths": {key: str(value) for key, value in stage_object_paths.items()},
        "stage_object_presence": {key: value.exists() for key, value in stage_object_paths.items()},
        "stage_artifact_presence": {key: value.exists() for key, value in stage_artifact_paths.items()},
    }


def keyword_first_decision_summary(workspace_root: str) -> dict[str, object]:
    design_path = Path(workspace_root) / "design" / "decisions.yaml"
    payload = read_yaml(design_path)
    decision_mode = str(payload.get("decision_mode", ""))
    explicit_decision = str(payload.get("keyword_first_decision", "")).strip()
    if not explicit_decision:
        explicit_decision = {
            "rewrite": "rewrite",
            "replace": "keyword_first_replace",
            "add": "minimal_add",
        }.get(decision_mode, decision_mode)
    return {
        "path": str(design_path),
        "decision_mode": decision_mode,
        "keyword_first_decision": explicit_decision,
        "seamless_state": payload.get("seamless_state", ""),
        "decision_items": payload.get("decision_items", []),
    }


def validation_closeout_summary(
    *,
    run_id: str,
    subagent_run: dict[str, object],
    runtask_payload: dict[str, object],
    runtask_validation: dict[str, object],
    artifact_refresh: dict[str, object],
    lint_audit: dict[str, object],
    git_traceability_summary: dict[str, object],
) -> dict[str, object]:
    run_root = _run_root(run_id)
    keyword_first = keyword_first_decision_summary(str(runtask_payload["workspace_root"]))
    keyword_writeback = _runtime_writeback(run_root, "runtime/keyword_first_decision.json", keyword_first)
    runtask_workspace_summary = {
        "workspace_root": str(runtask_payload["workspace_root"]),
        "task_runtime_file": str(runtask_payload["task_runtime_file"]),
        "task_runtime_status": runtask_validation.get("task_runtime", {}).get("task_status", ""),
        "current_stage": runtask_validation.get("task_runtime", {}).get("current_stage", ""),
        "stage_object_presence": runtask_validation.get("stage_object_presence", {}),
        "stage_artifact_presence": runtask_validation.get("stage_artifact_presence", {}),
    }
    evidence_check_writeback = _runtime_writeback(run_root, "runtime/runtask_evidence_check.json", runtask_workspace_summary)
    required_outputs = {
        "factory_payload": True,
        "enhanced_intent": True,
        "subagent_summary": bool(subagent_run.get("run_id")),
        "runtask_workspace_summary": True,
        "keyword_first_decision_summary": bool(keyword_first.get("decision_mode")),
        "artifact_refresh_summary": artifact_refresh.get("status") == "pass",
        "lint_audit_summary": lint_audit.get("status") == "pass",
        "git_traceability_summary": True,
    }
    passed_checks = [
        "nine_stage_objects_present" if all(runtask_validation.get("stage_object_presence", {}).values()) else "missing_stage_objects",
        "nine_stage_artifacts_present" if all(runtask_validation.get("stage_artifact_presence", {}).values()) else "missing_stage_artifacts",
        "manual_tmux_termination_verified" if subagent_run.get("manual_termination", {}).get("status") == "pass" else "manual_tmux_termination_failed",
        "artifact_refresh_passed" if artifact_refresh.get("status") == "pass" else "artifact_refresh_failed",
        "lint_audit_passed" if lint_audit.get("status") == "pass" else "lint_audit_failed",
    ]
    closeout = {
        "status": "pass"
        if all(required_outputs.values())
        and runtask_validation.get("status") == "pass"
        and lint_audit.get("status") == "pass"
        and subagent_run.get("manual_termination", {}).get("status") == "pass"
        else "fail",
        "required_outputs": required_outputs,
        "passed_checks": passed_checks,
        "keyword_first_decision_summary": keyword_first,
        "runtask_workspace_summary": runtask_workspace_summary,
        "git_traceability_summary": git_traceability_summary,
    }
    closeout_writeback = _runtime_writeback(run_root, "runtime/validation_closeout.json", closeout)
    _update_checklist(
        _runtime_checklist_path(run_root, "workflow_runtime_checklist"),
        status="in_progress" if closeout["status"] == "pass" else "failed",
        current_step="validation_closeout" if closeout["status"] == "pass" else "failed",
        previous_output_ref="artifact_refresh_summary",
        writeback_ref=relpath(Path(closeout_writeback), run_root),
        step_id="artifact_refresh",
        step_status="completed" if artifact_refresh.get("status") == "pass" else "failed",
        step_notes="artifact refresh summary persisted before validation closeout",
        produced_output_ref="artifact_refresh_summary",
    )
    _update_checklist(
        _runtime_checklist_path(run_root, "stage_runtime_checklist"),
        status="in_progress" if closeout["status"] == "pass" else "failed",
        current_step="verify_manual_termination" if closeout["status"] == "pass" else "failed",
        previous_output_ref="architect_preview_impact_outputs",
        writeback_ref=relpath(Path(keyword_writeback), run_root),
        step_id="capture_keyword_first_decision",
        step_status="completed" if keyword_first.get("decision_mode") else "failed",
        step_notes="design stage keyword-first decision captured from runtask workspace",
        produced_output_ref="keyword_first_decision",
    )
    _update_checklist(
        _runtime_checklist_path(run_root, "stage_runtime_checklist"),
        status="in_progress" if closeout["status"] == "pass" else "failed",
        current_step="verify_manual_termination" if closeout["status"] == "pass" else "failed",
        previous_output_ref="runtask_workspace",
        writeback_ref=relpath(Path(evidence_check_writeback), run_root),
        step_id="verify_runtask_stage_evidence",
        step_status="completed" if runtask_validation.get("status") == "pass" else "failed",
        step_notes="nine-stage runtask evidence validated from workspace objects and artifacts",
        produced_output_ref="nine_stage_evidence_check",
    )
    _update_checklist(
        _runtime_checklist_path(run_root, "workflow_runtime_checklist"),
        status="completed" if closeout["status"] == "pass" else "failed",
        current_step="done" if closeout["status"] == "pass" else "failed",
        previous_output_ref="closeout_summary",
        writeback_ref=relpath(Path(closeout_writeback), run_root),
        step_id="validation_closeout",
        step_status="completed" if closeout["status"] == "pass" else "failed",
        step_notes="validation closeout completed with runtask, artifact, lint, and git summaries",
        produced_output_ref="closeout_summary",
    )
    _update_checklist(
        _runtime_checklist_path(run_root, "stage_runtime_checklist"),
        status="completed" if closeout["status"] == "pass" else "failed",
        current_step="done" if closeout["status"] == "pass" else "failed",
        previous_output_ref="subagent_finalize",
        writeback_ref=relpath(Path(closeout_writeback), run_root),
    )
    return closeout
