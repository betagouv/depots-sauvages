import { createTestingPinia } from '@pinia/testing'
import '@testing-library/jest-dom'
import { render, screen } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import DefaultLayout from '../layouts/default-layout.vue'

const route = { fullPath: '/', meta: {} as Record<string, unknown> }
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
