import path from 'node:path'
import { promises as fs } from 'node:fs'
import matter from 'gray-matter'
import { defaultSkillRoot } from './docstructure.js'

type GateStatus = 'pass' | 'pass_with_warnings' | 'fail'

interface GateMatrix {
  matrix_name: string
  matrix_version: string
  required_frontmatter_keys: string[]
  required_docs: string[]
  excluded_doc_prefixes?: string[]
  blueprint_doc_prefixes: string[]
  visual_doc_prefixes: string[]
  component_doc_prefixes: string[]
  keyword_gate_exempt_docs?: string[]
  split_gate_exempt_docs?: string[]
  split_gate_exempt_prefixes?: string[]
  layout_keywords: string[]
  visual_keywords: string[]
  component_keywords: string[]
  split_keyword_rules: Array<{
    rule_id: string
    keywords: string[]
    threshold: number
    blocking: boolean
    message: string
  }>
}

interface ProductDocRecord {
  path: string
  docId: string
  topic: string
  title: string
  body: string
  docLinks: string[]
  markdownLinks: string[]
  frontmatter: Record<string, unknown>
}

interface ProductGraphEdge {
  source: string
  target: string
  kind: 'doc_link' | 'markdown_link'
}

interface LintIssue {
  code: string
  doc?: string
  message: string
}

interface ProductMotherDocProfile {
  panelCatalog: string[]
  panelBlueprintCoverage: string[]
  panelComponentCoverage: string[]
  componentIdsDefined: string[]
  componentIdsReferenced: string[]
  containerIdsDefined: string[]
  containerIdsReferenced: string[]
  surfaceIdsDefined: string[]
  surfaceIdsReferenced: string[]
  requirementAtoms: string[]
  blueprintDocs: string[]
  visualDocs: string[]
  componentDocs: string[]
}

export interface ProductMotherDocGraphPayload {
  status: GateStatus
  docsRoot: string
  motherDocRoot: string
  graphRoot: string
  matrixName: string
  summary: {
    docCount: number
    edgeCount: number
    errorCount: number
    warningCount: number
  }
  graph: {
    nodes: Array<{
      path: string
      docId: string
      topic: string
      title: string
      docLinkCount: number
      markdownLinkCount: number
    }>
    edges: ProductGraphEdge[]
  }
  profile: ProductMotherDocProfile
  warnings: LintIssue[]
  errors: LintIssue[]
}

export interface ProductMotherDocLintPayload extends ProductMotherDocGraphPayload {
  writtenAssets?: {
    graphPath: string
    profilePath: string
    reportPath: string
  }
}

export class ProductMotherDocGateError extends Error {}

interface ResolvedProductContext {
  docsRoot: string
  motherDocRoot: string
  graphRoot: string
  matrixPath: string
}

const IDENTIFIER_REGEX = /\b(?:container|cmp|surface|panel)\.[A-Za-z0-9_.-]+\b/g
const PANEL_ID_REGEX = /\bpanel\.[A-Za-z0-9_.-]+\b/g
const COMPONENT_ID_REGEX = /\bcmp\.[A-Za-z0-9_.-]+\b/g
const CONTAINER_ID_REGEX = /\bcontainer\.[A-Za-z0-9_.-]+\b/g
const SURFACE_ID_REGEX = /\bsurface\.[A-Za-z0-9_.-]+\b/g
const REQUIREMENT_ID_REGEX = /\bUP-REQ-\d+\b/g
const MARKDOWN_LINK_REGEX = /\[[^\]]+\]\(([^)]+\.md)\)/g

function uniq(items: string[]): string[] {
  return [...new Set(items)].sort()
}

async function fileExists(candidate: string): Promise<boolean> {
  try {
    await fs.access(candidate)
    return true
  } catch {
    return false
  }
}

