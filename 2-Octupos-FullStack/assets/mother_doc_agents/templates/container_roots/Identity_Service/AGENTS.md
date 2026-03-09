# AGENTS

## 1. 目标
- 当前层作用：`Identity_Service` 容器根的开发回写合同入口。
- 本文件提醒模型遵守当前容器的抽象层通用规则、文档回写入口和 evidence 闭环要求。

## 2. 同层入口
- `README.md`: 当前容器项目的 AI-facing summary；可选阅读，但如果本容器发生了代码、文档或 evidence 相关落盘，必须考虑维护本文件。
- `../Mother_Doc/docs/Identity_Service/README.md`: 当前容器对应的 authored-doc 根说明。

## 3. 下一层入口
- `../Mother_Doc/docs/Identity_Service/`: 当前容器对应的文档树入口。

## 4. 选择规则
- 如果当前任务需要确认容器用途、维护范围或当前阶段总结，可选读取同层 `README.md`。
- 如果当前任务是新需求的项目级目标、作用面或当前试点范围判定，`Mother_Doc` 容器先进入 `docs/Mother_Doc/project_baseline/`。
- 若任务是文档设计、需求回写或结构浏览，优先转入对应的 `Mother_Doc/docs` 路径。
- 若任务是代码落盘或运行时处理，则留在当前容器路径，并同时回看对应的 `Mother_Doc/docs/<Container_Name>/common/`。

## 5. 更新边界
- 当前层只负责容器根入口与开发回写提醒，不替代容器内部正文。
- 文档正文仍由 `Mother_Doc/docs` 承载，graph 资产由 `Mother_Doc/graph` 承载。
- 若当前容器内容被修改，必须检查同层 `README.md` 是否需要更新总结。

## 6. 索引契约
- 当前文件属于 `container_roots` 分支。
- 每个顶层容器都必须有自己的容器根 `AGENTS.md` 与 `README.md` 模板与推送路径。

## 7. 递归动作
- 命中文档域时，进入对应 `Mother_Doc/docs` 容器路径。
- 命中当前容器实际子路径时，继续进入对应子目录处理。
