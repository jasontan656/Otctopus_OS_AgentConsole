import path from 'node:path'
import { promises as fs } from 'node:fs'
import matter from 'gray-matter'
import YAML from 'yaml'
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
  localCoordinateSpaces: string[]
  panelBlueprintContracts: string[]
  viewportBlueprintDocs: string[]
}

interface SpatialRectNode {
  nodeId: string
  parentId: string | null
  x: number | null
  y: number | null
  w: number | null
  h: number | null
  overlapTargets: string[]
  overlapMode: string | null
  collisionPolicy: string | null
  relationRefs: string[]
  elevation: number | null
  allowOverlap: boolean
  missingKeys: string[]
}

interface ParsedPanelBlueprint {
  sourceDoc: string
  panelId: string
  bodyContainerId: string
  localCoordinateSpace: string
  frameWidth: number | null
  frameHeight: number | null
  overflowPolicy: string | null
  interactionStates: string[]
  missingKeys: string[]
  responsiveVariants: Record<string, {
    gridSpan: number | null
    frameWidth: number | null
    frameHeight: number | null
  }>
  nodes: SpatialRectNode[]
}

interface LocalCoordinateSpaceContract {
  sourceDoc: string
  id: string
  width: number | null
  height: number | null
  overflowPolicy: string | null
  missingKeys: string[]
}

interface ParsedViewportScene {
  sourceDoc: string
  viewportId: string
  viewportWidth: number | null
  viewportHeight: number | null
  nodes: SpatialRectNode[]
  missingKeys: string[]
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
const SPATIAL_NODE_REQUIRED_KEYS = [
  'node_id',
  'parent_id',
  'x',
  'y',
  'w',
  'h',
  'allow_overlap',
  'overlap_targets',
  'overlap_mode',
  'collision_policy',
  'relation_refs',
  'elevation',
]
const PANEL_BLUEPRINT_REQUIRED_KEYS = [
  'panel_id',
  'body_container_id',
  'local_coordinate_space',
  'frame_width',
  'frame_height',
  'overflow_policy',
  'interaction_states',
  'responsive_variants',
  'nodes',
]
const LOCAL_COORDINATE_SPACE_REQUIRED_KEYS = [
  'local_coordinate_space_id',
  'width',
  'height',
  'overflow_policy',
]
const VIEWPORT_REQUIRED_KEYS = [
  'viewport_id',
  'viewport_width',
  'viewport_height',
]

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

function extractYamlBlocks(body: string): string[] {
  const blocks: string[] = []
  const regex = /```yaml\s*\n([\s\S]*?)```/g
  for (const match of body.matchAll(regex)) {
    const candidate = match[1]?.trim()
    if (candidate) {
      blocks.push(candidate)
    }
  }
  return blocks
}

function parseYamlDocument(source: string): unknown | null {
  try {
    return YAML.parse(source)
  } catch {
    return null
  }
}

function toRecord(value: unknown): Record<string, unknown> | null {
  return value !== null && typeof value === 'object' && !Array.isArray(value)
    ? (value as Record<string, unknown>)
    : null
}

function toNumber(value: unknown): number | null {
  return typeof value === 'number' && Number.isFinite(value) ? value : null
}

function toStringArray(value: unknown): string[] {
  if (!Array.isArray(value)) {
    return []
  }
  return value.filter((item): item is string => typeof item === 'string').map((item) => item.trim()).filter(Boolean)
}

function hasOwnField(record: Record<string, unknown>, field: string): boolean {
  return Object.prototype.hasOwnProperty.call(record, field)
}

function missingRecordKeys(record: Record<string, unknown>, requiredKeys: string[]): string[] {
  return requiredKeys.filter((field) => !hasOwnField(record, field))
}

function parseSpatialNode(value: unknown): SpatialRectNode | null {
  const record = toRecord(value)
  if (!record || typeof record.node_id !== 'string') {
    return null
  }
  return {
    nodeId: record.node_id,
    parentId: typeof record.parent_id === 'string' ? record.parent_id : null,
    x: toNumber(record.x),
    y: toNumber(record.y),
    w: toNumber(record.w),
    h: toNumber(record.h),
    overlapTargets: toStringArray(record.overlap_targets),
    overlapMode: typeof record.overlap_mode === 'string' ? record.overlap_mode : null,
    collisionPolicy: typeof record.collision_policy === 'string' ? record.collision_policy : null,
    relationRefs: toStringArray(record.relation_refs),
    elevation: toNumber(record.elevation),
    allowOverlap: record.allow_overlap === true,
    missingKeys: missingRecordKeys(record, SPATIAL_NODE_REQUIRED_KEYS),
  }
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
  const localCoordinateSpaces = uniq(
    docs.flatMap((doc) =>
      extractYamlBlocks(doc.body)
        .map(parseYamlDocument)
        .flatMap((parsed) => {
          const record = toRecord(parsed)
          const spaces = Array.isArray(record?.local_coordinate_spaces) ? record.local_coordinate_spaces : []
          return spaces.flatMap((item) => {
            const space = toRecord(item)
            return typeof space?.local_coordinate_space_id === 'string' ? [space.local_coordinate_space_id] : []
          })
        }),
    ),
  )
  const panelBlueprintContracts = uniq(
    docs.flatMap((doc) =>
      extractYamlBlocks(doc.body)
        .map(parseYamlDocument)
        .flatMap((parsed) => {
          const blueprint = toRecord(toRecord(parsed)?.panel_blueprint)
          return typeof blueprint?.panel_id === 'string' ? [blueprint.panel_id] : []
        }),
    ),
  )
  const viewportBlueprintDocs = docs
    .filter((doc) =>
      extractYamlBlocks(doc.body).some((block) => {
        const parsed = parseYamlDocument(block)
        const record = toRecord(parsed)
        return Boolean(record?.viewport && Array.isArray(record.nodes))
      }),
    )
    .map((doc) => doc.path)

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
    localCoordinateSpaces,
    panelBlueprintContracts,
    viewportBlueprintDocs,
  }
}

