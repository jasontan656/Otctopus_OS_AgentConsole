---
doc_id: skillsmanager_production_form.path.working_contract.contract
doc_type: contract_doc
topic: Working contract contract
reading_chain:
- key: tools
  target: 15_TOOLS.md
  hop: next
  reason: After the contract, read the command surface.
---

# 工作合同合同

## 当前动作的目标
- 稳定表达当前 console 产品形态、运行根、日志根和产品化硬边界。

## 当前动作必须满足的约束
- `Skills/` 目录是当前 console 产品化源面。
- codex 安装目录只作为部署面，不作为产品化直接编辑面。
- active 连续性日志只能写入受管 runtime root。
- 任何 root file 正文修改都必须路由到 `$Meta-RootFile-Manager`。

## 下一跳列表
- [tools]：`15_TOOLS.md`
