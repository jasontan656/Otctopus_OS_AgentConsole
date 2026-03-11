<script setup lang="ts">
import GraphCanvas from '../components/GraphCanvas.vue'
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
</script>

<template>
  <section class="panel graph-panel">
    <div class="panel-head">
      <div>
        <h2>Anchor Graph</h2>
        <p>{{ targetRoot || 'waiting for workspace' }}</p>
      </div>
      <span class="timestamp">{{ updatedAt || 'loading' }}</span>
    </div>

    <div v-if="docs.length" class="graph-shell">
      <GraphCanvas
        :docs="docs"
        :edges="edges"
        :selected-path="selectedPath"
        @select="emit('select-doc', $event)"
      />
    </div>

    <div v-else class="empty-state">
      当前还没有可展示的文档 graph。
    </div>
  </section>
</template>
