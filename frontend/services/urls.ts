import { BACKEND_URL } from './api'

// Get the URL for downloading the doc "rapport de constatation"
export const getDocConstatUrl = (id: number): string =>
  `${BACKEND_URL}/documents/signalements/${id}/`
