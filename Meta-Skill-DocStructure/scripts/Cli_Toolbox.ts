#!/usr/bin/env node
import process from 'node:process'
import {
  buildDocGraphWorkspace,
  defaultSkillRoot,
  loadRuntimeContract,
  rebuildSelfGraph,
} from '../src/lib/docstructure.js'

function printJson(payload: unknown): void {
  process.stdout.write(`${JSON.stringify(payload, null, 2)}\n`)
}

function readFlag(args: string[], name: string): string | undefined {
  const index = args.indexOf(name)
  if (index === -1) {
    return undefined
  }
  return args[index + 1]
}

function hasFlag(args: string[], name: string): boolean {
  return args.includes(name)
}

function usage(): never {
  console.error([
    'Usage:',
    '  npm run cli -- runtime-contract --json',
    '  npm run cli -- lint-doc-anchors --target <skill_root> --json',
    '  npm run cli -- build-anchor-graph --target <skill_root> --json',
    '  npm run cli -- rebuild-self-graph --json',
  ].join('\n'))
  process.exit(2)
}

async function main(): Promise<void> {
  const [command, ...rest] = process.argv.slice(2)
  if (!command) {
    usage()
  }

  const wantsJson = hasFlag(rest, '--json')
  const target = readFlag(rest, '--target') ?? defaultSkillRoot()

  try {
    if (command === 'runtime-contract') {
      const payload = await loadRuntimeContract(target)
      printJson(payload)
      return
    }

    if (command === 'build-anchor-graph') {
      const payload = await buildDocGraphWorkspace(target)
      printJson({
        status: payload.status,
        targetRoot: payload.targetRoot,
        summary: payload.summary,
        graph: payload.graph,
        warnings: payload.warnings,
        errors: payload.errors,
      })
      process.exit(payload.status === 'fail' ? 1 : 0)
    }

    if (command === 'lint-doc-anchors') {
      const payload = await buildDocGraphWorkspace(target)
      printJson({
        status: payload.status,
        targetRoot: payload.targetRoot,
        summary: payload.summary,
        warnings: payload.warnings,
        errors: payload.errors,
      })
      process.exit(payload.status === 'fail' ? 1 : 0)
    }

    if (command === 'rebuild-self-graph') {
      const { graphPath, workspace } = await rebuildSelfGraph(target)
      printJson({
        status: workspace.status === 'fail' ? 'error' : 'written',
        graphPath,
        summary: workspace.summary,
        warnings: workspace.warnings,
        errors: workspace.errors,
      })
      process.exit(workspace.status === 'fail' ? 1 : 0)
    }

    usage()
  } catch (error) {
    const payload = {
      status: 'error',
      error: error instanceof Error ? error.message : String(error),
    }
    if (wantsJson) {
      printJson(payload)
    } else {
      console.error(payload.error)
    }
    process.exit(2)
  }
}

main()
