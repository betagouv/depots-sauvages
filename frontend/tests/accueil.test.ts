import { createTestingPinia } from '@pinia/testing'
import '@testing-library/jest-dom'
import { render } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { axe } from 'vitest-axe'
import Accueil from '../pages/accueil.vue'
import * as api from '../services/api'

vi.mock('vue-router', () => ({
  useRoute: () => ({
    path: '/',
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
  }
})

describe('Page Accueil', () => {
  beforeEach(() => {
    vi.resetAllMocks()
    ;(api.fetchResource as any).mockResolvedValue(null)
  })

  it('doit être accessible (A11y)', async () => {
    const pinia = createTestingPinia({ stubActions: true })
    const { container } = render(Accueil, {
      global: {
        plugins: [pinia],
        stubs: {
          DsfrCard: true,
          DsfrNotice: true,
          DsfrPicture: true,
          DsfrCallout: true,
          RouterLink: true,
          DsfrModal: true,
        },
      },
    })

    const results = await axe(container)
    expect(results.violations).toHaveLength(0)
  })
})
