# CONSTITUTION_CONTENT_CHANGE_STANDARD_v1

## 1. 目的
- 统一宪法库新增内容的写法、质量门槛和挂钩方式。
- 禁止“模板化空话”进入宪法条款，保证每条都可执行、可审计、可验收。

## 2. 适用范围
1. 新增任意 `anchor_docs` 文档。
2. 修改任意既有条款的语义、约束、命令、验收标准。
3. 新增或变更 `SKILL.md` 入口索引与图谱挂钩关系。

## 3. 强制写法（命令式）
1. 每条必须写清楚：在项目中起什么作用。
2. 每条必须给出：`Do`、`Don't`、`Why`。
3. 每条必须给出：最小可执行命令（用于自检或反查）。
4. 每条必须给出：最小验收（可判定通过/失败）。
5. 文本必须是执行指令，不写政策口号，不写空泛愿景。

## 4. 强制结构
每个条款文档至少包含以下段落：
1. `anchor_id/category/mol_resident_source/graph_hook`
2. `## 在项目中起什么作用`
3. `## 必须做（Do）`
4. `## 不要做（Don't）`
5. `## 为什么（Why）`
6. `## 实操命令`
7. `## 最小验收`

## 5. 挂钩规则
1. `anchor_id` 必须在 `references/anchor_docs/ANCHOR_DOC_REGISTRY.yaml` 可反查。
2. `graph_hook.graph_node` 必须与 `MOL_TECH_STACK_KEYWORD_ANCHOR_GRAPH_v1.md` 节点一致。
3. 任何新增条款若无法挂钩图谱，视为未完成，不得合入。

## 6. 质量门禁
1. 缺失 `Do/Don't/Why` 任一项，阻断。
2. 没有可执行命令，阻断。
3. 最小验收不可判定（模糊描述），阻断。
4. 与既有条款冲突但未给出裁决顺序，阻断。

## 7. 变更流程
1. 先定义条款目标与影响范围。
2. 再写条款正文并挂钩图谱与注册表。
3. 执行反查命令确认可检索。
4. 通过门禁后再更新 `SKILL.md` 入口。

## 8. 反查命令
```bash
rg -n "CONSTITUTION_CONTENT_CHANGE_STANDARD_v1" SKILL.md
rg -n "anchor_id:" references/anchor_docs
rg -n "graph_node:" references/anchor_docs/ANCHOR_DOC_REGISTRY.yaml
```

## 9. 禁止事项
1. 禁止脚本批量生成未经人工审校的条款文本。
2. 禁止只改标题不改执行语义。
3. 禁止新增业务向条款（会计、税务、法务流程等）进入本技能。
