# Background Subagent Mainline

- background terminal 固定使用 `tmux`
- SUBAGENT 固定模型：`gpt-5.4`
- reasoning effort 固定：`high`
- 主 AGENT 必须持续轮询输出；只有连续 `10` 分钟无新输出时才允许判死
- SUBAGENT 固定执行 `$Functional-Analysis-Runtask analysis_loop` 九阶段
- `design` 固定显式使用 `$Meta-keyword-first-edit`
