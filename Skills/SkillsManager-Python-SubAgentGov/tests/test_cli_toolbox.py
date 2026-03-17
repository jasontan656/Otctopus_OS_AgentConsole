from __future__ import annotations

import json
import subprocess
import sys
import threading
import time
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
CLI_PATH = SKILL_ROOT / "scripts" / "Cli_Toolbox.py"
SCRIPT_ROOT = SKILL_ROOT / "scripts"
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from result_support import expected_exit_code
from result_support import load_result
from runtime_support import build_config
from runtime_support import build_worker


def run_cli(*args: str) -> dict[str, object]:
    completed = subprocess.run(
        ["python3", str(CLI_PATH), *args, "--json"],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def write_skill(skill_root: Path, skill_name: str) -> None:
    target = skill_root / skill_name
    target.mkdir(parents=True)
    (target / "SKILL.md").write_text(
        f"---\nname: {skill_name}\ndescription: Test skill.\n---\n\n# {skill_name}\n",
        encoding="utf-8",
    )


def test_contract_exposes_govern_entry() -> None:
    payload = run_cli("contract")
    assert payload["skill_role"] == "python_subagent_governor"
    assert "govern" in payload["tool_entry"]["commands"]


def test_list_targets_excludes_reserved_dirs_and_self_by_default(tmp_path: Path) -> None:
    skills_root = tmp_path / "Skills"
    skills_root.mkdir()
    (skills_root / ".system").mkdir()
    (skills_root / "_shared").mkdir()
    write_skill(skills_root, "Target-Skill")
    write_skill(skills_root, SKILL_ROOT.name)
    (skills_root / "NoFacade").mkdir()

    payload = run_cli("list-targets", "--skills-root", str(skills_root))
    assert payload["discovered_skills"] == ["Target-Skill"]
    reasons = {item["skill_name"]: item["reason"] for item in payload["excluded_skills"]}
    assert reasons[".system"] == "reserved_skill_container"
    assert reasons["_shared"] == "reserved_skill_container"
    assert reasons["NoFacade"] == "missing_skill_facade"
    assert reasons[SKILL_ROOT.name] == "self_governance_requires_explicit_target"


def test_render_prompt_writes_runtime_artifacts(tmp_path: Path) -> None:
    runtime_root = tmp_path / "runtime"
    payload = run_cli("render-prompt", "--runtime-root", str(runtime_root), "--skill-name", "Target-Skill")
    prompt_path = Path(str(payload["prompt_path"]))
    assert prompt_path.exists()
    prompt_text = prompt_path.read_text(encoding="utf-8")
    assert "Target-Skill" in prompt_text
    assert str(runtime_root / "Target-Skill") in prompt_text
    assert "__SKILL_NAME__" not in prompt_text


def test_status_reports_pending_active_and_completed(tmp_path: Path) -> None:
    skills_root = tmp_path / "Skills"
    skills_root.mkdir()
    runtime_root = tmp_path / "Codex_Skill_Runtime" / "SkillsManager-Python-SubAgentGov"
    for skill_name in ("Skill-A", "Skill-B", "Skill-C"):
        write_skill(skills_root, skill_name)

    config = build_config(skills_root=skills_root, runtime_root=runtime_root)
    worker_a = build_worker(config, "Skill-A")
    worker_a.runtime_dir.mkdir(parents=True)
    worker_a.closure_path.write_text("{}", encoding="utf-8")

    worker_b = build_worker(config, "Skill-B")
    worker_b.runtime_dir.mkdir(parents=True)
    worker_b.exit_code_path.write_text("0\n", encoding="utf-8")

    payload = run_cli("status", "--skills-root", str(skills_root), "--runtime-root", str(runtime_root))
    assert payload["completed_count"] == 1
    assert payload["completed_skills"] == ["Skill-A"]
    assert "Skill-B" in payload["active"]
    assert payload["pending_skills"] == ["Skill-C"]


def test_expected_exit_code_accepts_string_and_object_schema() -> None:
    string_payload = {
        "verification_commands": ["pytest Skills/Target-Skill/tests"],
        "verification_evidence": {"pytest": {"exit_code": 5}},
    }
    object_payload = {
        "verification_commands": [{"command": "pytest Skills/Target-Skill/tests", "exit_code": 0}],
    }
    assert expected_exit_code(string_payload, "pytest Skills/Target-Skill") == 5
    assert expected_exit_code(object_payload, "pytest Skills/Target-Skill") == 0


def test_load_result_retries_until_json_is_complete(tmp_path: Path) -> None:
    config = build_config(runtime_root=tmp_path / "runtime")
    worker = build_worker(config, "Retry-Skill")
    worker.runtime_dir.mkdir(parents=True)
    worker.result_json_path.write_text("{", encoding="utf-8")

    def repair_result() -> None:
        time.sleep(0.05)
        worker.result_json_path.write_text(
            json.dumps({"status": "success_no_change", "skill_name": "Retry-Skill"}, ensure_ascii=False),
            encoding="utf-8",
        )

    thread = threading.Thread(target=repair_result)
    thread.start()
    payload = load_result(worker, attempts=20, sleep_seconds=0.01)
    thread.join()
    assert payload["status"] == "success_no_change"
