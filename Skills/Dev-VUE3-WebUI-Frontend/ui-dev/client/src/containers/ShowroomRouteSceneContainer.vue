<script setup lang="ts">
import { computed } from 'vue'
import LocatorNodeFrame from '../components/LocatorNodeFrame'
import { UI_CONTAINERS } from '../contracts/ui-identity-registry'
import RuntimeStatusContainer from './RuntimeStatusContainer.vue'
import { useUiLocatorNode } from '../composables/useUiLocatorNode'
import ShowroomWorkspaceContainer from './ShowroomWorkspaceContainer.vue'
import { useShowroomRuntimeBridge } from '../composables/useShowroomRuntimeBridge'

const routeSceneNode = useUiLocatorNode(UI_CONTAINERS.showroomRouteScene.id)
const { payload, liveState, lastError } = useShowroomRuntimeBridge()

const statusLabel = computed(() => {
  if (!payload.value) return 'Loading'
  if (payload.value.status === 'fail') return 'Graph Broken'
  if (payload.value.status === 'pass_with_warnings') return 'Graph Warning'
  return 'Graph Healthy'
})
</script>

<template>
  <LocatorNodeFrame :node="routeSceneNode">
    <section class="scene-stack">
      <RuntimeStatusContainer
        :payload="payload"
        :live-state="liveState"
        :status-label="statusLabel"
        :last-error="lastError"
      />
      <ShowroomWorkspaceContainer :payload="payload" />
    </section>
  </LocatorNodeFrame>
</template>
