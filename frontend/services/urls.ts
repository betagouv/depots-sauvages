import { API_URL, DN_BASE_URL } from './api'

// Get the URL for downloading the doc "rapport de constatation"
export const getDocConstatUrl = (id: number | null) => {
  if (!id) return ''
  return `${API_URL}/signalements/${id}/documents/doc-constat/`
}

export const getLettreInfoUrl = (id: number | null) => {
  if (!id) return ''
  return `${API_URL}/signalements/${id}/documents/lettre-info/`
}

export const getDnDocConstatUrl = (id: number | null) => {
  if (!id) return ''
  return `${API_URL}/dn-signalements/${id}/documents/doc-constat/`
}

export const getDnLettreInfoUrl = (id: number | null) => {
  if (!id) return ''
  return `${API_URL}/dn-signalements/${id}/documents/lettre-info/`
}

export const getDnModifyUrl = (numeroDossier: string | null) => {
  if (!numeroDossier) return ''
  return `${DN_BASE_URL}/dossiers/${numeroDossier}/modifier`
}

export const LOGIN_URL = '/oidc/authenticate/'
export const LOGOUT_URL = '/logout/'
