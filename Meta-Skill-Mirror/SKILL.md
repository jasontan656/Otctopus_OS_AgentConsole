---
name: "Meta-Skill-Mirror"
description: 将 codex skill mirror 导入 codex skills 安装目录，并在 `Push` / `Install` 双模式之间自动导航。使用场景：需要把 mirror 中的技能落到安装目录、判断目标技能是否已安装、对已存在技能执行覆盖同步，或对尚未存在的技能先校验格式再走外部安装链路。
---

# Meta-Skill-Mirror

## 1. 抽象层

### 1.1 目标
- 提供唯一入口，把 mirror 中的技能安全导入 codex 安装目录。
- 先判断目标技能在安装目录是否已存在，再在两种模式之间自动导航：
  - `Push`
  - `Install`
- 将 mirror 根目录固定为非隐藏路径：`/home/jasontan656/AI_Projects/Codex_Skills_Mirror`。

### 1.2 统一入口
- 本技能唯一 CLI 入口：`scripts/Cli_Toolbox.py`
- 本技能唯一本地工具名：`Cli_Toolbox.sync_mirror_to_codex`
- 默认导航模式：`auto`

### 1.3 自动导航合同
- 输入至少包含：
  - `scope`
  - 可选 `skill_name`
- 路由顺序固定：
  1. 校验根路径与 `skill_name`
  2. 归一化 mirror 根目录
  3. 检查目标技能在 codex 安装目录是否已存在
  4. 已存在则进入 `Push`
  5. 不存在则进入 `Install`

### 1.4 抽象层硬约束
- 除抽象层外，`Push` 与 `Install` 两个模式不得共享工作流内容。
- `scope=skill` 时必须提供 `skill_name`。
- `skill_name` 必须通过白名单字符校验：`[A-Za-z0-9._-]+`。
- 只允许在 skills 边界目录内工作，禁止越界路径拼接。
- 若本回合此前已对 `Codex_Skills_Mirror` 发生实际写入，则在完成真正写操作后，必须同回合执行该仓库自己的 Git 留痕收尾。

## 2. Push 模式

### 2.1 模式目标
- 当目标技能已存在于 codex 安装目录时，用 mirror 版本覆盖安装目录版本。

### 2.2 模式入口条件
- `scope=all`
- 或 `scope=skill` 且目标目录已存在
- 或显式指定 `--mode push`

### 2.3 模式工作流
1. 锁定源目录与目标目录。
2. 执行 `rsync -a --delete`。
3. 返回结构化 JSON，明确已执行覆盖同步。

### 2.4 模式输出
- `status=ok`
- `action=mirror_to_codex`
- `resolved_mode=push`
- `source`
- `destination`
- `command`

### 2.5 模式约束
- 仅执行 mirror -> codex 覆盖同步。
- 不负责格式修正。
- 不调用外部技能。

## 3. Install 模式

### 3.1 模式目标
- 当目标技能尚未存在于 codex 安装目录时，不直接用 rsync 生造安装目录，而是先校验技能格式，再调用外部安装技能完成安装。

### 3.2 模式入口条件
- `scope=skill` 且目标目录不存在
- 或显式指定 `--mode install`

### 3.3 模式工作流
1. 检查目标技能目录不存在。
2. 先使用 `$Skill-creator` 校验当前 skill folder 的创建格式是否合规。
3. 若不合规，先修正到合规状态。
4. 再使用 `$Skill-installer` 执行安装。
5. 安装完成后，再次确认目标技能已出现在 codex 安装目录。

### 3.4 外部技能顺序
- 第一步：`$Skill-creator`
- 第二步：`$Skill-installer`

### 3.5 模式输出
- 若通过 CLI 自动导航到本模式，先返回结构化路由结果：
  - `status=route_required`
  - `action=install_via_external_skills`
  - `resolved_mode=install`
  - `next_skills`
  - `source`
  - `destination`
- 真正的安装动作由外部技能继续完成。

### 3.6 模式约束
- 不允许在目标目录缺失时直接执行 rsync 覆盖式创建。
- 不把 `$Skill-creator` 与 `$Skill-installer` 的完整实现复制进本技能。
- 本模式只声明自动导航顺序与进入条件，不接管外部技能内部实现。

## 4. 工具与文档
- 工具入口：`scripts/Cli_Toolbox.py`
- Agent 元数据：`agents/openai.yaml`
- 使用文档：`references/tooling/Cli_Toolbox_USAGE.md`
- 开发文档：`references/tooling/Cli_Toolbox_DEVELOPMENT.md`

## 5. 方法论约束
- 先导航，再执行；不要先执行覆盖再事后解释为什么该覆盖。
- 已安装对象走 `Push`，未安装对象走 `Install`，不得混用。
- `Install` 模式的价值是防止把“未安装 skill 的首次落盘”伪装成“覆盖同步”。

## 6. 架构契约
```text
Meta-Skill-Mirror/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
│   └── Cli_Toolbox.py
├── assets/
└── references/
    └── tooling/
        ├── Cli_Toolbox_USAGE.md
        ├── Cli_Toolbox_DEVELOPMENT.md
        └── development/
            ├── 00_ARCHITECTURE_OVERVIEW.md
            ├── 10_MODULE_CATALOG.yaml
            ├── 20_CATEGORY_INDEX.md
            ├── 90_CHANGELOG.md
            └── modules/
                ├── MODULE_TEMPLATE.md
                └── mod_sync_mirror.md
```

## 7. 落地规则
- `Push` 与 `Install` 必须作为独立模式书写与维护。
- 抽象层可以共享入口、边界与路由合同；模式层禁止复用对方流程描述。
- 若修改了 `scripts/Cli_Toolbox.py`，必须同步更新相关 tooling 文档。
