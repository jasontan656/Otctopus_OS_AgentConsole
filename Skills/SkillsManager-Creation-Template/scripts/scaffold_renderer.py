from __future__ import annotations

import json

from scaffold_models import DirectivePayload, RuntimeContractPayload, ScaffoldRequest
from template_loader import render_template


def _replacements(request: ScaffoldRequest) -> dict[str, str]:
    return {
        "skill_name": request.skill_name,
        "description": request.description,
        "slug": request.slug,
        "doc_topology": request.profile.doc_topology,
        "tooling_surface": request.profile.tooling_surface,
        "workflow_control": request.profile.workflow_control,
        "runtime_command": "run --json" if request.profile.tooling_surface == "automation_cli" else "contract --json",
    }


def render_skill_md(request: ScaffoldRequest) -> str:
    replacements = _replacements(request)
    if request.profile.doc_topology == "inline":
        return render_template("facades/inline_skill.md.tpl", replacements)
    if request.profile.doc_topology == "referenced":
        return render_template("facades/referenced_skill.md.tpl", replacements)
    return render_template("facades/workflow_skill.md.tpl", replacements)


def render_agent_yaml(request: ScaffoldRequest) -> str:
    return render_template("shared/agent_openai.yaml.tpl", _replacements(request))


def render_profile_doc(request: ScaffoldRequest) -> str:
    return render_template("references/selected_profile.md.tpl", _replacements(request))


def render_task_routing(request: ScaffoldRequest) -> str:
    replacements = _replacements(request)
    replacements["routing_line"] = (
        "- 先进入 `path/development_loop/00_DEVELOPMENT_LOOP_ENTRY.md`，再顺着 workflow 正文继续下沉。"
        if request.profile.doc_topology == "workflow_path"
        else "- 先读 `references/policies/SKILL_EXECUTION_RULES.md`，再按需要进入 tooling 文档。"
    )
    return render_template("references/task_routing.md.tpl", replacements)


def render_execution_policy(request: ScaffoldRequest) -> str:
    return render_template("references/skill_execution_rules.md.tpl", _replacements(request))


