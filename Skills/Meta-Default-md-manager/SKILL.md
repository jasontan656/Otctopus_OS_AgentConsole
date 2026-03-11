---
name: "Meta-Default-md-manager"
description: "集中管理 workspace 内的常驻默认文档。当前提供 scan / lint / collect / push / target-contract CLI，并以静态治理合同约束工具行为。"
---

# Meta-Default-md-manager

## 1. 工具入口
- 本技能提供可执行 CLI：
  - `scaffold`
  - `scan`
  - `lint`
  - `collect`
  - `push`
  - `target-contract`
- 所有写操作类命令必须支持 `--dry-run`。
- 工具行为必须服从 `references/runtime_contracts/` 下的静态治理合同。

## 2. 受管范围
- 当前仅治理 `AI_Projects` 下两份 `AGENTS.md`：
  - `/home/jasontan656/AI_Projects/AGENTS.md`
  - `/home/jasontan656/AI_Projects/octopus-os-agent-console/AGENTS.md`
- 兼容路径 alias 仅允许作为 runtime fallback，不得再被表述为受管 repo 身份。
- 当前 CLI 的 scan 结果也必须严格限制在这两份受管目标内。

## 3. 双模版语义
- 本技能内与“模版”相关的语义只允许分成两类，后续文档必须按此命名：
  - `治理映射模版`
    - 定义：skill 内一对一收敛、长期保存、会被 `collect` / `push` 持续读写的被治理文件映射层。
    - 目的：承载某个具体外部目标当前的真实治理内容，而不是只承载初始化骨架。
    - 对 AGENTS 而言：`assets/managed_targets/.../AGENTS_human.md` 与 `AGENTS_machine.json` 这一对文件共同构成 `治理映射模版`。
    - 真源边界：`collect` 把外部真源收敛进来覆盖它；`push` 再把它作为内部真源推出去覆盖外部目标。
  - `骨架生成模版`
    - 定义：`scaffold` 阶段用于初始化新被治理目标的默认骨架生成规则与默认内容。
    - 目的：只负责产出第一版外部骨架与第一版 `治理映射模版`，不直接代表后续长期治理真源。
    - 生命周期：主要服务于初始化时刻；一旦具体目标开始被 `collect` / `push` 维护，长期语义应回到 `治理映射模版`。
- 术语边界：
  - `治理映射模版` 不是“结构合同”；它承载具体目标内容。
  - `骨架生成模版` 不是“长期真源模版”；它只负责初始化。
  - `AGENTS_content_structure.md` 这类结构合同不属于上述两类模版，它只定义形状约束。

## 4. AGENTS 资产治理模型
- 外部 `AGENTS.md` 的规范形态是 `Part A only`。
- AGENTS 的 skill 内部 `human` 模版必须显式分成两段：
  - `<part_A> ... </part_A>`
  - `<part_B> ... </part_B>`
- skill 内部 `AGENTS_human.md` 必须承载 `Part A + Part B`，并且它属于 `治理映射模版`。
- `Part A` 用于外部 `AGENTS.md` 的真实形态与真实回写内容。
- `Part B` 仅保留在 skill 内部 `human` 模版与对应 machine JSON 中，不直接推送到外部。
- machine JSON 只承载 `Part B` 的结构化内容，并且与 `AGENTS_human.md` 一起构成同一个 `治理映射模版`。

## 5. 阶段阅读入口
- `scaffold`
  - 说明：使用 `骨架生成模版` 在用户指定目录落下第一版被治理文件骨架，并同步创建第一版 `治理映射模版`。
  - 阅读入口：`references/runtime_contracts/SCAFFOLD_STAGE_CONTRACT.md`
- `new-file`
  - 说明：把新的被治理文件类型正式纳入本技能支持范围，并为该文件类型同时定义 `治理映射模版` 与 `骨架生成模版` 的语义。
  - 阅读入口：`references/runtime_contracts/NEW_FILE_STAGE_CONTRACT.md`
- `scan`
  - 说明：发现当前已经处于治理范围内的外部目标。
  - 阅读入口：`references/runtime_contracts/SCAN_STAGE_CONTRACT.md`
- `collect`
  - 说明：把外部真源内容回收覆盖到技能内部 `治理映射模版`。
  - 阅读入口：`references/runtime_contracts/COLLECT_STAGE_CONTRACT.md`
- `push`
  - 说明：把技能内部 `治理映射模版` 内容直接覆盖推送到外部目标。
  - 阅读入口：`references/runtime_contracts/PUSH_STAGE_CONTRACT.md`

## 6. 维护入口
- 本入口只描述技能自身维护，不承载新增被治理目标的具体阶段流程。
- 当用户要求修改脚本、架构或通用约束时，从这里进入。
- 当用户要求新增被治理目录或新增被治理文件类型时，分别转到 `scaffold` 或 `new-file` 阶段文档。

## 7. 参考入口
- [AGENTS 资产治理模型] -> [references/runtime_contracts/AGENTS_ASSET_GOVERNANCE.md]
- [AGENTS 结构模版] -> [references/runtime_contracts/AGENTS_content_structure.md]
- [Scaffold 阶段合同] -> [references/runtime_contracts/SCAFFOLD_STAGE_CONTRACT.md]
- [New-File 阶段合同] -> [references/runtime_contracts/NEW_FILE_STAGE_CONTRACT.md]
- [Scan 规则合同] -> [references/runtime_contracts/SCAN_RULESET_CONTRACT.json]
- [Scan 阶段合同] -> [references/runtime_contracts/SCAN_STAGE_CONTRACT.md]
- [Collect 阶段合同] -> [references/runtime_contracts/COLLECT_STAGE_CONTRACT.md]
- [Push 阶段合同] -> [references/runtime_contracts/PUSH_STAGE_CONTRACT.md]
- [Payload 归档 JSON] -> [references/runtime_contracts/AGENTS_PAYLOAD_ARCHIVE.json]
- [技能运行状态] -> [references/runtime_contracts/SKILL_RUNTIME_CONTRACT.json]
- [当前受管资产根目录] -> [assets/managed_targets/AI_Projects]
- [新增被治理文件类型流程] -> [references/runtime_contracts/NEW_FILE_STAGE_CONTRACT.md]

## 8. 约束
- 工具实现必须以本技能当前保留的静态治理文档为准，不得回滚到旧的隐式分段或旧 CLI 结构。
- 各阶段文档必须独立加载。
- 除非用户显式要求完整流程，否则模型仅允许按需加载当前所需阶段内容，禁止默认通读全部阶段文档。
- `scan` 规则资产必须外置，不得把 disallowed list 或 keyword 规则重新硬编码进 CLI。
- `collect` 必须以外部源为真源覆盖技能内 `治理映射模版`。
- `push` 必须以技能内 `治理映射模版` 为真源覆盖外部目标。
- `scaffold` 只能消费 `骨架生成模版` 做初始化，不得把骨架初始化语义误当成长期治理真源。
