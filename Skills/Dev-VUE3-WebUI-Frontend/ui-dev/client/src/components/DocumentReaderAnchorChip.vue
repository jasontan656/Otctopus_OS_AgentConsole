<script setup lang="ts">
import LocatorNodeFrame from './LocatorNodeFrame.vue'
import { UI_COMPONENTS } from '../contracts/ui-identity-registry'
import { useUiLocatorNode } from '../composables/useUiLocatorNode'
import type { GraphEdgeRecord } from '../types'

defineProps<{
  edge: GraphEdgeRecord
  mode: 'incoming' | 'outgoing'
}>()

const emit = defineEmits<{
  follow: [path: string]
}>()

const anchorChipNode = useUiLocatorNode(UI_COMPONENTS.documentReaderAnchorChip.id)
</script>

<template>
  <LocatorNodeFrame :node="anchorChipNode">
    <button
      class="anchor-chip"
      :class="{ secondary: mode === 'incoming' }"
      @click="emit('follow', mode === 'incoming' ? edge.source : edge.target)"
    >
      <template v-if="mode === 'incoming'">
        {{ edge.direction }} · {{ edge.relation }} ← {{ edge.source }}
      </template>
      <template v-else>
        {{ edge.direction }} · {{ edge.relation }} → {{ edge.target }}
      </template>
    </button>
  </LocatorNodeFrame>
</template>
