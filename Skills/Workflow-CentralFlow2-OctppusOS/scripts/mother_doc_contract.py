from __future__ import annotations

# contract_name: octopus_devflow_mother_doc_contract
# contract_version: 6.0.0
# validation_mode: strict
# required_fields:
#   - MOTHER_DOC_ROOT_REQUIRED_FILES
#   - MOTHER_DOC_REQUIRED_ENTRY_ALTERNATIVES
#   - MOTHER_DOC_FRONTMATTER_REQUIRED_FIELDS
#   - MOTHER_DOC_FRONTMATTER_OPTIONAL_FIELDS
#   - MOTHER_DOC_ANCHOR_FIELDS
#   - MOTHER_DOC_WORK_STATES
#   - MOTHER_DOC_STATE_TRANSITIONS
#   - MOTHER_DOC_ALLOWED_DOC_ROLES
#   - MOTHER_DOC_REQUIRED_ROOT_INDEX_RULES
#   - MOTHER_DOC_REQUIRED_DESIGN_PLAN_ROLE
#   - MOTHER_DOC_REQUIRED_STAGE_IDS
#   - MOTHER_DOC_STAGE_PLAN_MARKERS
#   - MOTHER_DOC_GUIDANCE_MARKERS
#   - MOTHER_DOC_FILE_BASENAME_PATTERN
#   - MOTHER_DOC_DIRECTORY_NAME_PATTERN
#   - MOTHER_DOC_HEADING_MAX_DEPTH
# optional_fields: []

MOTHER_DOC_ROOT_REQUIRED_FILES = [
    "00_index.md",
]

MOTHER_DOC_REQUIRED_ENTRY_ALTERNATIVES = {
    "root_index": ["00_index.md"],
}

MOTHER_DOC_ANCHOR_FIELDS = [
    "anchors_down",
    "anchors_support",
]

MOTHER_DOC_DISPLAY_LAYERS = [
    "overview",
    "entry",
    "resolution",
    "capability",
    "support",
]

MOTHER_DOC_DISPLAY_LAYER_ORDER = {
    "overview": 0,
    "entry": 1,
    "resolution": 2,
    "capability": 3,
    "support": 4,
}

MOTHER_DOC_FORBIDDEN_FRONTMATTER_FIELDS = [
    "layer",
    "anchors_up",
    "anchors_right",
    "anchors_left",
]

MOTHER_DOC_FRONTMATTER_REQUIRED_FIELDS = [
    "doc_work_state",
    "doc_pack_refs",
    "doc_kind",
    "content_family",
    "thumb_title",
    "thumb_summary",
    "display_layer",
    "always_read",
    *MOTHER_DOC_ANCHOR_FIELDS,
]

MOTHER_DOC_FRONTMATTER_OPTIONAL_FIELDS = [
    "doc_role",
    "branch_family",
]

MOTHER_DOC_WORK_STATES = [
    "modified",
    "planned",
    "developed",
    "ref",
]

MOTHER_DOC_STATE_TRANSITIONS = {
    "modified": ["planned"],
    "planned": ["modified", "developed"],
    "developed": ["modified", "ref"],
    "ref": ["modified"],
}

MOTHER_DOC_ALLOWED_DOC_ROLES = [
    "root_index",
    "design_plan",
]

MOTHER_DOC_ALLOWED_DOC_KINDS = [
    "trunk_node",
    "branch_root",
    "taxonomy_doc",
    "contract_doc",
    "scene_spec",
    "interaction_spec",
    "decision_doc",
    "execution_binding_doc",
]

MOTHER_DOC_ALLOWED_BRANCH_FAMILIES = [
    "framework_branch",
    "domain_branch",
    "contract_branch",
    "scene_branch",
    "interaction_branch",
    "decision_branch",
    "execution_binding_branch",
]

MOTHER_DOC_ALLOWED_CONTENT_FAMILIES = [
    "root_index_auto",
    "overview_narrative",
    "overview_mapping",
    "branch_overview",
    "layer_taxonomy_root",
    "layer_item_doc",
    "container_item_doc",
    "contract_spec_doc",
]

MOTHER_DOC_CONTENT_FAMILY_REQUIRED_HEADINGS = {
    "root_index_auto": [
        "## 当前职责",
        "## 自动目录结构图",
        "## 自动目录清单",
        "## 根入口约束",
    ],
    "overview_narrative": [
        "## 来源",
        "## 当前节点职责",
        "## 当前内容",
    ],
    "overview_mapping": [
        "## 来源",
        "## 当前节点职责",
        "## 当前内容",
    ],
    "branch_overview": [
        "## 来源",
        "## 当前节点职责",
        "## 当前内容",
        "## 当前延伸规则",
    ],
    "layer_taxonomy_root": [
        "## 来源",
        "## 当前节点职责",
        "## 当前内容",
        "## 当前延伸规则",
    ],
    "layer_item_doc": [
        "## 来源",
        "## 当前节点职责",
        "## 当前内容",
        "## 当前延伸边界",
    ],
    "container_item_doc": [
        "## 来源",
        "## 当前节点职责",
        "## 当前内容",
        "## 当前承载边界",
    ],
    "contract_spec_doc": [
        "## 来源",
        "## 当前节点职责",
        "## 当前规则",
        "## 当前配置",
    ],
}

MOTHER_DOC_REQUIRED_ROOT_INDEX_RULES = {
    "relative_path": "00_index.md",
    "doc_role": "root_index",
    "always_read": True,
    "anchor_fields_must_be_empty": True,
}

MOTHER_DOC_REQUIRED_DESIGN_PLAN_ROLE = "design_plan"

MOTHER_DOC_REQUIRED_STAGE_IDS = [
    "mother_doc",
    "construction_plan",
    "implementation",
    "acceptance",
]

MOTHER_DOC_STAGE_PLAN_MARKERS = [
    "stage_id",
    "stage_goal",
    "stage_assertions",
    "stage_tests",
    "stage_exit_evidence",
]

MOTHER_DOC_GUIDANCE_MARKERS = [
    "fill_rule:",
    "Replace every replace_me token",
    "Remove this guidance block after drafting.",
]

MOTHER_DOC_FILE_BASENAME_PATTERN = r"^(00_index|\d{2}_[a-z0-9_]+|ADR_TEMPLATE)\.md$"
MOTHER_DOC_DIRECTORY_NAME_PATTERN = (
    r"^(\d{2}_[a-z0-9_]+|acceptance|execution_atom_plan_validation_packs|graph|12_adrs)$"
)
MOTHER_DOC_HEADING_MAX_DEPTH = 4
