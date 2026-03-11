/**
 * Direct CLI Tool Commands
 *
 * Exposes GitNexus tools (query, context, impact, cypher) as direct CLI commands.
 * Bypasses MCP entirely — invokes LocalBackend directly for minimal overhead.
 *
 * Usage:
 *   gitnexus query "authentication flow"
 *   gitnexus context --name "validateUser"
 *   gitnexus impact --target "AuthService" --direction upstream
 *   gitnexus cypher "MATCH (n:Function) RETURN n.name LIMIT 10"
 *
 * Note: Output goes to stderr because KuzuDB's native module captures stdout
 * at the OS level during init. This is consistent with augment.ts.
 */
import { LocalBackend } from '../mcp/local/local-backend.js';
import { readResource } from '../mcp/resources.js';
let _backend = null;
async function getBackend() {
    if (_backend)
        return _backend;
    _backend = new LocalBackend();
    const ok = await _backend.init();
    if (!ok) {
        console.error('Meta-code-graph-base: No indexed repositories found. Run: meta-code-graph-base-core analyze');
        process.exit(1);
    }
    return _backend;
}
function output(data) {
    const text = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
    // stderr because KuzuDB captures stdout at OS level
    process.stderr.write(text + '\n');
}
export async function queryCommand(queryText, options) {
    if (!queryText?.trim()) {
        console.error('Usage: gitnexus query <search_query>');
        process.exit(1);
    }
    const backend = await getBackend();
    const result = await backend.callTool('query', {
        query: queryText,
        task_context: options?.context,
        goal: options?.goal,
        limit: options?.limit ? parseInt(options.limit) : undefined,
        include_content: options?.content ?? false,
        repo: options?.repo,
    });
    output(result);
}
export async function contextCommand(name, options) {
    if (!name?.trim() && !options?.uid) {
        console.error('Usage: gitnexus context <symbol_name> [--uid <uid>] [--file <path>]');
        process.exit(1);
    }
    const backend = await getBackend();
    const result = await backend.callTool('context', {
        name: name || undefined,
        uid: options?.uid,
        file_path: options?.file,
        include_content: options?.content ?? false,
        repo: options?.repo,
    });
    output(result);
}
export async function impactCommand(target, options) {
    if (!target?.trim()) {
        console.error('Usage: gitnexus impact <symbol_name> [--direction upstream|downstream]');
        process.exit(1);
    }
    const backend = await getBackend();
    const result = await backend.callTool('impact', {
        target,
        direction: options?.direction || 'upstream',
        maxDepth: options?.depth ? parseInt(options.depth) : undefined,
        includeTests: options?.includeTests ?? false,
        repo: options?.repo,
    });
    output(result);
}
export async function cypherCommand(query, options) {
    if (!query?.trim()) {
        console.error('Usage: gitnexus cypher <cypher_query>');
        process.exit(1);
    }
    const backend = await getBackend();
    const result = await backend.callTool('cypher', {
        query,
        repo: options?.repo,
    });
    output(result);
}
export async function detectChangesCommand(options) {
    const backend = await getBackend();
    const result = await backend.callTool('detect_changes', {
        scope: options?.scope,
        base_ref: options?.baseRef,
        repo: options?.repo,
    });
    output(result);
}
export async function renameCommand(options) {
    if (!options?.newName?.trim()) {
        console.error('Usage: meta-code-graph-base-core rename --new-name <name> [--symbol-name <name>|--symbol-uid <uid>]');
        process.exit(1);
    }
    const backend = await getBackend();
    const result = await backend.callTool('rename', {
        symbol_name: options?.symbolName,
        symbol_uid: options?.symbolUid,
        new_name: options.newName,
        file_path: options?.file,
        dry_run: !(options?.apply ?? false),
        repo: options?.repo,
    });
    output(result);
}
export async function resourceCommand(uri) {
    if (!uri?.trim()) {
        console.error('Usage: meta-code-graph-base-core resource <uri>');
        process.exit(1);
    }
    const backend = await getBackend();
    const result = await readResource(uri, backend);
    output(result);
}
