# Skills Runtime Entry

- 这个文件是 `Octopus OS` 工作区中 `Skills/` 容器的本地运行入口。
- 它用于提醒后续 AI：`Skills/` 是产品仓中唯一的技能容器，真实可同步技能根都在这里。
- 它属于工作区生态的一部分，应随产品安装一起进入工作区镜像。
- 它不是 codex 安装目录的一部分，不能同步到 `~/.codex/skills/AGENTS.md`。
- `~/.codex/skills` 只允许放置真实技能根与 `.system/`，不允许保留误同步的根级 `AGENTS.md`。
