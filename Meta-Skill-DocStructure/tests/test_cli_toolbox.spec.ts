import { mkdtemp, mkdir, readFile, rm, writeFile } from 'node:fs/promises'
import path from 'node:path'
import os from 'node:os'
import { afterEach, describe, expect, it } from 'vitest'
import { buildDocGraphWorkspace, loadRuntimeContract, rebuildSelfGraph } from '../src/lib/docstructure.js'

const tempDirs: string[] = []

async function createTempSkill(): Promise<string> {
  const tempRoot = await mkdtemp(path.join(os.tmpdir(), 'docstructure-'))
  tempDirs.push(tempRoot)
  return tempRoot
}

afterEach(async () => {
  for (const tempDir of tempDirs.splice(0, tempDirs.length)) {
    await rm(tempDir, { recursive: true, force: true })
  }
})

describe('Meta-Skill-DocStructure TS runtime', () => {
  it('loads the runtime contract', async () => {
    const contract = await loadRuntimeContract(path.resolve(__dirname, '..'))
    expect(contract.contract_name).toBe('META_SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT')
    expect(contract.semantic_split_contract.navigation_model).toBe('tree_first_graph_second')
  })

  it('builds a doc graph workspace for the current skill', async () => {
    const workspace = await buildDocGraphWorkspace(path.resolve(__dirname, '..'))
    expect(['pass', 'pass_with_warnings']).toContain(workspace.status)
    expect(workspace.graph.nodes.length).toBeGreaterThan(0)
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
})
