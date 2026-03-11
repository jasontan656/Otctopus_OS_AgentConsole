export type StageId =
  | 'foundation_north_star'
  | 'responsive_surface_system'
  | 'motion_component_architecture'
  | 'showroom_runtime_delivery'

export interface StageChecklist {
  stage_id: StageId
  stage_objective: string
  required_outputs: string[]
  resident_docs: string[]
  stage_docs: string[]
  entry_actions: string[]
  exit_gates: string[]
  discard_policy: {
    read_policy: string
    update_policy: string
  }
}

export interface StageDocContract {
  stage_id: StageId
  doc_boundary: string[]
  do_not_read_by_default: string[]
  focus_rule: string
}

export interface StageCommandContract {
  stage_id: StageId
  entry_commands: string[]
  gate_commands: string[]
  stage_actions: string[]
  forbidden_actions: string[]
}

export interface StageGraphContract {
  stage_id: StageId
  graph_role: {
    read_policy: string
    update_policy: string
  }
  prioritize_nodes: string[]
  allowed_cross_links: string[]
}

export interface StageDefinition {
  checklist: StageChecklist
  docContract: StageDocContract
  commandContract: StageCommandContract
  graphContract: StageGraphContract
}

const RESIDENT_DOCS = [
  'SKILL.md',
  'references/runtime/SKILL_RUNTIME_CONTRACT.md',
  'references/stages/00_STAGE_INDEX.md',
  'references/stages/01_RESIDENT_FRONTEND_NORTH_STAR.md',
]

