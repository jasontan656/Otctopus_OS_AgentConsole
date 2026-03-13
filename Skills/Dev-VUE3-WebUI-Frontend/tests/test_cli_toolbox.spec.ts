import os from 'node:os'
import path from 'node:path'
import { promises as fs } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { describe, expect, it } from 'vitest'
import { buildProductMotherDocGraph, lintProductMotherDoc } from '../src/lib/product-mother-doc-lint.js'
import { getStageDefinition, listStages, RUNTIME_CONTRACT } from '../src/lib/stage-contracts.js'

describe('Dev-VUE3-WebUI-Frontend stage contracts', () => {
  it('declares four explicit stages', () => {
    expect(listStages()).toEqual([
      'foundation_north_star',
      'responsive_surface_system',
      'motion_component_architecture',
      'showroom_runtime_delivery',
    ])
  })

  it('keeps resident docs in the runtime contract', () => {
    expect(RUNTIME_CONTRACT.resident_doc_policy.top_level_resident_docs).toContain('SKILL.md')
    expect(RUNTIME_CONTRACT.stage_contract_policy.stage_order).toContain('showroom_runtime_delivery')
  })

  it('exposes product-runtime handoff docs in the showroom runtime stage', () => {
    const showroom = getStageDefinition('showroom_runtime_delivery')
    expect(showroom.docContract.doc_boundary).toContain('frontend_dev_contracts/00_UI_DEVELOPMENT_INDEX.md')
    expect(showroom.docContract.doc_boundary).toContain('frontend_dev_contracts/design_system/00_DESIGN_SYSTEM_INDEX.md')
    expect(showroom.docContract.doc_boundary).toContain('frontend_dev_contracts/component_system/00_COMPONENT_SYSTEM_INDEX.md')
    expect(showroom.docContract.doc_boundary).toContain('frontend_dev_contracts/rules/UI_LANGUAGE_AND_COPY_RULES.md')
    expect(showroom.docContract.doc_boundary).toContain(
      'frontend_dev_contracts/containers/state/20_CONTAINER_PAYLOAD_NORMALIZATION.md',
    )
    expect(showroom.docContract.doc_boundary).toContain('frontend_dev_contracts/positioning/00_POSITIONING_INDEX.md')
    expect(showroom.docContract.doc_boundary).toContain('references/stages/40_STAGE_SHOWROOM_RUNTIME.md')
    expect(showroom.commandContract.gate_commands).toContain('npm run cli -- rebuild-self-graph --json')
  })

  it('exposes container taxonomy in the motion architecture stage', () => {
    const motion = getStageDefinition('motion_component_architecture')
    expect(motion.commandContract.gate_commands).toContain('npm run typecheck')
    expect(motion.commandContract.gate_commands).toContain('npm test')
    expect(motion.docContract.doc_boundary).toContain(
      'frontend_dev_contracts/containers/model/10_CONTAINER_ROLE_TAXONOMY.md',
    )
    expect(motion.docContract.doc_boundary).toContain('frontend_dev_contracts/layers/10_LAYER_TAXONOMY.md')
    expect(motion.docContract.doc_boundary).toContain('frontend_dev_contracts/component_system/packaging/10_COMPONENT_PACKAGE_SHAPE.md')
  })

  it('includes product mother doc lint commands in the runtime contract', () => {
    expect(RUNTIME_CONTRACT.tool_contracts['Cli_Toolbox.build-product-doc-graph']).toContain('product Development_Docs')
    expect(RUNTIME_CONTRACT.tool_contracts['Cli_Toolbox.lint-product-mother-doc']).toContain('frontend contract')
  })

  it('fails lint when a product mother doc misses panel detail coverage', async () => {
    const docsRoot = await fs.mkdtemp(path.join(os.tmpdir(), 'portal-docs-'))
    const motherDocRoot = path.join(docsRoot, 'mother_doc')
    await fs.mkdir(path.join(motherDocRoot, '04_frontend_contract_layer'), { recursive: true })
    await fs.mkdir(path.join(motherDocRoot, '05_domain_contracts'), { recursive: true })

    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '35_container_surface_and_slot_matrix.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: a\ntopic: a\ndoc_links: []\n---\n# A\n\`container.panel.body.docs_catalog\`\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '36_spatial_blueprint_protocol.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: b\ntopic: b\ndoc_links: ["35_container_surface_and_slot_matrix.md"]\n---\n# B\nlayout blueprint panel\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '37_desktop_viewport_baseline_blueprint.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: c\ntopic: c\ndoc_links: ["36_spatial_blueprint_protocol.md"]\n---\n# C\n\`panel.docs_catalog\`\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '38_workspace_and_panel_state_blueprints.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: d\ntopic: d\ndoc_links: ["36_spatial_blueprint_protocol.md"]\n---\n# D\n\`panel.docs_catalog\`\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '50_component_system_contract.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: e\ntopic: e\ndoc_links: ["55_component_registry_seed.md"]\n---\n# E\ncomponent props\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '55_component_registry_seed.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: f\ntopic: f\ndoc_links: ["50_component_system_contract.md"]\n---\n# F\n\`cmp.panel.frame\`\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '60_design_system_contract.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: g\ntopic: g\ndoc_links: ["65_visual_token_and_surface_matrix.md"]\n---\n# G\nsurface token\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '65_visual_token_and_surface_matrix.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: h\ntopic: h\ndoc_links: ["35_container_surface_and_slot_matrix.md"]\n---\n# H\n\`surface.panel.base\`\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '80_rules_and_validation_contract.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: i\ntopic: i\ndoc_links: []\n---\n# I\nlayout component\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '05_domain_contracts', '20_navigation_canvas_panel_contract.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: j\ntopic: j\ndoc_links: []\n---\n# J\n\`panel.docs_catalog\`\n`, 'utf8')

    const payload = await lintProductMotherDoc(docsRoot)
    expect(payload.status).toBe('fail')
    expect(payload.errors.some((item) => item.code === 'coverage.missing_required_doc')).toBe(true)
    expect(payload.errors.some((item) => item.code === 'component.missing_panel_component_contract')).toBe(true)
  })

  it('builds graph and passes lint on Unified Portal docs', async () => {
    const docsRoot = path.resolve(
      defaultPortalDocsRoot(),
    )
    const graphPayload = await buildProductMotherDocGraph(docsRoot)
    expect(graphPayload.summary.docCount).toBeGreaterThan(10)
    const lintPayload = await lintProductMotherDoc(docsRoot)
    expect(lintPayload.status).not.toBe('fail')
  })
})

function defaultPortalDocsRoot(): string {
  const currentDir = path.dirname(fileURLToPath(import.meta.url))
  return path.resolve(
    currentDir,
    '..',
    '..',
    '..',
    '..',
    'Octopus_OS',
    'Client_Applications',
    'Unified_Portal',
    'Development_Docs',
  )
}
