import { UI_NODE_MAP, type UiNodeDefinition } from '../contracts/ui-identity-registry'

export function useUiLocatorNode(nodeId: string): UiNodeDefinition {
  const node = UI_NODE_MAP[nodeId]
  if (!node) {
    throw new Error(`unknown ui locator node: ${nodeId}`)
  }
  return node
}
