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
  
  // Always start with Home
  crumbs.push({
    name: 'Home',
    path: getHomePath()
  })
  
  // Build breadcrumbs based on current route
  if (currentRoute.path === '/' || currentRoute.name === 'login') {
    return [] // Don't show breadcrumbs on login page
  }
  
  // Handle different route patterns
  const pathSegments = currentRoute.path.split('/').filter(segment => segment)
  
  // Handle admin routes
  if (currentRoute.path.startsWith('/admin')) {
    crumbs.push({
      name: routeMappings['HomePageAdmin'] || 'Admin Dashboard',
      path: '/admin'
    })
  }
  
  // Handle reviewer routes
  if (currentRoute.path.startsWith('/reviewer')) {
    crumbs.push({
      name: routeMappings['HomePageReviewer'] || 'Reviewer Dashboard',
      path: '/reviewer'
    })
  }
  
  // Handle QA Head routes
  if (currentRoute.path.startsWith('/qahead')) {
    crumbs.push({
      name: routeMappings['HomePageQAHead'] || 'QA Head Dashboard',
      path: '/qahead'
    })
  }
  
  // Handle Design Head routes
  if (currentRoute.path.startsWith('/designhead')) {
    crumbs.push({
      name: routeMappings['HomePageDesignHead'] || 'Design Head Dashboard',
      path: '/designhead'
    })
  }
  
  // Handle Designer routes
  if (currentRoute.path.startsWith('/designer')) {
    crumbs.push({
      name: routeMappings['HomePageDesigner'] || 'Designer Dashboard',
      path: '/designer'
    })
  }
  
  // Handle user activities routes
  if (currentRoute.path.startsWith('/user-activities')) {
    crumbs.push({
      name: routeMappings['UserActivities'] || 'User Activities',
      path: '/user-activities'
    })
  }
  
  // Handle projects routes
  if (currentRoute.path.startsWith('/projects')) {
    crumbs.push({
      name: routeMappings['ProjectsDashboard'] || 'Projects',
      path: '/projects'
    })
    
    // Add LRU level if present
    if (pathSegments.length > 1 && pathSegments[1] !== 'projects') {
      crumbs.push({
        name: routeMappings['LruDashboard'] || 'LRUs',
        path: currentRoute.path
      })
    }
  }
  
  // Handle memos routes
  if (currentRoute.path.startsWith('/memos')) {
    crumbs.push({
      name: routeMappings['MemoDashboard'] || 'Memos',
      path: '/memos'
    })
    
    // Add specific memo actions
    if (pathSegments.length > 1) {
      if (pathSegments[1] === 'submit') {
        crumbs.push({
          name: routeMappings['SubmitMemo'] || 'Submit Memo',
          path: currentRoute.path
        })
      } else if (pathSegments[1] === 'notifications') {
        crumbs.push({
          name: routeMappings['QAHeadNotifications'] || 'Notifications',
          path: currentRoute.path
        })
      } else if (pathSegments[1] === 'view') {
        crumbs.push({
          name: routeMappings['ViewOnlyMemoForm'] || 'View Memo',
          path: currentRoute.path
        })
      } else if (pathSegments[1] !== 'memos') {
        crumbs.push({
          name: routeMappings['MemoForm'] || 'Memo Form',
          path: currentRoute.path
        })
      }
    }
  }
  
  // Handle reports routes
  if (currentRoute.path.startsWith('/reports')) {
    crumbs.push({
      name: routeMappings['ReportDashboard'] || 'Reports',
      path: '/reports'
    })
    
    // Add specific report types
    if (pathSegments.length > 1) {
      if (pathSegments[1] === 'individual') {
        crumbs.push({
          name: routeMappings['IndividualReport'] || 'Report Details',
          path: currentRoute.path
        })
      } else if (pathSegments[1] === 'memo-id') {
        crumbs.push({
          name: routeMappings['TestReports'] || 'Test Reports',
          path: currentRoute.path
        })
      } else if (pathSegments[1] === 'view-observations') {
        crumbs.push({
          name: routeMappings['ObservationReport'] || 'Observation Report',
          path: currentRoute.path
        })
      }
    }
  }
  
  // Handle templates routes
  if (currentRoute.path.startsWith('/templates')) {
    crumbs.push({
      name: routeMappings['TemplateDashboard'] || 'Templates',
      path: '/templates'
    })
    
    // Add specific template types
    if (pathSegments.length > 1) {
      if (pathSegments[1] === 'view') {
        crumbs.push({
          name: routeMappings['TemplateViewer'] || 'Template Viewer',
          path: currentRoute.path
        })
      } else {
        // Handle specific template types
        const templateName = pathSegments[1]
        const templateMapping = {
          'bare-pcb-inspection': 'Bare PCB Inspection',
          'conformal-coating-inspection': 'Conformal Coating Inspection',
          'raw-material-inspection': 'Raw Material Inspection',
          'cots-screening-inspection': 'COTS Screening Inspection',
          'assembled-board-inspection': 'Assembled Board Inspection',
          'kit-of-part-inspection': 'Kit of Parts Inspection',
          'mechanical-inspection': 'Mechanical Inspection'
        }
        
        if (templateMapping[templateName]) {
          crumbs.push({
            name: templateMapping[templateName],
            path: currentRoute.path
          })
        }
      }
    }
  }
  
  // Handle assign projects routes
  if (currentRoute.path.startsWith('/assign-projects')) {
    crumbs.push({
      name: routeMappings['ProjectsForAssigning'] || 'Assign Projects',
      path: '/assign-projects'
    })
    
    if (pathSegments.length > 2) {
      if (pathSegments[2] === 'members') {
        crumbs.push({
          name: routeMappings['ProjectMembers'] || 'Project Members',
          path: currentRoute.path
        })
        
        if (pathSegments[3] === 'add') {
          crumbs.push({
            name: routeMappings['AddMember'] || 'Add Member',
            path: currentRoute.path
          })
        }
      }
    }
  }
  
  // Handle shared memos routes
  if (currentRoute.path.startsWith('/shared-memos')) {
    crumbs.push({
      name: routeMappings['SharedMemoDashboard'] || 'Shared Memos',
      path: '/shared-memos'
    })
    
    if (pathSegments.length > 1 && pathSegments[1] === 'view') {
      crumbs.push({
        name: routeMappings['SharedMemoView'] || 'Shared Memo',
        path: currentRoute.path
      })
    }
  }
  
  // Handle specific admin sub-routes
  if (currentRoute.path.startsWith('/user-activities/')) {
    const subRoute = pathSegments[1]
    const subRouteMapping = {
      'add-update-projects': 'Add/Update Projects',
      'manage-projects': 'Manage Projects',
      'add-update-users': 'Add/Update Users',
      'manage-users': 'Manage Users',
      'activity-logs': 'Activity Logs',
      'major-test-groups': 'Major Test Groups',
      'manufacturing-test-group': 'Manufacturing Test Group',
      'cots-screening-test-group': 'COTS Screening Test Group',
      'ess-test-group': 'ESS Test Group',
      'qt-test-group': 'QT Test Group',
      'soft-test-group': 'SoFT Test Group',
      'news-updates': 'News Updates',
      'customise-background': 'Customize Background'
    }
    
    if (subRouteMapping[subRoute]) {
      crumbs.push({
        name: subRouteMapping[subRoute],
        path: currentRoute.path
      })
    }
  }
  
  // Handle edit routes
  if (currentRoute.path.startsWith('/edit-user/')) {
    crumbs.push({
      name: routeMappings['EditUser'] || 'Edit User',
      path: currentRoute.path
    })
  }
  
  if (currentRoute.path.startsWith('/edit-project/')) {
    crumbs.push({
      name: routeMappings['EditProject'] || 'Edit Project',
      path: currentRoute.path
    })
  }
  
  // Handle select routes
  if (currentRoute.path === '/select-user-to-edit') {
    crumbs.push({
      name: routeMappings['SelectUserToEdit'] || 'Select User',
      path: currentRoute.path
    })
  }
  
  if (currentRoute.path === '/select-project-to-edit') {
    crumbs.push({
      name: routeMappings['SelectProjectToEdit'] || 'Select Project',
      path: currentRoute.path
    })
  }
  
  // Handle document viewer
  if (currentRoute.path.startsWith('/document-viewer/')) {
    crumbs.push({
      name: routeMappings['DocumentViewer'] || 'Document Viewer',
      path: currentRoute.path
    })
  }
  
  // Handle QA Head specific routes
  if (currentRoute.path.startsWith('/qahead/')) {
    if (pathSegments[1] === 'assign-reviewer') {
      crumbs.push({
        name: routeMappings['QAHeadAssignReviewer'] || 'Assign Reviewer',
        path: currentRoute.path
      })
    } else if (pathSegments[1] === 'projects') {
      crumbs.push({
        name: routeMappings['QAHeadDocumentVersionView'] || 'Document Version',
        path: currentRoute.path
      })
    }
  }
  
  // Handle reviewer specific routes
  if (currentRoute.path.startsWith('/reviewer/')) {
    if (pathSegments[1] === 'memo-dashboard') {
      crumbs.push({
        name: routeMappings['ReviewerMemoDashboard'] || 'Memo Dashboard',
        path: currentRoute.path
      })
    } else if (pathSegments[1] === 'InspectionMemo') {
      crumbs.push({
        name: routeMappings['InspectionMemo'] || 'Inspection Memo',
        path: currentRoute.path
      })
    }
  }
  
  // Handle designer specific routes
  if (currentRoute.path.startsWith('/designer/iqa-observation-report/')) {
    crumbs.push({
      name: routeMappings['DesignerIqaObservationReport'] || 'IQA Observation Report',
      path: currentRoute.path
    })
  }
  
  // Handle test routes
  if (currentRoute.path === '/test-role-system') {
    crumbs.push({
      name: routeMappings['RoleTestComponent'] || 'Role Test',
      path: currentRoute.path
    })
  }
  
  if (currentRoute.path === '/test-plan-docs') {
    crumbs.push({
      name: routeMappings['PlanDocsTestComponent'] || 'Plan Docs Test',
      path: currentRoute.path
    })
  }
  
  return crumbs
})

// Determine the home path based on user role or current route
function getHomePath() {
  const currentPath = route.path
  
  if (currentPath.startsWith('/admin')) {
    return '/admin'
  } else if (currentPath.startsWith('/reviewer')) {
    return '/reviewer'
  } else if (currentPath.startsWith('/qahead')) {
    return '/qahead'
  } else if (currentPath.startsWith('/designhead')) {
    return '/designhead'
  } else if (currentPath.startsWith('/designer')) {
    return '/designer'
  } else if (currentPath.startsWith('/user-activities')) {
    return '/user-activities'
  } else {
    return '/admin' // Default to admin dashboard
  }
}
</script>

<style scoped>
.breadcrumb-nav {
  background-color: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
  padding: 8px 0;
  margin: 0;
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
