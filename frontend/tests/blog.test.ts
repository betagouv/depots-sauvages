import { createTestingPinia } from '@pinia/testing'
import '@testing-library/jest-dom'
import { fireEvent, render, screen } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { axe } from 'vitest-axe'
import BlogArticleCard, { type BlogArticleItem } from '../components/blog/BlogArticleCard.vue'
import BlogArticleModal from '../components/blog/BlogArticleModal.vue'
import BlogPage from '../pages/blog.vue'
import BlogArticlePage from '../pages/blog-article.vue'
import * as api from '../services/api'
import { normalizeRichTextLinks, toInternalPath } from '../vue-guillotine/utils/links'

vi.mock('vue-router', () => ({
  useRoute: () => ({
    path: '/blog/test-article',
    params: { slug: 'test-article' },
  }),
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn(),
  }),
}))

vi.mock('../services/api', async () => {
  const actual = await vi.importActual('../services/api')
  return {
    ...actual,
    fetchResource: vi.fn(),
    createResource: vi.fn(),
    patchResource: vi.fn(),
    deleteResource: vi.fn(),
    postResource: vi.fn(),
  }
})

const mockArticle: BlogArticleItem = {
  id: 1,
  title: 'Article de test',
  slug: 'article-de-test',
  summary: 'Un super résumé pour l article de test.',
  cover_image: 'https://example.com/image.jpg',
  content: [{ type: 'rich_text', value: '<p>Contenu détaillé</p>' }],
  is_published: true,
  order: 0,
  created_at: '2026-08-01T12:00:00Z',
  updated_at: '2026-08-01T12:00:00Z',
}

describe('Composant BlogArticleCard', () => {
  it('affiche correctement les informations de l article', () => {
    const { getByText, getByAltText } = render(BlogArticleCard, {
      props: { article: mockArticle },
      global: {
        stubs: { RouterLink: { template: '<a><slot /></a>' } },
      },
    })
    expect(getByText('Article de test')).toBeInTheDocument()
    expect(getByText('Un super résumé pour l article de test.')).toBeInTheDocument()
    expect(getByAltText('Article de test')).toHaveAttribute('src', 'https://example.com/image.jpg')
  })

  it('affiche un badge brouillon si non publié', () => {
    const draftArticle = { ...mockArticle, is_published: false }
    const { getByText } = render(BlogArticleCard, {
      props: { article: draftArticle },
      global: {
        stubs: { RouterLink: { template: '<a><slot /></a>' } },
      },
    })
    expect(getByText('Brouillon')).toBeInTheDocument()
  })
})

describe('Page Blog Listing', () => {
  beforeEach(() => {
    vi.resetAllMocks()
  })

  it('affiche la liste des articles reçus', async () => {
    ;(api.fetchResource as any).mockResolvedValue([mockArticle])
    const pinia = createTestingPinia({ stubActions: true })
    const { findByText } = render(BlogPage, {
      global: {
        plugins: [pinia],
        stubs: {
          RouterLink: { template: '<a><slot /></a>' },
          DsfrButton: { template: '<button><slot /></button>' },
          DsfrModal: true,
          ConfirmModal: true,
          AdminControls: true,
        },
      },
    })
    expect(await findByText('Article de test')).toBeInTheDocument()
  })

  it('doit être accessible (A11y)', async () => {
    ;(api.fetchResource as any).mockResolvedValue([mockArticle])
    const pinia = createTestingPinia({ stubActions: true })
    const { container, findByText } = render(BlogPage, {
      global: {
        plugins: [pinia],
        stubs: {
          RouterLink: { template: '<a><slot /></a>' },
          DsfrButton: { template: '<button><slot /></button>' },
          DsfrModal: true,
          ConfirmModal: true,
          AdminControls: true,
        },
      },
    })
    await findByText('Article de test')
    const results = await axe(container)
    expect(results.violations).toHaveLength(0)
  })
})