function collectPanelBlueprints(docs: ProductDocRecord[]): ParsedPanelBlueprint[] {
  const blueprints: ParsedPanelBlueprint[] = []

  for (const doc of docs) {
    for (const block of extractYamlBlocks(doc.body)) {
      const parsed = parseYamlDocument(block)
      const blueprint = toRecord(toRecord(parsed)?.panel_blueprint)
      if (!blueprint || typeof blueprint.panel_id !== 'string') {
        continue
      }

      const responsiveVariantsRecord = toRecord(blueprint.responsive_variants) ?? {}
      const responsiveVariants = Object.fromEntries(
        Object.entries(responsiveVariantsRecord).map(([variantKey, rawValue]) => {
          const variant = toRecord(rawValue) ?? {}
          return [
            variantKey,
            {
              gridSpan: toNumber(variant.grid_span),
              frameWidth: toNumber(variant.frame_width),
              frameHeight: toNumber(variant.frame_height),
            },
          ]
        }),
      )

      blueprints.push({
        sourceDoc: doc.path,
        panelId: blueprint.panel_id,
        bodyContainerId: typeof blueprint.body_container_id === 'string' ? blueprint.body_container_id : '',
        localCoordinateSpace: typeof blueprint.local_coordinate_space === 'string' ? blueprint.local_coordinate_space : '',
        frameWidth: toNumber(blueprint.frame_width),
        frameHeight: toNumber(blueprint.frame_height),
        overflowPolicy: typeof blueprint.overflow_policy === 'string' ? blueprint.overflow_policy : null,
        interactionStates: toStringArray(blueprint.interaction_states),
        missingKeys: missingRecordKeys(blueprint, PANEL_BLUEPRINT_REQUIRED_KEYS),
        responsiveVariants,
        nodes: Array.isArray(blueprint.nodes)
          ? blueprint.nodes.map(parseSpatialNode).filter((node): node is SpatialRectNode => Boolean(node))
          : [],
      })
    }
  }

  return blueprints
}

