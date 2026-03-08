from __future__ import annotations

import json
import sys
import subprocess
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str((Path(__file__).resolve().parents[1] / "scripts")))
from managed_lock import acquire_cli_lock


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "Cli_Toolbox.py"


class MetaAgentsCliTests(unittest.TestCase):
    def run_cli(self, *args: str) -> dict[str, object]:
        completed = subprocess.run(
            ["python3", str(SCRIPT), *args, "--json"],
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(completed.stdout)

    def test_scan_collect_copies_agents_and_writes_registry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_root = Path(tmp) / "skill"
            source_root = Path(tmp) / "src"
            (source_root / "repo-a").mkdir(parents=True)
            (source_root / "AGENTS.md").write_text("root agents\n", encoding="utf-8")
            (source_root / "repo-a" / "AGENTS.md").write_text("repo agents\n", encoding="utf-8")

            scan_payload = self.run_cli(
                "scan",
                "--skill-root", str(skill_root),
                "--source-root", str(source_root),
            )
            self.assertEqual(scan_payload["count"], 2)
            payload = self.run_cli(
                "collect",
                "--skill-root", str(skill_root),
                "--source-root", str(source_root),
            )

            self.assertEqual(payload["count"], 2)
            registry = json.loads((skill_root / "assets" / "managed_agents" / "registry.json").read_text(encoding="utf-8"))
            self.assertEqual(len(registry["entries"]), 2)
            index_text = (skill_root / "assets" / "managed_agents" / "index.md").read_text(encoding="utf-8")
            self.assertIn(str(source_root / "AGENTS.md"), index_text)
            self.assertIn("root agents", index_text)

    def test_sync_out_overwrites_target_from_managed_copy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_root = Path(tmp) / "skill"
            source_root = Path(tmp) / "src"
            target = source_root / "repo-a" / "AGENTS.md"
            target.parent.mkdir(parents=True)
            target.write_text("old\n", encoding="utf-8")

            self.run_cli(
                "scan",
                "--skill-root", str(skill_root),
                "--source-root", str(source_root),
            )
            collect = self.run_cli(
                "collect",
                "--skill-root", str(skill_root),
                "--source-root", str(source_root),
            )
            managed = Path(collect["entries"][0]["managed_path"])
            managed.write_text("new managed\n", encoding="utf-8")

            self.run_cli(
                "push",
                "--skill-root", str(skill_root),
                "--target-source-path", str(target),
            )
            self.assertEqual(target.read_text(encoding="utf-8"), "new managed\n")

    def test_rescan_picks_up_new_agents_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_root = Path(tmp) / "skill"
            source_root = Path(tmp) / "src"
            (source_root / "one").mkdir(parents=True)
            (source_root / "one" / "AGENTS.md").write_text("one\n", encoding="utf-8")

            first = self.run_cli(
                "scan",
                "--skill-root", str(skill_root),
                "--source-root", str(source_root),
            )
            self.assertEqual(first["count"], 1)

            (source_root / "two").mkdir(parents=True)
            (source_root / "two" / "AGENTS.md").write_text("two\n", encoding="utf-8")
            second = self.run_cli(
                "scan",
                "--skill-root", str(skill_root),
                "--source-root", str(source_root),
            )
            self.assertEqual(second["count"], 2)

    def test_scan_collect_ignores_human_work_zone(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_root = Path(tmp) / "skill"
            source_root = Path(tmp) / "src"
            (source_root / "repo-a").mkdir(parents=True)
            (source_root / "repo-a" / "AGENTS.md").write_text("keep\n", encoding="utf-8")
            (source_root / "Human_Work_Zone" / "repo-b").mkdir(parents=True)
            (source_root / "Human_Work_Zone" / "repo-b" / "AGENTS.md").write_text("ignore\n", encoding="utf-8")

            payload = self.run_cli(
                "scan",
                "--skill-root", str(skill_root),
                "--source-root", str(source_root),
            )

            self.assertEqual(payload["count"], 1)
            self.assertEqual(payload["entries"][0]["source_path"], str(source_root / "repo-a" / "AGENTS.md"))
            self.run_cli(
                "collect",
                "--skill-root", str(skill_root),
                "--source-root", str(source_root),
            )
            stale = list((skill_root / "assets" / "managed_agents").rglob("*Human_Work_Zone*"))
            self.assertEqual(stale, [])

    def test_collect_fails_when_scan_report_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_root = Path(tmp) / "skill"
            completed = subprocess.run(
                ["python3", str(SCRIPT), "collect", "--skill-root", str(skill_root), "--json"],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("scan report missing", completed.stdout)

    def test_push_fails_when_registry_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_root = Path(tmp) / "skill"
            completed = subprocess.run(
                ["python3", str(SCRIPT), "push", "--skill-root", str(skill_root), "--all", "--json"],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("registry missing", completed.stdout)

    def test_collect_fails_when_scan_report_empty(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_root = Path(tmp) / "skill"
            scan_report = skill_root / "assets" / "managed_agents" / "scan_report.json"
            scan_report.parent.mkdir(parents=True)
            scan_report.write_text("", encoding="utf-8")
            completed = subprocess.run(
                ["python3", str(SCRIPT), "collect", "--skill-root", str(skill_root), "--json"],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("scan report file is empty", completed.stdout)

    def test_push_fails_when_registry_empty(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_root = Path(tmp) / "skill"
            registry = skill_root / "assets" / "managed_agents" / "registry.json"
            registry.parent.mkdir(parents=True)
            registry.write_text("", encoding="utf-8")
            completed = subprocess.run(
                ["python3", str(SCRIPT), "push", "--skill-root", str(skill_root), "--all", "--json"],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("registry file is empty", completed.stdout)

    def test_stage_lock_blocks_parallel_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_root = Path(tmp) / "skill"
            source_root = Path(tmp) / "src"
            source_root.mkdir(parents=True)
            with acquire_cli_lock(skill_root, "test"):
                completed = subprocess.run(
                    [
                        "python3",
                        str(SCRIPT),
                        "scan",
                        "--skill-root",
                        str(skill_root),
                        "--source-root",
                        str(source_root),
                        "--json",
                    ],
                    check=False,
                    capture_output=True,
                    text=True,
                )
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("command lock busy", completed.stdout)


if __name__ == "__main__":
    unittest.main()
