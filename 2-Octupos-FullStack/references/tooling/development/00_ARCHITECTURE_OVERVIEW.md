# Cli_Toolbox Architecture Overview

适用技能：`2-Octupos-FullStack`

## 当前范围

- 当前只提供一个第一阶段工具：
  - `Cli_Toolbox.materialize_container_layout`

## 目标

- 接收 AI 已判定好的容器名
- 在工作目录创建同名容器目录
- 在 `Mother_Doc` 下创建同名文档目录
- 按容器族补齐 `README.md + common/` 骨架
- 对 `Mother_Doc` 特例补齐 `Mother_Doc/Mother_Doc/00_INDEX.md`
- 保持幂等
