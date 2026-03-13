---
name: SkillsManager-Mirror-To-Codex
description: 将产品仓内的 syncable skills 导入 codex skills 安装目录，并在 `Push` / `Install` / `Rename` 三种模式之间使用受控入口完成同步或安装。
metadata:
  doc_structure:
    doc_id: skillsmanager_mirror_to_codex.entry.facade
    doc_type: skill_facade
    topic: Entry facade for the SkillsManager-Mirror-To-Codex skill
    anchors:
    - target: ./references/runtime_contracts/SKILL_RUNTIME_CONTRACT_human.md
      relation: routes_to
      direction: downstream
      reason: The facade routes runtime execution to the CLI-first contract.
---

# SkillsManager-Mirror-To-Codex

## Runtime Entry
- Primary runtime entry: `./.venv_backend_skills/bin/python Skills/SkillsManager-Mirror-To-Codex/scripts/Cli_Toolbox.py contract --json`
- CLI JSON is the primary runtime source; `SKILL.md` only remains as a facade and routing narrative.


## 1. 抽象层

### 1.1 目标
- 提供唯一入口，把 mirror 中的技能安全导入 codex 安装目录。
- 先判断目标技能在安装目录是否已存在，再在两种自动导航模式之间收敛：
  - `Push`
  - `Install`
- 为显式重命名场景提供第三个独立入口：
  - `Rename`
- 将 product repo 根目录固定为可见工程路径：`/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole`。

### 1.2 统一入口
- 本技能唯一 CLI 入口：`scripts/Cli_Toolbox.py`
- 本技能唯一本地工具名：`Cli_Toolbox.sync_mirror_to_codex`
- 默认导航模式：`auto`
- 显式 rename 模式：`--mode rename --scope skill --skill-name <new_name> --rename-from <old_name>`

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
- `Rename` 不参与 `auto` 猜测；必须显式指定 `--mode rename`

### 1.4 抽象层硬约束
- 除抽象层外，`Push`、`Install`、`Rename` 三个模式不得共享工作流正文。
- `scope=skill` 时必须提供 `skill_name`。
- `skill_name` 必须是 skills 边界内的相对路径；允许多段 nested path，但每段都必须通过白名单字符校验：`[A-Za-z0-9._-]+`。
- `skill_name` 禁止包含空段、反斜杠、绝对路径与 `.` / `..` 越界段。
- `.system/*` 技能在 codex 安装目录使用小写规范名；工具必须自动把 mirror 侧实际目录名映射到安装目录规范名。
- `Rename` 模式下必须显式提供 `--rename-from`，且旧名与新名不得相同。
- 只允许在 skills 边界目录内工作，禁止越界路径拼接。
- 若本回合此前已对 `Otctopus_OS_AgentConsole` 发生实际写入，则在完成真正写操作后，必须同回合执行该仓库自己的 Git 留痕收尾。

## 2. Push 模式

### 2.1 模式目标
- 当目标技能已存在于 codex 安装目录时，用 mirror 版本覆盖安装目录版本。

### 2.2 模式入口条件
- `scope=all`
- 或 `scope=skill` 且目标目录已存在
- 或显式指定 `--mode push`

### 2.3 模式工作流
1. 锁定源目录与目标目录。
2. 若 `scope=all`，先发现 mirror 顶层真正可同步的技能根，再逐个执行 `rsync -a --delete --checksum`。
3. 若 `scope=skill`，只对目标技能执行 `rsync -a --delete --checksum`。
4. 返回结构化 JSON，明确已执行覆盖同步。

### 2.4 模式输出
- `status=ok`
- `action=mirror_to_codex`
- `resolved_mode=push`
- `source`
- `destination`
- `command`（单技能）
- `commands`（全量）
- `synced_entries`（全量）

### 2.5 模式约束
- 仅执行 mirror -> codex 覆盖同步。
- 不负责格式修正。
- 不调用外部技能。
- `scope=all` 只允许同步技能根与 `.system/`，不得把产品门面、产品工具和顶层文档直接推入 codex 安装目录。

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

## 4. Rename 模式

### 4.1 模式目标
- 为技能重命名提供一个明确、单义的同步入口，避免 codex 安装目录同时保留新旧两个文件夹。

### 4.2 模式入口条件
- 显式指定 `--mode rename`
- 且 `scope=skill`
- 且同时提供：
  - `--skill-name <new_name>`
  - `--rename-from <old_name>`

### 4.3 模式工作流
1. 在真正修改前，先用 `$Meta-Impact-Investigation` 盘清 rename 影响面。
2. 在 mirror repo 中，直接完成 skill 文件夹与内容内的命名替换，形成新名字作为唯一源目录。
3. 推送时，用新名字对应的 mirror 源目录先覆盖 codex 中旧名字对应的目录，保持 `rsync -a --delete --checksum` 语义。
4. 覆盖完成后，把 codex 安装目录中的旧文件夹名落成新文件夹名，确保不会出现新旧双目录并存。
5. 其他非目录名变更，继续在 mirror 侧用 `apply_patch` 手工修改。

### 4.4 模式输出
- `status=ok`
- `action=mirror_rename_to_codex`
- `resolved_mode=rename`
- `rename_from`
- `rename_from_destination`
- `staged_destination`
- `destination`
- `command`
- `workflow`

### 4.5 模式约束
- 不参与 `auto` 模式推断。
- 不接受 `scope=all`。
- 若 codex 安装目录中旧名与新名都不存在，则应停止并要求改走 `Push` 或 `Install`，而不是伪装成 rename。
- rename 的目标是消灭双目录并存，而不是保留 old/new mapping 作为长期结构。

## 5. 工具与文档
- 工具入口：`scripts/Cli_Toolbox.py`
- Agent 元数据：`agents/openai.yaml`
- 使用文档：`references/tooling/Cli_Toolbox_USAGE.md`
- 开发文档：`references/tooling/Cli_Toolbox_DEVELOPMENT.md`

## 6. 方法论约束
- 先导航，再执行；不要先执行覆盖再事后解释为什么该覆盖。
- 已安装对象走 `Push`，未安装对象走 `Install`，显式重命名对象走 `Rename`，三者不得混用。
- `Install` 模式的价值是防止把“未安装 skill 的首次落盘”伪装成“覆盖同步”。
- `Rename` 模式的价值是防止把“技能更名”退化成“旧目录保留 + 新目录新建”。

## 7. 架构契约
```text
SkillsManager-Mirror-To-Codex/
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

## 8. 落地规则
- `Push`、`Install`、`Rename` 必须作为独立模式书写与维护。
- 抽象层可以共享入口、边界与路由合同；模式层禁止复用对方流程描述。
- 若修改了 `scripts/Cli_Toolbox.py`，必须同步更新相关 tooling 文档。
