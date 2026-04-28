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
    server: {
      allowedHosts: ['localhost', '.local', '.protect-envi.beta.gouv.fr'],
      fs: {
        allow: [
          '.', // Project root and node_modules
          '../../.yarn', // loading fonts from yarn cache
        ],
      },
      watch: {
        ignored: ['**/.venv/**', '**/backend/**', '**/django_cache/**', '**/static/**'],
      },
    },
    build: {
      assetsDir: 'static',
    },
    css: {
      lightningcss: {
        errorRecovery: true,
      },
    },
    test: {
      environment: 'jsdom',
      globals: true,
      setupFiles: './vitest.setup.ts',
      exclude: ['node_modules', 'dist', 'e2e'],
    },
  }
})
