# AGENTS

## 1. 目标
- 当前层作用：technology stack abstraction scope under code abstractions for the current container。
- 本文件只承担当前层入口索引与递归选域，不承载正文细节。

## 2. 同层入口
- `README.md`: 当前层用途说明。
- `stack.md`: 当前层目录实体说明。

## 3. 下一层入口
- `AI_Service/common/code_abstractions/stack/async_stack.md`: `async stack` leaf rule file inside the `stack` abstract domain.
- `AI_Service/common/code_abstractions/stack/runtime_stack.md`: `runtime stack` leaf rule file inside the `stack` abstract domain.
- `AI_Service/common/code_abstractions/stack/storage_stack.md`: `storage stack` leaf rule file inside the `stack` abstract domain.
- `AI_Service/common/code_abstractions/stack/transport_stack.md`: `transport stack` leaf rule file inside the `stack` abstract domain.

## 4. 选择规则
- 先读当前层 `README.md`，再读当前层同名实体文档。
- 再从当前 `AGENTS.md` 的入口中选择下一层或目标叶子。
- 选择时只依据强化后的用户意图，不跨到无关域。

## 5. 更新边界
- 当前层只负责把下一步入口说清楚，不负责替代下层正文。
- 当前层不得把别的域的规则、workflow 或实现细节混写进来。

## 6. 索引契约
- 当前文件属于 `mother_doc_docs` 分支；总容器根与容器根的 `AGENTS.md` 由同一 AGENTS manager 的其他分支管理。
- 当前层索引必须同时指向同层用途文档、同层实体文档和下一层入口。
- 子路径说明必须简短且可判断作用域。

## 7. 递归动作
- 命中目标后进入下一层，重复当前链路。
- 直到完整影响面被覆盖，再执行文档覆盖写回或规则读取。
