import { render, screen } from '@testing-library/vue'
import userEvent from '@testing-library/user-event'
import '@testing-library/jest-dom'
import { axe } from 'vitest-axe'
import Accueil from '../pages/accueil.vue'
import { describe, expect, it, vi } from 'vitest'

const replace = vi.fn()
vi.mock('vue-router', () => ({
  useRouter: () => ({
    replace
  })
}))

describe('Page Accueil', () => {
  it('vérifie l’accessibilité de la page', async () => {
    const { container } = render(Accueil, {
      global: {
        stubs: { DsfrCard: true }
      }
    })

    const results = await axe(container)
    expect(results.violations).toHaveLength(0)
  })

  it('redirige vers la page "Débuter une procédure" au clic', async () => {
    render(Accueil, {
      global: {
        mocks: {
          $router: {replace}
        },
        stubs: {
          DsfrCard: true,
          RouterLink: {
            props: ['to'],
            template: `<a href="#" @click.prevent="$router.replace(to)"><slot /></a>`
          }
        }
      }
    })

    await userEvent.click(
      screen.getByRole('link', { name: /débuter une procédure/i })
    )

    expect(replace).toHaveBeenCalledWith('/debuter-procedure')
  })
})