async function resolveProductContext(docsRootInput: string): Promise<ResolvedProductContext> {
  const docsRoot = path.resolve(docsRootInput)
  const motherDocRoot = path.join(docsRoot, 'mother_doc')
  if (!(await fileExists(motherDocRoot))) {
    throw new ProductMotherDocGateError(`mother_doc root does not exist under docs root: ${docsRoot}`)
  }

  return {
    docsRoot,
    motherDocRoot,
    graphRoot: path.join(docsRoot, 'graph'),
    matrixPath: path.join(defaultSkillRoot(), 'assets', 'runtime', 'product_mother_doc_gate_matrix.json'),
  }
}

async function readJsonFile<T>(filePath: string): Promise<T> {
  const raw = await fs.readFile(filePath, 'utf8')
  return JSON.parse(raw) as T
}

async function collectMarkdownDocs(root: string, dir = root): Promise<string[]> {
  const entries = await fs.readdir(dir, { withFileTypes: true })
  const docs: string[] = []

  for (const entry of entries) {
    const absolute = path.join(dir, entry.name)
    if (entry.isDirectory()) {
      docs.push(...(await collectMarkdownDocs(root, absolute)))
      continue
    }
    if (entry.isFile() && entry.name.endsWith('.md')) {
      docs.push(absolute)
    }
  }

  return docs.sort()
}

function relativePath(root: string, absolutePath: string): string {
  return path.relative(root, absolutePath).split(path.sep).join('/')
}

function extractTitle(body: string, absolutePath: string): string {
  const heading = body.split('\n').find((line) => line.startsWith('# '))
  return heading ? heading.slice(2).trim() : path.basename(absolutePath, '.md')
}

function normalizeRelativeDocTarget(sourceAbsolutePath: string, rawTarget: string, motherDocRoot: string): string | null {
  if (!rawTarget.endsWith('.md')) {
    return null
  }
  const absoluteTarget = path.resolve(path.dirname(sourceAbsolutePath), rawTarget)
  const relative = relativePath(motherDocRoot, absoluteTarget)
  if (relative.startsWith('..')) {
    return null
  }
  return relative
}

function extractMarkdownLinks(body: string, sourceAbsolutePath: string, motherDocRoot: string): string[] {
  const links: string[] = []
  for (const match of body.matchAll(MARKDOWN_LINK_REGEX)) {
    const target = match[1]
    if (!target) {
      continue
    }
    const normalized = normalizeRelativeDocTarget(sourceAbsolutePath, target, motherDocRoot)
    if (normalized) {
      links.push(normalized)
    }
  }
  return uniq(links)
}

function extractIdentifiers(text: string, regex: RegExp): string[] {
  return uniq((text.match(regex) ?? []).map((item) => item.trim()))
}

function hasKeyword(text: string, keywords: string[]): boolean {
  const haystack = text.toLowerCase()
  return keywords.some((keyword) => haystack.includes(keyword.toLowerCase()))
}

function startsWithAny(candidate: string, prefixes: string[]): boolean {
  return prefixes.some((prefix) => candidate === prefix || candidate.startsWith(prefix))
}

function isIndexDoc(docPath: string): boolean {
  return docPath === '00_index.md' || docPath.endsWith('/00_index.md')
}

function buildAdjacency(docs: ProductDocRecord[]): Map<string, string[]> {
  return new Map(
    docs.map((doc) => [
      doc.path,
      uniq([...doc.docLinks, ...doc.markdownLinks]),
    ]),
  )
}

function docCanReachPrefix(
  startDoc: string,
  prefixes: string[],
  adjacency: Map<string, string[]>,
): boolean {
  if (startsWithAny(startDoc, prefixes)) {
    return true
  }

  const queue = [startDoc]
  const visited = new Set<string>(queue)

  while (queue.length > 0) {
    const current = queue.shift()
    if (!current) {
      continue
    }
    const targets = adjacency.get(current) ?? []
    for (const target of targets) {
      if (startsWithAny(target, prefixes)) {
        return true
      }
      if (visited.has(target)) {
        continue
      }
      visited.add(target)
      queue.push(target)
    }
  }

  return false
}

