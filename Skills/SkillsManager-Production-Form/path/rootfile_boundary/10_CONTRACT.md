---
doc_id: skillsmanager_production_form.path.rootfile_boundary.contract
doc_type: contract_doc
topic: Rootfile boundary contract
reading_chain:
- key: tools
  target: 15_TOOLS.md
  hop: next
  reason: After the contract, read the route commands and execution rule.
---

# RootFile 边界合同

## 当前动作的目标
- 当 console 产品形态判断触及外部 root file 时，明确切换到受管 rootfile 流程。

## 当前动作必须满足的约束
- 本技能可以声明 root file 为什么重要，但不得直接维护外部受管文件正文。
- 外部 root file 正文必须通过 `$Meta-RootFile-Manager` 的 collect / push / target-contract 流程维护。

## 下一跳列表
- [tools]：`15_TOOLS.md`
