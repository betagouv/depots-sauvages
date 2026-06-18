// URLs from environment variables
export const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'
export const API_URL = `${BACKEND_URL}/api`
export const DN_BASE_URL = import.meta.env.VITE_DN_BASE_URL || 'https://demarche.numerique.gouv.fr'

// Helper to get CSRF token
const getCSRFToken = (): string => {
  // First try to get from cookie
  const decodedCookie = decodeURIComponent(document.cookie)
  const cookieArray = decodedCookie.split(';')

  // Try secure cookie first (prod/staging)
  const secureName = '__Host-csrftoken='
  for (let cookie of cookieArray) {
    cookie = cookie.trim()
    if (cookie.indexOf(secureName) === 0) {
      return cookie.substring(secureName.length, cookie.length)
    }
  }

  // Fallback to standard cookie (local dev)
  const standardName = 'csrftoken='
  for (let cookie of cookieArray) {
    cookie = cookie.trim()
    if (cookie.indexOf(standardName) === 0) {
      return cookie.substring(standardName.length, cookie.length)
    }
  }

  // If not in cookie, try to get from meta tag
  const element = document.querySelector('meta[name="csrf-token"]')
  if (element && element.getAttribute('content')) {
    return element.getAttribute('content') as string
  }

  return ''
}

export type APIResponseStatus = 'success' | 'error' | 'sync_triggered'

// API endpoints
export const API_URLS = {
  processDossier: `${API_URL}/signalements/process-dn-dossier/`,
  userInfo: `${API_URL}/user-info/`,
  userDossiers: `${API_URL}/constatations/`,
  syncDossiers: `${API_URL}/dossiers/sync/`,
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
export interface UserSignalement {
  id: number
  numero_dossier: number
  title: string
  date_creation?: string
  date_modification: string | null
  state?: string
  date_constat: string | null
  heure_constat: string | null
  localisation_depot: string | null
  last_sync: string | null
}

export const getUserSignalements = (): Promise<UserSignalement[]> =>
  makeRequest(API_URLS.userDossiers, 'GET', {})

export const syncDossiers = (): Promise<{ status: string }> =>
  makeRequest(API_URLS.syncDossiers, 'POST', {})

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
