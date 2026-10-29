import type { ProcedureOverview } from '../services/api'
import { getSuiviProcedureUrl } from '../services/urls'
import {
  createEmptySuivi,
  isSuiviStepCompleted,
  type SuiviProcedure,
} from '../stores/suivi-procedure'
import { calculateContradictoire } from './procedure'

/**
 * "Mes procédures" dashboard: files placement across columns.
 *
 * Rule: each section on the tracking page corresponds to a column, and a file
 * is placed in the column of the first section not yet marked as completed
 * (see isSuiviStepCompleted). The "Notifier l'auteur" section is split into
 * 3 columns depending on dates, and "Sanctionner / Abandonner" into 2 depending
 * on the decision. The etape_en_cours field (last opened section) is intentionally ignored.
 */

export type ColonneId =
  | 'a_completer'
  | 'documents_a_signer'
  | 'lettre_a_envoyer'
  | 'attente_reception'
  | 'contradictoire'
  | 'decision'
  | 'sanction'
  | 'abandon'
  | 'cloture'

export const COLONNES: { id: ColonneId; titre: string }[] = [
  { id: 'a_completer', titre: 'À compléter' },
  { id: 'documents_a_signer', titre: 'Documents à signer' },
  { id: 'lettre_a_envoyer', titre: 'Lettre à envoyer' },
  { id: 'attente_reception', titre: 'En attente de réception' },
  { id: 'contradictoire', titre: 'Contradictoire en cours' },
  { id: 'decision', titre: 'Décision à prendre' },
  { id: 'sanction', titre: 'Auteur à sanctionner' },
  { id: 'abandon', titre: 'Abandon des poursuites' },
  { id: 'cloture', titre: 'Clôturé' },
]

export interface PlacementProcedure {
  colonne: ColonneId
  libelle?: string
  info?: string
  alertes: string[]
  issue?: string
  action: { label?: string; to: string }
}

const AR_STATUT_ALERTES: Record<string, string> = {
  npai: 'Courrier revenu (NPAI)',
  non_reclame: 'Pli non réclamé',
  refuse: 'Courrier refusé',
}

const versSection = (procedure: ProcedureOverview, etape: number) =>
  `${getSuiviProcedureUrl(procedure.id)}?etape=${etape}`

const formatMontant = (montant: number | string | null | undefined) => {
  if (montant === null || montant === undefined || montant === '') return ''
  return `${Number(montant).toLocaleString('fr-FR')} €`
}

const finContradictoire = (joursRestants: number, dateFin: string | null) => {
  const date = dateFin ? ` (${dateFin.slice(0, 5)})` : ''
  if (joursRestants === 1) return `Fin du contradictoire dans 1 jour${date}`
  return `Fin du contradictoire dans ${joursRestants} jours${date}`
}

const etapesNotificationRestantes = (suivi: SuiviProcedure) => {
  const restantes: string[] = []
  if (!suivi.lettre_envoyee_date) restantes.push("date d'envoi")
  if (!suivi.ar_recu || !suivi.ar_statut) restantes.push("statut de l'accusé de réception")
  return restantes
}

