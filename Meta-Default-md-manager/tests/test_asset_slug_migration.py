from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str((Path(__file__).resolve().parents[1] / "scripts")))
from managed_paths import legacy_root_slugs, root_slug


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "Cli_Toolbox.py"


class MetaDefaultMdManagerAssetSlugMigrationTests(unittest.TestCase):
    def run_cli(self, *args: str) -> dict[str, object]:
        completed = subprocess.run(
            ["python3", str(SCRIPT), *args, "--json"],
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(completed.stdout)

    def test_collect_migrates_legacy_agents_asset_without_manual_steps(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_root = Path(tmp) / "skill"
            source_root = Path(tmp) / "src"
            target = source_root / "AGENTS.md"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("[PART A]\n- current\n\n[PART B]\nlegacy\n", encoding="utf-8")

            legacy_dir = skill_root / "assets" / "managed_targets" / root_slug(source_root)
            legacy_dir.mkdir(parents=True, exist_ok=True)
            legacy_file = legacy_dir / "AGENTS.md"
            legacy_file.write_text("old legacy asset\n", encoding="utf-8")
            (skill_root / "assets" / "managed_targets" / "registry.json").write_text(
                json.dumps(
                    {
                        "version": 2,
                        "entries": [
                            {
                                "source_root": str(source_root),
                                "source_path": str(target),
                                "target_kind": "AGENTS.md",
                                "managed_rel_path": f"{root_slug(source_root)}/AGENTS.md",
                                "managed_path": str(legacy_file),
                                "sha256": "legacy",
                            }
                        ],
                    },
                    ensure_ascii=False,
                    indent=2,
                ) + "\n",
                encoding="utf-8",
            )

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

            migrated_entry = collect["entries"][0]
            self.assertFalse(legacy_file.exists())
            migrated_human = Path(migrated_entry["human_path"])
            self.assertTrue(migrated_human.exists())
            self.assertTrue(Path(migrated_entry["machine_path"]).exists())
            self.assertIn("[PART B]\n\n```json\n", migrated_human.read_text(encoding="utf-8"))
            self.assertFalse((Path(migrated_entry["managed_dir"]) / "AGENT_AUDIT.md").exists())

    def test_collect_prunes_legacy_full_path_namespace_when_slug_contract_changes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_root = Path(tmp) / "skill"
            source_root = Path(tmp) / "AI_Projects"
            target = source_root / "AGENTS.md"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("[PART A]\n- current\n", encoding="utf-8")

            legacy_namespace = skill_root / "assets" / "managed_targets" / legacy_root_slugs(source_root)[-1]
            legacy_namespace.mkdir(parents=True, exist_ok=True)
            (legacy_namespace / "AGENTS.md").write_text("legacy\n", encoding="utf-8")

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

            self.assertEqual(collect["entries"][0]["managed_rel_path"], "AI_Projects/AGENTS.md")
            self.assertFalse(legacy_namespace.exists())

    def test_collect_normalizes_legacy_scan_report_and_prunes_legacy_runtime_namespace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_root = Path(tmp) / "skill"
            source_root = Path(tmp) / "AI_Projects"
            target_agents = source_root / "AGENTS.md"
            target_ignore = source_root / "repo-a" / ".gitignore"
            target_agents.parent.mkdir(parents=True, exist_ok=True)
            target_ignore.parent.mkdir(parents=True, exist_ok=True)
            target_agents.write_text("[PART A]\n- current\n", encoding="utf-8")
            target_ignore.write_text("dist/\n", encoding="utf-8")

            old_slug = legacy_root_slugs(source_root)[-1]
            managed_root = skill_root / "assets" / "managed_targets"
            legacy_namespace = managed_root / old_slug
            legacy_namespace.mkdir(parents=True, exist_ok=True)
            (legacy_namespace / "AGENTS_human.md").write_text("legacy\n", encoding="utf-8")
            (legacy_namespace / "repo-a").mkdir(parents=True, exist_ok=True)
            (legacy_namespace / "repo-a" / ".gitignore").write_text("legacy\n", encoding="utf-8")

            legacy_runtime_root = managed_root / "runtime_rules" / old_slug / "repo-a"
            legacy_runtime_root.mkdir(parents=True, exist_ok=True)
            (legacy_runtime_root / "orphan.runtime.json").write_text("{}", encoding="utf-8")
            (legacy_runtime_root / "ORPHAN_AUDIT.md").write_text("legacy\n", encoding="utf-8")

            (managed_root / "scan_report.json").write_text(
                json.dumps(
                    {
                        "version": 2,
                        "action": "scan",
                        "source_root": str(source_root),
                        "root_slug": old_slug,
                        "managed_root": str(managed_root),
                        "count": 2,
                        "entries": [
                            {
                                "source_root": str(source_root),
                                "source_path": str(target_agents),
                                "target_kind": "AGENTS.md",
                                "managed_rel_path": f"{old_slug}/AGENTS.md",
                                "managed_path": str(legacy_namespace / "AGENTS.md"),
                            },
                            {
                                "source_root": str(source_root),
                                "source_path": str(target_ignore),
                                "target_kind": ".gitignore",
                                "managed_rel_path": f"{old_slug}/repo-a/.gitignore",
                                "managed_path": str(legacy_namespace / "repo-a" / ".gitignore"),
                            },
                        ],
                    },
                    ensure_ascii=False,
                    indent=2,
                ) + "\n",
                encoding="utf-8",
            )

            collect = self.run_cli(
                "collect",
                "--skill-root", str(skill_root),
                "--source-root", str(source_root),
            )

            rel_paths = {entry["managed_rel_path"] for entry in collect["entries"]}
            self.assertIn("AI_Projects/AGENTS.md", rel_paths)
            self.assertIn("AI_Projects/repo-a/.gitignore", rel_paths)
            self.assertFalse(legacy_namespace.exists())
            self.assertFalse((managed_root / "runtime_rules" / old_slug).exists())


if __name__ == "__main__":
    unittest.main()
