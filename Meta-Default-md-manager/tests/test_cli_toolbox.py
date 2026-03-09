from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str((Path(__file__).resolve().parents[1] / "scripts")))
from managed_lock import acquire_cli_lock


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "Cli_Toolbox.py"


class MetaDefaultMdManagerCliTests(unittest.TestCase):
    def write_guidance_contracts(self, skill_root: Path) -> None:
        runtime_dir = skill_root / "references" / "runtime"
        runtime_dir.mkdir(parents=True, exist_ok=True)
        (runtime_dir / "SKILL_RUNTIME_CONTRACT.json").write_text(
            json.dumps(
                {
                    "version": 1,
                    "skill_name": "Meta-Default-md-manager",
                    "description": "test",
                    "runtime_access_policy": {
                        "model_must_not_read_markdown_for_runtime_guidance": True,
                    },
                    "command_map": {
                        "contract": "skill contract",
                        "directive": "stage contract",
                    },
                    "sync_policy": {
                        "update_rule": "update json then render markdown",
                    },
                },
                ensure_ascii=False,
                indent=2,
            ) + "\n",
            encoding="utf-8",
        )
        for stage in ("scan", "collect", "push"):
            stage_dir = skill_root / "references" / "stages" / stage
            stage_dir.mkdir(parents=True, exist_ok=True)
            (stage_dir / "DIRECTIVE.json").write_text(
                json.dumps(
                    {
                        "version": 1,
                        "stage": stage,
                        "instruction": [f"{stage} instruction"],
                        "workflow": [f"{stage} workflow"],
                        "rules": [f"{stage} rule"],
                    },
                    ensure_ascii=False,
                    indent=2,
                ) + "\n",
                encoding="utf-8",
            )

    def run_cli(self, *args: str) -> dict[str, object]:
        completed = subprocess.run(
            ["python3", str(SCRIPT), *args, "--json"],
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(completed.stdout)

    def test_contract_outputs_runtime_policy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_root = Path(tmp) / "skill"
            self.write_guidance_contracts(skill_root)
            payload = self.run_cli("contract", "--skill-root", str(skill_root))
            self.assertEqual(payload["skill_name"], "Meta-Default-md-manager")
            self.assertTrue(payload["runtime_access_policy"]["model_must_not_read_markdown_for_runtime_guidance"])

    def test_directive_and_render_audit_docs_work(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_root = Path(tmp) / "skill"
            self.write_guidance_contracts(skill_root)
            directive = self.run_cli("directive", "--skill-root", str(skill_root), "--stage", "scan")
            self.assertEqual(directive["stage"], "scan")
            render = self.run_cli("render-audit-docs", "--skill-root", str(skill_root))
            self.assertGreaterEqual(render["count"], 10)
            self.assertTrue((skill_root / "references" / "runtime" / "SKILL_RUNTIME_CONTRACT.md").exists())
            self.assertTrue((skill_root / "references" / "stages" / "scan" / "INSTRUCTION.md").exists())

    def test_scan_collect_copies_default_docs_and_writes_registry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_root = Path(tmp) / "skill"
            source_root = Path(tmp) / "src"
            (source_root / "repo-a").mkdir(parents=True)
            (source_root / "repo-b").mkdir(parents=True)
            (source_root / "Octopus_CodeBase_Backend").mkdir(parents=True)
            (source_root / "AGENTS.md").write_text("root agents\n", encoding="utf-8")
            (source_root / "repo-a" / "AGENTS.md").write_text("repo agents\n", encoding="utf-8")
            (source_root / "repo-b" / ".gitignore").write_text("dist/\n", encoding="utf-8")
            (source_root / "Octopus_CodeBase_Backend" / "README.md").write_text("# backend\n", encoding="utf-8")
            (source_root / "Octopus_CodeBase_Backend" / "Deployment_Guide.md").write_text("deploy\n", encoding="utf-8")

            scan_payload = self.run_cli(
                "scan",
                "--skill-root", str(skill_root),
                "--source-root", str(source_root),
            )
            self.assertEqual(scan_payload["count"], 5)
            payload = self.run_cli(
                "collect",
                "--skill-root", str(skill_root),
                "--source-root", str(source_root),
            )

            self.assertEqual(payload["count"], 5)
            registry = json.loads((skill_root / "assets" / "managed_targets" / "registry.json").read_text(encoding="utf-8"))
            self.assertEqual(len(registry["entries"]), 5)
            kinds = {entry["target_kind"] for entry in registry["entries"]}
            self.assertEqual(kinds, {"AGENTS.md", ".gitignore", "README.md", "Deployment_Guide.md"})
            index_text = (skill_root / "assets" / "managed_targets" / "index.md").read_text(encoding="utf-8")
            self.assertIn(str(source_root / "AGENTS.md"), index_text)
            self.assertIn(str(source_root / "repo-b" / ".gitignore"), index_text)
            self.assertIn("target_kind: `.gitignore`", index_text)
            managed_agents_entry = next(entry for entry in registry["entries"] if entry["source_path"] == str(source_root / "AGENTS.md"))
            managed_agents = Path(managed_agents_entry["managed_path"])
            self.assertIn("target-contract", managed_agents.read_text(encoding="utf-8"))
            runtime_rule = Path(managed_agents_entry["managed_path"]).parents[1] / "runtime_rules" / Path(managed_agents_entry["managed_rel_path"]).parent / "AGENTS.runtime.json"
            self.assertTrue(runtime_rule.exists())

    def test_sync_out_overwrites_target_from_managed_copy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_root = Path(tmp) / "skill"
            source_root = Path(tmp) / "src"
            target = source_root / "repo-a" / ".gitignore"
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

    def test_rescan_picks_up_new_default_doc(self) -> None:
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
            (source_root / "two" / ".gitignore").write_text("two\n", encoding="utf-8")
            second = self.run_cli(
                "scan",
                "--skill-root", str(skill_root),
                "--source-root", str(source_root),
            )
            self.assertEqual(second["count"], 2)

    def test_scan_collect_ignores_excluded_directories(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_root = Path(tmp) / "skill"
            source_root = Path(tmp) / "src"
            (source_root / "repo-a").mkdir(parents=True)
            (source_root / "repo-a" / "AGENTS.md").write_text("keep\n", encoding="utf-8")
            (source_root / "Octopus_OS" / "User_UI").mkdir(parents=True)
            (source_root / "Octopus_OS" / "AGENTS.md").write_text("octopus root\n", encoding="utf-8")
            (source_root / "Octopus_OS" / "User_UI" / "AGENTS.md").write_text("octopus ui\n", encoding="utf-8")
            (source_root / "Codex_Skills_Mirror" / "DemoSkill" / "assets" / "managed").mkdir(parents=True)
            (source_root / "Codex_Skills_Mirror" / "DemoSkill" / "assets" / "managed" / "AGENTS.md").write_text("ignore\n", encoding="utf-8")
            (source_root / "Human_Work_Zone" / "repo-b").mkdir(parents=True)
            (source_root / "Human_Work_Zone" / "repo-b" / "AGENTS.md").write_text("ignore\n", encoding="utf-8")
            (source_root / "Codex_Skill_Runtime" / "repo-c").mkdir(parents=True)
            (source_root / "Codex_Skill_Runtime" / "repo-c" / ".gitignore").write_text("ignore\n", encoding="utf-8")

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
            stale = list((skill_root / "assets" / "managed_targets").rglob("*Human_Work_Zone*"))
            self.assertEqual(stale, [])
            octopus_stale = list((skill_root / "assets" / "managed_targets").rglob("*Octopus_OS*"))
            self.assertEqual(octopus_stale, [])
            skill_asset_stale = list((skill_root / "assets" / "managed_targets").rglob("*DemoSkill*"))
            self.assertEqual(skill_asset_stale, [])

    def test_target_contract_returns_target_specific_payload(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_root = Path(tmp) / "skill"
            source_root = Path(tmp) / "src"
            (source_root / "repo-a").mkdir(parents=True)
            (source_root / "repo-a" / "AGENTS.md").write_text("repo agents\n", encoding="utf-8")
            (source_root / "Codex_Skills_Mirror").mkdir(parents=True)
            (source_root / "Codex_Skills_Mirror" / "AGENTS.md").write_text("skill agents\n", encoding="utf-8")
            (source_root / "AGENTS.md").write_text("root agents\n", encoding="utf-8")

            self.run_cli(
                "scan",
                "--skill-root", str(skill_root),
                "--source-root", str(source_root),
            )
            self.run_cli(
                "collect",
                "--skill-root", str(skill_root),
                "--source-root", str(source_root),
            )
            payload = self.run_cli(
                "target-contract",
                "--skill-root", str(skill_root),
                "--source-path", str(source_root / "repo-a" / "AGENTS.md"),
            )
            self.assertEqual(payload["target"]["target_kind"], "AGENTS.md")
            self.assertEqual(payload["turn_contract"]["status"], "n_a")
            self.assertIn("target-contract", payload["runtime_entry"]["cli"])

            root_payload = self.run_cli(
                "target-contract",
                "--skill-root", str(skill_root),
                "--source-path", str(source_root / "AGENTS.md"),
            )
            self.assertEqual(root_payload["turn_contract"]["status"], "enforced")
            self.assertEqual(root_payload["turn_contract"]["turn_end"], ["print TURN_END guardrails"])

            skills_payload = self.run_cli(
                "target-contract",
                "--skill-root", str(skill_root),
                "--source-path", str(source_root / "Codex_Skills_Mirror" / "AGENTS.md"),
            )
            self.assertEqual(skills_payload["turn_contract"]["status"], "enforced")
            self.assertIn("Constitution lint", " ".join(skills_payload["turn_contract"]["turn_end"]))

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
            scan_report = skill_root / "assets" / "managed_targets" / "scan_report.json"
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
            registry = skill_root / "assets" / "managed_targets" / "registry.json"
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
