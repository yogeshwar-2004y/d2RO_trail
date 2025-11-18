// src/router/qaheadroutes.js

import HomePageDesigner from '@/views/designer/HomePageDesigner.vue'
import IqaObservationReport from '@/views/designer/IqaObservationReport.vue'

const routes = [
  {
    path: '/designer',
    name: 'HomePageDesigner',
    component: HomePageDesigner,
    meta: { requiresAuth: true } // All authenticated users
  },
  {
    path: '/designer/iqa-observation-report/:reportId',
    name: 'DesignerIqaObservationReport',
    component: IqaObservationReport,
    props: true,
    meta: { requiresAuth: true } // All authenticated users
  }
]

export default routes
