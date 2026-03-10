<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import MarkdownIt from 'markdown-it'
import GraphCanvas from './components/GraphCanvas.vue'
import type { PreviewDocumentRecord, PreviewPayload } from './types'

const payload = ref<PreviewPayload | null>(null)
const selectedPath = ref('SKILL.md')
const liveState = ref<'connecting' | 'live' | 'stale'>('connecting')
const search = ref('')
let socket: WebSocket | null = null

const markdown = new MarkdownIt({
  html: false,
  linkify: true,
  typographer: true,
})

async function loadInitialPayload() {
  const response = await fetch('/api/preview')
  const nextPayload = (await response.json()) as PreviewPayload
  payload.value = nextPayload
  ensureSelection(nextPayload)
}

function connectSocket() {
  const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws'
  socket = new WebSocket(`${protocol}://${window.location.host}/live`)

  socket.addEventListener('open', () => {
    liveState.value = 'live'
  })

  socket.addEventListener('message', (event) => {
    const packet = JSON.parse(event.data)
    if (packet.type === 'payload') {
      payload.value = packet.payload as PreviewPayload
      ensureSelection(packet.payload as PreviewPayload)
      liveState.value = 'live'
    }
    if (packet.type === 'error') {
      liveState.value = 'stale'
    }
  })

  socket.addEventListener('close', () => {
    liveState.value = 'stale'
  })
}

function ensureSelection(nextPayload: PreviewPayload) {
  const entryPath = nextPayload.view.entryPath || nextPayload.docs[0]?.path || ''
  if (!nextPayload.docs.some((doc) => doc.path === selectedPath.value)) {
    selectedPath.value = entryPath
  }
}

const docs = computed(() => payload.value?.docs ?? [])
const filteredDocs = computed(() => {
  const keyword = search.value.trim().toLowerCase()
  if (!keyword) {
    return docs.value
  }
  return docs.value.filter((doc) => {
    return [doc.path, doc.title, doc.docType, doc.topic].some((item) => item.toLowerCase().includes(keyword))
  })
})

const selectedDoc = computed<PreviewDocumentRecord | null>(() => {
  return docs.value.find((doc) => doc.path === selectedPath.value) ?? null
})

const renderedMarkdown = computed(() => {
  return selectedDoc.value ? markdown.render(selectedDoc.value.body) : ''
})

const statusLabel = computed(() => {
  if (!payload.value) return 'Loading'
  if (payload.value.status === 'fail') return 'Graph Broken'
  if (payload.value.status === 'pass_with_warnings') return 'Graph Warning'
  return 'Graph Healthy'
})

watch(payload, (nextPayload) => {
  if (nextPayload) {
    ensureSelection(nextPayload)
  }
})

onMounted(async () => {
  await loadInitialPayload()
  connectSocket()
})

onBeforeUnmount(() => {
  socket?.close()
})
</script>

<template>
  <div class="page-shell">
    <header class="page-hero">
      <div>
        <p class="eyebrow">Skill Front Door</p>
        <h1>Meta-VUE3-WebUI-frontend Showroom</h1>
        <p class="hero-copy">
          默认落点就是 <code>SKILL.md</code>。左边筛文档，中间看 graph，右边读正文和挂钩关系；这个页面既是前端规范展厅，也是当前技能的 live doc graph 门面。
        </p>
      </div>
      <div class="hero-stats">
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
    </header>

    <main class="dashboard-grid">
      <aside class="panel sidebar">
        <div class="panel-head">
          <h2>Document Index</h2>
          <input v-model="search" class="search-box" placeholder="Search path / topic / type" />
        </div>
        <div class="doc-list">
          <button
            v-for="doc in filteredDocs"
            :key="doc.path"
            class="doc-item"
            :class="{ active: doc.path === selectedPath }"
            @click="selectedPath = doc.path"
          >
            <span class="doc-title">{{ doc.title }}</span>
            <span class="doc-meta">{{ doc.docType }} · {{ doc.anchorCount }} anchors</span>
            <span class="doc-path">{{ doc.path }}</span>
          </button>
        </div>
      </aside>

      <section class="panel graph-panel">
        <div class="panel-head">
          <div>
            <h2>Anchor Graph</h2>
            <p>{{ payload?.targetRoot }}</p>
          </div>
          <span class="timestamp">{{ payload?.updatedAt }}</span>
        </div>
        <GraphCanvas
          :docs="docs"
          :edges="payload?.graph.edges ?? []"
          :selected-path="selectedPath"
          @select="selectedPath = $event"
        />
      </section>

      <section class="panel detail-panel">
        <div v-if="selectedDoc" class="detail-stack">
          <div class="detail-hero">
            <p class="eyebrow">Selected Doc</p>
            <h2>{{ selectedDoc.title }}</h2>
            <p class="detail-topic">{{ selectedDoc.topic }}</p>
            <p class="detail-path">{{ selectedDoc.path }}</p>
          </div>

          <div class="anchor-section">
            <div>
              <h3>Outgoing Anchors</h3>
              <button
                v-for="edge in selectedDoc.outgoing"
                :key="`${edge.source}-${edge.target}-${edge.relation}`"
                class="anchor-chip"
                @click="selectedPath = edge.target"
              >
                {{ edge.direction }} · {{ edge.relation }} → {{ edge.target }}
              </button>
            </div>
            <div>
              <h3>Incoming Anchors</h3>
              <button
                v-for="edge in selectedDoc.incoming"
                :key="`${edge.target}-${edge.source}-${edge.relation}`"
                class="anchor-chip secondary"
                @click="selectedPath = edge.source"
              >
                {{ edge.direction }} · {{ edge.relation }} ← {{ edge.source }}
              </button>
            </div>
          </div>

          <div v-if="selectedDoc.warnings.length" class="warning-box">
            <h3>Atomicity Warnings</h3>
            <p v-for="warning in selectedDoc.warnings" :key="warning.ruleId">
              {{ warning.ruleId }} · {{ warning.message }}
            </p>
          </div>

          <article class="markdown-body" v-html="renderedMarkdown"></article>
        </div>
      </section>
    </main>
  </div>
</template>
