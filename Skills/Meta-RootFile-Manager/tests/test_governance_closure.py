from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_cli_toolbox import TestCliToolbox as _BaseTestCliToolbox

_BaseTestCliToolbox.__test__ = False


class TestGovernanceClosure:
    def setup_method(self) -> None:
        self._base = _BaseTestCliToolbox()
        self._base.setup_method()
        self.workspace = self._base.workspace
        self.skill_root = self._base.skill_root

    def teardown_method(self) -> None:
        self._base.teardown_method()

    def run_cli(self, *args: str, workspace_root: Path | None = None, expect_ok: bool = True) -> dict:
        return self._base.run_cli(*args, workspace_root=workspace_root, expect_ok=expect_ok)

    def test_contract_declares_artifact_policy(self) -> None:
        result = self.run_cli("contract", "--json")
        assert result["artifact_policy"]["mode"] == "runtime_local_artifacts"
        assert result["artifact_policy"]["resolver"] == "runtime_contract_paths"
        assert any(
            "Codex_Skill_Runtime/<skill>/artifacts/<stage>/latest.json" in note
            for note in result["artifact_policy"]["notes"]
        )

    def test_push_skips_ephemeral_runtime_targets_by_default(self) -> None:
        target_dir = self.workspace / "tmpabc1234" / "sample_repo" / "Development_Docs"
        self.run_cli(
            "scaffold",
            "--json",
            "--target-dir",
            str(target_dir),
            "--file-kind",
            "AGENTS.md",
        )
        result = self.run_cli("push", "--json", "--dry-run")
        assert all("tmpabc1234" not in item["source_path"] for item in result["operations"])
        assert all("tmpabc1234" not in item["source_path"] for item in result["failures"])

    def test_codex_skills_managed_assets_use_symbolic_paths(self) -> None:
        managed_root = self.skill_root / "assets" / "managed_targets" / "AI_Projects" / ".codex" / "skills"
        human_text = (managed_root / "AGENTS_human.md").read_text(encoding="utf-8")
        assert "agents-maintain" in human_text
        assert "MDM_WORKSPACE_ROOT=<codex_home_parent>" in human_text
        assert "/home/jasontan656/AI_Projects/.codex/skills/AGENTS.md" in human_text
