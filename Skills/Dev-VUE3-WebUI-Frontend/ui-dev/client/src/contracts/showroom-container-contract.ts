import type { Ref } from 'vue'
import type { PreviewPayload } from '../types'

export type RuntimeLiveState = 'connecting' | 'live' | 'stale'

export interface ShowroomRuntimeSnapshot {
  payload: Ref<PreviewPayload | null>
  liveState: Ref<RuntimeLiveState>
  lastError: Ref<string | null>
}

export interface ShowroomSelectionIntent {
  path: string
}
