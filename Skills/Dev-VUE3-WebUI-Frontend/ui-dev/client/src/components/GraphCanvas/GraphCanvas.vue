<script setup lang="ts">
import { computed } from 'vue'
import dagre from '@dagrejs/dagre'
import { Background } from '@vue-flow/background'
import { Controls } from '@vue-flow/controls'
import { MiniMap } from '@vue-flow/minimap'
import { MarkerType, Position, VueFlow } from '@vue-flow/core'
import type { Edge, Node } from '@vue-flow/core'
import LocatorNodeFrame from '../LocatorNodeFrame'
import { DOC_TYPE_PALETTE } from './GraphCanvas.contract'
import { UI_COMPONENTS } from '../../contracts/ui-identity-registry'
import { useUiLocatorNode } from '../../composables/useUiLocatorNode'
import type { GraphEdgeRecord, PreviewDocumentRecord } from '../../types'

const props = defineProps<{
  docs: PreviewDocumentRecord[]
  edges: GraphEdgeRecord[]
  selectedPath: string
}>()

const emit = defineEmits<{
  select: [path: string]
}>()

const graphCanvasNode = useUiLocatorNode(UI_COMPONENTS.graphPanelGraphCanvas.id)

const flowNodes = computed<Node[]>(() => {
  const graph = new dagre.graphlib.Graph()
  graph.setGraph({ rankdir: 'LR', ranksep: 68, nodesep: 28, marginx: 24, marginy: 24 })
  graph.setDefaultEdgeLabel(() => ({}))

  for (const doc of props.docs) {
    graph.setNode(doc.path, { width: 260, height: 90 })
  }

  for (const edge of props.edges) {
    graph.setEdge(edge.source, edge.target)
  }

  dagre.layout(graph)

  return props.docs.map((doc) => {
    const box = graph.node(doc.path)
    return {
      id: doc.path,
      position: { x: box?.x ?? 0, y: box?.y ?? 0 },
      sourcePosition: Position.Right,
      targetPosition: Position.Left,
      draggable: true,
      data: {
        label: `${doc.title}\n${doc.docType}`,
      },
        style: {
          width: '260px',
          borderRadius: '20px',
          border: doc.path === props.selectedPath ? '2px solid #fefefe' : '1px solid rgba(255,255,255,0.18)',
          background: doc.path === props.selectedPath
          ? `linear-gradient(135deg, ${DOC_TYPE_PALETTE[doc.docType] ?? '#1f2937'} 0%, #0f172a 100%)`
          : `linear-gradient(135deg, ${DOC_TYPE_PALETTE[doc.docType] ?? '#334155'} 0%, rgba(15,23,42,0.92) 100%)`,
        color: '#f8fafc',
        boxShadow: doc.path === props.selectedPath ? '0 24px 60px rgba(15, 23, 42, 0.35)' : '0 12px 32px rgba(15, 23, 42, 0.18)',
        fontFamily: '"IBM Plex Sans", "Segoe UI", sans-serif',
        whiteSpace: 'pre-line',
        padding: '14px 16px',
      },
    }
  })
})

const flowEdges = computed<Edge[]>(() => props.edges.map((edge) => ({
  id: `${edge.source}=>${edge.target}`,
  source: edge.source,
  target: edge.target,
  label: edge.relation,
  markerEnd: MarkerType.ArrowClosed,
  style: {
    stroke: edge.direction === 'downstream'
      ? '#f97316'
      : edge.direction === 'upstream'
        ? '#38bdf8'
        : edge.direction === 'cross'
          ? '#facc15'
          : '#c084fc',
    strokeWidth: 2,
  },
  labelStyle: {
    fill: '#0f172a',
    fontWeight: 600,
    fontSize: 12,
  },
  labelBgStyle: {
    fill: 'rgba(255,255,255,0.92)',
    fillOpacity: 1,
  },
  animated: edge.direction === 'cross',
})))
</script>

<template>
  <LocatorNodeFrame :node="graphCanvasNode">
    <div class="graph-canvas-shell">
      <VueFlow
        :nodes="flowNodes"
        :edges="flowEdges"
        fit-view-on-init
        :min-zoom="0.2"
        :max-zoom="1.8"
        class="graph-canvas-flow"
        @node-click="({ node }) => emit('select', node.id)"
      >
        <Background pattern-color="rgba(15, 23, 42, 0.1)" :gap="28" />
        <MiniMap pannable zoomable />
        <Controls />
      </VueFlow>
    </div>
  </LocatorNodeFrame>
</template>