function collectLocalCoordinateSpaces(docs: ProductDocRecord[]): LocalCoordinateSpaceContract[] {
  const spaces: LocalCoordinateSpaceContract[] = []

  for (const doc of docs) {
    for (const block of extractYamlBlocks(doc.body)) {
      const parsed = parseYamlDocument(block)
      const record = toRecord(parsed)
      const rawSpaces = Array.isArray(record?.local_coordinate_spaces) ? record.local_coordinate_spaces : []
      for (const rawSpace of rawSpaces) {
        const space = toRecord(rawSpace)
        if (!space || typeof space.local_coordinate_space_id !== 'string') {
          continue
        }
        spaces.push({
          sourceDoc: doc.path,
          id: space.local_coordinate_space_id,
          width: toNumber(space.width),
          height: toNumber(space.height),
          overflowPolicy: typeof space.overflow_policy === 'string' ? space.overflow_policy : null,
          missingKeys: missingRecordKeys(space, LOCAL_COORDINATE_SPACE_REQUIRED_KEYS),
        })
      }
    }
  }

  return spaces
}

function collectViewportScenes(docs: ProductDocRecord[]): ParsedViewportScene[] {
  const scenes: ParsedViewportScene[] = []

  for (const doc of docs) {
    for (const block of extractYamlBlocks(doc.body)) {
      const parsed = parseYamlDocument(block)
      const record = toRecord(parsed)
      const viewport = toRecord(record?.viewport)
      if (!viewport || !Array.isArray(record?.nodes)) {
        continue
      }
      scenes.push({
        sourceDoc: doc.path,
        viewportId: typeof viewport.viewport_id === 'string' ? viewport.viewport_id : 'viewport',
        viewportWidth: toNumber(viewport.viewport_width),
        viewportHeight: toNumber(viewport.viewport_height),
        nodes: record.nodes.map(parseSpatialNode).filter((node): node is SpatialRectNode => Boolean(node)),
        missingKeys: missingRecordKeys(viewport, VIEWPORT_REQUIRED_KEYS),
      })
    }
  }

  return scenes
}

function rectsOverlap(a: SpatialRectNode, b: SpatialRectNode): boolean {
  if (a.x === null || a.y === null || a.w === null || a.h === null || b.x === null || b.y === null || b.w === null || b.h === null) {
    return false
  }
  return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y
}

