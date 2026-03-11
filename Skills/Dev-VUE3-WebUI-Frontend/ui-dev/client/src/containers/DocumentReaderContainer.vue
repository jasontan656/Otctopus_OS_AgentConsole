<script setup lang="ts">
import { computed } from 'vue'
import MarkdownIt from 'markdown-it'
import DocumentReaderAnchorChip from '../components/DocumentReaderAnchorChip.vue'
import DocumentReaderDetailHero from '../components/DocumentReaderDetailHero.vue'
import DocumentReaderMarkdownBody from '../components/DocumentReaderMarkdownBody.vue'
import DocumentReaderWarningList from '../components/DocumentReaderWarningList.vue'
import LocatorNodeFrame from '../components/LocatorNodeFrame.vue'
import { UI_CONTAINERS } from '../contracts/ui-identity-registry'
import { useUiLocatorNode } from '../composables/useUiLocatorNode'
import type { PreviewDocumentRecord } from '../types'

const props = defineProps<{
  selectedDoc: PreviewDocumentRecord | null
}>()

const emit = defineEmits<{
  'follow-anchor': [path: string]
}>()

const readerNode = useUiLocatorNode(UI_CONTAINERS.documentReader.id)

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
  <LocatorNodeFrame :node="readerNode">
    <section class="panel detail-panel">
      <div v-if="selectedDoc" class="detail-stack">
        <DocumentReaderDetailHero :selected-doc="selectedDoc" />

        <div class="anchor-section">
          <div>
            <h3>Outgoing Anchors</h3>
            <DocumentReaderAnchorChip
              v-for="edge in selectedDoc.outgoing"
              :key="`${edge.source}-${edge.target}-${edge.relation}`"
              :edge="edge"
              mode="outgoing"
              @follow="emit('follow-anchor', $event)"
            />
          </div>
          <div>
            <h3>Incoming Anchors</h3>
            <DocumentReaderAnchorChip
              v-for="edge in selectedDoc.incoming"
              :key="`${edge.target}-${edge.source}-${edge.relation}`"
              :edge="edge"
              mode="incoming"
              @follow="emit('follow-anchor', $event)"
            />
          </div>
        </div>

        <DocumentReaderWarningList
          v-if="selectedDoc.warnings.length"
          :warnings="selectedDoc.warnings"
        />

        <DocumentReaderMarkdownBody :html="renderedMarkdown" />
      </div>

      <div v-else class="empty-state">
        当前没有选中文档，等待 payload 到达或从左侧、graph 中选择一个节点。
      </div>
    </section>
  </LocatorNodeFrame>
</template>
