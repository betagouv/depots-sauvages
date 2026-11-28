import { defineStore } from 'pinia'
import type { UserInfo } from '../services/api'
import { getUserInfo } from '../services/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    userInfo: null as UserInfo | null,
    teamId: null as number | null,
    teamName: null as string | null,
    teamLogo: null as string | null,
    teamSiret: null as string | null,
    loading: false,
    error: null as string | null,
    loaded: false,
    _fetchPromise: null as Promise<UserInfo> | null,
  }),

  getters: {
    isAuthenticated: (state) => state.userInfo?.is_authenticated ?? false,
    isStaff: (state) => state.userInfo?.is_staff ?? false,
    hasTeam: (state) => state.teamId !== null,
    userDisplayName: (state): string | null => {
      if (!state.userInfo) return null
      const fullName = [state.userInfo.first_name, state.userInfo.last_name]
        .map((part) => (part ?? '').trim())
        .filter(Boolean)
        .join(' ')
      if (fullName) return fullName
      if (state.userInfo.email) return state.userInfo.email.trim()
      return null
    },
  },

  actions: {
    async fetchUserInfo(force = false): Promise<UserInfo> {
      if (this.loaded && !force && this.userInfo) return this.userInfo
      if (this._fetchPromise) return this._fetchPromise

      this.loading = true
      this._fetchPromise = getUserInfo()
        .then((info) => {
          this.userInfo = info
          this.teamId = info.team_id ?? null
          this.teamName = info.team_name ?? null
          this.teamLogo = info.team_logo ?? null
          this.teamSiret = info.team_siret ?? null
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
      this.teamId = null
      this.teamName = null
      this.teamLogo = null
      this.teamSiret = null
      this.loaded = false
    },
  },
})
