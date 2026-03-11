<script setup lang="ts">
import type { RuntimeLiveState } from '../contracts/showroom-container-contract'
import type { PreviewPayload } from '../types'

defineProps<{
  payload: PreviewPayload | null
  liveState: RuntimeLiveState
  statusLabel: string
  lastError: string | null
}>()
</script>

<template>
  <section class="panel runtime-status-panel">
    <div class="panel-head">
      <div>
        <h2>Runtime Status</h2>
        <p>runtime bridge、payload 健康度与 graph 摘要由 scene 层统一暴露。</p>
      </div>
      <span class="timestamp">{{ payload?.updatedAt ?? 'waiting for payload' }}</span>
    </div>

    <div class="runtime-status-grid">
      <div class="stat-card">
        <span>Live</span>
        <strong>{{ liveState }}</strong>
      </div>
      <div class="stat-card">
        <span>Status</span>
        <strong>{{ statusLabel }}</strong>
      </div>
      <div class="stat-card">
        <span>Docs</span>
        <strong>{{ payload?.summary.nodeCount ?? 0 }}</strong>
      </div>
      <div class="stat-card">
        <span>Edges</span>
        <strong>{{ payload?.summary.edgeCount ?? 0 }}</strong>
      </div>
    </div>

    <p class="runtime-note">
      <strong>Target:</strong> {{ payload?.targetRoot ?? 'loading' }}
      <span v-if="lastError"> · {{ lastError }}</span>
    </p>
  </section>
</template>
