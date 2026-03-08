/**
 * Resource Views (Multi-Repo)
 *
 * Provides structured on-demand data to the local code-graph CLI.
 * All resources use repo-scoped URIs: codegraph://repo/{name}/context
 */
import type { LocalBackend } from './local/local-backend.js';
export interface ResourceDefinition {
    uri: string;
    name: string;
    description: string;
    mimeType: string;
}
export interface ResourceTemplate {
    uriTemplate: string;
    name: string;
    description: string;
    mimeType: string;
}
/**
 * Static resources — includes the global repos list
 */
export declare function getResourceDefinitions(): ResourceDefinition[];
/**
 * Dynamic resource templates
 */
export declare function getResourceTemplates(): ResourceTemplate[];
/**
 * Read a resource and return its content
 */
export declare function readResource(uri: string, backend: LocalBackend): Promise<string>;
