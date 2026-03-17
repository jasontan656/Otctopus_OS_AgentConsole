# Factory Stage

- factory 负责请求拆分与结构化输出，不负责替代后续决策。
- 输出至少包含问题定义、产物侧目标、技能侧目标、写入范围、验证范围、下游消费者与 keyword-first 候选动作。
- factory payload 之后必须进入 `$Meta-Enhance-Prompt`。
