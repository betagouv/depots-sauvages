import { render, screen } from '@testing-library/vue'
import userEvent from '@testing-library/user-event'
import '@testing-library/jest-dom'
import { axe } from 'vitest-axe'
import IntroductionFormulaire from '../pages/introduction-formulaire.vue'
import { describe, expect, it, vi, beforeEach, afterEach, beforeAll } from 'vitest'
import { createTestingPinia } from '@pinia/testing'
import {useSignalementStore} from '../stores/signalement'

const push = vi.fn()
vi.mock('vue-router', () => ({
  useRouter: () => ({
    push
  })
}))

let store: ReturnType<typeof useSignalementStore>

describe('Page Introduction formulaire procédure', () => {

  beforeAll(() => {
    HTMLCanvasElement.prototype.getContext = vi.fn()
  })

  beforeEach(() => {
    render(IntroductionFormulaire, {
      global: {
        plugins: [createTestingPinia({ createSpy: vi.fn, stubActions: true })],
        mocks: {
          $router: {push}
        },
        stubs: {
          DsfrCard: true,
          DsfrCallout: true,
          VIcon: true,
          RouterLink: {
            props: ['to'],
            template: `<a href="#" @click.prevent="$router.push(to)"><slot /></a>`
          }
        }
      }
    })

    store = useSignalementStore()
  })

  afterEach(() => {
    vi.clearAllMocks()
    vi.unstubAllEnvs()
  })

  it('vérifie l’accessibilité de la page', async () => {
    const { container } = render(IntroductionFormulaire, {
      global: {
        stubs: {
          DsfrCard: true,
          RouterLink: {
            props: ['to'],
            template: `<a :href="to"><slot /></a>`
          }
        }
      }
    })

    const results = await axe(container)
    expect(results.violations).toHaveLength(0)
  })

  it('affiche le contenu', async () => {
    expect(screen.getByRole('heading', {  level: 1, name: 'Commencer la procédure'})).toBeInTheDocument()
  })

  it('redirige vers la première étape du formulaire', async () => {
    await userEvent.click(
      screen.getByRole('link', { name: /démarrez la procédure/i })
    )

    expect(push).toHaveBeenCalledWith('/debuter-procedure/formulaire')
  })

})
