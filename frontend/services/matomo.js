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
  window._paq.push(['enableLinkTracking'])
  // Ping every 15s so time spent on the last page of a visit is measured too,
  // which matters for content pages people read and then leave.
  window._paq.push(['enableHeartBeatTimer', 15])

  const script = document.createElement('script')
  script.async = true
  script.src = `${matomoHost.endsWith('/') ? matomoHost : matomoHost + '/'}matomo.js`
  script.onerror = () => console.error('[Matomo] Erreur lors du chargement du script')
  document.head.appendChild(script)

  router.afterEach((to) => {
    const title = to.meta.title
      ? `${to.meta.title} - Protect'Envi`
      : 'Protect’Envi - Accompagner les collectivités pour mieux lutter contre les dépôts sauvages.'
    document.title = title
    window._paq.push(['setCustomUrl', window.location.origin + to.fullPath])
    window._paq.push(['setDocumentTitle', title])
    window._paq.push(['trackPageView'])
  })
}

export function trackDownload(url) {
  if (window._paq) {
    window._paq.push(['trackLink', url, 'download'])
  }
}

export function trackEvent(category, action, name, value) {
  if (window._paq) {
    const args = ['trackEvent', category, action]
    if (name !== undefined) {
      args.push(name)
    }
    if (value !== undefined && typeof value === 'number') {
      args.push(value)
    }
    window._paq.push(args)
  }
}

export function trackAndOpenLink(category, action, url) {
  if (url) {
    trackEvent(category, action, url)
    window.open(url, '_blank', 'noopener,noreferrer')
  }
}

