# Deployment Log Rules

适用阶段：`evidence`

## Core Rule

- 当系统达到可部署状态，或已经产生真实部署 witness 时，必须追加 deployment checkpoint。
- deployment checkpoint 是项目内部替代版本分支的交付检查点。

## Log Location

- 日志固定落在：
  - `Octopus_OS/Mother_Doc/Mother_Doc/common/development_logs/deployment_batches.md`

## Entry Semantics

- 每条 deployment checkpoint 必须绑定：
  - 对应的文档范围
  - 对应的代码范围
  - 当前部署/上线的 witness 摘要
- `deployment_batches.md` 不是规划文档，而是交付历史与线上检查点日志。
- 日志只保留摘要，不复制具体部署 diff 或文件级修改内容。
- 每条日志的 `summary` 必须等于同轮 Git 提交 message；具体修改内容交由 Git / GitHub 追踪。
