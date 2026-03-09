# AGENTS

## 1. 目标
- 当前层作用：`AI_Service` 容器根入口。
- 先读 `README.md` 获取当前容器用途，再决定进入代码、文档或其他子路径。

## 2. 同层入口
- `README.md`: 当前容器用途说明。
- `../Mother_Doc/docs/AI_Service/README.md`: 当前容器对应的 authored-doc 根说明。

## 3. 下一层入口
- `../Mother_Doc/docs/AI_Service/`: 当前容器对应的文档树入口。

## 4. 选择规则
- 先读当前层 `README.md`。
- 若任务是文档设计、需求回写或结构浏览，优先转入对应的 `Mother_Doc/docs` 路径。
- 若任务是容器根层结构或后续代码落点，再留在当前容器路径继续处理。

## 5. 更新边界
- 当前层只负责容器根入口，不替代容器内部正文。
- 文档正文仍由 `Mother_Doc/docs` 承载，graph 资产由 `Mother_Doc/graph` 承载。

## 6. 索引契约
- 当前文件属于 `container_roots` 分支。
- 每个顶层容器都必须有自己的容器根 `AGENTS.md` 模板与推送路径。

## 7. 递归动作
- 命中文档域时，进入对应 `Mother_Doc/docs` 容器路径。
- 命中当前容器实际子路径时，继续进入对应子目录处理。
