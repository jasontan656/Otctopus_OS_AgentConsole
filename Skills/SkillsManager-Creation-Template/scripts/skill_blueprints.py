from __future__ import annotations

import json
from textwrap import dedent

GUIDE_ONLY_MODE = "guide_only"
GUIDE_WITH_TOOL_MODE = "guide_with_tool"
EXECUTABLE_WORKFLOW_MODE = "executable_workflow_skill"
SKILL_MODE_CHOICES = (
    GUIDE_ONLY_MODE,
    GUIDE_WITH_TOOL_MODE,
    EXECUTABLE_WORKFLOW_MODE,
)


def title_from_slug(slug: str) -> str:
    return " ".join(part.capitalize() for part in slug.replace("_", "-").split("-"))


def render_numbered(lines: list[str]) -> str:
    return "\n".join(f"{index}. {line}" for index, line in enumerate(lines, start=1))


def render_bullets(lines: list[str]) -> str:
    return "\n".join(f"- {line}" for line in lines)


def render_skill_md(skill_name: str, description: str, skill_mode: str) -> str:
    if skill_mode == GUIDE_ONLY_MODE:
        structure_tree = [
            "<skill-name>/",
            "├── SKILL.md",
            "└── agents/",
        ]
        frontmatter = [
            "---",
            f"name: {skill_name}",
            f"description: {description}",
            f"skill_mode: {skill_mode}",
            "metadata:",
            "  doc_structure:",
            f"    doc_id: {skill_name}.entry.facade",
            "    doc_type: skill_facade",
            f"    topic: Self-contained facade for {skill_name}",
            "---",
            "",
        ]
        lines = [
            f"# {skill_name}",
            "",
            "## 1. 模型立刻需要知道的事情",
            "### 1. 总览",
            f"- 本技能采用 `{skill_mode}` 形态。",
            "- 本文件既是门面，也是完整技能正文的唯一承载面。",
            "- 根目录只保留 `SKILL.md / agents`。",
            "",
            "### 2. 技能约束",
            "- 不生成 `path/`。",
            "- 不生成 `scripts/`。",
            "- 不把当前技能继续拆成外跳链路；完整说明直接保留在 `SKILL.md`。",
            "",
            "### 3. 顶层常驻合同",
            "- `SKILL.md` 本身就是唯一入口与唯一正文。",
            "",
            "## 2. 技能正文",
            "- [在此直接填写目标技能的完整正文，不要假设存在 `path/` 或 `scripts/`。]",
            "",
            "## 3. 目录结构图",
            "```text",
            *structure_tree,
            "```",
            "",
        ]
        return "\n".join(frontmatter + lines)

    if skill_mode == GUIDE_WITH_TOOL_MODE:
        mode_overview = [
            f"- 本技能采用 `{skill_mode}` 形态。",
            "- 本文件只做门面入口，不承载深层正文。",
            "- 默认提供一个主入口；若扩展多个入口，每个入口内部必须单线到底。",
            "- 本形态的 `scripts/` 承载当前技能自己的 tool/lint 能力面，不要求两者都存在。",
            "- 根目录组织固定为 `SKILL.md / path / agents / scripts`。",
        ]
        mode_constraints = [
            "- `SKILL.md` 只保留：`模型立刻需要知道的事情`、`唯一入口`、`目录结构图`。",
            "- `SKILL.md` 只能暴露入口层，不回填 workflow 正文。",
            "- 每个入口进入后都必须沿 `contract -> tools -> execution -> validation` 单线闭环到底。",
            "- 允许多个平行入口，但不允许某个入口内部再次分叉。",
            "- 命令脚本本体统一放在 `scripts/`；tool/lint 说明写在对应入口的 `tools` 节点里。",
        ]
    else:
        mode_overview = [
            f"- 本技能采用 `{skill_mode}` 形态。",
            "- 本文件只做门面入口，不承载深层正文。",
            "- 入口层可以保持简洁，但某个入口进入后允许继续承载复合 workflow。",
            "- 根目录组织固定为 `SKILL.md / path / agents / scripts`。",
        ]
        mode_constraints = [
            "- `SKILL.md` 只保留：`模型立刻需要知道的事情`、`唯一入口`、`目录结构图`。",
            "- `SKILL.md` 只能暴露入口层，不回填复合 workflow 正文。",
            "- 入口进入后允许先经过 `contract -> tools -> workflow_index`，再下沉到复合步骤。",
            "- 复合步骤自身继续承载自己的 `contract -> tools -> execution -> validation`。",
            "- 命令脚本本体统一放在 `scripts/`；命令说明写在入口或步骤自己的 `tools` 节点里。",
        ]

    structure_tree = [
        "<skill-name>/",
        "├── SKILL.md",
        "├── agents/",
        "├── path/",
        "└── scripts/",
    ]
    frontmatter = [
        "---",
        f"name: {skill_name}",
        f"description: {description}",
        f"skill_mode: {skill_mode}",
        "metadata:",
        "  doc_structure:",
        f"    doc_id: {skill_name}.entry.facade",
        "    doc_type: skill_facade",
        f"    topic: Entry facade for {skill_name}",
        "    anchors:",
        "    - target: path/00_SKILL_ENTRY.md",
        "      relation: routes_to",
        "      direction: downstream",
        "      reason: The facade exposes only the entry layer.",
        "---",
        "",
    ]
    lines = [
        f"# {skill_name}",
        "",
        "## 1. 模型立刻需要知道的事情",
        "### 1. 总览",
        *mode_overview,
        "",
        "### 2. 技能约束",
        *mode_constraints,
        "",
        "### 3. 顶层常驻合同",
        "- `./scripts/Cli_Toolbox.py runtime-contract --json`",
        "- `path/00_SKILL_ENTRY.md`",
        "",
        "## 2. 唯一入口",
        "- [技能主入口]：`path/00_SKILL_ENTRY.md`",
        "  - 作用：先进入入口层，再按当前模式的协议继续向下读取。",
        "",
        "## 3. 目录结构图",
        "```text",
        *structure_tree,
        "```",
        "",
    ]
    return "\n".join(frontmatter + lines)


