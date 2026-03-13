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

  it('fails lint when blueprint nodes omit required overlap schema keys', async () => {
    const docsRoot = await fs.mkdtemp(path.join(os.tmpdir(), 'portal-docs-overlap-'))
    const motherDocRoot = path.join(docsRoot, 'mother_doc')
    await fs.mkdir(path.join(motherDocRoot, '04_frontend_contract_layer', '39_panel_blueprint_catalog'), { recursive: true })
    await fs.mkdir(path.join(motherDocRoot, '04_frontend_contract_layer', '56_component_property_matrix'), { recursive: true })
    await fs.mkdir(path.join(motherDocRoot, '05_domain_contracts'), { recursive: true })

    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '35_container_surface_and_slot_matrix.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: a\ntopic: a\ndoc_links: []\n---\n# A\n\`container.panel.body.docs_catalog\`\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '36_spatial_blueprint_protocol.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: b\ntopic: b\ndoc_links: [\"39_panel_blueprint_catalog/00_index.md\"]\n---\n# B\n\`\`\`yaml\nlocal_coordinate_spaces:\n  - local_coordinate_space_id: panel_local_px.4col\n    width: 311\n    height: 284\n    overflow_policy: forbid_overflow\n\`\`\`\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '37_desktop_viewport_baseline_blueprint.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: c\ntopic: c\ndoc_links: [\"36_spatial_blueprint_protocol.md\"]\n---\n# C\n\`\`\`yaml\nviewport:\n  viewport_id: demo\n  viewport_width: 100\n  viewport_height: 100\nnodes: []\n\`\`\`\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '38_workspace_and_panel_state_blueprints.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: d\ntopic: d\ndoc_links: [\"36_spatial_blueprint_protocol.md\"]\n---\n# D\nstate blueprint\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '39_panel_blueprint_catalog', '00_index.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: e\ntopic: e\ndoc_links: [\"10_primary_workspace_panels.md\"]\n---\n# E\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '39_panel_blueprint_catalog', '10_primary_workspace_panels.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: f\ntopic: f\ndoc_links: [\"../56_component_property_matrix/10_shell_nav_foundations.md\"]\n---\n# F\n\`panel.docs_catalog\`\n\`\`\`yaml\npanel_blueprint:\n  panel_id: panel.docs_catalog\n  body_container_id: container.panel.body.docs_catalog\n  local_coordinate_space: panel_local_px.4col\n  frame_width: 311\n  frame_height: 284\n  overflow_policy: forbid_overflow\n  interaction_states: [default]\n  responsive_variants:\n    desktop_default:\n      grid_span: 4\n      frame_width: 311\n      frame_height: 284\n  nodes:\n    - node_id: panel.docs_catalog.toolbar\n      parent_id: panel.docs_catalog.body\n      component_id: cmp.viewer.toolbar_strip\n      x: 0\n      y: 0\n      w: 311\n      h: 36\n\`\`\`\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '39_panel_blueprint_catalog', '20_docs_governance_panels.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: g\ntopic: g\ndoc_links: []\n---\n# G\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '39_panel_blueprint_catalog', '30_code_panels.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: h\ntopic: h\ndoc_links: []\n---\n# H\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '39_panel_blueprint_catalog', '40_ai_runtime_panels.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: i\ntopic: i\ndoc_links: []\n---\n# I\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '50_component_system_contract.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: j\ntopic: j\ndoc_links: [\"55_component_registry_seed.md\"]\n---\n# J\ncomponent props\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '55_component_registry_seed.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: k\ntopic: k\ndoc_links: [\"50_component_system_contract.md\"]\n---\n# K\n\`cmp.viewer.toolbar_strip\`\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '56_component_property_matrix', '00_index.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: l\ntopic: l\ndoc_links: [\"10_shell_nav_foundations.md\", \"20_panel_viewer_foundations.md\", \"30_reader_ai_runtime_components.md\"]\n---\n# L\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '56_component_property_matrix', '10_shell_nav_foundations.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: m\ntopic: m\ndoc_links: []\n---\n# M\n\`panel.docs_catalog\`\n\`cmp.viewer.toolbar_strip\`\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '56_component_property_matrix', '20_panel_viewer_foundations.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: n\ntopic: n\ndoc_links: []\n---\n# N\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '56_component_property_matrix', '30_reader_ai_runtime_components.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: o\ntopic: o\ndoc_links: []\n---\n# O\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '60_design_system_contract.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: p\ntopic: p\ndoc_links: [\"65_visual_token_and_surface_matrix.md\"]\n---\n# P\nsurface token\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '65_visual_token_and_surface_matrix.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: q\ntopic: q\ndoc_links: [\"35_container_surface_and_slot_matrix.md\"]\n---\n# Q\n\`surface.panel.base\`\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '80_rules_and_validation_contract.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: r\ntopic: r\ndoc_links: [\"81_frontend_mother_doc_gate_contract.md\", \"82_semantic_split_graph_gate_contract.md\", \"83_blueprint_numeric_integrity_gate_contract.md\", \"84_spatial_field_relation_gate_contract.md\"]\n---\n# R\nlayout component\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '81_frontend_mother_doc_gate_contract.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: s\ntopic: s\ndoc_links: [\"80_rules_and_validation_contract.md\"]\n---\n# S\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '82_semantic_split_graph_gate_contract.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: t\ntopic: t\ndoc_links: [\"80_rules_and_validation_contract.md\"]\n---\n# T\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '83_blueprint_numeric_integrity_gate_contract.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: u\ntopic: u\ndoc_links: [\"36_spatial_blueprint_protocol.md\"]\n---\n# U\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '84_spatial_field_relation_gate_contract.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: w\ntopic: w\ndoc_links: [\"36_spatial_blueprint_protocol.md\"]\n---\n# W\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '05_domain_contracts', '20_navigation_canvas_panel_contract.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: v\ntopic: v\ndoc_links: []\n---\n# V\n\`panel.docs_catalog\`\n`, 'utf8')

    const payload = await lintProductMotherDoc(docsRoot)
    expect(payload.status).toBe('fail')
    expect(payload.errors.some((item) => item.code === 'blueprint.node_missing_required_fields')).toBe(true)
  })

  it('fails lint when peer node does not accept declared overlap relation', async () => {
    const docsRoot = await fs.mkdtemp(path.join(os.tmpdir(), 'portal-docs-peer-'))
    const motherDocRoot = path.join(docsRoot, 'mother_doc')
    await fs.mkdir(path.join(motherDocRoot, '04_frontend_contract_layer', '39_panel_blueprint_catalog'), { recursive: true })
    await fs.mkdir(path.join(motherDocRoot, '04_frontend_contract_layer', '56_component_property_matrix'), { recursive: true })
    await fs.mkdir(path.join(motherDocRoot, '05_domain_contracts'), { recursive: true })

    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '35_container_surface_and_slot_matrix.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: a\ntopic: a\ndoc_links: []\n---\n# A\n\`container.panel.body.docs_catalog\`\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '36_spatial_blueprint_protocol.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: b\ntopic: b\ndoc_links: [\"39_panel_blueprint_catalog/00_index.md\"]\n---\n# B\n\`\`\`yaml\nlocal_coordinate_spaces:\n  - local_coordinate_space_id: panel_local_px.4col\n    width: 311\n    height: 284\n    overflow_policy: forbid_overflow\n\`\`\`\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '37_desktop_viewport_baseline_blueprint.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: c\ntopic: c\ndoc_links: [\"36_spatial_blueprint_protocol.md\"]\n---\n# C\n\`\`\`yaml\nviewport:\n  viewport_id: demo\n  viewport_width: 100\n  viewport_height: 100\nnodes: []\n\`\`\`\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '38_workspace_and_panel_state_blueprints.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: d\ntopic: d\ndoc_links: [\"36_spatial_blueprint_protocol.md\"]\n---\n# D\nstate blueprint\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '39_panel_blueprint_catalog', '00_index.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: e\ntopic: e\ndoc_links: [\"10_primary_workspace_panels.md\"]\n---\n# E\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '39_panel_blueprint_catalog', '10_primary_workspace_panels.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: f\ntopic: f\ndoc_links: [\"../56_component_property_matrix/10_shell_nav_foundations.md\"]\n---\n# F\n\`panel.docs_catalog\`\n\`\`\`yaml\npanel_blueprint:\n  panel_id: panel.docs_catalog\n  body_container_id: container.panel.body.docs_catalog\n  local_coordinate_space: panel_local_px.4col\n  frame_width: 311\n  frame_height: 284\n  overflow_policy: forbid_overflow\n  interaction_states: [default]\n  responsive_variants:\n    desktop_default:\n      grid_span: 4\n      frame_width: 311\n      frame_height: 284\n  nodes:\n    - node_id: panel.docs_catalog.viewport\n      parent_id: panel.docs_catalog.body\n      component_id: cmp.viewer.toolbar_strip\n      x: 0\n      y: 0\n      w: 220\n      h: 180\n      allow_overlap: false\n      overlap_targets: []\n      overlap_mode: null\n      collision_policy: forbid\n      inbound_overlap_policy: forbid\n      occlusion_policy: forbid_occlusion\n      relation_refs: []\n      elevation: null\n    - node_id: panel.docs_catalog.detail\n      parent_id: panel.docs_catalog.body\n      component_id: cmp.viewer.toolbar_strip\n      x: 160\n      y: 40\n      w: 151\n      h: 120\n      allow_overlap: true\n      overlap_targets: [panel.docs_catalog.viewport]\n      overlap_mode: cover_peer\n      collision_policy: allow_with_declaration\n      inbound_overlap_policy: forbid\n      occlusion_policy: forbid_occlusion\n      relation_refs: []\n      elevation: 1\n\`\`\`\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '39_panel_blueprint_catalog', '20_docs_governance_panels.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: g\ntopic: g\ndoc_links: []\n---\n# G\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '39_panel_blueprint_catalog', '30_code_panels.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: h\ntopic: h\ndoc_links: []\n---\n# H\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '39_panel_blueprint_catalog', '40_ai_runtime_panels.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: i\ntopic: i\ndoc_links: []\n---\n# I\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '50_component_system_contract.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: j\ntopic: j\ndoc_links: [\"55_component_registry_seed.md\"]\n---\n# J\ncomponent props\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '55_component_registry_seed.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: k\ntopic: k\ndoc_links: [\"50_component_system_contract.md\"]\n---\n# K\n\`cmp.viewer.toolbar_strip\`\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '56_component_property_matrix', '00_index.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: l\ntopic: l\ndoc_links: [\"10_shell_nav_foundations.md\", \"20_panel_viewer_foundations.md\", \"30_reader_ai_runtime_components.md\"]\n---\n# L\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '56_component_property_matrix', '10_shell_nav_foundations.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: m\ntopic: m\ndoc_links: []\n---\n# M\n\`panel.docs_catalog\`\n\`cmp.viewer.toolbar_strip\`\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '56_component_property_matrix', '20_panel_viewer_foundations.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: n\ntopic: n\ndoc_links: []\n---\n# N\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '56_component_property_matrix', '30_reader_ai_runtime_components.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: o\ntopic: o\ndoc_links: []\n---\n# O\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '60_design_system_contract.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: p\ntopic: p\ndoc_links: [\"65_visual_token_and_surface_matrix.md\"]\n---\n# P\nsurface token\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '65_visual_token_and_surface_matrix.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: q\ntopic: q\ndoc_links: [\"35_container_surface_and_slot_matrix.md\"]\n---\n# Q\n\`surface.panel.base\`\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '80_rules_and_validation_contract.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: r\ntopic: r\ndoc_links: [\"81_frontend_mother_doc_gate_contract.md\", \"82_semantic_split_graph_gate_contract.md\", \"83_blueprint_numeric_integrity_gate_contract.md\", \"84_spatial_field_relation_gate_contract.md\"]\n---\n# R\nlayout component\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '81_frontend_mother_doc_gate_contract.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: s\ntopic: s\ndoc_links: [\"80_rules_and_validation_contract.md\"]\n---\n# S\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '82_semantic_split_graph_gate_contract.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: t\ntopic: t\ndoc_links: [\"80_rules_and_validation_contract.md\"]\n---\n# T\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '83_blueprint_numeric_integrity_gate_contract.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: u\ntopic: u\ndoc_links: [\"36_spatial_blueprint_protocol.md\"]\n---\n# U\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '04_frontend_contract_layer', '84_spatial_field_relation_gate_contract.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: w\ntopic: w\ndoc_links: [\"36_spatial_blueprint_protocol.md\"]\n---\n# W\n`, 'utf8')
    await fs.writeFile(path.join(motherDocRoot, '05_domain_contracts', '20_navigation_canvas_panel_contract.md'), `---\ndoc_work_state: modified\ndoc_pack_refs: []\ndoc_id: v\ntopic: v\ndoc_links: []\n---\n# V\n\`panel.docs_catalog\`\n`, 'utf8')

    const payload = await lintProductMotherDoc(docsRoot)
    expect(payload.status).toBe('fail')
    expect(payload.errors.some((item) => item.code === 'field_relation.peer_contract_mismatch')).toBe(true)
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
