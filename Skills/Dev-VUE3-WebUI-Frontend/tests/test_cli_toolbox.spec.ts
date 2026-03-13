import { describe, expect, it } from 'vitest'
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
})
