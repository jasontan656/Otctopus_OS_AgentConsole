/**
 * Repository Manager
 *
 * Manages GitNexus index storage in .gitnexus/ at repo root.
 * Also maintains a global registry at ~/.gitnexus/registry.json
 * so the MCP server can discover indexed repos from any cwd.
 */
import fs from 'fs/promises';
import path from 'path';
import crypto from 'crypto';
function resolveRuntimeRoot() {
    const explicit = process.env.META_CODE_GRAPH_RUNTIME_ROOT;
    if (explicit && explicit.trim()) {
        return path.resolve(explicit);
    }
    throw new Error('Meta-code-graph-base: runtime root is required. Set META_CODE_GRAPH_RUNTIME_ROOT or use the Python wrapper with --runtime-root.');
}
const RUNTIME_ROOT = resolveRuntimeRoot();
const INDEXES_DIR = 'indexes';
const REGISTRY_DIR = 'registry';
const CONFIG_DIR = 'config';
function getRepoKey(repoPath) {
    const resolved = path.resolve(repoPath);
    const base = path.basename(resolved).replace(/[^a-zA-Z0-9._-]+/g, '_') || 'repo';
    const hash = crypto.createHash('sha1').update(resolved).digest('hex').slice(0, 12);
    return `${base}-${hash}`;
}
// ─── Local Storage Helpers ─────────────────────────────────────────────
/**
 * Get the centralized runtime storage path for a repository
 */
export const getStoragePath = (repoPath) => {
    return path.join(RUNTIME_ROOT, INDEXES_DIR, getRepoKey(repoPath));
};
/**
 * Get paths to key storage files
 */
export const getStoragePaths = (repoPath) => {
    const storagePath = getStoragePath(repoPath);
    return {
        storagePath,
        kuzuPath: path.join(storagePath, 'kuzu'),
        metaPath: path.join(storagePath, 'meta.json'),
    };
};
/**
 * Load metadata from an indexed repo
 */
export const loadMeta = async (storagePath) => {
    try {
        const metaPath = path.join(storagePath, 'meta.json');
        const raw = await fs.readFile(metaPath, 'utf-8');
        return JSON.parse(raw);
    }
    catch {
        return null;
    }
};
/**
 * Save metadata to storage
 */
export const saveMeta = async (storagePath, meta) => {
    await fs.mkdir(storagePath, { recursive: true });
    const metaPath = path.join(storagePath, 'meta.json');
    await fs.writeFile(metaPath, JSON.stringify(meta, null, 2), 'utf-8');
};
/**
 * Check if a path has a GitNexus index
 */
export const hasIndex = async (repoPath) => {
    const { metaPath } = getStoragePaths(repoPath);
    try {
        await fs.access(metaPath);
        return true;
    }
    catch {
        return false;
    }
};
/**
 * Load an indexed repo from a path
 */
export const loadRepo = async (repoPath) => {
    const paths = getStoragePaths(repoPath);
    const meta = await loadMeta(paths.storagePath);
    if (!meta)
        return null;
    return {
        repoPath: path.resolve(repoPath),
        ...paths,
        meta,
    };
};
/**
 * Find the indexed repo whose path contains the starting path.
 */
export const findRepo = async (startPath) => {
    const entries = await listRegisteredRepos({ validate: true });
    const resolved = path.resolve(startPath);
    const isWindows = process.platform === 'win32';
    const normalizedStart = isWindows ? resolved.toLowerCase() : resolved;
    let best = null;
    for (const entry of entries) {
        const entryPath = path.resolve(entry.path);
        const normalizedEntry = isWindows ? entryPath.toLowerCase() : entryPath;
        if (normalizedStart === normalizedEntry ||
            normalizedStart.startsWith(`${normalizedEntry}${path.sep}`)) {
            if (!best || normalizedEntry.length > path.resolve(best.path).length) {
                best = entry;
            }
        }
    }
    if (!best)
        return null;
    const paths = getStoragePaths(best.path);
    const meta = await loadMeta(paths.storagePath);
    if (!meta)
        return null;
    return {
        repoPath: path.resolve(best.path),
        ...paths,
        meta,
    };
};
// ─── Runtime Registry (code_graph_runtime/registry/registry.json) ──────
/**
 * Get the runtime root directory
 */
