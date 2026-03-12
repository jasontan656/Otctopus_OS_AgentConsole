# Doc Code Binding Rules

适用阶段：`evidence`

## Core Rule

- 文档与代码的绑定依据是语义覆盖单元，不是文件路径相等。
- 一个文档可以绑定一个代码文件，也可以绑定多个代码文件。
- 一个代码模块也可以被上层语义文档统一收束，只要绑定关系显式存在。

## Binding Targets

- `overview/*.md` -> narrative_layer
- `features/*.md` -> narrative_layer / contract_layer
- `shared/*.md` -> contract_layer
- `common/code_abstractions/*.md` -> contract_layer / implementation_layer
- code modules / helpers -> implementation_layer
- witness / logs -> evidence_layer

## Output Rule

- 绑定关系既要可供机械读取，也要能在 Admin 界面中可视化展示。
- evidence 写回时，必须把新 witness 绑定回已存在的文档节点与代码节点，不得悬空。
