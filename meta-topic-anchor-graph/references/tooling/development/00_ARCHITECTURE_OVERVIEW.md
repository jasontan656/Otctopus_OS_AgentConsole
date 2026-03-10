# 文档架构总览

适用技能：`meta-topic-anchor-graph`

## v1 结构
- `SKILL.md`：门面与触发描述。
- `references/topic-anchor-graph-contract.md`：真正的方法论合同。
- `assets/templates/*.md`：写作模板。
- `references/tooling/*`：为未来 CLI 预留的扩展位。

## 设计主张
- 把“如何拆文档”沉到合同里，不把细则堆进门面。
- 把“怎么写节点”沉到模板里，不把示例散落在正文。
- 如果未来增加脚本，只能作为合同落地器，不能反过来篡改结构原则。
