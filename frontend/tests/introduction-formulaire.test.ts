import { render, screen } from '@testing-library/vue'
import userEvent from '@testing-library/user-event'
import '@testing-library/jest-dom'
import { axe } from 'vitest-axe'
import DebuterProcedure from '../pages/debuter-procedure.vue'
import { describe, expect, it, vi, beforeEach, afterEach, beforeAll } from 'vitest'
import { createTestingPinia } from '@pinia/testing'
import {useSignalementStore} from '../stores/signalement'

const replace = vi.fn()
vi.mock('vue-router', () => ({
  useRouter: () => ({
    replace
  })
}))

let store: ReturnType<typeof useSignalementStore>

describe('Page Débuter procédure', () => {

  beforeAll(() => {
    HTMLCanvasElement.prototype.getContext = vi.fn()
  })

  beforeEach(() => {
    render(DebuterProcedure, {
      global: {
        plugins: [createTestingPinia({ createSpy: vi.fn, stubActions: true })],
        mocks: {
          $router: {replace}
        },
        stubs: {
          DsfrCard: true,
          DsfrCallout: true,
          DsfrStepper: true,
          DsfrButton: true,
          VIcon: true,
          RouterLink: {
            props: ['to'],
            template: `<a href="#" @click.prevent="$router.replace(to)"><slot /></a>`
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
    const { container } = render(DebuterProcedure, {
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

  it('redirige vers la première étape du formulaire', async () => {
    await userEvent.click(
      screen.getByRole('link', { name: /débuter une procédure/i })
    )

    expect(replace).toHaveBeenCalledWith('/debuter-procedure/procedure')
  })

})
