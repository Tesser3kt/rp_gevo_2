import '../node_modules/bulma/css/bulma.min.css'
import './assets/style.scss'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import axios from 'axios'
import GoogleSignInPlugin from 'vue3-google-signin'

import App from './App.vue'
import router from './router'
import VueCookies from 'vue-cookies'

axios.defaults.baseURL = import.meta.env.VITE_API_URL
axios.defaults.withCredentials = true
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.withXSRFToken = true
axios.defaults.headers.common['Content-Type'] = 'application/json'
axios.defaults.headers.common['Language'] = 'en'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(VueCookies)
app.use(GoogleSignInPlugin, {
  clientId: import.meta.env.VITE_GOOGLE_CLIENT_ID
})

app.mount('#app')
