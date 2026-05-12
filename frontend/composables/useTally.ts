import { openTallyPopup, type TallyPopupOptions } from '@/utils/tally'
import { onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

interface TallyRouteConfig {
  [path: string]: {
    formId: string
    options?: TallyPopupOptions
  }
}

/**
 * Composable to handle Tally popup opening based on the current URL route.
 * @param config A mapping of paths to Tally form IDs and options.
 */
export function useTallyRoutes(config: TallyRouteConfig) {
  const route = useRoute()
  const router = useRouter()

  const handleTallyRoute = (path: string) => {
    const setup = config[path]
    if (setup) {
      openTallyPopup(setup.formId, {
        ...setup.options,
        onClose: () => {
          // If we are still on the specific route when closing, go back to home
          if (route.path === path) {
            router.push('/')
          }
          // Call original onClose if provided
          if (setup.options?.onClose) {
            setup.options.onClose()
          }
        },
      })
    }
  }

  onMounted(() => {
    handleTallyRoute(route.path)
  })

  watch(
    () => route.path,
    (newPath) => {
      handleTallyRoute(newPath)
    }
  )
}
