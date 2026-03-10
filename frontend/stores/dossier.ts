import { defineStore } from 'pinia'
import type { UserDossier } from '../services/api'
import { getUserDossiers, syncDossiers } from '../services/api'

export const useDossierStore = defineStore('dossier', {
  state: () => ({
    dossiers: [] as UserDossier[],
    loading: false,
    error: null as string | null,
    loaded: false,
    isSynced: false,
    _fetchPromise: null as Promise<void> | null,
  }),

  actions: {
    async fetchDossiers() {
      if (this.loaded) return
      if (this._fetchPromise) return this._fetchPromise

      this._fetchPromise = (async () => {
        this.loading = true
        try {
          const dossiers = await getUserDossiers()
          this.dossiers = dossiers
          this.loaded = true
        } catch (error) {
          this.error = 'Erreur lors de la récupération des dossiers'
          console.error('Error fetching dossiers:', error)
        } finally {
          this.loading = false
          this._fetchPromise = null
        }
      })()

      return this._fetchPromise
    },
    async syncDossiers() {
      if (this.isSynced) {
        return
      }
      try {
        await syncDossiers()
        this.isSynced = true
      } catch (error) {
        console.error('Error syncing dossiers:', error)
      }
    },

    getDossierById(id: number | string): UserDossier | undefined {
      // id can be a string or number, doing loose comparison or ensuring type match
      const numericId = Number(id)
      return this.dossiers.find((d) => d.id === numericId)
    },
  },
})
