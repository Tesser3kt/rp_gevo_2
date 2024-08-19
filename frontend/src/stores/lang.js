import { defineStore } from 'pinia'

export const useLangStore = defineStore('lang', {
  state: () => ({
    lang: 'en'
  }),
  getters: {
    getLang: (state) => state.lang
  },
  actions: {
    setLang(lang) {
      this.lang = lang
    }
  }
})
