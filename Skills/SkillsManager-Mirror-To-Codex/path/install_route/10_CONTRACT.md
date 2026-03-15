---
doc_id: skillsmanager_mirror_to_codex.path.install_route.contract
doc_type: contract_doc
topic: Install route contract
reading_chain:
- key: tools
  target: 15_TOOLS.md
  hop: next
  reason: After the contract, read the route commands and expected payload.
---

# Install 路由合同

## 当前动作的目标
- 当目标技能不在 codex 安装目录中时，返回受管安装路由。

## 当前动作必须满足的约束
- `install` 只允许与 `scope=skill` 配合。
- 目标目录缺失时，不允许直接用 `rsync` 伪造首次安装。
- 当前线路只返回 `route_required`，真正安装由外部技能继续完成。

## 下一跳列表
- [tools]：`15_TOOLS.md`
