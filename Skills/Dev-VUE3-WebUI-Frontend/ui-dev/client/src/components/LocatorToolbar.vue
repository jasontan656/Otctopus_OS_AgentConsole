<script setup lang="ts">
import LocatorNodeFrame from './LocatorNodeFrame.vue'
import { UI_COMPONENTS } from '../contracts/ui-identity-registry'
import { useUiLocatorState } from '../composables/useUiLocatorState'
import { useUiLocatorNode } from '../composables/useUiLocatorNode'

const toolbarNode = useUiLocatorNode(UI_COMPONENTS.locatorToolbar.id)
const { enabled, toggle } = useUiLocatorState()
</script>

<template>
  <LocatorNodeFrame :node="toolbarNode">
    <div class="locator-toolbar">
      <div>
        <p class="locator-toolbar-label">AI Locator</p>
        <strong>{{ enabled ? 'Visible' : 'Hidden' }}</strong>
      </div>
      <button class="locator-toggle" @click="toggle">
        {{ enabled ? 'Hide IDs' : 'Show IDs' }}
      </button>
    </div>
  </LocatorNodeFrame>
</template>
