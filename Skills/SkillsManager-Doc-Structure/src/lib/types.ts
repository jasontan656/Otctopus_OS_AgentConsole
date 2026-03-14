export type AnchorDirection = 'upstream' | 'downstream' | 'lateral' | 'cross'

export interface AnchorDefinition {
  target: string
  relation: string
  direction: AnchorDirection
  reason: string
}

export interface GraphNodeRecord {
  path: string
  docId: string
  docType: string
  topic: string
  title: string
  anchorCount: number
  depth: number
  nodeRole?: string
  domainType?: string
}

export interface GraphEdgeRecord {
  source: string
  target: string
  relation: string
  direction: AnchorDirection
  reason: string
}

export interface ScanWarning {
  doc: string
  ruleId: string
  severity: string
  message: string
  hits: number
}

export interface ScanError {
  doc: string
  error: string
}

export type SplitDecision = 'accepted' | 'split_required'
export type SplitDecisionStatus = 'requires_decision' | 'accepted' | 'split_required'

export interface SplitDecisionRegistryEntry {
  doc_path: string
  doc_id: string
  rule_id: string
  fingerprint: string
  decision: SplitDecision
  note: string
  decided_at: string
}

export interface SplitDecisionRegistry {
  registry_name: string
  registry_version: string
  entries: SplitDecisionRegistryEntry[]
}

export interface SplitCandidate {
  doc: string
  docId: string
  title: string
  ruleId: string
  severity: string
  message: string
  hits: number
  fingerprint: string
  decisionStatus: SplitDecisionStatus
  blocking: boolean
  note?: string
}

export interface RuntimeContractPayload {
  contract_name: string
  contract_version: string
  skill_name: string
  target_skill_mode?: string
  applicability?: string
  notes?: string[]
  scope: string
  primary_goal: string
  thinking_chain: string[]
  commands: Record<string, string>
  knowledge_tracks: {
    rules_track_entry: string
    fewshot_track_entry: string
    metadata_track_entry: string
  }
  workflow_tracks: {
    query_workflow_entry: string
    architecture_workflow_entry: string
    single_doc_workflow_entry: string
  }
  frontmatter_contract: {
    template_path: string
    template_assets: string[]
    required_fields: string[]
    optional_fields: string[]
    skill_md_metadata_path: string
  }
  graph_contract: {
    matrix_path: string
    self_graph_path: string
    min_anchor_count_per_doc: number
    target_must_be_markdown: boolean
  }
  semantic_split_contract: {
    navigation_model: string
    node_roles: string[]
    role_rules: Record<string, string>
    split_triggers: string[]
    stop_split_conditions: string[]
    routing_principles: string[]
    split_decision_registry_path: string
  }
}

export interface AnchorMatrix {
  matrix_name: string
  matrix_version: string
  scope: string
  required_frontmatter_fields: string[]
  required_anchor_fields: string[]
  allowed_directions: AnchorDirection[]
  hard_rules: string[]
  anchor_query_semantics: Array<{
    query: string
    relations: string[]
    directions: AnchorDirection[]
    keywords: string[]
  }>
  split_keyword_rules: Array<{
    rule_id: string
    scope: 'title' | 'body'
    keywords: string[]
    threshold: number
    severity: string
    message: string
  }>
}

export interface SkillDocRecord extends GraphNodeRecord {
  body: string
  anchors: AnchorDefinition[]
}

export interface DocGraphWorkspace {
  status: 'pass' | 'pass_with_warnings' | 'fail' | 'skipped'
  targetRoot: string
  targetSkillMode: string
  applicability: 'enforced' | 'skipped_guide_only'
  updatedAt: string
  runtimeContract: RuntimeContractPayload
  matrix: AnchorMatrix
  summary: {
    nodeCount: number
    edgeCount: number
    errorCount: number
    warningCount: number
    splitCandidateCount: number
    blockingSplitCandidateCount: number
  }
  graph: {
    nodes: GraphNodeRecord[]
    edges: GraphEdgeRecord[]
  }
  docs: SkillDocRecord[]
  splitCandidates: SplitCandidate[]
  warnings: ScanWarning[]
  errors: ScanError[]
  notes: string[]
}
