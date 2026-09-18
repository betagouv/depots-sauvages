/**
 * Normalisation des liens saisis dans les contenus éditoriaux (articles, FAQ).
 *
 * L'éditeur de texte pose par défaut `target="_blank"` et
 * `rel="noopener noreferrer nofollow"` sur tous les liens, y compris ceux qui
 * pointent vers le site lui-même. Trois conséquences : le lecteur perd le
 * bouton « retour », les moteurs de recherche ne suivent pas notre propre
 * maillage interne, et la mesure d'audience compte ces clics comme des sorties
 * du site. On rétablit ici le comportement attendu à l'affichage, ce qui
 * couvre aussi les contenus déjà enregistrés.
 */

// Le site répond sur deux domaines : stopdepotsauvage redirige vers protect-envi.
const SITE_HOSTS = ['protect-envi.beta.gouv.fr', 'stopdepotsauvage.beta.gouv.fr']

export const INTERNAL_LINK_ATTRIBUTE = 'data-internal-link'
export const NEW_WINDOW_MENTION = 'nouvelle fenêtre'

function isSiteHost(hostname: string): boolean {
  return SITE_HOSTS.some((host) => hostname === host || hostname.endsWith(`.${host}`))
}

/**
 * Renvoie le chemin interne correspondant au lien, ou null s'il est externe.
 */
export function toInternalPath(href: string): string | null {
  if (!href) {
    return null
  }
  if (href.startsWith('#') || href.startsWith('mailto:') || href.startsWith('tel:')) {
    return null
  }
  if (href.startsWith('/') && !href.startsWith('//')) {
    return href
  }
  try {
    const url = new URL(href, window.location.origin)
    if (url.protocol !== 'http:' && url.protocol !== 'https:') {
      return null
    }
    if (url.hostname === window.location.hostname || isSiteHost(url.hostname)) {
      return `${url.pathname}${url.search}${url.hash}`
    }
  } catch {
    return null
  }
  return null
}

/**
 * Réécrit les liens d'un contenu HTML : navigation interne pour les liens du
 * site, nouvel onglet annoncé pour les liens externes.
 */
export function normalizeRichTextLinks(html: string): string {
  if (!html || typeof window === 'undefined' || typeof DOMParser === 'undefined') {
    return html
  }

  const doc = new DOMParser().parseFromString(html, 'text/html')
  const links = doc.body.querySelectorAll('a[href]')
  if (!links.length) {
    return html
  }

  links.forEach((link) => {
    const href = link.getAttribute('href') || ''
    const internalPath = toInternalPath(href)

    if (internalPath) {
      link.setAttribute('href', internalPath)
      link.removeAttribute('target')
      link.removeAttribute('rel')
      link.setAttribute(INTERNAL_LINK_ATTRIBUTE, 'true')
      return
    }

    if (href.startsWith('http://') || href.startsWith('https://')) {
      link.setAttribute('target', '_blank')
      link.setAttribute('rel', 'noopener noreferrer')
      // RGAA 13.1 : l'ouverture d'une nouvelle fenêtre doit être annoncée.
      const existingTitle = link.getAttribute('title')
      if (!existingTitle) {
        link.setAttribute('title', `${link.textContent?.trim() || href} - ${NEW_WINDOW_MENTION}`)
      } else if (!existingTitle.includes(NEW_WINDOW_MENTION)) {
        link.setAttribute('title', `${existingTitle} - ${NEW_WINDOW_MENTION}`)
      }
    }
  })

  return doc.body.innerHTML
}
