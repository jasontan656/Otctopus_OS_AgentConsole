---
doc_id: skillsmanager_tooling_checkup.path.techstack_baseline.execution
doc_type: topic_atom
topic: Execution for techstack baseline checking
reading_chain:
- key: validation
  target: 30_VALIDATION.md
  hop: next
  reason: baseline execution ends in validation.
---

# 依赖基线检查实施

## 当前动作怎么做
1. 锁定目标技能路径与具体 tooling 文件范围。
2. 把目标实现映射到它实际提供的能力，而不是它的命名。
3. 对照 repo 既定依赖栈，判断哪些能力已经被现有依赖直接覆盖。
4. 区分通用轮子与目标技能自己的域内语义，只标记真正可删或可缩小的部分。
5. 明确结论属于：
   - 仅怀疑，证据不足
   - 语义重叠，可整改
   - 仍承载目标技能语义，不应替换

## 当前动作不能做什么
- 不能把模式相似直接升级成整改结论。
- 不能把目标技能的业务语义误判成通用依赖能力。

## 下一跳列表
- [validation]：`30_VALIDATION.md`
