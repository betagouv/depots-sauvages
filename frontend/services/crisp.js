export function initCrisp() {
  const crispEnabled = import.meta.env.VITE_CRISP_ENABLED === 'true' || import.meta.env.VITE_CRISP_ENABLED === true
  const websiteId = import.meta.env.VITE_CRISP_WEBSITE_ID

  if (crispEnabled && websiteId) {
    window.$crisp = []
    window.CRISP_WEBSITE_ID = websiteId
    const script = document.createElement('script')
    script.src = 'https://client.crisp.chat/l.js'
    script.async = true
    document.head.appendChild(script)
  }
}
