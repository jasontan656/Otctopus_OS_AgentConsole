<script setup lang="ts">
import DocumentNavigatorDocItem from '../components/DocumentNavigatorDocItem.vue'
import DocumentNavigatorSearchBox from '../components/DocumentNavigatorSearchBox.vue'
import LocatorNodeFrame from '../components/LocatorNodeFrame.vue'
import { UI_CONTAINERS } from '../contracts/ui-identity-registry'
import { useUiLocatorNode } from '../composables/useUiLocatorNode'
import type { PreviewDocumentRecord } from '../types'

defineProps<{
  docs: PreviewDocumentRecord[]
  searchKeyword: string
  selectedPath: string
}>()

const emit = defineEmits<{
  'update-search': [keyword: string]
  'select-doc': [path: string]
}>()

const navigatorNode = useUiLocatorNode(UI_CONTAINERS.documentNavigator.id)
</script>

<template>
  <LocatorNodeFrame :node="navigatorNode">
    <aside class="panel sidebar">
      <div class="panel-head panel-head-stack">
        <div>
          <h2>Document Index</h2>
          <p>工作区统一持有选择态；导航容器只负责过滤和发出选择意图。</p>
        </div>
        <DocumentNavigatorSearchBox
          :model-value="searchKeyword"
          @update:model-value="emit('update-search', $event)"
        />
      </div>

      <div class="doc-list">
        <DocumentNavigatorDocItem
          v-for="doc in docs"
          :key="doc.path"
          :doc="doc"
          :active="doc.path === selectedPath"
          @select="emit('select-doc', $event)"
        />

        <div v-if="docs.length === 0" class="empty-state">
          当前搜索结果为空，调整关键字后重试。
        </div>
      </div>
    </aside>
  </LocatorNodeFrame>
</template>
