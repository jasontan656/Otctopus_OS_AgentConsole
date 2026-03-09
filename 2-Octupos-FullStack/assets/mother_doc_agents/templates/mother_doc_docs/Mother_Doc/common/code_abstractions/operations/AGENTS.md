[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]

`HOOK_LOAD`: Apply this AGENTS contract. This file is a thin runtime entry that points to the skill-managed CLI/JSON rule source.

[TURN START - MANDATORY]

1. Load Target Contract
- Must run this command before following any path-specific rule:
- `python3 /home/jasontan656/AI_Projects/Codex_Skills_Mirror/2-Octupos-FullStack/scripts/Cli_Toolbox.py mother-doc-agents-target-contract --relative-path "mother_doc_docs/Mother_Doc/common/code_abstractions/operations" --file-kind agents --json`

2. TURN_START Contract
- N/A

3. Peer Read Gate
- See the returned `peer_doc` object to decide whether the same-level peer file must be read.

[EXECUTION - MANDATORY]

4. Runtime Rule Source
- The returned JSON is the runtime rule source for this path.
- Skill-internal markdown audit files are for human audit only; models must not treat them as runtime guidance.

5. Routing
- Use the returned `routing` and `update_boundary` fields instead of reading extra markdown for runtime rules.

[TURN END - MANDATORY]

6. TURN_END Contract
- N/A
