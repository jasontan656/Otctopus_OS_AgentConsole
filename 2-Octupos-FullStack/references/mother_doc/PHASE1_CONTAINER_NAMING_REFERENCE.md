# Phase 1 Container Naming Reference

适用技能：`2-Octupos-FullStack`

## 命名目标

- 一个目录 = 一个可独立部署或独立演进的单元。
- 名字必须让老板和开发者都能直接看懂用途。
- 顶层工作目录与 `Mother_Doc` 内的同名目录必须保持一致。
- 容器命名只解决“这个单元是什么”；容器内部的抽象层由 `common/` 再细分。

## 第一阶段优先后缀

- `_UI`
- `_Gateway`
- `_Service`
- `_DB`
- `_Cache`
- `_Broker`
- `_Storage`

## 第一阶段避免名称

- `Shared_*`
- `Business_*`
- `Runtime_*`

这些名字会把多个边界塞进一个桶，不利于后续按容器独立演进。

## 容器族归类

- `Mother_Doc` -> `Mother_Doc`
- `*_UI` -> `UI`
- `*_Gateway` -> `Gateway`
- `*_Service` -> `Service`
- `*_DB` / `*_Cache` / `*_Broker` / `*_Storage` -> `Data_Infra`

## 示例

- `Mother_Doc`（self-description entry lives at `Mother_Doc/Mother_Doc/`，self index lives at `Mother_Doc/Mother_Doc/00_INDEX.md`）
- `User_UI`
- `Admin_UI`
- `API_Gateway`
- `Identity_Service`
- `Order_Service`
- `Mongo_DB`
- `Redis_Cache`
- `MQ_Broker`
- `Object_Storage`
