import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '@/views/LoginPage.vue'
import HomePageAdmin from '@/views/HomePageAdmin.vue'
import ProjectsDashboard from '@/views/ProjectsDashboard.vue'
import LruDashboard from '@/views/LruDashboard.vue'
import MemoDashboard from '@/views/MemoDashboard.vue'
import ReportDashboard from '@/views/ReportDashboard.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: LoginPage,
    },
    {
      path: '/admin',
      name: 'HomePageAdmin',
      component: HomePageAdmin,
    },
    {
      path: '/projects',
      name: 'ProjectsDashboard',
      component: ProjectsDashboard
    },
    {
      path: '/projects/:projectName/lrus', // New route for the LRU dashboard
      name: 'LruDashboard',
      component: LruDashboard
    },
    {
      path: '/memos',
      name: 'MemoDashboard',
      component: MemoDashboard
    },
    {
      path: '/reports',
      name: 'ReportDashboard',
      component: ReportDashboard
    },
  ],
})

export default router




// {
//   path: '/about',
//   name: 'about',
//   // route level code-splitting
//   // this generates a separate chunk (About.[hash].js) for this route
//   // which is lazy-loaded when the route is visited.
//   component: () => import('../views/AboutView.vue'),
// },