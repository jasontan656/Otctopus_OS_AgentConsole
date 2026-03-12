<script setup lang="ts">
import { UI_COMPONENTS, type UiNodeDefinition } from '../../contracts/ui-identity-registry'
import { useUiLocatorState } from '../../composables/useUiLocatorState'

defineProps<{
  node: UiNodeDefinition
}>()

const locatorFrameNodeId = UI_COMPONENTS.locatorFrame.id
const { enabled } = useUiLocatorState()
</script>

<template>
  <div class="locator-node-frame" :class="[`locator-layer-${node.layerId.toLowerCase()}`]" :data-locator-frame-id="locatorFrameNodeId">
    <div v-if="enabled" class="locator-chip">
      <span class="locator-chip-code">[{{ node.shortCode }}]</span>
      <span>{{ node.id }}</span>
    </div>
    <slot />
  </div>
</template>
