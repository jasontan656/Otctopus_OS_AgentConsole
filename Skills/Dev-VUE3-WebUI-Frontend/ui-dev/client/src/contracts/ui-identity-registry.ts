export type UiLayerId = 'SH' | 'SC' | 'RT' | 'WK' | 'PN' | 'AT' | 'GV' | 'DC' | 'DX' | 'OV'

export interface UiLayerDefinition {
  id: UiLayerId
  shortCode: UiLayerId
  name: string
  description: string
}

export interface UiContainerDefinition {
  kind: 'container'
  id: `${UiLayerId}-${string}`
  shortCode: string
  layerId: UiLayerId
  containerName: string
  file: string
  surface: 'frame' | 'legend'
}

export interface UiComponentDefinition {
  kind: 'component'
  id: `${UiLayerId}-${string}-${string}`
  shortCode: string
  layerId: UiLayerId
  containerId: UiContainerDefinition['id']
  componentName: string
  role: 'primitive' | 'composite' | 'visual_engine' | 'dev_support'
  file: string
  packageDir: string
  entryFile: string
  contractFile: string
  styleFile: string
  surface: 'frame' | 'legend'
}

export type UiNodeDefinition = UiContainerDefinition | UiComponentDefinition

export const UI_LAYERS: UiLayerDefinition[] = [
  { id: 'SH', shortCode: 'SH', name: 'Shell', description: '顶层页面骨架与全局 page chrome。' },
  { id: 'SC', shortCode: 'SC', name: 'Scene', description: 'route scene 入口与场景级编排。' },
  { id: 'RT', shortCode: 'RT', name: 'Runtime', description: 'payload bridge、live status 与 runtime handshake。' },
  { id: 'WK', shortCode: 'WK', name: 'Workspace', description: '多 panel 工作区与共享选择态。' },
  { id: 'PN', shortCode: 'PN', name: 'Panel', description: 'feature panel 容器。' },
  { id: 'AT', shortCode: 'AT', name: 'Atom', description: '轻量 UI 原子件。' },
  { id: 'GV', shortCode: 'GV', name: 'GraphView', description: 'graph 可视表达。' },
  { id: 'DC', shortCode: 'DC', name: 'DocContent', description: '正文、anchor、warning 阅读表达。' },
  { id: 'DX', shortCode: 'DX', name: 'DevLocator', description: 'AI / human 协作定位层。' },
  { id: 'OV', shortCode: 'OV', name: 'Overlay', description: '未来 drawer / modal / palette 等瞬时界面。' },
]

