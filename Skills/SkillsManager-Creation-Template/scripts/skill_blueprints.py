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


def _code_block(lines: list[str]) -> str:
    return "\n".join(lines)


def _skill_tree(skill_mode: str) -> list[str]:
    if skill_mode == GUIDE_ONLY_MODE:
        return ["<skill-name>/", "├── SKILL.md", "└── agents/"]
    return ["<skill-name>/", "├── SKILL.md", "├── agents/", "├── path/", "└── scripts/"]


def render_skill_md(skill_name: str, description: str, skill_mode: str) -> str:
    frontmatter = [
        "---",
        f"name: {skill_name}",
        f"description: {description}",
        f"skill_mode: {skill_mode}",
    ]
    if skill_mode != GUIDE_ONLY_MODE:
        frontmatter.extend(
            [
                "metadata:",
                "  doc_structure:",
                f"    doc_id: {skill_name}.entry.facade",
                "    doc_type: skill_facade",
                f"    topic: Entry facade for {skill_name}",
                "    reading_chain:",
                "    - key: primary_flow",
                "      target: path/primary_flow/00_PRIMARY_FLOW_ENTRY.md",
                "      hop: entry",
                "      reason: The facade exposes the default function entry.",
            ]
        )
    frontmatter.extend(["---", ""])

    if skill_mode == GUIDE_ONLY_MODE:
        body = [
            f"# {skill_name}",
            "",
            "## 1. 模型立刻需要知道的事情",
            "### 1. 总览",
            "- 当前形态为最小技能。",
            "- `SKILL.md` 承载完整正文。",
            "- 根目录包含 `SKILL.md / agents`。",
            "",
            "### 2. 技能约束",
            "- 不使用 `path/`。",
            "- 不使用 `scripts/`。",
            "",
            "### 3. 顶层常驻合同",
            "- 阅读从 `SKILL.md` 开始，也在 `SKILL.md` 内结束。",
            "",
            "## 2. 技能正文",
            "- [在此直接填写目标技能的完整正文，不要假设存在 `path/` 或 `scripts/`。]",
            "",
            "## 3. 目录结构图",
            "```text",
            *_skill_tree(skill_mode),
            "```",
            "",
        ]
        return "\n".join(frontmatter + body)

    overview = [
        f"- 当前形态为 `{skill_mode}`。",
        "- `SKILL.md + path/*.md` 承载完整正文。",
        "- 功能入口通过 `reading_chain` 继续下沉。",
        "- `scripts/` 提供 `read-contract-context` 与 `read-path-context`。",
    ]
    if skill_mode == GUIDE_WITH_TOOL_MODE:
        constraints = [
            "- 允许多个平行功能入口，但每个入口进入后必须单线到底。",
            "- 默认闭环为 `contract -> tools -> execution -> validation`。",
            "- 入口内部不允许再次分叉。",
        ]
    else:
        constraints = [
            "- 允许入口进入后继续下沉到复合 workflow。",
            "- 默认主链为 `contract -> tools -> workflow_index -> steps -> validation`。",
            "- workflow index 以下的步骤继续形成各自局部闭环。",
        ]
    body = [
        f"# {skill_name}",
        "",
        "## 1. 模型立刻需要知道的事情",
        "### 1. 总览",
        *overview,
        "",
        "### 2. 技能约束",
        "- `SKILL.md` 直接暴露功能入口。",
        "- 深层正文沿当前入口继续下沉。",
        "- 有 `scripts/` 的技能形态必须提供链路编译型 CLI。",
        *constraints,
        "",
        "### 3. 顶层常驻合同",
        "- 文档链本身是真源；CLI 只是文档链的编译输出。",
        "- 后续阅读只沿当前选中的功能入口继续下沉。",
        "",
        "## 2. 功能入口",
        "- [primary_flow]：`path/primary_flow/00_PRIMARY_FLOW_ENTRY.md`",
        "  - 作用：默认功能入口；如需新增入口，应与它平行出现。",
        "  - 快捷阅读：`python3 ./scripts/Cli_Toolbox.py read-contract-context --entry primary_flow --json`",
        "",
        "## 3. 目录结构图",
        "```text",
        *_skill_tree(skill_mode),
        "```",
        "",
    ]
    return "\n".join(frontmatter + body)


