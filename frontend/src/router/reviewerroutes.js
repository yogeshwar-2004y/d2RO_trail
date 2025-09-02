// src/router/reviewerroutes.js

import HomePageReviewer from '@/views/reviewer/HomePageReviewer.vue'
import InspectionMemo from '@/views/reviewer/InspectionMemo.vue'
import ReviewerMemoDashboard from '@/views/reviewer/ReviewerMemoDashboard.vue'
import SharedMemoDashboard from '@/views/reviewer/SharedMemoDashboard.vue'
import SharedMemoView from '@/views/reviewer/SharedMemoView.vue'

const reviewerRoutes = [
  {
    path: '/reviewer',
    name: 'HomePageReviewer',
    component: HomePageReviewer,
  },
  {
    path: '/inspection-memo',
    name: 'InspectionMemo',
    component: InspectionMemo,
  },
  {
    path: '/memo-dashboard',
    name: 'ReviewerMemoDashboard',
    component: ReviewerMemoDashboard,
  },
  {
    path: '/shared-memos',
    name: 'SharedMemoDashboard',
    component: SharedMemoDashboard,
  },
    {
    path: '/shared-memo-view',
    name: 'SharedMemoView',
    component: SharedMemoView,
  },
]

export default reviewerRoutes
