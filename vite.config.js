import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': '/frontend',
    },
  },
  server: {
    fs: {
      allow: [
        '.', // Project root and node_modules
        '../../.yarn', // loading fonts from yarn cache
      ],
    },
  },
  build: {
    assetsDir: 'static',
  },
})
