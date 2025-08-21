// src/router/qaheadroutes.js

import HomePageQAHead from '@/views/qahead/HomePageQAHead.vue'
import QAHeadProjectsDashboard from '@/views/qahead/QAHeadProjectsDashboard.vue'
import QAHeadLruDashboard from '@/views/qahead/QAHeadLruDashboard.vue'
import QAHeadMemoDashboard from '@/views/qahead/QAHeadMemoDashboard.vue'
import QAHeadReportDashboard from '@/views/qahead/QAHeadReportDashboard.vue'

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
    path: '/qahead/projects/:projectName/lrus',
    name: 'QAHeadLruDashboard',
    component: QAHeadLruDashboard,
  },
  {
    path: '/qahead/memos',
    name: 'QAHeadMemoDashboard',
    component: QAHeadMemoDashboard,
  },
  {
    path: '/qahead/reports',
    name: 'QAHeadReportDashboard',
    component: QAHeadReportDashboard,
  },
]

export default qaheadRoutes
