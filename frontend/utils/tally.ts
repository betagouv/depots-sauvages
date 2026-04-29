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
  if (typeof window !== 'undefined' && window.Tally) {
    window.Tally.openPopup(formId, options)
  } else {
    console.warn('Tally script is not loaded yet.')
  }
}

export const closeTallyPopup = (formId: string) => {
  if (typeof window !== 'undefined' && window.Tally) {
    window.Tally.closePopup(formId)
  }
}
