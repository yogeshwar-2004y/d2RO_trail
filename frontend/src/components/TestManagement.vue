<template>
  <div class="test-management-page">
    <!-- Header -->
    <div class="page-header">
      <div class="header-left">
        <button class="back-button" @click="$router.go(-1)">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19 12H5"></path>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
        </button>
      </div>
      <div class="header-center">
        <h1 class="page-title">TEST MANAGEMENT</h1>
        <p class="page-subtitle">Select a test group to manage sub-tests and bulletins</p>
      </div>
      <div class="header-right">
        <button class="add-group-btn" @click="showAddGroupForm = !showAddGroupForm">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
          ADD GROUP
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Add Group Form -->
      <div v-if="showAddGroupForm" class="add-group-form">
        <div class="form-header">
          <h3>Add New Test Group</h3>
          <button @click="showAddGroupForm = false" class="close-form-btn">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <form @submit.prevent="saveGroup">
          <div class="form-group">
            <label for="groupName">Group Name *</label>
            <input 
              type="text" 
              id="groupName"
              v-model="groupForm.group_name" 
              placeholder="Enter group name"
              required
            >
          </div>
          
          <div class="form-group">
            <label for="groupDescription">Description</label>
            <textarea 
              id="groupDescription"
              v-model="groupForm.group_description" 
              placeholder="Enter group description"
              rows="3"
            ></textarea>
          </div>
          
          <div class="form-actions">
            <button type="button" @click="showAddGroupForm = false" class="cancel-btn">Cancel</button>
            <button type="submit" class="save-btn" :disabled="saving">
              {{ saving ? 'Saving...' : 'Create Group' }}
            </button>
          </div>
        </form>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="loading-spinner"></div>
        <p>Loading test groups...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error-state">
        <div class="error-icon">⚠️</div>
        <h3>Error Loading Data</h3>
        <p>{{ error }}</p>
        <button @click="loadTestGroups" class="retry-btn">Retry</button>
      </div>

      <!-- Test Groups Grid -->
      <div v-else class="test-groups-grid">
        <div 
          v-for="group in testGroups" 
          :key="group.group_id"
          class="group-card"
          @click="goToGroup(group)"
        >
          <div class="group-header">
            <div class="group-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="9 11 12 14 22 4"></polyline>
                <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path>
              </svg>
            </div>
            <div class="group-actions">
              <button @click.stop="editGroup(group)" class="action-btn edit-btn">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                  <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                </svg>
              </button>
              <button @click.stop="deleteGroup(group)" class="action-btn delete-btn">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="3 6 5 6 21 6"></polyline>
                  <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                </svg>
              </button>
            </div>
          </div>
          <div class="group-content">
            <h3 class="group-name">{{ group.group_name }}</h3>
            <p class="group-description">{{ group.group_description || 'No description available' }}</p>
            <div class="group-stats">
              <span class="stat">
                <strong>{{ getSubTestCount(group.group_id) }}</strong> Sub-tests
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="!loading && !error && testGroups.length === 0" class="empty-state">
        <div class="empty-icon">📋</div>
        <h3>No Test Groups Found</h3>
        <p>Create your first test group to get started with test management.</p>
        <button @click="showAddGroupForm = true" class="add-first-group-btn">
          Create First Group
        </button>
      </div>
    </div>

    <!-- Edit Group Form -->
    <div v-if="showEditGroupForm" class="edit-group-form">
      <div class="form-header">
        <h3>Edit Test Group</h3>
        <button @click="closeEditForm" class="close-form-btn">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>
      <form @submit.prevent="updateGroup">
        <div class="form-group">
          <label for="editGroupName">Group Name *</label>
          <input 
            type="text" 
            id="editGroupName"
            v-model="editingGroupForm.group_name" 
            placeholder="Enter group name"
            required
          >
        </div>
        
        <div class="form-group">
          <label for="editGroupDescription">Description</label>
          <textarea 
            id="editGroupDescription"
            v-model="editingGroupForm.group_description" 
            placeholder="Enter group description"
            rows="3"
          ></textarea>
        </div>
        
        <div class="form-actions">
          <button type="button" @click="closeEditForm" class="cancel-btn">Cancel</button>
          <button type="submit" class="save-btn" :disabled="saving">
            {{ saving ? 'Saving...' : 'Update Group' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TestManagement',
  data() {
    return {
      // Data
      testGroups: [],
      subTestCounts: {},
      
      // Loading states
      loading: false,
      saving: false,
      
      // Error handling
      error: null,
      
      // Form states
      showAddGroupForm: false,
      showEditGroupForm: false,
      
      // Selected items
      editingGroup: null,
      
      // Forms
      groupForm: {
        group_name: '',
        group_description: ''
      },
      editingGroupForm: {
        group_name: '',
        group_description: ''
      }
    }
  },
  mounted() {
    this.loadTestGroups()
  },
  methods: {
    // API Methods
    async loadTestGroups() {
      this.loading = true
      this.error = null
      
      try {
        const response = await fetch('http://localhost:8000/api/test-groups')
        const data = await response.json()
        
        if (data.success) {
          this.testGroups = data.groups
          await this.loadSubTestCounts()
        } else {
          this.error = data.message || 'Failed to load test groups'
        }
      } catch (error) {
        console.error('Error loading test groups:', error)
        this.error = 'Failed to load test groups. Please try again.'
      } finally {
        this.loading = false
      }
    },
    
    async loadSubTestCounts() {
      for (const group of this.testGroups) {
        try {
          const response = await fetch(`http://localhost:8000/api/test-groups/${group.group_id}/sub-tests`)
          const data = await response.json()
          
          if (data.success) {
            this.subTestCounts[group.group_id] = data.sub_tests.length
          }
        } catch (error) {
          console.error(`Error loading sub-tests for group ${group.group_id}:`, error)
          this.subTestCounts[group.group_id] = 0
        }
      }
    },
    
    async saveGroup() {
      this.saving = true
      
      try {
        const response = await fetch('http://localhost:8000/api/test-groups', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.groupForm)
        })
        
        const data = await response.json()
        
        if (data.success) {
          await this.loadTestGroups()
          this.showAddGroupForm = false
          this.resetGroupForm()
        } else {
          alert(data.message || 'Failed to save group')
        }
      } catch (error) {
        console.error('Error saving group:', error)
        alert('Failed to save group. Please try again.')
      } finally {
        this.saving = false
      }
    },
    
    async updateGroup() {
      this.saving = true
      
      try {
        const response = await fetch(`http://localhost:8000/api/test-groups/${this.editingGroup.group_id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.editingGroupForm)
        })
        
        const data = await response.json()
        
        if (data.success) {
          await this.loadTestGroups()
          this.closeEditForm()
        } else {
          alert(data.message || 'Failed to update group')
        }
      } catch (error) {
        console.error('Error updating group:', error)
        alert('Failed to update group. Please try again.')
      } finally {
        this.saving = false
      }
    },
    
    async deleteGroup(group) {
      if (!confirm(`Are you sure you want to delete "${group.group_name}"? This will also delete all sub-tests and bulletins.`)) {
        return
      }
      
      try {
        const response = await fetch(`http://localhost:8000/api/test-groups/${group.group_id}`, {
          method: 'DELETE'
        })
        
        const data = await response.json()
        
        if (data.success) {
          await this.loadTestGroups()
        } else {
          alert(data.message || 'Failed to delete group')
        }
      } catch (error) {
        console.error('Error deleting group:', error)
        alert('Failed to delete group. Please try again.')
      }
    },
    
    // Navigation Methods
    goToGroup(group) {
      // Navigate to group detail page
      this.$router.push({
        name: 'GroupDetail',
        params: {
          groupId: group.group_id,
          groupName: group.group_name
        }
      })
    },
    
    // UI Methods
    editGroup(group) {
      this.editingGroup = group
      this.editingGroupForm = {
        group_name: group.group_name,
        group_description: group.group_description || ''
      }
      this.showEditGroupForm = true
    },
    
    closeEditForm() {
      this.showEditGroupForm = false
      this.editingGroup = null
      this.editingGroupForm = {
        group_name: '',
        group_description: ''
      }
    },
    
    // Form Management
    resetGroupForm() {
      this.groupForm = {
        group_name: '',
        group_description: ''
      }
    },
    
    // Utility Methods
    getSubTestCount(groupId) {
      return this.subTestCounts[groupId] || 0
    }
  }
}
</script>

