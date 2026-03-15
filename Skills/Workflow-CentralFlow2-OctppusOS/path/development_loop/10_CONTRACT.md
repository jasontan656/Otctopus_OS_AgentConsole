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

## 全局职责
- 当前技能的唯一主闭环为：`mother_doc -> construction_plan -> implementation -> acceptance`。
- `mother_doc` 是唯一需求源；`construction_plan` 负责把当前修改切片拆成 packs；`implementation` 只消费当前 active pack；`acceptance` 负责真实 witness 与交付收口。

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
