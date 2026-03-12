# Project Baseline Routing Rules

适用阶段：`mother_doc`

## Purpose

- 在进入任何具体容器前，先固定读取项目统一目标基线。
- 把当前需求先放到项目级总目标、当前试点和动态增长规则里判断，再进入具体容器。

## Impact Selection Rule

- 起点固定为 `default_all_relevant`。
- 第一轮先把所有容器、共享合同、graph/evidence 消费面都视为潜在相关。
- 第二轮再按 `highest_probability_unrelated -> next_highest_probability_unrelated` 做减法排除。
- 没有可读语义依据，不得排除容器或域。

## Writeback Rule

- 项目级总目标、当前开发说明、当前范围和当前排除结论优先回填到 `Octopus_OS/Mother_Doc/docs/Mother_Doc/project_baseline/`。
- 进入具体容器后，再把明确内容写回该容器的 `overview / features / shared / common`。
- 如果当前需求的影响面尚未收口，先在项目级基线写出当前判断，再通过 `question_backfill` 继续追问。
