import { defineStore } from 'pinia'
import type { UserInfo } from '../services/api'
import { getUserInfo } from '../services/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    userInfo: null as UserInfo | null,
    loading: false,
    error: null as string | null,
    loaded: false,
    _fetchPromise: null as Promise<UserInfo> | null,
  }),

  getters: {
    isAuthenticated: (state) => state.userInfo?.is_authenticated ?? false,
    isStaff: (state) => state.userInfo?.is_staff ?? false,
  },

  actions: {
    async fetchUserInfo(force = false): Promise<UserInfo> {
      if (this.loaded && !force && this.userInfo) return this.userInfo
      if (this._fetchPromise) return this._fetchPromise

      this.loading = true
      this._fetchPromise = getUserInfo()
        .then((info) => {
          this.userInfo = info
          this.loaded = true
          return info
        })
        .catch((error) => {
          this.error = 'Erreur lors de la récupération des informations utilisateur'
          console.error('Error fetching user info:', error)
          throw error
        })
        .finally(() => {
          this.loading = false
          this._fetchPromise = null
        })

      return this._fetchPromise
    },

    clearUser() {
      this.userInfo = null
      this.loaded = false
    },
  },
})
