# Mother_Doc Entry Rules

适用技能：`2-Octupos-FullStack`

## Root Entry

- `Octopus_OS/Mother_Doc/README.md` 是镜像根说明。
- `Octopus_OS/Mother_Doc/agents.md` 是镜像根索引入口。
- `Octopus_OS/Mother_Doc/Mother_Doc/README.md` 说明 `Mother_Doc` 容器自身用途。
- `Octopus_OS/Mother_Doc/Mother_Doc/agents.md` 是 `Mother_Doc` 容器自身索引入口。
- `Mother_Doc` 当前入口形态以同名容器目录为主，不保留 `01-07` 这类编号治理目录。
- 禁止继续使用 `index.md`、`00_INDEX.md` 或其他平行索引文件作为入口。

## Dynamic Expansion

- 容器目录参考内容可以静态存在，但真实容器集合不是封闭白名单。
- AI 必须依据用户当前项目描述，判断是否需要横向新增容器目录。
- 若需求引入可独立部署、可独立演进或可独立承载职责的模块，AI 必须判定为可新增容器。

## Synchronized Creation

若决定新增容器，必须同步新增：

- `Octopus_OS/<Container_Name>/`
- `Octopus_OS/Mother_Doc/<Container_Name>/`

新增后必须同步补齐：

- 容器目录 `README.md`
- 容器文档目录 `README.md`
- 容器文档目录 `agents.md`
- 容器族对应的 `common/` 抽象层骨架
- 受影响父层与当前层的递归 `agents.md`

## Recursive Navigation Rule

- 先读当前层 `README.md` 理解当前作用域。
- 再读当前层 `agents.md` 查看下一层索引。
- 再根据强化后的用户意图选择下一层路径。
- 如此递归，直到完整影响面被覆盖。

## Structure Protocol

- 每个容器文档目录必须先固定为：
  - `README.md`
  - `agents.md`
  - `common/`
- `common/` 当前固定 5 个一级域：
  - `architecture/`
  - `stack/`
  - `naming/`
  - `contracts/`
  - `operations/`
- 每个最小知识点单独一个 `*.md`。