def render_openai_yaml(skill_name: str, skill_mode: str) -> str:
    display_name = title_from_slug(skill_name)
    if skill_mode == GUIDE_ONLY_MODE:
        default_prompt = f"请直接读取 {skill_name} 的 SKILL.md 完成任务，不要假设存在 path/ 或 scripts/。"
    elif skill_mode == GUIDE_WITH_TOOL_MODE:
        default_prompt = (
            f"请围绕 {skill_name} 的真实业务目标执行任务；先读取 SKILL.md 与 path/00_SKILL_ENTRY.md，"
            "进入某个入口后沿单线 workflow 读到底，不要在入口内部再次分叉。"
        )
    else:
        default_prompt = (
            f"请围绕 {skill_name} 的真实业务目标执行任务；先读取 SKILL.md 与 path/00_SKILL_ENTRY.md，"
            "进入入口后按复合 workflow 逐层下沉到步骤级文档。"
        )
    return dedent(
        f"""\
        version: 1
        agent:
          name: {display_name}
          description: {skill_name} skill agent for {skill_mode}
          default_prompt: |
            {default_prompt}
        """
    )


def runtime_contract_payload(skill_name: str, skill_mode: str) -> dict[str, object]:
    if skill_mode == GUIDE_ONLY_MODE:
        return {
            "skill_name": skill_name,
            "skill_mode": skill_mode,
            "root_shape": ["SKILL.md", "agents"],
            "entry_doc": "SKILL.md",
            "reading_protocol": ["SKILL.md"],
            "layout_rule": "Self-contained skill. No path or scripts are generated.",
        }

    payload: dict[str, object] = {
        "skill_name": skill_name,
        "skill_mode": skill_mode,
        "root_shape": ["SKILL.md", "path", "agents", "scripts"],
        "entry_doc": "path/00_SKILL_ENTRY.md",
        "layout_rule": "Folder layout must mirror reading order.",
    }
    if skill_mode == GUIDE_WITH_TOOL_MODE:
        payload["reading_protocol"] = [
            "SKILL.md",
            "path/00_SKILL_ENTRY.md",
            "entry_doc",
            "contract",
            "tools",
            "execution",
            "validation",
        ]
        payload["workflow_shape"] = {
            "entry_policy": "multiple top-level entries allowed",
            "entry_internal_shape": "linear_only",
            "default_entry_doc": "path/primary_flow/00_PRIMARY_FLOW_ENTRY.md",
        }
        return payload

    payload["reading_protocol"] = [
        "SKILL.md",
        "path/00_SKILL_ENTRY.md",
        "entry_doc",
        "contract",
        "tools",
        "workflow_index",
        "step_entry",
        "step_contract",
        "step_tools",
        "step_execution",
        "step_validation",
        "flow_validation",
    ]
    payload["compound_protocol"] = {
        "entry_policy": "entry may contain nested workflow",
        "default_entry_doc": "path/primary_flow/00_PRIMARY_FLOW_ENTRY.md",
        "workflow_index_doc": "path/primary_flow/20_WORKFLOW_INDEX.md",
        "step_order": ["step_01", "step_02", "step_03"],
    }
    return payload


