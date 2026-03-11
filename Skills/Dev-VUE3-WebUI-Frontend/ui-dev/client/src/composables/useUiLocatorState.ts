import { inject, provide, ref, watch, type Ref } from 'vue'

interface UiLocatorState {
  enabled: Ref<boolean>
  toggle: () => void
}

const UI_LOCATOR_STATE_KEY = Symbol('ui-locator-state')
const STORAGE_KEY = 'dev-vue3-showroom-locator-enabled'

export function provideUiLocatorState(): UiLocatorState {
  const enabled = ref(false)

  if (typeof window !== 'undefined') {
    enabled.value = window.localStorage.getItem(STORAGE_KEY) === '1'
    watch(enabled, (nextValue) => {
      window.localStorage.setItem(STORAGE_KEY, nextValue ? '1' : '0')
    }, { immediate: true })
  }

  const state: UiLocatorState = {
    enabled,
    toggle: () => {
      enabled.value = !enabled.value
    },
  }

  provide(UI_LOCATOR_STATE_KEY, state)
  return state
}

export function useUiLocatorState(): UiLocatorState {
  const state = inject<UiLocatorState>(UI_LOCATOR_STATE_KEY)
  if (!state) {
    throw new Error('ui locator state has not been provided')
  }
  return state
}
