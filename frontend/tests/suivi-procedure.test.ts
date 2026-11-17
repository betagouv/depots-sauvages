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
    patchResource: vi.fn(),
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

  describe('Séquentialité et verrouillage des étapes', () => {
    it('débloque l’étape 1 initialement et verrouille les étapes suivantes si l’étape 1 n’est pas complète', async () => {
      ;(api.getUserInfo as any).mockResolvedValue({ is_authenticated: true })
      ;(api.fetchResource as any).mockImplementation((url: string) => {
        if (url.includes('/suivi-procedure/')) {
          return Promise.resolve({
            etape_en_cours: 2,
            preuves_fournies: false,
            constatation_signee: false,
            lettre_signe: false,
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

      let capturedSteps: any[] = []
      const stubs = {
        StepperProcedure: {
          props: ['steps', 'currentStep'],
          template: '<div data-testid="stepper"><slot :name="`step-${currentStep}`" :locked="steps[currentStep]?.locked" /></div>',
          mounted() {
            capturedSteps = (this as any).steps
          },
        },
        Chargement: true,
        LoginInvitation: true,
        DsfrBadge: true,
        DsfrButton: true,
        Metadata: true,
        InfosComplementaires: true,
        Notification: {
          props: ['disabled'],
          template: '<div data-testid="notification-step" :data-disabled="disabled" />',
        },
      }

      render(SuiviProcedurePage, {
        global: { plugins: [createTestingPinia({ stubActions: false })], stubs },
      })

      await waitFor(() => {
        expect(screen.getByTestId('notification-step')).toBeInTheDocument()
      })

      // Étape 1 est débloquée
      expect(capturedSteps[1].locked).toBe(false)
      // Étape 2 est verrouillée car étape 1 non complétée
      expect(capturedSteps[2].locked).toBe(true)
      expect(screen.getByTestId('notification-step')).toHaveAttribute('data-disabled', 'true')
    })
  })

  describe('Store Suivi - Verrouillage Optimiste & Conflits Concurrence (HTTP 409)', () => {
    it('enregistre lastSyncedModified lors du fetchSuivi', async () => {
      const { useSuiviStore } = await import('../stores/suivi-procedure')
      const pinia = createTestingPinia({ stubActions: false })
      const store = useSuiviStore(pinia)

      vi.spyOn(api, 'fetchResource').mockResolvedValue({
        id: 163,
        modified: '2026-11-16T12:00:00Z',
        etape_en_cours: 2,
      })

      await store.fetchSuivi('163', 163)

      expect(store.lastSyncedModified['163']).toBe('2026-11-16T12:00:00Z')
      expect(store.conflictModalVisible).toBe(false)
      expect(store.conflictDetails).toBeNull()
    })

    it('envoie last_synced_modified lors de saveSuivi', async () => {
      const { useSuiviStore } = await import('../stores/suivi-procedure')
      const pinia = createTestingPinia({ stubActions: false })
      const store = useSuiviStore(pinia)

      store.getOrCreateSuivi('163')
      store.lastSyncedModified['163'] = '2026-11-16T12:00:00Z'

      vi.spyOn(api, 'patchResource').mockResolvedValue({
        id: 163,
        modified: '2026-11-16T12:05:00Z',
      })

      await store.saveSuivi('163', 163)

      expect(api.patchResource).toHaveBeenCalledWith(
        expect.stringContaining('/suivi-procedure/163/'),
        expect.objectContaining({
          last_synced_modified: '2026-11-16T12:00:00Z',
        })
      )
      expect(store.lastSyncedModified['163']).toBe('2026-11-16T12:05:00Z')
    })

    it('gère une réponse HTTP 409 sur saveSuivi', async () => {
      const { useSuiviStore } = await import('../stores/suivi-procedure')
      const pinia = createTestingPinia({ stubActions: false })
      const store = useSuiviStore(pinia)

      store.getOrCreateSuivi('163')
      store.lastSyncedModified['163'] = '2026-11-16T12:00:00Z'

      const conflictError = {
        error: 'CONCURRENT_MODIFICATION',
        message: 'Ce dossier a été modifié par Alice MARTIN entre-temps.',
        updated_by: 'Alice MARTIN',
        server_modified: '2026-11-16T12:05:00Z',
      }
      vi.spyOn(api, 'patchResource').mockRejectedValue(conflictError)

      await expect(store.saveSuivi('163', 163)).rejects.toEqual(conflictError)

      expect(store.conflictBannerVisible).toBe(true)
      expect(store.conflictDetails).toEqual({
        updatedBy: 'Alice MARTIN',
        message: 'Ce dossier a été modifié par Alice MARTIN entre-temps.',
        serverModified: '2026-11-16T12:05:00Z',
      })
    })

    it('permet de forcer la mise à jour via forceSave', async () => {
      const { useSuiviStore } = await import('../stores/suivi-procedure')
      const pinia = createTestingPinia({ stubActions: false })
      const store = useSuiviStore(pinia)

      store.getOrCreateSuivi('163')
      store.conflictModalVisible = true
      store.conflictDetails = {
        updatedBy: 'Alice MARTIN',
        message: 'Conflit',
        serverModified: '2026-11-16T12:05:00Z',
      }

      vi.spyOn(api, 'patchResource').mockResolvedValue({
        id: 163,
        modified: '2026-11-16T12:10:00Z',
      })

      await store.forceSave('163', 163)

      expect(api.patchResource).toHaveBeenCalledWith(
        expect.stringContaining('/suivi-procedure/163/'),
        expect.objectContaining({
          force: true,
        })
      )
      expect(store.conflictModalVisible).toBe(false)
      expect(store.conflictDetails).toBeNull()
      expect(store.lastSyncedModified['163']).toBe('2026-11-16T12:10:00Z')
    })

    it('permet de recharger le suivi serveur via resolveConflictReload', async () => {
      const { useSuiviStore } = await import('../stores/suivi-procedure')
      const pinia = createTestingPinia({ stubActions: false })
      const store = useSuiviStore(pinia)

      store.conflictModalVisible = true
      store.conflictDetails = {
        updatedBy: 'Alice MARTIN',
        message: 'Conflit',
        serverModified: '2026-11-16T12:05:00Z',
      }

      vi.spyOn(api, 'fetchResource').mockResolvedValue({
        id: 163,
        modified: '2026-11-16T12:05:00Z',
        etape_en_cours: 3,
      })

      await store.resolveConflictReload('163', 163)

      expect(api.fetchResource).toHaveBeenCalledWith(expect.stringContaining('/suivi-procedure/163/'))
      expect(store.procedures['163'].etape_en_cours).toBe(3)
      expect(store.lastSyncedModified['163']).toBe('2026-11-16T12:05:00Z')
      expect(store.conflictModalVisible).toBe(false)
      expect(store.conflictDetails).toBeNull()
    })
  })
})