def render_generated_toolbox_script(skill_name: str, skill_mode: str) -> str:
    payload = json.dumps(runtime_contract_payload(skill_name, skill_mode), ensure_ascii=False, indent=2)
    return "\n".join(
        [
            "#!/usr/bin/env python3",
            "from __future__ import annotations",
            "",
            "import argparse",
            "import json",
            "",
            f"RUNTIME_CONTRACT = {payload}",
            "",
            "",
            "def main() -> int:",
            f'    parser = argparse.ArgumentParser(description="{skill_name} toolbox")',
            '    subparsers = parser.add_subparsers(dest="command", required=True)',
            "",
            '    runtime_contract = subparsers.add_parser("runtime-contract")',
            '    runtime_contract.add_argument("--json", action="store_true")',
            "",
            "    args = parser.parse_args()",
            '    if args.command == "runtime-contract":',
            "        if args.json:",
            "            print(json.dumps(RUNTIME_CONTRACT, ensure_ascii=False, indent=2))",
            "        else:",
            "            for key, value in RUNTIME_CONTRACT.items():",
            '                print(f"{key}: {value}")',
            "        return 0",
            "    return 1",
            "",
            "",
            'if __name__ == "__main__":',
            "    raise SystemExit(main())",
            "",
        ]
    )


def render_generated_test_script(skill_name: str, skill_mode: str) -> str:
    if skill_mode == GUIDE_ONLY_MODE:
        expected_paths = ["SKILL.md", "agents/openai.yaml"]
    elif skill_mode == GUIDE_WITH_TOOL_MODE:
        expected_paths = [
            "SKILL.md",
            "agents/openai.yaml",
            "path/00_SKILL_ENTRY.md",
            "path/primary_flow/00_PRIMARY_FLOW_ENTRY.md",
            "path/primary_flow/10_CONTRACT.md",
            "path/primary_flow/15_TOOLS.md",
            "path/primary_flow/20_EXECUTION.md",
            "path/primary_flow/30_VALIDATION.md",
            "scripts/Cli_Toolbox.py",
            "scripts/test_skill_layout.py",
        ]
    else:
        expected_paths = [
            "SKILL.md",
            "agents/openai.yaml",
            "path/00_SKILL_ENTRY.md",
            "path/primary_flow/00_PRIMARY_FLOW_ENTRY.md",
            "path/primary_flow/10_CONTRACT.md",
            "path/primary_flow/15_TOOLS.md",
            "path/primary_flow/20_WORKFLOW_INDEX.md",
            "path/primary_flow/30_VALIDATION.md",
            "path/primary_flow/steps/step_01/00_STEP_ENTRY.md",
            "path/primary_flow/steps/step_02/30_VALIDATION.md",
            "path/primary_flow/steps/step_03/30_VALIDATION.md",
            "scripts/Cli_Toolbox.py",
            "scripts/test_skill_layout.py",
        ]
    expected_json = json.dumps(expected_paths, ensure_ascii=False, indent=2)
    return dedent(
        f"""\
        from __future__ import annotations

        from pathlib import Path


        SKILL_ROOT = Path(__file__).resolve().parents[1]
        EXPECTED_PATHS = {expected_json}


        def test_layout() -> None:
            for relative_path in EXPECTED_PATHS:
                assert (SKILL_ROOT / relative_path).exists(), relative_path
        """
    )


