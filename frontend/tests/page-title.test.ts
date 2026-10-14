import { describe, expect, it } from 'vitest'
import { buildPageTitle, hasContentTitle, setPageTitle } from '../services/pageTitle'

describe('Titre de page', () => {
  it('ajoute le nom du site au titre', () => {
    expect(buildPageTitle('Contact')).toBe('Contact - Stop Dépôt Sauvage')
  })

  it('utilise le titre par défaut sans titre de route', () => {
    expect(buildPageTitle(undefined)).toMatch(/^Stop Dépôt Sauvage - Accompagner/)
  })

  it('met à jour l onglet du navigateur', () => {
    setPageTitle('FAQ')
    expect(document.title).toBe('FAQ - Stop Dépôt Sauvage')
  })

  it('laisse les articles et questions FAQ poser leur propre titre', () => {
    expect(hasContentTitle({ name: 'BlogArticle', params: { slug: 'a' } })).toBe(true)
    expect(hasContentTitle({ name: 'FAQ', params: { slug: 'question' } })).toBe(true)
    expect(hasContentTitle({ name: 'FAQ', params: { slug: '' } })).toBe(false)
    expect(hasContentTitle({ name: 'Blog', params: {} })).toBe(false)
  })
})
