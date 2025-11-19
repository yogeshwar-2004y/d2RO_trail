// src/router/qaheadroutes.js

import HomePageQAHead from '@/views/qahead/HomePageQAHead.vue'
import QAHeadDocumentVersionView from '@/views/qahead/QAHeadDocumentVersionView.vue'
import QAHeadAssignReviewer from '@/views/qahead/QAHeadAssignReviewer.vue'
import QAHeadNotifications from '@/views/qahead/QAHeadNotifications.vue'

const qaheadRoutes = [
  {
    path: '/qahead',
    name: 'HomePageQAHead',
    component: HomePageQAHead,
    meta: { requiresAuth: true } // All authenticated users
  },
  {
    path: '/qahead/projects/:projectName/lrus/:lruName/versions/:versionId',
    name: 'QAHeadDocumentVersionView',
    component: QAHeadDocumentVersionView,
    meta: { requiresAuth: true } // All authenticated users
  },
  {
    path: '/qahead/assign-reviewer',
    name: 'QAHeadAssignReviewer',
    component: QAHeadAssignReviewer,
    meta: { requiresAuth: true } // All authenticated users
  },
  {
    path: '/memos/notifications',
    name: 'QAHeadNotifications',
    component: QAHeadNotifications,
    meta: { requiresAuth: true } // All authenticated users
  },
];

export default qaheadRoutes;
