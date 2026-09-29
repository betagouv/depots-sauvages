import { trackPageView } from './matomo'

const SITE_NAME = 'Stop Dépôt Sauvage'
const DEFAULT_TITLE = `${SITE_NAME} - Accompagner les collectivités pour mieux lutter contre les dépôts sauvages.`

export const formatPageTitle = (title) => (title ? `${title} - ${SITE_NAME}` : DEFAULT_TITLE)

export function setPageTitle(title, path = window.location.pathname + window.location.search) {
  document.title = formatPageTitle(title)
  trackPageView(document.title, path)
}

export function initPageTitles(router) {
  router.afterEach((to) => {
    if (to.meta.dynamicTitle && to.params.slug) return
    setPageTitle(to.meta.title, to.fullPath)
  })
}
