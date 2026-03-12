<script setup lang="ts">
import LocatorNodeFrame from '../LocatorNodeFrame'
import { UI_COMPONENTS } from '../../contracts/ui-identity-registry'
import { useUiLocatorNode } from '../../composables/useUiLocatorNode'
import type { PreviewDocumentRecord } from '../../types'

defineProps<{
  selectedDoc: PreviewDocumentRecord
}>()

const detailHeroNode = useUiLocatorNode(UI_COMPONENTS.documentReaderDetailHero.id)
</script>

<template>
  <LocatorNodeFrame :node="detailHeroNode">
    <div class="detail-hero">
      <p class="eyebrow">Selected Doc</p>
      <h2>{{ selectedDoc.title }}</h2>
      <p class="reader-detail-hero__topic">{{ selectedDoc.topic }}</p>
      <p class="reader-detail-hero__path">{{ selectedDoc.path }}</p>
    </div>
  </LocatorNodeFrame>
</template>
