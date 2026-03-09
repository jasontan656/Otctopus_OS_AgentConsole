# AGENTS

## 1. 目标
- 当前层作用：`Octopus_OS` 总容器根，是 AI 进入项目开发与维护链路的第一站。
- 项目相关介绍只看 `README.md`。
- 开发、文档、evidence、工具和 graph 的维护方式都从章鱼OS全栈技能锚点进入。

## 2. 同层入口
- `README.md`: 项目相关介绍与当前顶层容器布局说明。

## 3. 章鱼OS技能锚点
- `/home/jasontan656/.codex/skills/2-Octupos-FullStack/SKILL.md`: 技能总门面。
- `/home/jasontan656/.codex/skills/2-Octupos-FullStack/references/skill_native/01_FACADE_LOAD_MAP.md`: 技能总入口图与规则分流。
- `/home/jasontan656/.codex/skills/2-Octupos-FullStack/references/stages/MOTHER_DOC_STAGE.md`: `mother_doc` 阶段入口。
- `/home/jasontan656/.codex/skills/2-Octupos-FullStack/references/stages/IMPLEMENTATION_STAGE.md`: `implementation` 阶段入口。
- `/home/jasontan656/.codex/skills/2-Octupos-FullStack/references/stages/EVIDENCE_STAGE.md`: `evidence` 阶段入口。
- `/home/jasontan656/.codex/skills/2-Octupos-FullStack/scripts/Cli_Toolbox.py`: 统一 CLI 工具入口。

## 4. 项目资产去处
- `Octopus_OS/<Container_Name>/`: 各独立容器的代码与运行时根路径。
- `Octopus_OS/Mother_Doc/docs/`: 所有容器的 authored-doc 文档树。
- `Octopus_OS/Mother_Doc/graph/`: OS_graph 资产与 evidence graph runtime 根。

## 5. 选择规则
- 先读当前层 `README.md` 获取项目介绍。
- 再读章鱼OS全栈技能锚点，确认当前任务属于 `mother_doc`、`implementation` 还是 `evidence`。
- 确认阶段后，再选择进入对应容器路径或 `Mother_Doc` 文档树，不跨到无关容器。

## 6. 索引契约
- 当前根层 `AGENTS.md` 属于 `octopus_os_root` 分支。
- 它必须固定指向 `README.md` 和章鱼OS全栈技能锚点。
- 它不负责展开具体文档正文或具体实现细节。

## 7. 递归动作
- 进入 `Account_Service/`：account and profile domain container。
- 进入 `Admin_UI/`：admin-facing client container and future operator surface。
- 进入 `AI_Service/`：AI domain container。
- 进入 `API_Gateway/`：unified ingress container for routing, auth forwarding, and traffic control。
- 进入 `File_Service/`：file domain container。
- 进入 `Identity_Service/`：identity and auth domain container。
- 进入 `Mother_Doc/`：authoritative authored-document and OS_graph container。
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
