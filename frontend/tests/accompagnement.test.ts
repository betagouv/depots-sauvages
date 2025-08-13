import { render, screen } from '@testing-library/vue'
import userEvent from '@testing-library/user-event'
import '@testing-library/jest-dom'
import { axe } from 'vitest-axe'
import Accompagnement from '../pages/accompagnement.vue'
import { describe, expect, it, vi, beforeEach, afterEach, beforeAll } from 'vitest'

const replace = vi.fn()
vi.mock('vue-router', () => ({
  useRouter: () => ({
    replace
  })
}))

describe('Page Accueil', () => {
  beforeAll(() => {
    HTMLCanvasElement.prototype.getContext = vi.fn()
  })

  beforeEach(() => {
    vi.stubEnv('VITE_CONTACT_EMAIL', 'contact@test.com')
    vi.stubEnv('VITE_WHATSAPP_LINK', 'http://whatsapp.com/')

    render(Accompagnement, {
      global: {
        mocks: {
          $router: {replace}
        },
        stubs: {
          DsfrCard: true,
          RouterLink: {
            props: ['to'],
            template: `<a href="to"><slot /></a>`
          }
        }
      }
    })

  })

  afterEach(() => {
    vi.unstubAllEnvs()
  })

  it('vérifie l’accessibilité de la page', async () => {
    const { container } = render(Accompagnement, {
      global: {
        stubs: { DsfrCard: true }
      }
    })

    const results = await axe(container)
    console.log(results.violations)
    expect(results.violations).toHaveLength(0)
  })

  it('affiche le contenu', async () => {
    expect(screen.getByRole('heading', {  level: 1, name: 'Un accompagnement personnalisé pour mieux agir'})).toBeInTheDocument()
  })


  it('affiche un lien pour contacter par e-mail', async () => {

    const lienContact = screen.getByRole('link', { name: /envoyer un e-mail/i })
    expect(lienContact).toHaveAttribute('href', 'mailto:contact@test.com')
    await userEvent.click(lienContact)
  })

  it('affiche un lien pour contacter par WhatsApp', async () => {

    const lienWhatsApp = screen.getByRole('link', { name: /démarrer une conversation/i })
    expect(lienWhatsApp).toHaveAttribute('href', 'http://whatsapp.com/')
    await userEvent.click(lienWhatsApp)
  })
})
