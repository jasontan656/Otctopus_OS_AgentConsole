<script setup lang="ts">
import GraphCanvas from '../components/GraphCanvas'
import LocatorNodeFrame from '../components/LocatorNodeFrame'
import { UI_CONTAINERS } from '../contracts/ui-identity-registry'
import { useUiLocatorNode } from '../composables/useUiLocatorNode'
import type { GraphEdgeRecord, PreviewDocumentRecord } from '../types'

defineProps<{
  docs: PreviewDocumentRecord[]
  edges: GraphEdgeRecord[]
  selectedPath: string
  targetRoot: string
  updatedAt: string
}>()

const emit = defineEmits<{
  'select-doc': [path: string]
}>()

const graphPanelNode = useUiLocatorNode(UI_CONTAINERS.graphPanel.id)
</script>

<template>
  <LocatorNodeFrame :node="graphPanelNode">
    <section class="surface-card graph-panel">
      <div class="surface-card__header">
        <div>
          <h2 class="surface-card__title">Anchor Graph</h2>
          <p class="surface-card__copy">{{ targetRoot || 'waiting for workspace' }}</p>
        </div>
        <span class="timestamp">{{ updatedAt || 'loading' }}</span>
      </div>

      <GraphCanvas
        v-if="docs.length"
        :docs="docs"
        :edges="edges"
        :selected-path="selectedPath"
        @select="emit('select-doc', $event)"
      />

      <div v-else class="empty-state">
        当前还没有可展示的文档 graph。
      </div>
    </section>
  </LocatorNodeFrame>
</template>
