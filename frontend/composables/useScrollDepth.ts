import { trackEvent } from '@/services/matomo'
import { onMounted, onUnmounted } from 'vue'

const THRESHOLDS = [25, 50, 75, 100] as const

/**
 * Tracks how far the visitor reads a content page and sends one Matomo event
 * per threshold reached (25/50/75/100 %), at most once per page visit.
 *
 * Reading depth is used instead of time on page because Matomo cannot measure
 * the time spent on the last page of a visit — precisely the case of a visitor
 * who reads a content page and then leaves.
 *
 * @param pageName Label sent as the event name, e.g. 'Comprendre la procédure'.
 * @param category Matomo event category, shared by the whole information journey.
 */
export function useScrollDepth(pageName: string, category = 'Parcours information') {
  const reached = new Set<number>()

  const currentDepth = () => {
    const scrollable = document.documentElement.scrollHeight - window.innerHeight
    // A page shorter than the viewport is entirely visible: count it as fully read.
    if (scrollable <= 0) {
      return 100
    }
    return Math.min(
      100,
      Math.round(
        ((window.scrollY + window.innerHeight) / document.documentElement.scrollHeight) * 100
      )
    )
  }

  const check = () => {
    const depth = currentDepth()
    for (const threshold of THRESHOLDS) {
      if (depth >= threshold && !reached.has(threshold)) {
        reached.add(threshold)
        trackEvent(category, `Lecture ${threshold}%`, pageName, threshold)
      }
    }
  }

  let ticking = false
  const onScroll = () => {
    if (ticking) {
      return
    }
    ticking = true
    window.requestAnimationFrame(() => {
      check()
      ticking = false
    })
  }

  onMounted(() => {
    trackEvent(category, 'Entrée parcours', pageName)
    check()
    window.addEventListener('scroll', onScroll, { passive: true })
    window.addEventListener('resize', onScroll, { passive: true })
  })

  onUnmounted(() => {
    window.removeEventListener('scroll', onScroll)
    window.removeEventListener('resize', onScroll)
  })
}
