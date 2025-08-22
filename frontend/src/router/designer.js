// src/router/qaheadroutes.js

import HomePageDesigner from '@/views/designer/HomePageDesigner.vue'
import DocumentsPage from '@/views/designer/DocumentsPage.vue'
import PlanDocumentsPage from '@/views/designer/PlanDocumentsPage.vue'
import MemoPage from '@/views/designer/MemoPage.vue'
import NewMemoForm from '@/views/designer/NewMemoForm.vue'
import TestReportsPage from '@/views/designer/TestReportsPage.vue'

const routes = [
  {
    path: '/designer',
    name: 'HomePageDesigner',
    component: HomePageDesigner
  },
  {
    path: '/designer/documents',
    name: 'DesignerDocuments',
    component: DocumentsPage
  },
  {
    path: '/designer/plan-documents/:projectId',
    name: 'DesignerPlanDocuments',
    component: PlanDocumentsPage,
    props: true
  },
  {
    path: '/designer/memo',
    name: 'DesignerMemo',
    component: MemoPage
  },
  {
    path: '/designer/new-memo',
    name: 'DesignerNewMemo',
    component: NewMemoForm
  },
  {
    path: '/designer/test-reports',
    name: 'DesignerTestReports',
    component: TestReportsPage
  }
]

export default routes
