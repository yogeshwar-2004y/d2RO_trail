<template>
  <nav class="breadcrumb-nav" v-if="breadcrumbs.length > 0">
    <div class="breadcrumb-container">
      <ol class="breadcrumb-list">
        <li 
          v-for="(breadcrumb, index) in breadcrumbs" 
          :key="index"
          class="breadcrumb-item"
          :class="{ 'active': index === breadcrumbs.length - 1 }"
        >
          <router-link 
            v-if="index < breadcrumbs.length - 1 && breadcrumb.path"
            :to="breadcrumb.path"
            class="breadcrumb-link"
          >
            {{ breadcrumb.name }}
          </router-link>
          <span v-else class="breadcrumb-current">
            {{ breadcrumb.name }}
          </span>
          <span 
            v-if="index < breadcrumbs.length - 1" 
            class="breadcrumb-separator"
          >
            /
          </span>
        </li>
      </ol>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { userStore } from '@/stores/userStore'

const route = useRoute()
const router = useRouter()

// Define route mappings for better breadcrumb names
const routeMappings = {
  'HomePageAdmin': 'Admin Dashboard',
  'HomePageReviewer': 'Reviewer Dashboard',
  'HomePageQAHead': 'QA Head Dashboard',
  'HomePageDesignHead': 'Design Head Dashboard',
  'HomePageDesigner': 'Designer Dashboard',
  'ProjectsDashboard': 'Projects',
  'LruDashboard': 'LRUs',
  'MemoDashboard': 'Memos',
  'ReportDashboard': 'Reports',
  'IndividualReport': 'Report Details',
  'UserActivities': 'User Activities',
  'AddUpdateProjects': 'Add/Update Projects',
  'ManageProjects': 'Manage Projects',
  'AddUpdateUser': 'Add/Update Users',
  'ManageUsers': 'Manage Users',
  'SelectUserToEdit': 'Select User',
  'EditUser': 'Edit User',
  'SelectProjectToEdit': 'Select Project',
  'EditProject': 'Edit Project',
  'ActivityLogs': 'Activity Logs',
  'MajorTestGroups': 'Major Test Groups',
  'ManufacturingTestGroup': 'Manufacturing Test Group',
  'CoTSScreeningTestGroup': 'COTS Screening Test Group',
  'ESSTestGroup': 'ESS Test Group',
  'QTTestGroup': 'QT Test Group',
  'SoFTTestGroup': 'SoFT Test Group',
  'NewsUpdates': 'News Updates',
  'CustomiseBackground': 'Customize Background',
  'ReviewerMemoDashboard': 'Memo Dashboard',
  'InspectionMemo': 'Inspection Memo',
  'SharedMemoDashboard': 'Shared Memos',
  'SharedMemoView': 'Shared Memo',
  'QAHeadDocumentVersionView': 'Document Version',
  'QAHeadAssignReviewer': 'Assign Reviewer',
  'QAHeadNotifications': 'Notifications',
  'ProjectsForAssigning': 'Assign Projects',
  'ProjectMembers': 'Project Members',
  'AddMember': 'Add Member',
  'DesignerIqaObservationReport': 'IQA Observation Report',
  'TestReports': 'Test Reports',
  'ObservationReport': 'Observation Report',
  'MemoForm': 'Memo Form',
  'ViewOnlyMemoForm': 'View Memo',
  'NewMemoForm': 'New Memo',
  'DocumentViewer': 'Document Viewer',
  'SubmitMemo': 'Submit Memo',
  'RoleTestComponent': 'Role Test',
  'PlanDocsTestComponent': 'Plan Docs Test',
  'TemplateDashboard': 'Templates',
  'TemplateViewer': 'Template Viewer',
  'BarePcbInspectionReport': 'Bare PCB Inspection',
  'Conformalcoatinginspectionreport': 'Conformal Coating Inspection',
  'RawMaterialInspectionReport': 'Raw Material Inspection',
  'CotsScreeningInspectionReport': 'COTS Screening Inspection',
  'AssembledBoardInspectionReport': 'Assembled Board Inspection',
  'KitOfPartInsp': 'Kit of Parts Inspection',
  'MechanicalInspection': 'Mechanical Inspection'
}

// Define parent-child relationships for hierarchical breadcrumbs
const routeHierarchy = {
  '/admin': 'HomePageAdmin',
  '/reviewer': 'HomePageReviewer',
  '/qahead': 'HomePageQAHead',
  '/designhead': 'HomePageDesignHead',
  '/designer': 'HomePageDesigner',
  '/user-activities': 'UserActivities',
  '/projects': 'ProjectsDashboard',
  '/memos': 'MemoDashboard',
  '/reports': 'ReportDashboard',
  '/templates': 'TemplateDashboard',
  '/assign-projects': 'ProjectsForAssigning',
  '/shared-memos': 'SharedMemoDashboard'
}

