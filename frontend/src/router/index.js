import { createRouter, createWebHistory } from "vue-router";

import reviewerRoutes from './reviewerroutes'
import qaheadRoutes from './qaheadroutes'
import designheadRoutes from './designhead'
import designerRoutes from './designer'

import LoginPage from '@/views/LoginPage.vue'
import HomePageAdmin from '@/views/admin/HomePageAdmin.vue'
import ProjectsDashboard from '@/components/ProjectsDashboard.vue'
import LruDashboard from '@/components/LruDashboard.vue'
import MemoDashboard from '@/components/MemoDashboard.vue'
import ReportDashboard from '@/components/ReportDashboard.vue'
import UserActivities from '@/views/admin/UserActivities.vue'
import AddUpdateProjects from "@/views/admin/AddUpdateProjects.vue";
import ManageProjects from "@/views/admin/ManageProjects.vue";
import AddUpdateUser from "@/views/admin/AddUpdateUser.vue";
import ManageUsers from "@/views/admin/ManageUsers.vue";
import SelectUserToEdit from "@/views/admin/SelectUserToEdit.vue";
import EditUser from "@/views/admin/EditUser.vue";
import SelectProjectToEdit from "@/views/admin/SelectProjectToEdit.vue";
import EditProject from "@/views/admin/EditProject.vue";
import ActivityLogs from "@/views/admin/ActivityLogs.vue";
import TestsPage from "@/views/admin/TestsPage.vue";
import ObservationReport from "@/components/ObservationReport.vue";
import MemoForm from "@/components/MemoForm.vue";
import DocumentViewer from "@/components/DocumentViewer.vue";
import SubmitMemo from '@/components/SubmitMemo.vue'
import RoleTestComponent from '@/components/RoleTestComponent.vue'
import PlanDocsTestComponent from '@/components/PlanDocsTestComponent.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "login",
      component: LoginPage,
    },
    {
      path: "/user-activities/activity-logs",
      name: "ActivityLogs",
      component: ActivityLogs
    },
    {
      path: "/user-activities/add-update-projects",
      name: "AddUpdateProjects",
      component: AddUpdateProjects,
    },
    {
      path: "/user-activities/add-update-users",
      name: "AddUpdateUser",
      component: AddUpdateUser
    },
    {
      path: "/admin",
      name: "HomePageAdmin",
      component: HomePageAdmin,
    },
    {
      path: "/user-activities/manage-projects",
      name: "ManageProjects",
      component: ManageProjects
    },
    {
      path: "/user-activities/manage-users",
      name: "ManageUsers",
      component: ManageUsers
    },
    {
      path: "/select-user-to-edit",
      name: "SelectUserToEdit",
      component: SelectUserToEdit
    },
    {
      path: "/edit-user/:userId",
      name: "EditUser",
      component: EditUser,
      props: true
    },
    {
      path: "/select-project-to-edit",
      name: "SelectProjectToEdit",
      component: SelectProjectToEdit
    },
    {
      path: "/edit-project/:projectId",
      name: "EditProject",
      component: EditProject,
      props: true
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
      path: "/user-activities/tests",
      name: "TestsPage",
      component: TestsPage
    },
    {
      path: "/user-activities",
      name: "UserActivities",
      component: UserActivities,
    },
    {
      path: "/reports/memo-id/:memoId",
      name: "TestReports",
      component: ObservationReport,
    },
    {
    path: '/reports/view-observations',
    name: 'ObservationReport',
    component: ObservationReport,
    },
    {
      path: '/memos/:memoId',
      name: 'MemoForm',
      component: MemoForm,
    },
    {
    path: '/document-viewer',
    name: 'DocumentViewer',
    component: DocumentViewer,
    },
    {
    path: '/memos/submit',
    name: 'SubmitMemo',             
    component: SubmitMemo,
    },
          {
        path: '/test-role-system',
        name: 'RoleTestComponent',
        component: RoleTestComponent,
      },
      {
        path: '/test-plan-docs',
        name: 'PlanDocsTestComponent',
        component: PlanDocsTestComponent,
      },
    ...reviewerRoutes,
    ...qaheadRoutes,
    ...designheadRoutes,
    ...designerRoutes,
  ],
  
});

export default router
