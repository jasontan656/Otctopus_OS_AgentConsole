/**
 * Clean Command
 *
 * Removes the Meta-code-graph-base index from the current repository.
 * Also unregisters it from the global registry.
 */
export declare const cleanCommand: (options?: {
    force?: boolean;
    all?: boolean;
}) => Promise<void>;
