# AGENTS

## 1. 目标
- 当前层作用：`Octopus_OS` 总容器根，承载所有独立容器的总入口。
- 先读 `README.md` 理解整体架构，再决定进入哪个容器。

## 2. 同层入口
- `README.md`: `Octopus_OS` 总介绍与当前顶层容器布局说明。

## 3. 下一层入口
- `Account_Service/`: account and profile domain container。
- `Admin_UI/`: admin-facing client container and future operator surface。
- `AI_Service/`: AI domain container。
- `API_Gateway/`: unified ingress container for routing, auth forwarding, and traffic control。
- `File_Service/`: file domain container。
- `Identity_Service/`: identity and auth domain container。
- `Mother_Doc/`: authoritative authored-document and OS_graph container。
- `MQ_Broker/`: message broker container。
- `Notification_Service/`: notification domain container。
- `Object_Storage/`: object storage container。
- `Order_Service/`: order domain container。
- `Payment_Service/`: payment domain container。
- `Postgres_DB/`: relational database container。
- `Redis_Cache/`: cache container。
- `User_UI/`: user-facing client container。

## 4. 选择规则
- 先读当前层 `README.md`，确认目标容器或目标系统边界。
- 只在用户需求命中该容器时进入对应容器路径，不跨到无关容器。

## 5. 更新边界
- 当前层只承担容器总索引，不承载各容器正文细节。
- 各容器的说明、文档和后续索引必须在各容器自己的路径中维护。

## 6. 索引契约
- 当前根层 `AGENTS.md` 属于 `octopus_os_root` 分支。
- 它必须固定指向 `README.md` 和所有当前顶层容器路径。

## 7. 递归动作
- 命中目标容器后，进入对应容器路径继续读取容器级 `AGENTS.md` 或 `README.md`。
- 若目标属于文档树，再转入 `Mother_Doc/docs/**` 的递归索引链。
