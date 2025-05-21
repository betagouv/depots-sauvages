import { defineStore } from 'pinia'
import { API_URLS, createResource, fetchResource, updateResource } from '../services/api'
import type { Signalement } from '../types/signalement'
import { createEmptySignalement, fromApiFormat, toApiFormat } from '../types/signalement'

export const useSignalementStore = defineStore('signalement', {
  // State
  state: () => ({
    currentStep: 1,
    currentId: null as number | null,
    formData: createEmptySignalement(),
  }),

  // Actions
  actions: {
    updateStep(step: number) {
      this.currentStep = step
    },

    resetStore() {
      this.currentStep = 1
      this.currentId = null
      this.formData = createEmptySignalement()
    },

    // Utils
    updateBooleanField(field: keyof Signalement, value: string) {
      if (typeof this.formData[field] === 'boolean') {
        this.formData[field] = (value === 'oui') as any
      }s
    },


    // API
    async saveFormData() {
      if (this.currentStep === 2) {
        this.formData.generateDoc = true
      }

      if (this.currentId) {
        return await updateResource(
          `${API_URLS.signalements}${this.currentId}/`,
          toApiFormat(this.formData)
        )
      } else {
        const data = await createResource(API_URLS.signalements, toApiFormat(this.formData))
        this.currentId = data.id
        return data
      }
    },

    async loadSignalement(id: number) {
      try {
        const data = await fetchResource(`${API_URLS.signalements}${id}/`)
        this.currentId = id
        this.formData = fromApiFormat(data)
      } catch (error) {
        console.error('Error loading signalement:', error)
        throw error
      }
    },
  },
})

export type SignalementStore = ReturnType<typeof useSignalementStore>