function docHasLinkedPrefix(
  doc: ProductDocRecord,
  prefixes: string[],
  adjacency: Map<string, string[]>,
): boolean {
  if (startsWithAny(doc.path, prefixes)) {
    return true
  }
  return docCanReachPrefix(doc.path, prefixes, adjacency)
}

function extractFrontmatterArray(data: Record<string, unknown>, field: string): string[] {
  const value = data[field]
  if (!Array.isArray(value)) {
    return []
  }
  return value.filter((item): item is string => typeof item === 'string').map((item) => item.trim()).filter(Boolean)
}

async function loadDocs(context: ResolvedProductContext, matrix: GateMatrix): Promise<{
  docs: ProductDocRecord[]
  edges: ProductGraphEdge[]
  errors: LintIssue[]
}> {
  const markdownDocs = await collectMarkdownDocs(context.motherDocRoot)
  const docs: ProductDocRecord[] = []
  const edges: ProductGraphEdge[] = []
  const errors: LintIssue[] = []
  const excludedPrefixes = matrix.excluded_doc_prefixes ?? []

  for (const absolutePath of markdownDocs) {
    const docPath = relativePath(context.motherDocRoot, absolutePath)
    if (startsWithAny(docPath, excludedPrefixes)) {
      continue
    }
    const raw = await fs.readFile(absolutePath, 'utf8')
    const parsed = matter(raw)
    const data = parsed.data as Record<string, unknown>
    const missingFields = matrix.required_frontmatter_keys.filter((field) => !(field in data))
    if (missingFields.length > 0) {
      errors.push({
        code: 'frontmatter.missing_required_keys',
        doc: docPath,
        message: `Missing frontmatter keys: ${missingFields.join(', ')}`,
      })
    }

    const docLinks = extractFrontmatterArray(data, 'doc_links').map((target) => {
      const normalized = normalizeRelativeDocTarget(absolutePath, target, context.motherDocRoot)
      return normalized ?? target
    })
    const markdownLinks = extractMarkdownLinks(parsed.content, absolutePath, context.motherDocRoot)

    docs.push({
      path: docPath,
      docId: typeof data.doc_id === 'string' ? data.doc_id : docPath,
      topic: typeof data.topic === 'string' ? data.topic : extractTitle(parsed.content, absolutePath),
      title: extractTitle(parsed.content, absolutePath),
      body: parsed.content.trim(),
      docLinks: uniq(docLinks.filter(Boolean)),
      markdownLinks,
      frontmatter: data,
    })
  }

  const docSet = new Set(docs.map((doc) => doc.path))
  for (const doc of docs) {
    for (const target of doc.docLinks) {
      if (!docSet.has(target)) {
        errors.push({
          code: 'graph.missing_doc_link_target',
          doc: doc.path,
          message: `doc_links target does not exist under mother_doc: ${target}`,
        })
        continue
      }
      edges.push({ source: doc.path, target, kind: 'doc_link' })
    }
    for (const target of doc.markdownLinks) {
      if (!docSet.has(target)) {
        errors.push({
          code: 'graph.missing_markdown_link_target',
          doc: doc.path,
          message: `markdown link target does not exist under mother_doc: ${target}`,
        })
        continue
      }
      edges.push({ source: doc.path, target, kind: 'markdown_link' })
    }
  }

  return {
    docs,
    edges,
    errors,
  }
}

