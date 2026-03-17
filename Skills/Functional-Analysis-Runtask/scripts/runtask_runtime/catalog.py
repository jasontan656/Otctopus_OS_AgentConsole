from __future__ import annotations

from pathlib import Path
import re

from .types import RuntimeContractPayload, StageChecklistPayload, StageMetadata


SKILL_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = SKILL_ROOT.parents[1]
AI_PROJECTS_ROOT = REPO_ROOT.parent
MANAGED_ROOT_ENV = "FUNCTIONAL_ANALYSIS_RUNTASK_MANAGED_ROOT"
TASK_RUNTIME_ROOT_ENV = "FUNCTIONAL_ANALYSIS_RUNTASK_TASK_RUNTIME_ROOT"
DEFAULT_MANAGED_ROOT = AI_PROJECTS_ROOT / "Human_Work_Zone"
DEFAULT_TASK_RUNTIME_ROOT = AI_PROJECTS_ROOT / "Codex_Skill_Runtime" / "Functional-Analysis-Runtask"
HUMENWORKZONE_COMMANDS = {
    "contract": "./.venv_backend_skills/bin/python Skills/Functional-HumenWorkZone-Manager/scripts/Cli_Toolbox.py contract --json",
    "task_routing": "./.venv_backend_skills/bin/python Skills/Functional-HumenWorkZone-Manager/scripts/Cli_Toolbox.py directive --topic task-routing --json",
    "execution_boundary": "./.venv_backend_skills/bin/python Skills/Functional-HumenWorkZone-Manager/scripts/Cli_Toolbox.py directive --topic execution-boundary --json",
    "paths": "./.venv_backend_skills/bin/python Skills/Functional-HumenWorkZone-Manager/scripts/Cli_Toolbox.py paths --json",
}
STAGE_ORDER = [
    "research",
    "architect",
    "preview",
    "design",
    "impact",
    "plan",
    "implementation",
    "validation",
    "final_delivery",
]
STAGE_STATUS_VALUES = {"pending", "in_progress", "blocked", "completed"}
PACKAGE_STATUS_VALUES = {"queued", "active", "blocked", "completed"}
TASK_STATUS_VALUES = {"in_progress", "awaiting_user_selection", "blocked", "closed"}
ACTION_TYPES = {"implementation", "validation", "phase_decision", "state_writeback"}
DESIGN_DECISION_MODES = {"rewrite", "replace", "add"}
REMOTE_PREFIXES = ("http://", "https://")
NUMBERED_SLOT_RE = re.compile(r"^(?P<prefix>\d{3})_(?P<slug>[a-z0-9][a-z0-9_]*)$")

WORKSPACE_LAYOUT = {
    "manifest": "workspace_manifest.yaml",
    "evidence_registry": "research/evidence_registry.yaml",
    "architect_assessment": "architect/assessment.yaml",
    "preview_projection": "preview/projection.yaml",
    "design_decisions": "design/decisions.yaml",
    "impact_map": "impact/impact_map.yaml",
    "milestone_packages": "plan/milestone_packages.yaml",
    "implementation_ledger": "implementation/turn_ledger.yaml",
}

STAGE_ARTIFACTS = {
    "research": "research/001_research_report.md",
    "architect": "architect/001_architecture_assessment_report.md",
    "preview": "preview/001_future_shape_preview.md",
    "design": "design/001_design_strategy.md",
    "impact": "impact/001_impact_investigation.md",
    "plan": WORKSPACE_LAYOUT["milestone_packages"],
    "implementation": WORKSPACE_LAYOUT["implementation_ledger"],
    "validation": "validation/001_acceptance_report.md",
    "final_delivery": "final_delivery/001_final_delivery_brief.md",
}

