# AGENTS.md Rules For Mother_Doc

适用技能：`2-Octupos-FullStack`

## Fixed Role

- `AGENTS.md` 统一由 `mother_doc > agents_readme_manager` 管理。
- 管理范围固定为 3 类路径：
  - `Octopus_OS/AGENTS.md`
  - `Octopus_OS/<Container_Name>/AGENTS.md`
  - `Octopus_OS/Mother_Doc/docs/**/AGENTS.md`
- `Octopus_OS/AGENTS.md` 是总容器根入口，必须显式指向 `Octopus_OS/README.md` 与章鱼OS技能锚点。
- `Octopus_OS/AGENTS.md` 还必须承载该仓库自己的 GitHub hook 硬合同：仅当本仓库在 Non-read-only 回合实际发生写入时才触发。
- 该合同必须要求在同一回合结束前完成 GitHub 收尾，不得延后到后续回合补留痕。
- 该合同必须给出精确命令：
  - `python3 /home/jasontan656/.codex/skills/Meta-github-operation/scripts/Cli_Toolbox.py commit-and-push --repo Octopus_OS --message "<commit message>" --use-latest-claims --auto-scope --allow-empty`
- 若命令失败、被跳过、或与实际写入不一致，必须声明 `violation` 并先修复后收尾。
- `Octopus_OS/AGENTS.md` 还必须承载该仓库自己的宪法技能与静态 lint 责任：只对本仓库真实被改的 concrete target root 运行 `Constitution-knowledge-base` static lint。
- `Octopus_OS/<Container_Name>/AGENTS.md` 是容器根的开发回写合同入口，必须指向同级 `README.md`。
- `Octopus_OS/User_UI/AGENTS.md` 与 `Octopus_OS/Admin_UI/AGENTS.md` 还必须提醒：前端开发、页面联调、浏览器测试、交互验证时加载 `Meta-browser-operation`。
- `Octopus_OS/Mother_Doc/docs/**/AGENTS.md` 是文档树递归索引入口，必须指向同级 `README.md` 与同级实体文档。
- `AGENTS.md` 管理是 `mother_doc` 阶段下的独立子分支，必须通过 `scan / collect / push` 明确分离。

## Fixed Shape

每个 `AGENTS.md` 必须固定包含：

1. `目标`
2. `同层入口`
3. `下一层入口`
4. `选择规则`
5. `更新边界`
6. `索引契约`
7. `递归动作`

## Managed Branch

- 总入口：[agents_branch/00_BRANCH_INDEX.md](agents_branch/00_BRANCH_INDEX.md)
- 统一模板根：`assets/mother_doc_agents/templates/`
- 统一索引：`assets/mother_doc_agents/index.md`
- `scan`：扫描 3 类路径中的当前 `AGENTS.md + README.md` 现状，不回写普通正文。
- `collect`：把产品侧 `AGENTS.md + README.md` 反向采集回技能内 `assets/mother_doc_agents/collected_tree/`。
- `push`：把技能侧当前模板反推回 3 类路径，随后自动重扫并回收。
