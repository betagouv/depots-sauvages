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

export const getDsDocConstatUrl = (id: number | null) => {
  if (!id) return ''
  return `${API_URL}/ds-signalements/${id}/documents/doc-constat/`
}

export const getDsLettreInfoUrl = (id: number | null) => {
  if (!id) return ''
  return `${API_URL}/ds-signalements/${id}/documents/lettre-info/`
}
