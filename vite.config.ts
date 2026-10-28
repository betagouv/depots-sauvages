import vue from '@vitejs/plugin-vue'
import path from 'path'
import { defineConfig, loadEnv } from 'vite'

function getSharedEnv(key: string, env: Record<string, string>, defaultValue = '') {
  return JSON.stringify(
    process.env[key] || env[key] || process.env[`VITE_${key}`] || env[`VITE_${key}`] || defaultValue
  )
}

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
      global: 'window',
      'import.meta.env.VITE_ENV_NAME': getSharedEnv('ENV_NAME', env),
      'import.meta.env.VITE_SENTRY_DSN': getSharedEnv('SENTRY_DSN', env),
      'import.meta.env.VITE_SENTRY_ENABLED': getSharedEnv('SENTRY_ENABLED', env, 'false'),
      'import.meta.env.VITE_SENTRY_TRACES_SAMPLE_RATE': getSharedEnv(
        'SENTRY_TRACES_SAMPLE_RATE',
        env,
        '0.1'
      ),
      'import.meta.env.VITE_LOGIN_REQUIRED': getSharedEnv('LOGIN_REQUIRED', env, 'true'),
      'import.meta.env.VITE_PROCONNECT_ENABLED': getSharedEnv('PROCONNECT_ENABLED', env, 'false'),
    },
    server: {
      allowedHosts: [
        'localhost',
        '.local',
        '.protect-envi.beta.gouv.fr',
        '.stopdepotsauvage.beta.gouv.fr',
        '.stop-depot-sauvage.beta.gouv.fr',
      ],
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
      exclude: ['node_modules', 'dist', 'e2e', '.dev', '.kilo'],
    },
  }
})
