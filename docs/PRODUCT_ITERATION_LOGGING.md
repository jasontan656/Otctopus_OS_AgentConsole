# 产品迭代日志模型

## 目的

这个仓库的 Git 历史不再只是“技能修补痕迹”，而应该逐步成为章鱼 OS 的产品迭代日志。

## 提交语义

推荐让每次提交都尽量回答这些问题：

- 新增了什么产品思路或能力
- 移除了什么错误方向
- 优化了什么边界或流程
- 解决了什么已知问题
- 哪些设计判断被正式收敛

## 适合的提交风格

- `product: introduce Octopus OS product facade and sync boundary`
- `product: add manifest-based local install and uninstall skeleton`
- `sync: restrict all-scope push to skill roots only`
- `docs: document product identity and iteration model`

## 不推荐的提交风格

- `fix stuff`
- `update files`
- `misc cleanup`

## 价值

当开发者未来回看仓库历史时，看到的不是零散 patch，而是章鱼 OS 作为一个产品如何逐步被想清楚、被装配、被收敛。
