import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useAdminModeStore = defineStore('adminMode', () => {
  const isAdminMode = ref(sessionStorage.getItem('protect_envi_admin_mode') === 'true')

  watch(isAdminMode, (newVal) => {
    sessionStorage.setItem('protect_envi_admin_mode', String(newVal))
  })

  function toggleAdminMode() {
    isAdminMode.value = !isAdminMode.value
  }

  function setAdminMode(value: boolean) {
    isAdminMode.value = value
  }

  return {
    isAdminMode,
    toggleAdminMode,
    setAdminMode,
  }
})
