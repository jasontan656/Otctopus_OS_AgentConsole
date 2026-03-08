import { SupportedLanguages } from '../../config/supported-languages.js';
/**
 * Yield control to the event loop so spinners/progress can render.
 * Call periodically in hot loops to prevent UI freezes.
 */
export declare const yieldToEventLoop: () => Promise<void>;
/**
 * Find a child of `childType` within a sibling node of `siblingType`.
 * Used for Kotlin AST traversal where visibility_modifier lives inside a modifiers sibling.
 */
export declare const findSiblingChild: (parent: any, siblingType: string, childType: string) => any | null;
/**
 * Map file extension to SupportedLanguage enum
 */
export declare const getLanguageFromFilename: (filename: string) => SupportedLanguages | null;
