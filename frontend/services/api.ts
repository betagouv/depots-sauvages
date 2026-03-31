// URLs from environment variables
export const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'
export const API_URL = `${BACKEND_URL}/api`
export const DN_BASE_URL = import.meta.env.VITE_DN_BASE_URL || 'https://demarche.numerique.gouv.fr'

// Helper to get CSRF token
const getCSRFToken = (): string => {
  // First try to get from cookie
  const name = 'csrftoken='
  const decodedCookie = decodeURIComponent(document.cookie)
  const cookieArray = decodedCookie.split(';')
  for (let cookie of cookieArray) {
    cookie = cookie.trim()
    if (cookie.indexOf(name) === 0) {
      return cookie.substring(name.length, cookie.length)
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
  userDossiers: `${API_URL}/dossiers/`,
  syncDossiers: `${API_URL}/dossiers/sync/`,
}

// API functions
async function makeRequest(url: string, method: 'GET' | 'POST' | 'PUT', data: any) {
  const options: RequestInit = {
    method,
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCSRFToken() || '',
    },
    credentials: 'include',
  }

  // Only include body for POST and PUT requests
  if (method !== 'GET' && data) {
    options.body = JSON.stringify(data)
  }

  const response = await fetch(url, options)

  if (!response.ok) {
    const error = await response.json()
    throw error
  }

  return response.json()
}

export const createResource = (url: string, data: any) => makeRequest(url, 'POST', data)

export const updateResource = (url: string, data: any) => makeRequest(url, 'PUT', data)

export const fetchResource = (url: string) => makeRequest(url, 'GET', {})

export interface UserInfo {
  is_authenticated: boolean
  proconnect_enabled: boolean
  first_name?: string
  last_name?: string
  email?: string
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
  localisation_depot: string | null
  last_sync: string | null
}

export const getUserSignalements = (): Promise<UserSignalement[]> =>
  makeRequest(API_URLS.userDossiers, 'GET', {})

export const syncDossiers = (): Promise<{ status: string }> =>
  makeRequest(API_URLS.syncDossiers, 'POST', {})
