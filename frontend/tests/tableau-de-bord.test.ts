import dayjs from 'dayjs'
import { describe, expect, it } from 'vitest'
import type { ProcedureOverview } from '../services/api'
import {
  comparerDansColonne,
  comparerProcedures,
  correspondRecherche,
  getPlacementProcedure,
} from '../utils/tableau-de-bord'

const ilYA = (jours: number) => dayjs().subtract(jours, 'day').format('YYYY-MM-DD')

const SIGNE = { preuves_fournies: true, constatation_signee: true, lettre_signe: true }
const ENVOYE = { ...SIGNE, lettre_envoyee: true, copie_archives: true }
const RECU = (jours: number) => ({
  ...ENVOYE,
  ar_recu: true,
  ar_statut: 'distribue',
  ar_presentation_date: ilYA(jours),
})

const dossier = (
  suivi: Record<string, unknown> = {},
  extra: Partial<ProcedureOverview> = {}
): ProcedureOverview => ({
  id: 1,
  date_modification: null,
  date_constat: '2026-09-01',
  heure_constat: null,
  localisation_depot: null,
  auteur_identifie: true,
  auteur_nom: 'Dupont',
  auteur_prenom: 'Marc',
  commune: 'Reignier-Ésery',
  is_draft: false,
  ...extra,
  suivi_procedure: { etape_en_cours: 1, ...suivi },
})

describe('Rangement des dossiers en colonnes', () => {
  it('range un brouillon dans « À compléter »', () => {
    const placement = getPlacementProcedure(dossier({}, { is_draft: true }))
    expect(placement.colonne).toBe('a_completer')
    expect(placement.libelle).toBe('Brouillon')
    expect(placement.action.label).toBe('Reprendre la constatation')
    expect(placement.action.to).toBe('/constatation/1')
  })

  it('range un auteur non identifié dans « À compléter »', () => {
    const placement = getPlacementProcedure(dossier(SIGNE, { auteur_identifie: false }))
    expect(placement.colonne).toBe('a_completer')
    expect(placement.libelle).toBe('Auteur non identifié')
    expect(placement.action.label).toBe("Identifier l'auteur")
  })

  it("n'utilise jamais la dernière section ouverte (etape_en_cours)", () => {
    const placement = getPlacementProcedure(dossier({ etape_en_cours: 4 }))
    expect(placement.colonne).toBe('documents_a_signer')
    expect(placement.action.to).toBe('/suivi-procedure/1?etape=1')
  })

  it('range un dossier signé mais non envoyé dans « Lettre à envoyer »', () => {
    expect(getPlacementProcedure(dossier(SIGNE)).colonne).toBe('lettre_a_envoyer')
  })

  it('attend la réception tant que la date de présentation manque', () => {
    const placement = getPlacementProcedure(dossier({ ...ENVOYE, lettre_envoyee_date: ilYA(3) }))
    expect(placement.colonne).toBe('attente_reception')
    expect(placement.action.label).toBe('Indiquer la réception')
  })

  it('démarre le contradictoire à la date de présentation', () => {
    const placement = getPlacementProcedure(dossier(RECU(3)))
    expect(placement.colonne).toBe('contradictoire')
    expect(placement.info).toMatch(/^Fin du contradictoire dans 7 jours \(\d{2}\/\d{2}\)$/)
    // Nothing to do during the contradictory phase: no action verb, card only has an arrow
    expect(placement.action.label).toBeUndefined()
    expect(placement.action.to).toBe('/suivi-procedure/1?etape=2')
  })

  it('signale un pli non réclamé pendant le contradictoire', () => {
    const placement = getPlacementProcedure(dossier({ ...RECU(2), ar_statut: 'non_reclame' }))
    expect(placement.colonne).toBe('contradictoire')
    expect(placement.alertes).toContain('Pli non réclamé')
  })

  it('garde le dossier en contradictoire si une case de la notification manque', () => {
    const placement = getPlacementProcedure(dossier({ ...RECU(20), copie_archives: false }))
    expect(placement.colonne).toBe('contradictoire')
    expect(placement.alertes[0]).toMatch(/copie aux archives/)
  })

  it('passe en « Décision à prendre » à la fin du contradictoire', () => {
    const placement = getPlacementProcedure(dossier(RECU(15)))
    expect(placement.colonne).toBe('decision')
    expect(placement.action.label).toBe('Décider des poursuites')
  })

  it('passe en « Décision à prendre » quand le courrier revient (NPAI)', () => {
    const placement = getPlacementProcedure(
      dossier({ ...ENVOYE, ar_recu: true, ar_statut: 'npai' })
    )
    expect(placement.colonne).toBe('decision')
    expect(placement.alertes).toContain('Courrier revenu (NPAI)')
  })

  it('range une sanction en cours dans « Auteur à sanctionner »', () => {
    const placement = getPlacementProcedure(
      dossier({ ...RECU(30), decision_poursuite: 'sanction', montant_amende: '500.00' })
    )
    expect(placement.colonne).toBe('sanction')
    expect(placement.action.label).toBe("Sanctionner l'auteur")
  })

  it('range un abandon en cours dans « Abandon des poursuites »', () => {
    const placement = getPlacementProcedure(dossier({ ...RECU(30), decision_poursuite: 'abandon' }))
    expect(placement.colonne).toBe('abandon')
    expect(placement.action.label).toBe("Confirmer le motif d'abandon")
  })

  it('clôture le dossier avec son issue', () => {
    const sanction = {
      ...RECU(30),
      decision_poursuite: 'sanction',
      montant_fixe: true,
      arrete_redige: true,
      titre_recette_emis: true,
      notification_sanction_envoyee: true,
    }
    expect(getPlacementProcedure(dossier(sanction)).issue).toBe('Amende émise')
    expect(getPlacementProcedure(dossier(sanction)).action.label).toBeUndefined()
    expect(getPlacementProcedure(dossier({ ...sanction, montant_recouvre: true })).issue).toBe(
      'Amende recouvrée'
    )
    const abandon = getPlacementProcedure(
      dossier({
        ...RECU(30),
        decision_poursuite: 'abandon',
        motif_abandon: 'Indulgence',
        souhaite_notifier_abandon: false,
      })
    )
    expect(abandon.colonne).toBe('cloture')
    expect(abandon.issue).toBe('Abandon')
  })
})