STAGE_UPSTREAM_REPORTS = {
    "research": [],
    "architect": [STAGE_ARTIFACTS["research"]],
    "preview": [STAGE_ARTIFACTS["research"], STAGE_ARTIFACTS["architect"]],
    "design": [STAGE_ARTIFACTS["research"], STAGE_ARTIFACTS["architect"], STAGE_ARTIFACTS["preview"]],
    "impact": [STAGE_ARTIFACTS["research"], STAGE_ARTIFACTS["architect"], STAGE_ARTIFACTS["preview"], STAGE_ARTIFACTS["design"]],
    "plan": [STAGE_ARTIFACTS["research"], STAGE_ARTIFACTS["architect"], STAGE_ARTIFACTS["preview"], STAGE_ARTIFACTS["design"], STAGE_ARTIFACTS["impact"]],
    "implementation": [
        STAGE_ARTIFACTS["research"],
        STAGE_ARTIFACTS["architect"],
        STAGE_ARTIFACTS["preview"],
        STAGE_ARTIFACTS["design"],
        STAGE_ARTIFACTS["impact"],
        STAGE_ARTIFACTS["plan"],
    ],
    "validation": [
        STAGE_ARTIFACTS["research"],
        STAGE_ARTIFACTS["architect"],
        STAGE_ARTIFACTS["preview"],
        STAGE_ARTIFACTS["design"],
        STAGE_ARTIFACTS["impact"],
        STAGE_ARTIFACTS["plan"],
        STAGE_ARTIFACTS["implementation"],
    ],
    "final_delivery": [
        STAGE_ARTIFACTS["research"],
        STAGE_ARTIFACTS["architect"],
        STAGE_ARTIFACTS["preview"],
        STAGE_ARTIFACTS["design"],
        STAGE_ARTIFACTS["impact"],
        STAGE_ARTIFACTS["plan"],
        STAGE_ARTIFACTS["implementation"],
        STAGE_ARTIFACTS["validation"],
    ],
}

STAGE_REQUIRED_SECTIONS = {
    "research": [
        "调研目标与范围",
        "输入资产与当前前提",
        "问题框架与强制追问",
        "证据登记",
        "显式推导链",
        "阶段结论",
        "未收口问题与进入 architect 的门禁",
    ],
    "architect": [
        "阶段目标",
        "消费的前序产物",
        "关键架构问题框架",
        "should change",
        "should not change",
        "架构判断推导链",
        "阶段结论与进入 preview 的门禁",
    ],
    "preview": [
        "阶段目标",
        "消费的前序产物",
        "关键预演问题框架",
        "future shape",
        "behavior delta",
        "failure modes",
        "rollback triggers",
        "预演推导链与进入 design 的门禁",
    ],
    "design": [
        "阶段目标",
        "消费的前序产物",
        "关键设计问题框架",
        "候选路径与取舍",
        "设计推导链",
        "selected strategy",
        "写回对象与进入 impact 的门禁",
    ],
    "impact": [
        "阶段目标",
        "消费的前序产物",
        "关键影响面问题框架",
        "direct scope",
        "indirect scope",
        "latent related",
        "regression surface",
        "影响面推导链与进入 plan 的门禁",
    ],
    "plan": [],
    "implementation": [],
    "validation": [
        "阶段目标",
        "消费的前序产物",
        "验收问题框架",
        "验收执行与成功反馈",
        "残余风险与可接受副作用",
        "验收推导链",
        "阶段结论与进入 final_delivery 的门禁",
    ],
    "final_delivery": [
        "交付目标",
        "消费的前序产物",
        "对人类的最终结论",
        "关键承接链摘要",
        "剩余风险与后续观察点",
    ],
}

STAGE_TITLES = {
    "research": "Research Report",
    "architect": "Architecture Assessment Report",
    "preview": "Future Shape Preview",
    "design": "Design Strategy",
    "impact": "Impact Investigation",
    "validation": "Acceptance Report",
    "final_delivery": "Final Delivery Brief",
}

