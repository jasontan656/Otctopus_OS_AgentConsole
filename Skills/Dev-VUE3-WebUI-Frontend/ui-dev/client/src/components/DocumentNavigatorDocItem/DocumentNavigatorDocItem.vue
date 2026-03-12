<script setup lang="ts">
import LocatorNodeFrame from '../LocatorNodeFrame'
import { UI_COMPONENTS } from '../../contracts/ui-identity-registry'
import { useUiLocatorNode } from '../../composables/useUiLocatorNode'
import type { PreviewDocumentRecord } from '../../types'

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
      class="document-doc-item"
      :class="{ 'is-active': active }"
      @click="emit('select', doc.path)"
    >
      <span class="document-doc-item__title">{{ doc.title }}</span>
      <span class="document-doc-item__meta">{{ doc.docType }} · {{ doc.anchorCount }} anchors</span>
      <span class="document-doc-item__path">{{ doc.path }}</span>
    </button>
  </LocatorNodeFrame>
</template>