export const getGlobalDir = () => {
    return RUNTIME_ROOT;
};
/**
 * Get the path to the registry directory
 */
export const getRegistryDir = () => {
    return path.join(getGlobalDir(), REGISTRY_DIR);
};
/**
 * Get the path to the global registry file
 */
export const getGlobalRegistryPath = () => {
    return path.join(getRegistryDir(), 'registry.json');
};
/**
 * Read the global registry. Returns empty array if not found.
 */
export const readRegistry = async () => {
    try {
        const raw = await fs.readFile(getGlobalRegistryPath(), 'utf-8');
        const data = JSON.parse(raw);
        return Array.isArray(data) ? data : [];
    }
    catch {
        return [];
    }
};
/**
 * Write the global registry to disk
 */
const writeRegistry = async (entries) => {
    const dir = getRegistryDir();
    await fs.mkdir(dir, { recursive: true });
    await fs.writeFile(getGlobalRegistryPath(), JSON.stringify(entries, null, 2), 'utf-8');
};
/**
 * Register (add or update) a repo in the global registry.
 * Called after `gitnexus analyze` completes.
 */
export const registerRepo = async (repoPath, meta) => {
    const resolved = path.resolve(repoPath);
    const name = path.basename(resolved);
    const { storagePath } = getStoragePaths(resolved);
    const entries = await readRegistry();
    const existing = entries.findIndex((e) => {
        const a = path.resolve(e.path);
        const b = resolved;
        return process.platform === 'win32'
            ? a.toLowerCase() === b.toLowerCase()
            : a === b;
    });
    const entry = {
        name,
        path: resolved,
        storagePath,
        indexedAt: meta.indexedAt,
        lastCommit: meta.lastCommit,
        stats: meta.stats,
    };
    if (existing >= 0) {
        entries[existing] = entry;
    }
    else {
        entries.push(entry);
    }
    await writeRegistry(entries);
};
/**
 * Remove a repo from the global registry.
 * Called after `gitnexus clean`.
 */
export const unregisterRepo = async (repoPath) => {
    const resolved = path.resolve(repoPath);
    const entries = await readRegistry();
    const filtered = entries.filter((e) => path.resolve(e.path) !== resolved);
    await writeRegistry(filtered);
};
/**
 * List all registered repos from the global registry.
 * Optionally validates that each entry's .gitnexus/ still exists.
 */
export const listRegisteredRepos = async (opts) => {
    const entries = await readRegistry();
    if (!opts?.validate)
        return entries;
    // Validate each entry still has a .gitnexus/ directory
    const valid = [];
    for (const entry of entries) {
        try {
            await fs.access(path.join(entry.storagePath, 'meta.json'));
            valid.push(entry);
        }
        catch {
            // Index no longer exists — skip
        }
    }
    // If we pruned any entries, save the cleaned registry
    if (valid.length !== entries.length) {
        await writeRegistry(valid);
    }
    return valid;
};
export const getRuntimeRoot = () => RUNTIME_ROOT;
export const getRuntimeArtifactPath = (kind, repoPath) => {
    if (!repoPath) {
        return path.join(RUNTIME_ROOT, kind);
    }
    return path.join(RUNTIME_ROOT, kind, getRepoKey(repoPath));
};
/**
 * Get the path to the global CLI config file
 */
export const getGlobalConfigPath = () => {
    return path.join(getGlobalDir(), CONFIG_DIR, 'config.json');
};
/**
 * Load CLI config from ~/.gitnexus/config.json
 */
export const loadCLIConfig = async () => {
    try {
        const raw = await fs.readFile(getGlobalConfigPath(), 'utf-8');
        return JSON.parse(raw);
    }
    catch {
        return {};
    }
};
/**
 * Save CLI config to ~/.gitnexus/config.json
 */
export const saveCLIConfig = async (config) => {
    const dir = path.dirname(getGlobalConfigPath());
    await fs.mkdir(dir, { recursive: true });
    const configPath = getGlobalConfigPath();
    await fs.writeFile(configPath, JSON.stringify(config, null, 2), 'utf-8');
    // Restrict file permissions on Unix (config may contain API keys)
    if (process.platform !== 'win32') {
        try {
            await fs.chmod(configPath, 0o600);
        }
        catch { /* best-effort */ }
    }
};
