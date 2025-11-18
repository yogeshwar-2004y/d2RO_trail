// src/router/reviewerRoutes.js

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
    meta: { requiresAuth: true } // All authenticated users
  },
  {
    path: '/reviewer/memo-dashboard',
    name: 'ReviewerMemoDashboard',
    component: ReviewerMemoDashboard,
    meta: { requiresAuth: true } // All authenticated users
  },
  {
    path: '/reviewer/InspectionMemo/:id',
    name: 'InspectionMemo',
    component: InspectionMemo,
    props: true,
    meta: { requiresAuth: true } // All authenticated users
  },
  {
    path: '/memos/shared-memos',
    name: 'SharedMemoDashboard',
    component: SharedMemoDashboard,
    meta: { requiresAuth: true } // All authenticated users
  },
  {
    path: '/shared-memo-view/:id',
    name: 'SharedMemoView',
    component: SharedMemoView,
    props: true,
    meta: { requiresAuth: true } // All authenticated users
  },
];

export default reviewerRoutes