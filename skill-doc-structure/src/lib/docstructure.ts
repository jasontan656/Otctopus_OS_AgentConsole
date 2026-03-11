import path from 'node:path'
import { promises as fs } from 'node:fs'
import { createHash } from 'node:crypto'
import matter from 'gray-matter'
import type {
  AnchorDefinition,
  AnchorMatrix,
  DocGraphWorkspace,
  GraphEdgeRecord,
  GraphNodeRecord,
  RuntimeContractPayload,
  ScanError,
  ScanWarning,
  SkillDocRecord,
  SplitCandidate,
  SplitDecision,
  SplitDecisionRegistry,
  SplitDecisionRegistryEntry,
} from './types.js'

const DEFAULT_SKILL_ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..', '..')

export class DocStructureError extends Error {}

interface ResolvedContext {
  currentSkillRoot: string
  targetRoot: string
  matrixPath: string
  runtimeContractPath: string
  selfGraphPath: string
  splitDecisionRegistryPath: string
}

const DEFAULT_SPLIT_DECISION_REGISTRY: SplitDecisionRegistry = {
  registry_name: 'META_SKILL_DOCSTRUCTURE_SPLIT_DECISION_REGISTRY',
  registry_version: 'v1',
  entries: [],
}

function normalizeFileUrlPath(rawPath: string): string {
  return decodeURIComponent(rawPath)
}

function currentSkillRoot(): string {
  return normalizeFileUrlPath(DEFAULT_SKILL_ROOT)
}

async function fileExists(candidate: string): Promise<boolean> {
  try {
    await fs.access(candidate)
    return true
  } catch {
    return false
  }
}

async function resolveContext(targetRootInput: string): Promise<ResolvedContext> {
  const currentRoot = currentSkillRoot()
  const targetRoot = path.resolve(targetRootInput)
  if (!(await fileExists(path.join(targetRoot, 'SKILL.md')))) {
    throw new DocStructureError(`target is not a skill root: ${targetRoot}`)
  }

  const targetMatrix = path.join(targetRoot, 'assets', 'runtime', 'anchor_query_matrix.json')
  const targetRuntimeContract = path.join(targetRoot, 'references', 'runtime', 'SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.json')
  const matrixPath = (await fileExists(targetMatrix))
    ? targetMatrix
    : path.join(currentRoot, 'assets', 'runtime', 'anchor_query_matrix.json')
  const runtimeContractPath = (await fileExists(targetRuntimeContract))
    ? targetRuntimeContract
    : path.join(currentRoot, 'references', 'runtime', 'SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.json')

  return {
    currentSkillRoot: currentRoot,
    targetRoot,
    matrixPath,
    runtimeContractPath,
    selfGraphPath: path.join(targetRoot, 'assets', 'runtime', 'self_anchor_graph.json'),
    splitDecisionRegistryPath: path.join(targetRoot, 'assets', 'runtime', 'split_decision_registry.json'),
  }
}

async function readJsonFile<T>(filePath: string): Promise<T> {
  const text = await fs.readFile(filePath, 'utf8')
  return JSON.parse(text) as T
}

async function collectMarkdownDocs(root: string, dir = root): Promise<string[]> {
  const entries = await fs.readdir(dir, { withFileTypes: true })
  const docs: string[] = []

  for (const entry of entries) {
    const absolute = path.join(dir, entry.name)
    if (entry.isDirectory()) {
      if (['.git', 'node_modules', 'dist'].includes(entry.name)) {
        continue
      }
      docs.push(...(await collectMarkdownDocs(root, absolute)))
      continue
    }
    if (entry.isFile() && entry.name.endsWith('.md')) {
      docs.push(absolute)
    }
  }

  return docs.sort()
}

function extractTitle(body: string, absolutePath: string): string {
  const heading = body.split('\n').find((line) => line.startsWith('# '))
  return heading ? heading.slice(2).trim() : path.basename(absolutePath, '.md')
}

function normalizeDirection(raw: unknown): AnchorDefinition['direction'] {
  const value = String(raw ?? '').trim() as AnchorDefinition['direction']
  return value
}

