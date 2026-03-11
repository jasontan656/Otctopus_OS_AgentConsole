<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import LocatorNodeFrame from '../components/LocatorNodeFrame.vue'
import { UI_CONTAINERS } from '../contracts/ui-identity-registry'
import { useUiLocatorNode } from '../composables/useUiLocatorNode'
import type { PreviewDocumentRecord, PreviewPayload } from '../types'
import DocumentNavigatorContainer from './DocumentNavigatorContainer.vue'
import DocumentReaderContainer from './DocumentReaderContainer.vue'
import GraphPanelContainer from './GraphPanelContainer.vue'

const props = defineProps<{
  payload: PreviewPayload | null
}>()

const workspaceNode = useUiLocatorNode(UI_CONTAINERS.showroomWorkspace.id)
const selectedPath = ref('SKILL.md')
const searchKeyword = ref('')

function ensureSelection(nextPayload: PreviewPayload) {
  const entryPath = nextPayload.view.entryPath || nextPayload.docs[0]?.path || ''
  if (!nextPayload.docs.some((doc) => doc.path === selectedPath.value)) {
    selectedPath.value = entryPath
  }
}

const docs = computed(() => props.payload?.docs ?? [])

const filteredDocs = computed(() => {
  const keyword = searchKeyword.value.trim().toLowerCase()
  if (!keyword) {
    return docs.value
  }

  return docs.value.filter((doc) => {
    return [doc.path, doc.title, doc.docType, doc.topic].some((item) => item.toLowerCase().includes(keyword))
  })
})

const selectedDoc = computed<PreviewDocumentRecord | null>(() => {
  return docs.value.find((doc) => doc.path === selectedPath.value) ?? null
})

watch(() => props.payload, (nextPayload) => {
  if (nextPayload) {
    ensureSelection(nextPayload)
  }
}, { immediate: true })
</script>

<template>
  <LocatorNodeFrame :node="workspaceNode">
    <main class="dashboard-grid">
      <DocumentNavigatorContainer
        :docs="filteredDocs"
        :search-keyword="searchKeyword"
        :selected-path="selectedPath"
        @update-search="searchKeyword = $event"
        @select-doc="selectedPath = $event"
      />
      <GraphPanelContainer
        :docs="docs"
        :edges="payload?.graph.edges ?? []"
        :selected-path="selectedPath"
        :target-root="payload?.targetRoot ?? ''"
        :updated-at="payload?.updatedAt ?? ''"
        @select-doc="selectedPath = $event"
      />
      <DocumentReaderContainer
        :selected-doc="selectedDoc"
        @follow-anchor="selectedPath = $event"
      />
    </main>
  </LocatorNodeFrame>
</template>
