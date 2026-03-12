from __future__ import annotations

import json
import pytest
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from registry_repo import ensure_remote_write_allowed, remote_policy_payload


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "Cli_Toolbox.py"


class TestMetaGithubOperationCliTests:
    def run_cli(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
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
        assert "baseline-contract" in completed.stdout
        assert "baseline-create" in completed.stdout
        assert "push-contract" in completed.stdout
        assert "rollback-contract" in completed.stdout
        assert "rollback-sync" in completed.stdout

        push_payload = json.loads(self.run_cli("push-contract", "--json").stdout)
        assert push_payload["entry"] == "push"
        assert any(command["name"] == "commit-and-push" for command in push_payload["commands"])
        assert not (any(command["name"] == "baseline-create" for command in push_payload["commands"]))
        assert (
            push_payload["remote_policy"]["octopus-os-agent-console"]["origin"]["role"]
            == "private_dev_remote"
        )
        assert push_payload["runtime_governance"]["skill_runtime_root"].endswith("/meta-github-operation")
        assert push_payload["runtime_governance"]["claims_dir"].endswith("/meta-github-operation/claims")
        assert push_payload["runtime_governance"]["result_root"].endswith("/meta-github-operation")
        assert not push_payload["remote_policy"]["octopus-os-agent-console"]["public-release"][
            "automation_write_allowed"
        ]

        baseline_payload = json.loads(self.run_cli("baseline-contract", "--json").stdout)
        assert baseline_payload["entry"] == "baseline"
        assert [command["name"] for command in baseline_payload["commands"]] == ["baseline-create"]
        assert baseline_payload["runtime_governance"]["result_policy"].startswith("This skill does not emit")
        assert (
            baseline_payload["release_publication_state"]["octopus-os-agent-console"]["public-release"]["status"]
            == "disabled"
        )

        rollback_payload = json.loads(self.run_cli("rollback-contract", "--json").stdout)
        assert rollback_payload["entry"] == "rollback"
        assert rollback_payload["runtime_governance"]["legacy_runtime_fallbacks"] == [
            "/home/jasontan656/AI_Projects/Codex_Skill_Runtime"
        ]
        assert any(command["name"] == "rollback-sync" for command in rollback_payload["commands"])
        assert not (any(command["name"] == "baseline-create" for command in rollback_payload["commands"]))

    def test_baseline_create_clean_repo_creates_tag_only_anchor(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp) / "repo"
            repo_root.mkdir()
            self.init_repo(repo_root)

            (repo_root / "tracked.txt").write_text("base\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo_root), "add", "."], check=True)
            subprocess.run(["git", "-C", str(repo_root), "commit", "-qm", "base"], check=True)
            head_before = subprocess.run(
                ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()

            payload = json.loads(
                self.run_cli(
                    "baseline-create",
                    "--repo-path",
                    str(repo_root),
                    "--name",
                    "before fullstack",
                    "--publish",
                    "local",
                    "--json",
                ).stdout
            )

            head_after = subprocess.run(
                ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            tag_target = subprocess.run(
                ["git", "-C", str(repo_root), "rev-list", "-n", "1", "baseline/before-fullstack"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()

            assert not (payload["dirty_before"])
            assert payload["baseline_mode"] == "tag_only"
            assert "commit" not in payload
            assert payload["tag"] == "baseline/before-fullstack"
            assert head_before == head_after
            assert tag_target == head_before

    def test_baseline_create_dirty_repo_creates_commit_plus_tag(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp) / "repo"
            repo_root.mkdir()
            self.init_repo(repo_root)

            (repo_root / "tracked.txt").write_text("base\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo_root), "add", "."], check=True)
            subprocess.run(["git", "-C", str(repo_root), "commit", "-qm", "base"], check=True)

            (repo_root / "tracked.txt").write_text("changed\n", encoding="utf-8")
            (repo_root / "extra.txt").write_text("extra\n", encoding="utf-8")

            payload = json.loads(
                self.run_cli(
                    "baseline-create",
                    "--repo-path",
                    str(repo_root),
                    "--name",
                    "dirty snapshot",
                    "--publish",
                    "local",
                    "--all",
                    "--json",
                ).stdout
            )

            head_after = subprocess.run(
                ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            tag_target = subprocess.run(
                ["git", "-C", str(repo_root), "rev-list", "-n", "1", "baseline/dirty-snapshot"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            status = subprocess.run(
                ["git", "-C", str(repo_root), "status", "--short"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()

            assert payload["dirty_before"]
            assert payload["baseline_mode"] == "commit_plus_tag"
            assert payload["commit"] == head_after[:7]
            assert payload["scope"]["mode"] == "all"
            assert payload["tag"] == "baseline/dirty-snapshot"
            assert tag_target == head_after
            assert status == ""

    def test_baseline_create_clean_repo_remote_publish_pushes_only_tag(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            remote_root = Path(tmp) / "remote.git"
            repo_root = Path(tmp) / "repo"
            subprocess.run(["git", "init", "--bare", "-q", str(remote_root)], check=True)
            repo_root.mkdir()
            self.init_repo(repo_root)

            (repo_root / "tracked.txt").write_text("base\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo_root), "add", "."], check=True)
            subprocess.run(["git", "-C", str(repo_root), "commit", "-qm", "base"], check=True)
            subprocess.run(["git", "-C", str(repo_root), "remote", "add", "origin", str(remote_root)], check=True)

            payload = json.loads(
                self.run_cli(
                    "baseline-create",
                    "--repo-path",
                    str(repo_root),
                    "--name",
                    "release candidate",
                    "--publish",
                    "remote",
                    "--json",
                ).stdout
            )

            remote_tag = subprocess.run(
                ["git", "-C", str(remote_root), "rev-parse", "--verify", "refs/tags/baseline/release-candidate"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            remote_heads = subprocess.run(
                ["git", "-C", str(remote_root), "show-ref", "--heads"],
                check=False,
                capture_output=True,
                text=True,
            )

            assert payload["baseline_mode"] == "tag_only"
            assert "publish_result" in payload
            assert "branch" not in payload["publish_result"]
            assert remote_tag
            assert remote_heads.returncode == 1
            assert remote_heads.stdout.strip() == ""

    def test_remote_info_exposes_managed_remote_policy(self) -> None:
        payload = json.loads(self.run_cli("remote-info", "--repo", "octopus-os-agent-console", "--json").stdout)
        policy = payload["managed_remote_policy"]
        assert policy["repo"] == "octopus-os-agent-console"
        assert any(item["name"] == "origin" for item in policy["remotes"])
        blocked = next(item for item in policy["remotes"] if item["name"] == "public-release")
        assert blocked["status"] == "disabled"
        assert not (blocked["automation_write_allowed"])

    def test_remote_policy_blocks_public_release_writes_for_product_repo(self) -> None:
        with pytest.raises(ValueError, match="remote_write_blocked"):
            ensure_remote_write_allowed(
                "octopus-os-agent-console",
                "public-release",
                operation="push",
            )

    def test_remote_policy_payload_marks_public_release_disabled(self) -> None:
        payload = remote_policy_payload("octopus-os-agent-console")
        blocked = next(item for item in payload["remotes"] if item["name"] == "public-release")
        assert blocked["role"] == "future_public_release_remote"
        assert not (blocked["manual_publish_allowed"])
        assert "publishable closure" in blocked["disabled_reason"]

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

            assert payload["mode"] == "paths"
            assert (watched / "a.txt").read_text(encoding="utf-8") == "base\n"
            assert not (watched / "extra.txt").exists()
            assert not (watched / "sub").exists()
            assert (watched / "nested.txt").exists()

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

            assert payload["mode"] == "all"
            assert (repo_root / "tracked.txt").read_text(encoding="utf-8") == "one\n"
            assert not (repo_root / "extra.txt").exists()
            status = subprocess.run(
                ["git", "-C", str(repo_root), "status", "--short"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            assert status == ""