function extractContract(
  absolutePath: string,
  data: Record<string, unknown>,
  requiredFields: string[],
): {
  docId: string
  docType: string
  topic: string
  anchors: AnchorDefinition[]
} {
  const contract = path.basename(absolutePath) === 'SKILL.md'
    ? ((data.metadata as Record<string, unknown> | undefined)?.doc_structure as Record<string, unknown> | undefined)
    : data

  if (!contract || typeof contract !== 'object') {
    throw new DocStructureError(`missing doc structure contract: ${absolutePath}`)
  }

  for (const field of requiredFields) {
    if (!(field in contract)) {
      throw new DocStructureError(`missing '${field}' in ${absolutePath}`)
    }
  }

  const anchors = contract.anchors
  if (!Array.isArray(anchors) || anchors.length === 0) {
    throw new DocStructureError(`anchors must be a non-empty list in ${absolutePath}`)
  }

  return {
    docId: String(contract.doc_id),
    docType: String(contract.doc_type),
    topic: String(contract.topic),
    anchors: anchors.map((anchor) => {
      if (!anchor || typeof anchor !== 'object') {
        throw new DocStructureError(`anchor entry must be an object in ${absolutePath}`)
      }
      return {
        target: String((anchor as Record<string, unknown>).target ?? ''),
        relation: String((anchor as Record<string, unknown>).relation ?? ''),
        direction: normalizeDirection((anchor as Record<string, unknown>).direction),
        reason: String((anchor as Record<string, unknown>).reason ?? ''),
      }
    }),
  }
}

function fingerprintRecord(record: Pick<SkillDocRecord, 'title' | 'body'>): string {
  return createHash('sha1')
    .update(`${record.title}\n${record.body}`.trim())
    .digest('hex')
}

function collectSplitCandidates(
  record: Pick<SkillDocRecord, 'path' | 'docId' | 'title' | 'body'>,
  matrix: AnchorMatrix,
): SplitCandidate[] {
  const candidates: SplitCandidate[] = []
  const fingerprint = fingerprintRecord(record)
  for (const rule of matrix.split_keyword_rules) {
    const haystack = (rule.scope === 'title' ? record.title : record.body).toLowerCase()
    let hits = 0
    for (const keyword of rule.keywords) {
      if (haystack.includes(keyword.toLowerCase())) {
        hits += 1
      }
    }
    if (hits >= rule.threshold) {
      candidates.push({
        doc: record.path,
        docId: record.docId,
        title: record.title,
        ruleId: rule.rule_id,
        severity: rule.severity,
        message: rule.message,
        hits,
        fingerprint,
        decisionStatus: 'requires_decision',
        blocking: true,
      })
    }
  }
  return candidates
}

async function loadSplitDecisionRegistry(registryPath: string): Promise<SplitDecisionRegistry> {
  if (!(await fileExists(registryPath))) {
    return { ...DEFAULT_SPLIT_DECISION_REGISTRY, entries: [] }
  }
  const registry = await readJsonFile<SplitDecisionRegistry>(registryPath)
  return {
    ...DEFAULT_SPLIT_DECISION_REGISTRY,
    ...registry,
    entries: Array.isArray(registry.entries) ? registry.entries : [],
  }
}

function resolveSplitCandidates(
  candidates: SplitCandidate[],
  registry: SplitDecisionRegistry,
): SplitCandidate[] {
  return candidates.map((candidate) => {
    const matched = registry.entries.find((entry) =>
      entry.doc_path === candidate.doc
      && entry.rule_id === candidate.ruleId
      && entry.fingerprint === candidate.fingerprint)

    if (!matched) {
      return candidate
    }

    if (matched.decision === 'accepted') {
      return {
        ...candidate,
        decisionStatus: 'accepted',
        blocking: false,
        note: matched.note,
      }
    }

    return {
      ...candidate,
      decisionStatus: 'split_required',
      blocking: true,
      note: matched.note,
    }
  })
}

function buildSplitDecisionErrors(candidates: SplitCandidate[]): ScanError[] {
  return candidates
    .filter((candidate) => candidate.blocking)
    .map((candidate) => ({
      doc: candidate.doc,
      error: candidate.decisionStatus === 'split_required'
        ? `split required by registry: ${candidate.ruleId} (${candidate.message})`
        : `split decision required: ${candidate.ruleId} (${candidate.message})`,
    }))
}

