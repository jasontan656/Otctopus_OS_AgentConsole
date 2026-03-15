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
    reading_chain:
    - key: primary_flow
      target: path/primary_flow/00_PRIMARY_FLOW_ENTRY.md
      hop: entry
      reason: facade routes to function entry
---

# Temp Linear

## 1. 模型立刻需要知道的事情
### 1. 总览
- linear path

### 2. 技能约束
- path first

### 3. 顶层常驻合同
- choose one function entry

## 2. 功能入口
- [primary_flow]：`path/primary_flow/00_PRIMARY_FLOW_ENTRY.md`

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
        root / "path" / "primary_flow" / "00_PRIMARY_FLOW_ENTRY.md",
        """---
reading_chain:
- key: contract
  target: 10_CONTRACT.md
  hop: next
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
        """---
reading_chain:
- key: tools
  target: 15_TOOLS.md
  hop: next
  reason: contract routes to tools
---

# Contract

## 本层说明
- define the current action

## 下一跳列表
- [tools]：`15_TOOLS.md`
""",
    )
    _write(
        root / "path" / "primary_flow" / "15_TOOLS.md",
        """---
reading_chain:
- key: execution
  target: 20_EXECUTION.md
  hop: next
  reason: tools route to execution
---

# Tools

## 支撑信息
- describe the tool or lint surface

## 下一跳列表
- [execution]：`20_EXECUTION.md`
""",
    )
    _write(
        root / "path" / "primary_flow" / "20_EXECUTION.md",
        """---
reading_chain:
- key: validation
  target: 30_VALIDATION.md
  hop: next
  reason: execution routes to validation
---

# Execution

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
    (root / "SKILL.md").write_text(
        (root / "SKILL.md").read_text(encoding="utf-8").replace("guide_with_tool", "executable_workflow_skill"),
        encoding="utf-8",
    )
    (root / "path" / "primary_flow" / "20_EXECUTION.md").unlink()
    _write(
        root / "path" / "primary_flow" / "15_TOOLS.md",
        """---
reading_chain:
- key: workflow
  target: 20_WORKFLOW_INDEX.md
  hop: next
  reason: tools route to workflow index
---

# Tools

## 支撑信息
- describe the tool or lint surface

## 下一跳列表
- [workflow]：`20_WORKFLOW_INDEX.md`
""",
    )
    _write(
        root / "path" / "primary_flow" / "20_WORKFLOW_INDEX.md",
        """---
reading_chain:
- key: step_01
  target: steps/step_01/00_STEP_ENTRY.md
  hop: branch
  reason: workflow index branches into steps
---

# Workflow Index

## 当前动作
- expose compound steps

## 下一跳列表
- [step_01]：`steps/step_01/00_STEP_ENTRY.md`
""",
    )
    _write(
        root / "path" / "primary_flow" / "steps" / "step_01" / "00_STEP_ENTRY.md",
        """---
reading_chain:
- key: contract
  target: 10_CONTRACT.md
  hop: next
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
            root / "path" / "primary_flow" / "steps" / "step_01" / name,
            f"""---
reading_chain:
- key: next
  target: {next_name}
  hop: next
  reason: follow the step chain
---

# {name}

## 当前动作
- handle {name}

## 下一跳列表
- [next]：`{next_name}`
""",
        )
    _write(
        root / "path" / "primary_flow" / "steps" / "step_01" / "30_VALIDATION.md",
        """# Step Validation

## 校验
- validate the step
""",
    )


def test_runtime_contract_reports_reading_chain_surface() -> None:
    payload = _run_cli("runtime-contract")
    assert payload["status"] == "ok"
    assert "compile-reading-chain" in payload["commands"]
    assert "read-contract-context" in payload["commands"]
    assert "read-path-context" in payload["commands"]


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


def test_compile_linear_chain_returns_compiled_markdown() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir) / "temp-linear"
        _linear_skill(root)
        payload = _run_cli("compile-reading-chain", "--target", str(root), "--entry", "primary_flow")
        assert payload["status"] == "ok"
        assert payload["resolved_chain"][0] == "SKILL.md"
        assert "Primary Flow Entry" in payload["compiled_markdown"]


def test_self_read_path_context_compiles_this_skill() -> None:
    payload = _run_cli("read-path-context", "--entry", "target_shape", "--selection", "facade_only,next_hop,skill_facade")
    assert payload["status"] == "ok"
    assert payload["resolved_chain"][0] == "SKILL.md"
    assert any(item.endswith("21_TARGET_SHAPE.md") for item in payload["resolved_chain"])


def test_self_read_contract_context_compiles_this_skill() -> None:
    payload = _run_cli("read-contract-context", "--entry", "target_shape", "--selection", "facade_only,next_hop,skill_facade")
    assert payload["status"] == "ok"
    assert payload["resolved_chain"][0] == "SKILL.md"
    assert any(item.endswith("21_TARGET_SHAPE.md") for item in payload["resolved_chain"])


def test_compile_compound_chain_requires_branch_selection() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir) / "temp-compound"
        _compound_skill(root)
        payload = _run_cli("compile-reading-chain", "--target", str(root), "--entry", "primary_flow")
        assert payload["status"] == "ok"
        assert any(item.endswith("steps/step_01/00_STEP_ENTRY.md") for item in payload["resolved_chain"])


def test_compile_compound_chain_with_selection_passes() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir) / "temp-compound"
        _compound_skill(root)
        payload = _run_cli(
            "compile-reading-chain",
            "--target",
            str(root),
            "--entry",
            "primary_flow",
            "--selection",
            "step_01",
        )
        assert payload["status"] == "ok"
        assert any(item.endswith("steps/step_01/00_STEP_ENTRY.md") for item in payload["resolved_chain"])


def test_extra_root_directory_fails_shape_lint() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir) / "temp-facade"
        _minimal_facade_skill(root)
        (root / "references").mkdir(parents=True, exist_ok=True)
        payload = _run_cli("lint-root-shape", "--target", str(root))
        assert payload["status"] == "error"
        assert "unexpected root entries: references" in payload["errors"][0]


def test_missing_reading_chain_target_fails() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir) / "temp-linear"
        _linear_skill(root)
        broken = root / "path" / "primary_flow" / "20_EXECUTION.md"
        broken.write_text(
            """---
reading_chain:
- key: validation
  target: 99_MISSING.md
  hop: next
  reason: broken chain
---

# Execution

## 下一跳列表
- [validation]：`99_MISSING.md`
""",
            encoding="utf-8",
        )
        payload = _run_cli("lint-reading-chain", "--target", str(root))
        assert payload["status"] == "error"
