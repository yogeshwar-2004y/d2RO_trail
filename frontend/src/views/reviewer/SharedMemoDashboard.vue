<template>
  <div class="shared-memo-dashboard">
    <div class="header">
      <div class="header-left">
        <button class="back-button" @click="$router.go(-1)">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19 12H5"></path>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
        </button>
        <h1 class="page-title">Shared with Me</h1>
      </div>
      <div class="header-right">
        <div class="search-box">
          <input type="text" v-model="searchQuery" placeholder="Search Shared Memos" class="search-input">
          <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </div>
        <div class="filter-dropdown">
          <button class="filter-button" @click="toggleProjectFilter">
            Filter By Projects
          </button>
          <div v-if="showProjectFilter" class="filter-panel">
            <div
              v-for="project in projects"
              :key="project"
              class="filter-option"
              :class="{ 'selected': activeProjectFilter === project }"
              @click="selectProject(project)"
            >
              {{ project }}
            </div>
          </div>
        </div>
        <div class="filter-dropdown">
          <button class="filter-button" @click="toggleMemoFilter">
            Filter Memos
          </button>
          <div v-if="showMemoFilter" class="filter-panel">
            <div
              v-for="status in memoStatuses"
              :key="status.name"
              class="filter-option"
              :class="[status.color, { 'selected': activeMemoFilter === status.name }]"
              @click="selectMemoStatus(status.name)"
            >
              {{ status.name }}
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="memo-list">
      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="loading-spinner"></div>
        <p>Loading shared memos...</p>
      </div>
      
      <!-- Error State -->
      <div v-else-if="error" class="error-state">
        <div class="error-icon">⚠️</div>
        <h3>Error Loading Shared Memos</h3>
        <p>{{ error }}</p>
        <button @click="fetchSharedMemos" class="retry-button">Retry</button>
      </div>
      
      <!-- Empty State -->
      <div v-else-if="filteredMemos.length === 0" class="empty-state">
        <div class="empty-icon">📄</div>
        <h3>No Shared Memos</h3>
        <p>You haven't received any shared memos yet.</p>
      </div>
      
      <!-- Memo Cards -->
      <div 
        v-else
        v-for="memo in filteredMemos" 
        :key="memo.id" 
        class="memo-card shared-memo-card" 
        :class="memo.status.toLowerCase().replace(/ /g, '-')"
        @click="viewSharedMemo(memo.id)"
      >
        <div class="memo-details">
          <div class="memo-project">{{ memo.project }}</div>
          <div class="memo-author">Shared by: {{ memo.sharedBy }}</div>
          <div class="memo-shared-date">Shared on: {{ memo.sharedDate }}</div>
          <div v-if="memo.assignedDate" class="memo-assigned">Assigned: {{ memo.assignedDate }}</div>
        </div>
        <div class="memo-schedule">
          <div v-if="memo.scheduledDate" class="memo-scheduled">TEST SCHEDULED ON: {{ memo.scheduledDate }}</div>
          <div class="memo-status">{{ memo.status }}</div>
          <div class="view-only-badge">VIEW ONLY</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { userStore } from '@/stores/userStore'

