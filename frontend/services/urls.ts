import { API_URL } from './api'

// Get the URL for downloading the doc "rapport de constatation"
export const getDocConstatUrl = (id: number | null) => {
  if (!id) return ''
  return `${API_URL}/signalements/${id}/documents/doc-constat/`
}

export const getLettreInfoUrl = (id: number | null) => {
  if (!id) return ''
  return `${API_URL}/signalements/${id}/documents/lettre-info/`
}

export const getSendEmailUrl = (id: number | null) => {
  if (!id) return ''
  return `${API_URL}/signalements/${id}/send-email/`
}
