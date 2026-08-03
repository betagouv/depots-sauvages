import { createTestingPinia } from '@pinia/testing'
import '@testing-library/jest-dom'
import { render, screen, waitFor } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import SuiviProcedurePage from '../pages/suivi-procedure.vue'
import * as api from '../services/api'
import * as tally from '../utils/tally'

vi.mock('../services/api', async () => {
  const actual = await vi.importActual('../services/api')
  return {
    ...actual,
    getUserInfo: vi.fn(),
    fetchResource: vi.fn(),
  }
})

vi.mock('../utils/tally', async () => {
  const actual = await vi.importActual('../utils/tally')
  return {
    ...actual,
    openTallyPopup: vi.fn(),
  }
})

const pushMock = vi.fn()
const routeParams = { constatation_id: '163' }
vi.mock('vue-router', () => ({
  useRoute: () => ({
    params: routeParams,
    query: {},
  }),
  useRouter: () => ({
    push: pushMock,
  }),
}))

describe('Page Suivi de Procédure', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    routeParams.constatation_id = '163'
  })

  it('doit charger et afficher le titre avec le numéro de procédure', async () => {
    ;(api.getUserInfo as any).mockResolvedValue({ is_authenticated: true })
    ;(api.fetchResource as any).mockResolvedValue({
      id: 163,
      created: true,
      auteur_identifie: true,
      commune: 'Amiens',
      date_constat: '2026-03-27',
    })

    const pinia = createTestingPinia({ stubActions: false })

    render(SuiviProcedurePage, {
      global: {
        plugins: [pinia],
        stubs: {
          StepperProcedure: {
            props: ['steps', 'currentStep'],
            template: '<div data-testid="stepper"><slot :name="`step-${currentStep}`" /></div>',
          },
          Chargement: true,
          LoginInvitation: true,
          DsfrBadge: true,
          DsfrButton: true,
          Metadata: true,
          InfosComplementaires: true,
          Notification: {
            props: ['lettreInfoUrl'],
            template: '<div data-testid="notification-step">{{ lettreInfoUrl }}</div>',
          },
        },
      },
    })

    await waitFor(() => {
      expect(screen.getByText('Procédure #163')).toBeInTheDocument()
    })
  })

  it("doit rendre l'étape 2 (Notification) correctement sans planter quand l'auteur est identifié", async () => {
    ;(api.getUserInfo as any).mockResolvedValue({ is_authenticated: true })
    ;(api.fetchResource as any).mockImplementation((url: string) => {
      if (url.includes('/suivi-procedure/')) {
        return Promise.resolve({
          etape_en_cours: 2,
          lettre_envoyee: false,
          copie_archives: false,
          ar_recu: false,
        })
      }
      return Promise.resolve({
        id: 163,
        created: true,
        auteur_identifie: true,
        commune: 'Amiens',
        date_constat: '2026-03-27',
      })
    })

    const pinia = createTestingPinia({ stubActions: false })

    render(SuiviProcedurePage, {
      global: {
        plugins: [pinia],
        stubs: {
          StepperProcedure: {
            props: ['steps', 'currentStep'],
            template: '<div data-testid="stepper"><slot :name="`step-${currentStep}`" /></div>',
          },
          Chargement: true,
          LoginInvitation: true,
          DsfrBadge: true,
          DsfrButton: true,
          Metadata: true,
          InfosComplementaires: true,
          Notification: {
            props: ['lettreInfoUrl'],
            template: '<div data-testid="notification-step">Lettre: {{ lettreInfoUrl }}</div>',
          },
        },
      },
    })

    await waitFor(() => {
      expect(screen.getByTestId('notification-step')).toHaveTextContent(
        '/api/constatations/163/documents/lettre-info/'
      )
    })
  })

  it("doit rendre l'étape 2 (Identification) correctement quand l'auteur n'est pas identifié", async () => {
    ;(api.getUserInfo as any).mockResolvedValue({ is_authenticated: true })
    ;(api.fetchResource as any).mockImplementation((url: string) => {
      if (url.includes('/suivi-procedure/')) {
        return Promise.resolve({
          etape_en_cours: 2,
          identification_reussie: null,
        })
      }
      return Promise.resolve({
        id: 163,
        created: true,
        auteur_identifie: false,
        commune: 'Amiens',
        date_constat: '2026-03-27',
      })
    })

    const pinia = createTestingPinia({ stubActions: false })

    render(SuiviProcedurePage, {
      global: {
        plugins: [pinia],
        stubs: {
          StepperProcedure: {
            props: ['steps', 'currentStep'],
            template: '<div data-testid="stepper"><slot :name="`step-${currentStep}`" /></div>',
          },
          Chargement: true,
          LoginInvitation: true,
          DsfrBadge: true,
          DsfrButton: true,
          Metadata: true,
          InfosComplementaires: true,
          Identification: {
            template: '<div data-testid="identification-step">Identification en cours</div>',
          },
        },
      },
    })

    await waitFor(() => {
      expect(screen.getByTestId('identification-step')).toBeInTheDocument()
    })
  })

  describe('Popup de mesure d’utilité (lettre d’information envoyée)', () => {
    const stubs = {
      StepperProcedure: {
        props: ['steps', 'currentStep'],
        template: '<div data-testid="stepper"><slot :name="`step-${currentStep}`" /></div>',
      },
      Chargement: true,
      LoginInvitation: true,
      DsfrBadge: true,
      DsfrButton: true,
      Metadata: true,
      InfosComplementaires: true,
      Notification: {
        props: ['lettreInfoUrl'],
        template: '<div data-testid="notification-step" />',
      },
    }

    const mockFetch = (constatationOverrides: Record<string, unknown> = {}) => {
      ;(api.fetchResource as any).mockImplementation((url: string) => {
        if (url.includes('/suivi-procedure/')) {
          return Promise.resolve({ etape_en_cours: 2, lettre_envoyee: true })
        }
        return Promise.resolve({
          id: 163,
          created: true,
          auteur_identifie: true,
          commune: 'Amiens',
          date_constat: '2026-03-27',
          ...constatationOverrides,
        })
      })
    }

    it('ouvre le popup Tally quand la lettre est envoyée sur un vrai dossier', async () => {
      ;(api.getUserInfo as any).mockResolvedValue({ is_authenticated: true })
      mockFetch({ ceci_est_un_test: false })

      render(SuiviProcedurePage, {
        global: { plugins: [createTestingPinia({ stubActions: false })], stubs },
      })

      await waitFor(() => {
        expect(tally.openTallyPopup).toHaveBeenCalledWith(
          'OD9RMg',
          expect.objectContaining({
            layout: 'default',
            doNotShowAfterSubmit: true,
            hideTitle: true,
            autoClose: 2000,
          })
        )
      })
    })

    it("n'ouvre pas le popup Tally sur un dossier de test", async () => {
      ;(api.getUserInfo as any).mockResolvedValue({ is_authenticated: true })
      mockFetch({ ceci_est_un_test: true })

      render(SuiviProcedurePage, {
        global: { plugins: [createTestingPinia({ stubActions: false })], stubs },
      })

      await waitFor(() => {
        expect(screen.getByTestId('notification-step')).toBeInTheDocument()
      })
      expect(tally.openTallyPopup).not.toHaveBeenCalled()
    })

    it("n'ouvre pas le popup Tally tant que la lettre n'a pas été envoyée", async () => {
      ;(api.getUserInfo as any).mockResolvedValue({ is_authenticated: true })
      ;(api.fetchResource as any).mockImplementation((url: string) => {
        if (url.includes('/suivi-procedure/')) {
          return Promise.resolve({ etape_en_cours: 2, lettre_envoyee: false })
        }
        return Promise.resolve({
          id: 163,
          created: true,
          auteur_identifie: true,
          commune: 'Amiens',
          date_constat: '2026-03-27',
          ceci_est_un_test: false,
        })
      })

      render(SuiviProcedurePage, {
        global: { plugins: [createTestingPinia({ stubActions: false })], stubs },
      })

      await waitFor(() => {
        expect(screen.getByTestId('notification-step')).toBeInTheDocument()
      })
      expect(tally.openTallyPopup).not.toHaveBeenCalled()
    })
  })
})