def render_openai_yaml(skill_name: str, skill_mode: str) -> str:
    display_name = title_from_slug(skill_name)
    if skill_mode == GUIDE_ONLY_MODE:
        default_prompt = f"Use ${skill_name}."
    else:
        default_prompt = f"Use ${skill_name}."
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
    payload: dict[str, object] = {
        "skill_name": skill_name,
        "skill_mode": skill_mode,
    }
    if skill_mode == GUIDE_ONLY_MODE:
        payload["root_shape"] = ["SKILL.md", "agents"]
        payload["reading_protocol"] = ["SKILL.md"]
        payload["layout_rule"] = "Self-contained skill. No path or scripts are generated."
        return payload

    payload["root_shape"] = ["SKILL.md", "path", "agents", "scripts"]
    payload["entry_doc"] = "path/primary_flow/00_PRIMARY_FLOW_ENTRY.md"
    payload["commands"] = ["runtime-contract", "read-contract-context", "read-path-context"]
    payload["layout_rule"] = "Folder layout must mirror reading order."
    payload["compiler_rule"] = "CLI compiles reading_chain into one context payload; docs remain the only source of truth."
    if skill_mode == GUIDE_WITH_TOOL_MODE:
        payload["reading_protocol"] = [
            "SKILL.md",
            "entry",
            "contract",
            "tools",
            "execution",
            "validation",
        ]
    else:
        payload["reading_protocol"] = [
            "SKILL.md",
            "entry",
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
            "from pathlib import Path",
            "",
            "import yaml",
            "",
            "SKILL_ROOT = Path(__file__).resolve().parents[1]",
            f"RUNTIME_CONTRACT = {payload}",
            "",
            "",
            "def _parse_frontmatter(markdown_path: Path) -> tuple[dict[str, object], str]:",
            "    text = markdown_path.read_text(encoding='utf-8')",
            "    if not text.startswith('---\\n'):",
            "        return {}, text",
            "    closing = text.find('\\n---\\n', 4)",
            "    if closing == -1:",
            "        return {}, text",
            "    payload = yaml.safe_load(text[4:closing]) or {}",
            "    if not isinstance(payload, dict):",
            "        payload = {}",
            "    return payload, text[closing + 5:]",
            "",
            "",
            "def _chain(markdown_path: Path) -> list[dict[str, str]]:",
            "    frontmatter, _ = _parse_frontmatter(markdown_path)",
            "    doc_structure = frontmatter.get('metadata', {}).get('doc_structure', {}) if isinstance(frontmatter.get('metadata'), dict) else {}",
            "    raw = doc_structure.get('reading_chain') if markdown_path.name == 'SKILL.md' else frontmatter.get('reading_chain')",
            "    if not isinstance(raw, list):",
            "        return []",
            "    items: list[dict[str, str]] = []",
            "    for item in raw:",
            "        if not isinstance(item, dict):",
            "            continue",
            "        key = item.get('key')",
            "        target = item.get('target')",
            "        hop = item.get('hop')",
            "        if isinstance(key, str) and isinstance(target, str) and isinstance(hop, str):",
            "            items.append({'key': key, 'target': target, 'hop': hop, 'reason': str(item.get('reason', ''))})",
            "    return items",
            "",
            "",
            "def _title(body: str) -> str:",
            "    for line in body.splitlines():",
            "        if line.startswith('#'):",
            "            return line.lstrip('#').strip()",
            "    return ''",
            "",
            "",
            "def _compile(entry: str, selection: list[str]) -> dict[str, object]:",
            "    if SKILL_ROOT.name == '' or not (SKILL_ROOT / 'SKILL.md').exists():",
            "        return {'status': 'error', 'error': 'missing_skill_root'}",
            "    skill_md = SKILL_ROOT / 'SKILL.md'",
            "    segments: list[dict[str, str]] = []",
            "    resolved_chain: list[str] = ['SKILL.md']",
            "    _, skill_body = _parse_frontmatter(skill_md)",
            "    segments.append({'source': 'SKILL.md', 'title': _title(skill_body), 'content': skill_body.strip()})",
            "    root_items = _chain(skill_md)",
            "    chosen = next((item for item in root_items if item['key'] == entry), None)",
            "    if chosen is None:",
            "        return {'status': 'error', 'error': 'entry_not_found', 'entry': entry, 'available_entries': [item['key'] for item in root_items]}",
            "    queue = list(selection)",
            "    current = (skill_md.parent / chosen['target']).resolve()",
            "    while True:",
            "        frontmatter, body = _parse_frontmatter(current)",
            "        rel = current.relative_to(SKILL_ROOT).as_posix()",
            "        resolved_chain.append(rel)",
            "        segments.append({'source': rel, 'title': _title(body), 'content': body.strip()})",
            "        items = _chain(current)",
            "        if not items:",
            "            break",
            "        if len(items) > 1:",
            "            if not queue:",
            "                return {'status': 'branch_selection_required', 'entry': entry, 'resolved_chain': resolved_chain, 'segments': segments, 'available_next': [item['key'] for item in items], 'current_source': rel}",
            "            wanted = queue.pop(0)",
            "            chosen = next((item for item in items if item['key'] == wanted), None)",
            "            if chosen is None:",
            "                return {'status': 'branch_selection_required', 'entry': entry, 'resolved_chain': resolved_chain, 'segments': segments, 'available_next': [item['key'] for item in items], 'current_source': rel}",
            "        else:",
            "            chosen = items[0]",
            "        current = (current.parent / chosen['target']).resolve()",
            "    return {'status': 'ok', 'entry': entry, 'resolved_chain': resolved_chain, 'segments': segments, 'compiled_markdown': '\\n\\n'.join(item['content'] for item in segments if item['content'])}",
            "",
            "",
            "def main() -> int:",
            f'    parser = argparse.ArgumentParser(description="{skill_name} toolbox")',
            "    subparsers = parser.add_subparsers(dest='command', required=True)",
            "    runtime_contract = subparsers.add_parser('runtime-contract')",
            "    runtime_contract.add_argument('--json', action='store_true')",
            "    for name in ('read-path-context', 'read-contract-context'):",
            "        read_context = subparsers.add_parser(name)",
            "        read_context.add_argument('--entry', required=True)",
            "        read_context.add_argument('--selection', default='')",
            "        read_context.add_argument('--json', action='store_true')",
            "    args = parser.parse_args()",
            "    if args.command == 'runtime-contract':",
            "        payload = RUNTIME_CONTRACT",
            "    elif args.command in {'read-path-context', 'read-contract-context'}:",
            "        selection = [item.strip() for item in args.selection.split(',') if item.strip()]",
            "        payload = _compile(args.entry, selection)",
            "    else:",
            "        return 1",
            "    if args.json:",
            "        print(json.dumps(payload, ensure_ascii=False, indent=2))",
            "    else:",
            "        print(payload.get('status', 'ok'))",
            "    return 0",
            "",
            "",
            "if __name__ == '__main__':",
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
    compile_assert = "" if skill_mode == GUIDE_ONLY_MODE else dedent(
        """\
        def test_read_path_context() -> None:
            completed = subprocess.run(
                ["python3", str(SKILL_ROOT / "scripts" / "Cli_Toolbox.py"), "read-contract-context", "--entry", "primary_flow", "--json"],
                check=True,
                capture_output=True,
                text=True,
            )
            payload = json.loads(completed.stdout)
            assert payload["status"] in {"ok", "branch_selection_required"}
        """
    )
    return dedent(
        f"""\
        from __future__ import annotations

        import json
        import subprocess
        from pathlib import Path


        SKILL_ROOT = Path(__file__).resolve().parents[1]
        EXPECTED_PATHS = {expected_json}


        def test_layout() -> None:
            for relative_path in EXPECTED_PATHS:
                assert (SKILL_ROOT / relative_path).exists(), relative_path


        {compile_assert}
        """
    )


def _linear_entry_doc(skill_name: str) -> str:
    return dedent(
        f"""\
        ---
        doc_id: {skill_name}.path.primary_flow.entry
        doc_type: path_doc
        topic: Primary linear entry for {skill_name}
        reading_chain:
        - key: contract
          target: 10_CONTRACT.md
          hop: next
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


def _linear_contract_doc(skill_name: str) -> str:
    return dedent(
        f"""\
        ---
        doc_id: {skill_name}.path.primary_flow.contract
        doc_type: topic_atom
        topic: Contract for the primary linear flow of {skill_name}
        reading_chain:
        - key: tools
          target: 15_TOOLS.md
          hop: next
          reason: Tool guidance follows the contract.
        ---

        # Primary Flow Contract

        ## 当前动作要完成什么
        - 形成一个入口内单线到底的 workflow。
        - 当前默认骨架包含：`contract -> tools -> execution -> validation`。

        ## 下一跳列表
        - [tools]：`15_TOOLS.md`
        """
    )


def _linear_tools_doc(skill_name: str) -> str:
    return dedent(
        f"""\
        ---
        doc_id: {skill_name}.path.primary_flow.tools
        doc_type: topic_atom
        topic: Tool or lint surface for the primary linear flow of {skill_name}
        reading_chain:
        - key: execution
          target: 20_EXECUTION.md
          hop: next
          reason: Execution follows the tool guidance.
        ---

        # Primary Flow Tool/Lint Surface

        ## 当前动作要用什么命令
        - `python3 ./scripts/Cli_Toolbox.py read-contract-context --entry primary_flow --json`
        - [在这里列出当前入口真正需要的其他命令。]

        ## 下一跳列表
        - [execution]：`20_EXECUTION.md`
        """
    )


def _linear_execution_doc(skill_name: str) -> str:
    return dedent(
        f"""\
        ---
        doc_id: {skill_name}.path.primary_flow.execution
        doc_type: topic_atom
        topic: Execution for the primary linear flow of {skill_name}
        reading_chain:
        - key: validation
          target: 30_VALIDATION.md
          hop: next
          reason: Validation closes the linear flow.
        ---

        # Primary Flow Execution

        ## 当前动作怎么做
        1. 明确当前入口的真实业务主轴与边界。
        2. 命令脚本放在 `scripts/`，命令说明写在 `15_TOOLS.md`。
        3. 让 `read-contract-context` 可以把当前链路完整编译出来。

        ## 下一跳列表
        - [validation]：`30_VALIDATION.md`
        """
    )


def _linear_validation_doc(skill_name: str) -> str:
    return dedent(
        f"""\
        ---
        doc_id: {skill_name}.path.primary_flow.validation
        doc_type: topic_atom
        topic: Validation for the primary linear flow of {skill_name}
        ---

        # Primary Flow Validation

        ## 当前动作如何校验
        - 结果目录包含 `SKILL.md / path / agents / scripts`。
        - `read-contract-context --entry primary_flow --json` 能输出完整链路上下文。
        - 不存在 `references/`、`assets/`、`tests/`。
        """
    )


def _compound_entry_doc(skill_name: str) -> str:
    return dedent(
        f"""\
        ---
        doc_id: {skill_name}.path.primary_flow.entry
        doc_type: path_doc
        topic: Primary compound entry for {skill_name}
        reading_chain:
        - key: contract
          target: 10_CONTRACT.md
          hop: next
          reason: The compound workflow starts from the contract doc.
        ---

        # Primary Flow Entry

        ## 这个入口是干什么的
        - 本入口承载当前默认主入口动作。
        - 进入本入口后，需要继续完成一个复合 workflow。

        ## 下一跳列表
        - [contract]：`10_CONTRACT.md`
        """
    )


def _compound_contract_doc(skill_name: str) -> str:
    return dedent(
        f"""\
        ---
        doc_id: {skill_name}.path.primary_flow.contract
        doc_type: topic_atom
        topic: Contract for the primary compound flow of {skill_name}
        reading_chain:
        - key: tools
          target: 15_TOOLS.md
          hop: next
          reason: Tool guidance follows the contract.
        ---

        # Primary Flow Contract

        ## 当前动作要完成什么
        - 形成一个入口内带复合 workflow 的技能骨架。
        - 当前默认骨架包含：`contract -> tools -> workflow_index -> steps -> validation`。

        ## 下一跳列表
        - [tools]：`15_TOOLS.md`
        """
    )


def _compound_tools_doc(skill_name: str) -> str:
    return dedent(
        f"""\
        ---
        doc_id: {skill_name}.path.primary_flow.tools
        doc_type: topic_atom
        topic: Tools for the primary compound flow of {skill_name}
        reading_chain:
        - key: workflow
          target: 20_WORKFLOW_INDEX.md
          hop: next
          reason: Workflow index follows the tool guidance.
        ---

        # Primary Flow Tools

        ## 当前动作要用什么命令
        - `python3 ./scripts/Cli_Toolbox.py read-contract-context --entry primary_flow --selection step_01 --json`
        - [若某个步骤需要额外命令，应写入该步骤自己的 tools 节点。]

        ## 下一跳列表
        - [workflow_index]：`20_WORKFLOW_INDEX.md`
        """
    )


def _compound_workflow_index_doc(skill_name: str) -> str:
    return dedent(
        f"""\
        ---
        doc_id: {skill_name}.path.primary_flow.workflow_index
        doc_type: index_doc
        topic: Workflow index for the primary compound flow of {skill_name}
        reading_chain:
        - key: step_01
          target: steps/step_01/00_STEP_ENTRY.md
          hop: branch
          reason: Compound execution starts from step_01.
        - key: step_02
          target: steps/step_02/00_STEP_ENTRY.md
          hop: branch
          reason: Compound execution can continue from step_02.
        - key: step_03
          target: steps/step_03/00_STEP_ENTRY.md
          hop: branch
          reason: Compound execution can continue from step_03.
        ---

        # Primary Flow Workflow Index

        ## 当前入口的复合步骤
        1. [step_01]：`steps/step_01/00_STEP_ENTRY.md`
        2. [step_02]：`steps/step_02/00_STEP_ENTRY.md`
        3. [step_03]：`steps/step_03/00_STEP_ENTRY.md`
        """
    )


def _step_entry_doc(skill_name: str, step_name: str) -> str:
    return dedent(
        f"""\
        ---
        doc_id: {skill_name}.path.primary_flow.steps.{step_name}.entry
        doc_type: path_doc
        topic: Entry doc for {step_name} of {skill_name}
        reading_chain:
        - key: contract
          target: 10_CONTRACT.md
          hop: next
          reason: Each step starts from its contract doc.
        ---

        # {step_name} Entry

        ## 这个入口是干什么的
        - 本入口承载 `{step_name}` 的局部闭环。

        ## 下一跳列表
        - [contract]：`10_CONTRACT.md`
        """
    )


def _step_contract_doc(skill_name: str, step_name: str) -> str:
    return dedent(
        f"""\
        ---
        doc_id: {skill_name}.path.primary_flow.steps.{step_name}.contract
        doc_type: topic_atom
        topic: Contract for {step_name} of {skill_name}
        reading_chain:
        - key: tools
          target: 15_TOOLS.md
          hop: next
          reason: Tool guidance follows the step contract.
        ---

        # {step_name} Contract

        ## 当前动作要完成什么
        - [写清 `{step_name}` 的目标、输入、输出与退出条件。]

        ## 下一跳列表
        - [tools]：`15_TOOLS.md`
        """
    )


def _step_tools_doc(skill_name: str, step_name: str) -> str:
    return dedent(
        f"""\
        ---
        doc_id: {skill_name}.path.primary_flow.steps.{step_name}.tools
        doc_type: topic_atom
        topic: Tools for {step_name} of {skill_name}
        reading_chain:
        - key: execution
          target: 20_EXECUTION.md
          hop: next
          reason: Execution follows the tool guidance.
        ---

        # {step_name} Tools

        ## 当前动作要用什么命令
        - [在这里列出当前步骤真正需要的命令。]

        ## 下一跳列表
        - [execution]：`20_EXECUTION.md`
        """
    )


def _step_execution_doc(skill_name: str, step_name: str) -> str:
    return dedent(
        f"""\
        ---
        doc_id: {skill_name}.path.primary_flow.steps.{step_name}.execution
        doc_type: topic_atom
        topic: Execution for {step_name} of {skill_name}
        reading_chain:
        - key: validation
          target: 30_VALIDATION.md
          hop: next
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


def _step_validation_doc(skill_name: str, step_name: str, next_doc: str) -> str:
    frontmatter = [
        "---",
        f"doc_id: {skill_name}.path.primary_flow.steps.{step_name}.validation",
        "doc_type: topic_atom",
        f"topic: Validation for {step_name} of {skill_name}",
    ]
    if next_doc:
        frontmatter.extend(
            [
                "reading_chain:",
                "- key: next",
                f"  target: {next_doc}",
                "  hop: next",
                "  reason: The next step or flow validation follows current-step validation.",
            ]
        )
    frontmatter.extend(["---", ""])
    body = [
        f"# {step_name} Validation",
        "",
        "## 当前动作如何校验",
        f"- [写清 `{step_name}` 的通过条件、失败信号与回退点。]",
    ]
    if next_doc:
        body.extend(["", "## 下一跳列表", f"- [next]：`{next_doc}`"])
    body.append("")
    return "\n".join(frontmatter + body)


def _compound_flow_validation_doc(skill_name: str) -> str:
    return dedent(
        f"""\
        ---
        doc_id: {skill_name}.path.primary_flow.validation
        doc_type: topic_atom
        topic: Validation for the primary compound flow of {skill_name}
        ---

        # Primary Flow Validation

        ## 当前动作如何校验
        - 结果目录包含 `SKILL.md / path / agents / scripts`。
        - `path/primary_flow/20_WORKFLOW_INDEX.md` 已列出复合步骤。
        - `read-contract-context` 支持通过 `--selection` 编译具体步骤链路。
        """
    )


def build_generated_skill_files(skill_name: str, description: str, skill_mode: str) -> dict[str, str]:
    files = {
        "SKILL.md": render_skill_md(skill_name, description, skill_mode),
        "agents/openai.yaml": render_openai_yaml(skill_name, skill_mode),
    }
    if skill_mode == GUIDE_ONLY_MODE:
        return files

    files["scripts/Cli_Toolbox.py"] = render_generated_toolbox_script(skill_name, skill_mode)
    files["scripts/test_skill_layout.py"] = render_generated_test_script(skill_name, skill_mode)

    if skill_mode == GUIDE_WITH_TOOL_MODE:
        files["path/primary_flow/00_PRIMARY_FLOW_ENTRY.md"] = _linear_entry_doc(skill_name)
        files["path/primary_flow/10_CONTRACT.md"] = _linear_contract_doc(skill_name)
        files["path/primary_flow/15_TOOLS.md"] = _linear_tools_doc(skill_name)
        files["path/primary_flow/20_EXECUTION.md"] = _linear_execution_doc(skill_name)
        files["path/primary_flow/30_VALIDATION.md"] = _linear_validation_doc(skill_name)
        return files

    files["path/primary_flow/00_PRIMARY_FLOW_ENTRY.md"] = _compound_entry_doc(skill_name)
    files["path/primary_flow/10_CONTRACT.md"] = _compound_contract_doc(skill_name)
    files["path/primary_flow/15_TOOLS.md"] = _compound_tools_doc(skill_name)
    files["path/primary_flow/20_WORKFLOW_INDEX.md"] = _compound_workflow_index_doc(skill_name)
    files["path/primary_flow/30_VALIDATION.md"] = _compound_flow_validation_doc(skill_name)
    step_sequence = ("step_01", "step_02", "step_03")
    for index, step_name in enumerate(step_sequence):
        next_doc = "../../30_VALIDATION.md" if index == len(step_sequence) - 1 else f"../{step_sequence[index + 1]}/00_STEP_ENTRY.md"
        base = f"path/primary_flow/steps/{step_name}"
        files[f"{base}/00_STEP_ENTRY.md"] = _step_entry_doc(skill_name, step_name)
        files[f"{base}/10_CONTRACT.md"] = _step_contract_doc(skill_name, step_name)
        files[f"{base}/15_TOOLS.md"] = _step_tools_doc(skill_name, step_name)
        files[f"{base}/20_EXECUTION.md"] = _step_execution_doc(skill_name, step_name)
        files[f"{base}/30_VALIDATION.md"] = _step_validation_doc(skill_name, step_name, next_doc)
    return files


def root_entries_for_mode(skill_mode: str) -> list[str]:
    if skill_mode == GUIDE_ONLY_MODE:
        return ["SKILL.md", "agents"]
    return ["SKILL.md", "path", "agents", "scripts"]
