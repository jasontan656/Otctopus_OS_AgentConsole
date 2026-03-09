# Phase 1 Container Naming Reference

适用技能：`2-Octupos-FullStack`

## Naming Goal

- 一个目录 = 一个可独立部署或独立演进的单元。
- 名字必须让老板和开发者都能直接看懂用途。
- 顶层工作目录与 `Mother_Doc` 内的同名目录必须保持一致。
- 容器命名只解决“这个单元是什么”；容器内部抽象层由 `common/` 再细分。

## Preferred Suffixes

- `_UI`
- `_Gateway`
- `_Service`
- `_DB`
- `_Cache`
- `_Broker`
- `_Storage`

## Avoid

- `Shared_*`
- `Business_*`
- `Runtime_*`

## Family Mapping

- `Mother_Doc` -> `Mother_Doc`
- `*_UI` -> `UI`
- `*_Gateway` -> `Gateway`
- `*_Service` -> `Service`
- `*_DB` / `*_Cache` / `*_Broker` / `*_Storage` -> `Data_Infra`

## Examples

- `Mother_Doc`
- `User_UI`
- `Admin_UI`
- `API_Gateway`
- `Identity_Service`
- `Order_Service`
- `Mongo_DB`
- `Redis_Cache`
- `MQ_Broker`
- `Object_Storage`
