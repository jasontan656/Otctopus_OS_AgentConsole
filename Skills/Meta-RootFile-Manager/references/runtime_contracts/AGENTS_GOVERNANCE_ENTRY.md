# AGENTS Governance Entry

## 稳定入口
- 日常 AGENTS 维护统一入口是 `agents-maintain`。
- 该入口接收自然语言请求，并完成：
  - governed target ranking
  - contract surface / domain block placement
  - ancestor inheritance / duplicate gate
  - 内部真源写入
  - centered push
  - lint

## 主链
- `自然语言意图 -> target ranking -> placement gate -> ancestor gate -> update AGENTS_human.md -> push -> lint`

## 承载裁决
- 可见 surface 的合同正文和 reminder 一起属于 `Part A`。
- 外部 `AGENTS.md` 只允许输出渲染后的最终可见内容，不得泄露任何内部模板壳。
- `Part A` 中：
  - `contract` 承载强约束与入口命令
  - `reminder` 承载提醒性信息
- `Part B` 只承载分域 machine contract blocks。
- frontmatter 元数据和 `<part_A>` 包裹标签只允许留在 `AGENTS_human.md`。

## 继承与重复
- 父级 `AGENTS` 语义对下级仍然生效。
- 父级已表达的语义，不得在子级重复声明。
- 检查范围覆盖：
  - 父/子 `contract`
  - 父/子 `Part B`
  - `Part A` 与 `Part B` 交叉重复
- `WRITE_EXEC` 标准固定块是唯一受控重复例外。

## 狭义入口
- `agents-payload-contract` 只保留为分域 block surgery 入口。
- `agents-domain-contract` 用于读取某个分域的二级 machine contract。