export const UI_CONTAINERS = {
  appShell: {
    kind: 'container',
    id: 'SH-AppShell',
    shortCode: 'AS',
    layerId: 'SH',
    containerName: 'AppShell',
    file: 'ui-dev/client/src/containers/AppShellContainer.vue',
    surface: 'frame',
  },
  showroomRouteScene: {
    kind: 'container',
    id: 'SC-ShowroomRouteScene',
    shortCode: 'RS',
    layerId: 'SC',
    containerName: 'ShowroomRouteScene',
    file: 'ui-dev/client/src/containers/ShowroomRouteSceneContainer.vue',
    surface: 'frame',
  },
  showroomRuntimeBridge: {
    kind: 'container',
    id: 'RT-ShowroomRuntimeBridge',
    shortCode: 'RB',
    layerId: 'RT',
    containerName: 'ShowroomRuntimeBridge',
    file: 'ui-dev/client/src/composables/useShowroomRuntimeBridge.ts',
    surface: 'legend',
  },
  runtimeStatus: {
    kind: 'container',
    id: 'RT-RuntimeStatus',
    shortCode: 'ST',
    layerId: 'RT',
    containerName: 'RuntimeStatus',
    file: 'ui-dev/client/src/containers/RuntimeStatusContainer.vue',
    surface: 'frame',
  },
  showroomWorkspace: {
    kind: 'container',
    id: 'WK-ShowroomWorkspace',
    shortCode: 'WS',
    layerId: 'WK',
    containerName: 'ShowroomWorkspace',
    file: 'ui-dev/client/src/containers/ShowroomWorkspaceContainer.vue',
    surface: 'frame',
  },
  documentNavigator: {
    kind: 'container',
    id: 'PN-DocumentNavigator',
    shortCode: 'NV',
    layerId: 'PN',
    containerName: 'DocumentNavigator',
    file: 'ui-dev/client/src/containers/DocumentNavigatorContainer.vue',
    surface: 'frame',
  },
  graphPanel: {
    kind: 'container',
    id: 'PN-GraphPanel',
    shortCode: 'GP',
    layerId: 'PN',
    containerName: 'GraphPanel',
    file: 'ui-dev/client/src/containers/GraphPanelContainer.vue',
    surface: 'frame',
  },
  documentReader: {
    kind: 'container',
    id: 'PN-DocumentReader',
    shortCode: 'DR',
    layerId: 'PN',
    containerName: 'DocumentReader',
    file: 'ui-dev/client/src/containers/DocumentReaderContainer.vue',
    surface: 'frame',
  },
  locatorOverlay: {
    kind: 'container',
    id: 'DX-LocatorOverlay',
    shortCode: 'LO',
    layerId: 'DX',
    containerName: 'LocatorOverlay',
    file: 'ui-dev/client/src/containers/LocatorOverlayContainer.vue',
    surface: 'frame',
  },
} satisfies Record<string, UiContainerDefinition>

