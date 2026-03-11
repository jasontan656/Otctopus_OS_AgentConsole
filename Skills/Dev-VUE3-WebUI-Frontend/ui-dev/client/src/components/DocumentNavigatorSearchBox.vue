<script setup lang="ts">
import LocatorNodeFrame from './LocatorNodeFrame.vue'
import { UI_COMPONENTS } from '../contracts/ui-identity-registry'
import { useUiLocatorNode } from '../composables/useUiLocatorNode'

defineProps<{
  modelValue: string
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const searchNode = useUiLocatorNode(UI_COMPONENTS.documentNavigatorSearchBox.id)
</script>

<template>
  <LocatorNodeFrame :node="searchNode">
    <input
      :value="modelValue"
      class="search-box"
      placeholder="Search path / topic / type"
      @input="emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    />
  </LocatorNodeFrame>
</template>
