<script setup lang="ts">
import LocatorNodeFrame from '../LocatorNodeFrame'
import { DOCUMENT_NAVIGATOR_SEARCH_BOX_CONTRACT } from './DocumentNavigatorSearchBox.contract'
import { UI_COMPONENTS } from '../../contracts/ui-identity-registry'
import { useUiLocatorNode } from '../../composables/useUiLocatorNode'

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
      class="document-search-box"
      :placeholder="DOCUMENT_NAVIGATOR_SEARCH_BOX_CONTRACT.placeholder"
      @input="emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    />
  </LocatorNodeFrame>
</template>
