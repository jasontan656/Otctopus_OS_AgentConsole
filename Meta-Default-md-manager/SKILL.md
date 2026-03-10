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
- 默认治理 workspace 中非 `Octopus_OS/` 域的常驻默认文档。
- 当前扫描规则仍以既定文件名匹配为准，核心对象包括：
  - `AGENTS.md`
  - `.gitignore`
  - `Octopus_CodeBase_Backend/README.md`
  - `Octopus_CodeBase_Backend/Deployment_Guide.md`
- `Octopus_OS/` 仍然是显式排除域，其内部默认文档由 `2-Octupos-FullStack` 独占治理。

## 3. AGENTS 资产治理模型
- 外部 `AGENTS.md` 的规范形态是 `Part A only`。
- AGENTS 的 skill 内部 `human` 模版必须显式分成两段：
  - `<part_A> ... </part_A>`
  - `<part_B> ... </part_B>`
- skill 内部 `AGENTS_human.md` 必须承载 `Part A + Part B`。
- `Part A` 用于外部 `AGENTS.md` 的真实形态与真实回写内容。
- `Part B` 仅保留在 skill 内部 `human` 模版与对应 machine JSON 中，不直接推送到外部。
- machine JSON 只承载 `Part B` 的结构化内容。

## 4. 阶段定义
- `scan`
  - 负责发现当前哪些文件处于本技能的受管范围，并输出清单。
  - 必须从外置 scan 规则资产读取文件名规则、关键字规则与 disallowed list。
  - 必须支持 stdout 与 json 两种输出；json 输出必须落盘到对应的 `Codex_Skill_Runtime` 文件夹。
  - 必须对扫描结果执行结构 lint。
- `collect`
  - 依据 scan 结果，在技能目录内创建或刷新对应的目录结构与受管文件。
  - 只从外部受管 `AGENTS.md` 中回收 `<part_A> ... </part_A>` 到 skill 内部 `human` 模版。
  - 必须以外部源为真源覆盖 skill mirror 与安装目录中的对应受管资产。
  - `Part B` 必须保留 skill 内部既有内容，不得被外部文件覆盖。
- `push`
  - 只从 skill 内部 `human` 模版中提取 `<part_A> ... </part_A>` 回写到外部 `AGENTS.md`。
  - 必须以技能内受管模版为真源，直接覆盖对应外部文件。
  - `Part B` 必须留在 skill 内部，不参与外推。

## 5. 维护入口
- 当用户要求修改本技能自身的规范、模版、stage 合同、运行逻辑或静态资产时，必须把所有隐式相关面一起纳入审查。
- 不允许只改某个单文件说明，然后忽略与之联动的 stage 文档、runtime contract、结构模版或受管资产规范。
- 当用户要求修改 `AGENTS.md` 治理内容时，必须同时判断需求对 `Part A` 和 `Part B` 的影响。
- 默认必须把 `Part A` 与 `Part B` 视为一个联动对象审查，禁止只改其中一半然后假设另一半自动正确。
- 如果字段结构、payload shape 或分段标记发生变化，必须同步修改：
  - `human` 模版
  - machine JSON
  - CLI 行为
- 如果受管文件名集合发生变化，必须同步补齐对应的结构模版与 lint 合同。

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

## 7. 约束
- 工具实现必须以本技能当前保留的静态治理文档为准，不得回滚到旧的隐式分段或旧 CLI 结构。
- `scan` 规则资产必须外置，不得把 disallowed list 或 keyword 规则重新硬编码进 CLI。
- `collect` 必须以外部源为真源覆盖技能内模版。
- `push` 必须以技能内模版为真源覆盖外部目标。
