const FILE_PATH = /^\/(media|static)\/|\.(pdf|docx?|xlsx?|odt|ods|csv|zip|jpe?g|png|webp|gif)$/i

const isSiteHost = (hostname, siteHosts) =>
  hostname === window.location.hostname ||
  siteHosts.some((host) => hostname === host || hostname.endsWith(`.${host}`))

export function getLinkTarget(href, siteHosts = []) {
  if (!href || href.startsWith('#')) return {}
  let url
  try {
    url = new URL(href, window.location.origin)
  } catch {
    return {}
  }
  if (!['http:', 'https:'].includes(url.protocol)) return {}
  if (isSiteHost(url.hostname, siteHosts) && !FILE_PATH.test(url.pathname)) {
    return { internalPath: `${url.pathname}${url.search}${url.hash}` }
  }
  return { newTab: true }
}

export function processLinks(html, siteHosts = []) {
  if (!html?.includes('<a')) return html
  const doc = new DOMParser().parseFromString(html, 'text/html')
  doc.querySelectorAll('a[href]').forEach((link) => {
    const { internalPath, newTab } = getLinkTarget(link.getAttribute('href'), siteHosts)
    link.removeAttribute('target')
    link.removeAttribute('rel')
    if (internalPath) {
      link.setAttribute('href', internalPath)
    }
    if (newTab) {
      link.setAttribute('target', '_blank')
      link.setAttribute('rel', 'noopener noreferrer')
      if (!link.title) {
        link.title = `${link.textContent.trim()} - nouvelle fenêtre`
      }
    }
  })
  return doc.body.innerHTML
}
