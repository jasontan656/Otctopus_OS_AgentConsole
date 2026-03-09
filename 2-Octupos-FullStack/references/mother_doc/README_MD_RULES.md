# README.md Rules For Mother_Doc

适用技能：`2-Octupos-FullStack`

## Fixed Role

- `README.md` 只说明当前目录的用途、边界与阅读入口。
- 它是当前层的用途说明，不是当前层的递归索引。

## Content Rule

- 必须说明当前层是什么。
- 必须说明当前层承载什么类型的内容。
- 必须提示同层 `agents.md` 是下一步导航入口。
- 不重复枚举下一层完整路径列表；路径索引统一交给 `agents.md`。

## Maintenance Rule

- 当前目录用途变化后，必须同步刷新当前层 `README.md`。
- 新增 `agents.md` 规则后，`README.md` 必须仍保持用途文档定位，不得被挤成索引副本。
- `README.md` 同样只维护当前状态，不保留旧版本说明。
