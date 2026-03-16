# AGENTS Asset Governance

## 真源与投影
- 外部 `AGENTS.md` 是受管 surface，不是手工散改文件。
- 内部 `AGENTS_human.md` 是唯一真源。
- `push` 以内部真源覆盖外部 surface。
- `collect` 只保留 reverse-sync / recovery 语义，不再属于日常维护主链。

## 外部资产规则
- 外部 `AGENTS.md` 必须只暴露可见合同面：
  - `<contract>`
  - `<reminder>`
- 外部不得携带任何 frontmatter 元数据块；`doc_id`、`doc_type`、`topic`、`anchors`、`owner` 等治理字段只允许存在于内部真源。
- 外部不得保留 `<part_A> ... </part_A>` 这类内部结构包裹标签。
- 外部不得携带任何 `Part B` machine contract block。

## 内部资产规则
- 内部 `AGENTS_human.md` 必须同时容纳：
  - 可见合同面
  - reminder 尾部
  - 分域 machine contract blocks
- `owner` 只允许存在于 frontmatter，不进入任何 `json` block。

## 维护主链
- 日常自然语言维护入口固定为 `agents-maintain`。
- 主链固定为：
  - target ranking
  - contract surface / domain block placement
  - ancestor duplicate gate
  - update `AGENTS_human.md`
  - centered push external `AGENTS.md`
  - lint

## 狭义 surgery
- `agents-payload-contract` 仍可用，但它只处理已知目标上的分域 machine contract surgery。
- 该入口不再承担 target ranking、层级裁决或日常主链闭环。

## 清理要求
- legacy `AGENTS_machine.json` 不得再生成。
- runtime/install 面不应保留旧 sidecar 残留。
- orphan `AGENTS_human.md` 映射必须被识别并裁决为恢复或删除。
