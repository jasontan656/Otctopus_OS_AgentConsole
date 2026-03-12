export const GRAPH_CANVAS_CONTRACT = {
  role: 'visual_engine',
  variants: ['default', 'selected-node'],
} as const

export const DOC_TYPE_PALETTE: Record<string, string> = {
  skill_facade: '#dd6742',
  runtime_contract: '#1d3557',
  tooling_usage: '#1f7a8c',
  tooling_development: '#0f766e',
  tooling_architecture: '#7c3aed',
  tooling_index: '#a16207',
  module_doc: '#0b7285',
  template_doc: '#9a3412',
  changelog: '#475569',
}
