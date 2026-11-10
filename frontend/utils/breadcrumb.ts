import type { RouteLocationNormalizedLoaded, RouteMeta, Router } from 'vue-router'

export interface BreadcrumbLink {
  text: string
  to?: string
}

const HOME_LINK: BreadcrumbLink = { text: 'Accueil', to: '/' }
const MAX_DEPTH = 5

const labelOf = (meta: RouteMeta): string | undefined =>
  (meta.breadcrumbLabel as string | undefined) ?? (meta.title as string | undefined)

/**
 * Builds the DSFR breadcrumb for the current route from its `meta`:
 * `breadcrumb: false` hides it, `breadcrumbParent` adds intermediate levels,
 * `breadcrumbLabel` overrides `title`. The last item has no link (current page).
 */
export function buildBreadcrumbLinks(
  route: RouteLocationNormalizedLoaded,
  router: Router,
  dynamicLabel?: string | null,
): BreadcrumbLink[] {
  const meta = route.meta
  if (meta.breadcrumb === false || meta.hideNavigation) {
    return []
  }
  const currentLabel = dynamicLabel || labelOf(meta)
  if (!currentLabel) {
    return []
  }

  const parents: BreadcrumbLink[] = []
  let parentPath = meta.breadcrumbParent as string | undefined
  while (parentPath && parents.length < MAX_DEPTH) {
    const parentMeta = router.resolve(parentPath).meta
    const parentLabel = labelOf(parentMeta)
    if (!parentLabel) {
      break
    }
    parents.unshift({ text: parentLabel, to: parentPath })
    parentPath = parentMeta.breadcrumbParent as string | undefined
  }

  return [HOME_LINK, ...parents, { text: currentLabel }]
}
