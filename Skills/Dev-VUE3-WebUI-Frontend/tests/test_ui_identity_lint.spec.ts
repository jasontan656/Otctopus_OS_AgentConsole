import path from 'node:path'
import { describe, expect, it } from 'vitest'
import { lintUiIdentity, loadUiIdentityContract } from '../src/lib/ui-identity.js'

describe('Dev-VUE3-WebUI-Frontend ui identity contract', () => {
  it('declares a fixed layer catalog', async () => {
    const skillRoot = path.resolve(__dirname, '..')
    const payload = await loadUiIdentityContract(skillRoot)
    expect(payload.layers.map((layer) => layer.id)).toEqual([
      'SH',
      'SC',
      'RT',
      'WK',
      'PN',
      'AT',
      'GV',
      'DC',
      'DX',
      'OV',
    ])
  })

  it('passes ui identity lint for the current showroom tree', async () => {
    const skillRoot = path.resolve(__dirname, '..')
    const payload = await lintUiIdentity(skillRoot)
    expect(payload.status).toBe('pass')
    expect(payload.summary.violationCount).toBe(0)
  })
})
