# Cli_Toolbox Architecture Overview

适用技能：`2-Octupos-FullStack`

## 当前范围

- 当前提供一个统一 CLI 入口下的四个命令：
  - `Cli_Toolbox.mother_doc_stage`
  - `Cli_Toolbox.materialize_container_layout`
  - `Cli_Toolbox.implementation_stage`
  - `Cli_Toolbox.evidence_stage`

## 目标

- 用同一 CLI 入口显式分隔 `mother_doc`、`implementation`、`evidence` 三阶段作用域
- 为各阶段输出 scope、must_load、requires、produces
- 在 `mother_doc` 阶段接收 AI 已判定好的容器名
- 在工作目录创建同名容器目录
- 在 `Mother_Doc` 下创建同名文档目录
- 按容器族补齐 `README.md + common/` 骨架
- 对 `Mother_Doc` 特例补齐 `Mother_Doc/Mother_Doc/00_INDEX.md`
- 保持幂等