function normalizeTarget(sourceAbsolutePath: string, targetRawPath: string, targetRoot: string): string {
  const targetAbsolutePath = path.resolve(path.dirname(sourceAbsolutePath), targetRawPath)
  const relative = path.relative(targetRoot, targetAbsolutePath)
  if (relative.startsWith('..') || path.isAbsolute(relative)) {
    throw new DocStructureError(`anchor target escapes skill root: ${sourceAbsolutePath} -> ${targetRawPath}`)
  }
  if (path.extname(targetAbsolutePath) !== '.md') {
    throw new DocStructureError(`anchor target must be markdown: ${sourceAbsolutePath} -> ${targetRawPath}`)
  }
  return relative.split(path.sep).join('/')
}

async function scanDocuments(context: ResolvedContext): Promise<{
  matrix: AnchorMatrix
  runtimeContract: RuntimeContractPayload
  docs: SkillDocRecord[]
  edges: GraphEdgeRecord[]
  splitCandidates: SplitCandidate[]
  errors: ScanError[]
  warnings: ScanWarning[]
}> {
  const matrix = await readJsonFile<AnchorMatrix>(context.matrixPath)
  const runtimeContract = await readJsonFile<RuntimeContractPayload>(context.runtimeContractPath)
  const splitDecisionRegistry = await loadSplitDecisionRegistry(context.splitDecisionRegistryPath)
  const markdownDocs = await collectMarkdownDocs(context.targetRoot)
  const docs: SkillDocRecord[] = []
  const edges: GraphEdgeRecord[] = []
  const errors: ScanError[] = []
  const warnings: ScanWarning[] = []
  const splitCandidates: SplitCandidate[] = []

  for (const absolutePath of markdownDocs) {
    const relativePath = path.relative(context.targetRoot, absolutePath).split(path.sep).join('/')
    try {
      const raw = await fs.readFile(absolutePath, 'utf8')
      const parsed = matter(raw)
      const contract = extractContract(absolutePath, parsed.data as Record<string, unknown>, matrix.required_frontmatter_fields)
      const record: SkillDocRecord = {
        path: relativePath,
        title: extractTitle(parsed.content, absolutePath),
        body: parsed.content.trim(),
        docId: contract.docId,
        docType: contract.docType,
        topic: contract.topic,
        anchors: contract.anchors,
        anchorCount: contract.anchors.length,
        depth: relativePath.split('/').length - 1,
      }
      docs.push(record)
      splitCandidates.push(...collectSplitCandidates(record, matrix))
    } catch (error) {
      errors.push({
        doc: relativePath,
        error: error instanceof Error ? error.message : String(error),
      })
    }
  }

  const documentSet = new Set(docs.map((doc) => doc.path))

  for (const doc of docs) {
    const sourceAbsolutePath = path.join(context.targetRoot, doc.path)
    for (const anchor of doc.anchors) {
      const anchorRecord = anchor as unknown as Record<string, unknown>
      const missing = matrix.required_anchor_fields.filter((field) => {
        const value = anchorRecord[field]
        return typeof value !== 'string' || !value.trim()
      })

      if (missing.length > 0) {
        errors.push({
          doc: doc.path,
          error: `anchor missing fields: ${missing.join(', ')}`,
        })
        continue
      }

      if (!matrix.allowed_directions.includes(anchor.direction)) {
        errors.push({
          doc: doc.path,
          error: `invalid anchor direction: ${anchor.direction}`,
        })
        continue
      }

      try {
        const normalizedTarget = normalizeTarget(sourceAbsolutePath, anchor.target, context.targetRoot)
        const targetAbsolutePath = path.join(context.targetRoot, normalizedTarget)
        const targetExists = await fileExists(targetAbsolutePath)
        if (!targetExists || !documentSet.has(normalizedTarget)) {
          throw new DocStructureError(`anchor target does not exist: ${sourceAbsolutePath} -> ${anchor.target}`)
        }
        edges.push({
          source: doc.path,
          target: normalizedTarget,
          relation: anchor.relation,
          direction: anchor.direction,
          reason: anchor.reason,
        })
      } catch (error) {
        errors.push({
          doc: doc.path,
          error: error instanceof Error ? error.message : String(error),
        })
      }
    }
  }

  const resolvedSplitCandidates = resolveSplitCandidates(splitCandidates, splitDecisionRegistry)
  errors.push(...buildSplitDecisionErrors(resolvedSplitCandidates))

  return {
    matrix,
    runtimeContract,
    docs,
    edges,
    splitCandidates: resolvedSplitCandidates,
    errors,
    warnings,
  }
}

