<script setup lang="ts">
import { computed } from 'vue'
import MarkdownIt from 'markdown-it'
import type { PreviewDocumentRecord } from '../types'

const props = defineProps<{
  selectedDoc: PreviewDocumentRecord | null
}>()

const emit = defineEmits<{
  'follow-anchor': [path: string]
}>()

const markdown = new MarkdownIt({
  html: false,
  linkify: true,
  typographer: true,
})

const renderedMarkdown = computed(() => {
  return props.selectedDoc ? markdown.render(props.selectedDoc.body) : ''
})
</script>

<template>
  <section class="panel detail-panel">
    <div v-if="selectedDoc" class="detail-stack">
      <div class="detail-hero">
        <p class="eyebrow">Selected Doc</p>
        <h2>{{ selectedDoc.title }}</h2>
        <p class="detail-topic">{{ selectedDoc.topic }}</p>
        <p class="detail-path">{{ selectedDoc.path }}</p>
      </div>

      <div class="anchor-section">
        <div>
          <h3>Outgoing Anchors</h3>
          <button
            v-for="edge in selectedDoc.outgoing"
            :key="`${edge.source}-${edge.target}-${edge.relation}`"
            class="anchor-chip"
            @click="emit('follow-anchor', edge.target)"
          >
            {{ edge.direction }} · {{ edge.relation }} → {{ edge.target }}
          </button>
        </div>
        <div>
          <h3>Incoming Anchors</h3>
          <button
            v-for="edge in selectedDoc.incoming"
            :key="`${edge.target}-${edge.source}-${edge.relation}`"
            class="anchor-chip secondary"
            @click="emit('follow-anchor', edge.source)"
          >
            {{ edge.direction }} · {{ edge.relation }} ← {{ edge.source }}
          </button>
        </div>
      </div>

      <div v-if="selectedDoc.warnings.length" class="warning-box">
        <h3>Atomicity Warnings</h3>
        <p v-for="warning in selectedDoc.warnings" :key="warning.ruleId">
          {{ warning.ruleId }} · {{ warning.message }}
        </p>
      </div>

      <article class="markdown-body" v-html="renderedMarkdown"></article>
    </div>

    <div v-else class="empty-state">
      当前没有选中文档，等待 payload 到达或从左侧、graph 中选择一个节点。
    </div>
  </section>
</template>
