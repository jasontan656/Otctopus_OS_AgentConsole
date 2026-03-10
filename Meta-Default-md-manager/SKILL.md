---
name: "Meta-Default-md-manager"
description: "集中管理 workspace 内的常驻默认文档。当前提供 scan / lint / collect / push / target-contract CLI，并以静态治理合同约束工具行为。"
---

# Meta-Default-md-manager

## 1. 工具入口
- 本技能提供可执行 CLI：
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
  - `/home/jasontan656/AI_Projects/Codex_Skills_Mirror/AGENTS.md`
- 当前 CLI 的 scan 结果也必须严格限制在这两份受管目标内。

## 3. AGENTS 资产治理模型
- 外部 `AGENTS.md` 的规范形态是 `Part A only`。
- AGENTS 的 skill 内部 `human` 模版必须显式分成两段：
  - `<part_A> ... </part_A>`
  - `<part_B> ... </part_B>`
- skill 内部 `AGENTS_human.md` 必须承载 `Part A + Part B`。
- `Part A` 用于外部 `AGENTS.md` 的真实形态与真实回写内容。
- `Part B` 仅保留在 skill 内部 `human` 模版与对应 machine JSON 中，不直接推送到外部。
- machine JSON 只承载 `Part B` 的结构化内容。

## 4. 阶段阅读入口
- `scan`
  - 阅读入口：`references/runtime_contracts/SCAN_STAGE_CONTRACT.md`
- `collect`
  - 阅读入口：`references/runtime_contracts/COLLECT_STAGE_CONTRACT.md`
- `push`
  - 阅读入口：`references/runtime_contracts/PUSH_STAGE_CONTRACT.md`

## 5. 维护入口
- 本入口用于新增受管文件，而不是在门面内展开完整维护流程。
- 当用户要求让新文件进入治理范围时，先从这里进入，再按独立维护文档执行后续动作。
- 新增受管文件的详细工作流、联动修改面与验证要求，见 `references/tooling/GOVERNED_FILE_ONBOARDING.md`。

## 6. 参考入口
- [AGENTS 资产治理模型] -> [references/runtime_contracts/AGENTS_ASSET_GOVERNANCE.md]
- [AGENTS 结构模版] -> [references/runtime_contracts/AGENTS_content_structure.md]
- [Scan 规则合同] -> [references/runtime_contracts/SCAN_RULESET_CONTRACT.json]
- [Scan 阶段合同] -> [references/runtime_contracts/SCAN_STAGE_CONTRACT.md]
- [Collect 阶段合同] -> [references/runtime_contracts/COLLECT_STAGE_CONTRACT.md]
- [Push 阶段合同] -> [references/runtime_contracts/PUSH_STAGE_CONTRACT.md]
- [Payload 归档 JSON] -> [references/runtime_contracts/AGENTS_PAYLOAD_ARCHIVE.json]
- [技能运行状态] -> [references/runtime_contracts/SKILL_RUNTIME_CONTRACT.json]
- [当前受管资产根目录] -> [assets/managed_targets/AI_Projects]
- [新增受管文件维护流程] -> [references/tooling/GOVERNED_FILE_ONBOARDING.md]

## 7. 约束
- 工具实现必须以本技能当前保留的静态治理文档为准，不得回滚到旧的隐式分段或旧 CLI 结构。
- 各阶段文档必须独立加载。
- 除非用户显式要求完整流程，否则模型仅允许按需加载当前所需阶段内容，禁止默认通读全部阶段文档。
- `scan` 规则资产必须外置，不得把 disallowed list 或 keyword 规则重新硬编码进 CLI。
- `collect` 必须以外部源为真源覆盖技能内模版。
- `push` 必须以技能内模版为真源覆盖外部目标。
