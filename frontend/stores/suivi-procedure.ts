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
  
  montant_amende: number | null
  motif_abandon: string
  date_recouvrement: string
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
        montant_amende: null,
        motif_abandon: '',
        date_recouvrement: '',
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

  return {
    procedures,
    getOrCreateSuivi,
  }
})
