---
doc_id: skill_creation_template.path.template_creation.executable.template
doc_type: topic_atom
topic: Template blueprint for executable_workflow_skill template creation
anchors:
- target: 10_CONTRACT.md
  relation: implements
  direction: upstream
  reason: The target-state template follows the executable workflow contract.
- target: 15_TOOLS.md
  relation: routes_to
  direction: downstream
  reason: Tool guidance follows after the target-state template is confirmed.
---

# Executable Workflow Target State

## 根目录结构
```text
<skill-name>/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── path/
│   └── primary_flow/
│       ├── 00_PRIMARY_FLOW_ENTRY.md
│       ├── 10_CONTRACT.md
│       ├── 15_TOOLS.md
│       ├── 20_WORKFLOW_INDEX.md
│       ├── 30_VALIDATION.md
│       └── steps/
│           ├── step_01/
│           ├── step_02/
│           └── step_03/
└── scripts/
    ├── Cli_Toolbox.py
    └── test_skill_layout.py
```

## 门面目标
- `SKILL.md` 只保留：模型立刻需要知道的事情、功能入口、目录结构图。
- `SKILL.md` 直接暴露功能入口，而不是再多套一层 root 索引。
- 门面不回填复合步骤正文。

## 路径目标
- `path/primary_flow/` 作为默认功能入口，先进入：
  - `10_CONTRACT.md`
  - `15_TOOLS.md`
  - `20_WORKFLOW_INDEX.md`
- workflow index 再进入 `steps/` 下的复合步骤。
- 每个步骤继续承载自己的：
  - `contract`
  - `tools`
  - `execution`
  - `validation`

## 下一跳列表
- [tools]：`15_TOOLS.md`
