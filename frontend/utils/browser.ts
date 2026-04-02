/**
 * Ouvre un lien externe dans un nouvel onglet avec les attributs de sécurité appropriés.
 * @param url URL à ouvrir
 */
export const openExternalLink = (url: string | null | undefined) => {
  if (url) {
    window.open(url, '_blank', 'noopener,noreferrer')
  }
}
