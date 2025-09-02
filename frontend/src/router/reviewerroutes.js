// src/router/reviewerRoutes.js

import HomePageReviewer from '@/views/reviewer/HomePageReviewer.vue'
import SharedMemoDashboard from '@/views/reviewer/SharedMemoDashboard.vue'
import SharedMemoView from '@/views/reviewer/SharedMemoView.vue'

const reviewerRoutes = [
  {
    path: '/reviewer',
    name: 'HomePageReviewer',
    component: HomePageReviewer,
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
];

export default reviewerRoutes