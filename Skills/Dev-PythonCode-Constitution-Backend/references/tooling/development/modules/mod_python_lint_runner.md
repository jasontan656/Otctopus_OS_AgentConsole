---
doc_id: "dev_pythoncode_constitution_backend.tooling.module.python_lint_runner"
doc_type: "topic_atom"
topic: "Implementation notes for the Python lint runner"
anchors:
  - target: "../20_CATEGORY_INDEX.md"
    relation: "implements"
    direction: "upstream"
    reason: "The category index routes readers into this module doc."
  - target: "../90_CHANGELOG.md"
    relation: "pairs_with"
    direction: "lateral"
    reason: "Changes to the lint runner should be tracked in the changelog."
---

# python_lint_runner 模块文档

## 模块标识
- `module_id`: `python_lint_runner`
- `tool_alias`: `Cli_Toolbox.run_python_code_lints`
- `entrypoint`: `scripts/run_python_code_lints.py`

## 职责
- 对目标目录执行 Python 代码治理静态 lint。
- 输出统一 JSON 报告，并在任一 gate 失败时返回非零退出码。

## 输入输出契约
- 输入：`--target <target_root>`
- 输出：单个 JSON 对象，包含 `target/gates/summary/summary_enhanced/gate_diagnostics/violation_details/clusters`
- 失败模式：任一 gate 失败或参数非法时返回非零退出码
- 扫描边界：显式排除虚拟环境、构建/缓存与临时目录，避免对 `.venv*`、`venv*`、`node_modules/`、`build/`、`dist/`、`coverage/`、`tmp/`、`temp/`、`.tmp*`、`.temp*` 等非治理源码目录误报

## 回归检查
```bash
cd /home/jasontan656/AI_Projects/octopus-os-agent-console/Skills/Dev-PythonCode-Constitution-Backend && python3 -m pytest tests/test_python_code_lints.py
```
