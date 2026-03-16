# Turn End Writeback

- `turn end` 必须检查是否出现 durable signal。
- 只有稳定信号才允许写回用户层或任务层 snapshot。
- 写回顺序固定：
  - 更新 JSON snapshot
  - 同步 Markdown mirror
  - 追加 turn delta
  - 重编译 active memory
- 若没有稳定信号，可以跳过写回，但不能跳过检查。
