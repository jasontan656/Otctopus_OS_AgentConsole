# Push Rules

- 只回推根层 `Octopus_OS/AGENTS.md`。
- push 时必须删除所有非法额外 `Octopus_OS/**/AGENTS.md`。
- push 后必须立刻重扫并回收，保证 skill 侧与产品侧一致。
- push 仍属于 `mother_doc` 阶段，不得写日志与 Git 留痕。
