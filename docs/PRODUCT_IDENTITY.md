# 产品身份

## 品牌

- 中文品牌：`章鱼 OS`
- 对外副标题：`自然语言驱动的多 Agent 控制台`
- 工程代号：`octopus-os-agent-console`

## 这个仓库是什么

这是章鱼 OS 的控制平面与技能基座仓库。

它不是：

- 一个只服务内部的技能镜像备份
- 一个纯文档项目
- 一个已经稳定的对外发行版

它是：

- 技能体系的产品化承载层
- 自然语言驱动的 Agent 工作方式的能力底座
- 未来一键安装、一键清理、工作区镜像与产品迭代日志的统一入口

## 对外叙事

推荐固定口径：

> 章鱼 OS 是一个自然语言驱动的多 Agent 控制台。  
> 它以技能为能力单元，以组合与编排为工作方式，让个人用户逐步搭建自己的定制化智能助理系统。

## 对内叙事

对内仍然保留以下硬事实：

- 这里是内部技能的唯一迭代源
- 技能修改后仍需推送到 `~/.codex/skills`
- 产品门面不应跟随技能推送进入安装目录

## 当前阶段

- release stage: `alpha`
- distribution strategy: `local-first`
- remote strategy: `current remote only acts as backup and traceability origin`