STAGES: dict[str, StageMetadata] = {
    "research": {
        "purpose": "调研目标项目或目标意图，并落盘调研报告。",
        "entry_requirements": [
            "明确目标意图、目标项目与本地落地对象。",
            "通过 Functional-HumenWorkZone-Manager 解析受管落点。",
            "新任务已经通过 task gate，并已生成 task_runtime.yaml。",
            "必须先整理未收口问题链、需要追问的缺口与默认全相关起始判断，再进入证据采样。",
        ],
        "required_objects": [WORKSPACE_LAYOUT["manifest"], WORKSPACE_LAYOUT["evidence_registry"]],
        "required_artifacts": [STAGE_ARTIFACTS["research"]],
        "writeback_targets": [
            WORKSPACE_LAYOUT["manifest"],
            WORKSPACE_LAYOUT["evidence_registry"],
            STAGE_ARTIFACTS["research"],
        ],
        "lint_focus": [
            "manifest/source_assets/evidence_registry",
            "research question density and follow-up chain",
            "research report section completeness",
        ],
        "question_framework": [
            "目标意图是否已被单句固定，是否仍混杂多个问题或多个对象。",
            "当前分析范围、排除范围、默认全相关起始判断是否已经写清。",
            "缺少哪些路径、版本、运行方式、输入条件或用户裁决会直接让后续阶段建立在错前提上。",
            "哪些未收口问题必须先追问，哪些可以带着显式假设进入后续阶段。",
        ],
        "derivation_chain": [
            "先锁定目标、范围、排除项与问题链，再登记 source assets 与 evidence registry。",
            "research report 必须把问题框架、证据、推导链、当前结论与未收口问题写透。",
            "只有当 architect 能直接引用 research report 继续推导时，research 才能结束。",
        ],
        "stage_blockers": [
            "不得只写结论不写问题框架、证据入口和显式推导链。",
            "不得把 architect/design/impact 的判断偷渡成 research 完成态。",
            "不得跳过用户追问与未收口问题整理。",
        ],
        "required_upstream_reports": STAGE_UPSTREAM_REPORTS["research"],
        "required_sections": STAGE_REQUIRED_SECTIONS["research"],
    },
    "architect": {
        "purpose": "强制使用 Meta-Architect-MindModel，对当前结构与目标结构给出应/应否评估并落盘。",
        "entry_requirements": [
            "research 已完成且 research report/evidence registry 已可直接引用。",
            "architect 只消费 research 产物，不得提前写 design/impact/plan 结论。",
            "必须先承认 research 中仍未收口的问题，并明确哪些前提已足够支撑架构裁决。",
        ],
        "required_objects": [
            WORKSPACE_LAYOUT["manifest"],
            WORKSPACE_LAYOUT["evidence_registry"],
            WORKSPACE_LAYOUT["architect_assessment"],
        ],
        "required_artifacts": [STAGE_ARTIFACTS["research"], STAGE_ARTIFACTS["architect"]],
        "writeback_targets": [WORKSPACE_LAYOUT["architect_assessment"], STAGE_ARTIFACTS["architect"]],
        "lint_focus": [
            "architect question framework and judgement chain",
            "architect assessment should/should_not",
            "explicit reference to research report",
        ],
        "question_framework": [
            "哪些结构边界必须改变，否则后续阶段都会建立在错误架构上。",
            "哪些现有结构必须保留，否则会破坏既有稳定性或证据链。",
            "哪些判断仍停留在 research 证据不足，不能在 architect 阶段伪装成已裁决。",
            "如果现在做错架构裁决，preview/design/impact 会分别被怎样误导。",
        ],
        "derivation_chain": [
            "architect report 必须逐条引用 research report 与 evidence registry，再写 should change / should not change。",
            "assessment.yaml 必须把问题框架、判断链、未收口问题与 evidence refs 固定为对象层真相源。",
            "preview 只能从 architect 的正式判断继续推演，不能回到聊天摘要里自由发挥。",
        ],
        "stage_blockers": [
            "不得输出代码级实现步骤、文件级施工切片或回归矩阵。",
            "不得绕过 research report 直接给主观架构喜好。",
            "不得在 research 未完成时把 architect 标成 completed。",
        ],
        "required_upstream_reports": STAGE_UPSTREAM_REPORTS["architect"],
        "required_sections": STAGE_REQUIRED_SECTIONS["architect"],
    },
    "preview": {
        "purpose": "强制使用 Meta-Reasoning-Chain，输出未来形态、行为变化、失败模式与回滚阈值。",
        "entry_requirements": [
            "architect 已完成，且 architect report 已明确 should change / should_not_change。",
            "preview 只消费 research 与 architect 产物，不直接定义实现策略。",
            "必须把未来形态推演、行为变化、失败模式和回滚阈值分别写清，不能用一句泛论收掉。",
        ],
        "required_objects": [WORKSPACE_LAYOUT["manifest"], WORKSPACE_LAYOUT["preview_projection"]],
        "required_artifacts": [STAGE_ARTIFACTS["architect"], STAGE_ARTIFACTS["preview"]],
        "writeback_targets": [WORKSPACE_LAYOUT["preview_projection"], STAGE_ARTIFACTS["preview"]],
        "lint_focus": [
            "preview question framework and reasoning chain",
            "future_shape/behavior_delta/failure_modes/rollback_triggers",
            "explicit reference to research and architect reports",
        ],
        "question_framework": [
            "如果 architect 判断成立，最终形态在结构、行为、失败模式上会如何变化。",
            "哪些 preview 结论只是预测，不得偷渡成 design 或 implementation 决策。",
            "哪些 failure modes 一旦忽略，会让 design 方案看似可行但实际上无回滚路径。",
            "哪些 rollback triggers 必须写死，才能让后续阶段知道何时停止推进。",
        ],
        "derivation_chain": [
            "preview report 必须逐条承接 research 与 architect 报告，而不是重新发明目标态。",
            "projection.yaml 必须把问题框架、推导链、future shape、failure modes 与 evidence refs 写成对象层真相源。",
            "design 只能消费 preview 已落盘的未来形态判断，不能自行补写 preview。",
        ],
        "stage_blockers": [
            "不得在 preview 阶段输出具体改文件步骤或 package 拆分。",
            "不得跳过 rollback triggers。",
            "不得把 impact/validation 的结论提前写进 preview。",
        ],
        "required_upstream_reports": STAGE_UPSTREAM_REPORTS["preview"],
        "required_sections": STAGE_REQUIRED_SECTIONS["preview"],
    },
    "design": {
        "purpose": "强制使用 Meta-keyword-first-edit，独立落盘优雅实现目标形态的设计方案。",
        "entry_requirements": [
            "architect 与 preview 已完成，且 research/architect/preview 三份报告都已可引用。",
            "design 只消费前序正式产物，不得把 architect/preview/impact 偷渡回设计阶段补写。",
            "必须先问透设计问题、候选路径与放弃路径，再进入 selected strategy。",
        ],
        "required_objects": [WORKSPACE_LAYOUT["manifest"], WORKSPACE_LAYOUT["design_decisions"]],
        "required_artifacts": [STAGE_ARTIFACTS["design"]],
        "writeback_targets": [WORKSPACE_LAYOUT["design_decisions"], STAGE_ARTIFACTS["design"]],
        "lint_focus": [
            "design question framework and decision chain",
            "design decision mode/seamless state",
            "explicit reference to research/architect/preview reports",
        ],
        "question_framework": [
            "为满足 architect judgement 与 preview projection，当前最小可行设计面是什么。",
            "有哪些候选路径被评估过，为什么被保留、推翻或升级。",
            "哪些设计决定若不显式写回，plan 和 implementation 就会退化成主观施工。",
            "哪些约束来自前序报告，哪些约束是 design 新增的实施边界。",
        ],
        "derivation_chain": [
            "design report 必须写清问题框架、候选路径、取舍链和 selected strategy。",
            "decisions.yaml 必须逐条引用前序 stage reports 与 evidence refs，不能只写偏好。",
            "impact 与 plan 只能从 design 已裁决方案继续，不允许回头补写 architect/preview。",
        ],
        "stage_blockers": [
            "不得跳过候选路径与放弃理由，直接落单一方案。",
            "不得预写 impact/plan/implementation 的内容。",
            "不得用 generic rewrite/replace/add 词汇代替真实设计判断。",
        ],
        "required_upstream_reports": STAGE_UPSTREAM_REPORTS["design"],
        "required_sections": STAGE_REQUIRED_SECTIONS["design"],
    },
    "impact": {
        "purpose": "强制使用 Meta-Impact-Investigation，补齐 direct/indirect/latent/regression 影响面。",
        "entry_requirements": [
            "design 已完成，且 design report 已明确 selected strategy 与取舍链。",
            "impact 只消费 research/architect/preview/design 前序产物，不得混入 implementation 结果。",
            "必须把 direct/indirect/latent/regression 四类影响面分别问透、写透。",
        ],
        "required_objects": [WORKSPACE_LAYOUT["manifest"], WORKSPACE_LAYOUT["impact_map"]],
        "required_artifacts": [STAGE_ARTIFACTS["impact"]],
        "writeback_targets": [WORKSPACE_LAYOUT["impact_map"], STAGE_ARTIFACTS["impact"]],
        "lint_focus": [
            "impact question framework and judgement chain",
            "impact map scopes",
            "explicit reference to research/architect/preview/design reports",
        ],
        "question_framework": [
            "这次设计变更会直接影响哪些对象、间接拖动哪些对象、可能遗漏哪些无锚点关联。",
            "哪些验证路径、证据入口和回归面必须提前写死，才能约束后续 plan/implementation。",
            "哪些对象暂时不改但必须检查，理由是什么。",
            "如果 impact 没写透，plan 会在哪些地方错误缩小施工面。",
        ],
        "derivation_chain": [
            "impact report 必须逐条承接 design 与更早阶段报告，说明每个影响面的来源。",
            "impact_map.yaml 必须把问题框架、判断链、evidence refs、confidence 与 evidence gaps 固定下来。",
            "plan 只能消费 impact 已落盘的 direct/indirect/latent/regression 结论，不能自己补影响面。",
        ],
        "stage_blockers": [
            "不得把 implementation 结果或 validation 结论倒灌进 impact。",
            "不得只给一份简短范围列表而省略判断链和证据链。",
            "不得跳过 latent_related 与 regression_surface。",
        ],
        "required_upstream_reports": STAGE_UPSTREAM_REPORTS["impact"],
        "required_sections": STAGE_REQUIRED_SECTIONS["impact"],
    },
    "plan": {
        "purpose": "把目标拆成可逐步修改、逐步验证的 milestone package。",
        "entry_requirements": [
            "impact 已完成，且 impact report 已明确 must_update / must_check_before_edit / regression_surface。",
            "plan 只消费 research/architect/preview/design/impact 正式产物，不得补写前序判断。",
            "每个 package 都必须说明为什么这样拆、依赖哪些阶段报告、如何验证与如何写回。",
        ],
        "required_objects": [WORKSPACE_LAYOUT["manifest"], WORKSPACE_LAYOUT["milestone_packages"]],
        "required_artifacts": [STAGE_ARTIFACTS["plan"]],
        "writeback_targets": [WORKSPACE_LAYOUT["milestone_packages"]],
        "lint_focus": [
            "planning basis and package derivation chain",
            "milestone package fields",
            "explicit reference to prior stage reports",
        ],
        "question_framework": [
            "当前设计与影响面结论应该拆成哪些 package 才能逐步实现、逐步验证、逐步回写。",
            "每个 package 消费什么、交付什么、退出条件是什么、失败后如何停住。",
            "哪些 package 看似能合并，但会破坏证据链或回滚边界。",
            "哪些写回动作必须与 package 同回合发生，不能留到最后统一补写。",
        ],
        "derivation_chain": [
            "plan 必须先把 planning basis 写进对象层，再逐个生成 package。",
            "每个 package 都必须显式引用前序 stage reports，并给出 stage gates、writeback targets、evidence expectations 与 exit signals。",
            "implementation 只允许消费 active package 与其引用的前序正式产物。",
        ],
        "stage_blockers": [
            "不得把 plan 退化成泛泛 TODO 列表。",
            "不得跳过 package derivation chain、验证方法或写回要求。",
            "不得在没有 impact 正式结论时直接开 implementation。",
        ],
        "required_upstream_reports": STAGE_UPSTREAM_REPORTS["plan"],
        "required_sections": STAGE_REQUIRED_SECTIONS["plan"],
    },
    "implementation": {
        "purpose": "按 milestone package 逐个实现，并持续回写证据、checklist 与状态裁决。",
        "entry_requirements": [
            "plan 已存在 active milestone package，且该 package 已声明 stage gates、writeback targets、evidence expectations 与 exit signals。",
            "implementation 只消费 active package 与其显式引用的前序正式产物。",
            "每次真实施工前都必须先写 preflight checks，明确本回合承接的是哪组阶段结论。",
        ],
        "required_objects": [
            WORKSPACE_LAYOUT["manifest"],
            WORKSPACE_LAYOUT["milestone_packages"],
            WORKSPACE_LAYOUT["implementation_ledger"],
        ],
        "required_artifacts": [STAGE_ARTIFACTS["implementation"]],
        "writeback_targets": [WORKSPACE_LAYOUT["implementation_ledger"], WORKSPACE_LAYOUT["manifest"]],
        "lint_focus": [
            "implementation preflight and derivation notes",
            "ledger/package/evidence linkage",
            "explicit reference to prior stage reports",
        ],
        "question_framework": [
            "当前 active package 的边界、禁止越界项、必须同步写回项和退出信号是什么。",
            "本回合实际修改是否仍严格承接前序 reports，而不是临时发散成新方案。",
            "哪些实现行为需要立刻跑验证，哪些验证结果必须当回合落入 ledger。",
            "哪些残余问题会阻止 package 进入 completed。",
        ],
        "derivation_chain": [
            "每条 ledger entry 都必须写清 consumed stage reports、preflight checks、derivation notes、changed paths 与 evidence refs。",
            "任何实现、验证、状态更新和写回都必须同回合进入 ledger 与 manifest/task runtime。",
            "validation 只能消费 implementation 已落盘 ledger 与前序 stage reports，不能代替 implementation 补证据。",
        ],
        "stage_blockers": [
            "不得先改真实实现，再在 turn 末尾凭记忆补证据。",
            "不得跳过 active package 或额外偷改未纳入当前 package 的范围。",
            "不得把 validation 或 final_delivery 内容提前写入 implementation 完成态。",
        ],
        "required_upstream_reports": STAGE_UPSTREAM_REPORTS["implementation"],
        "required_sections": STAGE_REQUIRED_SECTIONS["implementation"],
    },
    "validation": {
        "purpose": "使用 backend terminal 做真实交互验收，并独立落盘说明如何判定通过。",
        "entry_requirements": [
            "implementation 已产生真实 ledger 记录，且每条关键 entry 都能回溯到前序 stage reports。",
            "validation 只消费前序阶段已落盘产物，不得代替前序阶段补写内容。",
            "必须先把验收问题框架、成功信号、失败信号、副作用边界与通过理由问透再出结论。",
        ],
        "required_objects": list(WORKSPACE_LAYOUT.values()),
        "required_artifacts": [STAGE_ARTIFACTS["validation"]],
        "writeback_targets": [WORKSPACE_LAYOUT["manifest"], STAGE_ARTIFACTS["validation"]],
        "lint_focus": [
            "validation question framework and acceptance reasoning chain",
            "acceptance report section completeness",
            "explicit reference to all prior stage outputs",
        ],
        "question_framework": [
            "当前实现到底验证了什么、没验证什么、为什么这些 witness 足以支持通过或不通过。",
            "前序阶段的哪些判断在真实运行里得到了证实、被推翻或仍未被覆盖。",
            "哪些副作用是可接受的，哪些残余风险必须继续观察或阻塞交付。",
            "如果现在宣称通过，是否存在任何“代码已改但无证据”或“结论已写但无引用”的漏洞。",
        ],
        "derivation_chain": [
            "validation report 必须逐条引用 research 到 implementation 的正式产物，再解释验收结论如何得出。",
            "验证结论只能来自 backend terminal witness、对象一致性和前序 stage reports 的承接链。",
            "final_delivery 只能消费 validation 已落盘验收报告，不能自己重做验收。",
        ],
        "stage_blockers": [
            "不得把暂时没写回伪装成阶段完成。",
            "不得只写 pass/fail 而不写 success feedback、failure signal 与推导链。",
            "不得在 implementation 证据不完整时把 validation 标成 completed。",
        ],
        "required_upstream_reports": STAGE_UPSTREAM_REPORTS["validation"],
        "required_sections": STAGE_REQUIRED_SECTIONS["validation"],
    },
    "final_delivery": {
        "purpose": "最终只向人类输出简要运行报告，因为完整过程已经在文件中落盘。",
        "entry_requirements": [
            "validation 已完成且 acceptance report 已写回。",
            "final_delivery 只做面向人类的交付摘要，不得新增新的实现、设计、影响面或验收判断。",
            "必须显式承接前八个阶段的正式产物，让人类能追溯最终结论从哪里来。",
        ],
        "required_objects": [WORKSPACE_LAYOUT["manifest"]],
        "required_artifacts": [STAGE_ARTIFACTS["validation"], STAGE_ARTIFACTS["final_delivery"]],
        "writeback_targets": [WORKSPACE_LAYOUT["manifest"], STAGE_ARTIFACTS["final_delivery"]],
        "lint_focus": [
            "final delivery references validation and prior stage outputs",
            "final delivery brief section completeness",
            "all stages completed before final delivery closes",
        ],
        "question_framework": [
            "对人类真正需要交付的最终结论、关键承接链、剩余风险和后续观察点是什么。",
            "哪些细节已经在前序阶段落盘，因此 final_delivery 只需摘要而不应重写。",
            "如果 final_delivery 说了一句前序文档里不存在的话，是否意味着它越权新增了判断。",
        ],
        "derivation_chain": [
            "final_delivery brief 必须显式引用 validation 以及更早阶段正式产物。",
            "它只允许压缩、摘要、归纳，不允许产生新的阶段结论。",
            "只有当前八个阶段都 completed，final_delivery 才能 closed 当前任务。",
        ],
        "stage_blockers": [
            "不得把 final_delivery 当成补写 validation 或 implementation 证据的地方。",
            "不得输出脱离前序正式产物的新结论。",
            "不得在任一前序阶段未完成时关闭任务。",
        ],
        "required_upstream_reports": STAGE_UPSTREAM_REPORTS["final_delivery"],
        "required_sections": STAGE_REQUIRED_SECTIONS["final_delivery"],
    },
}


