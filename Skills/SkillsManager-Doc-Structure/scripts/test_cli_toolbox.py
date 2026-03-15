from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
CLI_PATH = SKILL_ROOT / "scripts" / "Cli_Toolbox.py"


def _run_cli(*args: str) -> dict[str, object]:
    completed = subprocess.run(
        ["python3", str(CLI_PATH), *args, "--json"],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _minimal_facade_skill(root: Path) -> None:
    _write(
        root / "SKILL.md",
        """---
name: temp-facade
description: facade only
skill_mode: guide_only
---

# Temp Facade

## 1. 模型立刻需要知道的事情
### 1. 总览
- facade only

### 2. 技能约束
- no path

### 3. 顶层常驻合同
- SKILL.md

## 2. 技能正文
- all guidance lives here

## 3. 目录结构图
```text
temp-facade/
├── SKILL.md
└── agents/
```
""",
    )
    _write(root / "agents" / "openai.yaml", "interface:\n  display_name: temp-facade\n")


def _linear_skill(root: Path) -> None:
    _write(
        root / "SKILL.md",
        """---
name: temp-linear
description: linear path
skill_mode: guide_with_tool
metadata:
  doc_structure:
    anchors:
    - target: path/00_SKILL_ENTRY.md
      relation: routes_to
      direction: downstream
      reason: facade routes to path
---

# Temp Linear

## 1. 模型立刻需要知道的事情
### 1. 总览
- linear path

### 2. 技能约束
- path first

### 3. 顶层常驻合同
- `path/00_SKILL_ENTRY.md`

## 2. 唯一入口
- [技能主入口]：`path/00_SKILL_ENTRY.md`

## 3. 目录结构图
```text
temp-linear/
├── SKILL.md
├── agents/
├── path/
└── scripts/
```
""",
    )
    _write(root / "agents" / "openai.yaml", "interface:\n  display_name: temp-linear\n")
    _write(root / "scripts" / "Cli_Toolbox.py", "print('linear')\n")
    _write(
        root / "path" / "00_SKILL_ENTRY.md",
        """---
anchors:
- target: primary_flow/00_PRIMARY_FLOW_ENTRY.md
  relation: routes_to
  direction: downstream
  reason: entry routes to primary flow
---

# Entry

## 当前动作
- route to the only path

## 下一跳列表
- [primary_flow]：`primary_flow/00_PRIMARY_FLOW_ENTRY.md`
""",
    )
    _write(
        root / "path" / "primary_flow" / "00_PRIMARY_FLOW_ENTRY.md",
        """---
anchors:
- target: 10_CONTRACT.md
  relation: routes_to
  direction: downstream
  reason: entry routes to contract
---

# Primary Flow Entry

## 当前动作
- enter the linear flow

## 下一跳列表
- [contract]：`10_CONTRACT.md`
""",
    )
    _write(
        root / "path" / "primary_flow" / "10_CONTRACT.md",
        """# Contract

## 本层说明
- define the current action

## 下一跳列表
- [tools]：`15_TOOLS.md`
""",
    )
    _write(
        root / "path" / "primary_flow" / "15_TOOLS.md",
        """# Tools

## 支撑信息
- describe the tool or lint surface

## 下一跳列表
- [execution]：`20_EXECUTION.md`
""",
    )
    _write(
        root / "path" / "primary_flow" / "20_EXECUTION.md",
        """# Execution

## 实施说明
- execute the linear flow

## 下一跳列表
- [validation]：`30_VALIDATION.md`
""",
    )
    _write(
        root / "path" / "primary_flow" / "30_VALIDATION.md",
        """# Validation

## 完成结果
- validate the result
""",
    )


def _compound_skill(root: Path) -> None:
    _linear_skill(root)
    skill_md = (root / "SKILL.md").read_text(encoding="utf-8").replace("guide_with_tool", "executable_workflow_skill")
    (root / "SKILL.md").write_text(skill_md, encoding="utf-8")
    primary_flow = root / "path" / "primary_flow"
    (primary_flow / "20_EXECUTION.md").unlink()
    _write(
        primary_flow / "20_WORKFLOW_INDEX.md",
        """# Workflow Index

## 当前动作
- expose the compound steps

## 下一跳列表
- [step_01]：`steps/step_01_shape/00_STEP_ENTRY.md`
""",
    )
    _write(
        primary_flow / "steps" / "step_01_shape" / "00_STEP_ENTRY.md",
        """---
anchors:
- target: 10_CONTRACT.md
  relation: routes_to
  direction: downstream
  reason: step entry routes to contract
---

# Step Entry

## 当前动作
- enter the step loop

## 下一跳列表
- [contract]：`10_CONTRACT.md`
""",
    )
    for name, next_name in [
        ("10_CONTRACT.md", "15_TOOLS.md"),
        ("15_TOOLS.md", "20_EXECUTION.md"),
        ("20_EXECUTION.md", "30_VALIDATION.md"),
    ]:
        _write(
            primary_flow / "steps" / "step_01_shape" / name,
            f"""# {name}

## 当前动作
- handle {name}

## 下一跳列表
- [next]：`{next_name}`
""",
        )
    _write(
        primary_flow / "steps" / "step_01_shape" / "30_VALIDATION.md",
        """# Step Validation

## 校验
- validate the step
""",
    )


def test_runtime_contract_reports_python_surface() -> None:
    payload = _run_cli("runtime-contract")
    assert payload["status"] == "ok"
    assert payload["runtime_entry"] == "./scripts/Cli_Toolbox.py"
    assert "lint-docstructure" in payload["commands"]


def test_linear_skill_docstructure_passes() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir) / "temp-linear"
        _linear_skill(root)
        payload = _run_cli("lint-docstructure", "--target", str(root))
        assert payload["status"] == "ok"
        assert payload["shape_kind"] == "linear_path"


def test_compound_skill_docstructure_passes() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir) / "temp-compound"
        _compound_skill(root)
        payload = _run_cli("lint-docstructure", "--target", str(root))
        assert payload["status"] == "ok"
        assert payload["shape_kind"] == "compound_path"


def test_extra_root_directory_fails_shape_lint() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir) / "temp-facade"
        _minimal_facade_skill(root)
        (root / "references").mkdir(parents=True, exist_ok=True)
        payload = _run_cli("lint-root-shape", "--target", str(root))
        assert payload["status"] == "error"
        assert "unexpected root entries: references" in payload["errors"][0]


def test_structure_lint_does_not_require_fixed_body_headings() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir) / "temp-linear-free-body"
        _linear_skill(root)
        payload = _run_cli("lint-reading-chain", "--target", str(root))
        assert payload["status"] == "ok"
