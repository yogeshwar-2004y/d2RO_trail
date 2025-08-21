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
    path: '/projects-for-assigning',
    name: 'ProjectsForAssigning',
    component: ProjectsForAssigning,
  },
  {
    path: '/assign-projects/:projectId/members',
    name: 'ProjectMembers',
    component: ProjectMembers,
  },
  {
    path: '/design-head/assign-projects/:projectId/members/add',
    name: 'AddMember',
    component: AddMember,
  },
  {
    path: '/design-head/lrus/:lruId/documents/:documentId',
    name: 'DocumentViewer',
    component: DocumentViewer,
  },
  {
    path: '/design-head/memos/submit',
    name: 'SubmitMemo',
    component: SubmitMemo,
  },
]

export default designheadRoutes