def runtime_contract_payload() -> RuntimeContractPayload:
    from .task_runtime import managed_root, task_runtime_root

    return {
        "status": "ok",
        "skill_name": "Functional-Analysis-Runtask",
        "skill_mode": "executable_workflow_skill",
        "root_shape": ["SKILL.md", "path", "agents", "scripts"],
        "entry_doc": "path/analysis_loop/00_ANALYSIS_LOOP_ENTRY.md",
        "commands": [
            "runtime-contract",
            "read-contract-context",
            "read-path-context",
            "stage-checklist",
            "stage-lint",
            "task-gate-check",
            "task-runtime-scaffold",
            "workspace-scaffold",
        ],
        "stage_order": STAGE_ORDER,
        "workspace_layout": WORKSPACE_LAYOUT,
        "stage_artifacts": STAGE_ARTIFACTS,
        "layout_rule": "小型对象是真相源；阶段正式产物是对外显式交付；每个阶段都只能消费前序已落盘产物或声明允许继承的输入；禁止一次性预写九阶段内容再直接施工。",
        "compiler_rule": "SKILL.md 只暴露 analysis_loop 入口；下游 markdown 通过 reading_chain 编译完整上下文。",
        "artifact_managed_root": str(managed_root()),
        "task_runtime_root": str(task_runtime_root()),
        "artifact_write_policy": "Task artifacts must first resolve a governed destination through Functional-HumenWorkZone-Manager and must not be written under the skill directory.",
        "task_runtime_policy": "Each task must create a numbered task_runtime.yaml skeleton under Codex_Skill_Runtime before workspace scaffold. New tasks are blocked until prior task runtimes are fully closed.",
        "artifact_handoff_commands": HUMENWORKZONE_COMMANDS,
    }


def stage_checklist_payload(stage: str) -> StageChecklistPayload:
    return {
        "stage": stage,
        **STAGES[stage],
        "workspace_layout": WORKSPACE_LAYOUT,
        "stage_artifacts": STAGE_ARTIFACTS,
    }