function buildProfile(docs: ProductDocRecord[], matrix: GateMatrix): ProductMotherDocProfile {
  const docsByPrefix = (prefixes: string[]): ProductDocRecord[] => docs.filter((doc) => startsWithAny(doc.path, prefixes))
  const blueprintDocs = docsByPrefix(matrix.blueprint_doc_prefixes)
  const visualDocs = docsByPrefix(matrix.visual_doc_prefixes)
  const componentDocs = docsByPrefix(matrix.component_doc_prefixes)

  const panelCatalogDoc = docs.find((doc) => doc.path === '05_domain_contracts/20_navigation_canvas_panel_contract.md')
  const panelCatalog = panelCatalogDoc ? extractIdentifiers(panelCatalogDoc.body, PANEL_ID_REGEX) : []
  const panelBlueprintCoverage = uniq(blueprintDocs.flatMap((doc) => extractIdentifiers(doc.body, PANEL_ID_REGEX)))
  const panelComponentCoverage = uniq(componentDocs.flatMap((doc) => extractIdentifiers(doc.body, PANEL_ID_REGEX)))
  const componentIdsDefined = uniq(componentDocs.flatMap((doc) => extractIdentifiers(doc.body, COMPONENT_ID_REGEX)))
  const componentIdsReferenced = uniq(docs.flatMap((doc) => extractIdentifiers(doc.body, COMPONENT_ID_REGEX)))
  const containerIdsDefined = uniq(docs.filter((doc) => doc.path === '04_frontend_contract_layer/35_container_surface_and_slot_matrix.md').flatMap((doc) => extractIdentifiers(doc.body, CONTAINER_ID_REGEX)))
  const containerIdsReferenced = uniq(docs.flatMap((doc) => extractIdentifiers(doc.body, CONTAINER_ID_REGEX)))
  const surfaceIdsDefined = uniq(docs.filter((doc) => doc.path === '04_frontend_contract_layer/65_visual_token_and_surface_matrix.md').flatMap((doc) => extractIdentifiers(doc.body, SURFACE_ID_REGEX)))
  const surfaceIdsReferenced = uniq(docs.flatMap((doc) => extractIdentifiers(doc.body, SURFACE_ID_REGEX)))
  const requirementAtoms = uniq(docs.flatMap((doc) => extractIdentifiers(doc.body, REQUIREMENT_ID_REGEX)))

  return {
    panelCatalog,
    panelBlueprintCoverage,
    panelComponentCoverage,
    componentIdsDefined,
    componentIdsReferenced,
    containerIdsDefined,
    containerIdsReferenced,
    surfaceIdsDefined,
    surfaceIdsReferenced,
    requirementAtoms,
    blueprintDocs: blueprintDocs.map((doc) => doc.path),
    visualDocs: visualDocs.map((doc) => doc.path),
    componentDocs: componentDocs.map((doc) => doc.path),
  }
}

function applySplitRules(doc: ProductDocRecord, matrix: GateMatrix): LintIssue[] {
  const issues: LintIssue[] = []
  const haystack = doc.body.toLowerCase()
  const headingLevelTwoCount = doc.body.split('\n').filter((line) => line.startsWith('## ')).length

  for (const rule of matrix.split_keyword_rules) {
    const hits = rule.keywords.filter((keyword) => haystack.includes(keyword.toLowerCase())).length
    if (hits >= rule.threshold && headingLevelTwoCount >= 3) {
      issues.push({
        code: rule.blocking ? 'split.required' : 'split.warning',
        doc: doc.path,
        message: `${rule.rule_id}: ${rule.message}`,
      })
    }
  }

  return issues
}

