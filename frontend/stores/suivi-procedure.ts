import { defineStore } from 'pinia'
import { reactive } from 'vue'

export interface SuiviProcedure {
  // Étape 1 : Pièces de procédure
  preuve_photos_jointes: boolean
  rapport_constat_signe: boolean
  lettre_info_signee: boolean

  // Étape 2 : Notification
  lettre_envoyee: boolean
  lettre_envoyee_date: string
  copie_archives: boolean
  ar_recu: boolean
  ar_statut: string
  ar_presentation_date: string

  // Étape 4 : Actions selon décision
  montant_fixe: boolean
  arrete_redige: boolean
  titre_recette_emis: boolean
  notification_sanction_envoyee: boolean
  notification_abandon_envoyee: boolean
  decision_poursuite: string // 'sanction' | 'abandon' | ''
  motif_abandon_choisi: boolean

  montant_amende: number | null
  motif_abandon: string
  date_recouvrement_effective: string
  nettoyage_fait: boolean | null
  nettoyage_par: string
  observations_internes: string

  // Étape 5 : Clôture
  nettoyage_confirme: boolean
  titre_recette_confirme: boolean
  montant_recouvre: boolean
  dossier_archive: boolean
}

export const useSuiviStore = defineStore('suiviProcedure', () => {
  const procedures = reactive<Record<string, SuiviProcedure>>({})

  const getOrCreateSuivi = (dossierId: string): SuiviProcedure => {
    if (!procedures[dossierId]) {
      procedures[dossierId] = {
        preuve_photos_jointes: false,
        rapport_constat_signe: false,
        lettre_info_signee: false,
        lettre_envoyee: false,
        lettre_envoyee_date: '',
        copie_archives: false,
        ar_recu: false,
        ar_statut: '',
        ar_presentation_date: '',
        montant_fixe: false,
        arrete_redige: false,
        titre_recette_emis: false,
        notification_sanction_envoyee: false,
        notification_abandon_envoyee: false,
        decision_poursuite: '',
        motif_abandon_choisi: false,
        montant_amende: null,
        motif_abandon: '',
        date_recouvrement_effective: '',
        nettoyage_fait: null,
        nettoyage_par: '',
        observations_internes: '',
        nettoyage_confirme: false,
        titre_recette_confirme: false,
        montant_recouvre: false,
        dossier_archive: false,
      }
    }
    return procedures[dossierId]
  }

  const isStepCompleted = (
    dossierId: string,
    stepIndex: number,
    context: { auteurIdentifie: boolean; currentStep: number }
  ): boolean => {
    const suivi = procedures[dossierId]
    if (!suivi && stepIndex > 0) return false

    // Pour l'étape 0, on se base sur le fait qu'on a avancé dans le stepper
    if (stepIndex === 0) {
      return context.currentStep > 0
    }

    if (!suivi) return false

    switch (stepIndex) {
      case 1:
        return (
          suivi.preuve_photos_jointes &&
          suivi.rapport_constat_signe &&
          (!context.auteurIdentifie || suivi.lettre_info_signee)
        )
      case 2:
        if (!context.auteurIdentifie) return false
        return suivi.lettre_envoyee && suivi.copie_archives && suivi.ar_recu
      case 3:
        if (suivi.decision_poursuite === 'nouvelle_adresse') return false
        return suivi.decision_poursuite !== ''
      case 4:
        if (suivi.decision_poursuite === 'sanction') {
          return (
            suivi.montant_fixe &&
            suivi.arrete_redige &&
            suivi.titre_recette_emis &&
            suivi.notification_sanction_envoyee
          )
        }
        if (suivi.decision_poursuite === 'abandon') {
          if (suivi.motif_abandon === 'Auteur introuvable (NPAI)') {
            return true
          }
          return (
            suivi.motif_abandon_choisi &&
            (suivi.motif_abandon === 'Un auteur identifié' || suivi.notification_abandon_envoyee)
          )
        }
        return false
      case 5:
        if (suivi.decision_poursuite === 'sanction') {
          return suivi.titre_recette_confirme && suivi.montant_recouvre && suivi.dossier_archive
        }
        return suivi.dossier_archive
      default:
        return false
    }
  }

  return {
    procedures,
    getOrCreateSuivi,
    isStepCompleted,
  }
})
