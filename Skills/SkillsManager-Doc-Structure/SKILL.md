---
name: SkillsManager-Doc-Structure
description: 治理 skills 内部 markdown 文档树、metadata 与 anchor graph 的技能。
metadata:
  doc_structure:
    doc_id: skillsmanager_doc_structure.entry.facade
    doc_type: skill_facade
    topic: Entry facade for the SkillsManager-Doc-Structure skill
    anchors:
    - target: ./references/runtime_contracts/SKILL_RUNTIME_CONTRACT_human.md
      relation: routes_to
      direction: downstream
      reason: The facade routes runtime execution to the CLI-first contract.
---

# SkillsManager-Doc-Structure

## Runtime Entry
- Full tool entry: `cd Skills/SkillsManager-Doc-Structure && npm run cli -- <command> ...`
- Contract-only compatibility entry: `./.venv_backend_skills/bin/python Skills/SkillsManager-Doc-Structure/scripts/Cli_Toolbox.py contract --json`
- CLI JSON is the primary runtime source; `SKILL.md` only remains as a facade and routing narrative.


## 1. 定位
- 本文件提供文档结构技能的入口节点与轨道分流。
- 本技能负责 skill 内部 markdown 文档从入口节点开始的 tree-first 组织、metadata 约束、anchor graph 与 fewshot 样例树。
- 本技能把知识面拆成三条入口轨：
  - 规则轨
  - fewshot 示例轨
  - 元信息轨
- 本技能另外提供三条 workflow 轨：
  - 查询 workflow
  - 架构组织 workflow
  - 单文件写作 workflow

## 2. 必读顺序
1. 先读取运行合同：
   - `cd Skills/SkillsManager-Doc-Structure && npm run cli -- runtime-contract --json`
2. 再进入规则轨：
   - `references/rules/00_RULE_SYSTEM_INDEX.md`
3. 再进入 fewshot 示例轨：
   - `references/fewshot/00_FEWSHOT_INDEX.md`
4. 再进入元信息轨：
   - `references/metadata/00_METADATA_INDEX.md`
5. 再进入 workflow 轨：
   - `references/workflows/00_FLOW_INDEX.md`
6. 若任务涉及 CLI 与 graph rebuild，再读取：
   - `references/tooling/Cli_Toolbox_USAGE.md`
   - `references/tooling/Cli_Toolbox_DEVELOPMENT.md`
7. 若任务涉及模板与 frontmatter，再读取：
   - `assets/templates/ROUTING_DOC_TEMPLATE.md`
   - `assets/templates/INDEX_DOC_TEMPLATE.md`
   - `assets/templates/ATOMIC_DOC_TEMPLATE.md`
   - `assets/templates/DOC_FRONTMATTER_TEMPLATE.yaml`

## 3. 分类入口
- 运行合同层：
  - `references/runtime/SKILL_DOCSTRUCTURE_RUNTIME_OVERVIEW.md`
- 规则轨：
  - `references/rules/00_RULE_SYSTEM_INDEX.md`
  - `references/methodology/SEMANTIC_ROUTING_TREE.md`
- fewshot 示例轨：
  - `references/fewshot/00_FEWSHOT_INDEX.md`
- 元信息轨：
  - `references/metadata/00_METADATA_INDEX.md`
- workflow 轨：
  - `references/workflows/00_FLOW_INDEX.md`
- 工具层：
  - `scripts/Cli_Toolbox.ts`
- 模板层：
  - `assets/templates/ROUTING_DOC_TEMPLATE.md`
  - `assets/templates/INDEX_DOC_TEMPLATE.md`
  - `assets/templates/ATOMIC_DOC_TEMPLATE.md`
  - `assets/templates/DOC_FRONTMATTER_TEMPLATE.yaml`
- 工具开发层：
  - `references/tooling/development/`

## 4. 适用域
- 适用于：skills 内 markdown 文档树设计、分叉节点设计、单 topic 原子文档、fewshot 样例树、frontmatter/anchors、graph JSON、文档 lint、self graph 重建。
- `guide_only` 目标技能为显式豁免形态：本技能读取其 `skill_mode` 后应返回 skip，而不是继续进入 graph/split lint。

## 5. 执行入口
- 完整工具入口必须在 skill 根目录执行：
  - `cd Skills/SkillsManager-Doc-Structure && npm run cli -- runtime-contract --json`
  - `cd Skills/SkillsManager-Doc-Structure && npm run cli -- lint-doc-anchors --target <skill_root> --json`
  - `cd Skills/SkillsManager-Doc-Structure && npm run cli -- lint-split-points --target <skill_root> --json`
  - `cd Skills/SkillsManager-Doc-Structure && npm run cli -- register-split-decision --target <skill_root> --doc <doc_path> --rule <rule_id> --decision <accepted|split_required> --note <text> --json`
  - `cd Skills/SkillsManager-Doc-Structure && npm run cli -- build-anchor-graph --target <skill_root> --json`
  - `cd Skills/SkillsManager-Doc-Structure && npm run cli -- rebuild-self-graph --json`
- Python `scripts/Cli_Toolbox.py` 只用于 `contract --json` 兼容读取；不要把它当成完整 lint CLI。

## 6. 读取原则
- 入口节点负责把读者送到对应知识轨与 workflow 轨。
- 文档结构规则以 CLI JSON 与下沉合同为准。
- 进入目标 skill 后先读取 `SKILL.md` 顶层 `skill_mode`。
- 若 `skill_mode=guide_only`，本技能只返回 `skipped` / `skipped_for_guide_only` 结果，不强行要求文档树。
- 文档树应先确定当前应进入哪一条知识轨，再确定对应 workflow。
- 文档结构应先形成清晰 tree，再用 anchors 把必要的跨层关系织成 graph。
- 若文档承担多个 topic 或多个独立分叉轴线，应优先拆分而不是堆补丁。
- 模型应从入口节点 -> 分叉节点 -> 主题原子节点逐层收敛读取，不默认通读整个 skill。

## 7. 结构索引
```text
SkillsManager-Doc-Structure/
├── SKILL.md
├── agents/
├── assets/
├── references/
│   ├── fewshot/
│   ├── metadata/
│   ├── methodology/
│   ├── rules/
│   ├── runtime/
│   ├── workflows/
│   └── tooling/
├── scripts/
├── src/
└── tests/
```
