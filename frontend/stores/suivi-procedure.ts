import { defineStore } from 'pinia'
import { reactive } from 'vue'

export interface SuiviProcedure {
  // Étape 2 : Notification
  lettre_envoyee: boolean
  lettre_envoyee_date: string
  copie_archives: boolean
  ar_recu: boolean
  ar_statut: string
  ar_presentation_date: string
  
  // Autres étapes (préparation)
  decision_poursuite: string // 'sanction' | 'abandon' | ''
  montant_amende: number | null
  motif_abandon: string
  date_recouvrement: string
  nettoyage_fait: boolean | null
  nettoyage_par: string
  observations_internes: string
}

export const useSuiviStore = defineStore('suiviProcedure', () => {
  const procedures = reactive<Record<string, SuiviProcedure>>({})

  const getOrCreateSuivi = (dossierId: string): SuiviProcedure => {
    if (!procedures[dossierId]) {
      procedures[dossierId] = {
        lettre_envoyee: false,
        lettre_envoyee_date: '',
        copie_archives: false,
        ar_recu: false,
        ar_statut: '',
        ar_presentation_date: '',
        decision_poursuite: '',
        montant_amende: null,
        motif_abandon: '',
        date_recouvrement: '',
        nettoyage_fait: null,
        nettoyage_par: '',
        observations_internes: '',
      }
    }
    return procedures[dossierId]
  }

  return {
    procedures,
    getOrCreateSuivi,
  }
})
