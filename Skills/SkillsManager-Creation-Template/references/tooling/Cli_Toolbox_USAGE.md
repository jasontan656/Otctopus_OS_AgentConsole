---
doc_id: skillsmanager_creation_template.references.tooling.cli_toolbox_usage
doc_type: topic_atom
topic: CLI usage for SkillsManager-Creation-Template
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: Tool usage is part of the governed runtime surface.
---

# Cli_Toolbox Usage

## Read runtime contract
```bash
python3 ./scripts/Cli_Toolbox.py contract --json
```

## Read supported profiles
```bash
python3 ./scripts/Cli_Toolbox.py profile --json
```

## Generate a referenced governance skill
```bash
python3 ./scripts/Cli_Toolbox.py scaffold \
  --skill-name Demo-Skill \
  --target-root /tmp/demo_skills \
  --description "Demo referenced governance skill." \
  --doc-topology referenced \
  --tooling-surface contract_cli \
  --workflow-control guardrailed \
  --overwrite
```

## Generate a workflow skill
```bash
python3 ./scripts/Cli_Toolbox.py scaffold \
  --skill-name Demo-Workflow \
  --target-root /tmp/demo_skills \
  --description "Demo workflow skill." \
  --doc-topology workflow_path \
  --tooling-surface automation_cli \
  --workflow-control compiled \
  --overwrite
```
