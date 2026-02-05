import { defineStore } from 'pinia'
import { getUserDossiers, type UserDossier } from '../services/api'

export const useDossierStore = defineStore('dossier', {
  state: () => ({
    dossiers: [] as UserDossier[],
    loading: false,
    error: null as string | null,
    loaded: false,
  }),

  actions: {
    async fetchDossiers(force = false) {
      if (this.loaded && !force) {
        return
      }

      this.loading = true
      this.error = null

      try {
        this.dossiers = await getUserDossiers()
        this.loaded = true
      } catch (err: any) {
        this.error = err.message || 'Failed to fetch dossiers'
        console.error('Error fetching dossiers:', err)
      } finally {
        this.loading = false
      }
    },

    getDossierById(id: number | string): UserDossier | undefined {
      // id can be a string or number, doing loose comparison or ensuring type match
      const numericId = Number(id)
      return this.dossiers.find((d) => d.id === numericId)
    },
  },
})
