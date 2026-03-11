<script setup lang="ts">
import LocatorNodeFrame from './LocatorNodeFrame.vue'
import { UI_COMPONENTS } from '../contracts/ui-identity-registry'
import { useUiLocatorNode } from '../composables/useUiLocatorNode'
import type { PreviewDocumentRecord } from '../types'

defineProps<{
  doc: PreviewDocumentRecord
  active: boolean
}>()

const emit = defineEmits<{
  select: [path: string]
}>()

const docItemNode = useUiLocatorNode(UI_COMPONENTS.documentNavigatorDocItem.id)
</script>

<template>
  <LocatorNodeFrame :node="docItemNode">
    <button
      class="doc-item"
      :class="{ active }"
      @click="emit('select', doc.path)"
    >
      <span class="doc-title">{{ doc.title }}</span>
      <span class="doc-meta">{{ doc.docType }} · {{ doc.anchorCount }} anchors</span>
      <span class="doc-path">{{ doc.path }}</span>
    </button>
  </LocatorNodeFrame>
</template>
