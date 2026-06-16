import { defineStore } from 'pinia'

export const useEditModeStore = defineStore('editMode', {
  state: () => ({
    isAdminMode: localStorage.getItem('protect_envi_admin_mode') === 'true',
  }),
  actions: {
    toggleAdminMode() {
      this.isAdminMode = !this.isAdminMode
      localStorage.setItem('protect_envi_admin_mode', String(this.isAdminMode))
    },
    setAdminMode(value: boolean) {
      this.isAdminMode = value
      localStorage.setItem('protect_envi_admin_mode', String(value))
    },
  },
})
