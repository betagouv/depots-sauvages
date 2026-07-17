export interface TallyPopupOptions {
  layout?: 'default' | 'modal'
  width?: number
  alignLeft?: boolean
  hideTitle?: boolean
  overlay?: boolean
  emoji?: {
    text: string
    animation:
      | 'none'
      | 'wave'
      | 'tada'
      | 'heart-beat'
      | 'spin'
      | 'flash'
      | 'bounce'
      | 'rubber-band'
      | 'head-shake'
  }
  autoClose?: number
  showOnce?: boolean
  doNotShowAfterSubmit?: boolean
  customFormUrl?: string
  hiddenFields?: Record<string, any>
  onOpen?: () => void
  onClose?: () => void
  onPageView?: (page: number) => void
  onSubmit?: (payload: any) => void
}

declare global {
  interface Window {
    Tally?: {
      openPopup: (formId: string, options?: TallyPopupOptions) => void
      closePopup: (formId: string) => void
      loadEmbeds: () => void
    }
  }
}

export const openTallyPopup = (formId: string, options: TallyPopupOptions = {}) => {
  const tryOpen = () => {
    if (typeof window !== 'undefined' && window.Tally) {
      window.Tally.openPopup(formId, options)
      return true
    }
    return false
  }

  if (!tryOpen()) {
    let attempts = 0
    const interval = setInterval(() => {
      attempts++
      if (tryOpen() || attempts >= 20) {
        clearInterval(interval)
        if (attempts >= 20 && !window.Tally) {
          console.warn('Tally script is not loaded yet after 2 seconds.')
        }
      }
    }, 100)
  }
}

export const closeTallyPopup = (formId: string) => {
  if (typeof window !== 'undefined' && window.Tally) {
    window.Tally.closePopup(formId)
  }
}

export const loadTallyEmbeds = () => {
  const tryLoad = () => {
    if (typeof window !== 'undefined' && window.Tally) {
      window.Tally.loadEmbeds()
      return true
    }
    return false
  }

  if (!tryLoad()) {
    let attempts = 0
    const interval = setInterval(() => {
      attempts++
      if (tryLoad() || attempts >= 20) {
        clearInterval(interval)
        if (attempts >= 20 && !window.Tally) {
          console.warn('Tally script is not loaded yet after 2 seconds.')
        }
      }
    }, 100)
  }
}
