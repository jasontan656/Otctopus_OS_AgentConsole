<script setup lang="ts">
import LocatorLegend from '../components/LocatorLegend'
import LocatorNodeFrame from '../components/LocatorNodeFrame'
import LocatorToolbar from '../components/LocatorToolbar'
import { UI_CONTAINERS } from '../contracts/ui-identity-registry'
import { useUiLocatorNode } from '../composables/useUiLocatorNode'
import { useUiLocatorState } from '../composables/useUiLocatorState'

const overlayNode = useUiLocatorNode(UI_CONTAINERS.locatorOverlay.id)
const { enabled } = useUiLocatorState()
</script>

<template>
  <div class="locator-overlay-host">
    <LocatorNodeFrame :node="overlayNode">
      <aside class="locator-overlay">
        <LocatorToolbar />
        <LocatorLegend v-if="enabled" />
      </aside>
    </LocatorNodeFrame>
  </div>
</template>
