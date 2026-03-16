from __future__ import annotations

from profile_registry import DEFAULT_PROFILE, is_supported, list_profiles
from scaffold_models import ProfileCatalogPayload, ScaffoldRequest, ScaffoldResultPayload, SkillProfile
from scaffold_renderer import render_files
from scaffold_writer import write_files


def profile_catalog_payload() -> ProfileCatalogPayload:
    return {
        "status": "ok",
        "default_profile": DEFAULT_PROFILE.as_dict(),
        "profiles": list_profiles(),
    }


def build_profile(doc_topology: str, tooling_surface: str, workflow_control: str) -> SkillProfile:
    profile = SkillProfile(doc_topology, tooling_surface, workflow_control)
    if not is_supported(profile):
        raise ValueError(f"unsupported profile combination: {profile.key()}")
    return profile


def scaffold_skill(request: ScaffoldRequest) -> ScaffoldResultPayload:
    files = render_files(request)
    written = write_files(request.skill_root, files, overwrite=request.overwrite)
    return {
        "status": "ok",
        "skill_root": str(request.skill_root),
        "profile": request.profile.as_dict(),
        "written_files": written,
    }
