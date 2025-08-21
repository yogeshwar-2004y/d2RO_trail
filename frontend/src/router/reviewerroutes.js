// src/router/reviewerroutes.js

import HomePageReviewer from '@/views/reviewer/HomePageReviewer.vue'
/**import ReviewerProjectsDashboard from '@/views/reviewer/ReviewerProjectsDashboard.vue'
import ReviewerReports from '@/views/reviewer/ReviewerReports.vue'
import ProjectsDashboard from "@/views/admin/ProjectsDashboard.vue";
import LruDashboard from "@/views/admin/LruDashboard.vue";
import MemoDashboard from "@/views/admin/MemoDashboard.vue";
import ReportDashboard from "@/views/admin/ReportDashboard.vue";*/

const reviewerRoutes = [
  {
    path: "/reviewer/home",
    name: "HomePageReviewer",
    component: HomePageReviewer,
  },
  /**{
    path: "/reviewer/projects",
    name: "ReviewerProjectsDashboard",
    component: ReviewerProjectsDashboard,
  },
  {
    path: "/reviewer/reports",
    name: "ReviewerReports",
    component: ReviewerReports,
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
    path: "/projects/:projectName/lrus",
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
    component: TestsPage,
  },*/
];

export default reviewerRoutes
