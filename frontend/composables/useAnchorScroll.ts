import { watch, type Ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { trackEvent } from '@/services/matomo'
import { smoothScrollTo } from '@/utils/scroll'

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
      setTimeout(() => {
        const el = document.getElementById(slug)
        if (el) {
          smoothScrollTo(el, 800, 50) // 800ms duration, 50px offset
        }
      }, 0)
    } else if (route.hash === `#${slug}`) {
      router.replace({ hash: '' })
    }
  })
}
