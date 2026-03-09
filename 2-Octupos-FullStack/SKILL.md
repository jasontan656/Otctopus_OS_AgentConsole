---
name: "2-Octupos-FullStack"
description: "未来项目 admin panel 内置的运营AI“章鱼”，负责 mother_doc、implementation 与 evidence 三阶段。"
---

# 2-Octupos-FullStack

## 1. 目标
- 本技能用于 `Octopus_OS` 的全栈文档驱动开发与落盘维护。
- 本技能是 `Octopus_OS` 的开发操作手册门面，运行对象是内置运营AI“章鱼”。
- 阶段固定为：`mother_doc`、`implementation`、`evidence`。
- 长规则不在门面展开；门面只负责给出入口与最小说明。

## 2. 可用工具
- 统一入口：[Cli_Toolbox.py](scripts/Cli_Toolbox.py)
- 工具分阶段使用，不在门面展开命令清单。
- 具体命令、作用和调用方式统一从 [Facade Load Map](references/skill_native/01_FACADE_LOAD_MAP.md) 进入。

## 3. 工作流约束
- 统一工作流入口：[Facade Load Map](references/skill_native/01_FACADE_LOAD_MAP.md)
- 顶层常驻文档、阶段进入顺序、阶段切换方式都从该入口继续读取。
- `mother_doc` 进入后先读子分支入口，再选择 `direct_writeback`、`question_backfill` 或 `AGENTS/README manager`。
- `mother_doc`、`implementation`、`evidence` 的细则不在门面展开。

## 4. 规则约束
- 顶层规则入口：[FULLSTACK_SKILL_HARD_RULES.md](rules/FULLSTACK_SKILL_HARD_RULES.md)
- 运行合同入口：[SKILL_RUNTIME_CONTRACT.md](references/runtime/SKILL_RUNTIME_CONTRACT.md)
- 门面不复述规则正文；需要细则时先读 [Facade Load Map](references/skill_native/01_FACADE_LOAD_MAP.md) 再进入具体规则文件。

## 5. 方法论约束
- 方法论入口：[Facade Load Map](references/skill_native/01_FACADE_LOAD_MAP.md)
- 具体方法论分别落在 `mother_doc`、`implementation`、`evidence` 的阶段文档与对齐文档中。
- 门面只声明一件事：文档即代码，规则分层读取，禁止在门面混写。

## 6. 内联导航索引
- [总入口图](references/skill_native/01_FACADE_LOAD_MAP.md)
- [skill native 索引](references/skill_native/00_SKILL_NATIVE_INDEX.md)
- [顶层规则](rules/FULLSTACK_SKILL_HARD_RULES.md)
- [运行合同](references/runtime/SKILL_RUNTIME_CONTRACT.md)
- [authored domains 索引](references/authored_domains/00_DOMAIN_INDEX.md)
- [工具入口](scripts/Cli_Toolbox.py)

## 7. 架构契约
- 架构契约入口：[Facade Load Map](references/skill_native/01_FACADE_LOAD_MAP.md)
- 运行边界入口：[SKILL_RUNTIME_CONTRACT.md](references/runtime/SKILL_RUNTIME_CONTRACT.md)
- 目录细节不在门面展开；需要结构时从上述入口继续进入具体目录与规则文件。
