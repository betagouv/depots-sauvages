import { createTestingPinia } from '@pinia/testing'
import '@testing-library/jest-dom'
import { render, screen, waitFor, within } from '@testing-library/vue'
import { describe, expect, it, vi } from 'vitest'
import { axe } from 'vitest-axe'
import VueDsfr from '@gouvminint/vue-dsfr'
import { fireEvent } from '@testing-library/vue'
import MesProcedures from '../pages/mes-procedures.vue'
import * as api from '../services/api'
import { useProcedureStore } from '../stores/procedure'

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

describe('Page Mes Procédures', () => {
  it('n’affiche plus l’identité de l’utilisateur (prévue dans le bandeau du site)', async () => {
    // Mock user info
    ;(api.getUserInfo as any).mockResolvedValue({
      is_authenticated: true,
      proconnect_enabled: true,
      first_name: 'Jean',
      last_name: 'Dupont',
      email: 'jean.dupont@example.com',
    })

    const pinia = createTestingPinia({ stubActions: true })

    render(MesProcedures, {
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
          VIcon: true,
        },
      },
    })

    // Wait until loading finishes before asserting absence
    await screen.findByText(/Aucune procédure en cours/)
    expect(screen.queryByText(/Jean/)).not.toBeInTheDocument()
    expect(screen.queryByText(/jean\.dupont@example\.com/)).not.toBeInTheDocument()
  })

  it('doit rester stable si l’utilisateur n’est pas connecté', async () => {
    // Mock unauthenticated or null
    ;(api.getUserInfo as any).mockResolvedValue({
      is_authenticated: false,
      proconnect_enabled: true,
    })

    render(MesProcedures, {
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
          VIcon: true,
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
    const procedureStore = useProcedureStore(pinia)
    procedureStore.procedures = []

    render(MesProcedures, {
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
          VIcon: true,
        },
      },
    })
    await waitFor(() => {
      expect(screen.getByText(/Aucune procédure en cours/)).toBeInTheDocument()
      expect(
        screen.getByText(
          /Vous n'avez pas encore créé de constatation pour initier une procédure administrative/
        )
      ).toBeInTheDocument()
    })
  })

  describe('Tableau de bord en colonnes', () => {
    const procedures = [
      {
        id: 10,
        commune: 'Nangy',
        date_modification: null,
        date_constat: '2026-09-01',
        heure_constat: null,
        localisation_depot: 'Chemin des Saules',
        auteur_identifie: true,
        auteur_nom: 'Dupont',
        auteur_prenom: 'Marc',
        is_draft: false,
        suivi_procedure: {
          etape_en_cours: 1,
          preuves_fournies: true,
          constatation_signee: true,
          lettre_signe: true,
        },
      },
      {
        id: 11,
        commune: 'Reignier-Ésery',
        date_modification: null,
        date_constat: '2026-09-05',
        heure_constat: null,
        localisation_depot: null,
        auteur_identifie: true,
        auteur_nom: 'Martin',
        auteur_prenom: 'Lucie',
        is_draft: false,
        suivi_procedure: { etape_en_cours: 1 },
      },
      {
        id: 12,
        commune: 'Nangy',
        date_modification: null,
        date_constat: '2026-06-01',
        heure_constat: null,
        localisation_depot: null,
        auteur_identifie: true,
        auteur_nom: 'Blanc',
        auteur_prenom: 'Sarah',
        is_draft: false,
        suivi_procedure: {
          etape_en_cours: 5,
          preuves_fournies: true,
          constatation_signee: true,
          lettre_signe: true,
          lettre_envoyee: true,
          copie_archives: true,
          ar_recu: true,
          ar_statut: 'distribue',
          ar_presentation_date: '2026-06-10',
          decision_poursuite: 'abandon',
          motif_abandon: 'Indulgence',
          souhaite_notifier_abandon: false,
        },
      },
    ]

    const renderTableau = () => {
      ;(api.getUserInfo as any).mockResolvedValue({
        is_authenticated: true,
        proconnect_enabled: true,
      })
      const pinia = createTestingPinia({ stubActions: true })
      useProcedureStore(pinia).procedures = procedures as any
      return render(MesProcedures, {
        global: {
          plugins: [pinia, VueDsfr],
          stubs: {
            RouterLink: { props: ['to'], template: '<a :href="to"><slot /></a>' },
          },
        },
      })
    }

    it('range chaque dossier dans sa colonne et masque les clôturés', async () => {
      renderTableau()
      const colonne = await screen.findByRole('region', { name: /Lettre à envoyer/ })
      expect(colonne).toHaveTextContent('Marc Dupont')
      expect(screen.getByRole('region', { name: /Documents à signer/ })).toHaveTextContent(
        'Lucie Martin'
      )
      expect(screen.queryByText('Sarah Blanc')).not.toBeInTheDocument()

      await fireEvent.click(screen.getByLabelText(/Afficher les dossiers clôturés \(1\)/))
      expect(screen.getByRole('region', { name: /Clôturé/ })).toHaveTextContent('Issue : Abandon')
    })

    it('cumule la recherche et l’interrupteur des dossiers clôturés', async () => {
      renderTableau()
      const champ = await screen.findByRole('searchbox')
      await fireEvent.update(champ, 'blanc')
      expect(screen.queryByText('Sarah Blanc')).not.toBeInTheDocument()
      expect(
        screen.getByText(
          /1 dossier clôturé correspond : activez « Afficher les dossiers clôturés » pour le voir\./
        )
      ).toBeInTheDocument()

      await fireEvent.click(screen.getByLabelText(/Afficher les dossiers clôturés/))
      expect(screen.getByText('Sarah Blanc')).toBeInTheDocument()
    })

    it('affiche le lieu du dépôt suivi de la commune, sans ambiguïté avec l’adresse de l’auteur', async () => {
      renderTableau()
      expect(await screen.findByText('Dépôt : Chemin des Saules – Nangy')).toBeInTheDocument()
      expect(screen.getByText('Dépôt : Reignier-Ésery')).toBeInTheDocument()
      expect(screen.getByText(/n°10 · Constat du 01\/09\/2026/)).toBeInTheDocument()
    })

    it('filtre les dossiers par nom du contrevenant', async () => {
      renderTableau()
      const champ = await screen.findByRole('searchbox')
      await fireEvent.update(champ, 'dupont')
      expect(screen.getByText('Marc Dupont')).toBeInTheDocument()
      expect(screen.queryByText('Lucie Martin')).not.toBeInTheDocument()
    })

    it('rend toute la carte cliquable, avec un seul lien au nom complet', async () => {
      renderTableau()
      const colonne = await screen.findByRole('region', { name: /Lettre à envoyer/ })
      const liens = within(colonne).getAllByRole('link')
      expect(liens).toHaveLength(1)
      expect(liens[0]).toHaveAccessibleName(
        'Particulier : Marc Dupont, dossier n°10. Marquer comme envoyé'
      )
      expect(liens[0]).toHaveAttribute('href', '/suivi-procedure/10?etape=2')
      // Action verb is also displayed at the bottom of the card
      expect(colonne).toHaveTextContent('Marquer comme envoyé')
    })

    it('est accessible (A11y)', async () => {
      const { container } = renderTableau()
      await screen.findByRole('region', { name: /Lettre à envoyer/ })
      const results = await axe(container)
      expect(results.violations).toEqual([])
    })
  })
})
