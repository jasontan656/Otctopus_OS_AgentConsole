<script setup lang="ts">
import LocatorNodeFrame from '../LocatorNodeFrame'
import { LOCATOR_TOOLBAR_CONTRACT } from './LocatorToolbar.contract'
import { UI_COMPONENTS } from '../../contracts/ui-identity-registry'
import { useUiLocatorState } from '../../composables/useUiLocatorState'
import { useUiLocatorNode } from '../../composables/useUiLocatorNode'

const toolbarNode = useUiLocatorNode(UI_COMPONENTS.locatorToolbar.id)
const { enabled, toggle } = useUiLocatorState()
</script>

<template>
  <LocatorNodeFrame :node="toolbarNode">
    <div class="locator-toolbar">
      <div>
        <p class="locator-toolbar-label">AI Locator</p>
        <strong>{{ enabled ? LOCATOR_TOOLBAR_CONTRACT.visibleLabel : LOCATOR_TOOLBAR_CONTRACT.hiddenLabel }}</strong>
      </div>
      <button class="locator-toggle" @click="toggle">
        {{ enabled ? LOCATOR_TOOLBAR_CONTRACT.disableLabel : LOCATOR_TOOLBAR_CONTRACT.enableLabel }}
      </button>
    </div>
  </LocatorNodeFrame>
</template>
