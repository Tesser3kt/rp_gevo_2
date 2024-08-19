import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    currentUser: {
      userId: null,
      username: null,
      firstName: null,
      lastName: null,
      email: null
    }
  }),
  getters: {
    isAuthenticated: (state) => state.currentUser.userId !== null,
    getCurrentUser: (state) => state.currentUser
  },
  actions: {
    authAllowed(userData) {
      if (userData?.hd !== 'gevo.cz') return false
      return true
    },
    setCurrentUser(userData) {
      this.currentUser.userId = userData.userId
      this.currentUser.username = userData.username
      this.currentUser.firstName = userData.firstName
      this.currentUser.lastName = userData.lastName
      this.currentUser.email = userData.email
    }
  }
})
