---
name: "skill-naming-manager"
description: 用于统一治理技能命名、prefix/family 归类、registry 注册与自然语言调用语义，方便整体调整技能命名规范和组织架构。
---

# Skill-Naming-Manager

## 1. 定位
- 本文件只做门面入口，不承载规则正文。
- 本技能的唯一主轴是：统一治理所有技能的命名规范、注册模型、prefix/family 组织方式，以及自然语言中的技能集合解析语义。
- 本技能是纯治理方法论技能，不提供本地 CLI；它负责命名与组织架构原则，不直接替代具体技能实现。

## 2. 必读顺序
1. 先读取 `references/naming_contract.md`。
2. 再读取 `references/registry_contract.md`。
3. 再读取 `references/skill_registry.yaml`，确认当前已登记技能与 family/prefix 归属。
4. 若用户要通过自然语言调用某个技能集合，再读取 `references/invocation_semantics.md`。
5. 若用户要改整体命名规范、prefix 体系或 family 组织架构，再读取 `references/rename_and_reorg_protocol.md`，并丢弃旧命名习惯带来的临时联想。

## 3. 分类入口
- 命名合同层：
  - `references/naming_contract.md`
- 注册合同层：
  - `references/registry_contract.md`
- 静态注册表层：
  - `references/skill_registry.yaml`
- 调用语义层：
  - `references/invocation_semantics.md`
- 重命名与重组层：
  - `references/rename_and_reorg_protocol.md`
- 工具层：
  - 无本地 `Cli_Toolbox.py`；本技能不提供 CLI。
- 运行边界层：
  - workspace/root `AGENTS.md`
  - concrete repo local `AGENTS.md`
  - `$skill-creation-template`
  - `$skill-mirror-to-codex`

## 4. 适用域
- 适用于：定义或调整全局技能命名规范、prefix 体系、family 分组与统一注册模型。
- 适用于：把自然语言里的“某前缀全技能”“某 family 技能集”收敛为稳定可解析的治理语义。
- 适用于：管理专门治理技能所创建的技能族群，例如 `[SKILL-GOV]`。
- 不适用于：替代具体技能的 domain 内容、脚本能力、repo 合同或安装执行本身。
- 若需要创建、改造或安装具体技能，本技能只给命名与注册边界，具体骨架仍由 `$skill-creation-template` 与 `$skill-mirror-to-codex` 承接。

## 5. 执行入口
- 统一入口：
  - 触发本技能后，按 `naming_contract -> registry_contract -> skill_registry -> invocation_semantics` 的顺序收敛命名规则。
- 变更入口：
  - 若是新增技能，先确定 `canonical_id`、`display_name`、`prefix`、`family`、`role_tag`。
  - 若用户要求“完成注册”但 registry 中已存在同一 `canonical_id`，则按更新流程覆盖该技能的注册字段，不重复新增第二条记录。
  - 若是整体改名或重组，转入 `rename_and_reorg_protocol.md` 对齐变更范围与迁移策略。
- 合同入口：
  - 无 runtime contract；本技能的有效内容来自静态治理文档。
- 资产入口：
  - 当前无本地模板资产或脚本入口。

## 6. 读取原则
- 门面只做路由，规则正文下沉到 `references/`。
- 需要什么读什么，不要把所有引用文档一次性展开成新的门面正文。
- 本技能是静态治理技能，markdown 参考文档就是主规则源；不要虚构不存在的 CLI 合同。
- 命名治理优先于局部命名偏好；新增技能时先落 canonical 规则，再考虑展示层名字。
- 注册请求默认按 `canonical_id` 执行 upsert；命中已登记技能时应更新原条目，而不是并列新增同名职责条目。
- registry 是自然语言技能路由的稳定锚点，没有注册就不应被当成 family/prefix 集合成员。
- `[SKILL-GOV]` 是当前专门用于治理技能族群的注册 family code；进入该族群的技能必须先完成 registry 登记。
- 改 prefix、family 或组织架构时，先改治理定义，再改消费方说法，避免自然语言与真实注册表漂移。
- 若命名规则、注册字段或调用语义变化，同步更新门面、参考文档与 tooling 说明。

## 7. 结构索引
```text
skill-naming-manager/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── naming_contract.md
│   ├── registry_contract.md
│   ├── skill_registry.yaml
│   ├── invocation_semantics.md
│   ├── rename_and_reorg_protocol.md
│   └── tooling/
├── assets/
└── tests/
```
