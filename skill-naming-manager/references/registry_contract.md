# 注册合同

## 目标
- 为所有技能提供统一注册模型，让“这个技能属于哪个 prefix/family、能否被某句自然语言一次性调度”有稳定依据。

## 每个技能最少应登记的字段
- `canonical_id`
- `display_name`
- `prefix`
- `family`
- `role_tag`
- `status`
  - `active`
  - `deprecated`
  - `draft`
- `trigger_summary`
  - 一句话说明它在什么场景下应被调用
- `companion_skills`
  - 可选
  - 记录常见协作技能，而不是复制对方正文

## registry 的使用方式
- registry 是逻辑主表，不一定要求某个固定文件立刻存在。
- 只要你未来要做统一命名治理，就必须把技能当成“应被注册的对象”，而不是零散目录。
- 当用户说“使用某 prefix 系列全技能”时，模型应以 registry 字段为准，而不是凭目录名猜测。

## family 与 prefix 的关系
- prefix 是第一层聚类。
- family 是 prefix 下的语义分组。
- 一个技能默认只应有一个主 prefix 和一个主 family，避免同时归属多个主族导致路由歧义。

## 状态治理
- `active`
  - 当前可被正常调用和编排。
- `deprecated`
  - 仍可能被历史上下文提及，但不应作为新任务默认入口。
- `draft`
  - 已创建但尚未应被广泛路由。

## 迁移时要改什么
- 技能目录与 frontmatter `name`
- 显示名
- prefix / family / role_tag
- 用户自然语言中常用的系列称呼
- 与该技能强绑定的 companion skill 说明

## OK 定义
- 模型能明确回答一个技能属于哪个 prefix 和 family。
- 模型能判断一句自然语言是否在请求单技能、family 技能集还是 prefix 全族。
- 改命名规范时，有清楚的注册字段作为迁移锚点。
