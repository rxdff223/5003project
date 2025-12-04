import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: DashboardView
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/UserProfileView.vue')
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('../views/AdminPanelView.vue')
    }
  ]
})

export default router
