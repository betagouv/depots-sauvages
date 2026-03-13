export const formatDate = (dateStr?: string | null) => {
  if (!dateStr) return 'Date inconnue'
  try {
    const date = new Date(dateStr)
    if (isNaN(date.getTime())) return 'Date invalide'
    return date.toLocaleString('fr-FR', {
      day: 'numeric',
      month: 'long',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  } catch (e) {
    console.error('Error formatting date:', e)
    return 'Date invalide'
  }
}

export const shouldShowModificationDate = (
  creationDate?: string | null,
  modificationDate?: string | null
) => {
  if (!creationDate || !modificationDate) return false
  const creation = new Date(creationDate).getTime()
  const modification = new Date(modificationDate).getTime()
  // Only show if modification is more than 1 minute after creation
  return modification - creation > 60000
}
