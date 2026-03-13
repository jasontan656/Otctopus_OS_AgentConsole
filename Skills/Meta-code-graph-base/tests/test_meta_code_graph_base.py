import json
import subprocess
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
PRODUCT_ROOT = SKILL_ROOT.parents[2]
WRAPPER = SKILL_ROOT / "scripts" / "meta_code_graph_base.py"
RUNTIME_ROOT = PRODUCT_ROOT / "Codex_Skill_Runtime" / "Meta-code-graph-base" / "code_graph_runtime"
TARGET_REPO = PRODUCT_ROOT / "Human_Work_Zone" / "Open_Source_Projects" / "GitNexus_repo-intel-hub"
TARGET_REPO_NAME = "GitNexus_repo-intel-hub"
TARGET_REPO_KEY = "GitNexus_repo-intel-hub-cd46025f10d5"


def run_cmd(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(WRAPPER), *args],
        text=True,
        capture_output=True,
        check=True,
        cwd=str(cwd) if cwd else None,
    )


class TestMetaCodeGraphBaseTest:
    def test_runtime_layout_exists(self) -> None:
        assert str(RUNTIME_ROOT).endswith("Codex_Skill_Runtime/Meta-code-graph-base/code_graph_runtime")
        expected = ["registry", "indexes", "maps", "wiki"]
        for name in expected:
            (RUNTIME_ROOT / name).mkdir(parents=True, exist_ok=True)
            assert (RUNTIME_ROOT / name).exists(), name

    def test_analyze_and_list(self) -> None:
        run_cmd("analyze", str(TARGET_REPO))
        result = run_cmd("list")
        assert TARGET_REPO_NAME in result.stdout

    def test_resource_context_and_impact(self) -> None:
        run_cmd("analyze", str(TARGET_REPO))
        context = run_cmd("resource", f"codegraph://repo/{TARGET_REPO_NAME}/context")
        assert "tools_available" in context.stdout
        impact = run_cmd("impact", "LocalBackend", "--direction", "upstream", "--repo", TARGET_REPO_NAME)
        payload = json.loads(impact.stdout or impact.stderr)
        assert "summary" in payload

    def test_detect_changes_and_rename_preview(self) -> None:
        run_cmd("analyze", str(TARGET_REPO))
        changes = run_cmd("detect-changes", "--repo", TARGET_REPO_NAME)
        change_payload = json.loads(changes.stdout)
        assert "summary" in change_payload

        rename = run_cmd("rename", "--symbol-name", "readResource", "--new-name", "readGraphResource", "--repo", TARGET_REPO_NAME)
        rename_payload = json.loads(rename.stdout)
        assert rename_payload["status"] == "success"
        assert not (rename_payload["applied"])
        assert rename_payload["files_affected"] >= 1

        augment = run_cmd("augment", "LocalBackend", cwd=TARGET_REPO)
        assert "[Meta-code-graph-base]" in augment.stdout
        assert "LocalBackend" in augment.stdout

    def test_map_generation_writes_runtime_artifacts(self) -> None:
        run_cmd("analyze", str(TARGET_REPO))
        result = run_cmd("map", TARGET_REPO_NAME)
        payload = json.loads(result.stdout)
        assert payload["status"] == "success"

        map_dir = RUNTIME_ROOT / "maps" / TARGET_REPO_KEY
        assert (map_dir / "repo_context.md").exists()
        assert (map_dir / "clusters.md").exists()
        assert (map_dir / "processes.md").exists()
        assert (map_dir / "schema.md").exists()
        assert (map_dir / "manifest.json").exists()

        context_text = (map_dir / "repo_context.md").read_text(encoding="utf-8")
        clusters_text = (map_dir / "clusters.md").read_text(encoding="utf-8")
        assert "tools_available" in context_text
        assert "modules:" in clusters_text

    def test_wiki_generation_writes_local_bundle(self) -> None:
        run_cmd("analyze", str(TARGET_REPO))
        result = run_cmd("wiki", TARGET_REPO_NAME)
        payload = json.loads(result.stdout)
        assert payload["status"] == "success"

        wiki_dir = RUNTIME_ROOT / "wiki" / TARGET_REPO_KEY
        assert (wiki_dir / "overview.md").exists()
        assert (wiki_dir / "clusters.md").exists()
        assert (wiki_dir / "processes.md").exists()
        assert (wiki_dir / "schema.md").exists()
        assert (wiki_dir / "index.html").exists()
        overview_text = (wiki_dir / "overview.md").read_text(encoding="utf-8")
        assert "local graph resources only" in overview_text
