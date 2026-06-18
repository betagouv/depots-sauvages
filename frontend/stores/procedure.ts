import { defineStore } from 'pinia'
import type { ProcedureOverview } from '../services/api'
import { getUserProcedures } from '../services/api'

export const useProcedureStore = defineStore('procedure', {
  state: () => ({
    procedures: [] as ProcedureOverview[],
    loading: false,
    error: null as string | null,
    loaded: false,
    _fetchPromise: null as Promise<void> | null,
  }),

  actions: {
    async fetchProcedures(force = false) {
      if (this.loaded && !force) return
      if (this._fetchPromise) return this._fetchPromise

      this._fetchPromise = (async () => {
        this.loading = true
        try {
          const procedures = await getUserProcedures()
          this.procedures = procedures
          this.loaded = true
        } catch (error) {
          this.error = 'Erreur lors de la récupération des procédures'
          console.error('Error fetching procedures:', error)
        } finally {
          this.loading = false
          this._fetchPromise = null
        }
      })()

      return this._fetchPromise
    },

    getProcedureById(id: number | string): ProcedureOverview | undefined {
      const numericId = Number(id)
      return this.procedures.find((p) => p.numero_dossier === numericId)
    },
  },
})