<style scoped>
.test-management-page {
  min-height: 100vh;
  background: #f5f5f5;
}

/* Header */
.page-header {
  background: #2d3748;
  padding: 20px 30px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 15px;
}

.back-button {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  cursor: pointer;
  padding: 10px;
  border-radius: 50%;
  transition: all 0.3s ease;
  color: white;
}

.back-button:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.05);
}

.header-center {
  flex: 1;
  text-align: center;
}

.page-title {
  color: white;
  font-size: 2.2em;
  font-weight: 700;
  margin: 0;
  letter-spacing: 2px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.page-subtitle {
  color: rgba(255, 255, 255, 0.8);
  font-size: 1em;
  margin: 5px 0 0 0;
}

.header-right {
  display: flex;
  align-items: center;
}

.add-group-btn {
  background: rgba(255, 255, 255, 0.95);
  border: none;
  border-radius: 25px;
  padding: 12px 20px;
  font-weight: 600;
  color: #4a5568;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.add-group-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  background: white;
}

/* Main Content */
.main-content {
  max-width: 1200px;
  margin: 30px auto;
  padding: 0 30px;
}

/* Add Group Form */
.add-group-form,
.edit-group-form {
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  padding: 25px;
  margin-bottom: 30px;
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #e9ecef;
}

.form-header h3 {
  margin: 0;
  color: #2d3748;
  font-size: 1.4em;
  font-weight: 600;
}

.close-form-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 5px;
  border-radius: 50%;
  transition: all 0.3s ease;
  color: #6c757d;
}

