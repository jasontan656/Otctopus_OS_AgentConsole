# 调用语义

## 目标
- 把自然语言中的技能集合调用收敛成可重复解析的语义，而不是临时猜测。

## 核心句式
- `使用 <canonical_id> 完成本次任务`
  - 解析为单技能调用
- `使用 <family> 系列技能`
  - 解析为单 family 范围内的技能集合
- `使用 <family_code> 技能族`
  - 解析为显式 family code 对应的技能集合
- `使用 <prefix> 系列全技能`
  - 解析为某 prefix 下所有 `active` 技能
- `使用 <prefix>/<family> 系列技能`
  - 解析为某 prefix 下某 family 的活动技能

## 解析优先级
1. 先看是否明确点名 `canonical_id`
2. 再看是否是 `prefix/family`
3. 再看是否是单独 `family`
4. 最后才允许根据上下文做有限推断

## “全技能”的含义
- 默认只包含 registry 中 `status=active` 的技能。
- `deprecated` 不默认纳入。
- `draft` 不默认纳入，除非用户明确要求。

## `[SKILL-GOV]` 的当前含义
- 代表专门治理技能命名、注册、模板、镜像同步与同类治理动作的技能族。
- 当用户说“使用 `[SKILL-GOV]` 技能族”时，解析为 registry 中 `family=[SKILL-GOV]` 且 `status=active` 的技能集合。

## `[Skill_prod]` 的当前含义
- 代表围绕 console 产品化、`Skills/` 目录产品形态与 continuity 上下文维护的技能族。
- 当用户说“使用 `[Skill_prod]` 技能族”时，解析为 registry 中 `family=[Skill_prod]` 且 `status=active` 的技能集合。

## 对你提出的句式的解释
- `使用 skill prefix 系列全技能 完成本次任务`
  - 正常化理解应为：调用某个 prefix 族下所有已注册且 active 的技能。
  - 为了避免歧义，未来推荐固定说法为：
    - `使用 <prefix> 系列全技能`
    - 或 `使用 <prefix>/<family> 系列技能`

## 歧义处理
- 如果某自然语言短语同时可能指向 `display_name` 和 `family`，优先按 registry 中显式字段解析。
- 如果一个技能未注册，则不应被自动算进任何 family/prefix 集合。
- 若上下文无法判定，先回到注册语义，不要凭主观相似度硬拼集合。
