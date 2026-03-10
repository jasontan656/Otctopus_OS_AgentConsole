import path from 'node:path'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

const uiRoot = path.resolve(__dirname, 'ui')

export default defineConfig({
  root: uiRoot,
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 4178,
  },
  resolve: {
    alias: {
      '@': path.resolve(uiRoot, 'src'),
    },
  },
  build: {
    outDir: path.resolve(__dirname, 'dist/client'),
    emptyOutDir: true,
  },
})