function validateBlueprintGeometry(
  panelBlueprints: ParsedPanelBlueprint[],
  localSpaces: LocalCoordinateSpaceContract[],
): LintIssue[] {
  const issues: LintIssue[] = []
  const localSpaceMap = new Map(localSpaces.map((space) => [space.id, space]))

  for (const localSpace of localSpaces) {
    if (localSpace.missingKeys.length > 0) {
      issues.push({
        code: 'blueprint.local_coordinate_space_missing_required_fields',
        doc: localSpace.sourceDoc,
        message: `Local coordinate space is missing required fields: ${localSpace.id} -> ${localSpace.missingKeys.join(', ')}`,
      })
    }
  }

  for (const blueprint of panelBlueprints) {
    if (blueprint.missingKeys.length > 0) {
      issues.push({
        code: 'blueprint.missing_required_fields',
        doc: blueprint.sourceDoc,
        message: `Panel blueprint is missing required fields: ${blueprint.panelId} -> ${blueprint.missingKeys.join(', ')}`,
      })
    }
    if (!blueprint.bodyContainerId) {
      issues.push({
        code: 'blueprint.missing_body_container',
        doc: blueprint.sourceDoc,
        message: `Panel blueprint is missing body_container_id: ${blueprint.panelId}`,
      })
    }
    if (!blueprint.localCoordinateSpace) {
      issues.push({
        code: 'blueprint.missing_local_coordinate_space',
        doc: blueprint.sourceDoc,
        message: `Panel blueprint is missing local_coordinate_space: ${blueprint.panelId}`,
      })
    }

    const localSpace = blueprint.localCoordinateSpace ? localSpaceMap.get(blueprint.localCoordinateSpace) : null
    if (blueprint.localCoordinateSpace && !localSpace) {
      issues.push({
        code: 'blueprint.undefined_local_coordinate_space',
        doc: blueprint.sourceDoc,
        message: `Panel blueprint references undefined local coordinate space: ${blueprint.panelId} -> ${blueprint.localCoordinateSpace}`,
      })
    }

    if (blueprint.frameWidth === null || blueprint.frameHeight === null) {
      issues.push({
        code: 'blueprint.missing_frame_dimensions',
        doc: blueprint.sourceDoc,
        message: `Panel blueprint is missing frame dimensions: ${blueprint.panelId}`,
      })
      continue
    }

    if (localSpace && (localSpace.width !== blueprint.frameWidth || localSpace.height !== blueprint.frameHeight)) {
      issues.push({
        code: 'blueprint.frame_space_mismatch',
        doc: blueprint.sourceDoc,
        message: `Panel blueprint frame does not match declared local coordinate space: ${blueprint.panelId}`,
      })
    }

    if (!blueprint.responsiveVariants.desktop_default) {
      issues.push({
        code: 'blueprint.missing_default_variant',
        doc: blueprint.sourceDoc,
        message: `Panel blueprint is missing desktop_default responsive variant: ${blueprint.panelId}`,
      })
    }

    if (blueprint.interactionStates.includes('focus') && !blueprint.responsiveVariants.panel_focus) {
      issues.push({
        code: 'blueprint.missing_focus_variant',
        doc: blueprint.sourceDoc,
        message: `Focus-capable panel blueprint is missing panel_focus responsive variant: ${blueprint.panelId}`,
      })
    }

    for (const [variantKey, variant] of Object.entries(blueprint.responsiveVariants)) {
      if (variant.frameWidth === null || variant.frameHeight === null) {
        issues.push({
          code: 'blueprint.variant_missing_dimensions',
          doc: blueprint.sourceDoc,
          message: `Responsive variant is missing frame dimensions: ${blueprint.panelId} -> ${variantKey}`,
        })
      }
    }

    const nodesByParent = new Map<string, SpatialRectNode[]>()
    for (const node of blueprint.nodes) {
      if (node.missingKeys.length > 0) {
        issues.push({
          code: 'blueprint.node_missing_required_fields',
          doc: blueprint.sourceDoc,
          message: `Blueprint node is missing required fields: ${blueprint.panelId} -> ${node.nodeId} -> ${node.missingKeys.join(', ')}`,
        })
      }
      if (node.x === null || node.y === null || node.w === null || node.h === null) {
        issues.push({
          code: 'blueprint.node_missing_geometry',
          doc: blueprint.sourceDoc,
          message: `Blueprint node is missing geometry: ${blueprint.panelId} -> ${node.nodeId}`,
        })
        continue
      }
      if (node.x < 0 || node.y < 0 || node.w <= 0 || node.h <= 0) {
        issues.push({
          code: 'blueprint.node_invalid_geometry',
          doc: blueprint.sourceDoc,
          message: `Blueprint node has invalid geometry: ${blueprint.panelId} -> ${node.nodeId}`,
        })
      }
      if (node.x + node.w > blueprint.frameWidth || node.y + node.h > blueprint.frameHeight) {
        issues.push({
          code: 'blueprint.node_out_of_bounds',
          doc: blueprint.sourceDoc,
          message: `Blueprint node exceeds frame bounds: ${blueprint.panelId} -> ${node.nodeId}`,
        })
      }
      const siblings = nodesByParent.get(node.parentId ?? '__missing_parent__') ?? []
      siblings.push(node)
      nodesByParent.set(node.parentId ?? '__missing_parent__', siblings)
    }

    for (const siblings of nodesByParent.values()) {
      for (let index = 0; index < siblings.length; index += 1) {
        for (let otherIndex = index + 1; otherIndex < siblings.length; otherIndex += 1) {
          const current = siblings[index]
          const peer = siblings[otherIndex]
          if (!current || !peer) {
            continue
          }
          if (!rectsOverlap(current, peer)) {
            continue
          }
          if (!current.allowOverlap && !peer.allowOverlap) {
            issues.push({
              code: 'blueprint.unexpected_overlap',
              doc: blueprint.sourceDoc,
              message: `Sibling blueprint nodes overlap without explicit allow_overlap: ${blueprint.panelId} -> ${current.nodeId} / ${peer.nodeId}`,
            })
            continue
          }

          for (const node of [current, peer]) {
            const otherNodeId = node.nodeId === current.nodeId ? peer.nodeId : current.nodeId
            if (!node.allowOverlap) {
              continue
            }
            if (!node.overlapMode) {
              issues.push({
                code: 'blueprint.overlap_missing_mode',
                doc: blueprint.sourceDoc,
                message: `Overlapping node is missing overlap_mode: ${blueprint.panelId} -> ${node.nodeId}`,
              })
            }
            if (!node.collisionPolicy) {
              issues.push({
                code: 'blueprint.overlap_missing_collision_policy',
                doc: blueprint.sourceDoc,
                message: `Overlapping node is missing collision_policy: ${blueprint.panelId} -> ${node.nodeId}`,
              })
            }
            if (node.collisionPolicy === 'forbid') {
              issues.push({
                code: 'blueprint.overlap_policy_conflict',
                doc: blueprint.sourceDoc,
                message: `Overlapping node declares allow_overlap but collision_policy forbids overlap: ${blueprint.panelId} -> ${node.nodeId}`,
              })
            }
            if (node.overlapTargets.length > 0 && !node.overlapTargets.includes(otherNodeId)) {
              issues.push({
                code: 'blueprint.overlap_target_mismatch',
                doc: blueprint.sourceDoc,
                message: `Overlapping node does not allow this peer in overlap_targets: ${blueprint.panelId} -> ${node.nodeId} / ${otherNodeId}`,
              })
            }
          }
        }
      }
    }
  }

  return issues
}