export async function buildDocGraphWorkspace(targetRootInput: string): Promise<DocGraphWorkspace> {
  const context = await resolveContext(targetRootInput)
  const { matrix, runtimeContract, docs, edges, splitCandidates, errors, warnings } = await scanDocuments(context)

  const graphNodes: GraphNodeRecord[] = docs.map((doc) => ({
    path: doc.path,
    docId: doc.docId,
    docType: doc.docType,
    topic: doc.topic,
    title: doc.title,
    anchorCount: doc.anchorCount,
    depth: doc.depth,
  }))

  const blockingSplitCandidateCount = splitCandidates.filter((candidate) => candidate.blocking).length
  const status = errors.length > 0
    ? 'fail'
    : warnings.length > 0
      ? 'pass_with_warnings'
      : 'pass'

  return {
    status,
    targetRoot: context.targetRoot,
    updatedAt: new Date().toISOString(),
    runtimeContract,
    matrix,
    summary: {
      nodeCount: graphNodes.length,
      edgeCount: edges.length,
      errorCount: errors.length,
      warningCount: warnings.length,
      splitCandidateCount: splitCandidates.length,
      blockingSplitCandidateCount,
    },
    graph: {
      nodes: graphNodes,
      edges,
    },
    docs,
    splitCandidates,
    warnings,
    errors,
  }
}

export async function loadRuntimeContract(targetRootInput: string): Promise<RuntimeContractPayload> {
  const context = await resolveContext(targetRootInput)
  return readJsonFile<RuntimeContractPayload>(context.runtimeContractPath)
}

export async function rebuildSelfGraph(targetRootInput: string): Promise<{ graphPath: string; workspace: DocGraphWorkspace }> {
  const context = await resolveContext(targetRootInput)
  const workspace = await buildDocGraphWorkspace(context.targetRoot)
  const snapshot = {
    graph_name: 'META_SKILL_DOCSTRUCTURE_SELF_ANCHOR_GRAPH',
    graph_version: 'v2',
    source_skill: path.basename(context.targetRoot),
    summary: workspace.summary,
    nodes: workspace.graph.nodes,
    edges: workspace.graph.edges,
    split_candidates: workspace.splitCandidates,
    warnings: workspace.warnings,
    updated_at: workspace.updatedAt,
  }
  await fs.mkdir(path.dirname(context.selfGraphPath), { recursive: true })
  await fs.writeFile(context.selfGraphPath, `${JSON.stringify(snapshot, null, 2)}\n`, 'utf8')
  return {
    graphPath: context.selfGraphPath,
    workspace,
  }
}

export function defaultSkillRoot(): string {
  return currentSkillRoot()
}

export async function registerSplitDecision(
  targetRootInput: string,
  docPath: string,
  ruleId: string,
  decision: SplitDecision,
  note: string,
): Promise<{
  registryPath: string
  entry: SplitDecisionRegistryEntry
}> {
  const context = await resolveContext(targetRootInput)
  const workspace = await buildDocGraphWorkspace(context.targetRoot)
  const candidate = workspace.splitCandidates.find((item) => item.doc === docPath && item.ruleId === ruleId)

  if (!candidate) {
    throw new DocStructureError(`split candidate not found: ${docPath} [${ruleId}]`)
  }

  const registry = await loadSplitDecisionRegistry(context.splitDecisionRegistryPath)
  const entry: SplitDecisionRegistryEntry = {
    doc_path: candidate.doc,
    doc_id: candidate.docId,
    rule_id: candidate.ruleId,
    fingerprint: candidate.fingerprint,
    decision,
    note,
    decided_at: new Date().toISOString(),
  }

  const nextRegistry: SplitDecisionRegistry = {
    ...registry,
    entries: [
      ...registry.entries.filter((item) => !(item.doc_path === docPath && item.rule_id === ruleId)),
      entry,
    ],
  }

  await fs.mkdir(path.dirname(context.splitDecisionRegistryPath), { recursive: true })
  await fs.writeFile(context.splitDecisionRegistryPath, `${JSON.stringify(nextRegistry, null, 2)}\n`, 'utf8')

  return {
    registryPath: context.splitDecisionRegistryPath,
    entry,
  }
}
