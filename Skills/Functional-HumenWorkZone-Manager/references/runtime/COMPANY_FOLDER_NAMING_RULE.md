---
doc_id: functional_humenworkzone_manager.runtime.company_folder_naming_rule
doc_type: topic_atom
topic: Naming rule for company-document folders
anchors:
- target: COMPANY_DOCUMENTS_ZONE_POLICY.md
  relation: implements
  direction: upstream
  reason: Naming is a governed part of the company-document zone.
- target: ORGANIZE_COMPANY_DOCUMENTS_FLOW.md
  relation: required_by
  direction: upstream
  reason: Intake needs a naming decision before relocation.
- target: COMPANY_DOCUMENTS_README_MAINTENANCE_FLOW.md
  relation: referenced_by
  direction: upstream
  reason: Inventory entries should align with this naming rule.
---

# Company Folder Naming Rule

## 固定格式
- 公司目录统一使用：`Company_<CompanyCore>_<Scope>/`。

## 命名解释
- `<CompanyCore>` 使用英文短语表达公司主识别名。
- `<Scope>` 使用英文短语表达该目录的主要资料范围，例如：`Operations`、`Project_Records`、`Business_Permit_Tax_Docs`。

## 兼容规则
- 若目录原本已经符合 `Company_` 前缀形态且可读性足够，迁入时允许保留原名。
- 若目录缺少 `Company_` 前缀，或公司名不明显，应在迁入时改到统一格式。

## 当前明确示例
- `Company_Bawang_King_Garlic_Product_Operations`
- `Company_Wyc_Funtrip_Travel_Operations`
- `Company_Haiyou_Business_Permit_Tax_Docs`

## 禁止项
- 不要把公司目录继续保留成完全看不出公司名的散乱名字。
- 不要为了收纳而创造业务语义过强的新命名；当前阶段只需要“看得出是哪家公司、装哪类资料”。
