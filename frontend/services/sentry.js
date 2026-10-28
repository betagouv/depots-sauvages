import * as Sentry from '@sentry/vue'
import { SENTRY_DEBUG, SENTRY_DSN, SENTRY_ENABLED } from './config'

export function initSentry(app, router) {
  if (!SENTRY_ENABLED || !SENTRY_DSN) {
    return
  }
  const environment = import.meta.env.VITE_ENV_NAME || import.meta.env.MODE || 'development'
  const release =
    import.meta.env.VITE_SENTRY_RELEASE || import.meta.env.VITE_SOURCE_VERSION || undefined
  const tracesSampleRate = parseFloat(import.meta.env.VITE_SENTRY_TRACES_SAMPLE_RATE || '0.1')
  Sentry.init({
    app,
    dsn: SENTRY_DSN,
    environment,
    release,
    integrations: [Sentry.browserTracingIntegration({ router })],
    tracesSampleRate,
    ignoreErrors: [
      'ResizeObserver loop completed with undelivered notifications',
      'ResizeObserver loop limit exceeded',
      'Non-Error promise rejection captured',
    ],
    beforeSend(event) {
      if (event.request?.headers) {
        delete event.request.headers['Authorization']
        delete event.request.headers['cookie']
      }
      return event
    },
  })
  if (SENTRY_DEBUG && typeof window !== 'undefined') {
    window.Sentry = Sentry
    window.triggerSentryTestError = () => {
      const testError = new Error('Test Sentry frontend manuel')
      Sentry.captureException(testError)
      console.info('Test error sent to Sentry:', testError)
      return testError
    }
  }
}
