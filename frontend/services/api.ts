import type { SuiviProcedure } from '../stores/suivi-procedure'
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
export const getCSRFToken = (): string => {
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
  proconnectRejectedInfo: `${API_URL}/proconnect/rejected-info/`,
  proconnectDemanderAcces: `${API_URL}/proconnect/demander-acces/`,
  backofficeProConnectConfig: `${API_URL}/backoffice/proconnect-config/`,
  chatbotConfig: `${API_URL}/chatbot/config/`,
  chatbotTestConnection: `${API_URL}/chatbot/test-connection/`,
  chatbotFeedback: `${API_URL}/chatbot/feedback/`,
  chatbotConversations: `${API_URL}/chatbot/conversations/`,
}

// API functions
async function makeRequest(
  url: string,
  method: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE',
  data?: any
) {
  const isFormData = typeof FormData !== 'undefined' && data instanceof FormData

  const headers: Record<string, string> = {
    'X-CSRFToken': getCSRFToken() || '',
  }
  if (!isFormData) {
    headers['Content-Type'] = 'application/json'
  }

  const options: RequestInit = {
    method,
    headers,
    credentials: 'include',
  }

  // Only include body for POST, PUT and PATCH requests
  if (method !== 'GET' && method !== 'DELETE' && data) {
    options.body = isFormData ? data : JSON.stringify(data)
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
  title?: string
  commune?: string
  date_creation?: string
  date_modification: string | null
  state?: string
  date_constat: string | null
  heure_constat: string | null
  localisation_depot: string | null
  last_sync?: string | null
  auteur_identifie: boolean | null
  statut_auteur?: string | null
  auteur_nom?: string
  auteur_prenom?: string
  is_draft?: boolean
  // Procedure tracking summary: fields needed to determine which sections are completed
  suivi_procedure?: Partial<SuiviProcedure> & { etape_en_cours: number }
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

export interface ProConnectRejectedInfo {
  siret?: string
  siren?: string
  organization_label?: string
  email?: string
  name?: string
}

export interface ProConnectAccessRequestPayload {
  siret?: string
  siren?: string
  organization_label?: string
  email: string
  name?: string
  message?: string
}

export const getProConnectRejectedInfo = (): Promise<ProConnectRejectedInfo> =>
  makeRequest(API_URLS.proconnectRejectedInfo, 'GET')

export const submitProConnectAccessRequest = (
  payload: ProConnectAccessRequestPayload
): Promise<{ success: boolean; message: string }> =>
  makeRequest(API_URLS.proconnectDemanderAcces, 'POST', payload)

export interface ChatbotConfigData {
  id?: number
  provider: string
  model: string
  api_key?: string
  base_url?: string
  timeout: number
  system_prompt: string
  has_api_key?: boolean
  api_key_masked?: string
  default_system_prompt?: string
}

export const getChatbotConfig = (): Promise<ChatbotConfigData> =>
  makeRequest(API_URLS.chatbotConfig, 'GET')

export const updateChatbotConfig = (
  payload: Partial<ChatbotConfigData> & { clear_api_key?: boolean }
): Promise<ChatbotConfigData> =>
  makeRequest(API_URLS.chatbotConfig, 'PUT', payload)

export interface ChatbotTestConnectionResponse {
  success: boolean
  message?: string
  error?: string
  provider?: string
  model?: string
  latency_ms?: number
  sample_reply?: string
  status_code?: number
}

export const testChatbotConnection = (
  payload: Partial<ChatbotConfigData>
): Promise<ChatbotTestConnectionResponse> =>
  makeRequest(API_URLS.chatbotTestConnection, 'POST', payload)

export interface SendChatbotFeedbackPayload {
  conversationId?: string
  messageId?: string
  messageIndex?: number
  feedback: 'up' | 'down' | ''
}

export const sendChatbotFeedback = (
  payload: SendChatbotFeedbackPayload
): Promise<{ success: boolean; conversationId: string; feedback: string }> =>
  makeRequest(API_URLS.chatbotFeedback, 'POST', payload)

export interface ChatbotConversationSummary {
  id: string
  user_email: string
  user_name: string
  current_path: string
  messages_count: number
  first_user_message: string
  last_user_message: string
  has_draft_proposed: boolean
  feedback: 'up' | 'down' | ''
  created_at: string
  updated_at: string
}

export interface ChatbotConversationDetail extends ChatbotConversationSummary {
  messages: Array<{
    id: string
    role: 'user' | 'assistant'
    content: string
    timestamp: string
    tool_calls?: Array<any>
    feedback?: 'up' | 'down'
  }>
}

export interface ChatbotConversationsListResponse {
  count: number
  page: number
  page_size: number
  stats: {
    total_conversations: number
    drafts_count: number
    positive_count: number
    negative_count: number
  }
  results: ChatbotConversationSummary[]
}

export const getChatbotConversations = (params: {
  page?: number
  page_size?: number
  search?: string
  has_draft?: string
  feedback?: string
}): Promise<ChatbotConversationsListResponse> => {
  const query = new URLSearchParams()
  if (params.page) query.append('page', params.page.toString())
  if (params.page_size) query.append('page_size', params.page_size.toString())
  if (params.search) query.append('search', params.search)
  if (params.has_draft) query.append('has_draft', params.has_draft)
  if (params.feedback) query.append('feedback', params.feedback)

  const queryString = query.toString() ? `?${query.toString()}` : ''
  return makeRequest(`${API_URLS.chatbotConversations}${queryString}`, 'GET')
}

export const getChatbotConversationDetail = (id: string): Promise<ChatbotConversationDetail> =>
  makeRequest(`${API_URLS.chatbotConversations}${id}/`, 'GET')

export const deleteChatbotConversation = (id: string): Promise<void> =>
  makeRequest(`${API_URLS.chatbotConversations}${id}/`, 'DELETE')



