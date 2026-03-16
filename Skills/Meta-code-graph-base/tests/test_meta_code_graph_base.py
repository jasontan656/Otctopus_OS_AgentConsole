import json
import os
import subprocess
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
CLI_ENTRY = SKILL_ROOT / "assets" / "gitnexus_core" / "dist" / "cli" / "index.js"
TARGET_REPO = (
    SKILL_ROOT.parents[2]
    / "Human_Work_Zone"
    / "Open_Source_Projects"
    / "GitNexus_repo-intel-hub"
)
TARGET_REPO_NAME = "GitNexus_repo-intel-hub"


def run_cmd(
    runtime_root: Path,
    *args: str,
    cwd: Path | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["META_CODE_GRAPH_RUNTIME_ROOT"] = str(runtime_root)
    return subprocess.run(
        ["node", str(CLI_ENTRY), *args],
        text=True,
        capture_output=True,
        check=check,
        cwd=str(cwd) if cwd else None,
        env=env,
    )


def runtime_root_for_test(tmp_path: Path) -> Path:
    runtime_root = tmp_path / "graph_runtime"
    runtime_root.mkdir(parents=True, exist_ok=True)
    return runtime_root


def result_text(result: subprocess.CompletedProcess[str]) -> str:
    return result.stdout or result.stderr


class TestMetaCodeGraphBaseTest:
    def test_runtime_root_is_required(self) -> None:
        result = subprocess.run(
            ["node", str(CLI_ENTRY), "status"],
            text=True,
            capture_output=True,
            check=False,
        )
        assert result.returncode != 0
        assert "runtime root is required" in result.stderr

    def test_analyze_and_list(self, tmp_path: Path) -> None:
        runtime_root = runtime_root_for_test(tmp_path)
        run_cmd(runtime_root, "analyze", str(TARGET_REPO))
        result = run_cmd(runtime_root, "list")
        assert TARGET_REPO_NAME in result.stdout

    def test_runtime_layout_uses_caller_provided_root(self, tmp_path: Path) -> None:
        runtime_root = runtime_root_for_test(tmp_path)
        run_cmd(runtime_root, "analyze", str(TARGET_REPO))
        expected = ["registry", "indexes"]
        for name in expected:
            assert (runtime_root / name).exists(), name

    def test_status_requires_repo_cwd(self, tmp_path: Path) -> None:
        runtime_root = runtime_root_for_test(tmp_path)
        run_cmd(runtime_root, "analyze", str(TARGET_REPO))
        result = run_cmd(runtime_root, "status", cwd=tmp_path)
        assert "Not a git repository." in result.stdout

    def test_status_reports_indexed_repo_inside_repo_cwd(self, tmp_path: Path) -> None:
        runtime_root = runtime_root_for_test(tmp_path)
        run_cmd(runtime_root, "analyze", str(TARGET_REPO))
        result = run_cmd(runtime_root, "status", cwd=TARGET_REPO)
        assert f"Repository: {TARGET_REPO}" in result.stdout
        assert "Indexed commit:" in result.stdout

    def test_resource_context_and_impact(self, tmp_path: Path) -> None:
        runtime_root = runtime_root_for_test(tmp_path)
        run_cmd(runtime_root, "analyze", str(TARGET_REPO))
        context = run_cmd(runtime_root, "resource", f"codegraph://repo/{TARGET_REPO_NAME}/context")
        assert "tools_available" in result_text(context)
        impact = run_cmd(runtime_root, "impact", "LocalBackend", "--direction", "upstream", "--repo", TARGET_REPO_NAME)
        payload = json.loads(result_text(impact))
        assert "summary" in payload

    def test_detect_changes_and_rename_preview(self, tmp_path: Path) -> None:
        runtime_root = runtime_root_for_test(tmp_path)
        run_cmd(runtime_root, "analyze", str(TARGET_REPO))
        changes = run_cmd(runtime_root, "detect-changes", "--repo", TARGET_REPO_NAME)
        change_payload = json.loads(result_text(changes))
        assert "summary" in change_payload

        rename = run_cmd(
            runtime_root,
            "rename",
            "--symbol-name",
            "readResource",
            "--new-name",
            "readGraphResource",
            "--repo",
            TARGET_REPO_NAME,
        )
        rename_payload = json.loads(result_text(rename))
        assert rename_payload["status"] == "success"
        assert not rename_payload["applied"]
        assert rename_payload["files_affected"] >= 1

        augment = run_cmd(runtime_root, "augment", "LocalBackend", cwd=TARGET_REPO)
        assert "[Meta-code-graph-base]" in result_text(augment)
        assert "LocalBackend" in result_text(augment)
