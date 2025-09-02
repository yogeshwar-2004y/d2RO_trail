// src/router/qaheadroutes.js

import HomePageDesignHead from '@/views/designhead/HomePageDesignHead.vue'
import ProjectsForAssigning from '@/views/designhead/ProjectsForAssigning.vue'
import ProjectMembers from '@/views/designhead/ProjectMembers.vue'
import AddMember from '@/views/designhead/AddMember.vue'

import SubmitMemo from '@/components/SubmitMemo.vue'

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
]

export default designheadRoutes
