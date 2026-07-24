// In development, use VITE_BACKEND_URL (e.g., to query local Django on port 8000 from Vite on port 5173).
// In production, the frontend and backend are served from the same host. We dynamically use
// the current origin (window.location.origin) to adapt seamlessly to Scalingo review apps/staging/prod
// and avoid Content Security Policy (connect-src 'self') errors.
export const BACKEND_URL = import.meta.env.DEV
  ? import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'
  : typeof window !== 'undefined'
    ? window.location.origin
    : ''
export const API_URL = `${BACKEND_URL}/api`
export const DN_BASE_URL = import.meta.env.VITE_DN_BASE_URL || 'https://demarche.numerique.gouv.fr'

// Helper to get CSRF token
const getCSRFToken = (): string => {
  const decodedCookie = decodeURIComponent(document.cookie)
  const cookies = decodedCookie.split(';').map((c) => c.trim())

  const secureCookie = cookies.find((c) => c.startsWith('__Host-csrftoken='))
  if (secureCookie) return secureCookie.substring('__Host-csrftoken='.length)

  const standardCookie = cookies.find((c) => c.startsWith('csrftoken='))
  if (standardCookie) return standardCookie.substring('csrftoken='.length)

  return document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || ''
}

export type APIResponseStatus = 'success' | 'error' | 'sync_triggered'

// API endpoints
export const API_URLS = {
  userInfo: `${API_URL}/user-info/`,
  userProcedures: `${API_URL}/constatations/`,
  bypassAuthConfig: `${API_URL}/bypass-auth/config/`,
  bypassAuthLogin: `${API_URL}/bypass-auth/login/`,
  constatations: `${API_URL}/constatations/`,
}

// API functions
async function makeRequest(
  url: string,
  method: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE',
  data?: any
) {
  const options: RequestInit = {
    method,
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCSRFToken() || '',
    },
    credentials: 'include',
  }

  // Only include body for POST, PUT and PATCH requests
  if (method !== 'GET' && method !== 'DELETE' && data) {
    options.body = JSON.stringify(data)
  }

  const response = await fetch(url, options)

  if (response.status === 204 || response.headers.get('content-length') === '0') {
    return null
  }

  const contentType = response.headers.get('content-type')
  const isJson = contentType && contentType.includes('application/json')

  if (!response.ok) {
    const error = isJson ? await response.json() : await response.text()
    throw error
  }

  return isJson ? response.json() : response.text()
}

export const createResource = (url: string, data: any) => makeRequest(url, 'POST', data)

export const updateResource = (url: string, data: any) => makeRequest(url, 'PUT', data)

export const patchResource = (url: string, data: any) => makeRequest(url, 'PATCH', data)

export const deleteResource = (url: string) => makeRequest(url, 'DELETE')

export const fetchResource = (url: string) => makeRequest(url, 'GET')

export const postResource = (url: string, data: any = {}) => makeRequest(url, 'POST', data)

export interface UserInfo {
  is_authenticated: boolean
  proconnect_enabled: boolean
  first_name?: string
  last_name?: string
  email?: string
  procedures_count?: number
  is_staff?: boolean
}

export const getUserInfo = (): Promise<UserInfo> => makeRequest(API_URLS.userInfo, 'GET', {})
export interface ProcedureOverview {
  id: number
  title: string
  date_creation?: string
  date_modification: string | null
  state?: string
  date_constat: string | null
  heure_constat: string | null
  localisation_depot: string | null
  last_sync: string | null
  auteur_identifie: boolean
  suivi_procedure?: {
    etape_en_cours: number
    identification_reussie?: boolean | null
    decision_poursuite?: string | null
    dossier_archive?: boolean
  }
}

export const getUserProcedures = (): Promise<ProcedureOverview[]> =>
  makeRequest(API_URLS.userProcedures, 'GET', {})

export interface BypassAuthConfig {
  enabled: boolean
}

export interface BypassAuthUser {
  id: number
  first_name: string
  last_name: string
  email: string
}

export const getBypassAuthConfig = (): Promise<BypassAuthConfig> =>
  makeRequest(API_URLS.bypassAuthConfig, 'GET', {})

export const loginBypassAuth = (
  email: string
): Promise<{ message: string; user: BypassAuthUser }> =>
  makeRequest(API_URLS.bypassAuthLogin, 'POST', { email })
