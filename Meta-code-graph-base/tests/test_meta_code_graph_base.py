import json
import subprocess
import unittest
from pathlib import Path


SKILL_ROOT = Path("/home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-code-graph-base")
WRAPPER = SKILL_ROOT / "scripts" / "meta_code_graph_base.py"
RUNTIME_ROOT = Path("/home/jasontan656/AI_Projects/OctuposOS_Runtime_Backend/code_graph_runtime")
TARGET_REPO = Path("/home/jasontan656/AI_Projects/Human_Work_Zone/GitNexus")
TARGET_REPO_NAME = "GitNexus"
TARGET_REPO_KEY = "GitNexus-ed2fb3eb9c1d"


def run_cmd(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(WRAPPER), *args],
        text=True,
        capture_output=True,
        check=True,
        cwd=str(cwd) if cwd else None,
    )


class MetaCodeGraphBaseTest(unittest.TestCase):
    def test_runtime_layout_exists(self) -> None:
        expected = ["registry", "indexes", "reports", "maps", "wiki", "snapshots"]
        for name in expected:
            self.assertTrue((RUNTIME_ROOT / name).exists(), name)

    def test_analyze_and_list(self) -> None:
        run_cmd("analyze", str(TARGET_REPO))
        result = run_cmd("list")
        self.assertIn(TARGET_REPO_NAME, result.stdout)

    def test_resource_context_and_impact(self) -> None:
        run_cmd("analyze", str(TARGET_REPO))
        context = run_cmd("resource", f"codegraph://repo/{TARGET_REPO_NAME}/context")
        self.assertIn("tools_available", context.stdout)
        impact = run_cmd("impact", "LocalBackend", "--direction", "upstream", "--repo", TARGET_REPO_NAME)
        payload = json.loads(impact.stdout or impact.stderr)
        self.assertIn("summary", payload)

    def test_detect_changes_and_rename_preview(self) -> None:
        run_cmd("analyze", str(TARGET_REPO))
        changes = run_cmd("detect-changes", "--repo", TARGET_REPO_NAME)
        change_payload = json.loads(changes.stdout)
        self.assertIn("summary", change_payload)

        rename = run_cmd("rename", "--symbol-name", "readResource", "--new-name", "readGraphResource", "--repo", TARGET_REPO_NAME)
        rename_payload = json.loads(rename.stdout)
        self.assertEqual(rename_payload["status"], "success")
        self.assertFalse(rename_payload["applied"])
        self.assertGreaterEqual(rename_payload["files_affected"], 1)

        augment = run_cmd("augment", "LocalBackend", cwd=TARGET_REPO)
        self.assertIn("[Meta-code-graph-base]", augment.stdout)
        self.assertIn("LocalBackend", augment.stdout)

    def test_map_generation_writes_runtime_artifacts(self) -> None:
        run_cmd("analyze", str(TARGET_REPO))
        result = run_cmd("map", TARGET_REPO_NAME)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "success")

        map_dir = RUNTIME_ROOT / "maps" / TARGET_REPO_KEY
        self.assertTrue((map_dir / "repo_context.md").exists())
        self.assertTrue((map_dir / "clusters.md").exists())
        self.assertTrue((map_dir / "processes.md").exists())
        self.assertTrue((map_dir / "schema.md").exists())
        self.assertTrue((map_dir / "manifest.json").exists())

        context_text = (map_dir / "repo_context.md").read_text(encoding="utf-8")
        clusters_text = (map_dir / "clusters.md").read_text(encoding="utf-8")
        self.assertIn("tools_available", context_text)
        self.assertIn("modules:", clusters_text)

    def test_wiki_generation_writes_local_bundle(self) -> None:
        run_cmd("analyze", str(TARGET_REPO))
        result = run_cmd("wiki", TARGET_REPO_NAME)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "success")

        wiki_dir = RUNTIME_ROOT / "wiki" / TARGET_REPO_KEY
        self.assertTrue((wiki_dir / "overview.md").exists())
        self.assertTrue((wiki_dir / "clusters.md").exists())
        self.assertTrue((wiki_dir / "processes.md").exists())
        self.assertTrue((wiki_dir / "schema.md").exists())
        self.assertTrue((wiki_dir / "index.html").exists())
        overview_text = (wiki_dir / "overview.md").read_text(encoding="utf-8")
        self.assertIn("local graph resources only", overview_text)
