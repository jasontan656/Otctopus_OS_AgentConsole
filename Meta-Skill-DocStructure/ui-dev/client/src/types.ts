export type AnchorDirection = 'upstream' | 'downstream' | 'lateral' | 'cross'

export interface GraphEdgeRecord {
  source: string
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

export interface ScanWarning {
  doc: string
  ruleId: string
  severity: string
  message: string
  hits: number
}

export interface PreviewDocumentRecord extends GraphNodeRecord {
  body: string
  outgoing: GraphEdgeRecord[]
  incoming: GraphEdgeRecord[]
  warnings: ScanWarning[]
}

export interface PreviewPayload {
  status: 'pass' | 'pass_with_warnings' | 'fail'
  targetRoot: string
  updatedAt: string
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
  errors: Array<{
    doc: string
    error: string
  }>
}
