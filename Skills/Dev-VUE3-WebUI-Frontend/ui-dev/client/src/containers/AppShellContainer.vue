<script setup lang="ts">
import LocatorNodeFrame from '../components/LocatorNodeFrame.vue'
import { UI_CONTAINERS } from '../contracts/ui-identity-registry'
import { provideUiLocatorState } from '../composables/useUiLocatorState'
import { useUiLocatorNode } from '../composables/useUiLocatorNode'
import LocatorOverlayContainer from './LocatorOverlayContainer.vue'
import ShowroomRouteSceneContainer from './ShowroomRouteSceneContainer.vue'

provideUiLocatorState()
const shellNode = useUiLocatorNode(UI_CONTAINERS.appShell.id)
</script>

<template>
  <LocatorNodeFrame :node="shellNode">
    <div class="page-shell">
      <header class="page-hero">
        <div>
          <p class="eyebrow">Skill Front Door</p>
          <h1>Dev-VUE3-WebUI-Frontend Showroom</h1>
          <p class="hero-copy">
            默认落点就是 <code>SKILL.md</code>。左边筛文档，中间看 graph，右边读正文和挂钩关系；这个页面既是前端规范展厅，也是当前技能的 live doc graph 门面。
          </p>
        </div>
        <div class="hero-sidecopy">
          <p>
            入口只承载 app shell。实际的 runtime bridge、workspace 编排和 panel 交互都在下层容器里收敛，不再由顶层页面单文件兼任。
          </p>
        </div>
      </header>

      <ShowroomRouteSceneContainer />
      <LocatorOverlayContainer />
    </div>
  </LocatorNodeFrame>
</template>
