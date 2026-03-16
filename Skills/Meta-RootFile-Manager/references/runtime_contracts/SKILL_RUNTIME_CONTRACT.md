# Skill Runtime Contract

## 核心入口
- `contract`
- `scan`
- `lint`
- `collect`
- `push`
- `scaffold`
- `new-writeback`
- `target-contract`
- `agents-maintain`
- `agents-domain-contract`
- `agents-payload-contract`

## AGENTS 治理总则
- 可见 `AGENTS.md` surface 本身必须是完整成立的 runtime hook contract。
- 外部 `AGENTS.md` 只允许输出最终可见合同面，不得泄露 frontmatter 元数据或 `<part_A>` 内部壳。
- 可见合同面固定拆为：
  - `<contract>`
  - `<reminder>`
- `Part B` 固定拆为多个分域 `json` block，而不是单个扁平 payload。

## 日常主链
- 日常 AGENTS 维护必须走 `agents-maintain`。
- 主链固定为：
  - ranking
  - placement gate
  - internal truth update
  - centered push
  - lint

## 窄域入口
- `agents-domain-contract` 负责读取单个分域二级合同。
- `agents-payload-contract` 只保留为分域 block surgery 入口。

## Lint 必须拦截
- 外部 `AGENTS.md` 泄露 frontmatter 元数据或 `<part_A>` 内部壳
- 可见合同面缺失 `<contract>` 或 `<reminder>`
- 可见合同面不是“contract followed by reminder”纯结构
- reminder 中混入硬合同语气
- `Part B` 缺域、重域、无 `domain_id`、非 `json` 内容
- 父子 AGENTS 语义重复
- payload/contract block 中出现软提示语义
- legacy sidecar 与 orphan managed AGENTS 残留
