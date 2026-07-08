import { defineStore } from 'pinia'
import { API_URL, fetchResource, patchResource } from '../services/api'

export interface SuiviProcedure {
  etape_en_cours: number
  preuves_fournies: boolean
  constatation_signee: boolean
  lettre_signe: boolean
  identification_reussie: boolean | null
  observations_internes: string
  personne_assignee: number | null
  date_assignation: string | null
  anomalie: string
  lettre_envoyee: boolean
  lettre_envoyee_date: string | null
  copie_archives: boolean
  ar_recu: boolean
  ar_statut: string
  ar_presentation_date: string | null
  decision_poursuite: string
  montant_fixe: boolean
  montant_amende: string | null
  arrete_redige: boolean
  titre_recette_emis: boolean
  notification_sanction_envoyee: boolean
  motif_abandon: string
  souhaite_notifier_abandon: boolean | null
  notification_abandon_envoyee: boolean
  nettoyage_fait: boolean | null
  nettoyage_par: string
  date_recouvrement_effective: string | null
  titre_recette_confirme: boolean
  montant_recouvre: boolean
  dossier_archive: boolean
  statut_traitement: string
}


export interface BackofficeProcedure {
  id: number
  commune: string
  date_constat: string
  constatant_role: string
  volume_depot: string
  nature_terrain: string[]
  ceci_est_un_test: boolean
  user_email: string
  agent: string
  auteur_identifie: boolean
  suivi_procedure: SuiviProcedure
  localisation_depot: string
  heure_constat: string | null
  constatant_civilite: string
  constatant_nom: string
  constatant_prenom: string
  proprietaire_terrain_prive: string
  types_depot: string[]
  precisions_depot: string
  photo_dispo: boolean
  risque_ecoulement: boolean
  statut_auteur: string | null
  auteur_civilite: string
  auteur_nom: string
  auteur_prenom: string
  auteur_adresse: string
  auteur_siret: string
  entreprise_francaise: boolean | null
  plainte_etat: string
  indices_disponibles: string[]
  precisions_indices: string
  prejudice_montant_connu: boolean
  prejudice_montant: number | null
  prejudice_nombre_personnes: number | null
  prejudice_nombre_heures: number | null
  prejudice_nombre_vehicules: number | null
  prejudice_kilometrage: number | null
  prejudice_autres_couts: number | null
  contact_nom: string
  contact_prenom: string
  contact_email: string
  contact_telephone: string
  accepte_accompagnement: boolean
  doc_constat_generated_at: string | null
  lettre_info_generated_at: string | null
}

export interface Assignee {
  id: number | null
  name: string
  email?: string
}

export interface BackofficeState {
  assignees: Assignee[]
  procedures: BackofficeProcedure[]
  stats: {
    totalActive: number
    arWaiting: number
    decisionToTake: number
    closedThisMonth: number
  }
}

export const useBackofficeStore = defineStore('backoffice', {
  state: (): BackofficeState => ({
    assignees: [{ id: null, name: 'Non assigné' }],
    procedures: [],
    stats: {
      totalActive: 84,
      arWaiting: 18,
      decisionToTake: 7,
      closedThisMonth: 23,
    },
  }),
  getters: {
    getProcedureById: (state) => (id: number | string) => {
      return state.procedures.find((p) => p.id === Number(id))
    },
    workloadByAssignee: (state) => {
      const realProcs = state.procedures.filter((p) => !p.ceci_est_un_test)
      const counts: Record<string, number> = {}
      state.assignees.forEach((assignee) => {
        counts[assignee.name] = 0
      })
      realProcs.forEach((p) => {
        const id = p.suivi_procedure.personne_assignee
        const assignee = state.assignees.find((a) => a.id === id)
        const name = assignee ? assignee.name : 'Non assigné'
        if (counts[name] !== undefined) {
          counts[name]++
        } else {
          counts[name] = 1
        }
      })
      // Filter out assignees with count === 0, except for 'Non assigné'
      return Object.fromEntries(
        Object.entries(counts).filter(([name, count]) => name === 'Non assigné' || count > 0)
      )
    },
  },

  actions: {
    async saveSuivi(procedureId: number) {
      const procedure = this.procedures.find((p) => p.id === procedureId)
      if (procedure && procedure.suivi_procedure) {
        try {
          const { anomalie, ...suiviPayload } = procedure.suivi_procedure
          const updated = await patchResource(
            `${API_URL}/suivi-procedure/${procedureId}/`,
            suiviPayload
          )
          if (updated) {
            procedure.suivi_procedure = {
              ...procedure.suivi_procedure,
              ...(updated as Partial<SuiviProcedure>),
            }
          }
        } catch (error) {
          console.error('Failed to save suivi procedure:', error)
        }
      }
    },
    assignCharge(procedureId: number, assigneeId: number | null) {
      const procedure = this.procedures.find((p) => p.id === procedureId)
      if (procedure && procedure.suivi_procedure) {
        procedure.suivi_procedure.personne_assignee = assigneeId
        this.saveSuivi(procedureId)
      }
    },
    updateNotes(procedureId: number, notes: string) {
      const procedure = this.procedures.find((p) => p.id === procedureId)
      if (procedure && procedure.suivi_procedure) {
        procedure.suivi_procedure.observations_internes = notes
        this.saveSuivi(procedureId)
      }
    },
    updateTraitement(procedureId: number, status: string) {
      const procedure = this.procedures.find((p) => p.id === procedureId)
      if (procedure && procedure.suivi_procedure) {
        procedure.suivi_procedure.statut_traitement = status
        this.saveSuivi(procedureId)
      }
    },

    toggleSuiviField(procedureId: number, field: string) {
      const procedure = this.procedures.find((p) => p.id === procedureId)
      if (procedure && procedure.suivi_procedure) {
        if (field === 'preuves') {
          procedure.suivi_procedure.preuves_fournies = !procedure.suivi_procedure.preuves_fournies
        } else if (field === 'rapportSigne') {
          procedure.suivi_procedure.constatation_signee =
            !procedure.suivi_procedure.constatation_signee
        } else if (field === 'lettreSignee') {
          procedure.suivi_procedure.lettre_signe = !procedure.suivi_procedure.lettre_signe
        } else if (field === 'auteurIdentifie') {
          const current = procedure.suivi_procedure.identification_reussie
          procedure.suivi_procedure.identification_reussie =
            current === true ? false : current === false ? null : true
        }
        this.saveSuivi(procedureId)
      }
    },

    async fetchAssignees() {
      try {
        const data = await fetchResource(`${API_URL}/backoffice-staff/`)
        const fetched = (data as any[]).map((u) => ({
          id: u.id,
          name: u.name,
          email: u.email,
        }))
        this.assignees = [{ id: null, name: 'Non assigné' }, ...fetched]
      } catch (error) {
        console.error('Failed to fetch assignees:', error)
      }
    },
    async fetchDashboardStats() {
      try {
        const data = await fetchResource(`${API_URL}/backoffice-dashboard-stats/`)
        if (data) {
          this.stats = {
            ...this.stats,
            ...(data as any),
          }
        }
      } catch (error) {
        console.error('Failed to fetch dashboard stats:', error)
      }
    },
    async fetchProcedures() {
      try {
        const data = await fetchResource(`${API_URL}/backoffice-procedures/`)
        this.procedures = data as BackofficeProcedure[]
        await this.fetchAssignees()
        await this.fetchDashboardStats()
      } catch (error) {
        console.error('Failed to fetch backoffice procedures:', error)
      }
    },
  },
})