export const UI_COMPONENTS = {
  locatorFrame: {
    kind: 'component',
    id: 'DX-LocatorOverlay-LocatorFrame',
    shortCode: 'LF',
    layerId: 'DX',
    containerId: UI_CONTAINERS.locatorOverlay.id,
    componentName: 'LocatorFrame',
    role: 'dev_support',
    file: 'ui-dev/client/src/components/LocatorNodeFrame/LocatorNodeFrame.vue',
    packageDir: 'ui-dev/client/src/components/LocatorNodeFrame',
    entryFile: 'ui-dev/client/src/components/LocatorNodeFrame/index.ts',
    contractFile: 'ui-dev/client/src/components/LocatorNodeFrame/LocatorNodeFrame.contract.ts',
    styleFile: 'ui-dev/client/src/components/LocatorNodeFrame/LocatorNodeFrame.tokens.css',
    surface: 'legend',
  },
  locatorToolbar: {
    kind: 'component',
    id: 'DX-LocatorOverlay-LocatorToolbar',
    shortCode: 'LT',
    layerId: 'DX',
    containerId: UI_CONTAINERS.locatorOverlay.id,
    componentName: 'LocatorToolbar',
    role: 'dev_support',
    file: 'ui-dev/client/src/components/LocatorToolbar/LocatorToolbar.vue',
    packageDir: 'ui-dev/client/src/components/LocatorToolbar',
    entryFile: 'ui-dev/client/src/components/LocatorToolbar/index.ts',
    contractFile: 'ui-dev/client/src/components/LocatorToolbar/LocatorToolbar.contract.ts',
    styleFile: 'ui-dev/client/src/components/LocatorToolbar/LocatorToolbar.tokens.css',
    surface: 'frame',
  },
  locatorLegend: {
    kind: 'component',
    id: 'DX-LocatorOverlay-LocatorLegend',
    shortCode: 'LG',
    layerId: 'DX',
    containerId: UI_CONTAINERS.locatorOverlay.id,
    componentName: 'LocatorLegend',
    role: 'dev_support',
    file: 'ui-dev/client/src/components/LocatorLegend/LocatorLegend.vue',
    packageDir: 'ui-dev/client/src/components/LocatorLegend',
    entryFile: 'ui-dev/client/src/components/LocatorLegend/index.ts',
    contractFile: 'ui-dev/client/src/components/LocatorLegend/LocatorLegend.contract.ts',
    styleFile: 'ui-dev/client/src/components/LocatorLegend/LocatorLegend.tokens.css',
    surface: 'frame',
  },
  runtimeStatusStatCard: {
    kind: 'component',
    id: 'AT-RuntimeStatus-StatCard',
    shortCode: 'RC',
    layerId: 'AT',
    containerId: UI_CONTAINERS.runtimeStatus.id,
    componentName: 'StatCard',
    role: 'primitive',
    file: 'ui-dev/client/src/components/RuntimeStatusStatCard/RuntimeStatusStatCard.vue',
    packageDir: 'ui-dev/client/src/components/RuntimeStatusStatCard',
    entryFile: 'ui-dev/client/src/components/RuntimeStatusStatCard/index.ts',
    contractFile: 'ui-dev/client/src/components/RuntimeStatusStatCard/RuntimeStatusStatCard.contract.ts',
    styleFile: 'ui-dev/client/src/components/RuntimeStatusStatCard/RuntimeStatusStatCard.tokens.css',
    surface: 'frame',
  },
  documentNavigatorSearchBox: {
    kind: 'component',
    id: 'AT-DocumentNavigator-SearchBox',
    shortCode: 'SB',
    layerId: 'AT',
    containerId: UI_CONTAINERS.documentNavigator.id,
    componentName: 'SearchBox',
    role: 'primitive',
    file: 'ui-dev/client/src/components/DocumentNavigatorSearchBox/DocumentNavigatorSearchBox.vue',
    packageDir: 'ui-dev/client/src/components/DocumentNavigatorSearchBox',
    entryFile: 'ui-dev/client/src/components/DocumentNavigatorSearchBox/index.ts',
    contractFile: 'ui-dev/client/src/components/DocumentNavigatorSearchBox/DocumentNavigatorSearchBox.contract.ts',
    styleFile: 'ui-dev/client/src/components/DocumentNavigatorSearchBox/DocumentNavigatorSearchBox.tokens.css',
    surface: 'frame',
  },
  documentNavigatorDocItem: {
    kind: 'component',
    id: 'AT-DocumentNavigator-DocItem',
    shortCode: 'DI',
    layerId: 'AT',
    containerId: UI_CONTAINERS.documentNavigator.id,
    componentName: 'DocItem',
    role: 'primitive',
    file: 'ui-dev/client/src/components/DocumentNavigatorDocItem/DocumentNavigatorDocItem.vue',
    packageDir: 'ui-dev/client/src/components/DocumentNavigatorDocItem',
    entryFile: 'ui-dev/client/src/components/DocumentNavigatorDocItem/index.ts',
    contractFile: 'ui-dev/client/src/components/DocumentNavigatorDocItem/DocumentNavigatorDocItem.contract.ts',
    styleFile: 'ui-dev/client/src/components/DocumentNavigatorDocItem/DocumentNavigatorDocItem.tokens.css',
    surface: 'frame',
  },
  graphPanelGraphCanvas: {
    kind: 'component',
    id: 'GV-GraphPanel-GraphCanvas',
    shortCode: 'GC',
    layerId: 'GV',
    containerId: UI_CONTAINERS.graphPanel.id,
    componentName: 'GraphCanvas',
    role: 'visual_engine',
    file: 'ui-dev/client/src/components/GraphCanvas/GraphCanvas.vue',
    packageDir: 'ui-dev/client/src/components/GraphCanvas',
    entryFile: 'ui-dev/client/src/components/GraphCanvas/index.ts',
    contractFile: 'ui-dev/client/src/components/GraphCanvas/GraphCanvas.contract.ts',
    styleFile: 'ui-dev/client/src/components/GraphCanvas/GraphCanvas.tokens.css',
    surface: 'frame',
  },
  documentReaderDetailHero: {
    kind: 'component',
    id: 'DC-DocumentReader-DetailHero',
    shortCode: 'DH',
    layerId: 'DC',
    containerId: UI_CONTAINERS.documentReader.id,
    componentName: 'DetailHero',
    role: 'composite',
    file: 'ui-dev/client/src/components/DocumentReaderDetailHero/DocumentReaderDetailHero.vue',
    packageDir: 'ui-dev/client/src/components/DocumentReaderDetailHero',
    entryFile: 'ui-dev/client/src/components/DocumentReaderDetailHero/index.ts',
    contractFile: 'ui-dev/client/src/components/DocumentReaderDetailHero/DocumentReaderDetailHero.contract.ts',
    styleFile: 'ui-dev/client/src/components/DocumentReaderDetailHero/DocumentReaderDetailHero.tokens.css',
    surface: 'frame',
  },
  documentReaderAnchorChip: {
    kind: 'component',
    id: 'DC-DocumentReader-AnchorChip',
    shortCode: 'AC',
    layerId: 'DC',
    containerId: UI_CONTAINERS.documentReader.id,
    componentName: 'AnchorChip',
    role: 'primitive',
    file: 'ui-dev/client/src/components/DocumentReaderAnchorChip/DocumentReaderAnchorChip.vue',
    packageDir: 'ui-dev/client/src/components/DocumentReaderAnchorChip',
    entryFile: 'ui-dev/client/src/components/DocumentReaderAnchorChip/index.ts',
    contractFile: 'ui-dev/client/src/components/DocumentReaderAnchorChip/DocumentReaderAnchorChip.contract.ts',
    styleFile: 'ui-dev/client/src/components/DocumentReaderAnchorChip/DocumentReaderAnchorChip.tokens.css',
    surface: 'frame',
  },
  documentReaderWarningList: {
    kind: 'component',
    id: 'DC-DocumentReader-WarningList',
    shortCode: 'WL',
    layerId: 'DC',
    containerId: UI_CONTAINERS.documentReader.id,
    componentName: 'WarningList',
    role: 'composite',
    file: 'ui-dev/client/src/components/DocumentReaderWarningList/DocumentReaderWarningList.vue',
    packageDir: 'ui-dev/client/src/components/DocumentReaderWarningList',
    entryFile: 'ui-dev/client/src/components/DocumentReaderWarningList/index.ts',
    contractFile: 'ui-dev/client/src/components/DocumentReaderWarningList/DocumentReaderWarningList.contract.ts',
    styleFile: 'ui-dev/client/src/components/DocumentReaderWarningList/DocumentReaderWarningList.tokens.css',
    surface: 'frame',
  },
  documentReaderMarkdownBody: {
    kind: 'component',
    id: 'DC-DocumentReader-MarkdownBody',
    shortCode: 'MB',
    layerId: 'DC',
    containerId: UI_CONTAINERS.documentReader.id,
    componentName: 'MarkdownBody',
    role: 'composite',
    file: 'ui-dev/client/src/components/DocumentReaderMarkdownBody/DocumentReaderMarkdownBody.vue',
    packageDir: 'ui-dev/client/src/components/DocumentReaderMarkdownBody',
    entryFile: 'ui-dev/client/src/components/DocumentReaderMarkdownBody/index.ts',
    contractFile: 'ui-dev/client/src/components/DocumentReaderMarkdownBody/DocumentReaderMarkdownBody.contract.ts',
    styleFile: 'ui-dev/client/src/components/DocumentReaderMarkdownBody/DocumentReaderMarkdownBody.tokens.css',
    surface: 'frame',
  },
} satisfies Record<string, UiComponentDefinition>

export const UI_CONTAINER_LIST = Object.values(UI_CONTAINERS)
export const UI_COMPONENT_LIST = Object.values(UI_COMPONENTS)
export const UI_NODE_LIST: UiNodeDefinition[] = [...UI_CONTAINER_LIST, ...UI_COMPONENT_LIST]

export const UI_NODE_MAP = Object.fromEntries(UI_NODE_LIST.map((node) => [node.id, node])) as Record<string, UiNodeDefinition>
