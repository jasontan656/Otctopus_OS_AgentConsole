# Cli_Toolbox Architecture Overview

适用技能：`2-Octupos-FullStack`

## 当前范围

- 一个统一 CLI 入口下，显式分离三阶段合同读取：
  - checklist
  - doc contract
  - command contract
  - graph contract

## Mother_Doc Structure

- `Mother_Doc` 每层目录都必须具备：
  - `README.md`
  - `agents.md`
  - `<folder_name>.md`
- `agents.md` 只属于 `Mother_Doc` 树，不进入实际工作目录容器。
