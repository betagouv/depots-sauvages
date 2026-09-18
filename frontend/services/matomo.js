import { MATOMO_ENABLED } from './config'

const DEFAULT_TITLE =
  'Stop Dépôt Sauvage - Accompagner les collectivités pour mieux lutter contre les dépôts sauvages.'

// Le site répond sur deux domaines (stopdepotsauvage redirige vers protect-envi).
// Sans cette liste, Matomo compte les liens d'un domaine vers l'autre comme des
// sorties du site : le parcours « article -> constatation » devient illisible.
const SITE_DOMAINS = ['*.protect-envi.beta.gouv.fr', '*.stopdepotsauvage.beta.gouv.fr']

// Sans battement de cœur, le temps passé sur la dernière page d'une visite est
// compté comme nul, ce qui fausse la lecture de l'engagement sur les articles.
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
 * Enregistre la vue de page avec un titre connu seulement après chargement des
 * données (article de blog par exemple), pour les routes marquées
 * `meta.deferPageView`.
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
    // Les pages dont le titre dépend d'un contenu chargé à l'affichage
    // déclarent leur vue de page elles-mêmes, une fois le titre réel connu.
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
