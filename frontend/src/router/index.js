import { createRouter, createWebHistory } from "vue-router";
import LoginPage from '@/views/LoginPage.vue'
import HomePageAdmin from '@/views/admin/HomePageAdmin.vue'
import ProjectsDashboard from '@/views/admin/ProjectsDashboard.vue'
import LruDashboard from '@/views/admin/LruDashboard.vue'
import MemoDashboard from '@/views/admin/MemoDashboard.vue'
import ReportDashboard from '@/views/admin/ReportDashboard.vue'
import UserActivities from '@/views/admin/UserActivities.vue'
import reviewerRoutes from './reviewerroutes'
import qaheadRoutes from './qaheadroutes'
import designheadRoutes from './designhead'
import designerRoutes from './designer'

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
    {
      path: '/user-activities',
      name: 'UserActivities',
      component: UserActivities
    },
    ...reviewerRoutes ,
    ...qaheadRoutes,
    ...designheadRoutes,
    ...designerRoutes
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