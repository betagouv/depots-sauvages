import { openTallyPopup, closeTallyPopup, type TallyPopupOptions } from '@/utils/tally'
import { onMounted, onUnmounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

interface TallyRouteConfig {
  [path: string]: {
    formId: string
    options?: TallyPopupOptions
    returnPath?: string
  }
}

/**
 * Composable to handle Tally popup opening based on the current URL route.
 * @param config A mapping of paths to Tally form IDs and options.
 */
export function useTallyRoutes(config: TallyRouteConfig) {
  const route = useRoute()
  const router = useRouter()
  let activeFormId: string | null = null

  const handleTallyRoute = (path: string) => {
    const setup = config[path]
    if (setup) {
      if (activeFormId && activeFormId !== setup.formId) {
        closeTallyPopup(activeFormId)
      }
      activeFormId = setup.formId
      openTallyPopup(setup.formId, {
        ...setup.options,
        onClose: () => {
          // If we are still on the specific route when closing, go back to the return path
          if (route.path === path) {
            router.push(setup.returnPath ?? '/')
          }
          // Call original onClose if provided
          if (setup.options?.onClose) {
            setup.options.onClose()
          }
          if (activeFormId === setup.formId) {
            activeFormId = null
          }
        },
      })
    } else {
      if (activeFormId) {
        closeTallyPopup(activeFormId)
        activeFormId = null
      }
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

  onUnmounted(() => {
    if (activeFormId) {
      closeTallyPopup(activeFormId)
    }
  })
}
