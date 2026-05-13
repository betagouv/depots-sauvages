import { CRISP_ENABLED } from './config'

export function initCrisp() {
  const websiteId = import.meta.env.VITE_CRISP_WEBSITE_ID

  if (CRISP_ENABLED && websiteId) {
    window.$crisp = []
    window.CRISP_WEBSITE_ID = websiteId
    const script = document.createElement('script')
    script.src = 'https://client.crisp.chat/l.js'
    script.async = true
    document.head.appendChild(script)
  }
}
