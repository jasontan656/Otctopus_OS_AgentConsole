import type {
  AnchorDefinition,
  AnchorMatrix,
  GraphEdgeRecord,
  GraphNodeRecord,
  RuntimeContractPayload,
  ScanError,
  ScanWarning,
} from '../../src/lib/types.js'

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
