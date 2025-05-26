import { BACKEND_URL } from './api'

// Get the URL for downloading a document
export const getDocumentUrl = (id: number): string => `${BACKEND_URL}/documents/signalements/${id}/`
