import { promises as fs } from 'node:fs'
import path from 'node:path'
import { pathToFileURL } from 'node:url'

type RegistryModule = typeof import('../../ui-dev/client/src/contracts/ui-identity-registry.js')

interface UiIdentityViolation {
  scope: 'layer' | 'container' | 'component' | 'file' | 'binding'
  nodeId?: string
  file?: string
  message: string
}

export interface UiIdentityContractPayload {
  layers: RegistryModule['UI_LAYERS']
  containers: RegistryModule['UI_CONTAINER_LIST']
  components: RegistryModule['UI_COMPONENT_LIST']
}

export interface UiIdentityLintPayload {
  status: 'pass' | 'fail'
  targetRoot: string
  summary: {
    layerCount: number
    containerCount: number
    componentCount: number
    violationCount: number
  }
  violations: UiIdentityViolation[]
}

async function loadRegistryModule(targetRoot: string): Promise<RegistryModule> {
  const registryPath = path.join(targetRoot, 'ui-dev', 'client', 'src', 'contracts', 'ui-identity-registry.ts')
  return import(`${pathToFileURL(registryPath).href}?t=${Date.now()}`) as Promise<RegistryModule>
}

async function fileExists(targetPath: string): Promise<boolean> {
  try {
    await fs.access(targetPath)
    return true
  } catch {
    return false
  }
}

async function walkFiles(targetPath: string, matcher: (filename: string) => boolean): Promise<string[]> {
  const entries = await fs.readdir(targetPath, { withFileTypes: true })
  const files: string[] = []

  for (const entry of entries) {
    const entryPath = path.join(targetPath, entry.name)
    if (entry.isDirectory()) {
      files.push(...await walkFiles(entryPath, matcher))
      continue
    }

    if (matcher(entry.name)) {
      files.push(entryPath)
    }
  }

  return files
}

function relativeToSkill(targetRoot: string, filePath: string): string {
  return path.relative(targetRoot, filePath).replaceAll(path.sep, '/')
}

export async function loadUiIdentityContract(targetRoot: string): Promise<UiIdentityContractPayload> {
  const registry = await loadRegistryModule(targetRoot)
  return {
    layers: registry.UI_LAYERS,
    containers: registry.UI_CONTAINER_LIST,
    components: registry.UI_COMPONENT_LIST,
  }
}

