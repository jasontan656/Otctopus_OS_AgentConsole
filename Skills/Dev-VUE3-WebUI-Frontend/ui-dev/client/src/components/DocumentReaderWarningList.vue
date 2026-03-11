<script setup lang="ts">
import LocatorNodeFrame from './LocatorNodeFrame.vue'
import { UI_COMPONENTS } from '../contracts/ui-identity-registry'
import { useUiLocatorNode } from '../composables/useUiLocatorNode'
import type { PreviewDocumentRecord } from '../types'

defineProps<{
  warnings: PreviewDocumentRecord['warnings']
}>()

const warningListNode = useUiLocatorNode(UI_COMPONENTS.documentReaderWarningList.id)
</script>

<template>
  <LocatorNodeFrame :node="warningListNode">
    <div class="warning-box">
      <h3>Atomicity Warnings</h3>
      <p v-for="warning in warnings" :key="warning.ruleId">
        {{ warning.ruleId }} · {{ warning.message }}
      </p>
    </div>
  </LocatorNodeFrame>
</template>