const breadcrumbs = computed(() => {
  const crumbs = []
  const currentRoute = route
  
  // Get user info for role-based home naming
  const userInfo = userStore.getters.currentUser()
  const userRole = userInfo?.role?.toLowerCase().replace(/\s+/g, '') || 'admin'
  
  // Determine the correct home name based on user role
  const getHomeName = () => {
    const roleToHomeName = {
      admin: 'Admin Dashboard',
      reviewer: 'Reviewer Dashboard',
      qahead: 'QA Head Dashboard', 
      designhead: 'Design Head Dashboard',
      designer: 'Designer Dashboard'
    }
    return roleToHomeName[userRole] || 'Admin Dashboard'
  }
  
  // Always start with role-appropriate Home
  crumbs.push({
    name: getHomeName(),
    path: getHomePath()
  })
  
  // Build breadcrumbs based on current route
  if (currentRoute.path === '/' || currentRoute.name === 'login') {
    return [] // Don't show breadcrumbs on login page
  }
  
  // Handle different route patterns
  const pathSegments = currentRoute.path.split('/').filter(segment => segment)
  
  // Only add additional breadcrumbs if we're not already on the home page
  const homePath = getHomePath()
  if (currentRoute.path !== homePath) {
    // Handle specific sub-routes based on current path
    if (currentRoute.path.startsWith('/projects')) {
      crumbs.push({
        name: routeMappings['ProjectsDashboard'] || 'Projects',
        path: '/projects'
      })
    } else if (currentRoute.path.startsWith('/memos')) {
      crumbs.push({
        name: routeMappings['MemoDashboard'] || 'Memos',
        path: '/memos'
      })
    } else if (currentRoute.path.startsWith('/reports')) {
      crumbs.push({
        name: routeMappings['ReportDashboard'] || 'Reports',
        path: '/reports'
      })
    } else if (currentRoute.path.startsWith('/user-activities')) {
      crumbs.push({
        name: routeMappings['UserActivities'] || 'User Activities',
        path: '/user-activities'
      })
    } else if (currentRoute.path.startsWith('/assign-projects')) {
      crumbs.push({
        name: routeMappings['ProjectsForAssigning'] || 'Assign Projects',
        path: '/assign-projects'
      })
    }
  }
  
  return crumbs
})

// Determine the home path based on user role
function getHomePath() {
  const userInfo = userStore.getters.currentUser()
  const userRole = userInfo?.role?.toLowerCase().replace(/\s+/g, '') || 'admin'
  
  console.log('Breadcrumb - User Role:', userRole) // Debug log
  
  // Map user roles to their corresponding home paths
  const roleToHomePath = {
    admin: '/admin',
    reviewer: '/reviewer', 
    qahead: '/qahead',
    designhead: '/designhead',
    designer: '/designer'
  }
  
  return roleToHomePath[userRole] || '/admin' // Default to admin if role not found
}
</script>

<style scoped>
.breadcrumb-nav {
  position: fixed !important;
  top: 100px !important;
  left: 0 !important;
  right: 0 !important;
  background-color: #f8f9fa !important;
  border-bottom: 1px solid #e9ecef !important;
  padding: 2px 0 !important;
  margin: 0 !important;
  z-index: 1001 !important;
  width: 100% !important;
}

.breadcrumb-container {
  max-width: 1350px;
  margin: 0 auto;
  padding: 0 20px;
}

.breadcrumb-list {
  display: flex;
  align-items: center;
  list-style: none;
  margin: 0;
  padding: 0;
  font-size: 14px;
}

.breadcrumb-item {
  display: flex;
  align-items: center;
}

.breadcrumb-link {
  color: #007bff;
  text-decoration: none;
  padding: 2px 4px;
  border-radius: 3px;
  transition: all 0.2s ease;
}

.breadcrumb-link:hover {
  color: #0056b3;
  background-color: #e9ecef;
  text-decoration: none;
}

.breadcrumb-current {
  color: #6c757d;
  font-weight: 500;
  padding: 2px 4px;
}

.breadcrumb-separator {
  color: #6c757d;
  margin: 0 6px;
  font-weight: 400;
}

.breadcrumb-item.active .breadcrumb-current {
  color: #495057;
  font-weight: 600;
}

/* Responsive design */
@media (max-width: 768px) {
  .breadcrumb-container {
    padding: 0 10px;
  }
  
  .breadcrumb-list {
    font-size: 12px;
  }
  
  .breadcrumb-separator {
    margin: 0 4px;
  }
  
  .breadcrumb-link,
  .breadcrumb-current {
    padding: 1px 2px;
  }
}

/* Hide breadcrumbs on very small screens if they get too long */
@media (max-width: 480px) {
  .breadcrumb-list {
    flex-wrap: wrap;
  }
  
  .breadcrumb-item {
    margin-bottom: 2px;
  }
}
</style>
