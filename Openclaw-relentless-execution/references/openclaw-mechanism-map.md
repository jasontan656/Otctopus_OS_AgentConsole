# OpenClaw Mechanism Map (for local replication)

This file maps key OpenClaw behavior patterns to this skill.

## 1) System prompt turns request into execution protocol
- Skills mandatory section and tooling policy:
  - `.Learning/OpenClaw/src/agents/system-prompt.ts:29`
  - `.Learning/OpenClaw/src/agents/system-prompt.ts:384`

## 2) Lifecycle hooks enforce pre/post run logic
- Hook definitions:
  - `.Learning/OpenClaw/src/plugins/hooks.ts:179`
  - `.Learning/OpenClaw/src/plugins/hooks.ts:202`
- Hook use in attempt:
  - `.Learning/OpenClaw/src/agents/pi-embedded-runner/run/attempt.ts:731`
  - `.Learning/OpenClaw/src/agents/pi-embedded-runner/run/attempt.ts:859`

## 3) Run loop uses retry/recovery, not single shot
- Main while loop:
  - `.Learning/OpenClaw/src/agents/pi-embedded-runner/run.ts:392`
- Context-overflow compaction + retry:
  - `.Learning/OpenClaw/src/agents/pi-embedded-runner/run.ts:502`
  - `.Learning/OpenClaw/src/agents/pi-embedded-runner/run.ts:533`
- Oversized tool-result truncation + retry:
  - `.Learning/OpenClaw/src/agents/pi-embedded-runner/run.ts:540`
  - `.Learning/OpenClaw/src/agents/pi-embedded-runner/run.ts:566`

## 4) Dependency installation is explicit, scriptable, and validated
- Install command building for brew/node/go/uv:
  - `.Learning/OpenClaw/src/agents/skills-install.ts:160`
- Install flow + execution:
  - `.Learning/OpenClaw/src/agents/skills-install.ts:411`
  - `.Learning/OpenClaw/src/agents/skills-install.ts:550`

## 5) Exec fallback resilience
- spawn fallback and PTY fallback:
  - `.Learning/OpenClaw/src/agents/bash-tools.exec.ts:462`
  - `.Learning/OpenClaw/src/agents/bash-tools.exec.ts:516`

## Localized replication in this skill
- Objective contract + done criteria + explicit constraints
- Mandatory lifecycle hooks via `before-hook` / `after-hook` / `flush-hook`
- Attempt loop with deterministic failure classification
- Dependency self-healing execution with install-plan fallback
- Guardrails to prevent infinite loops:
  - max attempts
  - max runtime
  - max stagnation
  - repeat-failure cap
  - per-kind retry budgets
- Stop only on done or hard blocker (or guardrail block requiring user decision)
