[OCTOPUS_CHANGE_CONTRACT - HARD ENFORCEMENT]
- 本合同适用于后端代码与前端代码。
- 术语映射：后端“输出”同等前端“UI 可观察行为”；后端“函数/类锚点”同等前端“组件/路由/状态/DOM锚点”。

0) Codebase 环境声明（Required）
- 本仓库是章鱼OS前端 codebase（运行时代码最终落盘目录）。
- 本仓库运行环境固定为：`Node.js LTS`（非 Python venv）。
- 包管理器选择顺序：`pnpm-lock.yaml -> pnpm`，`yarn.lock -> yarn`，`package-lock.json -> npm`，无 lockfile 时默认 `npm`。
- 依赖安装、代码执行、测试命令必须在上述 Node.js 工具链环境下运行。

1) Pre-Change (Required)
- 修改前必须先判断变更类型：`existing_change`（修改已有代码）或 `new_code_bootstrap`（首次落盘新代码）。
- 若是 `existing_change`：必须检索目标函数名/代码片段（前端同等：组件名/路由键/状态键/DOM锚点），并命中 `code_anchors.jsonl` 与 `impact_map.jsonl`；未命中即 `violation` 并停止修改。
- 若是 `new_code_bootstrap`：允许无历史锚点进入施工，但必须先创建初始锚点与初始影响映射（最小 stub），再写入业务代码。
- 禁止人工指定影响包，影响面必须由扫描器自动推导。
- 禁止人工提供 `expected impact` 或手工指定 `EXPECTED_IMPACT_PACKAGES`。

2) In-Change (Required)
- 覆盖面集合必须由机器计算：
  `coverage_set = direct_changed_packages U propagated_impacted_packages`
- 传播依据必须来自 `impact_map.jsonl` 与锚点关联关系。

3) Post-Change (Required)
- 对 coverage_set 内每个包，必须回填并更新：
  `plan.md`
  `spec_3l.md`
  `code_anchors.jsonl`
  `impact_map.jsonl`
  `current_test_commands.md`
  `tests/`
  `trace_log.jsonl`
- 当前施工任务包必须回填：`task_evidence/<TASK_ID>/refill_evidence.jsonl`。
- `spec_3l.md / impact_map.jsonl / trace_log.jsonl` 必须引用 `anchor_id`（后端与前端一致）。
- `code_anchors.jsonl` 必须反向引用文档路径（doc_refs）。
- `refill_evidence.jsonl` 每条必须引用：
  - `anchor_id`
  - `target_doc_path`
  - `decision_basis_refs`（指向扫描器产物）
  - `updated_by_commit`
- 双向绑定缺失即 `violation`。

4) CI Gates (Required)
- Diff Gate: 代码有变更但 coverage_set 工件未同步更新，或当前施工任务包缺少 `task_evidence/<TASK_ID>/refill_evidence.jsonl` => fail
- Anchor Gate: 锚点失配未更新 => fail
- Impact Expansion Gate: 传播链包未同步更新 => fail
- Behavior Evidence Gate: coverage_set 对应测试未执行或失败（后端行为测试/前端可观察行为测试） => fail
- Runtime Entry Smoke Gate: `README.md`/`Deployment_Guide.md`/`current_test_commands.md` 中新增或修改的可执行命令必须逐条实跑并成功，任一失败 => fail
- Regression Gate: 完工前必须执行回归测试集合（至少包含当前任务包测试 + 受影响链路测试）；缺执行记录或失败 => fail
- Observability Implementation Gate: 若代码未实现可检索的 `logs/metrics/traces/audit/ledger` 最小集合（至少存在结构化日志字段、指标暴露、trace 关联键、审计记录、事件账本落点），或无 lint 证据 => fail
- Observability Gate 收尾必须执行对应 codebase 的 lint CLI，并把结果回写 `task_evidence/<TASK_ID>/gate_report.json`；未生成 lint 报告或未回写 gate 字段一律 fail

5) Non-Bypass Rule
- No waiver.
- No bypass.
- Any gate fail blocks merge.

6) Scanner Evidence Outputs (Required)
- 固定存放目录（当前施工任务包内）：`task_evidence/<TASK_ID>/`
- 每次施工后必须产出并落盘：
  - `task_evidence/<TASK_ID>/coverage_set.json`
  - `task_evidence/<TASK_ID>/required_doc_updates.json`
  - `task_evidence/<TASK_ID>/gate_report.json`
  - `task_evidence/<TASK_ID>/refill_evidence.jsonl`
- 与回填文档的锚点绑定规则：
  - `plan.md` 必须包含 `evidence_bundle_path`，指向 `task_evidence/<TASK_ID>/`。
  - `trace_log.jsonl` 每条回填记录必须包含 `evidence_ref`（引用上述 4 个产物之一）。
  - `refill_evidence.jsonl` 每条必须引用 `anchor_id` 与 `target_doc_path`，并写明 `decision_basis_refs`（由哪些扫描器产物支持本次回填）。
  - 若文档更新无法追溯到 `task_evidence/<TASK_ID>/` 产物，判定 `violation`。

