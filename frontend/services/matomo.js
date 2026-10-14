import { INTERNAL_HOSTS } from '../vue-guillotine/utils/linkUtils.js'
import { MATOMO_ENABLED } from './config'

const DEFAULT_TITLE =
  'Stop Dépôt Sauvage - Accompagner les collectivités pour mieux lutter contre les dépôts sauvages.'

// The site responds on multiple domains/aliases (stopdepotsauvage, protect-envi, etc.).
// Without this list, Matomo treats cross-domain clicks as outlinks.
const SITE_DOMAINS = Array.from(
  new Set(
    INTERNAL_HOSTS.filter((host) => !host.includes('localhost') && !host.includes('127.0.0.1')).map(
      (host) => `*.${host.replace(/^www\./, '')}`
    )
  )
)

// Heartbeat timer ensures time spent on the last page of a visit is accurately counted.
const HEARTBEAT_DELAY_SECONDS = 15

export function buildPageTitle(title) {
  return title ? `${title} - Stop Dépôt Sauvage` : DEFAULT_TITLE
}

function pushPageView(title, url) {
  if (!window._paq) {
    return
  }
  window._paq.push(['setCustomUrl', url])
  window._paq.push(['setDocumentTitle', title])
  window._paq.push(['trackPageView'])
}

/**
 * Tracks page view with custom title for routes with `meta.deferPageView`
 * (e.g. blog articles whose real titles are known only after fetching data).
 */
export function trackPageViewWithTitle(title) {
  const pageTitle = buildPageTitle(title)
  document.title = pageTitle
  pushPageView(pageTitle, window.location.origin + window.location.pathname)
}

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
  window._paq.push(['setDomains', SITE_DOMAINS])
  window._paq.push(['enableHeartBeatTimer', HEARTBEAT_DELAY_SECONDS])
  window._paq.push(['enableLinkTracking'])

  const script = document.createElement('script')
  script.async = true
  script.src = `${matomoHost.endsWith('/') ? matomoHost : matomoHost + '/'}matomo.js`
  script.onerror = () => console.error('[Matomo] Erreur lors du chargement du script')
  document.head.appendChild(script)

  router.afterEach((to) => {
    const title = buildPageTitle(to.meta.title)
    document.title = title
    // Routes with deferPageView manually trigger trackPageView once their content is loaded
    if (to.meta.deferPageView) {
      return
    }
    pushPageView(title, window.location.origin + to.fullPath)
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