const STAGES: Record<StageId, StageDefinition> = {
  foundation_north_star: {
    checklist: {
      stage_id: 'foundation_north_star',
      stage_objective: 'Define the long-lived frontend north star, skill scope, design tone, and showroom role.',
      required_outputs: [
        'Resident docs describe the skill purpose, audience, and constraints.',
        'Foundation docs define the shared visual language and graph-display intent.',
      ],
      resident_docs: RESIDENT_DOCS,
      stage_docs: [
        'references/stages/10_STAGE_FOUNDATION.md',
        'references/runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.md',
      ],
      entry_actions: [
        'Read the resident docs and current stage doc contract.',
        'Confirm the site is both a standards system and a live showroom.',
      ],
      exit_gates: [
        'The frontend north star is explicit and single-axis.',
        'The viewer is positioned as a reusable display shell, not a one-off page.',
      ],
      discard_policy: {
        read_policy: 'Drop previous stage-specific implementation details when leaving this stage.',
        update_policy: 'Only keep resident docs plus approved foundation changes.',
      },
    },
    docContract: {
      stage_id: 'foundation_north_star',
      doc_boundary: [
        ...RESIDENT_DOCS,
        'references/stages/10_STAGE_FOUNDATION.md',
        'references/runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.md',
      ],
      do_not_read_by_default: [
        'frontend_dev_contracts/VIEWER_SERVICE_WORKFLOW.md',
        'ui-dev/client/src/App.vue',
      ],
      focus_rule: 'Stay at strategy, IA, and skill boundary level before touching responsive or runtime details.',
    },
    commandContract: {
      stage_id: 'foundation_north_star',
      entry_commands: [
        'npm run cli -- runtime-contract --json',
        'npm run cli -- stage-checklist --stage foundation_north_star --json',
      ],
      gate_commands: [
        'npm run cli -- stage-doc-contract --stage foundation_north_star --json',
        'npm run cli -- stage-graph-contract --stage foundation_north_star --json',
      ],
      stage_actions: [
        'Update resident docs.',
        'Adjust stage index and runtime contract when the skill scope changes.',
      ],
      forbidden_actions: [
        'Do not start page-level polishing.',
        'Do not patch runtime scripts before the foundation is stable.',
      ],
    },
    graphContract: {
      stage_id: 'foundation_north_star',
      graph_role: {
        read_policy: 'Read resident docs first, then the single foundation stage doc.',
        update_policy: 'Only add anchors that clarify the north-star path or stage routing.',
      },
      prioritize_nodes: [
        'SKILL.md',
        'references/runtime/SKILL_RUNTIME_CONTRACT.md',
        'references/stages/01_RESIDENT_FRONTEND_NORTH_STAR.md',
        'references/stages/10_STAGE_FOUNDATION.md',
      ],
      allowed_cross_links: [
        'Foundation docs may link to ui-dev positioning docs when they affect the showroom role.',
      ],
    },
  },
  responsive_surface_system: {
    checklist: {
      stage_id: 'responsive_surface_system',
      stage_objective: 'Define desktop, mobile landscape, and mobile portrait surface rules.',
      required_outputs: [
        'Desktop and mobile layout rules are explicit.',
        'The graph display remains primary across surface variants.',
      ],
      resident_docs: RESIDENT_DOCS,
      stage_docs: [
        'references/stages/20_STAGE_SURFACE_LAYOUTS.md',
        'frontend_dev_contracts/rules/UI_LAYOUT_ADJUSTMENT_RULES.md',
      ],
      entry_actions: [
        'Read the current surface-system docs.',
        'Check how graph, document index, and content panel adapt by viewport.',
      ],
      exit_gates: [
        'Desktop, mobile landscape, and mobile portrait rules are separately stated.',
        'The graph is never demoted into a hidden secondary feature.',
      ],
      discard_policy: {
        read_policy: 'Discard previous layout experiments that are not reflected in stage docs.',
        update_policy: 'Only keep responsive rules that survive doc-level review.',
      },
    },
    docContract: {
      stage_id: 'responsive_surface_system',
      doc_boundary: [
        ...RESIDENT_DOCS,
        'references/stages/20_STAGE_SURFACE_LAYOUTS.md',
        'frontend_dev_contracts/rules/UI_LAYOUT_ADJUSTMENT_RULES.md',
        'frontend_dev_contracts/VIEWER_STACK_AND_REUSE.md',
      ],
      do_not_read_by_default: [
        'ui-dev/server/viewer-server.ts',
        'ui-dev/scripts/install_user_service.sh',
      ],
      focus_rule: 'Stay on layout behavior, viewport choreography, and graph readability instead of runtime plumbing.',
    },
    commandContract: {
      stage_id: 'responsive_surface_system',
      entry_commands: [
        'npm run cli -- stage-checklist --stage responsive_surface_system --json',
        'npm run cli -- stage-doc-contract --stage responsive_surface_system --json',
      ],
      gate_commands: [
        'cd ui-dev && npm run typecheck',
      ],
      stage_actions: [
        'Adjust layout docs before editing Vue components.',
        'Update App.vue and related styles after the docs are aligned.',
      ],
      forbidden_actions: [
        'Do not change service/runtime files for pure viewport work.',
        'Do not bury the graph behind a second navigation layer.',
      ],
    },
    graphContract: {
      stage_id: 'responsive_surface_system',
      graph_role: {
        read_policy: 'Prioritize docs that describe viewport hierarchy and panel choreography.',
        update_policy: 'Surface-stage changes may add anchors between stage docs and ui-dev layout rules.',
      },
      prioritize_nodes: [
        'references/stages/20_STAGE_SURFACE_LAYOUTS.md',
        'frontend_dev_contracts/rules/UI_LAYOUT_ADJUSTMENT_RULES.md',
        'frontend_dev_contracts/VIEWER_STACK_AND_REUSE.md',
      ],
      allowed_cross_links: [
        'Cross-link responsive docs with showroom stack docs when a surface rule changes the runtime shell.',
      ],
    },
  },
  motion_component_architecture: {
    checklist: {
      stage_id: 'motion_component_architecture',
      stage_objective: 'Govern motion language, reusable components, and frontend code organization.',
      required_outputs: [
        'Motion rules are explicit and tied to information hierarchy.',
        'Component and code-organization boundaries are stable enough for reuse.',
      ],
      resident_docs: RESIDENT_DOCS,
      stage_docs: [
        'references/stages/30_STAGE_MOTION_COMPONENT_ARCHITECTURE.md',
        'frontend_dev_contracts/UI_FILE_ORGANIZATION.md',
        'frontend_dev_contracts/VIEWER_STACK_AND_REUSE.md',
      ],
      entry_actions: [
        'Read component-system and motion docs before touching implementation files.',
        'Treat the viewer as a seed of a broader UI kit and showroom.',
      ],
      exit_gates: [
        'Motion is purposeful instead of decorative.',
        'Reusable component boundaries and file organization are documented.',
      ],
      discard_policy: {
        read_policy: 'Discard ad-hoc component experiments unless they are reflected in the stage docs.',
        update_policy: 'Keep only component patterns that fit the documented architecture.',
      },
    },
    docContract: {
      stage_id: 'motion_component_architecture',
      doc_boundary: [
        ...RESIDENT_DOCS,
        'references/stages/30_STAGE_MOTION_COMPONENT_ARCHITECTURE.md',
        'frontend_dev_contracts/UI_FILE_ORGANIZATION.md',
        'frontend_dev_contracts/VIEWER_STACK_AND_REUSE.md',
      ],
      do_not_read_by_default: [
        'frontend_dev_contracts/VIEWER_SERVICE_WORKFLOW.md',
      ],
      focus_rule: 'Stay on reusable component architecture, motion semantics, and code shape.',
    },
    commandContract: {
      stage_id: 'motion_component_architecture',
      entry_commands: [
        'npm run cli -- stage-checklist --stage motion_component_architecture --json',
        'npm run cli -- stage-doc-contract --stage motion_component_architecture --json',
      ],
      gate_commands: [
        'cd ui-dev && npm run typecheck',
        'cd ui-dev && npm test',
      ],
      stage_actions: [
        'Refine component/file organization docs before restructuring code.',
        'Promote stable UI pieces into reusable components instead of one-off view code.',
      ],
      forbidden_actions: [
        'Do not solve architecture drift with local patches only.',
        'Do not add motion that obscures reading or graph comprehension.',
      ],
    },
    graphContract: {
      stage_id: 'motion_component_architecture',
      graph_role: {
        read_policy: 'Follow the component/motion doc chain before opening implementation files.',
        update_policy: 'New anchors should clarify how motion, components, and architecture reinforce each other.',
      },
      prioritize_nodes: [
        'references/stages/30_STAGE_MOTION_COMPONENT_ARCHITECTURE.md',
        'frontend_dev_contracts/UI_FILE_ORGANIZATION.md',
        'frontend_dev_contracts/VIEWER_STACK_AND_REUSE.md',
      ],
      allowed_cross_links: [
        'Cross-link stage docs with frontend contracts when a runtime component pattern becomes a general frontend rule.',
      ],
    },
  },
  showroom_runtime_delivery: {
    checklist: {
      stage_id: 'showroom_runtime_delivery',
      stage_objective: 'Keep the runnable showroom, live graph page, and delivery workflow healthy.',
      required_outputs: [
        'The site runs in dev and production mode.',
        'The showroom reflects live doc changes and remains the human-readable exhibit of the skill.',
      ],
      resident_docs: RESIDENT_DOCS,
      stage_docs: [
        'references/stages/40_STAGE_SHOWROOM_RUNTIME.md',
        'ui-dev/UI_DEV_ENTRY.md',
        'frontend_dev_contracts/00_UI_DEVELOPMENT_INDEX.md',
        'frontend_dev_contracts/VIEWER_SERVICE_WORKFLOW.md',
      ],
      entry_actions: [
        'Read the runtime/showroom docs before editing server or service files.',
        'Verify the target skill root and viewer ports before deploy actions.',
      ],
      exit_gates: [
        'Dev and production entrypoints both work.',
        'The viewer shows the current skill graph without static drift.',
      ],
      discard_policy: {
        read_policy: 'Discard stale runtime assumptions after each restart or target change.',
        update_policy: 'Only keep runtime settings that match the current service and package configuration.',
      },
    },
    docContract: {
      stage_id: 'showroom_runtime_delivery',
      doc_boundary: [
        ...RESIDENT_DOCS,
        'references/stages/40_STAGE_SHOWROOM_RUNTIME.md',
        'ui-dev/UI_DEV_ENTRY.md',
        'frontend_dev_contracts/00_UI_DEVELOPMENT_INDEX.md',
        'frontend_dev_contracts/VIEWER_SERVICE_WORKFLOW.md',
        'frontend_dev_contracts/UI_TOOL_POSITIONING.md',
      ],
      do_not_read_by_default: [
        'references/stages/20_STAGE_SURFACE_LAYOUTS.md',
      ],
      focus_rule: 'Stay on runtime health, viewer behavior, and showroom delivery rather than strategic redesign.',
    },
    commandContract: {
      stage_id: 'showroom_runtime_delivery',
      entry_commands: [
        'npm run cli -- stage-checklist --stage showroom_runtime_delivery --json',
        'npm run cli -- rebuild-self-graph --json',
      ],
      gate_commands: [
        'cd ui-dev && npm run typecheck',
        'cd ui-dev && npm test',
        'cd ui-dev && npm run build',
      ],
      stage_actions: [
        'Run the viewer in dev mode.',
        'Install or restart the user-level systemd service when required.',
      ],
      forbidden_actions: [
        'Do not ship a static mock page disconnected from the live payload.',
        'Do not leave runtime naming tied to another skill.',
      ],
    },
    graphContract: {
      stage_id: 'showroom_runtime_delivery',
      graph_role: {
        read_policy: 'Prioritize runtime docs, ui-dev entry, and live viewer workflow.',
        update_policy: 'Keep anchors aligned with the runnable showroom path and service chain.',
      },
      prioritize_nodes: [
        'references/stages/40_STAGE_SHOWROOM_RUNTIME.md',
        'ui-dev/UI_DEV_ENTRY.md',
        'frontend_dev_contracts/VIEWER_SERVICE_WORKFLOW.md',
      ],
      allowed_cross_links: [
        'Showroom runtime docs may cross-link to any stage when the display shell exposes their rules to humans.',
      ],
    },
  },
}