def render_generated_skill_entry_doc(skill_name: str) -> str:
    return dedent(
        f"""\
        ---
        doc_id: {skill_name}.path.skill_entry
        doc_type: path_doc
        topic: Entry index for {skill_name}
        anchors:
        - target: ../SKILL.md
          relation: implements
          direction: upstream
          reason: The facade points only to this file.
        - target: primary_flow/00_PRIMARY_FLOW_ENTRY.md
          relation: routes_to
          direction: downstream
          reason: The default scaffold starts from the primary entry.
        ---

        # Skill Main Entry

        ## 这个入口是干什么的
        - 这是 `{skill_name}` 的入口层索引。
        - 默认骨架提供一个主入口；如需新增入口，只能在同一层平行扩展。

        ## 下一跳列表
        - [主入口]：`primary_flow/00_PRIMARY_FLOW_ENTRY.md`
        """
    )


def render_linear_entry_doc(skill_name: str) -> str:
    return dedent(
        f"""\
        ---
        doc_id: {skill_name}.path.primary_flow.entry
        doc_type: path_doc
        topic: Primary linear entry for {skill_name}
        anchors:
        - target: ../00_SKILL_ENTRY.md
          relation: implements
          direction: upstream
          reason: The entry index routes here.
        - target: 10_CONTRACT.md
          relation: routes_to
          direction: downstream
          reason: The linear workflow starts from the contract doc.
        ---

        # Primary Flow Entry

        ## 这个入口是干什么的
        - 本入口承载当前默认主 workflow。
        - 进入本入口后，必须沿单线闭环读到底。

        ## 下一跳列表
        - [contract]：`10_CONTRACT.md`
        """
    )


def render_linear_contract_doc(skill_name: str) -> str:
    return dedent(
        f"""\
        ---
        doc_id: {skill_name}.path.primary_flow.contract
        doc_type: topic_atom
        topic: Contract for the primary linear flow of {skill_name}
        anchors:
        - target: 00_PRIMARY_FLOW_ENTRY.md
          relation: implements
          direction: upstream
          reason: The linear entry starts here.
        - target: 15_TOOLS.md
          relation: routes_to
          direction: downstream
          reason: Tool guidance follows the contract.
        ---

        # Primary Flow Contract

        ## 当前动作要完成什么
        - 形成一个入口内单线到底的 workflow。
        - 当前默认骨架包含：`contract -> tools -> execution -> validation`。

        ## 当前动作必须满足什么
        - 允许存在多个平行入口。
        - 任一入口进入后，不允许再次分叉。
        - `tools` 节点承载该入口自己的 tool/lint 说明。
        - 命令说明只写在该入口自己的 `tools` 节点中。

        ## 下一跳列表
        - [tools]：`15_TOOLS.md`
        """
    )


def render_linear_tools_doc(skill_name: str, script_name: str) -> str:
    return dedent(
        f"""\
        ---
        doc_id: {skill_name}.path.primary_flow.tools
        doc_type: topic_atom
        topic: Tool or lint surface for the primary linear flow of {skill_name}
        anchors:
        - target: 10_CONTRACT.md
          relation: implements
          direction: upstream
          reason: Tool guidance follows the contract.
        - target: 20_EXECUTION.md
          relation: routes_to
          direction: downstream
          reason: Execution follows the tool guidance.
        ---

        # Primary Flow Tool/Lint Surface

        ## 当前动作要用什么命令
        - `python3 ./scripts/{script_name} runtime-contract --json`
        - 当前节点承载该入口自己的 tool/lint 说明。
        - [如需新增入口专属命令或 lint，只在当前入口自己的 tools 节点内补充。]

        ## 下一跳列表
        - [execution]：`20_EXECUTION.md`
        """
    )


def render_linear_execution_doc(skill_name: str) -> str:
    steps = [
        "明确当前入口的真实业务主轴与边界。",
        "把命令脚本放入 `scripts/`，把命令说明写入当前入口的 `15_TOOLS.md`。",
        "让当前入口沿单线闭环写到底，不在入口内部新增分叉。",
    ]
    return dedent(
        f"""\
        ---
        doc_id: {skill_name}.path.primary_flow.execution
        doc_type: topic_atom
        topic: Execution for the primary linear flow of {skill_name}
        anchors:
        - target: 15_TOOLS.md
          relation: implements
          direction: upstream
          reason: Execution follows the tool guidance.
        - target: 30_VALIDATION.md
          relation: routes_to
          direction: downstream
          reason: Validation closes the linear flow.
        ---

        # Primary Flow Execution

        ## 当前动作怎么做
        {render_numbered(steps)}

        ## 下一跳列表
        - [validation]：`30_VALIDATION.md`
        """
    )


