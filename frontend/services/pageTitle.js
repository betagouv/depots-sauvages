const SITE_NAME = 'Stop Dépôt Sauvage'
const DEFAULT_TITLE = `${SITE_NAME} - Accompagner les collectivités pour mieux lutter contre les dépôts sauvages.`

export function buildPageTitle(title) {
  return title ? `${title} - ${SITE_NAME}` : DEFAULT_TITLE
}

export function setPageTitle(title) {
  const fullTitle = buildPageTitle(title)
  document.title = fullTitle
  return fullTitle
}

/**
 * Pages whose title depends on loaded content (blog article, FAQ question)
 * set the title and send the page view themselves.
 */
export function hasContentTitle(route) {
  return route.name === 'BlogArticle' || (route.name === 'FAQ' && !!route.params.slug)
}

export function initPageTitle(router) {
  router.afterEach((to) => {
    if (!hasContentTitle(to)) {
      setPageTitle(to.meta.title)
    }
  })
}