describe('Page Blog Article Détail', () => {
  beforeEach(() => {
    vi.resetAllMocks()
  })

  it('charge et affiche le détail de l article', async () => {
    ;(api.fetchResource as any).mockResolvedValue(mockArticle)
    const pinia = createTestingPinia({ stubActions: true })
    const { findByText } = render(BlogArticlePage, {
      global: {
        plugins: [pinia],
        stubs: {
          DsfrBreadcrumb: true,
          RouterLink: { template: '<a><slot /></a>' },
          BlockRenderer: { template: '<div><slot /></div>' },
          BlogArticleModal: true,
        },
      },
    })
    expect(await findByText('Article de test')).toBeInTheDocument()
  })

  it('déclare la vue de page Matomo avec le titre réel de l article', async () => {
    ;(window as any)._paq = []
    ;(api.fetchResource as any).mockResolvedValue(mockArticle)
    const pinia = createTestingPinia({ stubActions: true })
    const { findByText } = render(BlogArticlePage, {
      global: {
        plugins: [pinia],
        stubs: {
          DsfrBreadcrumb: true,
          RouterLink: { template: '<a><slot /></a>' },
          BlockRenderer: { template: '<div><slot /></div>' },
          BlogArticleModal: true,
        },
      },
    })
    await findByText('Article de test')

    const expectedTitle = 'Article de test - Stop Dépôt Sauvage'
    expect(document.title).toBe(expectedTitle)
    expect((window as any)._paq).toContainEqual(['setDocumentTitle', expectedTitle])
    expect((window as any)._paq).toContainEqual(['trackPageView'])
  })

  it('signale un article introuvable plutôt que de rester muet', async () => {
    ;(window as any)._paq = []
    ;(api.fetchResource as any).mockRejectedValue(new Error('404'))
    const pinia = createTestingPinia({ stubActions: true })
    const { findByText } = render(BlogArticlePage, {
      global: {
        plugins: [pinia],
        stubs: {
          DsfrBreadcrumb: true,
          RouterLink: { template: '<a><slot /></a>' },
          BlockRenderer: { template: '<div><slot /></div>' },
          BlogArticleModal: true,
        },
      },
    })
    await findByText('Article introuvable')
    expect((window as any)._paq).toContainEqual([
      'setDocumentTitle',
      'Article introuvable - Stop Dépôt Sauvage',
    ])
  })
})

describe('Normalisation des liens des contenus éditoriaux', () => {
  const parse = (html: string) => {
    const doc = new DOMParser().parseFromString(normalizeRichTextLinks(html), 'text/html')
    return doc.body.querySelector('a') as HTMLAnchorElement
  }

  it('ramène un lien vers le site en navigation interne', () => {
    const link = parse(
      '<p><a target="_blank" rel="noopener noreferrer nofollow" class="fr-link" ' +
        'href="https://stopdepotsauvage.beta.gouv.fr/demarrer-constatation">Démarrer</a></p>'
    )
    expect(link.getAttribute('href')).toBe('/demarrer-constatation')
    expect(link.hasAttribute('target')).toBe(false)
    expect(link.getAttribute('rel')).toBeNull()
    expect(link.getAttribute('data-internal-link')).toBe('true')
    // La classe de style saisie dans l'éditeur est préservée.
    expect(link.classList.contains('fr-link')).toBe(true)
  })

  it('traite aussi les liens vers l autre domaine du site et les liens relatifs', () => {
    expect(toInternalPath('https://protect-envi.beta.gouv.fr/blog/mon-article')).toBe(
      '/blog/mon-article'
    )
    expect(toInternalPath('/faq')).toBe('/faq')
  })

  it('laisse un lien externe s ouvrir dans un nouvel onglet, en le signalant', () => {
    const link = parse('<p><a href="https://www.legifrance.gouv.fr/article">L541-3</a></p>')
    expect(link.getAttribute('target')).toBe('_blank')
    expect(link.getAttribute('rel')).toBe('noopener noreferrer')
    expect(link.getAttribute('title')).toContain('nouvelle fenêtre')
  })

  it('ne touche ni aux ancres ni aux adresses e-mail', () => {
    expect(toInternalPath('#section-2')).toBeNull()
    expect(toInternalPath('mailto:contact@stopdepotsauvage.beta.gouv.fr')).toBeNull()
  })

  it('renvoie le contenu inchangé quand il ne comporte aucun lien', () => {
    const html = '<p>Un texte sans lien.</p>'
    expect(normalizeRichTextLinks(html)).toBe(html)
  })
})

describe('Mesure des clics dans un article', () => {
  beforeEach(() => {
    vi.resetAllMocks()
  })

  it('distingue le clic vers la constatation des autres liens', async () => {
    ;(window as any)._paq = []
    ;(api.fetchResource as any).mockResolvedValue({
      ...mockArticle,
      content: [
        {
          type: 'rich_text',
          value:
            '<p><a href="https://stopdepotsauvage.beta.gouv.fr/demarrer-constatation">Démarrer</a>' +
            '<a href="https://www.legifrance.gouv.fr/article">Légifrance</a></p>',
        },
      ],
    })
    const pinia = createTestingPinia({ stubActions: true })
    const { findByText, getByText } = render(BlogArticlePage, {
      global: {
        plugins: [pinia],
        stubs: {
          DsfrBreadcrumb: true,
          RouterLink: { template: '<a><slot /></a>' },
          BlogArticleModal: true,
        },
      },
    })
    await findByText('Article de test')

    await fireEvent.click(getByText('Démarrer'))
    expect((window as any)._paq).toContainEqual([
      'trackEvent',
      'Blog',
      'Clic vers démarrer une constatation',
      'test-article',
    ])

    await fireEvent.click(getByText('Légifrance'))
    expect(
      (window as any)._paq.some(
        (entry: any[]) => entry[2] === 'Clic lien dans article' && entry[0] === 'trackEvent'
      )
    ).toBe(true)
  })
})