def render_linear_validation_doc(skill_name: str) -> str:
    checks = [
        "结果目录包含 `SKILL.md / path / agents / scripts`。",
        "入口索引位于 `path/00_SKILL_ENTRY.md`。",
        "默认主入口位于 `path/primary_flow/`，并形成单线闭环。",
        "不存在 `references/`、`assets/`、`tests/`。",
    ]
    return dedent(
        f"""\
        ---
        doc_id: {skill_name}.path.primary_flow.validation
        doc_type: topic_atom
        topic: Validation for the primary linear flow of {skill_name}
        anchors:
        - target: 20_EXECUTION.md
          relation: implements
          direction: upstream
          reason: Validation closes the linear flow.
        ---

        # Primary Flow Validation

        ## 当前动作如何校验
        {render_bullets(checks)}
        """
    )


def render_compound_entry_doc(skill_name: str) -> str:
    return dedent(
        f"""\
        ---
        doc_id: {skill_name}.path.primary_flow.entry
        doc_type: path_doc
        topic: Primary compound entry for {skill_name}
        anchors:
        - target: ../00_SKILL_ENTRY.md
          relation: implements
          direction: upstream
          reason: The entry index routes here.
        - target: 10_CONTRACT.md
          relation: routes_to
          direction: downstream
          reason: The compound workflow starts from the contract doc.
        ---

        # Primary Flow Entry

        ## 这个入口是干什么的
        - 本入口承载当前默认主入口动作。
        - 进入本入口后，需要继续完成一个复合 workflow，而不是一条线直接写到底。

        ## 下一跳列表
        - [contract]：`10_CONTRACT.md`
        """
    )


def render_compound_contract_doc(skill_name: str) -> str:
    return dedent(
        f"""\
        ---
        doc_id: {skill_name}.path.primary_flow.contract
        doc_type: topic_atom
        topic: Contract for the primary compound flow of {skill_name}
        anchors:
        - target: 00_PRIMARY_FLOW_ENTRY.md
          relation: implements
          direction: upstream
          reason: The compound entry starts here.
        - target: 15_TOOLS.md
          relation: routes_to
          direction: downstream
          reason: Tool guidance follows the contract.
        ---

        # Primary Flow Contract

        ## 当前动作要完成什么
        - 形成一个入口内带复合 workflow 的技能骨架。
        - 当前默认骨架包含：`contract -> tools -> workflow_index -> steps -> validation`。

        ## 当前动作必须满足什么
        - 复合 workflow 的步骤必须继续物理下沉到子目录。
        - 每个步骤都应拥有自己的 `contract -> tools -> execution -> validation`。
        - 步骤规则不回填到入口门面。

        ## 下一跳列表
        - [tools]：`15_TOOLS.md`
        """
    )


def render_compound_tools_doc(skill_name: str, script_name: str) -> str:
    return dedent(
        f"""\
        ---
        doc_id: {skill_name}.path.primary_flow.tools
        doc_type: topic_atom
        topic: Tools for the primary compound flow of {skill_name}
        anchors:
        - target: 10_CONTRACT.md
          relation: implements
          direction: upstream
          reason: Tool guidance follows the contract.
        - target: 20_WORKFLOW_INDEX.md
          relation: routes_to
          direction: downstream
          reason: Workflow index follows the tool guidance.
        ---

        # Primary Flow Tools

        ## 当前动作要用什么命令
        - `python3 ./scripts/{script_name} runtime-contract --json`
        - [若某个步骤需要额外命令，应写入该步骤自己的 tools 节点。]

        ## 下一跳列表
        - [workflow_index]：`20_WORKFLOW_INDEX.md`
        """
    )


def render_compound_workflow_index_doc(skill_name: str) -> str:
    return dedent(
        f"""\
        ---
        doc_id: {skill_name}.path.primary_flow.workflow_index
        doc_type: index_doc
        topic: Workflow index for the primary compound flow of {skill_name}
        anchors:
        - target: 15_TOOLS.md
          relation: implements
          direction: upstream
          reason: Workflow index follows the tool guidance.
        - target: steps/step_01/00_STEP_ENTRY.md
          relation: routes_to
          direction: downstream
          reason: Compound execution starts from step_01.
        ---

        # Primary Flow Workflow Index

        ## 当前入口的复合步骤
        1. [step_01]：`steps/step_01/00_STEP_ENTRY.md`
        2. [step_02]：`steps/step_02/00_STEP_ENTRY.md`
        3. [step_03]：`steps/step_03/00_STEP_ENTRY.md`
        """
    )


