import { getProcedureTraitement } from '@/utils/backoffice'
import { defineStore } from 'pinia'
import { API_URL, fetchResource, patchResource } from '../services/api'

export interface SuiviProcedure {
  etape_en_cours: number
  preuves_fournies: boolean
  constatation_signee: boolean
  lettre_signe: boolean
  identification_reussie: boolean | null
  observations_internes: string
  notes_traitement: string
  personne_assignee: number | null
  date_pilotage: string | null
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
  modified: string
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
  modified: string
}

export interface Assignee {
  id: number | null
  name: string
  email?: string
}

export interface BackofficeState {
  assignees: Assignee[]
  procedures: BackofficeProcedure[]
  totalProceduresCount: number
  stats: {
    totalActive: number
    arWaiting: number
    decisionToTake: number
    closed: number
    generalStats?: {
      total: number
      real: number
      test: number
      authorIdentified: number
      authorNotIdentified: number
    }
    steps?: {
      identified: Record<number, number>
      notIdentified: Record<number, number>
    }
    byStatus?: Record<string, number>
    workloadByAssigneeId?: Record<string, number>
  }
}

export const useBackofficeStore = defineStore('backoffice', {
  state: (): BackofficeState => ({
    assignees: [{ id: null, name: 'Non assigné' }],
    procedures: [],
    totalProceduresCount: 0,
    stats: {
      totalActive: 0,
      arWaiting: 0,
      decisionToTake: 0,
      closed: 0,
    },
  }),
  getters: {
    getProcedureById: (state) => (id: number | string) => {
      return state.procedures.find((p) => p.id === Number(id))
    },
    workloadByAssignee: (state) => {
      if (state.stats.workloadByAssigneeId) {
        const counts: Record<string, number> = {}
        state.assignees.forEach((assignee) => {
          counts[assignee.name] = 0
        })
        Object.entries(state.stats.workloadByAssigneeId).forEach(([key, count]) => {
          const id = key === 'null' || key === 'None' ? null : Number(key)
          const assignee = state.assignees.find((a) => a.id === id)
          const name = assignee ? assignee.name : 'Non assigné'
          counts[name] = (counts[name] || 0) + count
        })
        return Object.fromEntries(
          Object.entries(counts).filter(([name, count]) => name === 'Non assigné' || count > 0)
        )
      }
      const realProcs = state.procedures.filter((p) => !p.ceci_est_un_test)
      const counts: Record<string, number> = {}
      state.assignees.forEach((assignee) => {
        counts[assignee.name] = 0
      })
      realProcs.forEach((p) => {
        const id = p.suivi_procedure?.personne_assignee
        const assignee = state.assignees.find((a) => a.id === id)
        const name = assignee ? assignee.name : 'Non assigné'
        if (counts[name] !== undefined) {
          counts[name]++
        } else {
          counts[name] = 1
        }
      })
      return Object.fromEntries(
        Object.entries(counts).filter(([name, count]) => name === 'Non assigné' || count > 0)
      )
    },
    proceduresByStatus: (state) => {
      if (state.stats.byStatus) {
        return state.stats.byStatus
      }
      const realProcs = state.procedures.filter((p) => !p.ceci_est_un_test)
      const counts: Record<string, number> = {
        Nouveau: 0,
        Ouvert: 0,
        'En pause': 0,
        Résolu: 0,
        Clôturé: 0,
      }
      realProcs.forEach((p) => {
        const status = getProcedureTraitement(p)
        if (counts[status] !== undefined) {
          counts[status]++
        }
      })
      return counts
    },
    generalStats: (state) => {
      if (state.stats.generalStats) {
        return state.stats.generalStats
      }
      const total = state.procedures.length
      const real = state.procedures.filter((p) => !p.ceci_est_un_test).length
      const test = state.procedures.filter((p) => p.ceci_est_un_test).length
      const authorIdentified = state.procedures.filter(
        (p) => !p.ceci_est_un_test && p.auteur_identifie
      ).length
      const authorNotIdentified = state.procedures.filter(
        (p) => !p.ceci_est_un_test && !p.auteur_identifie
      ).length

      return {
        total,
        real,
        test,
        authorIdentified,
        authorNotIdentified,
      }
    },
    proceduresByStepAndAuthor: (state) => {
      if (state.stats.steps) {
        return state.stats.steps
      }
      const realProcs = state.procedures.filter((p) => !p.ceci_est_un_test)
      const identified: Record<number, number> = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 }
      const notIdentified: Record<number, number> = { 1: 0, 2: 0, 3: 0, 5: 0 }

      realProcs.forEach((p) => {
        const etape = p.suivi_procedure?.etape_en_cours ?? 1
        if (p.auteur_identifie) {
          if (etape >= 5) {
            identified[5]++
          } else if (etape in identified) {
            identified[etape]++
          }
        } else {
          if (etape >= 5) {
            notIdentified[5]++
          } else if (etape === 4) {
            notIdentified[3]++
          } else if (etape in notIdentified) {
            notIdentified[etape]++
          }
        }
      })

      return { identified, notIdentified }
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
    assignAssignee(procedureId: number, assigneeId: number | null) {
      const procedure = this.procedures.find((p) => p.id === procedureId)
      if (procedure && procedure.suivi_procedure) {
        procedure.suivi_procedure.personne_assignee = assigneeId
        this.saveSuivi(procedureId)
      }
    },
    updateNotes(procedureId: number, notes: string) {
      const procedure = this.procedures.find((p) => p.id === procedureId)
      if (procedure && procedure.suivi_procedure) {
        procedure.suivi_procedure.notes_traitement = notes
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
        const current = (procedure.suivi_procedure as any)[field]
        ;(procedure.suivi_procedure as any)[field] = !current
        this.saveSuivi(procedureId)
      }
    },
    async fetchAssignees() {
      try {
        const staff = await fetchResource(`${API_URL}/backoffice-staff/`)
        if (Array.isArray(staff)) {
          this.assignees = [
            { id: null, name: 'Non assigné' },
            ...staff.map((s: any) => ({ id: s.id, name: s.name, email: s.email })),
          ]
        }
      } catch (error) {
        console.error('Failed to fetch staff assignees:', error)
      }
    },
    async fetchDashboardStats() {
      try {
        await this.fetchAssignees()
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
    async fetchProcedures(params?: Record<string, any>) {
      try {
        const query = new URLSearchParams()
        if (params) {
          Object.entries(params).forEach(([key, val]) => {
            if (val !== undefined && val !== null && val !== '' && val !== 'Tous') {
              query.append(key, String(val))
            }
          })
        }
        const queryString = query.toString() ? `?${query.toString()}` : ''
        const data = await fetchResource(`${API_URL}/backoffice-procedures/${queryString}`)
        if (data && typeof data === 'object' && 'results' in data) {
          this.procedures = data.results as BackofficeProcedure[]
          this.totalProceduresCount = data.count ?? data.results.length
        } else {
          this.procedures = (data as BackofficeProcedure[]) || []
          this.totalProceduresCount = this.procedures.length
        }
        await this.fetchAssignees()
      } catch (error) {
        console.error('Failed to fetch backoffice procedures:', error)
      }
    },
  },
})
