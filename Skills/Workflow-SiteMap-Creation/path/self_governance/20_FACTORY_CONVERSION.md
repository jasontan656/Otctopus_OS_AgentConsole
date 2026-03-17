---
doc_id: workflow_sitemap_creation.path.self_governance.factory_conversion
doc_type: topic_atom
topic: Factory conversion rules for self governance
reading_chain:
- key: intent_enhance
  target: 30_INTENT_ENHANCE.md
  hop: next
  reason: factory 完成后先做意图强化，禁止直连落盘。
---

# Factory Conversion

- factory 化后的 payload 至少包含：
  - 当前轮次的结构化问题定义
  - 产物侧目标
  - 技能侧目标
  - 预期写入范围
  - 预期验证范围
  - 上下游关系
  - 目标真源路径
  - 禁止词
  - lint 轴
  - 技能演化信号
- 若用户输入没有显式写出这些元素，也要由本技能按当前稳定规则补齐。
- factory payload 必须服务后续 `$Meta-Enhance-Prompt` 强化，不得直接替代最终执行意图。
- factory payload 必须显式保留“当前轮次到底要做什么”的候选判断信号，供后续 nine-stage analysis_loop 裁决。
