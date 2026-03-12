#!/usr/bin/env node
import { promises as fs } from 'node:fs'
import path from 'node:path'
import process from 'node:process'
import {
  buildDocGraphWorkspace,
  defaultSkillRoot,
  rebuildSelfGraph,
} from '../src/lib/docstructure.js'
import {
  lintUiIdentity,
  lintUiPackageShape,
  loadUiIdentityContract,
  loadUiPackageContract,
} from '../src/lib/ui-identity.js'
import {
  RUNTIME_CONTRACT,
  getStageDefinition,
} from '../src/lib/stage-contracts.js'

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

function usage(): never {
  console.error([
    'Usage:',
    '  npm run cli -- runtime-contract --json',
    '  npm run cli -- stage-checklist --stage <stage> --json',
    '  npm run cli -- stage-doc-contract --stage <stage> --json',
    '  npm run cli -- stage-command-contract --stage <stage> --json',
    '  npm run cli -- stage-graph-contract --stage <stage> --json',
    '  npm run cli -- ui-identity-contract --json',
    '  npm run cli -- lint-ui-identity --json',
    '  npm run cli -- ui-package-contract --json',
    '  npm run cli -- lint-ui-package-shape --json',
    '  npm run cli -- build-anchor-graph --target <skill_root> --json',
    '  npm run cli -- rebuild-self-graph --json',
  ].join('\n'))
  process.exit(2)
}

async function readRuntimeMarkdown(): Promise<string> {
  const runtimeMarkdown = path.join(defaultSkillRoot(), 'references', 'runtime', 'SKILL_RUNTIME_CONTRACT.md')
  return fs.readFile(runtimeMarkdown, 'utf8')
}

async function main(): Promise<void> {
  const [command, ...rest] = process.argv.slice(2)
  if (!command) {
    usage()
  }

  const target = readFlag(rest, '--target') ?? defaultSkillRoot()
  const stage = readFlag(rest, '--stage')

  try {
    if (command === 'runtime-contract') {
      printJson({
        ...RUNTIME_CONTRACT,
        runtime_markdown_path: 'references/runtime/SKILL_RUNTIME_CONTRACT.md',
        runtime_markdown_preview: (await readRuntimeMarkdown()).split('\n').slice(0, 12).join('\n'),
      })
      return
    }

    if (command === 'stage-checklist') {
      if (!stage) usage()
      printJson(getStageDefinition(stage).checklist)
      return
    }

    if (command === 'stage-doc-contract') {
      if (!stage) usage()
      printJson(getStageDefinition(stage).docContract)
      return
    }

    if (command === 'stage-command-contract') {
      if (!stage) usage()
      printJson(getStageDefinition(stage).commandContract)
      return
    }

    if (command === 'stage-graph-contract') {
      if (!stage) usage()
      printJson(getStageDefinition(stage).graphContract)
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

    if (command === 'ui-identity-contract') {
      printJson(await loadUiIdentityContract(target))
      return
    }

    if (command === 'lint-ui-identity') {
      const payload = await lintUiIdentity(target)
      printJson(payload)
      process.exit(payload.status === 'fail' ? 1 : 0)
    }

    if (command === 'ui-package-contract') {
      printJson(await loadUiPackageContract(target))
      return
    }

    if (command === 'lint-ui-package-shape') {
      const payload = await lintUiPackageShape(target)
      printJson(payload)
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
    printJson({
      status: 'error',
      error: error instanceof Error ? error.message : String(error),
    })
    process.exit(2)
  }
}

main()
