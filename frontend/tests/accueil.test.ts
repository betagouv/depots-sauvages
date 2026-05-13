import '@testing-library/jest-dom'
import { render } from '@testing-library/vue'
import { describe, expect, it, vi } from 'vitest'
import { axe } from 'vitest-axe'
import Accueil from '../pages/accueil.vue'

vi.mock('vue-router', () => ({
  useRoute: () => ({
    path: '/',
  }),
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn(),
  }),
}))

describe('Page Accueil', () => {
  it('doit être accessible (A11y)', async () => {
    const { container } = render(Accueil, {
      global: {
        stubs: {
          DsfrCard: true,
          DsfrNotice: true,
          DsfrPicture: true,
          DsfrCallout: true,
          RouterLink: true,
        },
      },
    })

    const results = await axe(container)
    expect(results.violations).toHaveLength(0)
  })
})
