<script setup lang="ts">
import LocatorNodeFrame from '../components/LocatorNodeFrame.vue'
import RuntimeStatusStatCard from '../components/RuntimeStatusStatCard.vue'
import { UI_CONTAINERS } from '../contracts/ui-identity-registry'
import type { RuntimeLiveState } from '../contracts/showroom-container-contract'
import { useUiLocatorNode } from '../composables/useUiLocatorNode'
import type { PreviewPayload } from '../types'

defineProps<{
  payload: PreviewPayload | null
  liveState: RuntimeLiveState
  statusLabel: string
  lastError: string | null
}>()

const runtimeStatusNode = useUiLocatorNode(UI_CONTAINERS.runtimeStatus.id)
</script>

<template>
  <LocatorNodeFrame :node="runtimeStatusNode">
    <section class="panel runtime-status-panel">
      <div class="panel-head">
        <div>
          <h2>Runtime Status</h2>
          <p>runtime bridge、payload 健康度与 graph 摘要由 scene 层统一暴露。</p>
        </div>
        <span class="timestamp">{{ payload?.updatedAt ?? 'waiting for payload' }}</span>
      </div>

      <div class="runtime-status-grid">
        <RuntimeStatusStatCard label="Live" :value="liveState" />
        <RuntimeStatusStatCard label="Status" :value="statusLabel" />
        <RuntimeStatusStatCard label="Docs" :value="payload?.summary.nodeCount ?? 0" />
        <RuntimeStatusStatCard label="Edges" :value="payload?.summary.edgeCount ?? 0" />
      </div>

      <p class="runtime-note">
        <strong>Target:</strong> {{ payload?.targetRoot ?? 'loading' }}
        <span v-if="lastError"> · {{ lastError }}</span>
      </p>
    </section>
  </LocatorNodeFrame>
</template>
