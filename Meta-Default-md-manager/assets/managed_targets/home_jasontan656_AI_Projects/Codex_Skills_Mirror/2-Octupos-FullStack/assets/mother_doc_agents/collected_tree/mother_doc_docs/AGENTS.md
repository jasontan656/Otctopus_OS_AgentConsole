# AGENTS

## 1. 目标
- 当前层作用：root navigation scope for Mother_Doc docs; choose the container documentation scope to enter。
- 本文件只承担当前层入口索引与递归选域，不承载正文细节。

## 2. 同层入口
- `README.md`: 当前层用途说明；可选阅读，但如果当前目录内容发生变更，则必须考虑维护它。
- `Mother_Doc.md`: 当前层目录实体说明。

## 3. 下一层入口
- `Account_Service`: container documentation scope for `Account_Service`.
- `Admin_UI`: container documentation scope for `Admin_UI`.
- `AI_Service`: container documentation scope for `AI_Service`.
- `API_Gateway`: container documentation scope for `API_Gateway`.
- `File_Service`: container documentation scope for `File_Service`.
- `Identity_Service`: container documentation scope for `Identity_Service`.
- `Mother_Doc`: self-description container scope for the Mother_Doc container itself.
- `MQ_Broker`: container documentation scope for `MQ_Broker`.
- `Notification_Service`: container documentation scope for `Notification_Service`.
- `Object_Storage`: container documentation scope for `Object_Storage`.
- `Order_Service`: container documentation scope for `Order_Service`.
- `Payment_Service`: container documentation scope for `Payment_Service`.
- `Postgres_DB`: container documentation scope for `Postgres_DB`.
- `Redis_Cache`: container documentation scope for `Redis_Cache`.
- `User_UI`: container documentation scope for `User_UI`.

## 4. 选择规则
- 若当前 `AGENTS.md` 的索引不足以判断，再读取当前层 `README.md` 与同名实体文档。
- 再从当前 `AGENTS.md` 的入口中选择下一层或目标叶子。
- 选择时只依据强化后的用户意图，不跨到无关域。

## 5. 更新边界
- 当前层只负责把下一步入口说清楚，不负责替代下层正文。
- 当前层不得把别的域的规则、workflow 或实现细节混写进来。
- 如果当前目录本身或其下子路径被修改，必须同时检查同层 `README.md` 是否需要维护。

## 6. 索引契约
- 当前文件属于 `mother_doc_docs` 分支；总容器根与容器根的 `AGENTS.md` 由同一 AGENTS/README manager 的其他分支管理。
- 当前层索引必须同时指向同层用途文档、同层实体文档和下一层入口。
- 子路径说明必须简短且可判断作用域。

## 7. 递归动作
- 命中目标后进入下一层，重复当前链路。
- 直到完整影响面被覆盖，再执行文档覆盖写回或规则读取。
