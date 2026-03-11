# 命名合同

## 目标
- 为所有技能定义统一、可长期治理的命名结构，避免目录名、显示名、自然语言称呼和 family 归属彼此漂移。

## 核心字段
- `canonical_id`
  - 技能的唯一安装名与注册主键。
  - 必须使用全小写 `hyphen-case`。
  - 例：`skill-naming-manager`、`meta-skill-template`、`temp-plan`
- `display_name`
  - 面向人类展示的标题。
  - 可保留大小写与分隔风格。
  - 例：`Skill-Naming-Manager`
- `prefix`
  - 技能族的第一层治理前缀。
  - 用于自然语言中的“某 prefix 系列”。
  - 例：`meta`、`skill`、`octopus`
- `family`
  - 某 prefix 下的语义簇。
  - 用于表达“一组承担相近职责的技能”。
  - 可使用稳定 family code。
  - 例：`governance`、`template`、`browser`、`[SKILL-GOV]`
- `role_tag`
  - 更细粒度的职责标签。
  - 例：`manager`、`router`、`template`、`installer`

## 命名分层
- 第一层是 `canonical_id`，它决定安装路径与 registry 主键。
- 第二层是 `display_name`，它只影响人类可读性，不影响 registry 主键。
- 第三层是 `prefix/family/role_tag`，它们负责组织与批量调用语义。

## 约束
- 不要把人类展示标题直接当安装名使用。
- 不要让目录名和 frontmatter `name` 分离。
- 不要只靠“看起来像同类”来判断 family；必须显式登记。
- prefix 应该稀少、稳定，不能每建一个技能就发明一个新 prefix。

## 推荐判断顺序
1. 先定这个技能是不是一个长期存在的能力单元。
2. 再定它的 `prefix` 属于哪一类。
3. 再定它的 `family`。
4. 最后定唯一 `canonical_id` 与展示层 `display_name`。

## 当前可接受的经验性前缀示意
- `meta`
  - Meta 层治理、思维、流程、规则技能。
- `skill`
  - 直接面向技能治理、注册、组织和调度的技能。
- `octopus`
  - 明确属于 Octopus 体系的业务或交付技能。

## Not OK
- 同一技能在不同地方使用多个 `canonical_id`。
- 只修改显示名，不同步确认 prefix/family 是否仍成立。
- 把“Meta-xxx”这种展示风格误当成真正的 canonical 规则来源。
- 想表达治理族群时只在文案里写“这一类技能”，但不在 registry 中落下像 `[SKILL-GOV]` 这样的稳定 family code。
