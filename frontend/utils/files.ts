export async function getFileSizeFromUrl(url) {
  try {
    const response = await fetch(url, { method: 'HEAD' })
    const length = response.headers.get('content-length')
    return length ? parseInt(length, 10) : null
  } catch (error) {
    console.error('Erreur lors de la récupération de la taille du fichier :', error)
    return null
  }
}

export function formatBytes(bytes) {
  if (typeof bytes !== 'number') return 'Inconnu'
  const units = ['o', 'Ko', 'Mo', 'Go']
  let i = 0
  while (bytes >= 1024 && i < units.length - 1) {
    bytes /= 1024
    i++
  }
  return `${bytes.toFixed(1)} ${units[i]}`
}
