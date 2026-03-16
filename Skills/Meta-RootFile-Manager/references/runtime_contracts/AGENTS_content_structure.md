# AGENTS Content Structure

## 目标形态
- 外部 `AGENTS.md` 的可见正文必须从头到尾就是一份完整成立的 runtime hook contract。
- 合同正文结束后，才允许追加 reminder 区。
- 更细的 machine contract 不再平铺在可见正文里，而是通过合同正文中的显式 CLI 读取命令按域二次读取。

## 外部结构
- 外部 `AGENTS.md` 必须包含：
  - hook header
  - `<contract> ... </contract>`
  - `<reminder> ... </reminder>`
- `contract` 是第一眼可见的强约束正文。
- `reminder` 只承载环境前提、核对提醒、协作提示等非执行性说明。
- `reminder` 不得混入硬合同语气。
- 外部文件不得出现任何 frontmatter 元数据块；`doc_id`、`doc_type`、`topic`、`anchors`、`owner` 等治理元信息只允许保留在内部真源。
- 外部文件不得出现 `<part_A> ... </part_A>`；这是内部装配壳，不是最终 surface。
- 外部文件不得出现 `<part_B>`。

## 内部结构
- 内部真源固定为 `AGENTS_human.md`。
- `AGENTS_human.md` 必须包含完整的外部可见合同面，并以 `<part_A>` 壳承载它，再追加 `<part_B>`。
- `<part_B>` 不再是单个大 payload，而是多个相互独立的 fenced `json` block。
- 每个 block 必须携带：
  - `domain_id`
  - `read_command_preview`
  - `contract`

## 分域约束
- 当前标准域顺序固定为：
  - `hook_identity`
  - `turn_start`
  - `runtime_constraints`
  - `execution_modes`
  - `repo_handoff`
  - `turn_end`
- 各域必须各占一个独立 `json` block。
- block 顺序必须与标准域顺序一致。
- block 不得缺域、重域或夹带非 `json` 内容。

## 语义边界
- `contract` 正文允许承载运行时硬约束、强制入口、路由与执行条件。
- `reminder` 只允许承载提醒，不得把“必须/不得/must/shall”这类硬约束放进去。
- `Part B` 只允许最小、纯机械、不可遗漏的 machine contract。
- `Part B` 不得承载技能排序、repo 摘要、技术栈清单、Markdown 叙事或其他软提示语义。

## CLI 读取关系
- `target-contract` 输出整体目标合同与分域读取入口。
- `agents-domain-contract --domain "<domain_id>"` 输出单个分域 machine contract。
- 可见合同正文中的二级读取命令，应与 `Part B` 中同域 `read_command_preview` 对应。
