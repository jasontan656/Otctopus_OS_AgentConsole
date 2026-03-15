---
doc_id: skill_creation_template.path.template_creation.guide_with_tool.template
doc_type: topic_atom
topic: Template blueprint for guide_with_tool template creation
reading_chain:
- key: tools
  target: 15_TOOLS.md
  hop: next
  reason: Tool guidance follows after the target-state template is confirmed.
---

# Guide With Tool/Lint Target State

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
│       ├── 20_EXECUTION.md
│       └── 30_VALIDATION.md
└── scripts/
    ├── Cli_Toolbox.py
    └── test_skill_layout.py
```

## 门面目标
- `SKILL.md` 只保留：模型立刻需要知道的事情、功能入口、目录结构图。
- `SKILL.md` 直接暴露功能入口，而不是再多套一层 root 索引。
- 门面不回填深层正文。

## 路径目标
- 默认骨架提供一个功能入口 `path/primary_flow/`。
- 若后续新增平行入口，每个入口内部仍必须保持单线闭环：
  - `contract`
  - `tools`
  - `execution`
  - `validation`
- `tools` 节点承载当前入口自己的 tool/lint 说明；若只有 lint，没有额外工具，也不另外改名。

## 下一跳列表
- [tools]：`15_TOOLS.md`
