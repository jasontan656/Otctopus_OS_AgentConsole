import { mkdtemp, mkdir, readFile, rm, writeFile } from 'node:fs/promises'
import path from 'node:path'
import os from 'node:os'
import { afterEach, describe, expect, it } from 'vitest'
import { buildPreviewPayload, loadRuntimeContract, rebuildSelfGraph } from '../src/lib/docstructure.js'

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
  })

  it('builds a preview payload for the current skill', async () => {
    const payload = await buildPreviewPayload(path.resolve(__dirname, '..'))
    expect(['pass', 'pass_with_warnings']).toContain(payload.status)
    expect(payload.view.entryPath).toBe('SKILL.md')
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

    const payload = await buildPreviewPayload(skillRoot)
    expect(payload.status).toBe('fail')
    expect(payload.errors.length).toBeGreaterThan(0)
  })

  it('rewrites self graph snapshot', async () => {
    const { graphPath } = await rebuildSelfGraph(path.resolve(__dirname, '..'))
    const snapshot = JSON.parse(await readFile(graphPath, 'utf8')) as { graph_version: string }
    expect(snapshot.graph_version).toBe('v2')
  })
})
