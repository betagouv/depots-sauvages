import { defineStore } from 'pinia'
import type { UserSignalement } from '../services/api'
import { getUserSignalements, syncDossiers } from '../services/api'

export const useDossierStore = defineStore('dossier', {
  state: () => ({
    dossiers: [] as UserSignalement[],
    loading: false,
    error: null as string | null,
    loaded: false,
    isSynced: false,
    syncing: false,
    _fetchPromise: null as Promise<void> | null,
  }),

  actions: {
    async fetchDossiers(force = false) {
      if (this.loaded && !force) return
      if (this._fetchPromise) return this._fetchPromise

      this._fetchPromise = (async () => {
        this.loading = true
        try {
          const dossiers = await getUserSignalements()
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
    async syncDossiers(force = false) {
      if (this.isSynced && !force) {
        return
      }
      this.syncing = true
      try {
        await syncDossiers()
        this.isSynced = true
        // If it was forced, we should reload the data afterwards
        if (force) {
          this.loaded = false
          await this.fetchDossiers(true)
        }
      } catch (error) {
        console.error('Error syncing dossiers:', error)
      } finally {
        this.syncing = false
      }
    },

    getDossierById(id: number | string): UserSignalement | undefined {
      // We look up by numero_dossier (DN ID) which is what is passed in the URL
      const numericId = Number(id)
      return this.dossiers.find((d) => d.numero_dossier === numericId)
    },
  },
})
