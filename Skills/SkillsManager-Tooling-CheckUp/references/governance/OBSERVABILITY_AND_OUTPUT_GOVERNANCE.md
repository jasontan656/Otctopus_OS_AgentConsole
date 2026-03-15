---
doc_id: skills_tooling_checkup.governance.observability_and_output_governance
doc_type: topic_atom
topic: Semantic governance for runtime observability, artifact output roots, and migration
  duties in target skills
---

# Observability And Output Governance

## 本地目的
- 为 `SkillsManager-Tooling-CheckUp` 增加第二条显式治理轴线：不仅检查是否重复造轮子，也要检查目标 skill 的工具代码是否把运行时日志、通用产物与定向产物落盘到受管根路径。
- 该检查必须基于代码语义、调用关系与文档合同，不依赖 lint 规则机械命中。

## 强制根路径
- 技能工具的可观测性日志、运行时审计信息、调试痕迹与类似 runtime 侧落盘，必须显式治理到 `/home/jasontan656/AI_Projects/Codex_Skill_Runtime`。
- 技能工具的通用生成物、默认结果集、汇总产物与类似 result 侧落盘，必须显式治理到 `/home/jasontan656/AI_Projects/Codex_Skills_Result`。
- 若目标技能属于“定向产物”类型，即产物天然面向用户指定位置，例如爬虫、抓取、导出、批处理同步等，则使用技能时必须支持或要求显式提供落点路径。
- 若这类定向产物技能在调用时未指定落点，则默认回退到 `/home/jasontan656/AI_Projects/Codex_Skills_Result`，不能私自散落到其他目录。

## 语义检查要求
- 必须读目标技能的实际代码语义，确认日志写入、默认输出目录、显式参数入口、路径回退逻辑和调用方约束是否真的存在。
- 必须检查目标技能文档是否显式声明日志落点与产物落点，而不是只在代码里隐式存在。
- 若目标技能已有本地 `Cli_Toolbox.py` 或等价入口，应确认 CLI 使用文档、开发文档或 runtime 合同中至少有一处把这两个根路径说明清楚。
- 若目标技能没有本地 CLI，也必须在其技能文档或运行时合同里说明等价的落盘约束。

## 迁移治理要求
- 若目标技能已将日志、缓存、产物或审计文件落到非受管目录，治理时不能只改新代码路径；必须把已有内容的迁移策略纳入范围。
- 迁移至少要覆盖三件事：旧路径识别、代码写入路径切换、已有日志或产物向新受管根路径的整理或搬迁。
- 若历史内容不适合自动搬迁，也必须在文档中显式声明处置方式，避免新旧目录长期并存且无主。

## 不可机械化的原因
- 同一路径字符串可能同时承担缓存、结果、模板或输入资产角色，不能只靠 grep 或 lint 机械定性。
- 某些技能把“日志”包装成 markdown、jsonl、html 或数据库样式文件；是否属于 runtime 可观测性，必须按用途语义判断。
- 某些技能把“产物”拆成下载原件、清洗中间件与最终交付件；是否属于定向产物、通用产物或运行时审计，也必须按行为边界判断。

## 退出门槛
- 只有当代码、默认路径、用户可控落点、文档声明和历史迁移责任五者都闭合时，才能判定该技能通过这条治理轴线。
