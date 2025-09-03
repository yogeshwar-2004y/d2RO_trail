<template>
  <div class="role-test-component">
    <h2>Global Role System Test</h2>
    
    <div class="user-info" v-if="isLoggedIn">
      <h3>Current User Information:</h3>
      <p><strong>Name:</strong> {{ currentUser?.name || 'N/A' }}</p>
      <p><strong>Email:</strong> {{ currentUser?.email || 'N/A' }}</p>
      <p><strong>Role ID:</strong> {{ currentUserRole || 'N/A' }}</p>
      <p><strong>Role Name:</strong> {{ roleName || 'N/A' }}</p>
    </div>
    
    <div class="role-checks">
      <h3>Role-based Access Checks:</h3>
      <div class="check-item" :class="{ 'has-access': hasRole(1) }">
        <span class="check-label">Admin (Role ID: 1):</span>
        <span class="check-result">{{ hasRole(1) ? '✅ Access' : '❌ No Access' }}</span>
      </div>
      
      <div class="check-item" :class="{ 'has-access': hasRole(2) }">
        <span class="check-label">QA Head (Role ID: 2):</span>
        <span class="check-result">{{ hasRole(2) ? '✅ Access' : '❌ No Access' }}</span>
      </div>
      
      <div class="check-item" :class="{ 'has-access': hasRole(3) }">
        <span class="check-label">QA Reviewer (Role ID: 3):</span>
        <span class="check-result">{{ hasRole(3) ? '✅ Access' : '❌ No Access' }}</span>
      </div>
      
      <div class="check-item" :class="{ 'has-access': hasRole(4) }">
        <span class="check-label">Design Head (Role ID: 4):</span>
        <span class="check-result">{{ hasRole(4) ? '✅ Access' : '❌ No Access' }}</span>
      </div>
      
      <div class="check-item" :class="{ 'has-access': hasRole(5) }">
        <span class="check-label">Designer (Role ID: 5):</span>
        <span class="check-result">{{ hasRole(5) ? '✅ Access' : '❌ No Access' }}</span>
      </div>
    </div>
    
    <div class="role-name-checks">
      <h3>Role Name Checks:</h3>
      <div class="check-item" :class="{ 'has-access': hasRoleName('admin') }">
        <span class="check-label">Admin (by name):</span>
        <span class="check-result">{{ hasRoleName('admin') ? '✅ Access' : '❌ No Access' }}</span>
      </div>
      
      <div class="check-item" :class="{ 'has-access': hasRoleName('qa head') }">
        <span class="check-label">QA Head (by name):</span>
        <span class="check-result">{{ hasRoleName('qa head') ? '✅ Access' : '❌ No Access' }}</span>
      </div>
    </div>
    
    <div class="actions">
      <button @click="refreshData" class="refresh-btn">Refresh Data</button>
      <button @click="logout" class="logout-btn" v-if="isLoggedIn">Logout</button>
    </div>
    
    <div class="debug-info">
      <h3>Debug Information:</h3>
      <pre>{{ JSON.stringify(debugInfo, null, 2) }}</pre>
    </div>
  </div>
</template>

<script>
import { userStore } from '@/stores/userStore'

export default {
  name: 'RoleTestComponent',
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
    debugInfo() {
      return {
        isLoggedIn: this.isLoggedIn,
        currentUser: this.currentUser,
        currentUserRole: this.currentUserRole,
        roleName: this.roleName,
        localStorage: {
          user: localStorage.getItem('user'),
          isLoggedIn: localStorage.getItem('isLoggedIn'),
          currentUserRole: localStorage.getItem('currentUserRole'),
          roleName: localStorage.getItem('roleName')
        }
      }
    }
  },
  methods: {
    hasRole(roleId) {
      return userStore.actions.hasRole(roleId)
    },
    hasRoleName(roleName) {
      return userStore.actions.hasRoleName(roleName)
    },
    refreshData() {
      // Force reactivity update
      this.$forceUpdate()
    },
    logout() {
      userStore.actions.logout()
      this.$router.push({ name: 'LoginPage' })
    }
  }
}
</script>

<style scoped>
.role-test-component {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 10px;
  font-family: Arial, sans-serif;
}

.user-info, .role-checks, .role-name-checks {
  background: white;
  padding: 15px;
  margin: 15px 0;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.check-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}

.check-item:last-child {
  border-bottom: none;
}

.check-item.has-access {
  background-color: #e8f5e8;
  padding: 8px 12px;
  border-radius: 4px;
  margin: 4px 0;
}

.check-label {
  font-weight: bold;
}

.check-result {
  font-weight: bold;
}

.actions {
  display: flex;
  gap: 10px;
  margin: 20px 0;
}

.refresh-btn, .logout-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
}

.refresh-btn {
  background: #007bff;
  color: white;
}

.logout-btn {
  background: #dc3545;
  color: white;
}

.debug-info {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  margin-top: 20px;
}

.debug-info pre {
  background: #e9ecef;
  padding: 10px;
  border-radius: 4px;
  overflow-x: auto;
  font-size: 12px;
}

h2, h3 {
  color: #333;
  margin-bottom: 15px;
}
</style>
