import { createRouter, createWebHistory } from "vue-router";
import LoginPage from '@/views/LoginPage.vue'
import HomePageAdmin from '@/views/admin/HomePageAdmin.vue'
import ProjectsDashboard from '@/views/admin/ProjectsDashboard.vue'
import LruDashboard from '@/views/admin/LruDashboard.vue'
import MemoDashboard from '@/views/admin/MemoDashboard.vue'
import ReportDashboard from '@/views/admin/ReportDashboard.vue'
import UserActivities from '@/views/admin/UserActivities.vue'
import AddUpdateProjects from "@/views/admin/AddUpdateProjects.vue";
import reviewerRoutes from './reviewerroutes'
import qaheadRoutes from './qaheadroutes'
import designheadRoutes from './designhead'
import designerRoutes from './designer'
import ManageProjects from "@/views/admin/ManageProjects.vue";
import AddUpdateUser from "@/views/admin/AddUpdateUser.vue";
import ManageUsers from "@/views/admin/ManageUsers.vue";
import ActivityLogs from "@/views/admin/ActivityLogs.vue";
import TestsPage from "@/views/admin/TestsPage.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "login",
      component: LoginPage,
    },
    {
      path: "/activity-logs",
      name: "ActivityLogs",
      component: ActivityLogs
    },
    {
      path: "/add-update-projects",
      name: "AddUpdateProjects",
      component: AddUpdateProjects,
    },
    {
      path: "/add-update-users",
      name: "AddUpdateUser",
      component: AddUpdateUser
    },
    {
      path: "/admin",
      name: "HomePageAdmin",
      component: HomePageAdmin,
    },
    {
      path: "/manage-projects",
      name: "ManageProjects",
      component: ManageProjects
    },
    {
      path: "/manage-users",
      name: "ManageUsers",
      component: ManageUsers
    },
    {
      path: "/memos",
      name: "MemoDashboard",
      component: MemoDashboard,
    },
    {
      path: "/projects",
      name: "ProjectsDashboard",
      component: ProjectsDashboard,
    },
    {
      path: "/projects/:projectId/lrus",
      name: "LruDashboard",
      component: LruDashboard,
    },
    {
      path: "/reports",
      name: "ReportDashboard",
      component: ReportDashboard,
    },
    {
      path: "/tests",
      name: "TestsPage",
      component: TestsPage
    },
    {
      path: "/user-activities",
      name: "UserActivities",
      component: UserActivities,
    },
    ...reviewerRoutes,
    ...qaheadRoutes,
    ...designheadRoutes,
    ...designerRoutes,
  ],
});

export default router




// {
//   path: '/about',
//   name: 'about',
//   // route level code-splitting
//   // this generates a separate chunk (About.[hash].js) for this route
//   // which is lazy-loaded when the route is visited.
//   component: () => import('../views/AboutView.vue'),
// },