def render_compound_step_entry_doc(skill_name: str, step_name: str) -> str:
    return dedent(
        f"""\
        ---
        doc_id: {skill_name}.path.primary_flow.steps.{step_name}.entry
        doc_type: path_doc
        topic: Entry doc for {step_name} of {skill_name}
        anchors:
        - target: ../../20_WORKFLOW_INDEX.md
          relation: implements
          direction: upstream
          reason: The workflow index routes here.
        - target: 10_CONTRACT.md
          relation: routes_to
          direction: downstream
          reason: Each step starts from its contract doc.
        ---

        # {step_name} Entry

        ## 这个入口是干什么的
        - 本入口承载 `{step_name}` 的局部闭环。
        - 当前步骤只处理自己的合同、命令、实施与校验。

        ## 下一跳列表
        - [contract]：`10_CONTRACT.md`
        """
    )


def render_compound_step_contract_doc(skill_name: str, step_name: str) -> str:
    return dedent(
        f"""\
        ---
        doc_id: {skill_name}.path.primary_flow.steps.{step_name}.contract
        doc_type: topic_atom
        topic: Contract for {step_name} of {skill_name}
        anchors:
        - target: 00_STEP_ENTRY.md
          relation: implements
          direction: upstream
          reason: The step entry starts here.
        - target: 15_TOOLS.md
          relation: routes_to
          direction: downstream
          reason: Tool guidance follows the step contract.
        ---

        # {step_name} Contract

        ## 当前动作要完成什么
        - [写清 `{step_name}` 的目标、输入、输出与退出条件。]
        - [只写当前步骤局部合同，不回填其他步骤正文。]

        ## 下一跳列表
        - [tools]：`15_TOOLS.md`
        """
    )


def render_compound_step_tools_doc(skill_name: str, step_name: str, script_name: str) -> str:
    return dedent(
        f"""\
        ---
        doc_id: {skill_name}.path.primary_flow.steps.{step_name}.tools
        doc_type: topic_atom
        topic: Tools for {step_name} of {skill_name}
        anchors:
        - target: 10_CONTRACT.md
          relation: implements
          direction: upstream
          reason: Tool guidance follows the step contract.
        - target: 20_EXECUTION.md
          relation: routes_to
          direction: downstream
          reason: Execution follows the tool guidance.
        ---

        # {step_name} Tools

        ## 当前动作要用什么命令
        - `python3 ./scripts/{script_name} runtime-contract --json`
        - [若当前步骤需要更多命令，只在这里继续补充。]

        ## 下一跳列表
        - [execution]：`20_EXECUTION.md`
        """
    )


def render_compound_step_execution_doc(skill_name: str, step_name: str) -> str:
    return dedent(
        f"""\
        ---
        doc_id: {skill_name}.path.primary_flow.steps.{step_name}.execution
        doc_type: topic_atom
        topic: Execution for {step_name} of {skill_name}
        anchors:
        - target: 15_TOOLS.md
          relation: implements
          direction: upstream
          reason: Execution follows the tool guidance.
        - target: 30_VALIDATION.md
          relation: routes_to
          direction: downstream
          reason: Validation follows execution.
        ---

        # {step_name} Execution

        ## 当前动作怎么做
        1. [写清 `{step_name}` 当前要执行的实际步骤。]
        2. [若需继续引用局部材料，只在当前步骤内向下引用。]

        ## 下一跳列表
        - [validation]：`30_VALIDATION.md`
        """
    )


def render_compound_step_validation_doc(skill_name: str, step_name: str, next_doc: str) -> str:
    return dedent(
        f"""\
        ---
        doc_id: {skill_name}.path.primary_flow.steps.{step_name}.validation
        doc_type: topic_atom
        topic: Validation for {step_name} of {skill_name}
        anchors:
        - target: 20_EXECUTION.md
          relation: implements
          direction: upstream
          reason: Validation closes the current step loop.
        - target: {next_doc}
          relation: routes_to
          direction: downstream
          reason: The next step or flow validation follows current-step validation.
        ---

        # {step_name} Validation

        ## 当前动作如何校验
        - [写清 `{step_name}` 的通过条件、失败信号与回退点。]

        ## 下一跳列表
        - [next]：`{next_doc}`
        """
    )