describe('Recherche et tri', () => {
  it('trouve un dossier par nom, sans tenir compte des accents ni de la casse', () => {
    const d = dossier({}, { auteur_nom: 'Lefèvre', auteur_prenom: 'Élodie', id: 42 })
    expect(correspondRecherche(d, 'lefevre')).toBe(true)
    expect(correspondRecherche(d, 'elodie')).toBe(true)
    expect(correspondRecherche(d, '#42')).toBe(true)
    expect(correspondRecherche(d, 'reignier')).toBe(true)
    expect(correspondRecherche(d, 'martin')).toBe(false)
  })

  it('trie par date du constat, la plus ancienne en haut', () => {
    const recent = dossier({}, { id: 1, date_constat: '2026-10-01' })
    const ancien = dossier({}, { id: 2, date_constat: '2026-08-01' })
    expect([recent, ancien].sort(comparerProcedures).map((d) => d.id)).toEqual([2, 1])
  })
  it('met les dossiers clôturés les plus récents en haut', () => {
    const recent = dossier({}, { id: 1, date_constat: '2026-10-01' })
    const ancien = dossier({}, { id: 2, date_constat: '2026-08-01' })
    const ordre = (colonne: Parameters<typeof comparerDansColonne>[0]) =>
      [ancien, recent].sort(comparerDansColonne(colonne)).map((d) => d.id)
    expect(ordre('cloture')).toEqual([1, 2])
    expect(ordre('decision')).toEqual([2, 1])
  })
})
