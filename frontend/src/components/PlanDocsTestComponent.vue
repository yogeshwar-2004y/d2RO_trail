<template>
  <div class="plan-docs-test">
    <h2>Plan Documents Global User Store Test</h2>
    
    <div class="test-section">
      <h3>Current User Information</h3>
      <p><strong>Is Logged In:</strong> {{ isLoggedIn }}</p>
      <p><strong>User ID:</strong> {{ currentUser?.id }}</p>
      <p><strong>User Name:</strong> {{ currentUser?.name }}</p>
      <p><strong>User Email:</strong> {{ currentUser?.email }}</p>
      <p><strong>Role ID:</strong> {{ currentUserRole }}</p>
      <p><strong>Role Name:</strong> {{ roleName }}</p>
    </div>

    <div class="test-section">
      <h3>Role-Based Access Test</h3>
      <div class="access-tests">
        <div class="test-item">
          <span>Can Upload Documents:</span>
          <span :class="canUpload ? 'success' : 'fail'">
            {{ canUpload ? '✓ Yes' : '✗ No' }}
          </span>
        </div>
        <div class="test-item">
          <span>Is QA Head:</span>
          <span :class="isQAHead ? 'success' : 'fail'">
            {{ isQAHead ? '✓ Yes' : '✗ No' }}
          </span>
        </div>
        <div class="test-item">
          <span>Is Design Head:</span>
          <span :class="isDesignHead ? 'success' : 'fail'">
            {{ isDesignHead ? '✓ Yes' : '✗ No' }}
          </span>
        </div>
        <div class="test-item">
          <span>Is Designer:</span>
          <span :class="isDesigner ? 'success' : 'fail'">
            {{ isDesigner ? '✓ Yes' : '✗ No' }}
          </span>
        </div>
        <div class="test-item">
          <span>Is Admin:</span>
          <span :class="isAdmin ? 'success' : 'fail'">
            {{ isAdmin ? '✓ Yes' : '✗ No' }}
          </span>
        </div>
      </div>
    </div>

    <div class="test-section">
      <h3>Component Integration Test</h3>
      <p>This component demonstrates that the global user store is working correctly across all plan documents modules.</p>
      <p>All plan documents components (LruDashboard, ProjectsDashboard, DocumentViewer) now use the global user store instead of hardcoded roles.</p>
    </div>

    <div class="actions">
      <button @click="refreshData" class="btn btn-primary">Refresh Data</button>
      <button @click="goToProjects" class="btn btn-secondary">Go to Projects Dashboard</button>
      <button @click="goToLRUs" class="btn btn-secondary">Go to LRU Dashboard</button>
    </div>
  </div>
</template>

<script>
import { userStore } from '@/stores/userStore'

export default {
  name: 'PlanDocsTestComponent',
  computed: {
    isLoggedIn() {
      return userStore.getters.isLoggedIn()
    },
    currentUser() {
      return userStore.getters.currentUser()
    },
    currentUserRole() {
      return userStore.getters.currentUserRole()
    },
    roleName() {
      return userStore.getters.roleName()
    },
    canUpload() {
      return this.roleName === 'Design Head' || this.roleName === 'Designer'
    },
    isQAHead() {
      return this.roleName === 'QA Head'
    },
    isDesignHead() {
      return this.roleName === 'Design Head'
    },
    isDesigner() {
      return this.roleName === 'Designer'
    },
    isAdmin() {
      return this.roleName === 'Admin'
    }
  },
  methods: {
    refreshData() {
      // Force reactivity update
      this.$forceUpdate()
    },
    goToProjects() {
      this.$router.push({ name: 'ProjectsDashboard' })
    },
    goToLRUs() {
      // Navigate to LRU dashboard with sample project
      this.$router.push({ 
        name: 'LruDashboard', 
        params: { 
          projectId: 1, 
          projectName: 'Test Project' 
        } 
      })
    }
  }
}
</script>

<style scoped>
.plan-docs-test {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.test-section {
  margin-bottom: 30px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.test-section h3 {
  margin-top: 0;
  color: #333;
  border-bottom: 2px solid #007bff;
  padding-bottom: 10px;
}

.access-tests {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.test-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background-color: white;
  border-radius: 4px;
  border: 1px solid #eee;
}

.success {
  color: #28a745;
  font-weight: bold;
}

.fail {
  color: #dc3545;
  font-weight: bold;
}

.actions {
  display: flex;
  gap: 10px;
  justify-content: center;
  margin-top: 20px;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
  text-decoration: none;
  display: inline-block;
  text-align: center;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background-color: #545b62;
}
</style>
