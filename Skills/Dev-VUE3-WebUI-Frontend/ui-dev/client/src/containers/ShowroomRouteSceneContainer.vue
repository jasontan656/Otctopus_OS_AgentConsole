<script setup lang="ts">
import { computed } from 'vue'
import RuntimeStatusContainer from './RuntimeStatusContainer.vue'
import ShowroomWorkspaceContainer from './ShowroomWorkspaceContainer.vue'
import { useShowroomRuntimeBridge } from '../composables/useShowroomRuntimeBridge'

const { payload, liveState, lastError } = useShowroomRuntimeBridge()

const statusLabel = computed(() => {
  if (!payload.value) return 'Loading'
  if (payload.value.status === 'fail') return 'Graph Broken'
  if (payload.value.status === 'pass_with_warnings') return 'Graph Warning'
  return 'Graph Healthy'
})
</script>

<template>
  <section class="scene-stack">
    <RuntimeStatusContainer
      :payload="payload"
      :live-state="liveState"
      :status-label="statusLabel"
      :last-error="lastError"
    />
    <ShowroomWorkspaceContainer :payload="payload" />
  </section>
</template>
