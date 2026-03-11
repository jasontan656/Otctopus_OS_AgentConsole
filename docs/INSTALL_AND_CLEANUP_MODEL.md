# 安装与清理模型

## 目标

未来对外试用必须支持：

- 一键安装
- 安装前覆盖警告
- 一键清理
- 不误删用户无关文件

## 最小模型

安装器必须同时处理两处目标：

1. `~/.codex/skills`
2. 用户指定的章鱼 OS workspace 目录

## 安装前必须输出

- 将同步哪些技能
- 哪些同名技能会被覆盖
- workspace 将创建到哪里
- 清理时会删除或恢复哪些对象

## 清理必须遵循 manifest

禁止按“猜测某些目录应该属于章鱼 OS”来删除。

必须依赖安装时生成的 manifest：

- install session id
- codex root
- workspace root
- installed skill list
- overwritten skill backups

## 当前实现状态

仓库已新增 `product_tools/octopus_os_agent_console.py` 作为产品安装器骨架，提供：

- `plan`
- `install`
- `uninstall`

它当前已经具备：

- 技能根发现
- 覆盖警告
- workspace 镜像落盘
- manifest 写入
- 基于 manifest 的卸载

后续仍可继续增强：

- 更细粒度的冲突检测
- 用户修改检测
- rollback 审计输出
