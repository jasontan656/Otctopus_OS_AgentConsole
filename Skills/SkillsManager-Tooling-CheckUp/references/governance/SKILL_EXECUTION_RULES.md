---
doc_id: skills_tooling_checkup.governance.execution_rules
doc_type: topic_atom
topic: Execution rules for reviewing and remediating self-built tooling wheels in installed skills
anchors:
- target: SKILL_DOCSTRUCTURE_POLICY.md
  relation: pairs_with
  direction: lateral
  reason: Execution rules and doc-structure policy should stay aligned.
- target: ../routing/TASK_ROUTING.md
  relation: implements
  direction: upstream
  reason: Task routing should send readers here for deep execution rules.
---

# Skill Execution Rules

## 本地目的
- 约束本技能如何判断已安装 skills 的 tooling code 是否违反 repo 已声明的 tech stack 基线，并在需要时推动修正。

## 当前边界
- 本技能只治理“已有依赖已可覆盖、却仍手写通用能力”的情况。
- 本技能也治理目标技能的工具代码与文档是否把 runtime 日志、默认产物与定向产物落到受管根路径。
- 本技能不负责新增依赖，不负责产出新的独立工具，不把目标 skill 的 domain-specific behavior 强行抽空成第三方库默认实现。

## 局部规则
- 先以 repo 已治理的 `skills_required_techstacks` 为唯一基线，再判断目标代码是否重复实现这些依赖已经覆盖的能力。
- 判断必须是语义级的：需要看输入、输出、约束、异常路径和调用方用途，不能只凭文件名、函数名或“看起来像 parser / validator”就直接定罪。
- 若任务涉及落盘治理，必须同时读代码和目标技能文档，确认 `/home/jasontan656/AI_Projects/Codex_Skill_Runtime` 与 `/home/jasontan656/AI_Projects/Codex_Skills_Result` 是否被显式声明并真正用于对应语义。
- 若目标技能存在“定向产物”语义，必须确认其工具入口支持或要求显式落点；未指定落点时，默认值必须回退到 `/home/jasontan656/AI_Projects/Codex_Skills_Result`。
- 若目标技能已有历史日志或产物散落在非受管目录，修正范围必须覆盖代码切换、文档声明和旧内容迁移责任，不能只改新增路径。
- 只有当替换后能减少自实现复杂度、且不丢失现有行为语义时，才应进入修正。
- 修正时优先删除冗余自实现，再接入现有依赖；同步维护目标 skill 的测试、文档、类型和契约。
- 本技能本身现在提供 CLI-first runtime contract 与 directive 输出；真正的目标 skill 执行与验证仍必须借助目标 skill 既有命令或 repo 已有治理命令完成。

## 例外与门禁
- 若当前 repo 合同没有把某个库声明为必用基线，即使它“更标准”，本技能也不能自行把它当成既定依赖要求。
- 若目标自实现承载 repo-specific contract、历史兼容语义或第三方库无法直接表达的行为，应保留实现或只做局部整理，不做强替换。
- 若目标技能的历史日志或产物包含人工整理价值、审计意义或用户交付语义，迁移策略应保持可追溯，不能粗暴清空。
- 进入修正前，应先完成目标 skill 自身合同阅读；退出前，必须完成目标 skill 现有测试 / lint，且 Python 改动还要补 `Dev-PythonCode-Constitution` lint。
