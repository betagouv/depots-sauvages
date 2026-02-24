import { createTestingPinia } from '@pinia/testing'
import '@testing-library/jest-dom'
import { render, screen, waitFor } from '@testing-library/vue'
import { describe, expect, it, vi } from 'vitest'
import MesDossiers from '../pages/mes-dossiers.vue'
import * as api from '../services/api'
import { useDossierStore } from '../stores/dossier'

vi.mock('../services/api', async () => {
  const actual = await vi.importActual('../services/api')
  return {
    ...actual,
    getUserInfo: vi.fn(),
  }
})

const push = vi.fn()
vi.mock('vue-router', () => ({
  useRouter: () => ({
    push,
  }),
}))

describe('Page Mes Dossiers', () => {
  it('doit afficher l’identité de l’utilisateur connecté', async () => {
    // Mock user info
    ;(api.getUserInfo as any).mockResolvedValue({
      is_authenticated: true,
      proconnect_enabled: true,
      first_name: 'Jean',
      last_name: 'Dupont',
      email: 'jean.dupont@example.com',
    })

    const pinia = createTestingPinia({ stubActions: true })

    render(MesDossiers, {
      global: {
        plugins: [pinia],
        stubs: {
          DsfrCard: true,
          DsfrButton: true,
          DsfrAlert: {
            props: ['title', 'description'],
            template: '<div>{{ title }} {{ description }}</div>',
          },
          DnLoading: true,
        },
      },
    })

    await waitFor(() => {
      // Use findByText which is more robust and handles normalized whitespace
      expect(screen.getByText('Jean Dupont')).toBeInTheDocument()
      // Correct the email expectation to match the component: " - jean.dupont@example.com"
      expect(screen.getByText(/jean\.dupont@example\.com/)).toBeInTheDocument()
    })
  })

  it('doit rester stable si l’utilisateur n’est pas connecté', async () => {
    // Mock unauthenticated or null
    ;(api.getUserInfo as any).mockResolvedValue({
      is_authenticated: false,
      proconnect_enabled: true,
    })

    render(MesDossiers, {
      global: {
        plugins: [createTestingPinia({ stubActions: true })],
        stubs: {
          DsfrCard: true,
          DsfrButton: true,
          DsfrAlert: {
            props: ['title', 'description'],
            template: '<div>{{ title }} {{ description }}</div>',
          },
          DnLoading: true,
        },
      },
    })

    // Wait for the finally block of onMounted to set showLoading to false
    await waitFor(() => {
      expect(screen.queryByText('Jean Dupont')).not.toBeInTheDocument()
      expect(screen.getByRole('heading', { level: 1, name: 'Mes procédures' })).toBeInTheDocument()
    })
  })

  it('doit afficher un message d’information quand aucun dossier n’est trouvé', async () => {
    // Mock user info authenticated
    ;(api.getUserInfo as any).mockResolvedValue({
      is_authenticated: true,
      proconnect_enabled: true,
      first_name: 'Jean',
      last_name: 'Dupont',
    })

    const pinia = createTestingPinia({ stubActions: true })
    const dossierStore = useDossierStore(pinia)
    dossierStore.dossiers = []

    render(MesDossiers, {
      global: {
        plugins: [pinia],
        stubs: {
          DsfrCard: true,
          DsfrButton: true,
          DsfrAlert: {
            props: ['title', 'description'],
            template: '<div>{{ title }} {{ description }}</div>',
          },
          DnLoading: true,
        },
      },
    })

    await waitFor(() => {
      expect(screen.getByText(/Aucune procédure trouvée/)).toBeInTheDocument()
      expect(
        screen.getByText(/Aucune procédure trouvée sur Démarche Numérique\./)
      ).toBeInTheDocument()
    })
  })
})