export async function lintUiIdentity(targetRoot: string): Promise<UiIdentityLintPayload> {
  const registry = await loadRegistryModule(targetRoot)
  const violations: UiIdentityViolation[] = []
  const layerMap = new Map(registry.UI_LAYERS.map((layer) => [layer.id, layer]))
  const shortCodes = new Map<string, string>()

  for (const layer of registry.UI_LAYERS) {
    if (!/^[A-Z]{2}$/.test(layer.id)) {
      violations.push({ scope: 'layer', nodeId: layer.id, message: 'layer id must be exactly two uppercase letters' })
    }
    if (layer.shortCode !== layer.id) {
      violations.push({ scope: 'layer', nodeId: layer.id, message: 'layer shortCode must equal layer id' })
    }
    if (shortCodes.has(layer.shortCode)) {
      violations.push({ scope: 'layer', nodeId: layer.id, message: `duplicate shortCode with ${shortCodes.get(layer.shortCode)}` })
    } else {
      shortCodes.set(layer.shortCode, layer.id)
    }
  }

  for (const [key, container] of Object.entries(registry.UI_CONTAINERS)) {
    if (!/^[A-Z]{2}-[A-Z][A-Za-z0-9]+$/.test(container.id)) {
      violations.push({ scope: 'container', nodeId: container.id, file: container.file, message: 'container id must match layerId-containerName' })
    }
    if (!layerMap.has(container.layerId)) {
      violations.push({ scope: 'container', nodeId: container.id, file: container.file, message: 'container layerId must exist in the fixed layer catalog' })
    }
    if (!container.id.startsWith(`${container.layerId}-`)) {
      violations.push({ scope: 'container', nodeId: container.id, file: container.file, message: 'container id must start with its layerId' })
    }
    if (!/^[A-Z]{2}$/.test(container.shortCode)) {
      violations.push({ scope: 'container', nodeId: container.id, file: container.file, message: 'container shortCode must be two uppercase letters' })
    }
    if (shortCodes.has(container.shortCode)) {
      violations.push({ scope: 'container', nodeId: container.id, file: container.file, message: `duplicate shortCode with ${shortCodes.get(container.shortCode)}` })
    } else {
      shortCodes.set(container.shortCode, container.id)
    }

    const absoluteFile = path.join(targetRoot, container.file)
    if (!await fileExists(absoluteFile)) {
      violations.push({ scope: 'file', nodeId: container.id, file: container.file, message: 'declared container file does not exist' })
      continue
    }

    const content = await fs.readFile(absoluteFile, 'utf8')
    if (!content.includes(`UI_CONTAINERS.${key}.id`)) {
      violations.push({ scope: 'binding', nodeId: container.id, file: container.file, message: 'container file must bind to its own registry entry' })
    }
  }

  for (const [key, component] of Object.entries(registry.UI_COMPONENTS)) {
    if (!/^[A-Z]{2}-[A-Z][A-Za-z0-9]+-[A-Z][A-Za-z0-9]+$/.test(component.id)) {
      violations.push({ scope: 'component', nodeId: component.id, file: component.file, message: 'component id must match layerId-containerName-componentName' })
    }
    if (!layerMap.has(component.layerId)) {
      violations.push({ scope: 'component', nodeId: component.id, file: component.file, message: 'component layerId must exist in the fixed layer catalog' })
    }
    if (!component.id.startsWith(`${component.layerId}-`)) {
      violations.push({ scope: 'component', nodeId: component.id, file: component.file, message: 'component id must start with its layerId' })
    }
    if (!registry.UI_NODE_MAP[component.containerId]) {
      violations.push({ scope: 'component', nodeId: component.id, file: component.file, message: 'component containerId must reference an existing container node' })
    }
    if (!/^[A-Z]{2}$/.test(component.shortCode)) {
      violations.push({ scope: 'component', nodeId: component.id, file: component.file, message: 'component shortCode must be two uppercase letters' })
    }
    if (shortCodes.has(component.shortCode)) {
      violations.push({ scope: 'component', nodeId: component.id, file: component.file, message: `duplicate shortCode with ${shortCodes.get(component.shortCode)}` })
    } else {
      shortCodes.set(component.shortCode, component.id)
    }

    const absoluteFile = path.join(targetRoot, component.file)
    if (!await fileExists(absoluteFile)) {
      violations.push({ scope: 'file', nodeId: component.id, file: component.file, message: 'declared component file does not exist' })
      continue
    }

    const content = await fs.readFile(absoluteFile, 'utf8')
    if (!content.includes(`UI_COMPONENTS.${key}.id`)) {
      violations.push({ scope: 'binding', nodeId: component.id, file: component.file, message: 'component file must bind to its own registry entry' })
    }
  }

  const containerFiles = await walkFiles(path.join(targetRoot, 'ui-dev', 'client', 'src', 'containers'), (filename) => filename.endsWith('Container.vue'))
  const componentFiles = await walkFiles(path.join(targetRoot, 'ui-dev', 'client', 'src', 'components'), (filename) => filename.endsWith('.vue'))

  const knownContainerFiles = new Set(registry.UI_CONTAINER_LIST
    .filter((node) => node.file.includes('/containers/'))
    .map((node) => node.file))
  const knownComponentFiles = new Set(registry.UI_COMPONENT_LIST.map((node) => node.file))

  for (const filePath of containerFiles) {
    const relativePath = relativeToSkill(targetRoot, filePath)
    if (!knownContainerFiles.has(relativePath)) {
      violations.push({ scope: 'file', file: relativePath, message: 'container file exists without registry coverage' })
    }
  }

  for (const filePath of componentFiles) {
    const relativePath = relativeToSkill(targetRoot, filePath)
    if (!knownComponentFiles.has(relativePath)) {
      violations.push({ scope: 'file', file: relativePath, message: 'component file exists without registry coverage' })
    }
  }

  return {
    status: violations.length === 0 ? 'pass' : 'fail',
    targetRoot,
    summary: {
      layerCount: registry.UI_LAYERS.length,
      containerCount: registry.UI_CONTAINER_LIST.length,
      componentCount: registry.UI_COMPONENT_LIST.length,
      violationCount: violations.length,
    },
    violations,
  }
}
