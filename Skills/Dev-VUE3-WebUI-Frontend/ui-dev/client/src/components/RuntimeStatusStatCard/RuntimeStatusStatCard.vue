<script setup lang="ts">
import LocatorNodeFrame from '../LocatorNodeFrame'
import { UI_COMPONENTS } from '../../contracts/ui-identity-registry'
import { useUiLocatorNode } from '../../composables/useUiLocatorNode'

defineProps<{
  label: string
  value: string | number
}>()

const statCardNode = useUiLocatorNode(UI_COMPONENTS.runtimeStatusStatCard.id)
</script>

<template>
  <LocatorNodeFrame :node="statCardNode">
    <div class="runtime-stat-card">
      <span>{{ label }}</span>
      <strong>{{ value }}</strong>
    </div>
  </LocatorNodeFrame>
</template>
