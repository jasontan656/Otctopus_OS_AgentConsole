---
name: "Meta-Default-md-manager"
description: "集中管理 workspace 内的常驻默认文档。当前处于无工具收敛期：不提供可执行 CLI，仅保留治理模型、资产文档与后续重建所需的静态归档。"
---

# Meta-Default-md-manager

## 1. 当前状态
- 本技能当前**不提供任何可执行工具入口**。
- `scripts/` 与 `tests/` 的代码文件已被整体移除，后续会在治理模型稳定后重建新的工具面。
- 模型不得自行假设 `Cli_Toolbox.py` 或其他历史脚本仍可运行。

## 2. 当前保留价值
- 保留 skill 内部的受管资产与审计文档。
- 保留 `references/runtime_contracts/` 下的静态治理合同与 payload 归档。
- 保留 `references/stages/` 下对 `scan / collect / push` 目标语义的非执行性说明。

## 3. 受管范围
- 默认治理 workspace 中非 `Octopus_OS/` 域的常驻默认文档。
- 当前扫描规则仍以既定文件名匹配为准，核心对象包括：
  - `AGENTS.md`
  - `.gitignore`
  - `Octopus_CodeBase_Backend/README.md`
  - `Octopus_CodeBase_Backend/Deployment_Guide.md`
- `Octopus_OS/` 仍然是显式排除域，其内部默认文档由 `2-Octupos-FullStack` 独占治理。

## 4. AGENTS 资产治理模型
- 外部 `AGENTS.md` 的规范形态是 `Part A only`。
- AGENTS 的 skill 内部 `human` 模版必须显式分成两段：
  - `<part_A> ... </part_A>`
  - `<part_B> ... </part_B>`
- skill 内部 `AGENTS_human.md` 必须承载 `Part A + Part B`。
- `Part A` 用于外部 `AGENTS.md` 的真实形态与真实回写内容。
- `Part B` 仅保留在 skill 内部 `human` 模版与对应 machine JSON 中，不直接推送到外部。
- machine JSON 只承载 `Part B` 的结构化内容。

## 5. 阶段目标定义
- `scan`
  - 只负责发现当前哪些文件处于本技能的受管范围，并输出清单。
  - 不负责写托管副本，不负责回写外部文件。
- `collect`
  - 只从外部受管 `AGENTS.md` 中回收 `<part_A> ... </part_A>` 到 skill 内部 `human` 模版。
  - `Part B` 必须保留 skill 内部既有内容，不得被外部文件覆盖。
- `push`
  - 只从 skill 内部 `human` 模版中提取 `<part_A> ... </part_A>` 回写到外部 `AGENTS.md`。
  - `Part B` 必须留在 skill 内部，不参与外推。

## 6. 维护入口
- 当用户要求修改 `AGENTS.md` 治理内容时，必须同时判断需求对 `Part A` 和 `Part B` 的影响。
- 默认必须把 `Part A` 与 `Part B` 视为一个联动对象审查，禁止只改其中一半然后假设另一半自动正确。
- 如果字段结构、payload shape 或分段标记发生变化，必须同步修改：
  - `human` 模版
  - machine JSON
  - 后续重建的新工具设计
- 本轮治理明确**不包含** external root `AGENTS.md` 与其对应的 skill 内部 root 模版资产。

## 7. 当前参考入口
- [AGENTS 资产治理模型] -> [references/runtime_contracts/AGENTS_ASSET_GOVERNANCE.md]
- [Payload 归档 JSON] -> [references/runtime_contracts/AGENTS_PAYLOAD_ARCHIVE.json]
- [技能运行状态] -> [references/runtime_contracts/SKILL_RUNTIME_CONTRACT.json]
- [阶段静态说明] -> [references/stages/scan/DIRECTIVE.json]
- [当前受管资产根目录] -> [assets/managed_targets/AI_Projects]

## 8. 约束
- 当前阶段不得把 `references/**/*.md` 或 `references/**/*.json` 误当成“已有工具可执行”的证明。
- 当前阶段的目标是先收敛治理模型，再重建工具；不要在 skill 内新增临时脚本替代旧 CLI。
- 后续重建工具时，必须以本技能当前保留的静态治理文档为准，不得回滚到旧的隐式分段或旧 CLI 结构。
