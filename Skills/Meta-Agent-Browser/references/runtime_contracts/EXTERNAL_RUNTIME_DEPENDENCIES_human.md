---
doc_id: meta_agent_browser.references_runtime_contracts_external_runtime_dependencies
doc_type: topic_atom
topic: EXTERNAL_RUNTIME_DEPENDENCIES
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# EXTERNAL_RUNTIME_DEPENDENCIES

Human mirror for `EXTERNAL_RUNTIME_DEPENDENCIES.json`.

```json
{
  "dependency_contract_name": "meta_agent_browser_external_runtime_dependencies",
  "contract_version": "1.0.0",
  "skill_name": "__SKILL_NAME__",
  "manager": "octopus_os_product_installer",
  "dependencies": [
    {
      "dependency_id": "agent-browser",
      "display_name": "agent-browser",
      "install_type": "npm_global_package",
      "install_root": "__WORKSPACE_ROOT__/.product_runtime/external_runtime_dependencies/agent-browser",
      "binary_name": "agent-browser",
      "binary_path": "__WORKSPACE_ROOT__/.product_runtime/external_runtime_dependencies/agent-browser/npm/bin/agent-browser",
      "runtime_env": {
        "PATH_prepend": [
          "__WORKSPACE_ROOT__/.product_runtime/external_runtime_dependencies/agent-browser/npm/bin"
        ],
        "PLAYWRIGHT_BROWSERS_PATH": "__WORKSPACE_ROOT__/.product_runtime/external_runtime_dependencies/agent-browser/ms-playwright",
        "HOME": "__PRODUCT_ROOT__"
      },
      "install_commands": [
        {
          "argv": [
            "npm",
            "install",
            "-g",
            "agent-browser@latest",
            "--prefix",
            "__WORKSPACE_ROOT__/.product_runtime/external_runtime_dependencies/agent-browser/npm"
          ]
        },
        {
          "argv": [
            "__WORKSPACE_ROOT__/.product_runtime/external_runtime_dependencies/agent-browser/npm/bin/agent-browser",
            "install"
          ],
          "env": {
            "PATH_prepend": [
              "__WORKSPACE_ROOT__/.product_runtime/external_runtime_dependencies/agent-browser/npm/bin"
            ],
            "PLAYWRIGHT_BROWSERS_PATH": "__WORKSPACE_ROOT__/.product_runtime/external_runtime_dependencies/agent-browser/ms-playwright",
            "HOME": "__PRODUCT_ROOT__"
          }
        }
      ],
      "validate_commands": [
        {
          "argv": [
            "__WORKSPACE_ROOT__/.product_runtime/external_runtime_dependencies/agent-browser/npm/bin/agent-browser",
            "--version"
          ],
          "env": {
            "PATH_prepend": [
              "__WORKSPACE_ROOT__/.product_runtime/external_runtime_dependencies/agent-browser/npm/bin"
            ],
            "PLAYWRIGHT_BROWSERS_PATH": "__WORKSPACE_ROOT__/.product_runtime/external_runtime_dependencies/agent-browser/ms-playwright",
            "HOME": "__PRODUCT_ROOT__"
          }
        }
      ],
      "required_artifacts": [
        {
          "path": "__WORKSPACE_ROOT__/.product_runtime/external_runtime_dependencies/agent-browser",
          "kind": "dir"
        },
        {
          "path": "__WORKSPACE_ROOT__/.product_runtime/external_runtime_dependencies/agent-browser/npm/bin/agent-browser",
          "kind": "file"
        },
        {
          "path": "__WORKSPACE_ROOT__/.product_runtime/external_runtime_dependencies/agent-browser/ms-playwright",
          "kind": "nonempty_dir"
        }
      ],
      "host_requirements": [
        "The host still needs any OS-level browser libraries required by upstream Playwright or Chromium.",
        "Product-managed install covers the target-local CLI package and browser assets only."
      ],
      "install_help": "If the target-local install fails, rerun the Octopus OS product installer or satisfy the host OS browser prerequisites and retry."
    }
  ]
}
```
