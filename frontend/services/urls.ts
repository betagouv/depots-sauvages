import { BACKEND_URL } from './api'

// Get the URL for downloading the doc "rapport de constatation"
export const getDocConstatUrl = (id: number | null) => {
  if (!id) return ''
  return `${BACKEND_URL}/api/signalements/${id}/documents/doc-constat/`
}

export const getLettreInfoUrl = (id: number | null) => {
  if (!id) return ''
  return `${BACKEND_URL}/api/signalements/${id}/documents/lettre-info/`
}