export default {
  name: 'SharedMemoDashboard',
  data() {
    return {
      searchQuery: '',
      showProjectFilter: false,
      showMemoFilter: false,
      activeProjectFilter: null,
      activeMemoFilter: null,
      projects: [],
      memoStatuses: [
        { name: 'SUCCESSFULLY COMPLETED', color: 'success', dbValue: 'successfully_completed' },
        { name: 'REJECTED', color: 'rejected', dbValue: 'disapproved' },
        { name: 'DISAPPROVED', color: 'disapproved', dbValue: 'disapproved' },
        { name: 'ASSIGNED', color: 'assigned', dbValue: 'assigned' },
        { name: 'COMPLETED WITH OBSERVATIONS', color: 'observation', dbValue: 'completed_with_observations' },
        { name: 'TEST NOT CONDUCTED', color: 'not-conducted', dbValue: 'test_not_conducted' },
        { name: 'NOT ASSIGNED', color: 'not-assigned', dbValue: 'not_assigned' },
        { name: 'TEST FAILED', color: 'test-failed', dbValue: 'test_failed' },
      ],
      sharedMemos: [],
      loading: true,
      error: null,
    };
  },
  computed: {
    filteredMemos() {
      let filtered = this.sharedMemos;

      if (this.activeProjectFilter) {
        filtered = filtered.filter(memo => memo.project === this.activeProjectFilter);
      }

      if (this.activeMemoFilter) {
        filtered = filtered.filter(memo => memo.status === this.activeMemoFilter);
      }

      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(memo => 
          memo.project.toLowerCase().includes(query) ||
          memo.sharedBy.toLowerCase().includes(query)
        );
      }

      return filtered;
    },
  },
  async mounted() {
    await this.fetchSharedMemos();
    await this.fetchProjects();
  },
  methods: {
    async fetchSharedMemos() {
      try {
        this.loading = true;
        this.error = null;
        
        // Get current user information
        const currentUser = userStore.getters.currentUser();
        if (!currentUser) {
          throw new Error('User not logged in');
        }
        
        const response = await fetch(`/api/memos/shared?user_id=${currentUser.id}`);
        if (!response.ok) {
          throw new Error(`Failed to fetch shared memos: ${response.statusText}`);
        }
        
        const data = await response.json();
        if (data.success) {
          // Transform backend memo data to frontend format
          this.sharedMemos = data.shared_memos.map(memo => this.transformSharedMemoData(memo));
          console.log(`Loaded ${this.sharedMemos.length} shared memos`);
        } else {
          throw new Error(data.message || 'Failed to fetch shared memos');
        }
      } catch (error) {
        console.error('Error fetching shared memos:', error);
        this.error = error.message;
        this.sharedMemos = [];
      } finally {
        this.loading = false;
      }
    },
    async fetchProjects() {
      try {
        const response = await fetch('/api/projects');
        if (!response.ok) {
          throw new Error(`Failed to fetch projects: ${response.statusText}`);
        }
        
        const data = await response.json();
        if (data.success) {
          this.projects = data.projects;
        } else {
          throw new Error(data.message || 'Failed to fetch projects');
        }
      } catch (error) {
        console.error('Error fetching projects:', error);
        this.projects = [];
      }
    },
    transformSharedMemoData(backendMemo) {
      // Map backend shared memo format to frontend expected format
      return {
        id: backendMemo.memo_id,
        project: backendMemo.wing_proj_ref_no || 'N/A',
        author: backendMemo.from_person || 'Design Team',
        sharedBy: backendMemo.shared_by_name || 'Unknown',
        sharedDate: this.formatDate(backendMemo.shared_at),
        assignedDate: this.formatDate(backendMemo.dated),
        scheduledDate: this.formatDate(backendMemo.memo_date),
        status: this.determineStatus(backendMemo),
        // Store the original backend data for detailed view
        originalData: backendMemo
      };
    },
    determineStatus(memo) {
      // Use memo_status field if available, otherwise fall back to legacy logic
      if (memo.memo_status) {
        switch (memo.memo_status) {
          case 'not_assigned':
            return 'NOT ASSIGNED';
          case 'assigned':
            return 'ASSIGNED';
          case 'disapproved':
            // Check if this memo was rejected (has rejection in memo_approval)
            return 'REJECTED';
          case 'successfully_completed':
            return 'SUCCESSFULLY COMPLETED';
          case 'test_not_conducted':
            return 'TEST NOT CONDUCTED';
          case 'completed_with_observations':
            return 'COMPLETED WITH OBSERVATIONS';
          case 'test_failed':
            return 'TEST FAILED';
          default:
            return memo.memo_status.toUpperCase().replace(/_/g, ' ');
        }
      }
      // Fallback to legacy logic
      if (memo.accepted_at) {
        return 'SUCCESSFULLY COMPLETED';
      } else if (memo.submitted_at) {
        return 'ASSIGNED';
      } else {
        return 'NOT ASSIGNED';
      }
    },
    formatDate(dateString) {
      if (!dateString) return null;
      try {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-GB', {
          day: '2-digit',
          month: '2-digit',
          year: 'numeric'
        });
      } catch (error) {
        console.error('Error formatting date:', error);
        return dateString;
      }
    },
    toggleProjectFilter() {
      this.showProjectFilter = !this.showProjectFilter;
      this.showMemoFilter = false;
    },
    toggleMemoFilter() {
      this.showMemoFilter = !this.showMemoFilter;
      this.showProjectFilter = false;
    },
    selectProject(project) {
      this.activeProjectFilter = this.activeProjectFilter === project ? null : project;
      this.showProjectFilter = false;
    },
    selectMemoStatus(status) {
      this.activeMemoFilter = this.activeMemoFilter === status ? null : status;
      this.showMemoFilter = false;
    },
    viewSharedMemo(memoId) {
      // Navigate to the shared memo view page (read-only)
      this.$router.push({ name: 'SharedMemoView', params: { id: memoId } });
    }
  }
};
</script>

