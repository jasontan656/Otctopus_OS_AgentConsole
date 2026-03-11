<script setup lang="ts">
import LocatorNodeFrame from './LocatorNodeFrame.vue'
import { UI_COMPONENTS } from '../contracts/ui-identity-registry'
import { useUiLocatorNode } from '../composables/useUiLocatorNode'

defineProps<{
  html: string
}>()

const markdownBodyNode = useUiLocatorNode(UI_COMPONENTS.documentReaderMarkdownBody.id)
</script>

<template>
  <LocatorNodeFrame :node="markdownBodyNode">
    <article class="markdown-body" v-html="html"></article>
  </LocatorNodeFrame>
</template>
