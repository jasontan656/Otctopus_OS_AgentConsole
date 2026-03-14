import { mkdtemp, mkdir, readFile, rm, writeFile } from 'node:fs/promises'
import path from 'node:path'
import os from 'node:os'
import { afterEach, describe, expect, it } from 'vitest'
import {
  buildDocGraphWorkspace,
  loadRuntimeContract,
  rebuildSelfGraph,
  registerSplitDecision,
} from '../src/lib/docstructure.js'

const tempDirs: string[] = []

async function createTempSkill(): Promise<string> {
  const tempRoot = await mkdtemp(path.join(os.tmpdir(), 'docstructure-'))
  tempDirs.push(tempRoot)
  return tempRoot
}

async function createSplitCandidateSkill(): Promise<string> {
  const skillRoot = await createTempSkill()
  await mkdir(path.join(skillRoot, 'docs'), { recursive: true })
  await mkdir(path.join(skillRoot, 'assets', 'runtime'), { recursive: true })
  await writeFile(
    path.join(skillRoot, 'assets', 'runtime', 'split_decision_registry.json'),
    JSON.stringify({
      registry_name: 'META_SKILL_DOCSTRUCTURE_SPLIT_DECISION_REGISTRY',
      registry_version: 'v1',
      entries: [],
    }, null, 2),
    'utf8',
  )
  await writeFile(
    path.join(skillRoot, 'SKILL.md'),
    `---\nname: "temp-skill"\ndescription: "temporary skill"\nmetadata:\n  doc_structure:\n    doc_id: "skill.entry"\n    doc_type: "skill_facade"\n    topic: "temp facade"\n    anchors:\n      - target: "docs/guide.md"\n        relation: "details"\n        direction: "downstream"\n        reason: "guide expands facade"\n---\n\n# Temp Skill\n`,
    'utf8',
  )
  await writeFile(
    path.join(skillRoot, 'docs', 'guide.md'),
    `---\ndoc_id: "docs.guide"\ndoc_type: "topic_atom"\ntopic: "guide"\nanchors:\n  - target: "../SKILL.md"\n    relation: "belongs_to"\n    direction: "upstream"\n    reason: "guide belongs to the facade"\n---\n\n# Read 和 Write\n\n## 定义\n说明。\n`,
    'utf8',
  )
  return skillRoot
}

async function createGuideOnlySkill(): Promise<string> {
  const skillRoot = await createTempSkill()
  await writeFile(
    path.join(skillRoot, 'SKILL.md'),
    `---\nname: "temp-guide-only"\ndescription: "temporary guide only skill"\nskill_mode: "guide_only"\n---\n\n# Temp Guide Only\n\n## 1. 技能定位\n- all guidance lives here\n`,
    'utf8',
  )
  return skillRoot
}

afterEach(async () => {
  for (const tempDir of tempDirs.splice(0, tempDirs.length)) {
    await rm(tempDir, { recursive: true, force: true })
  }
})