function validateViewportScenes(scenes: ParsedViewportScene[]): LintIssue[] {
  const issues: LintIssue[] = []

  for (const scene of scenes) {
    if (scene.missingKeys.length > 0) {
      issues.push({
        code: 'viewport.missing_required_fields',
        doc: scene.sourceDoc,
        message: `Viewport blueprint is missing required fields: ${scene.viewportId} -> ${scene.missingKeys.join(', ')}`,
      })
    }
    if (scene.viewportWidth === null || scene.viewportHeight === null) {
      issues.push({
        code: 'viewport.missing_dimensions',
        doc: scene.sourceDoc,
        message: `Viewport blueprint is missing viewport dimensions: ${scene.viewportId}`,
      })
      continue
    }

    const bounds = new Map<string, { x: number; y: number; w: number; h: number }>()
    bounds.set('viewport', { x: 0, y: 0, w: scene.viewportWidth, h: scene.viewportHeight })
    const nodesByParent = new Map<string, SpatialRectNode[]>()

    for (const node of scene.nodes) {
      if (node.missingKeys.length > 0) {
        issues.push({
          code: 'viewport.node_missing_required_fields',
          doc: scene.sourceDoc,
          message: `Viewport node is missing required fields: ${scene.viewportId} -> ${node.nodeId} -> ${node.missingKeys.join(', ')}`,
        })
      }
      if (node.x === null || node.y === null || node.w === null || node.h === null) {
        issues.push({
          code: 'viewport.node_missing_geometry',
          doc: scene.sourceDoc,
          message: `Viewport node is missing geometry: ${scene.viewportId} -> ${node.nodeId}`,
        })
        continue
      }
      const parentBounds = bounds.get(node.parentId ?? '__missing_parent__')
      if (!parentBounds) {
        issues.push({
          code: 'viewport.undefined_parent',
          doc: scene.sourceDoc,
          message: `Viewport node references unknown parent: ${scene.viewportId} -> ${node.nodeId} -> ${node.parentId}`,
        })
        continue
      }
      if (node.x < 0 || node.y < 0 || node.w <= 0 || node.h <= 0) {
        issues.push({
          code: 'viewport.node_invalid_geometry',
          doc: scene.sourceDoc,
          message: `Viewport node has invalid geometry: ${scene.viewportId} -> ${node.nodeId}`,
        })
      }
      if (node.x + node.w > parentBounds.w || node.y + node.h > parentBounds.h) {
        issues.push({
          code: 'viewport.node_out_of_bounds',
          doc: scene.sourceDoc,
          message: `Viewport node exceeds parent bounds: ${scene.viewportId} -> ${node.nodeId}`,
        })
      }
      bounds.set(node.nodeId, { x: node.x, y: node.y, w: node.w, h: node.h })
      const siblings = nodesByParent.get(node.parentId ?? '__missing_parent__') ?? []
      siblings.push(node)
      nodesByParent.set(node.parentId ?? '__missing_parent__', siblings)
    }

    for (const siblings of nodesByParent.values()) {
      for (let index = 0; index < siblings.length; index += 1) {
        for (let otherIndex = index + 1; otherIndex < siblings.length; otherIndex += 1) {
          const current = siblings[index]
          const peer = siblings[otherIndex]
          if (!current || !peer) {
            continue
          }
          if (!rectsOverlap(current, peer)) {
            continue
          }
          if (!current.allowOverlap && !peer.allowOverlap) {
            issues.push({
              code: 'viewport.unexpected_overlap',
              doc: scene.sourceDoc,
              message: `Viewport sibling nodes overlap without explicit allow_overlap: ${scene.viewportId} -> ${current.nodeId} / ${peer.nodeId}`,
            })
            continue
          }

          for (const node of [current, peer]) {
            const otherNodeId = node.nodeId === current.nodeId ? peer.nodeId : current.nodeId
            if (!node.allowOverlap) {
              continue
            }
            if (!node.overlapMode) {
              issues.push({
                code: 'viewport.overlap_missing_mode',
                doc: scene.sourceDoc,
                message: `Overlapping viewport node is missing overlap_mode: ${scene.viewportId} -> ${node.nodeId}`,
              })
            }
            if (!node.collisionPolicy) {
              issues.push({
                code: 'viewport.overlap_missing_collision_policy',
                doc: scene.sourceDoc,
                message: `Overlapping viewport node is missing collision_policy: ${scene.viewportId} -> ${node.nodeId}`,
              })
            }
            if (node.collisionPolicy === 'forbid') {
              issues.push({
                code: 'viewport.overlap_policy_conflict',
                doc: scene.sourceDoc,
                message: `Overlapping viewport node declares allow_overlap but collision_policy forbids overlap: ${scene.viewportId} -> ${node.nodeId}`,
              })
            }
            if (node.overlapTargets.length > 0 && !node.overlapTargets.includes(otherNodeId)) {
              issues.push({
                code: 'viewport.overlap_target_mismatch',
                doc: scene.sourceDoc,
                message: `Overlapping viewport node does not allow this peer in overlap_targets: ${scene.viewportId} -> ${node.nodeId} / ${otherNodeId}`,
              })
            }
          }
        }
      }
    }
  }

  return issues
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
  const panelBlueprints = collectPanelBlueprints(docs)
  const localCoordinateSpaces = collectLocalCoordinateSpaces(docs)
  const viewportScenes = collectViewportScenes(docs)
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

  errors.push(...validateBlueprintGeometry(panelBlueprints, localCoordinateSpaces))
  errors.push(...validateViewportScenes(viewportScenes))

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
