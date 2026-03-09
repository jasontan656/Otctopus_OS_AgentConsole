# Authored Domain Index

适用技能：`2-Octupos-FullStack`

## Purpose

- This index groups authored product-domain rule families.
- Each family owns its own writing rules, implementation rules, and development canon automation scope.
- Do not collapse all authored domains into a single `mother_doc` rule set.

## Families

- `mother_doc`
- `ui`
- `gateway`
- `service`
- `data_infra`

## Loading Rule

- implementation must first load the matching domain family rules.
- Then load the target container's `common/` documents under `Octopus_OS/Mother_Doc/docs/<Container_Name>/`.
