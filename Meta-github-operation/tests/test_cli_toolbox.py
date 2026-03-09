from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "Cli_Toolbox.py"


class MetaGithubOperationCliTests(unittest.TestCase):
    def run_cli(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(SCRIPT), *args],
            check=check,
            capture_output=True,
            text=True,
        )

    def init_repo(self, repo_root: Path) -> None:
        subprocess.run(["git", "-C", str(repo_root), "init", "-q"], check=True)
        subprocess.run(["git", "-C", str(repo_root), "config", "user.email", "test@example.com"], check=True)
        subprocess.run(["git", "-C", str(repo_root), "config", "user.name", "Test User"], check=True)

    def test_contract_commands_are_exposed(self) -> None:
        completed = self.run_cli("--help")
        self.assertIn("push-contract", completed.stdout)
        self.assertIn("rollback-contract", completed.stdout)
        self.assertIn("rollback-sync", completed.stdout)

        push_payload = json.loads(self.run_cli("push-contract", "--json").stdout)
        self.assertEqual(push_payload["entry"], "push")
        self.assertTrue(any(command["name"] == "commit-and-push" for command in push_payload["commands"]))

        rollback_payload = json.loads(self.run_cli("rollback-contract", "--json").stdout)
        self.assertEqual(rollback_payload["entry"], "rollback")
        self.assertTrue(any(command["name"] == "rollback-sync" for command in rollback_payload["commands"]))

    def test_rollback_paths_strongly_restores_and_deletes_extra_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp) / "repo"
            repo_root.mkdir()
            self.init_repo(repo_root)

            watched = repo_root / "watched"
            watched.mkdir()
            (watched / "a.txt").write_text("base\n", encoding="utf-8")
            (watched / "nested.txt").write_text("keep\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo_root), "add", "."], check=True)
            subprocess.run(["git", "-C", str(repo_root), "commit", "-qm", "base"], check=True)
            base_ref = subprocess.run(
                ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()

            (watched / "a.txt").write_text("changed\n", encoding="utf-8")
            (watched / "extra.txt").write_text("extra\n", encoding="utf-8")
            (watched / "sub").mkdir()
            (watched / "sub" / "more.txt").write_text("more\n", encoding="utf-8")

            payload = json.loads(
                self.run_cli(
                    "rollback-paths",
                    "--repo-path",
                    str(repo_root),
                    "--to-ref",
                    base_ref,
                    "--path",
                    "watched",
                    "--json",
                ).stdout
            )

            self.assertEqual(payload["mode"], "paths")
            self.assertEqual((watched / "a.txt").read_text(encoding="utf-8"), "base\n")
            self.assertFalse((watched / "extra.txt").exists())
            self.assertFalse((watched / "sub").exists())
            self.assertTrue((watched / "nested.txt").exists())

    def test_rollback_sync_all_restores_repo_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp) / "repo"
            repo_root.mkdir()
            self.init_repo(repo_root)

            (repo_root / "tracked.txt").write_text("one\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo_root), "add", "."], check=True)
            subprocess.run(["git", "-C", str(repo_root), "commit", "-qm", "base"], check=True)
            base_ref = subprocess.run(
                ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()

            (repo_root / "tracked.txt").write_text("two\n", encoding="utf-8")
            (repo_root / "extra.txt").write_text("extra\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo_root), "add", "tracked.txt"], check=True)

            payload = json.loads(
                self.run_cli(
                    "rollback-sync",
                    "--repo-path",
                    str(repo_root),
                    "--to-ref",
                    base_ref,
                    "--all",
                    "--json",
                ).stdout
            )

            self.assertEqual(payload["mode"], "all")
            self.assertEqual((repo_root / "tracked.txt").read_text(encoding="utf-8"), "one\n")
            self.assertFalse((repo_root / "extra.txt").exists())
            status = subprocess.run(
                ["git", "-C", str(repo_root), "status", "--short"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            self.assertEqual(status, "")


if __name__ == "__main__":
    unittest.main()
