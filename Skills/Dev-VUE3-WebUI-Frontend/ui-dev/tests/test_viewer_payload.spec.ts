import path from 'node:path'
import { describe, expect, it } from 'vitest'
import { buildViewerPayload } from '../lib/viewer-payload.js'

describe('Dev-VUE3-WebUI-Frontend viewer payload', () => {
  it('defaults the viewer entry to SKILL.md', async () => {
    const skillRoot = path.resolve(__dirname, '..', '..')
    const payload = await buildViewerPayload(skillRoot)
    expect(payload.view.entryPath).toBe('SKILL.md')
  })

  it('materializes incoming and outgoing anchor relations for docs', async () => {
    const skillRoot = path.resolve(__dirname, '..', '..')
    const payload = await buildViewerPayload(skillRoot)
    const skillEntry = payload.docs.find((doc) => doc.path === 'SKILL.md')
    expect(skillEntry).toBeTruthy()
    expect((skillEntry?.outgoing.length ?? 0) > 0).toBe(true)
  })
})
