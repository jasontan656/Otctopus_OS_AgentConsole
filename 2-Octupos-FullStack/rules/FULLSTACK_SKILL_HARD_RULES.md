# FULLSTACK Skill Hard Rules

适用技能：
- `2-Octupos-FullStack`

## Rule Set

1. 本技能用于 OctopusOS 的全栈文档驱动开发、长期维护与架构治理。
2. 本技能覆盖的顶层域固定为：
- `frontend`
- `backend`
- `database`
- `api_and_contracts`
- `deployment_and_runtime`
- `operations_and_maintenance`
- `app_and_multi_client`
- `integration_and_messaging`
- `testing_and_acceptance`
- `observability_and_security`
- `documentation_and_mother_doc_governance`
- `fullstack_graph_and_architecture_contracts`
3. 本技能本质上是“文档维护系统 + 开发落盘系统 + 架构治理系统”，不是单纯编码技能。
4. `mother_doc` 是顶层需求源与长期维护容器；单域实施不得绕过它直接定义真实意图。
5. `fullstack graph` 负责补充现状、结构边界、代码关系、文档关系、合同依赖与架构回写意图；但不得替代 `mother_doc` 作为需求源。
6. 文档必须原子化、分域清晰、人类可读、机器可消费；禁止把多域规则堆成单篇胖文档。
7. 顶层阶段顺序固定为：
- `mother_doc`
- `construction_plan`
- `implementation`
- `acceptance`
8. `implementation` 不得绕过 `construction_plan` 直接靠代码与测试定义真实意图。
9. 公共内核只承载跨域稳定规则；前端、后端、数据库、部署、运维、APP 等差异约束必须以下沉 overlay 承载，不得污染顶层内核。
10. 架构变化必须可回写；稳定决策应回写到 `mother_doc`、ADR 或 graph contract，而不是只留在代码差异里。
11. 在阶段级 CLI 合同尚未完成前，`references/runtime/SKILL_RUNTIME_CONTRACT.json` 是静态运行合同源；CLI 完成后切换为 CLI-first。
12. 技能内部规则不得覆盖 workspace/runtime 的外层硬合同。
