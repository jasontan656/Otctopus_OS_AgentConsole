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

export interface RuntimeContractPayload {
  contract_name: string
  contract_version: string
  skill_name: string
  scope: string
  primary_goal: string
  thinking_chain: string[]
  commands: Record<string, string>
  frontmatter_contract: {
    template_path: string
    required_fields: string[]
    skill_md_metadata_path: string
  }
  graph_contract: {
    matrix_path: string
    self_graph_path: string
    min_anchor_count_per_doc: number
    target_must_be_markdown: boolean
  }
  viewer_contract?: {
    host_env: string
    port_env: string
    api_path: string
    ws_path: string
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

export interface PreviewDocumentRecord extends GraphNodeRecord {
  body: string
  anchors: AnchorDefinition[]
  outgoing: GraphEdgeRecord[]
  incoming: GraphEdgeRecord[]
  warnings: ScanWarning[]
}

export interface PreviewPayload {
  status: 'pass' | 'pass_with_warnings' | 'fail'
  targetRoot: string
  updatedAt: string
  runtimeContract: RuntimeContractPayload
  matrix: AnchorMatrix
  summary: {
    nodeCount: number
    edgeCount: number
    errorCount: number
    warningCount: number
  }
  view: {
    entryPath: string
    targetSkillName: string
  }
  graph: {
    nodes: GraphNodeRecord[]
    edges: GraphEdgeRecord[]
  }
  docs: PreviewDocumentRecord[]
  warnings: ScanWarning[]
  errors: ScanError[]
}
