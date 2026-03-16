from __future__ import annotations

from scaffold_models import ProfileCatalogEntry, SkillProfile


SUPPORTED_PROFILES = (
    {
        "name": "inline_minimal",
        "profile": SkillProfile("inline", "none", "advisory"),
        "recommended_for": "thin facade or tiny advisory skill",
    },
    {
        "name": "referenced_contract",
        "profile": SkillProfile("referenced", "contract_cli", "guardrailed"),
        "recommended_for": "governance skill with referenced documents and static contract entry",
    },
    {
        "name": "referenced_automation",
        "profile": SkillProfile("referenced", "automation_cli", "guardrailed"),
        "recommended_for": "governance skill that needs referenced docs and active CLI actions",
    },
    {
        "name": "workflow_contract",
        "profile": SkillProfile("workflow_path", "contract_cli", "compiled"),
        "recommended_for": "compiled workflow skill with minimal automation",
    },
    {
        "name": "workflow_automation",
        "profile": SkillProfile("workflow_path", "automation_cli", "compiled"),
        "recommended_for": "compiled workflow skill with action commands",
    },
)

DEFAULT_PROFILE = SUPPORTED_PROFILES[1]["profile"]


def list_profiles() -> list[ProfileCatalogEntry]:
    payload: list[ProfileCatalogEntry] = []
    for item in SUPPORTED_PROFILES:
        payload.append(
            {
                "name": item["name"],
                "profile": item["profile"].as_dict(),
                "recommended_for": item["recommended_for"],
            }
        )
    return payload


def is_supported(profile: SkillProfile) -> bool:
    return any(item["profile"] == profile for item in SUPPORTED_PROFILES)