function lintDocs(
  docs: ProductDocRecord[],
  matrix: GateMatrix,
  profile: ProductMotherDocProfile,
  baseErrors: LintIssue[],
): { warnings: LintIssue[]; errors: LintIssue[] } {
  const warnings: LintIssue[] = []
  const errors = [...baseErrors]
  const docSet = new Set(docs.map((doc) => doc.path))
  const adjacency = buildAdjacency(docs)
  const keywordGateTargets = new Set([
    '05_domain_contracts/20_navigation_canvas_panel_contract.md',
    '05_domain_contracts/30_requirement_atoms.md',
    '08_dev_execution_plan.md',
  ])
  const keywordGateExemptDocs = new Set(matrix.keyword_gate_exempt_docs ?? [])
  const splitGateExemptDocs = new Set(matrix.split_gate_exempt_docs ?? [])
  const splitGateExemptPrefixes = matrix.split_gate_exempt_prefixes ?? []

  for (const requiredDoc of matrix.required_docs) {
    if (!docSet.has(requiredDoc)) {
      errors.push({
        code: 'coverage.missing_required_doc',
        message: `Required mother_doc file is missing: ${requiredDoc}`,
      })
    }
  }

  for (const panelId of profile.panelCatalog) {
    if (!profile.panelBlueprintCoverage.includes(panelId)) {
      errors.push({
        code: 'blueprint.missing_panel_detail',
        message: `Panel catalog item is missing detailed blueprint coverage: ${panelId}`,
      })
    }
    if (!profile.panelComponentCoverage.includes(panelId)) {
      errors.push({
        code: 'component.missing_panel_component_contract',
        message: `Panel catalog item is missing component property coverage: ${panelId}`,
      })
    }
  }

  for (const componentId of profile.componentIdsReferenced) {
    if (!profile.componentIdsDefined.includes(componentId)) {
      errors.push({
        code: 'component.undefined_reference',
        message: `Component id is referenced but not defined in component docs: ${componentId}`,
      })
    }
  }

  for (const containerId of profile.containerIdsReferenced) {
    if (!profile.containerIdsDefined.includes(containerId)) {
      errors.push({
        code: 'container.undefined_reference',
        message: `Container id is referenced but not defined in container matrix: ${containerId}`,
      })
    }
  }

  for (const surfaceId of profile.surfaceIdsReferenced) {
    if (!profile.surfaceIdsDefined.includes(surfaceId)) {
      errors.push({
        code: 'surface.undefined_reference',
        message: `Surface id is referenced but not defined in visual matrix: ${surfaceId}`,
      })
    }
  }

  for (const doc of docs) {
    if (doc.path.startsWith('12_adrs/')) {
      continue
    }

    const shouldApplyKeywordGate =
      doc.path.startsWith('04_frontend_contract_layer/') || keywordGateTargets.has(doc.path)

    if (!shouldApplyKeywordGate || keywordGateExemptDocs.has(doc.path)) {
      continue
    }

    if (
      hasKeyword(doc.body, matrix.layout_keywords) &&
      !docHasLinkedPrefix(doc, matrix.blueprint_doc_prefixes, adjacency)
    ) {
      errors.push({
        code: 'layout.missing_blueprint_link',
        doc: doc.path,
        message: 'Layout-heavy doc is not linked to blueprint contracts or blueprint detail docs.',
      })
    }

    if (
      hasKeyword(doc.body, matrix.visual_keywords) &&
      !docHasLinkedPrefix(doc, matrix.visual_doc_prefixes, adjacency)
    ) {
      errors.push({
        code: 'visual.missing_surface_link',
        doc: doc.path,
        message: 'Visual-heavy doc is not linked to surface/token contracts.',
      })
    }

    if (
      hasKeyword(doc.body, matrix.component_keywords) &&
      !docHasLinkedPrefix(doc, matrix.component_doc_prefixes, adjacency)
    ) {
      errors.push({
        code: 'component.missing_component_link',
        doc: doc.path,
        message: 'Component-heavy doc is not linked to component registry/property contracts.',
      })
    }

    if (
      isIndexDoc(doc.path) ||
      splitGateExemptDocs.has(doc.path) ||
      startsWithAny(doc.path, splitGateExemptPrefixes)
    ) {
      continue
    }

    for (const issue of applySplitRules(doc, matrix)) {
      if (issue.code === 'split.warning') {
        warnings.push(issue)
      } else {
        errors.push(issue)
      }
    }
  }

  return { warnings, errors }
}

