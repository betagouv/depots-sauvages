import { defineStore } from 'pinia'
import type { UserDossier } from '../services/api'
import { getUserDossiers } from '../services/api'

export const useDossierStore = defineStore('dossier', {
  state: () => ({
    dossiers: [] as UserDossier[],
    loading: false,
    error: null as string | null,
    loaded: false,
  }),

  actions: {
    async fetchDossiers() {
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
      }
    },

    getDossierById(id: number | string): UserDossier | undefined {
      // id can be a string or number, doing loose comparison or ensuring type match
      const numericId = Number(id)
      return this.dossiers.find((d) => d.id === numericId)
    },
  },
})
