// src/router/qaheadroutes.js

import HomePageQAHead from '@/views/qahead/HomePageQAHead.vue'
import QAHeadProjectsDashboard from '@/views/qahead/QAHeadProjectsDashboard.vue'
import QAHeadLruDashboard from '@/views/qahead/QAHeadLruDashboard.vue'
import QAHeadLruDocumentView from '@/views/qahead/QAHeadLruDocumentView.vue'
import QAHeadDocumentVersionView from '@/views/qahead/QAHeadDocumentVersionView.vue'
import QAHeadAssignReviewer from '@/views/qahead/QAHeadAssignReviewer.vue'
import QAHeadViewObservations from '@/views/qahead/QAHeadViewObservations.vue'
import QAHeadMemoDashboard from '@/views/qahead/QAHeadMemoDashboard.vue'
import QAHeadMemoForm from '@/views/qahead/QAHeadMemoForm.vue'
import QAHeadReportDashboard from '@/views/qahead/QAHeadReportDashboard.vue'
import QAHeadNotifications from '@/views/qahead/QAHeadNotifications.vue'

const qaheadRoutes = [
  {
    path: '/qahead/home',
    name: 'HomePageQAHead',
    component: HomePageQAHead,
  },
  {
    path: '/qahead/projects',
    name: 'QAHeadProjectsDashboard',
    component: QAHeadProjectsDashboard,
  },
  {
    path: '/qahead/projects/:projectId/lrus',
    name: 'QAHeadLruDashboard',
    component: QAHeadLruDashboard,
  },
  {
    path: '/qahead/projects/:projectName/lrus/:lruName',
    name: 'QAHeadLruDocumentView',
    component: QAHeadLruDocumentView,
  },
  {
    path: '/qahead/projects/:projectName/lrus/:lruName/versions/:versionId',
    name: 'QAHeadDocumentVersionView',
    component: QAHeadDocumentVersionView,
  },
  {
    path: '/qahead/assign-reviewer',
    name: 'QAHeadAssignReviewer',
    component: QAHeadAssignReviewer,
  },
  {
    path: '/qahead/view-observations',
    name: 'QAHeadViewObservations',
    component: QAHeadViewObservations,
  },
  {
    path: '/qahead/memos',
    name: 'QAHeadMemoDashboard',
    component: QAHeadMemoDashboard,
  },
  {
    path: '/qahead/memos/:memoId',
    name: 'QAHeadMemoForm',
    component: QAHeadMemoForm,
  },
  {
    path: '/qahead/reports',
    name: 'QAHeadReportDashboard',
    component: QAHeadReportDashboard,
  },
  {
    path: '/qahead/notifications',
    name: 'QAHeadNotifications',
    component: QAHeadNotifications,
  },
];

export default qaheadRoutes;
