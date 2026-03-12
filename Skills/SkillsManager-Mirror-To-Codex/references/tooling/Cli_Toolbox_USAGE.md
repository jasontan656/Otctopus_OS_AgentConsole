# Cli_Toolbox 使用文档

## 命名约束
- 统一入口：`scripts/Cli_Toolbox.py`
- 默认先做自动导航，再进入 `Push` 或 `Install`
- rename 场景必须显式进入 `Rename`

## 工具清单
- `Cli_Toolbox.sync_mirror_to_codex`

## 同步排除项（固定）
- `Codex_Skill_Runtime/`：运行态临时产物，不参与 mirror -> codex 同步。
- `.git/`、`__pycache__/`、`*.pyc`：仓库与编译缓存噪声，按 rsync exclude 固定过滤。

## 叙事式使用说明（固定格式）
### Cli_Toolbox.sync_mirror_to_codex（自动导航）
- 人类叙事版输入：
  - “把 mirror 里的某个技能导入 codex 安装目录，你先判断该走覆盖还是安装。”
  - 命令：
    - `python3 scripts/Cli_Toolbox.py --scope skill --skill-name Meta-Impact-Investigation`
    - `python3 scripts/Cli_Toolbox.py --scope skill --skill-name .system/skill-creator`
- 电脑动作发生了什么：
  - 解析参数并归一化 mirror/codex 根目录。
  - 将 `skill_name` 归一化为 skills 边界内的相对路径；允许 nested path，但拒绝空段、反斜杠、绝对路径与 `.` / `..` 越界段。
  - 若请求的是 `.system/*`，自动把 codex 目标目录收敛为小写规范名，并按实际 mirror 目录名解析源路径。
  - 先检查目标技能在 codex 安装目录是否已存在。
  - 若已存在，自动进入 `Push` 模式。
  - 若不存在，自动返回 `Install` 路由结果，不直接 rsync 创建目标目录。
- 人类叙事版输出：
  - 若进入 `Push`，返回 `status=ok` 与同步命令。
  - 若进入 `Install`，返回 `status=route_required`、`resolved_mode=install` 与外部技能顺序。

### Cli_Toolbox.sync_mirror_to_codex（Push / 全量）
- 人类叙事版输入：
  - “把 mirror 里当前所有技能完整同步回 codex 安装目录。”
  - 命令：
    - `python3 scripts/Cli_Toolbox.py --scope all --mode push`
- 电脑动作发生了什么：
  - 解析参数，确认已显式进入 `Push` 模式。
  - 扫描 mirror 顶层，发现真正可同步的技能根。
  - 仅对包含 `SKILL.md` 的顶层技能目录与 `.system/` 系统技能根执行 `rsync -a --delete --checksum`。
  - 顶层 `README.md`、`docs/`、`product_tools/` 等产品层对象不会进入 codex 安装目录。
- 人类叙事版输出：
  - 返回 `status=ok`、`resolved_mode=push`、`synced_entries` 与实际 `commands`。

### Cli_Toolbox.sync_mirror_to_codex（Install / 单技能）
- 人类叙事版输入：
  - “这个技能还没安装，你不要直接覆盖，走安装链路。”
  - 命令：
    - `python3 scripts/Cli_Toolbox.py --scope skill --skill-name Meta-Impact-Investigation --mode install`
    - `python3 scripts/Cli_Toolbox.py --scope skill --skill-name .system/skill-installer --mode install`
- 电脑动作发生了什么：
  - 锁定源目录与目标目录，但不执行 rsync。
  - 输出外部技能顺序：
    - 先 `$Skill-creator`
    - 后 `$Skill-installer`
- 人类叙事版输出：
  - 返回 `status=route_required`，提示当前应由外部技能继续完成安装。

### Cli_Toolbox.sync_mirror_to_codex（Rename / 单技能）
- 人类叙事版输入：
  - “这个技能已经改名了，你把新目录内容覆盖旧目录，再把 codex 里的文件夹名一起改掉，不要保留双目录。”
  - 命令：
    - `python3 scripts/Cli_Toolbox.py --scope skill --skill-name WorkFlow-RealState-Posting-Web --mode rename --rename-from Meta-browser-operation`
- 电脑动作发生了什么：
  - 先验证 rename 是显式请求，并确认旧名与新名是两个不同的 skill path。
  - 要求 mirror 侧已经完成目录与内容重命名，新名字目录成为唯一源。
  - 用新目录内容先覆盖 codex 中旧目录，保留 `rsync -a --delete --checksum` 的清理语义。
  - 覆盖完成后，把 codex 中旧目录名改成新目录名，彻底消灭旧/新双目录并存。
- 人类叙事版输出：
  - 返回 `status=ok`、`resolved_mode=rename`、`rename_from`、`staged_destination`、最终 `destination` 与同步命令。

## 参数说明
- `--scope`：`all` 或 `skill`
- `--skill-name`：`scope=skill` 时必填；允许 `family/child-skill` 或 `.system/skill-creator` 这类 nested path
- `--mode`：`auto`、`push`、`install` 或 `rename`
- `--rename-from`：仅 `mode=rename` 时必填；表示 codex 安装目录中的旧 skill 名
- `--codex-root`：可选；未提供时按 `CODEX_SKILLS_ROOT`，否则回退到 `$HOME/.codex/skills`
- `--mirror-root`：可选；未提供时按 `CODEX_SKILLS_MIRROR_ROOT` 或自动发现/迁移 mirror 目录
- `--dry-run`：可选，预演同步命令

## 输出说明
- `resolved_mode=push`：
  - 已实际执行覆盖同步
- `synced_entries`：
  - 仅在 `scope=all` 下出现，列出真正被同步的技能根
- `resolved_mode=install`：
  - 仅完成路由，不直接安装
- `resolved_mode=rename`：
  - 已执行“新内容覆盖旧目录 + 目标目录更名”语义
- `source_skill_name` / `destination_skill_name`：
  - 仅在 `scope=skill` 下出现，用于显式区分 mirror 实际源目录名与 codex 安装目录规范名
- `rename_from_destination_skill_name`：
  - 仅在 `Rename` 下出现，用于明确旧目录在 codex 中的规范名
- `next_skills`：
  - 仅在 `Install` 路由下出现
