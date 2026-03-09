# AGENTS

## 1. 目标
- 当前层作用：`Octopus_OS` 总容器根，是 AI 进入项目开发与维护链路的第一站。
- 项目相关介绍看同层 `README.md`；本文件不展开项目正文。
- 本文件只负责把章鱼OS全栈技能锚点、代码去处、文档去处、graph 去处和工具入口说清楚。

## 2. 同层入口
- `README.md`: 当前总容器层的浓缩总结说明；可选阅读，但如果本层容器布局或维护入口发生变化，必须同步维护对应章节总结。

## 3. 章鱼OS技能锚点
- `/home/jasontan656/.codex/skills/2-Octupos-FullStack/SKILL.md`: 技能总门面。
- `/home/jasontan656/.codex/skills/2-Octupos-FullStack/references/skill_native/01_FACADE_LOAD_MAP.md`: 技能总入口图与规则分流。
- `/home/jasontan656/.codex/skills/2-Octupos-FullStack/references/skill_native/10_PROJECT_BASELINE_INDEX.md`: 项目统一目标基线入口。
- `/home/jasontan656/.codex/skills/2-Octupos-FullStack/references/stages/MOTHER_DOC_STAGE.md`: `mother_doc` 阶段入口。
- `/home/jasontan656/.codex/skills/2-Octupos-FullStack/references/stages/IMPLEMENTATION_STAGE.md`: `implementation` 阶段入口。
- `/home/jasontan656/.codex/skills/2-Octupos-FullStack/references/stages/EVIDENCE_STAGE.md`: `evidence` 阶段入口。
- `/home/jasontan656/.codex/skills/2-Octupos-FullStack/scripts/Cli_Toolbox.py`: 统一 CLI 工具入口。

## 4. 项目资产去处
- `Octopus_OS/<Container_Name>/`: 各独立容器的代码与运行时根路径。
- `Octopus_OS/Mother_Doc/docs/`: 所有容器的 authored-doc 文档树。
- `Octopus_OS/Mother_Doc/docs/Mother_Doc/project_baseline/`: 项目统一目标基线与当前开发说明。
- `Octopus_OS/Mother_Doc/graph/`: OS_graph 资产与 evidence graph runtime 根。

## 5. 选择规则
- 先看当前任务是否只需要技能锚点即可判断；若不足，再可选读取同层 `README.md`。
- 再读章鱼OS全栈技能锚点与项目统一目标基线，确认当前任务属于 `mother_doc`、`implementation` 还是 `evidence`。
- 确认阶段后，再选择进入对应容器路径或 `Mother_Doc` 文档树，不跨到无关容器。
- 如果本仓库在写入回合发生文件变动，则必须进行 GitHub 留痕；commit message 必须依据本轮实际变动内容编写。
- 本仓库承担宪法技能与静态 lint 收口责任；写入本仓库时，必须对实际被修改的 concrete target root 运行 `Constitution-knowledge-base` static lint。
- 禁止把 `/home/jasontan656/AI_Projects` 当作 lint 目标；若出现非零退出或 `status=fail`，必须声明 `violation` 并修复后重跑。

## 6. 索引契约
- 当前根层 `AGENTS.md` 属于 `octopus_os_root` 分支。
- 它必须固定指向 `README.md` 和章鱼OS全栈技能锚点。
- 它不负责展开具体文档正文或具体实现细节。
- 当本层内容发生变更时，必须同时检查同层 `README.md` 是否需要更新总结。

## 7. 递归动作
- 进入 `Account_Service/`：account and profile domain container。
- 进入 `Admin_UI/`：admin-facing client container and future operator surface。
- 进入 `AI_Service/`：AI domain container。
- 进入 `API_Gateway/`：unified ingress container for routing, auth forwarding, and traffic control。
- 进入 `File_Service/`：file domain container。
- 进入 `Identity_Service/`：identity and auth domain container。
- 进入 `Mother_Doc/`：authoritative authored-document, project-baseline, and OS_graph container。
- 进入 `MQ_Broker/`：message broker container。
- 进入 `Notification_Service/`：notification domain container。
- 进入 `Object_Storage/`：object storage container。
- 进入 `Order_Service/`：order domain container。
- 进入 `Payment_Service/`：payment domain container。
- 进入 `Postgres_DB/`：relational database container。
- 进入 `Redis_Cache/`：cache container。
- 进入 `User_UI/`：user-facing client container。
- 若目标属于文档树，则转入 `Mother_Doc/docs/**` 的递归索引链。
- 若目标属于 graph 或 evidence，则转入 `Mother_Doc/graph/` 与技能 `evidence` 锚点继续处理。