describe('SkillsManager-Doc-Structure TS runtime', () => {
  it('loads the runtime contract', async () => {
    const contract = await loadRuntimeContract(path.resolve(__dirname, '..'))
    expect(contract.contract_name).toBe('META_SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT')
    expect(contract.semantic_split_contract.navigation_model).toBe('tree_first_graph_second')
    expect(contract.knowledge_tracks.rules_track_entry).toBe('references/rules/00_RULE_SYSTEM_INDEX.md')
    expect(contract.workflow_tracks.single_doc_workflow_entry).toBe('references/workflows/30_SINGLE_DOC_AUTHORING_FLOW.md')
    expect(contract.frontmatter_contract.optional_fields).toContain('node_role')
  })

  it('builds a doc graph workspace for the current skill', async () => {
    const workspace = await buildDocGraphWorkspace(path.resolve(__dirname, '..'))
    expect(workspace.status).toBe('pass')
    expect(workspace.applicability).toBe('enforced')
    expect(workspace.graph.nodes.length).toBeGreaterThan(0)
    expect(workspace.graph.nodes.some((node) => node.path === 'references/fewshot/00_FEWSHOT_INDEX.md')).toBe(true)
  })

  it('skips graph lint for guide_only skills', async () => {
    const skillRoot = await createGuideOnlySkill()
    const contract = await loadRuntimeContract(skillRoot)
    const workspace = await buildDocGraphWorkspace(skillRoot)

    expect(contract.target_skill_mode).toBe('guide_only')
    expect(contract.applicability).toBe('skipped_for_guide_only')
    expect(workspace.status).toBe('skipped')
    expect(workspace.applicability).toBe('skipped_guide_only')
    expect(workspace.summary.nodeCount).toBe(0)
    expect(workspace.notes[0]).toContain('guide_only')
  })

  it('captures optional node metadata fields when present', async () => {
    const skillRoot = await createTempSkill()
    await mkdir(path.join(skillRoot, 'docs'), { recursive: true })
    await writeFile(
      path.join(skillRoot, 'SKILL.md'),
      `---\nname: "temp-skill"\ndescription: "temporary skill"\nmetadata:\n  doc_structure:\n    doc_id: "skill.entry"\n    doc_type: "skill_facade"\n    topic: "temp facade"\n    anchors:\n      - target: "docs/guide.md"\n        relation: "details"\n        direction: "downstream"\n        reason: "guide expands facade"\n---\n\n# Temp Skill\n`,
      'utf8',
    )
    await writeFile(
      path.join(skillRoot, 'docs', 'guide.md'),
      `---\ndoc_id: "docs.guide"\ndoc_type: "topic_atom"\ntopic: "guide"\nnode_role: "topic_atom"\ndomain_type: "example"\nanchors:\n  - target: "../SKILL.md"\n    relation: "belongs_to"\n    direction: "upstream"\n    reason: "guide belongs to the facade"\n---\n\n# Guide\n`,
      'utf8',
    )

    const workspace = await buildDocGraphWorkspace(skillRoot)
    const guide = workspace.graph.nodes.find((node) => node.path === 'docs/guide.md')
    expect(guide?.nodeRole).toBe('topic_atom')
    expect(guide?.domainType).toBe('example')
  })

  it('fails when a document loses its anchors', async () => {
    const skillRoot = await createTempSkill()
    await mkdir(path.join(skillRoot, 'docs'))
    await writeFile(
      path.join(skillRoot, 'SKILL.md'),
      `---\nname: "temp-skill"\ndescription: "temporary skill"\nmetadata:\n  doc_structure:\n    doc_id: "skill.entry"\n    doc_type: "skill_facade"\n    topic: "temp facade"\n    anchors:\n      - target: "docs/guide.md"\n        relation: "details"\n        direction: "downstream"\n        reason: "guide expands facade"\n---\n\n# Temp Skill\n`,
      'utf8',
    )
    await writeFile(
      path.join(skillRoot, 'docs', 'guide.md'),
      `---\ndoc_id: "docs.guide"\ndoc_type: "guide"\ntopic: "guide"\nanchors: []\n---\n\n# Guide\n`,
      'utf8',
    )

    const workspace = await buildDocGraphWorkspace(skillRoot)
    expect(workspace.status).toBe('fail')
    expect(workspace.errors.length).toBeGreaterThan(0)
  })

  it('rewrites self graph snapshot', async () => {
    const { graphPath } = await rebuildSelfGraph(path.resolve(__dirname, '..'))
    const snapshot = JSON.parse(await readFile(graphPath, 'utf8')) as { graph_version: string }
    expect(snapshot.graph_version).toBe('v2')
  })

  it('fails when a split candidate requires user decision', async () => {
    const skillRoot = await createSplitCandidateSkill()
    const workspace = await buildDocGraphWorkspace(skillRoot)
    expect(workspace.status).toBe('fail')
    expect(workspace.summary.blockingSplitCandidateCount).toBeGreaterThan(0)
    expect(workspace.splitCandidates[0]?.decisionStatus).toBe('requires_decision')
  })

  it('accepts a split candidate after writing a registry decision', async () => {
    const skillRoot = await createSplitCandidateSkill()
    await registerSplitDecision(skillRoot, 'docs/guide.md', 'title_conjunction_zh', 'accepted', 'user keeps this bundled title')
    const workspace = await buildDocGraphWorkspace(skillRoot)
    expect(workspace.status).toBe('pass')
    expect(workspace.summary.blockingSplitCandidateCount).toBe(0)
    expect(workspace.splitCandidates[0]?.decisionStatus).toBe('accepted')
  })
})