7) `plan.md` Mandatory Requirements
- `plan.md` 为任务包强制工件。
- `plan.md` 必须包含 `## 被修改文件` 章节。
- `## 被修改文件` 章节至少列出：
  - 文件绝对路径
  - 修改类型（新增/修改/删除）
  - 关联锚点（anchor_id）
  - 修改原因（对应四维合同：输入输出/副作用/时序/失败语义）
  - 受影响包（由扫描器自动推导）
  - 证据引用（`task_evidence/<TASK_ID>/` 下的产物路径）
- 若代码已变更但 `plan.md` 缺失或缺少 `## 被修改文件`，直接 `violation`。

8) `plan.md` Template (Copy-Paste)
```md
# 施工 Plan

## 1. 任务目标
- TASK_ID:
- 需求描述:
- BASE_REF:
- evidence_bundle_path: `task_evidence/<TASK_ID>/`

## 2. 变更类型判定
- 类型: `existing_change` | `new_code_bootstrap`
- 判定依据:

## 3. 自动覆盖面分析
- 直接改动包:
- 传播影响包（自动推导）:
- 扫描器产物目录: `task_evidence/<TASK_ID>/`
- coverage_set 生成命令/结果文件: `task_evidence/<TASK_ID>/coverage_set.json`
- required_doc_updates: `task_evidence/<TASK_ID>/required_doc_updates.json`
- gate_report: `task_evidence/<TASK_ID>/gate_report.json`

## 4. 四维合同映射
- 输入输出合同变更（后端：输入/输出；前端：UI可观察行为/DOM状态/URL状态）:
- 可观察副作用变更（后端：日志/DB/消息/外调/文件；前端：请求/存储/cookie/埋点/错误上报）:
- 时序一致性变更（后端：顺序/幂等/重试/并发一致性；前端：状态切换顺序/并发覆盖规则）:
- 失败语义变更（后端：异常/降级/补偿；前端：错误态UI/降级UI/重试回退）:

## 5. 被修改文件
| 文件路径 | 修改类型 | anchor_id | 修改原因 | 受影响包 | 证据引用 |
|---|---|---|---|---|---|
| /abs/path/example.tsx | modify | ANC-001 | 输出字段新增（同等前端：UI可见状态新增） | 01_xxx,07_xxx | task_evidence/TASK-001/coverage_set.json |

## 6. 工件回填清单（覆盖面包7类 + 任务级证据1类）
- [ ] plan.md
- [ ] spec_3l.md
- [ ] code_anchors.jsonl
- [ ] impact_map.jsonl
- [ ] current_test_commands.md
- [ ] tests/
- [ ] trace_log.jsonl
- [ ] task_evidence/<TASK_ID>/refill_evidence.jsonl

## 7. 回填证据日志（任务级）
- 文件: `task_evidence/<TASK_ID>/refill_evidence.jsonl`
- 每条必须包含:
  - `anchor_id`
  - `target_doc_path`
  - `decision_summary`
  - `decision_basis_refs`（coverage_set/required_doc_updates/gate_report）
  - `updated_by_commit`
- 示例:
  - `{\"anchor_id\":\"ANC-001\",\"target_doc_path\":\"01_xxx/spec_3l.md\",\"decision_summary\":\"字段新增触发文档回填\",\"decision_basis_refs\":[\"task_evidence/TASK-001/coverage_set.json\"],\"updated_by_commit\":\"<sha>\"}`

## 8. 测试执行计划
- 测试来源: `current_test_commands.md`
- 目标包与传播包测试清单（后端行为测试 + 前端可观察行为测试）:
- 执行结果记录位置: `trace_log.jsonl`
- `trace_log.jsonl` 每条必须包含 `evidence_ref`（指向 `task_evidence/<TASK_ID>/` 下产物）

## 9. 门禁结果
- Diff Gate:
- Anchor Gate:
- Impact Expansion Gate:
- Behavior Evidence Gate:

## 10. 完成判定
- [ ] coverage_set 内全部包已完成 7 类工件更新
- [ ] 当前施工任务包 `task_evidence/<TASK_ID>/refill_evidence.jsonl` 已更新
- [ ] 四维行为测试全部通过
- [ ] CI 全绿
```

9) Root Docs Maintenance (Required)
- 必须在 codebase 根目录长期维护 `README.md` 与 `Deployment_Guide.md`。
- 开发模式下的服务启动命令必须强制使用热加载（hot reload），禁止写入非热加载开发命令。
- `README.md` 必须包含“快速一键启动命令”，并使用“可复制粘贴即可执行”的完整命令（例如 `cd ... && pnpm dev --host` / `cd ... && npm run dev -- --host`）。
- 前端开发启动命令必须使用 dev server 热加载命令（例如 `pnpm dev --host` / `npm run dev -- --host` / `yarn dev --host`），禁止写入 `vite preview` 或生产模式启动作为开发命令。
- `README.md` 与 `Deployment_Guide.md` 中出现的命令必须经过实跑验证，禁止写入未验证命令。
- `Deployment_Guide.md` 必须记录当前部署实况：
  - 是否由 AI 管理
  - 是否由 systemd 管理
  - 当前服务清单
  - 运行形态（本地 + ngrok / 远端托管）
  - 随部署迁移持续更新，不允许长期过期
