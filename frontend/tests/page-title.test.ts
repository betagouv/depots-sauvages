import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { formatPageTitle, initPageTitles, setPageTitle } from '../services/pageTitle'

describe('Titres de page', () => {
  beforeEach(() => {
    window._paq = []
  })
  afterEach(() => {
    delete window._paq
  })

  it('formate le titre avec le nom du service', () => {
    expect(formatPageTitle('Contact')).toBe('Contact - Stop Dépôt Sauvage')
    expect(formatPageTitle(undefined)).toMatch(/^Stop Dépôt Sauvage - Accompagner/)
  })

  it('met à jour l onglet et envoie la page vue à Matomo avec le titre du contenu', () => {
    setPageTitle('Quel est le montant de l amende ?', '/faq/montant-amende')
    const title = 'Quel est le montant de l amende ? - Stop Dépôt Sauvage'
    expect(document.title).toBe(title)
    expect(window._paq).toEqual([
      ['setCustomUrl', `${window.location.origin}/faq/montant-amende`],
      ['setDocumentTitle', title],
      ['trackPageView'],
    ])
  })

  it('laisse les articles et questions FAQ fixer eux-mêmes leur titre', () => {
    let hook: (to: any) => void = () => {}
    initPageTitles({ afterEach: (fn: any) => (hook = fn) })

    hook({
      meta: { title: 'Article', dynamicTitle: true },
      params: { slug: 'x' },
      fullPath: '/blog/x',
    })
    expect(window._paq).toEqual([])

    hook({
      meta: { title: 'Foire Aux Questions', dynamicTitle: true },
      params: { slug: '' },
      fullPath: '/faq',
    })
    expect(document.title).toBe('Foire Aux Questions - Stop Dépôt Sauvage')
    expect(window._paq).toHaveLength(3)
  })
})
