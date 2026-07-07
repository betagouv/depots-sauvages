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

export interface WeeklySnapshot {
  date: string
  procedures: number
  activeCollectivities: number
  finesCount: number
  amountFines: number
  cleanedCount: number
  cleanedVolume: number
  webinarsCount: number
}

export interface OkrMetric {
  label: string
  current: number
  target: number
  unit: string
}

export interface BackofficeHistory {
  date: string
  total: number
  success: number
  abandoned: number
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
    actionRequired: number
    arWaiting: number
    decisionToTake: number
    closedThisMonth: number
    weeklySnapshots: WeeklySnapshot[]
    okrs: Record<string, OkrMetric>
    history: BackofficeHistory[]
  }
}

export const useBackofficeStore = defineStore('backoffice', {
  state: (): BackofficeState => ({
    assignees: [{ id: null, name: 'Non assigné' }],
    procedures: [],
    // OKR and Weekly stats targets
    stats: {
      totalActive: 84,
      actionRequired: 12,
      arWaiting: 18,
      decisionToTake: 7,
      closedThisMonth: 23,

      // Weekly meeting tracking table (from stats-sample.md)
      weeklySnapshots: [
        {
          date: '02/06',
          procedures: 345,
          activeCollectivities: 180,
          finesCount: 42,
          amountFines: 21180.34,
          cleanedCount: 17,
          cleanedVolume: 548,
          webinarsCount: 570,
        },
        {
          date: '02/06', // preserved duplicate date from original code
          procedures: 345,
          activeCollectivities: 180,
          finesCount: 42,
          amountFines: 21180.34,
          cleanedCount: 17,
          cleanedVolume: 548,
          webinarsCount: 570,
        },
        {
          date: '09/06',
          procedures: 384,
          activeCollectivities: 189,
          finesCount: 43,
          amountFines: 21330.34,
          cleanedCount: 17,
          cleanedVolume: 548,
          webinarsCount: 608,
        },
        {
          date: '16/06',
          procedures: 433,
          activeCollectivities: 196,
          finesCount: 49,
          amountFines: 25530.34,
          cleanedCount: 18,
          cleanedVolume: 548,
          webinarsCount: 648,
        },
        {
          date: '23/06',
          procedures: 491,
          activeCollectivities: 245,
          finesCount: 50,
          amountFines: 26280.0,
          cleanedCount: 19,
          cleanedVolume: 558,
          webinarsCount: 691,
        },
        {
          date: '30/06',
          procedures: 545,
          activeCollectivities: 264,
          finesCount: 50,
          amountFines: 26280.0,
          cleanedCount: 19,
          cleanedVolume: 558,
          webinarsCount: 721,
        },
      ],

      okrs: {
        kr1_1: {
          label: 'Procédures administratives engagées (LI)',
          current: 545,
          target: 1300,
          unit: 'procédures',
        },
        kr1_2: {
          label: 'Taux de complétion des constatations',
          current: 92,
          target: 90,
          unit: '%',
        },
        kr1_3: {
          label: 'Décision validée après 1 mois (Sanction/Abandon)',
          current: 48,
          target: 50,
          unit: '%',
        },
        kr2_1: {
          label: 'Participants aux webinaires (cumul)',
          current: 721,
          target: 2000,
          unit: 'participants',
        },
        kr2_2: {
          label: 'Communes actives (LI lancée 6 derniers mois)',
          current: 264,
          target: 500,
          unit: 'communes',
        },
        kr3_1: { label: 'NPS Moyen Utilisateurs', current: 42, target: 40, unit: 'NPS' },
        kr3_2: {
          label: "Taux de rétention des communes (>1 mois d'intervalle)",
          current: 28,
          target: 33,
          unit: '%',
        },
      },

      // Chart line graph history
      history: [
        { date: 'Janvier', total: 180, success: 50, abandoned: 15 },
        { date: 'Février', total: 240, success: 75, abandoned: 20 },
        { date: 'Mars', total: 310, success: 98, abandoned: 28 },
        { date: 'Avril', total: 390, success: 120, abandoned: 32 },
        { date: 'Mai', total: 470, success: 150, abandoned: 45 },
        { date: 'Juin', total: 545, success: 180, abandoned: 50 },
      ],
    },
  }),
  getters: {
    getProcedureById: (state) => (id: number | string) => {
      return state.procedures.find((p) => p.id === Number(id))
    },
    realProcedures: (state) => {
      return state.procedures.filter((p) => !p.ceci_est_un_test)
    },
    activeCommunesCount: (state) => {
      const realProcs = state.procedures.filter((p) => !p.ceci_est_un_test)
      const communes = realProcs.map((p) => p.commune.trim())
      return new Set(communes).size
    },
    liveIdentificationRate: (state) => {
      const realProcs = state.procedures.filter((p) => !p.ceci_est_un_test)
      if (realProcs.length === 0) return 0
      const identified = realProcs.filter(
        (p) => p.suivi_procedure.identification_reussie === true
      ).length
      return Math.round((identified / realProcs.length) * 100)
    },
    liveCompletionRate: (state) => {
      const realProcs = state.procedures.filter((p) => !p.ceci_est_un_test)
      if (realProcs.length === 0) return 0
      const completed = realProcs.filter((p) => p.suivi_procedure.etape_en_cours >= 2).length
      return Math.round((completed / realProcs.length) * 100)
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
      return counts
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
    saveWeeklySnapshot(snapshot: WeeklySnapshot) {
      const existingIndex = this.stats.weeklySnapshots.findIndex((s) => s.date === snapshot.date)
      if (existingIndex !== -1) {
        this.stats.weeklySnapshots[existingIndex] = { ...snapshot }
      } else {
        this.stats.weeklySnapshots.push({ ...snapshot })
      }
    },
    deleteWeeklySnapshot(date: string) {
      this.stats.weeklySnapshots = this.stats.weeklySnapshots.filter((s) => s.date !== date)
    },
    updateOkrValue(okrKey: string, newValue: number) {
      if (this.stats.okrs[okrKey]) {
        this.stats.okrs[okrKey].current = newValue
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
