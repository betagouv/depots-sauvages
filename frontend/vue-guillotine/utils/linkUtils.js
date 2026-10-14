export const INTERNAL_HOSTS = [
  'stopdepotsauvage.beta.gouv.fr',
  'www.stopdepotsauvage.beta.gouv.fr',
  'stop-depot-sauvage.beta.gouv.fr',
  'www.stop-depot-sauvage.beta.gouv.fr',
  'protect-envi.beta.gouv.fr',
  'www.protect-envi.beta.gouv.fr',
  'depots-sauvages.beta.gouv.fr',
  'www.depots-sauvages.beta.gouv.fr',
  'localhost',
  '127.0.0.1',
]

export const NEW_WINDOW_MENTION = 'nouvelle fenêtre'

export function isInternalUrl(url) {
  if (!url) return false
  const trimmed = url.trim()
  if (
    trimmed.startsWith('/') ||
    trimmed.startsWith('#') ||
    trimmed.startsWith('mailto:') ||
    trimmed.startsWith('tel:')
  )
    return true
  try {
    const parsed = new URL(trimmed, 'https://protect-envi.beta.gouv.fr')
    if (INTERNAL_HOSTS.includes(parsed.hostname)) return true
    if (typeof window !== 'undefined' && window.location?.hostname) {
      if (parsed.hostname === window.location.hostname) return true
    }
    return false
  } catch {
    return false
  }
}

export function normalizeLinkHref(url) {
  if (!url) return ''
  const trimmed = url.trim()
  if (trimmed.startsWith('#') || trimmed.startsWith('mailto:') || trimmed.startsWith('tel:')) {
    return trimmed
  }
  try {
    const parsed = new URL(trimmed, 'https://protect-envi.beta.gouv.fr')
    const currentHost = typeof window !== 'undefined' && window.location?.hostname
    if (
      INTERNAL_HOSTS.includes(parsed.hostname) ||
      (currentHost && parsed.hostname === currentHost)
    ) {
      return (parsed.pathname || '/') + parsed.search + parsed.hash
    }
  } catch {}
  return trimmed
}

export function cleanHtmlLinks(htmlContent) {
  if (typeof htmlContent !== 'string' || !htmlContent.includes('<a')) return htmlContent
  const attrRegex = /([a-zA-Z0-9_\-]+)(?:\s*=\s*(?:(["'])(.*?)\2|([^>\s]+)))?/g
  return htmlContent.replace(/<a\b([^>]*)>/gi, (_match, attrsStr) => {
    const attrs = {}
    let m
    while ((m = attrRegex.exec(attrsStr)) !== null) {
      const name = m[1].toLowerCase()
      const val = m[3] !== undefined ? m[3] : m[4] !== undefined ? m[4] : ''
      attrs[name] = val
    }
    const href = attrs.href || ''
    if (isInternalUrl(href)) {
      delete attrs.target
      delete attrs.rel
      attrs.href = normalizeLinkHref(href)
    } else {
      attrs.target = '_blank'
      attrs.rel = 'noopener noreferrer'
      // RGAA 13.1 : l'ouverture d'une nouvelle fenêtre doit être annoncée.
      if (!attrs.title) {
        attrs.title = NEW_WINDOW_MENTION
      } else if (!attrs.title.includes(NEW_WINDOW_MENTION)) {
        attrs.title = `${attrs.title} - ${NEW_WINDOW_MENTION}`
      }
    }
    const formatted = Object.entries(attrs)
      .map(([k, v]) => `${k}="${v}"`)
      .join(' ')
    return formatted ? `<a ${formatted}>` : '<a>'
  })
}
