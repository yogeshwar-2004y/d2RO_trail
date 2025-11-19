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
    meta: { requiresAuth: true, requiresRole: 4 } // Design Head only
  },
  {
    path: '/assign-projects',
    name: 'ProjectsForAssigning',
    component: ProjectsForAssigning,
    meta: { requiresAuth: true, requiresRole: 4 } // Design Head only
  },
  {
    path: '/assign-projects/:projectId/members',
    name: 'ProjectMembers',
    component: ProjectMembers,
    meta: { requiresAuth: true, requiresRole: 4 } // Design Head only
  },
  {
    path: '/assign-projects/:projectId/members/add',
    name: 'AddMember',
    component: AddMember,
    meta: { requiresAuth: true, requiresRole: 4 } // Design Head only
  },
]

export default designheadRoutes
