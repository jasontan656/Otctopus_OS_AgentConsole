---
doc_id: skillsmanager_tooling_checkup.path.remediation.validation
doc_type: topic_atom
topic: Validation for tooling remediation
---

# 整改校验

## 当前动作如何判定完成
- 目标技能现有测试 / lint 已完成。
- 若涉及 Python，已补充对应 constitution 的 lint。
- 若目标技能属于已安装 skill，镜像同步链路已在后续动作中继续完成。

## 通过标准
- 行为没有退化。
- 问题本身已经闭合，而不是被新兼容层掩盖。
