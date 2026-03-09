---
name: "Meta-Skill-Mirror"
description: 将 codex skill mirror 单向同步到 codex skills 安装目录（全量或单技能），并维护非隐藏 mirror 根目录。
---

# Meta-Skill-Mirror

## 1. 目标
- 提供唯一同步能力入口，避免“脚本散落 + 手工拷贝”导致目录漂移。
- 仅承载唯一动作：
  - `mirror -> codex`（全量/单技能）
- 将 mirror 根目录收敛到非隐藏路径 `~/AI_Projects/Codex_Skills_Mirror`。

## 2. 可用工具（可选填充，条目必须存在）
- 统一命名约束：技能内工具统一使用前缀 `Cli_Toolbox`。
- 工具清单（本技能）：
  - `Cli_Toolbox.sync_mirror_to_codex` - "将 mirror 同步到 codex 安装目录，支持 `--scope all|skill`。"
- 命令入口：`scripts/Cli_Toolbox.py`
- 文档同步约束（强制）：
  - 使用文档：`references/tooling/Cli_Toolbox_USAGE.md`
  - 开发文档：`references/tooling/Cli_Toolbox_DEVELOPMENT.md`
  - 工具变更必须同步更新以上两类文档。
  - `Cli_Toolbox_USAGE.md` 采用固定叙事：人类输入 -> 电脑动作 -> 人类输出。
- 开发文档结构化约束（强制）：
  - `references/tooling/development/00_ARCHITECTURE_OVERVIEW.md`
  - `references/tooling/development/10_MODULE_CATALOG.yaml`
  - `references/tooling/development/20_CATEGORY_INDEX.md`
  - `references/tooling/development/modules/MODULE_TEMPLATE.md`

## 3. 工作流约束
- 输入：范围（all/skill）+ 可选 `skill_name`。
- 步骤：
  - 校验根路径与 `skill_name`。
  - 归一化 mirror 根目录（可见目录优先）。
  - 执行 `rsync -a --delete`。
  - 若本回合此前已对 `Codex_Skills_Mirror` 发生实际写入，则在 sync 完成后，必须在同一回合执行该仓库的 GitHub 留痕收尾。
  - 输出结构化 JSON 执行结果。
- 输出：`status/action(固定 mirror_to_codex)/scope/source/destination/command`。
- 完成判定：返回 `status=ok`，且 `exit_code=0`。

## 4. 规则约束
- 禁止引入第三类业务动作（例如 lint、生成、重构）。
- `--scope skill` 时必须提供 `--skill-name`。
- `--skill-name` 必须通过白名单字符校验：`[A-Za-z0-9._-]+`。
- 只允许同步 skills 边界目录，禁止越界路径拼接。
- 默认 mirror 根目录必须是非隐藏路径：`/home/jasontan656/AI_Projects/Codex_Skills_Mirror`。
- 本技能不代替 GitHub hook；若本回合修改了 `Codex_Skills_Mirror`，必须在 sync 后另行执行：
  - `python3 /home/jasontan656/.codex/skills/Meta-github-operation/scripts/Cli_Toolbox.py commit-and-push --repo Codex_Skills_Mirror --message "<commit message>" --use-latest-claims --auto-scope --allow-empty`

## 5. 方法论约束
- 采用单入口 CLI：对外只暴露 `Cli_Toolbox.py`，避免多脚本并行入口。
- 采用职责纯度：入口脚本只做参数解析、路径归一化、调用 rsync、输出结果。
- 采用替换优先：已有同步路径优先覆盖，不叠加同义脚本。

## 6. 内联导航索引
- [Cli_Toolbox 工具入口] -> [scripts/Cli_Toolbox.py]
- [Agent 元数据] -> [agents/openai.yaml]
- [Cli_Toolbox 使用文档] -> [references/tooling/Cli_Toolbox_USAGE.md]
- [Cli_Toolbox 开发文档] -> [references/tooling/Cli_Toolbox_DEVELOPMENT.md]
- [Cli_Toolbox 开发架构总览] -> [references/tooling/development/00_ARCHITECTURE_OVERVIEW.md]
- [Cli_Toolbox 开发分类索引] -> [references/tooling/development/20_CATEGORY_INDEX.md]
- [Cli_Toolbox 模块目录] -> [references/tooling/development/10_MODULE_CATALOG.yaml]

## 7. 架构契约
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

落地规则：
- `1-7` 章节必须完整保留。
- 本技能仅允许 mirror -> codex 单向同步能力，不得扩张到其他治理动作。
