---
doc_id: workflow_centralflow2_octppusos.path.development_loop.contract
doc_type: action_contract_doc
topic: Development loop contract
reading_chain:
- key: tools
  target: 15_TOOLS.md
  hop: next
  reason: 先读全局合同，再看工具与运行时辅助面。
---

# 开发闭环合同

## Contract Header
- `contract_name`: `workflow_centralflow2_development_loop_contract`
- `contract_version`: `1.0.0`
- `validation_mode`: `strict`
- `required_fields`:
  - `global_responsibilities`
  - `global_boundaries`
  - `resident_docs`
  - `stage_order`
- `optional_fields`:
  - `notes`

## 全局职责
- 当前技能的唯一主闭环为：`mother_doc_audit -> mother_doc -> construction_plan -> implementation -> acceptance`。
- `mother_doc_audit` 是固定前置治理阶段；它先清理文档树结构、识别 growth debt，并在需要时先完成拆分与注册，再允许进入 `mother_doc`。
- `mother_doc` 是唯一需求源；`construction_plan` 负责把当前修改切片拆成 packs；`implementation` 只消费当前 active pack；`acceptance` 负责真实 witness 与交付收口。
- `mother_doc` 默认应主动把语义长成更细的框架树，而不是尽量把内容塞回现有文档；只要当前节点已经承载多个独立语义，就应优先考虑替用户做拆分与分叉裁决。

## 全局边界
- 当前技能只服务当前 `target_root` 的开发文档与实现闭环，不替代项目结构治理。
- 动态运行态必须先由 CLI 解析，再进入具体阶段；门面与静态文档链不直接内嵌这些路径值。
- 只有极少数全局常驻合同允许跨阶段保留；其余 focus 必须在阶段切换时丢弃。

## 全局常驻项
- `/home/jasontan656/AI_Projects/AGENTS.md`
- `<docs_root>/AGENTS.md`，若当前目标已存在
- 当前技能主闭环合同与当前阶段 checklist

## 下一跳列表
- [tools]：`15_TOOLS.md`