.close-form-btn:hover {
  background: #f8f9fa;
  color: #dc3545;
}

/* Form Styles */
.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #2d3748;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 12px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 1em;
  transition: border-color 0.3s ease;
  box-sizing: border-box;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #007bff;
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

.form-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
  margin-top: 25px;
}

.cancel-btn {
  background: #6c757d;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-btn:hover {
  background: #5a6268;
}

.save-btn {
  background: #007bff;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.save-btn:hover:not(:disabled) {
  background: #0056b3;
}

.save-btn:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

/* Loading State */
.loading-state {
  text-align: center;
  padding: 60px 20px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Error State */
.error-state {
  text-align: center;
  padding: 60px 20px;
}

.error-icon {
  font-size: 4em;
  margin-bottom: 20px;
}

.error-state h3 {
  color: #dc3545;
  font-size: 1.5em;
  margin-bottom: 10px;
}

.error-state p {
  color: #6c757d;
  margin-bottom: 20px;
}

.retry-btn {
  background: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.retry-btn:hover {
  background: #0056b3;
}

/* Test Groups Grid */
.test-groups-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 25px;
  margin-top: 20px;
}

.group-card {
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  padding: 25px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.group-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
  border-color: #007bff;
}

.group-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.group-icon {
  color: #007bff;
}

.group-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  background: none;
  border: 1px solid #e9ecef;
  border-radius: 6px;
  padding: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn:hover {
  transform: scale(1.1);
}

.edit-btn:hover {
  background: #e3f2fd;
  border-color: #2196f3;
  color: #2196f3;
}

.delete-btn:hover {
  background: #ffebee;
  border-color: #f44336;
  color: #f44336;
}

.group-content {
  text-align: left;
}

.group-name {
  color: #2d3748;
  font-size: 1.4em;
  font-weight: 600;
  margin: 0 0 10px 0;
}

.group-description {
  color: #6c757d;
  font-size: 0.95em;
  line-height: 1.5;
  margin: 0 0 15px 0;
}

.group-stats {
  display: flex;
  gap: 15px;
}

.stat {
  color: #4a5568;
  font-size: 0.9em;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 80px 20px;
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.empty-icon {
  font-size: 5em;
  margin-bottom: 20px;
  opacity: 0.6;
}

.empty-state h3 {
  color: #6c757d;
  font-size: 1.8em;
  margin-bottom: 10px;
}

.empty-state p {
  color: #6c757d;
  font-size: 1.1em;
  margin-bottom: 30px;
}

.add-first-group-btn {
  background: #007bff;
  color: white;
  border: none;
  padding: 15px 30px;
  border-radius: 10px;
  font-size: 1.1em;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.add-first-group-btn:hover {
  background: #0056b3;
  transform: translateY(-2px);
}

/* Responsive Design */
@media (max-width: 768px) {
  .page-header {
    padding: 15px 20px;
    flex-direction: column;
    gap: 15px;
  }
  
  .page-title {
    font-size: 1.8em;
  }
  
  .main-content {
    padding: 0 20px;
    margin: 20px auto;
  }
  
  .test-groups-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .group-card {
    padding: 20px;
  }
  
  .add-group-form,
  .edit-group-form {
    padding: 20px;
  }
}
</style>