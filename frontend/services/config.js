/**
 * Convert value string to boolean.
 */
export const getEnvBool = (key, defaultValue = false) => {
  const value = import.meta.env[key]
  if (value === undefined || value === null) return defaultValue
  if (typeof value === 'boolean') return value
  if (typeof value === 'string') {
    return value.toLowerCase() === 'true'
  }
  return !!value
}

export const LOGIN_REQUIRED = getEnvBool('VITE_LOGIN_REQUIRED', true)
export const PROCONNECT_ENABLED = getEnvBool('VITE_PROCONNECT_ENABLED', false)
export const MATOMO_ENABLED = getEnvBool('VITE_MATOMO_ENABLED', false)
export const CRISP_ENABLED = getEnvBool('VITE_CRISP_ENABLED', false)
export const LA_POSTE_SUIVI_BASE_URL =
  import.meta.env.VITE_LA_POSTE_SUIVI_URL || 'https://www.laposte.fr/outils/suivre-vos-envois'
export const SENTRY_ENABLED = getEnvBool('VITE_SENTRY_ENABLED', false)
export const SENTRY_DEBUG = getEnvBool('VITE_SENTRY_DEBUG', false)
export const SENTRY_DSN = import.meta.env.VITE_SENTRY_DSN || ''

