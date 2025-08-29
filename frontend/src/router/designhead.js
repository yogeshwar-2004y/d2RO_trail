// src/router/qaheadroutes.js

import HomePageDesignHead from '@/views/designhead/HomePageDesignHead.vue'
import ProjectsForAssigning from '@/views/designhead/ProjectsForAssigning.vue'
import ProjectMembers from '@/views/designhead/ProjectMembers.vue'
import AddMember from '@/views/designhead/AddMember.vue'
import DocumentViewer from '@/views/designhead/DocumentViewer.vue'
import SubmitMemo from '@/views/designhead/SubmitMemo.vue'

const designheadRoutes = [
  {
    path: '/designhead',
    name: 'HomePageDesignHead',
    component: HomePageDesignHead,
  },
  {
    path: '/assign-projects',
    name: 'ProjectsForAssigning',
    component: ProjectsForAssigning,
  },
  {
    path: '/assign-projects/:projectId/members',
    name: 'ProjectMembers',
    component: ProjectMembers,
  },
  {
    path: '/assign-projects/:projectId/members/add',
    name: 'AddMember',
    component: AddMember,
  },
  {
    path: '/document-viewer',
    name: 'DocumentViewer',
    component: DocumentViewer,
  },
  {
    path: '/memos/submit',
    name: 'SubmitMemo',             
    component: SubmitMemo,
  },
]

export default designheadRoutes
