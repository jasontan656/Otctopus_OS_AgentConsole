---
doc_id: skillsmanager_production_form.path.rootfile_boundary.execution
doc_type: execution_doc
topic: Rootfile boundary execution
reading_chain:
- key: validation
  target: 30_VALIDATION.md
  hop: next
  reason: Validate that rootfile work is routed away from this skill.
---

# RootFile 边界实施

## 执行顺序
1. 先判断本回合是否触及 `AGENTS.md`、`README.md`、`LICENSE` 等 root file 受管文件。
2. 若未触及，则继续当前技能的产品形态治理。
3. 若已触及，则在本技能中只保留边界说明。
4. 切换到 `$Meta-RootFile-Manager` 继续受管正文维护。

## 下一跳列表
- [validation]：`30_VALIDATION.md`
