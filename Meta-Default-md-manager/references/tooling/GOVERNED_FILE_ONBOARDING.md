# Governed File Onboarding

## Purpose
- This document defines only the maintenance workflow for adding a new governed file into `Meta-Default-md-manager`.
- It does not redefine runtime contracts, stage semantics, or AGENTS asset governance.

## Entry Rule
- Skill maintenance in this manager is primarily the work of adding new governed files and the matching support around them.
- Script changes, lint changes, scan rule changes, and asset updates are treated as supporting work for that onboarding task, not as isolated maintenance with hidden scope.

## Onboarding Workflow
1. Add the governed file template under the skill-managed asset tree.
2. Keep the managed target path aligned one-to-one with the external governed target path and filename.
3. Let the user define and refine the target file shape and content during governance; do not freeze the target shape before that user-driven correction happens.
4. After the user finishes governing the file structure and content, add the matching lint, add or update the required tools, and update the supporting tool assets.
5. Validate that every dry-run result matches the user's governance expectation before any real overwrite is accepted.
6. Sync the mirror skill and installed skill together, then complete repo traceability for the supporting changes.

## Required Coupling
- A newly governed filename must have a matching structure template before scan/lint may accept it.
- Managed asset paths, lint coverage, scan rules, collect behavior, push behavior, and user-facing references must be updated together when a new governed file is introduced.
- If a user request changes the intended target shape, update the managed template and every supporting contract or tool surface that depends on that shape.

## Boundary
- This document does not define the exact runtime payload of any governed file.
- This document does not define the concrete collect or push semantics beyond the onboarding coupling required to support a newly governed target.
- Stage-specific behavior still belongs to the dedicated stage documents.
