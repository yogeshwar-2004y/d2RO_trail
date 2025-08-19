// src/router/reviewerroutes.js

import HomePageReviewer from '@/views/reviewer/HomePageReviewer.vue'
import ReviewerProjectsDashboard from '@/views/reviewer/ReviewerProjectsDashboard.vue'
import ReviewerReports from '@/views/reviewer/ReviewerReports.vue'

const reviewerRoutes = [
  {
    path: '/reviewer/home',
    name: 'HomePageReviewer',
    component: HomePageReviewer,
  },
  {
    path: '/reviewer/projects',
    name: 'ReviewerProjectsDashboard',
    component: ReviewerProjectsDashboard,
  },
  {
    path: '/reviewer/reports',
    name: 'ReviewerReports',
    component: ReviewerReports,
  },
]

export default reviewerRoutes
