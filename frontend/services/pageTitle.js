import { trackPageView } from './matomo'

const SITE_NAME = 'Stop Dépôt Sauvage'
const DEFAULT_TITLE = `${SITE_NAME} - Accompagner les collectivités pour mieux lutter contre les dépôts sauvages.`

export const formatPageTitle = (title) => (title ? `${title} - ${SITE_NAME}` : DEFAULT_TITLE)

/**
 * Met à jour le titre de l'onglet et enregistre la page vue dans Matomo.
 */
export function setPageTitle(title, path = window.location.pathname + window.location.search) {
  document.title = formatPageTitle(title)
  trackPageView(document.title, path)
}

export function initPageTitles(router) {
  router.afterEach((to) => {
    // Article ou question FAQ : la page fixe elle-même son titre une fois le contenu connu
    if (to.meta.dynamicTitle && to.params.slug) return
    setPageTitle(to.meta.title, to.fullPath)
  })
}
