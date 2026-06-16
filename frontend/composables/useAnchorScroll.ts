import { trackEvent } from '@/services/matomo'
import { smoothScrollTo } from '@/utils/scroll'
import { watch, type Ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

/**
 * Synchronizes a component's expanded/active state with the route hash,
 * automatically scrolls to the element when expanded, and tracks views.
 */
export function useAnchorScroll(
  isExpanded: Ref<boolean>,
  slug: string,
  title: string,
  category = 'FAQ'
) {
  const route = useRoute()
  const router = useRouter()

  onMounted(() => {
    if (typeof window !== 'undefined' && route.hash === `#${slug}`) {
      // Prevent browser from trying to restore previous scroll position on reload
      if ('scrollRestoration' in history) {
        history.scrollRestoration = 'manual'
      }
    }
  })

  watch(
    () => route.hash,
    (newHash) => {
      if (newHash === `#${slug}`) {
        isExpanded.value = true
      }
    },
    { immediate: true }
  )

  watch(isExpanded, (expanded) => {
    if (expanded) {
      trackEvent(category, 'Ouverture', title)
      if (route.hash !== `#${slug}`) {
        router.replace({ hash: `#${slug}` })
      }
      const tryScroll = (attempts = 0) => {
        const el = document.getElementById(slug)
        if (el) {
          setTimeout(() => {
            smoothScrollTo(el, 800, 50) // 800ms duration, 50px offset
          }, 250)
        } else if (attempts < 40) { // Retry for a maximum of 2 seconds (40 * 50ms)
          setTimeout(() => tryScroll(attempts + 1), 50)
        }
      }
      tryScroll()
    } else if (route.hash === `#${slug}`) {
      router.replace({ hash: '' })
    }
  }, { immediate: true })
}
