import path from 'node:path'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

const clientRoot = path.resolve(__dirname, 'client')

export default defineConfig({
  root: clientRoot,
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 4178,
  },
  resolve: {
    alias: {
      '@': path.resolve(clientRoot, 'src'),
    },
  },
  build: {
    outDir: path.resolve(__dirname, 'dist/client'),
    emptyOutDir: true,
  },
})
