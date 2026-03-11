#!/usr/bin/env node
// Heap re-spawn removed — only analyze.ts needs the 8GB heap (via its own ensureHeap()).
// Removing it from here improves MCP server startup time significantly.
import { Command } from 'commander';
import { analyzeCommand } from './analyze.js';
import { listCommand } from './list.js';
import { statusCommand } from './status.js';
import { cleanCommand } from './clean.js';
import { augmentCommand } from './augment.js';
import { queryCommand, contextCommand, impactCommand, cypherCommand, detectChangesCommand, renameCommand, resourceCommand } from './tool.js';
import { createRequire } from 'node:module';
const _require = createRequire(import.meta.url);
const pkg = _require('../../package.json');
const program = new Command();
program
    .name('meta-code-graph-base-core')
    .description('Meta-code-graph-base local code-graph CLI')
    .version(pkg.version);
program
    .command('analyze [path]')
    .description('Index a repository (full analysis)')
    .option('-f, --force', 'Force full re-index even if up to date')
    .option('--embeddings', 'Enable embedding generation for semantic search (off by default)')
    .action(analyzeCommand);
program
    .command('list')
    .description('List all indexed repositories')
    .action(listCommand);
program
    .command('status')
    .description('Show index status for current repo')
    .action(statusCommand);
program
    .command('clean')
    .description('Delete Meta-code-graph-base index for current repo')
    .option('-f, --force', 'Skip confirmation prompt')
    .option('--all', 'Clean all indexed repos')
    .action(cleanCommand);
program
    .command('augment <pattern>')
    .description('Augment a search pattern with knowledge graph context (used by hooks)')
    .action(augmentCommand);
// ─── Direct Tool Commands (no MCP overhead) ────────────────────────
// These invoke LocalBackend directly for use in eval, scripts, and CI.
program
    .command('query <search_query>')
    .description('Search the knowledge graph for execution flows related to a concept')
    .option('-r, --repo <name>', 'Target repository (omit if only one indexed)')
    .option('-c, --context <text>', 'Task context to improve ranking')
    .option('-g, --goal <text>', 'What you want to find')
    .option('-l, --limit <n>', 'Max processes to return (default: 5)')
    .option('--content', 'Include full symbol source code')
    .action(queryCommand);
program
    .command('context [name]')
    .description('360-degree view of a code symbol: callers, callees, processes')
    .option('-r, --repo <name>', 'Target repository')
    .option('-u, --uid <uid>', 'Direct symbol UID (zero-ambiguity lookup)')
    .option('-f, --file <path>', 'File path to disambiguate common names')
    .option('--content', 'Include full symbol source code')
    .action(contextCommand);
program
    .command('impact <target>')
    .description('Blast radius analysis: what breaks if you change a symbol')
    .option('-d, --direction <dir>', 'upstream (dependants) or downstream (dependencies)', 'upstream')
    .option('-r, --repo <name>', 'Target repository')
    .option('--depth <n>', 'Max relationship depth (default: 3)')
    .option('--include-tests', 'Include test files in results')
    .action(impactCommand);
program
    .command('cypher <query>')
    .description('Execute raw Cypher query against the knowledge graph')
    .option('-r, --repo <name>', 'Target repository')
    .action(cypherCommand);
program
    .command('detect-changes')
    .description('Analyze git changes and find affected execution flows')
    .option('-s, --scope <scope>', 'unstaged | staged | all | compare', 'unstaged')
    .option('-b, --base-ref <ref>', 'Base ref for compare scope')
    .option('-r, --repo <name>', 'Target repository')
    .action(detectChangesCommand);
program
    .command('rename')
    .description('Multi-file coordinated rename using graph + text search')
    .option('-n, --symbol-name <name>', 'Current symbol name')
    .option('-u, --symbol-uid <uid>', 'Direct symbol UID')
    .option('-m, --new-name <name>', 'Replacement symbol name')
    .option('-f, --file <path>', 'File path to disambiguate common names')
    .option('--apply', 'Apply edits instead of dry-run preview')
    .option('-r, --repo <name>', 'Target repository')
    .action(renameCommand);
program
    .command('resource <uri>')
    .description('Read a structured resource view from the local code graph')
    .action(resourceCommand);
program.parse(process.argv);
