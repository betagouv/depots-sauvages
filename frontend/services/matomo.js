import { MATOMO_ENABLED } from './config'

export function initMatomo(router) {
  const matomoHost = import.meta.env.VITE_MATOMO_HOST
  const matomoSiteId = parseInt(import.meta.env.VITE_MATOMO_SITE_ID)

  if (!MATOMO_ENABLED || !matomoHost || !matomoSiteId) {
    return
  }

  window._paq = window._paq || []
  window._paq.push([
    'setTrackerUrl',
    `${matomoHost.endsWith('/') ? matomoHost : matomoHost + '/'}matomo.php`,
  ])
  window._paq.push(['setSiteId', matomoSiteId])
  window._paq.push(['disableCookies'])
  window._paq.push(['trackPageView'])
  window._paq.push(['enableLinkTracking'])

  const script = document.createElement('script')
  script.async = true
  script.src = `${matomoHost.endsWith('/') ? matomoHost : matomoHost + '/'}matomo.js`
  script.onerror = () => console.error('[Matomo] Erreur lors du chargement du script')
  document.head.appendChild(script)

  router.afterEach((to) => {
    window._paq.push(['setCustomUrl', window.location.origin + to.fullPath])
    window._paq.push(['setDocumentTitle', to.meta.title || document.title])
    window._paq.push(['trackPageView'])
  })
}
