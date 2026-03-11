<script setup lang="ts">
import LocatorNodeFrame from './LocatorNodeFrame.vue'
import {
  UI_COMPONENTS,
  UI_COMPONENT_LIST,
  UI_CONTAINER_LIST,
  UI_LAYERS,
} from '../contracts/ui-identity-registry'
import { useUiLocatorNode } from '../composables/useUiLocatorNode'

const legendNode = useUiLocatorNode(UI_COMPONENTS.locatorLegend.id)
</script>

<template>
  <LocatorNodeFrame :node="legendNode">
    <section class="locator-legend">
      <div class="locator-legend-section">
        <h3>Layers</h3>
        <p v-for="layer in UI_LAYERS" :key="layer.id" class="locator-legend-item">
          <strong>[{{ layer.shortCode }}]</strong> {{ layer.id }} · {{ layer.name }}
        </p>
      </div>

      <div class="locator-legend-section">
        <h3>Containers</h3>
        <p v-for="node in UI_CONTAINER_LIST" :key="node.id" class="locator-legend-item">
          <strong>[{{ node.shortCode }}]</strong> {{ node.id }}
        </p>
      </div>

      <div class="locator-legend-section">
        <h3>Components</h3>
        <p v-for="node in UI_COMPONENT_LIST" :key="node.id" class="locator-legend-item">
          <strong>[{{ node.shortCode }}]</strong> {{ node.id }}
        </p>
      </div>
    </section>
  </LocatorNodeFrame>
</template>
