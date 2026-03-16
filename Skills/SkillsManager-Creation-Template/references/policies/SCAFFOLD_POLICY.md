---
doc_id: skillsmanager_creation_template.references.policies.scaffold_policy
doc_type: topic_atom
topic: Scaffold policy for final-form skill generation
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This policy defines what the scaffold generator must create.
---

# Scaffold Policy

## 基线目录
- `inline`
  - 必须生成：`SKILL.md`、`agents/openai.yaml`
- `referenced`
  - 必须生成：`SKILL.md`、`agents/openai.yaml`、`references/`
  - 若 `tooling_surface != none`，再生成：`scripts/`、`tests/`
- `workflow_path`
  - 必须生成：`SKILL.md`、`agents/openai.yaml`、`references/`、`path/`
  - 若 `tooling_surface != none`，再生成：`scripts/`、`tests/`

## 合同规则
- 只要生成 `scripts/`，就必须同步生成：
  - `references/runtime_contracts/SKILL_RUNTIME_CONTRACT.json`
  - `references/runtime_contracts/SKILL_RUNTIME_CONTRACT_human.md`
  - `references/tooling/Cli_Toolbox_USAGE.md`
  - `references/tooling/Cli_Toolbox_DEVELOPMENT.md`
  - 至少一个 CLI 回归测试
- 若 `workflow_control == compiled`，`path/` 必须包含入口、合同、workflow index、步骤节点与验证节点。
- 生成器写出的成品必须像一次性正确创建出来的目标形态，不保留 legacy shell、过渡 alias 或映射层。

## 下放边界
- repo-local 运行结果目录不属于模板强约束。
- 具体业务文案、业务 schema 与业务 action 不属于本技能模板正文。