<style scoped>
.shared-memo-dashboard {
  font-family: Arial, sans-serif;
  min-height: 100vh;
  background-color: #ebf7fd;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 10;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.back-button {
  background: none;
  border: none;
  cursor: pointer;
}

.logo {
  width: 150px;
}

.page-title {
  margin: 0;
  color: #333;
  font-size: 1.5em;
  font-weight: bold;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.search-box {
  position: relative;
}

.search-input {
  padding: 10px 15px;
  padding-left: 40px;
  border: 1px solid #ccc;
  border-radius: 25px;
}

.search-icon {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #888;
}

.filter-dropdown {
  position: relative;
}

.filter-button {
  background: #f0f0f0;
  border: 1px solid #ccc;
  border-radius: 20px;
  padding: 10px 15px;
  font-weight: bold;
  cursor: pointer;
}

.filter-panel {
  position: absolute;
  top: 100%;
  left: 0;
  margin-top: 10px;
  width: 250px;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  padding: 10px;
  z-index: 5;
}

.filter-option {
  padding: 15px;
  margin-bottom: 5px;
  border-radius: 8px;
  font-weight: bold;
  color: #000;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
  text-align: center;
}

.filter-option:hover {
  transform: translateY(-2px);
}

.filter-option.selected {
  border: 2px solid #007bff;
}

/* Status-based colors for Memo Filters */
.success, .successfully-completed {
  background-color: #e2fbdc; /* Light Green */
}
.rejected {
  background-color: #ff4757; /* Bright Red */
  color: white;
}
.disapproved {
  background-color: #ffd8d6; /* Light Red */
}
.assigned {
  background-color: #d1d8ff; /* Light Blue */
}
.observation, .completed-with-observations {
  background-color: #fdddfa; /* Light Purple */
}
.not-conducted, .test-not-conducted {
  background-color: #fdd8d6; /* Light Pink */
}
.not-assigned {
  background-color: #fff1d6; /* Light Orange */
}
.test-failed {
  background-color: #ff6b6b; /* Red */
  color: white;
}

.memo-list {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.memo-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  color: #000;
  cursor: pointer;
  transition: all 0.3s ease;
}

.memo-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.shared-memo-card {
  border-left: 4px solid #007bff;
}

.memo-details {
  flex-grow: 1;
}

.memo-project {
  font-weight: bold;
  font-size: 1.1em;
}

.memo-author {
  font-size: 0.9em;
  color: #555;
}

.memo-shared-date {
  font-size: 0.8em;
  color: #007bff;
  font-weight: bold;
  margin-top: 2px;
}

.memo-assigned {
  font-size: 0.8em;
  color: #666;
  margin-top: 2px;
}

.memo-schedule {
  text-align: right;
  font-size: 0.9em;
  color: #555;
}

.memo-status {
  font-weight: bold;
  margin-top: 5px;
  padding: 4px 8px;
  border-radius: 4px;
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
}

.view-only-badge {
  background-color: #007bff;
  color: white;
  font-size: 0.7em;
  font-weight: bold;
  padding: 2px 6px;
  border-radius: 3px;
  margin-top: 5px;
  display: inline-block;
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-state p {
  color: #666;
  font-size: 1.1em;
  margin: 0;
}

/* Error State */
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin: 20px;
}

.error-icon {
  font-size: 3em;
  margin-bottom: 20px;
}

.error-state h3 {
  color: #dc3545;
  margin: 0 0 10px 0;
  font-size: 1.5em;
}

.error-state p {
  color: #666;
  margin: 0 0 20px 0;
  font-size: 1.1em;
}

.retry-button {
  background: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.3s;
}

.retry-button:hover {
  background: #0056b3;
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin: 20px;
}

.empty-icon {
  font-size: 4em;
  margin-bottom: 20px;
  opacity: 0.5;
}

.empty-state h3 {
  color: #333;
  margin: 0 0 10px 0;
  font-size: 1.5em;
}

.empty-state p {
  color: #666;
  margin: 0;
  font-size: 1.1em;
}
</style>
