import path from 'node:path'
import type { GraphEdgeRecord } from '../../src/lib/types.js'
import { buildDocGraphWorkspace } from '../../src/lib/docstructure.js'
import type { PreviewDocumentRecord, PreviewPayload } from './viewer-types.js'

export async function buildViewerPayload(targetRootInput: string): Promise<PreviewPayload> {
  const workspace = await buildDocGraphWorkspace(targetRootInput)
  const incomingByTarget = new Map<string, GraphEdgeRecord[]>()
  const outgoingBySource = new Map<string, GraphEdgeRecord[]>()

  for (const edge of workspace.graph.edges) {
    outgoingBySource.set(edge.source, [...(outgoingBySource.get(edge.source) ?? []), edge])
    incomingByTarget.set(edge.target, [...(incomingByTarget.get(edge.target) ?? []), edge])
  }

  const previewDocs: PreviewDocumentRecord[] = workspace.docs.map((doc) => ({
    path: doc.path,
    docId: doc.docId,
    docType: doc.docType,
    topic: doc.topic,
    title: doc.title,
    anchorCount: doc.anchorCount,
    depth: doc.depth,
    body: doc.body,
    anchors: doc.anchors,
    outgoing: outgoingBySource.get(doc.path) ?? [],
    incoming: incomingByTarget.get(doc.path) ?? [],
    warnings: workspace.warnings.filter((warning) => warning.doc === doc.path),
  }))

  return {
    status: workspace.status,
    targetRoot: workspace.targetRoot,
    updatedAt: workspace.updatedAt,
    runtimeContract: workspace.runtimeContract,
    matrix: workspace.matrix,
    summary: workspace.summary,
    view: {
      entryPath: previewDocs.some((doc) => doc.path === 'SKILL.md') ? 'SKILL.md' : (previewDocs[0]?.path ?? ''),
      targetSkillName: path.basename(workspace.targetRoot),
    },
    graph: workspace.graph,
    docs: previewDocs,
    warnings: workspace.warnings,
    errors: workspace.errors,
  }
}
