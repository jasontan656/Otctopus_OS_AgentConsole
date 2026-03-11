import path from 'node:path'
import { promises as fs } from 'node:fs'
import http from 'node:http'
import express from 'express'
import chokidar from 'chokidar'
import WebSocket, { WebSocketServer } from 'ws'
import type { IncomingMessage } from 'node:http'
import type { PreviewPayload } from '../lib/viewer-types.js'
import { buildViewerPayload } from '../lib/viewer-payload.js'
import { defaultSkillRoot } from '../../src/lib/docstructure.js'

const SKILL_ROOT = defaultSkillRoot()
const UI_DEV_ROOT = path.resolve(SKILL_ROOT, 'ui-dev')
const UI_ROOT = path.resolve(UI_DEV_ROOT, 'client')
const DIST_ROOT = path.resolve(UI_DEV_ROOT, 'dist/client')
const PORT = Number(process.env.PORT ?? '4178')
const HOST = process.env.HOST ?? '0.0.0.0'
const TARGET_SKILL_ROOT = path.resolve(process.env.TARGET_SKILL_ROOT ?? SKILL_ROOT)
const WS_PATH = '/live'
const isProduction = process.env.NODE_ENV === 'production'

let payloadCache: PreviewPayload | null = null
let errorCache: { status: 'error'; error: string } | null = null
let refreshTimer: NodeJS.Timeout | null = null

function shouldWatch(filePath: string): boolean {
  return !filePath.includes(`${path.sep}node_modules${path.sep}`)
    && !filePath.includes(`${path.sep}.git${path.sep}`)
    && !filePath.includes(`${path.sep}dist${path.sep}`)
}

async function loadPayload(): Promise<PreviewPayload> {
  const payload = await buildViewerPayload(TARGET_SKILL_ROOT)
  payloadCache = payload
  errorCache = null

  return payload
}

function scheduleRefresh(callback: () => void): void {
  if (refreshTimer) {
    clearTimeout(refreshTimer)
  }
  refreshTimer = setTimeout(callback, 120)
}

async function createApplication() {
  const app = express()
  const server = http.createServer(app)
  const webSocketServer = new WebSocketServer({ server, path: WS_PATH })

  async function broadcast(type: 'payload' | 'error'): Promise<void> {
    if (type === 'payload' && payloadCache) {
      const message = JSON.stringify({ type: 'payload', payload: payloadCache })
      for (const client of webSocketServer.clients) {
        if (client.readyState === WebSocket.OPEN) {
          client.send(message)
        }
      }
    }
    if (type === 'error' && errorCache) {
      const message = JSON.stringify(errorCache)
      for (const client of webSocketServer.clients) {
        if (client.readyState === WebSocket.OPEN) {
          client.send(message)
        }
      }
    }
  }

  app.get('/api/health', (_req, res) => {
    res.json({
      status: errorCache ? 'degraded' : 'ok',
      targetSkillRoot: TARGET_SKILL_ROOT,
      wsPath: WS_PATH,
      updatedAt: payloadCache?.updatedAt ?? null,
    })
  })

  app.get('/api/preview', async (_req, res) => {
    try {
      if (!payloadCache) {
        await loadPayload()
      }
      res.json(payloadCache)
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error)
      errorCache = { status: 'error', error: message }
      res.status(500).json(errorCache)
    }
  })

  const watcher = chokidar.watch(TARGET_SKILL_ROOT, {
    ignoreInitial: true,
    awaitWriteFinish: {
      stabilityThreshold: 160,
      pollInterval: 40,
    },
  })

  watcher.on('all', (_eventName, filePath) => {
    if (!shouldWatch(filePath)) {
      return
    }
    scheduleRefresh(async () => {
      try {
        await loadPayload()
        await broadcast('payload')
      } catch (error) {
        const message = error instanceof Error ? error.message : String(error)
        errorCache = { status: 'error', error: message }
        await broadcast('error')
      }
    })
  })

  if (!isProduction) {
    const { createServer: createViteServer } = await import('vite')
    const vite = await createViteServer({
      root: UI_ROOT,
      server: { middlewareMode: true },
      appType: 'custom',
      configFile: path.resolve(UI_DEV_ROOT, 'vite.config.ts'),
    })

    app.use(vite.middlewares)

    app.use(async (req, res) => {
      try {
        const template = await fs.readFile(path.resolve(UI_ROOT, 'index.html'), 'utf8')
        const html = await vite.transformIndexHtml(req.originalUrl, template)
        res.status(200).setHeader('Content-Type', 'text/html').end(html)
      } catch (error) {
        const message = error instanceof Error ? error.stack ?? error.message : String(error)
        res.status(500).end(message)
      }
    })
  } else {
    app.use('/assets', express.static(path.join(DIST_ROOT, 'assets')))
    app.use(express.static(DIST_ROOT))
    app.use(async (_req, res) => {
      const html = await fs.readFile(path.join(DIST_ROOT, 'index.html'), 'utf8')
      res.status(200).setHeader('Content-Type', 'text/html').end(html)
    })
  }

  webSocketServer.on('connection', async (socket, request: IncomingMessage) => {
    if (request.url !== WS_PATH) {
      socket.close()
      return
    }
    try {
      if (!payloadCache) {
        await loadPayload()
      }
      socket.send(JSON.stringify({ type: 'payload', payload: payloadCache }))
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error)
      socket.send(JSON.stringify({ type: 'error', error: message }))
    }
  })

  await loadPayload()

  server.listen(PORT, HOST, () => {
    process.stdout.write(`[viewer] http://${HOST}:${PORT}\n`)
  })
}

createApplication().catch((error) => {
  process.stderr.write(`${error instanceof Error ? error.stack ?? error.message : String(error)}\n`)
  process.exit(1)
})
