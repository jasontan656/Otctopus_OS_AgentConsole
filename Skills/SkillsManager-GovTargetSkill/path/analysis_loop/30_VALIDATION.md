---
doc_id: skillsmanager_govtargetskill.path.analysis_loop.validation
doc_type: action_validation_doc
topic: Analysis loop global validation for governing a target skill
---

# analysis_loop 全局校验

- `research_baseline` 必须保留目标技能当前真实状态与问题证据，不能只写目标态。
- `architecture_convergence` 必须明确区分保留、删除、重写、替换、下放。
- `plan` 必须给出可执行迁移顺序、影响面与风险边界。
- `implementation` 若触及 CLI 或 Python，必须同步处理 contract、tooling 文档、lint 与 tests。
- `validation` 必须说明实际跑了哪些校验、哪些未跑以及原因。
- 整个治理动作必须符合 `Meta-keyword-first-edit`：避免 legacy 壳、兼容映射层与补丁痕迹残留。
