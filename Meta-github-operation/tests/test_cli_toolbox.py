from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
CLI = SKILL_ROOT / "scripts" / "Cli_Toolbox.py"


def run_cli(*args: str) -> dict[str, object]:
    completed = subprocess.run(
        ["python3", str(CLI), *args, "--json"],
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(completed.stdout)


def run_cli_raw(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(CLI), *args, "--json"],
        text=True,
        capture_output=True,
        check=False,
    )


def git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        capture_output=True,
        check=True,
    )


class CliToolboxTest(unittest.TestCase):
    def test_registry_lists_known_repos(self) -> None:
        payload = run_cli("registry")
        repos = {item["repo"] for item in payload["repos"]}
        self.assertIn("Codex_Skills_Mirror", repos)
        self.assertIn("Octopus_CodeBase_Backend", repos)
        self.assertIn("OctuposOS_Runtime_Backend", repos)
        aliases = {item["alias"]: item["repo"] for item in payload["aliases"]}
        self.assertEqual(aliases["Octopus_CodeBase"], "Octopus_CodeBase_Backend")
        self.assertEqual(aliases["OctuposOS_Runtime"], "OctuposOS_Runtime_Backend")

    def test_status_accepts_real_repo_name_identifier(self) -> None:
        payload = run_cli("status", "--repo", "Codex_Skills_Mirror")
        self.assertEqual(payload["repo_root"], "/home/jasontan656/AI_Projects/Codex_Skills_Mirror")

    def test_status_accepts_legacy_repo_alias_identifier(self) -> None:
        payload = run_cli("status", "--repo", "Octopus_CodeBase")
        self.assertEqual(payload["repo"], "Octopus_CodeBase_Backend")
        self.assertEqual(payload["repo_root"], "/home/jasontan656/AI_Projects/Octopus_CodeBase_Backend")

    def test_status_reports_dirty_entries_for_repo_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir) / "repo"
            repo.mkdir()
            git(repo, "init", "-b", "main")
            git(repo, "config", "user.name", "Codex")
            git(repo, "config", "user.email", "codex@example.com")
            (repo / "tracked.txt").write_text("hello\n", encoding="utf-8")
            git(repo, "add", "--", "tracked.txt")
            git(repo, "commit", "-m", "init")
            (repo / "tracked.txt").write_text("changed\n", encoding="utf-8")

            payload = run_cli("status", "--repo-path", str(repo))
            self.assertTrue(payload["dirty"])
            self.assertEqual(payload["branch"], "main")
            self.assertEqual(payload["entries"][0]["path"], "tracked.txt")

    def test_commit_and_push_scoped_path_does_not_stage_unrelated_changes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            remote = Path(temp_dir) / "remote.git"
            local = Path(temp_dir) / "local"
            subprocess.run(["git", "init", "--bare", str(remote)], check=True, capture_output=True, text=True)
            local.mkdir()
            git(local, "init", "-b", "main")
            git(local, "config", "user.name", "Codex")
            git(local, "config", "user.email", "codex@example.com")
            git(local, "remote", "add", "origin", str(remote))
            (local / "a.txt").write_text("a0\n", encoding="utf-8")
            (local / "b.txt").write_text("b0\n", encoding="utf-8")
            git(local, "add", "--", "a.txt", "b.txt")
            git(local, "commit", "-m", "init")
            git(local, "push", "-u", "origin", "main")

            (local / "a.txt").write_text("a1\n", encoding="utf-8")
            (local / "b.txt").write_text("b1\n", encoding="utf-8")

            payload = run_cli(
                "commit-and-push",
                "--repo-path",
                str(local),
                "--message",
                "update a only",
                "--path",
                "a.txt",
            )
            self.assertEqual(payload["scope"]["paths"], ["a.txt"])

            status = git(local, "status", "--short").stdout
            self.assertIn(" M b.txt", status)
            self.assertNotIn("a.txt", status)

    def test_commit_and_push_allow_empty_marker_on_clean_repo(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            remote = Path(temp_dir) / "remote.git"
            local = Path(temp_dir) / "local"
            subprocess.run(["git", "init", "--bare", str(remote)], check=True, capture_output=True, text=True)
            local.mkdir()
            git(local, "init", "-b", "main")
            git(local, "config", "user.name", "Codex")
            git(local, "config", "user.email", "codex@example.com")
            git(local, "remote", "add", "origin", str(remote))
            (local / "tracked.txt").write_text("hello\n", encoding="utf-8")
            git(local, "add", "--", "tracked.txt")
            git(local, "commit", "-m", "init")
            git(local, "push", "-u", "origin", "main")

            payload = run_cli(
                "commit-and-push",
                "--repo-path",
                str(local),
                "--message",
                "marker",
                "--allow-empty",
            )
            self.assertEqual(payload["scope"]["mode"], "allow_empty_marker")
            self.assertTrue(payload["commit"])

    def test_rollback_paths_restores_file_from_ref(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir) / "repo"
            repo.mkdir()
            git(repo, "init", "-b", "main")
            git(repo, "config", "user.name", "Codex")
            git(repo, "config", "user.email", "codex@example.com")
            target = repo / "tracked.txt"
            target.write_text("v1\n", encoding="utf-8")
            git(repo, "add", "--", "tracked.txt")
            git(repo, "commit", "-m", "init")
            target.write_text("v2\n", encoding="utf-8")

            payload = run_cli(
                "rollback-paths",
                "--repo-path",
                str(repo),
                "--to-ref",
                "HEAD",
                "--path",
                "tracked.txt",
            )
            self.assertEqual(payload["to_ref"], "HEAD")
            self.assertEqual(target.read_text(encoding="utf-8"), "v1\n")
            self.assertEqual(payload["pruned_empty_dirs"], [])

    def test_rollback_paths_prunes_empty_directories_removed_by_ref(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir) / "repo"
            repo.mkdir()
            git(repo, "init", "-b", "main")
            git(repo, "config", "user.name", "Codex")
            git(repo, "config", "user.email", "codex@example.com")
            (repo / "keep.txt").write_text("keep\n", encoding="utf-8")
            git(repo, "add", "--", "keep.txt")
            git(repo, "commit", "-m", "base")

            nested = repo / "nested" / "dir"
            nested.mkdir(parents=True)
            target = nested / "tracked.txt"
            target.write_text("v2\n", encoding="utf-8")
            git(repo, "add", "--", "nested/dir/tracked.txt")
            git(repo, "commit", "-m", "add nested tracked")

            git(repo, "rm", "--", "nested/dir/tracked.txt")
            git(repo, "commit", "-m", "remove nested tracked")

            (repo / "nested" / "dir").mkdir(parents=True, exist_ok=True)

            payload = run_cli(
                "rollback-paths",
                "--repo-path",
                str(repo),
                "--to-ref",
                "HEAD",
                "--path",
                "nested/dir/tracked.txt",
            )
            self.assertFalse((repo / "nested").exists())
            self.assertIn("nested/dir", payload["pruned_empty_dirs"])
            self.assertIn("nested", payload["pruned_empty_dirs"])

    def test_auto_scope_fails_on_ambiguous_changes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir) / "repo"
            repo.mkdir()
            git(repo, "init", "-b", "main")
            git(repo, "config", "user.name", "Codex")
            git(repo, "config", "user.email", "codex@example.com")
            (repo / "a.txt").write_text("a0\n", encoding="utf-8")
            (repo / "b.txt").write_text("b0\n", encoding="utf-8")
            git(repo, "add", "--", "a.txt", "b.txt")
            git(repo, "commit", "-m", "init")
            (repo / "a.txt").write_text("a1\n", encoding="utf-8")
            (repo / "b.txt").write_text("b1\n", encoding="utf-8")

            completed = run_cli_raw(
                "commit",
                "--repo-path",
                str(repo),
                "--message",
                "ambiguous",
                "--auto-scope",
            )
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("scope_ambiguous", completed.stderr)


if __name__ == "__main__":
    unittest.main()