def render_compound_flow_validation_doc(skill_name: str) -> str:
    checks = [
        "结果目录包含 `SKILL.md / path / agents / scripts`。",
        "`path/00_SKILL_ENTRY.md` 是入口层索引。",
        "`path/primary_flow/20_WORKFLOW_INDEX.md` 已列出复合步骤。",
        "每个步骤目录都包含自己的 `contract -> tools -> execution -> validation`。",
        "不存在 `references/`、`assets/`、`tests/`。",
    ]
    return dedent(
        f"""\
        ---
        doc_id: {skill_name}.path.primary_flow.validation
        doc_type: topic_atom
        topic: Validation for the primary compound flow of {skill_name}
        anchors:
        - target: steps/step_03/30_VALIDATION.md
          relation: implements
          direction: upstream
          reason: Flow validation runs after the final compound step.
        ---

        # Primary Flow Validation

        ## 当前动作如何校验
        {render_bullets(checks)}
        """
    )


def build_generated_skill_files(skill_name: str, description: str, skill_mode: str) -> dict[str, str]:
    files = {
        "SKILL.md": render_skill_md(skill_name, description, skill_mode),
        "agents/openai.yaml": render_openai_yaml(skill_name, skill_mode),
    }
    if skill_mode == GUIDE_ONLY_MODE:
        return files

    files["path/00_SKILL_ENTRY.md"] = render_generated_skill_entry_doc(skill_name)
    files["scripts/Cli_Toolbox.py"] = render_generated_toolbox_script(skill_name, skill_mode)
    files["scripts/test_skill_layout.py"] = render_generated_test_script(skill_name, skill_mode)

    if skill_mode == GUIDE_WITH_TOOL_MODE:
        files["path/primary_flow/00_PRIMARY_FLOW_ENTRY.md"] = render_linear_entry_doc(skill_name)
        files["path/primary_flow/10_CONTRACT.md"] = render_linear_contract_doc(skill_name)
        files["path/primary_flow/15_TOOLS.md"] = render_linear_tools_doc(skill_name, "Cli_Toolbox.py")
        files["path/primary_flow/20_EXECUTION.md"] = render_linear_execution_doc(skill_name)
        files["path/primary_flow/30_VALIDATION.md"] = render_linear_validation_doc(skill_name)
        return files

    files["path/primary_flow/00_PRIMARY_FLOW_ENTRY.md"] = render_compound_entry_doc(skill_name)
    files["path/primary_flow/10_CONTRACT.md"] = render_compound_contract_doc(skill_name)
    files["path/primary_flow/15_TOOLS.md"] = render_compound_tools_doc(skill_name, "Cli_Toolbox.py")
    files["path/primary_flow/20_WORKFLOW_INDEX.md"] = render_compound_workflow_index_doc(skill_name)
    files["path/primary_flow/30_VALIDATION.md"] = render_compound_flow_validation_doc(skill_name)
    step_sequence = ("step_01", "step_02", "step_03")
    for index, step_name in enumerate(step_sequence):
        next_doc = "../../30_VALIDATION.md" if index == len(step_sequence) - 1 else f"../{step_sequence[index + 1]}/00_STEP_ENTRY.md"
        base = f"path/primary_flow/steps/{step_name}"
        files[f"{base}/00_STEP_ENTRY.md"] = render_compound_step_entry_doc(skill_name, step_name)
        files[f"{base}/10_CONTRACT.md"] = render_compound_step_contract_doc(skill_name, step_name)
        files[f"{base}/15_TOOLS.md"] = render_compound_step_tools_doc(skill_name, step_name, "Cli_Toolbox.py")
        files[f"{base}/20_EXECUTION.md"] = render_compound_step_execution_doc(skill_name, step_name)
        files[f"{base}/30_VALIDATION.md"] = render_compound_step_validation_doc(skill_name, step_name, next_doc)
    return files


def root_entries_for_mode(skill_mode: str) -> list[str]:
    if skill_mode == GUIDE_ONLY_MODE:
        return ["SKILL.md", "agents"]
    return ["SKILL.md", "path", "agents", "scripts"]
