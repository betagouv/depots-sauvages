import { API_URL, BACKEND_URL } from './api'

// Get the URL for downloading the doc "rapport de constatation"
export const getDocConstatUrl = (id: number | null) => {
  if (!id) return ''
  return `${API_URL}/constatations/${id}/documents/doc-constat/`
}

export const getLettreInfoUrl = (id: number | null) => {
  if (!id) return ''
  return `${API_URL}/constatations/${id}/documents/lettre-info/`
}


export const getSuiviProcedureUrl = (id: number | string) => {
  return `/suivi-procedure/${id}`
}

export const LOGIN_URL = `${BACKEND_URL}/oidc/authenticate/`
export const LOGOUT_URL = `${BACKEND_URL}/logout/`
