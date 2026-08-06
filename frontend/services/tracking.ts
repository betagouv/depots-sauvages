import { API_URL, postResource } from './api'

const TRACK_URL = `${API_URL}/track-action/`

export function trackUserAction(
  action: string,
  objectId?: string | number | null,
  data?: Record<string, unknown>
) {
  postResource(TRACK_URL, {
    action,
    object: objectId != null ? String(objectId) : undefined,
    data,
  }).catch(() => {
    // Fire-and-forget: do not break UX if tracking fails
  })
}
