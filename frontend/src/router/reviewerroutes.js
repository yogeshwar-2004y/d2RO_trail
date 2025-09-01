// src/router/reviewerRoutes.js

import HomePageReviewer from '@/views/reviewer/HomePageReviewer.vue'
import InspectionMemo from '@/views/reviewer/InspectionMemo.vue';
import ReviewerMemoDashboard from '@/views/reviewer/ReviewerMemoDashboard.vue';
import SharedMemoDashboard from '@/views/reviewer/SharedMemoDashboard.vue';
import SharedMemoView from '@/views/reviewer/SharedMemoView.vue';

const reviewerRoutes = [
  {
    path: "/reviewer/home",
    name: "HomePageReviewer",
    component: HomePageReviewer,
  },
  {
    path: "/reviewer/memo-dashboard",
    name: "ReviewerMemoDashboard",
    component: ReviewerMemoDashboard,
  },
  {
    path: "/reviewer/InspectionMemo/:id", // Dynamic path with memo ID parameter
    name: "InspectionMemo",
    component: InspectionMemo,
    props: true, // Enable props to pass route params as component props
  },
  {
    path: "/reviewer/shared-memos",
    name: "SharedMemoDashboard",
    component: SharedMemoDashboard,
  },
  {
    path: "/reviewer/shared-memo/:id", // Dynamic path for shared memo view
    name: "SharedMemoView",
    component: SharedMemoView,
    props: true, // Enable props to pass route params as component props
  },
];

export default reviewerRoutes