import { onBeforeUnmount, onMounted, ref } from 'vue'
import type { ShowroomRuntimeSnapshot } from '../contracts/showroom-container-contract'
import type { PreviewPayload } from '../types'

export function useShowroomRuntimeBridge(): ShowroomRuntimeSnapshot {
  const payload = ref<PreviewPayload | null>(null)
  const liveState = ref<'connecting' | 'live' | 'stale'>('connecting')
  const lastError = ref<string | null>(null)
  let socket: WebSocket | null = null

  async function loadInitialPayload() {
    try {
      const response = await fetch('/api/preview')
      if (!response.ok) {
        throw new Error(`preview request failed: ${response.status}`)
      }
      payload.value = (await response.json()) as PreviewPayload
      liveState.value = 'live'
      lastError.value = null
    } catch (error) {
      liveState.value = 'stale'
      lastError.value = error instanceof Error ? error.message : 'unknown preview error'
    }
  }

  function connectSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws'
    socket = new WebSocket(`${protocol}://${window.location.host}/live`)

    socket.addEventListener('open', () => {
      liveState.value = 'live'
      lastError.value = null
    })

    socket.addEventListener('message', (event) => {
      const packet = JSON.parse(event.data) as
        | { type: 'payload'; payload: PreviewPayload }
        | { type: 'error'; error?: string }

      if (packet.type === 'payload') {
        payload.value = packet.payload
        liveState.value = 'live'
        lastError.value = null
        return
      }

      liveState.value = 'stale'
      lastError.value = packet.error ?? 'runtime payload error'
    })

    socket.addEventListener('close', () => {
      liveState.value = 'stale'
    })

    socket.addEventListener('error', () => {
      liveState.value = 'stale'
      lastError.value = 'websocket connection error'
    })
  }

  onMounted(async () => {
    await loadInitialPayload()
    connectSocket()
  })

  onBeforeUnmount(() => {
    socket?.close()
  })

  return {
    payload,
    liveState,
    lastError,
  }
}