export const RUNTIME_CONTRACT = {
  contract_name: 'META_VUE3_WEBUI_FRONTEND_RUNTIME_CONTRACT',
  contract_version: 'v1',
  validation_mode: 'cli_first_strict',
  skill_name: 'Dev-VUE3-WebUI-Frontend',
  skill_profile: 'staged_cli_first',
  facade_contract: {
    skill_md_role: 'entry_only',
    required_sections: [
      '定位',
      '必读顺序',
      '分类入口',
      '适用域',
      '执行入口',
      '读取原则',
      '结构索引',
    ],
  },
  routing_protocol: {
    first_command: 'npm run cli -- runtime-contract --json',
    stage_contract_sequence: [
      'stage-checklist',
      'stage-doc-contract',
      'stage-command-contract',
      'stage-graph-contract',
    ],
    markdown_role: 'human_audit_and_narrow_navigation',
    machine_rule_source: 'Cli_Toolbox JSON outputs',
  },
  resident_doc_policy: {
    top_level_resident_docs: RESIDENT_DOCS,
    stage_switch_rule: 'Keep only resident docs across stage switches; drop prior stage docs and temporary focus.',
  },
  stage_contract_policy: {
    stage_order: Object.keys(STAGES),
    required_contracts: [
      'stage-checklist',
      'stage-doc-contract',
      'stage-command-contract',
      'stage-graph-contract',
    ],
  },
  tool_contracts: {
    'Cli_Toolbox.runtime-contract': 'Emit the staged runtime contract for the skill facade.',
    'Cli_Toolbox.stage-checklist': 'Emit stage objective, required outputs, resident docs, stage docs, entry actions, exit gates, and discard policy.',
    'Cli_Toolbox.stage-doc-contract': 'Emit the current stage document boundary.',
    'Cli_Toolbox.stage-command-contract': 'Emit entry commands, gate commands, stage actions, and forbidden actions.',
    'Cli_Toolbox.stage-graph-contract': 'Emit graph-reading and graph-update policy for the current stage.',
    'Cli_Toolbox.build-anchor-graph': 'Emit the current markdown graph workspace for a target skill root.',
    'Cli_Toolbox.rebuild-self-graph': 'Rebuild self_anchor_graph.json for the current skill root.',
  },
  governance_rules: [
    'SKILL.md must stay entry-only.',
    'The skill doubles as a frontend standards system and a human-readable live showroom.',
    'Runtime rules must be consumed from machine-readable contracts instead of markdown.',
    'The graph display remains a first-class narrative surface across desktop and mobile variants.',
    'Reusable component, motion, architecture, and runtime rules must stay document-first before code changes.',
  ],
  validation_closure: [
    'npm run typecheck',
    'npm test',
    'cd ui-dev && npm run typecheck',
    'cd ui-dev && npm test',
    'cd ui-dev && npm run build',
    'npm run cli -- rebuild-self-graph --json',
  ],
} as const

export function listStages(): StageId[] {
  return Object.keys(STAGES) as StageId[]
}

export function getStageDefinition(stageId: string): StageDefinition {
  if (!(stageId in STAGES)) {
    throw new Error(`unknown stage: ${stageId}`)
  }
  return STAGES[stageId as StageId]
}
