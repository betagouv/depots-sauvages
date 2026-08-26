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
})
