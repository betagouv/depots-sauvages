import vue from '@vitejs/plugin-vue'
import path from 'path'
import { defineConfig, loadEnv } from 'vite'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  return {
    plugins: [vue()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'frontend'),
      },
    },
    define: {
      'import.meta.env.VITE_PROCONNECT_ENABLED': JSON.stringify(env.PROCONNECT_ENABLED),
    },
    server: {
      allowedHosts: ['localhost', '.local', '.protect-envi.beta.gouv.fr'],
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
    test: {
      environment: 'jsdom',
      globals: true,
      setupFiles: './vitest.setup.ts',
    },
  }
})
