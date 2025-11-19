import { createRouter, createWebHistory } from "vue-router";
import { userStore } from "@/stores/userStore";

import reviewerRoutes from './reviewerroutes'
import qaheadRoutes from './qaheadroutes'
import designheadRoutes from './designhead'
import designerRoutes from './designer'

import LoginPage from '@/views/LoginPage.vue'
import TechSupportPage from '@/views/TechSupportPage.vue'
import TechSupportUserDashboard from '@/views/TechSupportUserDashboard.vue'
import HomePageAdmin from '@/views/admin/HomePageAdmin.vue'
import ProjectsDashboard from '@/components/ProjectsDashboard.vue'
import LruDashboard from '@/components/LruDashboard.vue'
import MemoDashboard from '@/components/MemoDashboard.vue'
import ReportDashboard from '@/components/ReportDashboard.vue'
import IndividualReport from '@/components/IndividualReport.vue'
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
import LoginLogs from "@/views/admin/LoginLogs.vue";
import MajorTestGroups from "@/views/admin/MajorTestGroups.vue";
import ManufacturingTestGroup from "@/views/admin/ManufacturingTestGroup.vue";
import CoTSScreeningTestGroup from "@/views/admin/CoTSScreeningTestGroup.vue";
import ESSTestGroup from "@/views/admin/ESSTestGroup.vue";
import QTTestGroup from "@/views/admin/QTTestGroup.vue";
import SoFTTestGroup from "@/views/admin/SoFTTestGroup.vue";
import TestManagement from "@/components/TestManagement.vue";
import GroupDetail from "@/components/GroupDetail.vue";
import SubTestDetail from "@/components/SubTestDetail.vue";
import NewsUpdates from "@/views/admin/NewsUpdates.vue";
import CustomiseBackground from "@/views/admin/CustomiseBackground.vue";
import TechSupportManagement from "@/views/admin/TechSupportManagement.vue";
import DocumentTypes from "@/views/designhead/DocumentTypes.vue";
import ObservationReport from "@/components/ObservationReport.vue";
import MemoForm from "@/components/MemoForm.vue";
import ViewOnlyMemoForm from "@/components/ViewOnlyMemoForm.vue";
import DocumentViewer from "@/components/DocumentViewer.vue";
import SubmitMemo from '@/components/SubmitMemo.vue'
import RoleTestComponent from '@/components/RoleTestComponent.vue'
import PlanDocsTestComponent from '@/components/PlanDocsTestComponent.vue'
import TemplateDashboard from '@/components/TemplateDashboard.vue'
import TemplateViewer from '@/components/TemplateViewer.vue'
import BarePcbInspectionReport from '@/templates/barepcbinspectionreport.vue'
import Conformalcoatinginspectionreport from '@/templates/Conformalcoatinginspectionreport.vue'
import RawMaterialInspectionReport from '@/templates/RawMaterialInspectionReport.vue'
import CotsScreeningInspectionReport from '@/templates/CotsScreeningInspectionReport.vue'
import AssembledBoardInspectionReport from '@/templates/AssembledBoardInspectionReport.vue'
import KitOfPartInsp from '@/templates/KitOfPartInsp.vue'
import MechanicalInspection from '@/templates/MechanicalInspection.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "login",
      component: LoginPage,
      meta: { requiresAuth: false } // Public route
    },
    {
      path: "/tech-support",
      name: "TechSupport",
      component: TechSupportPage,
      meta: { requiresAuth: false } // Public route
    },
    {
      path: "/my-tech-support",
      name: "TechSupportUserDashboard",
      component: TechSupportUserDashboard,
      meta: { requiresAuth: true } // Authenticated users only
    },
    {
      path: "/user-activities/activity-logs",
      name: "ActivityLogs",
      component: ActivityLogs,
      meta: { requiresAuth: true, requiresRole: 1 } // Admin only
    },
    {
      path: "/user-activities/login-logs",
      name: "LoginLogs",
      component: LoginLogs,
      meta: { requiresAuth: true, requiresRole: 1 } // Admin only
    },
    {
      path: "/user-activities/add-update-projects",
      name: "AddUpdateProjects",
      component: AddUpdateProjects,
      meta: { requiresAuth: true, requiresRole: 1 } // Admin only
    },
    {
      path: "/user-activities/add-update-users",
      name: "AddUpdateUser",
      component: AddUpdateUser,
      meta: { requiresAuth: true, requiresRole: 1 } // Admin only
    },
    {
      path: "/admin",
      name: "HomePageAdmin",
      component: HomePageAdmin,
      meta: { requiresAuth: true, requiresRole: 1 } // Admin only
    },
    {
      path: "/user-activities/manage-projects",
      name: "ManageProjects",
      component: ManageProjects,
      meta: { requiresAuth: true, requiresRole: 1 } // Admin only
    },
    {
      path: "/user-activities/manage-users",
      name: "ManageUsers",
      component: ManageUsers,
      meta: { requiresAuth: true, requiresRole: 1 } // Admin only
    },
    {
      path: "/user-activities/document-types",
      name: "DocumentTypes",
      component: DocumentTypes,
      meta: { requiresAuth: true, requiresRole: 1 } // Admin only
    },
    {
      path: "/select-user-to-edit",
      name: "SelectUserToEdit",
      component: SelectUserToEdit,
      meta: { requiresAuth: true, requiresRole: 1 } // Admin only
    },
    {
      path: "/edit-user/:userId",
      name: "EditUser",
      component: EditUser,
      props: true,
      meta: { requiresAuth: true, requiresRole: 1 } // Admin only
    },
    {
      path: "/select-project-to-edit",
      name: "SelectProjectToEdit",
      component: SelectProjectToEdit,
      meta: { requiresAuth: true, requiresRole: 1 } // Admin only
    },
    {
      path: "/edit-project/:projectId",
      name: "EditProject",
      component: EditProject,
      props: true,
      meta: { requiresAuth: true, requiresRole: 1 } // Admin only
    },
    {
      path: "/memos",
      name: "MemoDashboard",
      component: MemoDashboard,
      meta: { requiresAuth: true } // All authenticated users
    },
    {
      path: "/projects",
      name: "ProjectsDashboard",
      component: ProjectsDashboard,
      meta: { requiresAuth: true } // All authenticated users
    },
    {
      path: "/projects/:projectId/lrus",
      name: "LruDashboard",
      component: LruDashboard,
      meta: { requiresAuth: true } // All authenticated users
    },
    {
      path: "/reports",
      name: "ReportDashboard",
      component: ReportDashboard,
      meta: { requiresAuth: true } // All authenticated users
    },
    {
      path: "/reports/individual/:reportId",
      name: "IndividualReport",
      component: IndividualReport,
      props: true,
      meta: { requiresAuth: true } // All authenticated users
    },
    {
      path: "/user-activities/major-test-groups",
      name: "MajorTestGroups",
      component: MajorTestGroups,
      meta: { requiresAuth: true, requiresRole: 1 } // Admin only
    },
    {
      path: "/user-activities/test-management",
      name: "TestManagement",
      component: TestManagement,
      meta: { requiresAuth: true, requiresRole: 1 } // Admin only
    },
    {
      path: "/user-activities/test-management/group/:groupId/:groupName",
      name: "GroupDetail",
      component: GroupDetail,
      props: true,
      meta: { requiresAuth: true, requiresRole: 1 } // Admin only
    },
    {
      path: "/user-activities/test-management/group/:groupId/:groupName/sub-test/:subTestId/:subTestName",
      name: "SubTestDetail",
      component: SubTestDetail,
      props: true,
      meta: { requiresAuth: true, requiresRole: 1 } // Admin only
    },
    {
      path: "/user-activities/manufacturing-test-group",
      name: "ManufacturingTestGroup",
      component: ManufacturingTestGroup,
      meta: { requiresAuth: true, requiresRole: 1 } // Admin only
    },
    {
      path: "/user-activities/cots-screening-test-group",
      name: "CoTSScreeningTestGroup",
      component: CoTSScreeningTestGroup,
      meta: { requiresAuth: true, requiresRole: 1 } // Admin only
    },
    {
      path: "/user-activities/ess-test-group",
      name: "ESSTestGroup",
      component: ESSTestGroup,
      meta: { requiresAuth: true, requiresRole: 1 } // Admin only
    },
    {
      path: "/user-activities/qt-test-group",
      name: "QTTestGroup",
      component: QTTestGroup,
      meta: { requiresAuth: true, requiresRole: 1 } // Admin only
    },
    {
      path: "/user-activities/soft-test-group",
      name: "SoFTTestGroup",
      component: SoFTTestGroup,
      meta: { requiresAuth: true, requiresRole: 1 } // Admin only
    },
    {
      path: "/user-activities/news-updates",
      name: "NewsUpdates",
      component: NewsUpdates,
      meta: { requiresAuth: true, requiresRole: 1 } // Admin only
    },
    {
      path: "/user-activities/customise-background",
      name: "CustomiseBackground",
      component: CustomiseBackground,
      meta: { requiresAuth: true, requiresRole: 1 } // Admin only
    },
    {
      path: "/user-activities/tech-support",
      name: "TechSupportManagement",
      component: TechSupportManagement,
      meta: { requiresAuth: true, requiresRole: 1 } // Admin only
    },
    {
      path: "/user-activities",
      name: "UserActivities",
      component: UserActivities,
      meta: { requiresAuth: true, requiresRole: 1 } // Admin only
    },
    {
      path: "/reports/memo-id/:memoId",
      name: "TestReports",
      component: ObservationReport,
      meta: { requiresAuth: true } // All authenticated users
    },
    {
    path: '/view-observations/:lruId/:lruName/:projectId',
    name: 'ObservationReport',
    component: ObservationReport,
    meta: { requiresAuth: true } // All authenticated users
    },
    {
      path: '/memos/:memoId',
      name: 'MemoForm',
      component: MemoForm,
      meta: { requiresAuth: true } // All authenticated users
    },
    {
      path: '/memos/view/:id',
      name: 'ViewOnlyMemoForm',
      component: ViewOnlyMemoForm,
      props: true,
      meta: { requiresAuth: true } // All authenticated users
    },
    {
      path: '/memos/submit/new',
      name: 'NewMemoForm',
      component: MemoForm,
      meta: { requiresAuth: true } // All authenticated users
    },
    {
    path: '/document-viewer/:lruId/:lruName/:projectId',
    name: 'DocumentViewer',
    component: DocumentViewer,
    meta: { requiresAuth: true } // All authenticated users
    },
    {
    path: '/memos/submit',
    name: 'SubmitMemo',             
    component: SubmitMemo,
    meta: { requiresAuth: true } // All authenticated users
    },
          {
        path: '/test-role-system',
        name: 'RoleTestComponent',
        component: RoleTestComponent,
        meta: { requiresAuth: true } // All authenticated users
      },
      {
        path: '/test-plan-docs',
        name: 'PlanDocsTestComponent',
        component: PlanDocsTestComponent,
        meta: { requiresAuth: true } // All authenticated users
      },
      {
        path: '/reports/templates',
        name: 'TemplateDashboard',
        component: TemplateDashboard,
        meta: { requiresAuth: true } // All authenticated users
      },
      {
        path: '/templates/view/:templateName',
        name: 'TemplateViewer',
        component: TemplateViewer,
        props: true,
        meta: { requiresAuth: true } // All authenticated users
      },
      {
        path: '/templates/bare-pcb-inspection/:projectName?/:lruName?',
        name: 'BarePcbInspectionReport',
        component: BarePcbInspectionReport,
        props: true,
        meta: { requiresAuth: true } // All authenticated users
      },
      {
        path: '/templates/conformal-coating-inspection/:projectName?/:lruName?',
        name: 'Conformalcoatinginspectionreport',
        component: Conformalcoatinginspectionreport,
        props: true,
        meta: { requiresAuth: true } // All authenticated users
      },
      {
        path: '/templates/raw-material-inspection/:projectName?/:lruName?',
        name: 'RawMaterialInspectionReport',
        component: RawMaterialInspectionReport,
        props: true,
        meta: { requiresAuth: true } // All authenticated users
      },
      {
        path: '/templates/cots-screening-inspection/:projectName?/:lruName?',
        name: 'CotsScreeningInspectionReport',
        component: CotsScreeningInspectionReport,
        props: true,
        meta: { requiresAuth: true } // All authenticated users
      },
      {
        path: '/templates/assembled-board-inspection/:projectName?/:lruName?',
        name: 'AssembledBoardInspectionReport',
        component: AssembledBoardInspectionReport,
        props: true,
        meta: { requiresAuth: true } // All authenticated users
      },
      {
        path: '/templates/kit-of-part-inspection/:projectName?/:lruName?',
        name: 'KitOfPartInsp',
        component: KitOfPartInsp,
        props: true,
        meta: { requiresAuth: true } // All authenticated users
      },
      {
        path: '/templates/mechanical-inspection/:projectName?/:lruName?',
        name: 'MechanicalInspection',
        component: MechanicalInspection,
        props: true,
        meta: { requiresAuth: true } // All authenticated users
      },
    ...reviewerRoutes,
    ...qaheadRoutes,
    ...designheadRoutes,
    ...designerRoutes,
  ],
  
});

