# Self Governance Mainline

- 正式主链：`factory_intake -> intent_enhance -> background_subagent -> artifact_refresh -> validation_closeout`
- `intent_enhance` 固定调用 `$Meta-Enhance-Prompt`
- `background_subagent` 固定通过 `tmux` 启动并轮询 `gpt-5.4 / reasoning=high`
- subagent 固定消费 `$Functional-Analysis-Runtask analysis_loop`
- 主 AGENT 固定负责回读结果、手工终止单进程与刷新实验产物
