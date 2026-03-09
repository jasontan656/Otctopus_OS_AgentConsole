# Octopus_OS

<!-- replace_me: 这里写当前项目总容器层的浓缩总结，内容应来自当前各容器与 Mother_Doc 的实际状态。 -->

## 1. 作用
- 当前文件是 `Octopus_OS` 总容器层的浓缩总结说明。
- 这里写人类和模型都能快速理解的顶层项目定位、容器分布和当前阶段概况。

## 2. 阅读关系
- 同层 `AGENTS.md` 是第一站索引与行动入口。
- 当 `AGENTS.md` 的锚点和入口已经足够判断当前任务时，可以不读本文件。
- 当本层容器布局、技能入口、代码去处、文档去处或 graph/evidence 去处发生变化时，必须维护本文件。

## 3. 顶层容器摘要
- `Account_Service/`: account and profile domain container.
- `Admin_UI/`: admin-facing client container and future operator surface.
- `AI_Service/`: AI domain container.
- `API_Gateway/`: unified ingress container for routing, auth forwarding, and traffic control.
- `File_Service/`: file domain container.
- `Identity_Service/`: identity and auth domain container.
- `Mother_Doc/`: authoritative authored-document, project-baseline, and OS_graph container.
- `MQ_Broker/`: message broker container.
- `Notification_Service/`: notification domain container.
- `Object_Storage/`: object storage container.
- `Order_Service/`: order domain container.
- `Payment_Service/`: payment domain container.
- `Postgres_DB/`: relational database container.
- `Redis_Cache/`: cache container.
- `User_UI/`: user-facing client container.

## 4. 当前维护约束
- 保持本文件为顶层总结，不在这里展开具体实现细节。
- 需要具体开发或回写规则时，转到同层 `AGENTS.md` 指向的章鱼OS技能锚点。
- 需要容器级细节时，进入对应容器目录下的 `README.md` 或 `Mother_Doc/docs/<Container_Name>/`。

## 5. 待补内容
- `replace_me`: 当前项目阶段总结。
- `replace_me`: 当前最关键的开发目标或上线目标。
