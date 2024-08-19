import axios from 'axios'
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useLangStore } from '@/stores/lang'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    }
  ]
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const langStore = useLangStore()

  axios.defaults.headers.common['Language'] = langStore.getLang
  if (to.name !== 'login' && !authStore.isAuthenticated) {
    next({ name: 'login' })
  } else {
    next()
  }
})

export default router