// Navigation guard for authentication and role-based access
router.beforeEach((to, from, next) => {
  // Initialize user from localStorage if not already initialized
  // This ensures we have the latest state even if the store wasn't initialized yet
  if (!userStore.state.isLoggedIn) {
    userStore.actions.initializeUser();
  }
  
  // Get authentication state - check both store and localStorage as fallback
  let isLoggedIn = userStore.getters.isLoggedIn();
  let userRole = userStore.getters.currentUserRole();
  
  // Fallback to localStorage if store values are not available
  if (!isLoggedIn) {
    const storedIsLoggedIn = localStorage.getItem("isLoggedIn");
    const storedRole = localStorage.getItem("currentUserRole");
    if (storedIsLoggedIn === "true") {
      isLoggedIn = true;
      userRole = storedRole ? parseInt(storedRole) : null;
    }
  }
  
  // Check if route explicitly requires authentication
  // Routes with meta.requiresAuth === false are public, others require auth
  // Check all matched route records for meta information
  const requiresAuth = to.matched.some(record => {
    const meta = record.meta || {};
    return meta.requiresAuth !== false; // Default to requiring auth if not explicitly set to false
  });
  
  // If route requires auth and user is not logged in, redirect to login
  if (requiresAuth && !isLoggedIn) {
    // Store the intended destination
    next({
      name: 'login',
      query: { redirect: to.fullPath }
    });
    return;
  }
  
  // If user is logged in and trying to access login page, redirect to their dashboard
  if (to.name === 'login' && isLoggedIn) {
    // Redirect based on role
    if (userRole === 1) {
      next({ name: 'HomePageAdmin' });
    } else if (userRole === 2) {
      next({ name: 'HomePageQAHead' });
    } else if (userRole === 3) {
      next({ name: 'HomePageReviewer' });
    } else if (userRole === 4) {
      next({ name: 'HomePageDesignHead' });
    } else if (userRole === 5) {
      next({ name: 'HomePageDesigner' });
    } else {
      next();
    }
    return;
  }
  
  // Check role-based access
  // Find the first route record that specifies a required role
  const routeWithRole = to.matched.find(record => record.meta && record.meta.requiresRole !== undefined);
  const requiresRole = routeWithRole?.meta?.requiresRole;
  
  if (requiresRole !== undefined && isLoggedIn) {
    if (userRole !== requiresRole) {
      // User doesn't have required role, redirect to their dashboard
      alert('You do not have permission to access this page.');
      if (userRole === 1) {
        next({ name: 'HomePageAdmin' });
      } else if (userRole === 2) {
        next({ name: 'HomePageQAHead' });
      } else if (userRole === 3) {
        next({ name: 'HomePageReviewer' });
      } else if (userRole === 4) {
        next({ name: 'HomePageDesignHead' });
      } else if (userRole === 5) {
        next({ name: 'HomePageDesigner' });
      } else {
        next({ name: 'login' });
      }
      return;
    }
  }
  
  // Allow navigation
  next();
});

export default router
