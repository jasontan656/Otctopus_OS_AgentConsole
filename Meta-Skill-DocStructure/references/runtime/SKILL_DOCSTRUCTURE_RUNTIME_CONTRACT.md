---
doc_id: "runtime.contract.audit"
doc_type: "runtime_contract"
topic: "Audit version of the Meta-Skill-DocStructure runtime contract"
anchors:
  - target: "../../SKILL.md"
    relation: "expands"
    direction: "upstream"
    reason: "This document expands the facade-level rules in SKILL.md."
  - target: "../tooling/Cli_Toolbox_USAGE.md"
    relation: "executed_via"
    direction: "downstream"
    reason: "Tooling usage turns the contract into actions."
---

# Runtime Contract

## 范围
- 只允许在 skill root 内组织和校验内部 markdown 文档。
- target 必须是带 `SKILL.md` 的 skill 目录。
- 默认 viewer target 就是当前 skill 自身；后续复用时可通过 `TARGET_SKILL_ROOT` 切换。

## 强制工作流
1. 先取 runtime contract。
2. 再运行 anchor lint。
3. 若要给页面与脚本消费，再产出 preview payload。
4. 修改本技能自身文档后，最后重建 `assets/runtime/self_anchor_graph.json`。
5. dev 模式通过 watcher server 热加载；常驻模式通过 systemd user service 运行。

## 强制思考链
1. `scope_check`
2. `doc_inventory`
3. `frontmatter_contract_check`
4. `anchor_graph_check`
5. `atomicity_signal_check`
6. `rewrite_or_split`
7. `preview_emit`

## Frontmatter 约束
- 普通 markdown 文档必须在 top-level frontmatter 提供：
  - `doc_id`
  - `doc_type`
  - `topic`
  - `anchors`
- `SKILL.md` 因为受 skill frontmatter 限制，必须把文档结构合同写在：
  - `metadata.doc_structure`
- frontmatter 模板固定在：
  - `assets/templates/DOC_FRONTMATTER_TEMPLATE.yaml`

## Anchor 约束
- 每个 markdown 文档至少一个 anchor。
- `target` 必须解析到 skill root 内另一个真实 markdown 文档。
- anchor 允许跨层、跨分支与跳读，但不能是死链接。

## Viewer 约束
- `Vue3 + Vue Flow` 页面必须默认落到 `SKILL.md`。
- 页面必须显示正文、出入边、anchor 挂钩方式与 graph 节点关系。
- 页面必须消费实时 payload，而不是静态快照。
