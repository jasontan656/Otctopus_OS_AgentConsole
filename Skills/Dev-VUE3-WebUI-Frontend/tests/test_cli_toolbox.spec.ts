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

  it('exposes ui-dev docs in the showroom runtime stage', () => {
    const showroom = getStageDefinition('showroom_runtime_delivery')
    expect(showroom.docContract.doc_boundary).toContain('ui-dev/UI_DEV_ENTRY.md')
    expect(showroom.docContract.doc_boundary).toContain('frontend_dev_contracts/00_UI_DEVELOPMENT_INDEX.md')
    expect(showroom.docContract.doc_boundary).toContain(
      'frontend_dev_contracts/containers/state/20_CONTAINER_PAYLOAD_NORMALIZATION.md',
    )
    expect(showroom.docContract.doc_boundary).toContain(
      'frontend_dev_contracts/showroom_runtime/VIEWER_SERVICE_WORKFLOW.md',
    )
    expect(showroom.commandContract.gate_commands).toContain('cd ui-dev && npm run build')
  })

  it('exposes container taxonomy in the motion architecture stage', () => {
    const motion = getStageDefinition('motion_component_architecture')
    expect(motion.docContract.doc_boundary).toContain(
      'frontend_dev_contracts/containers/model/10_CONTAINER_ROLE_TAXONOMY.md',
    )
  })
})
