# AGENTS Payload Governance Contract

## 定位
- `agents-payload-contract` 是历史命名保留入口。
- 它现在治理的是 `AGENTS_human.md` 内的分域 machine contract block，而不是旧式单块 payload。

## 入口
- `./.venv_backend_skills/bin/python Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-payload-contract --source-path "<external AGENTS path>" --json`

## 适用边界
- 仅当调用者已经知道：
  - 目标 `AGENTS.md`
  - 需要改哪个分域 block
  - 不需要 target ranking / placement gate / centered push 主链裁决
- 其他常规维护，一律回到 `agents-maintain`。

## 工作流
1. 解析目标 `AGENTS.md` 的 governed mapping。
2. 读取目标的 `target-contract` 与相关分域 block。
3. 把用户意图压缩成最小、精确的 domain-contract 语义。
4. 只修改对应 block 的 `contract` 内容。
5. 运行 `lint`。

## 禁止项
- 不要扩写 reminder。
- 不要扩写 contract 正文。
- 不要把技能排序、repo 摘要、技术栈、Markdown 说明写进 block。
- 不要借模糊口语去推断隐藏意图。
