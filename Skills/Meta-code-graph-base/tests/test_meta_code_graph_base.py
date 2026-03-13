import json
import subprocess
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
WRAPPER = SKILL_ROOT / "scripts" / "meta_code_graph_base.py"
TARGET_REPO = (
    SKILL_ROOT.parents[2]
    / "Human_Work_Zone"
    / "Open_Source_Projects"
    / "GitNexus_repo-intel-hub"
)
TARGET_REPO_NAME = "GitNexus_repo-intel-hub"
TARGET_REPO_KEY = "GitNexus_repo-intel-hub-cd46025f10d5"


def run_cmd(
    runtime_root: Path,
    *args: str,
    cwd: Path | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(WRAPPER), "--runtime-root", str(runtime_root), *args],
        text=True,
        capture_output=True,
        check=check,
        cwd=str(cwd) if cwd else None,
    )


def runtime_root_for_test(tmp_path: Path) -> Path:
    runtime_root = tmp_path / "graph_runtime"
    runtime_root.mkdir(parents=True, exist_ok=True)
    return runtime_root


class TestMetaCodeGraphBaseTest:
    def test_runtime_root_is_required(self) -> None:
        result = subprocess.run(
            ["python3", str(WRAPPER), "status"],
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

    def test_resource_context_and_impact(self, tmp_path: Path) -> None:
        runtime_root = runtime_root_for_test(tmp_path)
        run_cmd(runtime_root, "analyze", str(TARGET_REPO))
        context = run_cmd(runtime_root, "resource", f"codegraph://repo/{TARGET_REPO_NAME}/context")
        assert "tools_available" in context.stdout
        impact = run_cmd(runtime_root, "impact", "LocalBackend", "--direction", "upstream", "--repo", TARGET_REPO_NAME)
        payload = json.loads(impact.stdout or impact.stderr)
        assert "summary" in payload

    def test_detect_changes_and_rename_preview(self, tmp_path: Path) -> None:
        runtime_root = runtime_root_for_test(tmp_path)
        run_cmd(runtime_root, "analyze", str(TARGET_REPO))
        changes = run_cmd(runtime_root, "detect-changes", "--repo", TARGET_REPO_NAME)
        change_payload = json.loads(changes.stdout)
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
        rename_payload = json.loads(rename.stdout)
        assert rename_payload["status"] == "success"
        assert not rename_payload["applied"]
        assert rename_payload["files_affected"] >= 1

        augment = run_cmd(runtime_root, "augment", "LocalBackend", cwd=TARGET_REPO)
        assert "[Meta-code-graph-base]" in augment.stdout
        assert "LocalBackend" in augment.stdout

    def test_map_generation_writes_runtime_artifacts(self, tmp_path: Path) -> None:
        runtime_root = runtime_root_for_test(tmp_path)
        run_cmd(runtime_root, "analyze", str(TARGET_REPO))
        result = run_cmd(runtime_root, "map", TARGET_REPO_NAME)
        payload = json.loads(result.stdout)
        assert payload["status"] == "success"

        map_dir = runtime_root / "maps" / TARGET_REPO_KEY
        assert (map_dir / "repo_context.md").exists()
        assert (map_dir / "clusters.md").exists()
        assert (map_dir / "processes.md").exists()
        assert (map_dir / "schema.md").exists()
        assert (map_dir / "manifest.json").exists()

        context_text = (map_dir / "repo_context.md").read_text(encoding="utf-8")
        clusters_text = (map_dir / "clusters.md").read_text(encoding="utf-8")
        assert "tools_available" in context_text
        assert "modules:" in clusters_text

    def test_wiki_generation_writes_local_bundle(self, tmp_path: Path) -> None:
        runtime_root = runtime_root_for_test(tmp_path)
        run_cmd(runtime_root, "analyze", str(TARGET_REPO))
        result = run_cmd(runtime_root, "wiki", TARGET_REPO_NAME)
        payload = json.loads(result.stdout)
        assert payload["status"] == "success"

        wiki_dir = runtime_root / "wiki" / TARGET_REPO_KEY
        assert (wiki_dir / "overview.md").exists()
        assert (wiki_dir / "clusters.md").exists()
        assert (wiki_dir / "processes.md").exists()
        assert (wiki_dir / "schema.md").exists()
        assert (wiki_dir / "index.html").exists()
        overview_text = (wiki_dir / "overview.md").read_text(encoding="utf-8")
        assert "local graph resources only" in overview_text
