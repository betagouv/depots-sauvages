import { createTestingPinia } from '@pinia/testing'
import '@testing-library/jest-dom'
import { render, screen } from '@testing-library/vue'
import { nextTick, reactive } from 'vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import DefaultLayout from '../layouts/default-layout.vue'

const route = reactive({ fullPath: '/', meta: {} as Record<string, unknown> })
const router = {
  resolve: vi.fn((to: string) => ({ href: to, meta: {} })),
}
vi.mock('vue-router', () => ({
  useRoute: () => route,
  useRouter: () => router,
}))

vi.mock('../services/api', async () => ({
  ...(await vi.importActual('../services/api')),
  getBypassAuthConfig: vi.fn().mockResolvedValue({ enabled: false }),
  getUserInfo: vi.fn().mockResolvedValue({ is_authenticated: false }),
}))

const renderLayout = () =>
  render(DefaultLayout, {
    global: {
      plugins: [createTestingPinia({ stubActions: true })],
      stubs: { DsfrHeader: true, DsfrFooter: true },
    },
  })

describe('Gabarit par défaut - liens d’évitement', () => {
  beforeEach(() => {
    route.meta = {}
  })

  it('propose d’aller au contenu, au menu et au pied de page', () => {
    renderLayout()

    expect(screen.getByRole('link', { name: 'Contenu' })).toHaveAttribute('href', '#content')
    expect(screen.getByRole('link', { name: 'Menu' })).toHaveAttribute('href', '#main-navigation')
    expect(screen.getByRole('link', { name: 'Pied de page' })).toHaveAttribute('href', '#footer')
  })

  it('ne propose pas le lien vers le menu sur une page sans menu', () => {
    route.meta = { hideNavigation: true }
    renderLayout()

    expect(screen.getByRole('link', { name: 'Contenu' })).toBeInTheDocument()
    expect(screen.queryByRole('link', { name: 'Menu' })).not.toBeInTheDocument()
  })

  it('rend la zone principale focalisable pour le lien « Contenu »', () => {
    renderLayout()

    expect(screen.getByRole('main')).toHaveAttribute('tabindex', '-1')
  })
})

describe('Gabarit par défaut - lien de connexion', () => {
  it('ramène sur la page en cours après la connexion, même après une navigation', async () => {
    route.fullPath = '/'
    route.meta = {}
    const api = await import('../services/api')
    vi.mocked(api.getBypassAuthConfig).mockResolvedValueOnce({ enabled: true })
    render(DefaultLayout, {
      global: {
        plugins: [createTestingPinia({ stubActions: false })],
        stubs: {
          DsfrHeader: {
            props: ['quickLinks'],
            template:
              '<div><a v-for="link in quickLinks" :key="link.label" :href="link.href">{{ link.label }}</a></div>',
          },
          DsfrFooter: true,
        },
      },
    })

    const demoLink = await screen.findByRole('link', { name: 'Connexion de démo' })
    expect(demoLink).toHaveAttribute('href', '/login-demo?next=%2Fmes-procedures')

    route.fullPath = '/se-preparer'
    await nextTick()
    expect(screen.getByRole('link', { name: 'Connexion de démo' })).toHaveAttribute(
      'href',
      '/login-demo?next=%2Fse-preparer'
    )
  })
})

describe('Gabarit par défaut - en-tête et pied de page', () => {
  it('affiche le nom du service "Stop Dépôt Sauvage" sans Protect\'Envi', () => {
    render(DefaultLayout, {
      global: {
        plugins: [createTestingPinia({ stubActions: true })],
        stubs: {
          DsfrHeader: {
            props: ['serviceTitle'],
            template: '<header data-testid="header">{{ serviceTitle }}</header>',
          },
          DsfrFooter: {
            template: '<footer><slot name="description" /></footer>',
          },
        },
      },
    })

    const header = screen.getByTestId('header')
    expect(header).toHaveTextContent('Stop Dépôt Sauvage')
    expect(header).not.toHaveTextContent("Protect'Envi")

    const footer = screen.getByRole('contentinfo')
    expect(footer).toHaveTextContent('Stop Dépôt Sauvage')
    expect(footer).not.toHaveTextContent("Protect'Envi")
  })
})
