import '@testing-library/jest-dom'
import { render, screen } from '@testing-library/vue'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { axe } from 'vitest-axe'
import Contact from '../pages/contact.vue'

const replace = vi.fn()
vi.mock('vue-router', () => ({
  useRouter: () => ({
    replace,
  }),
}))

describe('Page Contact', () => {
  beforeEach(() => {
    vi.stubEnv('VITE_CONTACT_EMAIL', 'contact@test.com')

    render(Contact, {
      global: {
        mocks: {
          $router: { replace },
        },
        stubs: {
          DsfrCard: true,
          DsfrCallout: true,
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

  it('doit être accessible (A11y)', async () => {
    const { container } = render(Contact, {
      global: {
        stubs: {
          DsfrCard: true,
          DsfrCallout: true,
        },
      },
    })

    const results = await axe(container)
  })

  it('doit afficher le titre principal', async () => {
    expect(
      screen.getByRole('heading', {
        level: 1,
        name: 'Contactez-nous',
      })
    ).toBeInTheDocument()
  })
})