export const getPlacementProcedure = (procedure: ProcedureOverview): PlacementProcedure => {
  const suivi: SuiviProcedure = { ...createEmptySuivi(), ...(procedure.suivi_procedure ?? {}) }
  const fait = (etape: number) =>
    isSuiviStepCompleted(suivi, etape, { auteurIdentifie: !!procedure.auteur_identifie })

  if (procedure.is_draft) {
    return {
      colonne: 'a_completer',
      libelle: 'Brouillon',
      alertes: [],
      action: { label: 'Reprendre la constatation', to: `/constatation/${procedure.id}` },
    }
  }

  if (!procedure.auteur_identifie) {
    if (suivi.dossier_archive) {
      return {
        colonne: 'cloture',
        libelle: 'Auteur non identifié',
        issue: 'Auteur non identifié',
        alertes: [],
        action: { to: versSection(procedure, 3) },
      }
    }
    // Until the identity is entered in the app, the author stays unidentified: same verb whether
    // the search is pending (section 2) or the author was found (section 3, enter the identity).
    let action: PlacementProcedure['action'] = {
      label: "Identifier l'auteur",
      to: versSection(procedure, 2),
    }
    if (suivi.identification_reussie === true) {
      action = { label: "Identifier l'auteur", to: versSection(procedure, 3) }
    } else if (suivi.identification_reussie === false) {
      action = { label: 'Clôturer le dossier', to: versSection(procedure, 3) }
    }
    return {
      colonne: 'a_completer',
      libelle: 'Auteur non identifié',
      alertes: [],
      action,
    }
  }

  if (!fait(1)) {
    return {
      colonne: 'documents_a_signer',
      alertes: [],
      action: { label: 'Marquer comme signé', to: versSection(procedure, 1) },
    }
  }

  if (!suivi.lettre_envoyee) {
    return {
      colonne: 'lettre_a_envoyer',
      alertes: [],
      action: { label: 'Marquer comme envoyé', to: versSection(procedure, 2) },
    }
  }

  const alerteAr = suivi.ar_recu ? AR_STATUT_ALERTES[suivi.ar_statut] : undefined
  const npai = suivi.ar_recu && suivi.ar_statut === 'npai'

  if (!npai && !(suivi.ar_recu && suivi.ar_presentation_date)) {
    return {
      colonne: 'attente_reception',
      alertes: [],
      action: { label: "Indiquer le statut de l'AR", to: versSection(procedure, 2) },
    }
  }

  if (!npai) {
    const contradictoire = calculateContradictoire(suivi.ar_presentation_date)
    if (contradictoire.joursRestants > 0) {
      return {
        colonne: 'contradictoire',
        info: finContradictoire(contradictoire.joursRestants, contradictoire.dateFin),
        alertes: alerteAr ? [alerteAr] : [],
        action: { to: versSection(procedure, 2) },
      }
    }
    if (!fait(2)) {
      return {
        colonne: 'contradictoire',
        alertes: [
          `Contradictoire terminé — étape restante : ${etapesNotificationRestantes(suivi).join(', ')}`,
        ],
        action: { label: 'Garder une copie pour archive', to: versSection(procedure, 2) },
      }
    }
  } else if (!fait(2)) {
    return {
      colonne: 'attente_reception',
      alertes: [
        'Courrier revenu (NPAI)',
        `Étape restante : ${etapesNotificationRestantes(suivi).join(', ')}`,
      ],
      action: { label: 'Garder une copie pour archive', to: versSection(procedure, 2) },
    }
  }

  if (!fait(3)) {
    const alertes: string[] = []
    if (alerteAr) alertes.push(alerteAr)
    if (suivi.decision_poursuite === 'recherche_adresse')
      alertes.push("Recherche d'adresse en cours")
    const contradictoire = calculateContradictoire(suivi.ar_presentation_date)
    return {
      colonne: 'decision',
      info: contradictoire.dateFin
        ? `Contradictoire terminé le ${contradictoire.dateFin.slice(0, 5)}`
        : undefined,
      alertes,
      action: { label: 'Décider des poursuites', to: versSection(procedure, 3) },
    }
  }

  if (!fait(4)) {
    if (suivi.decision_poursuite === 'sanction') {
      const montant = formatMontant(suivi.montant_amende)
      return {
        colonne: 'sanction',
        info: montant ? `Amende de ${montant}` : undefined,
        alertes: [],
        action: { label: "Sanctionner l'auteur", to: versSection(procedure, 4) },
      }
    }
    return {
      colonne: 'abandon',
      alertes: [],
      action: { label: "Confirmer le motif d'abandon", to: versSection(procedure, 4) },
    }
  }

  let issue = 'Abandon'
  if (suivi.decision_poursuite === 'sanction') {
    issue = suivi.montant_recouvre ? 'Amende recouvrée' : 'Amende émise'
  }
  const montant = suivi.decision_poursuite === 'sanction' ? formatMontant(suivi.montant_amende) : ''
  return {
    colonne: 'cloture',
    issue,
    info: montant ? `Amende de ${montant}` : undefined,
    alertes: [],
    action: { to: versSection(procedure, 5) },
  }
}

export const getNomContrevenant = (procedure: ProcedureOverview) =>
  [procedure.auteur_prenom, procedure.auteur_nom]
    .map((part) => (part ?? '').trim())
    .filter(Boolean)
    .join(' ')

const normaliser = (texte: string) =>
  texte.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().trim()

export const correspondRecherche = (procedure: ProcedureOverview, recherche: string) => {
  const terme = normaliser(recherche).replace(/^#/, '')
  if (!terme) return true
  const champs = [getNomContrevenant(procedure), String(procedure.id), procedure.commune ?? '']
  return champs.some((champ) => normaliser(champ).includes(terme))
}

export const comparerProcedures = (a: ProcedureOverview, b: ProcedureOverview) => {
  if (a.date_constat !== b.date_constat) {
    if (!a.date_constat) return 1
    if (!b.date_constat) return -1
    return a.date_constat < b.date_constat ? -1 : 1
  }
  return a.id - b.id
}

/**
 * Card order within a column. Active columns show oldest records first (highest priority).
 * Closed column shows newest records first. Since closure date is not recorded,
 * constatation date is used as an approximation.
 */
export const comparerDansColonne =
  (colonne: ColonneId) => (a: ProcedureOverview, b: ProcedureOverview) => {
    if (colonne !== 'cloture') return comparerProcedures(a, b)
    if (a.date_constat !== b.date_constat) {
      if (!a.date_constat) return 1
      if (!b.date_constat) return -1
      return a.date_constat > b.date_constat ? -1 : 1
    }
    return b.id - a.id
  }
