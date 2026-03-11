<script setup lang="ts">
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
</script>

<template>
  <aside class="panel sidebar">
    <div class="panel-head">
      <div>
        <h2>Document Index</h2>
        <p>工作区统一持有选择态；导航容器只负责过滤和发出选择意图。</p>
      </div>
      <input
        :value="searchKeyword"
        class="search-box"
        placeholder="Search path / topic / type"
        @input="emit('update-search', ($event.target as HTMLInputElement).value)"
      />
    </div>

    <div class="doc-list">
      <button
        v-for="doc in docs"
        :key="doc.path"
        class="doc-item"
        :class="{ active: doc.path === selectedPath }"
        @click="emit('select-doc', doc.path)"
      >
        <span class="doc-title">{{ doc.title }}</span>
        <span class="doc-meta">{{ doc.docType }} · {{ doc.anchorCount }} anchors</span>
        <span class="doc-path">{{ doc.path }}</span>
      </button>

      <div v-if="docs.length === 0" class="empty-state">
        当前搜索结果为空，调整关键字后重试。
      </div>
    </div>
  </aside>
</template>