def render_runtime_contract_json(request: ScaffoldRequest) -> str:
    commands = {"contract": "read the runtime contract", "directive": "read a fixed directive"}
    if request.profile.tooling_surface == "automation_cli":
        commands["run"] = "placeholder automation entry"
    payload: RuntimeContractPayload = {
        "contract_name": f"{request.slug}_runtime_contract",
        "contract_version": "1.0.0",
        "skill_name": request.skill_name,
        "skill_role": "skill_scaffold_output",
        "runtime_source_policy": {
            "runtime_rule_source": "CLI_JSON",
            "documents_are_source_of_truth": True,
        },
        "tool_entry": {
            "script": "scripts/Cli_Toolbox.py",
            "commands": commands,
        },
        "artifact_policy": {
            "mode": "ephemeral_stdout_only",
            "resolver": "repo_local_integration_contract",
        },
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def render_runtime_contract_human(request: ScaffoldRequest) -> str:
    return render_template("runtime/skill_runtime_contract_human.md.tpl", _replacements(request))


def render_directive_index() -> str:
    payload = {
        "topics": {
            "execution-boundary": {
                "doc_kind": "guide",
                "json_path": "EXECUTION_BOUNDARY_DIRECTIVE.json",
                "human_path": "EXECUTION_BOUNDARY_DIRECTIVE_human.md",
            }
        }
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def render_execution_boundary_directive_json(request: ScaffoldRequest) -> str:
    payload: DirectivePayload = {
        "directive_name": f"{request.slug}_execution_boundary",
        "directive_version": "1.0.0",
        "doc_kind": "guide",
        "topic": "execution-boundary",
        "purpose": "Keep stable contracts in docs and implementation details in code.",
        "instruction": [
            "Update references and tests together with scripts.",
            "Do not hardcode repo-level runtime result paths in the skill contract.",
        ],
        "workflow": [
            "Read the runtime contract.",
            "Read the selected profile.",
            "Execute the governed command.",
        ],
        "rules": [
            "Do not reintroduce legacy skill_mode semantics.",
        ],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def render_execution_boundary_directive_human(request: ScaffoldRequest) -> str:
    return render_template("runtime/execution_boundary_human.md.tpl", _replacements(request))


def render_cli_usage(request: ScaffoldRequest) -> str:
    return render_template("tooling/cli_usage.md.tpl", _replacements(request))


def render_cli_development(request: ScaffoldRequest) -> str:
    return render_template("tooling/cli_development.md.tpl", _replacements(request))


def render_generated_cli(request: ScaffoldRequest) -> str:
    template_name = "scripts/cli_automation.py.tpl" if request.profile.tooling_surface == "automation_cli" else "scripts/cli_contract.py.tpl"
    return render_template(template_name, _replacements(request))


def render_generated_test(request: ScaffoldRequest) -> str:
    template_name = "tests/test_cli_automation.py.tpl" if request.profile.tooling_surface == "automation_cli" else "tests/test_cli_contract.py.tpl"
    return render_template(template_name, _replacements(request))


def render_workflow_files() -> dict[str, str]:
    return {
        "path/development_loop/00_DEVELOPMENT_LOOP_ENTRY.md": render_template("workflow/00_DEVELOPMENT_LOOP_ENTRY.md.tpl", {}),
        "path/development_loop/20_WORKFLOW_INDEX.md": render_template("workflow/20_WORKFLOW_INDEX.md.tpl", {}),
        "path/development_loop/30_VALIDATION.md": render_template("workflow/30_VALIDATION.md.tpl", {}),
        "path/development_loop/steps/primary_step/00_PRIMARY_STEP_ENTRY.md": render_template("workflow/steps/00_PRIMARY_STEP_ENTRY.md.tpl", {}),
        "path/development_loop/steps/primary_step/10_CONTRACT.md": render_template("workflow/steps/10_CONTRACT.md.tpl", {}),
        "path/development_loop/steps/primary_step/20_EXECUTION.md": render_template("workflow/steps/20_EXECUTION.md.tpl", {}),
        "path/development_loop/steps/primary_step/30_VALIDATION.md": render_template("workflow/steps/30_VALIDATION.md.tpl", {}),
    }


def render_files(request: ScaffoldRequest) -> dict[str, str]:
    files = {
        "SKILL.md": render_skill_md(request),
        "agents/openai.yaml": render_agent_yaml(request),
    }
    if request.profile.doc_topology != "inline":
        files.update(
            {
                "references/routing/TASK_ROUTING.md": render_task_routing(request),
                "references/profiles/SELECTED_PROFILE.md": render_profile_doc(request),
                "references/policies/SKILL_EXECUTION_RULES.md": render_execution_policy(request),
            }
        )
    if request.profile.tooling_surface != "none":
        files.update(
            {
                "references/runtime_contracts/SKILL_RUNTIME_CONTRACT.json": render_runtime_contract_json(request),
                "references/runtime_contracts/SKILL_RUNTIME_CONTRACT_human.md": render_runtime_contract_human(request),
                "references/runtime_contracts/DIRECTIVE_INDEX.json": render_directive_index(),
                "references/runtime_contracts/EXECUTION_BOUNDARY_DIRECTIVE.json": render_execution_boundary_directive_json(request),
                "references/runtime_contracts/EXECUTION_BOUNDARY_DIRECTIVE_human.md": render_execution_boundary_directive_human(request),
                "references/tooling/Cli_Toolbox_USAGE.md": render_cli_usage(request),
                "references/tooling/Cli_Toolbox_DEVELOPMENT.md": render_cli_development(request),
                "scripts/Cli_Toolbox.py": render_generated_cli(request),
                "tests/test_cli_toolbox.py": render_generated_test(request),
            }
        )
    if request.profile.doc_topology == "workflow_path":
        files.update(render_workflow_files())
        contract_name = "workflow/10_CONTRACT_WITH_TOOLS.md.tpl" if request.profile.tooling_surface != "none" else "workflow/10_CONTRACT.md.tpl"
        files["path/development_loop/10_CONTRACT.md"] = render_template(contract_name, {})
        if request.profile.tooling_surface != "none":
            files["path/development_loop/15_TOOLS.md"] = render_template("workflow/15_TOOLS.md.tpl", {})
    return files