async function writeAssets(
  context: ResolvedProductContext,
  graphPayload: ProductMotherDocGraphPayload,
  lintWarnings: LintIssue[],
  lintErrors: LintIssue[],
): Promise<{ graphPath: string; profilePath: string; reportPath: string }> {
  await fs.mkdir(context.graphRoot, { recursive: true })
  const graphPath = path.join(context.graphRoot, 'frontend_mother_doc_graph.json')
  const profilePath = path.join(context.graphRoot, 'frontend_mother_doc_lint_profile.json')
  const reportPath = path.join(context.graphRoot, 'frontend_mother_doc_lint_report.json')

  await fs.writeFile(graphPath, `${JSON.stringify({
    generated_at: new Date().toISOString(),
    docs_root: context.docsRoot,
    mother_doc_root: context.motherDocRoot,
    graph: graphPayload.graph,
    summary: graphPayload.summary,
  }, null, 2)}\n`, 'utf8')
  await fs.writeFile(profilePath, `${JSON.stringify({
    generated_at: new Date().toISOString(),
    docs_root: context.docsRoot,
    profile: graphPayload.profile,
  }, null, 2)}\n`, 'utf8')
  await fs.writeFile(reportPath, `${JSON.stringify({
    generated_at: new Date().toISOString(),
    docs_root: context.docsRoot,
    status: lintErrors.length > 0 ? 'fail' : lintWarnings.length > 0 ? 'pass_with_warnings' : 'pass',
    warnings: lintWarnings,
    errors: lintErrors,
  }, null, 2)}\n`, 'utf8')

  return { graphPath, profilePath, reportPath }
}

export async function buildProductMotherDocGraph(
  docsRootInput: string,
  options: { writeAssets?: boolean } = {},
): Promise<ProductMotherDocGraphPayload> {
  const context = await resolveProductContext(docsRootInput)
  const matrix = await readJsonFile<GateMatrix>(context.matrixPath)
  const { docs, edges, errors } = await loadDocs(context, matrix)
  const profile = buildProfile(docs, matrix)
  const warnings: LintIssue[] = []
  const status: GateStatus = errors.length > 0 ? 'fail' : 'pass'

  const payload: ProductMotherDocGraphPayload = {
    status,
    docsRoot: context.docsRoot,
    motherDocRoot: context.motherDocRoot,
    graphRoot: context.graphRoot,
    matrixName: matrix.matrix_name,
    summary: {
      docCount: docs.length,
      edgeCount: edges.length,
      errorCount: errors.length,
      warningCount: warnings.length,
    },
    graph: {
      nodes: docs.map((doc) => ({
        path: doc.path,
        docId: doc.docId,
        topic: doc.topic,
        title: doc.title,
        docLinkCount: doc.docLinks.length,
        markdownLinkCount: doc.markdownLinks.length,
      })),
      edges,
    },
    profile,
    warnings,
    errors,
  }

  if (options.writeAssets) {
    await writeAssets(context, payload, warnings, errors)
  }

  return payload
}

export async function lintProductMotherDoc(
  docsRootInput: string,
  options: { writeAssets?: boolean } = {},
): Promise<ProductMotherDocLintPayload> {
  const context = await resolveProductContext(docsRootInput)
  const matrix = await readJsonFile<GateMatrix>(context.matrixPath)
  const { docs, edges, errors: baseErrors } = await loadDocs(context, matrix)
  const profile = buildProfile(docs, matrix)
  const { warnings, errors } = lintDocs(docs, matrix, profile, baseErrors)
  const status: GateStatus = errors.length > 0 ? 'fail' : warnings.length > 0 ? 'pass_with_warnings' : 'pass'

  const payload: ProductMotherDocLintPayload = {
    status,
    docsRoot: context.docsRoot,
    motherDocRoot: context.motherDocRoot,
    graphRoot: context.graphRoot,
    matrixName: matrix.matrix_name,
    summary: {
      docCount: docs.length,
      edgeCount: edges.length,
      errorCount: errors.length,
      warningCount: warnings.length,
    },
    graph: {
      nodes: docs.map((doc) => ({
        path: doc.path,
        docId: doc.docId,
        topic: doc.topic,
        title: doc.title,
        docLinkCount: doc.docLinks.length,
        markdownLinkCount: doc.markdownLinks.length,
      })),
      edges,
    },
    profile,
    warnings,
    errors,
  }

  if (options.writeAssets) {
    payload.writtenAssets = await writeAssets(context, payload, warnings, errors)
  }

  return payload
}
