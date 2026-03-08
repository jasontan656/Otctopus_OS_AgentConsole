# L2 Tool-Doc Packet: chain_usage_contract_backfill

## Source
- from_l1: `docs/L1/chains/chain_usage_contract_backfill.md`
- chain_id: `chain_usage_contract_backfill`

## Objective
为每个工具补齐可执行的使用文档（命令示例、输入输出、锚点映射），让接手者可直接运行。

## Tool Coverage
- managed_tool_count: `25`
- tool_source: `runtime/TOOL_REGISTRY.yaml`

## Required Tool Doc Sections
- usage: command_examples / inputs / outputs / script_anchor_refs / doc_anchor_refs
- modification: update_workflow / required_docs / sync_contract
- development: owner / self_evolution_requirements / records

## Packets
- m1: `m1_usage_command_examples`
- m2: `m2_usage_inputs_outputs`
- m3: `m3_usage_doc_anchor_binding`
- m4: `m4_usage_nonempty_validation`
- m5: `m5_usage_contract_gate`

## Closure Contract
- final_layer: `L13`
- required_evidence_ref: `docs/L13/README.md#验收证据与闭环归档`
