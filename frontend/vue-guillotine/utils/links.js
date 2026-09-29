// Domaines du site (et leurs sous-domaines), en plus du domaine courant :
// liens absolus saisis en prod, y compris avec l'ancien nom du service.
const SITE_DOMAINS = [
  'stopdepotsauvage.beta.gouv.fr',
  'stop-depot-sauvage.beta.gouv.fr',
  'protect-envi.beta.gouv.fr',
  'protectenvi.beta.gouv.fr',
]

const isSiteDomain = (hostname) =>
  SITE_DOMAINS.some((domain) => hostname === domain || hostname.endsWith(`.${domain}`))

// Fichiers servis par le site : ils gardent l'ouverture dans un nouvel onglet.
const FILE_PATH_PREFIXES = ['/media/', '/static/']
const FILE_EXTENSION = /\.(pdf|docx?|xlsx?|odt|ods|csv|zip|jpe?g|png|webp|gif)$/i

/**
 * Classe un lien : 'internal' (page du site), 'file' (fichier du site),
 * 'anchor' (ancre dans la page), 'external' (autre site) ou 'other' (mailto, tel...).
 */
export function classifyLink(href, currentHost = window.location.host) {
  if (!href) return 'other'
  if (href.startsWith('#')) return 'anchor'

  let url
  try {
    url = new URL(href, `https://${currentHost}`)
  } catch {
    return 'other'
  }
  if (!['http:', 'https:'].includes(url.protocol)) return 'other'

  const isSiteHost = url.host === currentHost || isSiteDomain(url.hostname)
  if (!isSiteHost) return 'external'

  const isFile =
    FILE_PATH_PREFIXES.some((prefix) => url.pathname.startsWith(prefix)) ||
    FILE_EXTENSION.test(url.pathname)
  return isFile ? 'file' : 'internal'
}

/**
 * Chemin relatif d'un lien interne (ex. "https://site/faq/x#y" -> "/faq/x#y"),
 * pour qu'il fonctionne sur tous les environnements (local, recette, prod).
 */
export function toSitePath(href, currentHost = window.location.host) {
  const url = new URL(href, `https://${currentHost}`)
  return `${url.pathname}${url.search}${url.hash}`
}

/**
 * Réécrit les liens d'un contenu HTML riche :
 * - pages du site : même onglet, sans "nofollow" ;
 * - autres sites et fichiers : nouvel onglet, avec "noopener".
 */
export function processLinks(html, currentHost = window.location.host) {
  if (!html || !html.includes('<a')) return html

  const doc = new DOMParser().parseFromString(html, 'text/html')
  doc.querySelectorAll('a[href]').forEach((link) => {
    const href = link.getAttribute('href')
    switch (classifyLink(href, currentHost)) {
      case 'internal':
        link.setAttribute('href', toSitePath(href, currentHost))
        link.removeAttribute('target')
        link.removeAttribute('rel')
        break
      case 'anchor':
        link.removeAttribute('target')
        link.removeAttribute('rel')
        break
      case 'file':
      case 'external':
        link.setAttribute('target', '_blank')
        link.setAttribute('rel', 'noopener noreferrer')
        // RGAA : signaler l'ouverture dans une nouvelle fenêtre
        if (!link.getAttribute('title')) {
          link.setAttribute('title', `${link.textContent.trim()} - nouvelle fenêtre`)
        }
        break
      default:
        link.removeAttribute('target')
    }
  })
  return doc.body.innerHTML
}
