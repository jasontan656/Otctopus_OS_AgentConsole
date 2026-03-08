import { KnowledgeGraph } from '../graph/types.js';
import { SymbolTable } from './symbol-table.js';
import { ASTCache } from './ast-cache.js';
import { WorkerPool } from './workers/worker-pool.js';
import type { ExtractedImport, ExtractedCall, ExtractedHeritage, ExtractedRoute } from './workers/parse-worker.js';
export type FileProgressCallback = (current: number, total: number, filePath: string) => void;
export interface WorkerExtractedData {
    imports: ExtractedImport[];
    calls: ExtractedCall[];
    heritage: ExtractedHeritage[];
    routes: ExtractedRoute[];
}
/**
 * Check if a symbol (function, class, etc.) is exported/public
 * Handles all 9 supported languages with explicit logic
 *
 * @param node - The AST node for the symbol name
 * @param name - The symbol name
 * @param language - The programming language
 * @returns true if the symbol is exported/public
 */
export declare const isNodeExported: (node: any, name: string, language: string) => boolean;
export declare const processParsing: (graph: KnowledgeGraph, files: {
    path: string;
    content: string;
}[], symbolTable: SymbolTable, astCache: ASTCache, onFileProgress?: FileProgressCallback, workerPool?: WorkerPool) => Promise<WorkerExtractedData | null>;
