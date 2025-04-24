import { BACKEND_URL } from './api'

// Get the URL for downloading a document
// giveng the ID of the signalement and the format, 'pdf' or 'odt'

export const getDocumentUrl = (id: number, format: 'pdf' | 'odt' = 'odt'): string =>
  `${BACKEND_URL}/documents/signalements/${id}${format === 'pdf' ? '/pdf' : ''}/`
