import '@testing-library/jest-dom'
import { render, screen } from '@testing-library/vue'
import { afterEach, beforeAll, beforeEach, describe, expect, it, vi } from 'vitest'
import { axe } from 'vitest-axe'
import Accompagnement from '../pages/accompagnement.vue'

const replace = vi.fn()
vi.mock('vue-router', () => ({
  useRouter: () => ({
    replace,
  }),
}))

describe('Page Accueil', () => {
  beforeAll(() => {
    HTMLCanvasElement.prototype.getContext = vi.fn()
  })

  beforeEach(() => {
    vi.stubEnv('VITE_CONTACT_EMAIL', 'contact@test.com')

    render(Accompagnement, {
      global: {
        mocks: {
          $router: { replace },
        },
        stubs: {
          DsfrCard: true,
          RouterLink: {
            props: ['to'],
            template: `<a href="to"><slot /></a>`,
          },
        },
      },
    })
  })

  afterEach(() => {
    vi.unstubAllEnvs()
  })

  it('vérifie l’accessibilité de la page', async () => {
    const { container } = render(Accompagnement, {
      global: {
        stubs: { DsfrCard: true },
      },
    })

    const results = await axe(container)
  })

  it('affiche le contenu', async () => {
    expect(
      screen.getByRole('heading', {
        level: 1,
        name: 'Contactez-nous',
      })
    ).toBeInTheDocument()
  })
})
