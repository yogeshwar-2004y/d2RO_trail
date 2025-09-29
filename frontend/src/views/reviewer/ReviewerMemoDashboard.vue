<template>
  <div class="memo-dashboard">
    <div class="header">
      <div class="header-left">
        <button class="back-button" @click="$router.go(-1)">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19 12H5"></path>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
        </button>
        <img src="@/assets/images/aviatrax-logo.png" alt="Aviatrax Logo" class="logo">
      </div>
      <div class="header-right">
        <div class="search-box">
          <input type="text" v-model="searchQuery" placeholder="Search Projects" class="search-input">
          <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </div>
        <button class="shared-with-me-button" @click="goToSharedMemos">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
            <circle cx="8.5" cy="7" r="4"></circle>
            <line x1="20" y1="8" x2="20" y2="14"></line>
            <line x1="23" y1="11" x2="17" y2="11"></line>
          </svg>
          Shared with Me
        </button>
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
        <p>Loading memos...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error-state">
        <div class="error-icon">⚠️</div>
        <p>Error loading memos: {{ error }}</p>
        <button @click="fetchMemos" class="retry-button">Retry</button>
      </div>

      <!-- Empty State -->
      <div v-else-if="filteredMemos.length === 0" class="empty-state">
        <div class="empty-icon">📝</div>
        <p>No memos found</p>
        <p class="empty-subtitle">{{ searchQuery || activeProjectFilter || activeMemoFilter ? 'Try adjusting your filters' : 'No memos have been submitted yet' }}</p>
      </div>

      <!-- Memo Cards -->
      <div 
        v-else
        v-for="memo in filteredMemos" 
        :key="memo.id" 
        class="memo-card" 
        :class="memo.status.toLowerCase().replace(/ /g, '-')"
        @click="openMemo(memo.id)"
      >
        <div class="memo-details">
          <div class="memo-project">{{ memo.project }}</div>
          <div class="memo-author">Author: {{ memo.author }}</div>
          <div v-if="memo.assignedDate" class="memo-assigned">Assigned: {{ memo.assignedDate }}</div>
        </div>
        <div class="memo-schedule">
          <div v-if="memo.scheduledDate" class="memo-scheduled">TEST SCHEDULED ON: {{ memo.scheduledDate }}</div>
          <div class="memo-status">{{ memo.status }}</div>
        </div>
        <div class="memo-actions">
          <button class="share-btn" @click.stop="shareMemo(memo)" title="Share memo">
            <svg class="icon share" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8M16 6l-4-4-4 4M12 2v13"/>
            </svg>
            <span class="share-text">Share</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Share Modal -->
    <div v-if="showShareModal" class="share-modal-overlay" @click.self="toggleShareModal">
      <div class="share-modal-content">
        <h2>Share Memo</h2>
        <p>Enter email addresses separated by commas to share this memo.</p>
        <div class="memo-info">
          <strong>Project:</strong> {{ selectedMemo?.project }}<br>
          <strong>Author:</strong> {{ selectedMemo?.author }}
        </div>
        <input type="text" v-model="emailAddresses" placeholder="e.g., mail1@example.com, mail2@example.com" class="email-input" />
        <div class="modal-actions">
          <button @click="sendEmails" class="send-btn">Send</button>
          <button @click="toggleShareModal" class="cancel-btn">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { userStore } from '@/stores/userStore'

export default {
  name: 'ReviewerMemoDashboard',
  data() {
    return {
      searchQuery: '',
      showProjectFilter: false,
      showMemoFilter: false,
      activeProjectFilter: null,
      activeMemoFilter: null,
      showShareModal: false,
      emailAddresses: '',
      selectedMemo: null,
      projects: [],
      memoStatuses: [
        { name: 'SUCCESSFULLY COMPLETED', color: 'success' },
        { name: 'DISAPPROVED', color: 'disapproved' },
        { name: 'ASSIGNED', color: 'assigned' },
        { name: 'COMPLETED WITH OBSERVATIONS', color: 'observation' },
        { name: 'TEST NOT CONDUCTED', color: 'not-conducted' },
        { name: 'NOT ASSIGNED', color: 'not-assigned' },
      ],
      memos: [],
      loading: true,
      error: null,
    };
  },
  computed: {
    filteredMemos() {
      let filtered = this.memos;

      if (this.activeProjectFilter) {
        filtered = filtered.filter(memo => memo.project === this.activeProjectFilter);
      }

      if (this.activeMemoFilter) {
        filtered = filtered.filter(memo => memo.status === this.activeMemoFilter);
      }

      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(memo => memo.project.toLowerCase().includes(query));
      }

      return filtered;
    },
  },
  async mounted() {
    await this.fetchMemos();
    await this.fetchProjects();
  },
  methods: {
    async fetchMemos() {
      try {
        this.loading = true;
        this.error = null;
        
        // Get current user information
        const currentUser = userStore.getters.currentUser();
        const currentUserRole = userStore.getters.currentUserRole();
        
        // Build query parameters
        const params = new URLSearchParams();
        if (currentUser && currentUserRole) {
          params.append('user_id', currentUser.id);
          params.append('user_role', currentUserRole);
        }
        
        const response = await fetch(`/api/memos?${params.toString()}`);
        if (!response.ok) {
          throw new Error(`Failed to fetch memos: ${response.statusText}`);
        }
        
        const data = await response.json();
        if (data.success) {
          // Transform backend memo data to frontend format
          this.memos = data.memos.map(memo => this.transformMemoData(memo));
        } else {
          throw new Error(data.message || 'Failed to fetch memos');
        }
      } catch (error) {
        console.error('Error fetching memos:', error);
        this.error = error.message;
        this.memos = [];
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
          this.projects = data.projects.map(project => project.name);
        }
      } catch (error) {
        console.error('Error fetching projects:', error);
        this.projects = [];
      }
    },

    transformMemoData(backendMemo) {
      // Map backend memo format to frontend expected format
      return {
        id: backendMemo.memo_id,
        project: backendMemo.wing_proj_ref_no || 'N/A',
        author: backendMemo.from_person || 'Design Team',
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
            return 'DISAPPROVED';
          default:
            return memo.memo_status.toUpperCase();
        }
      }
      
      // Fallback to legacy logic for backward compatibility
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
        }).replace(/\//g, '-');
      } catch {
        return dateString;
      }
    },

    async openMemo(memoId) {
      try {
        // Fetch detailed memo data from backend
        const response = await fetch(`/api/memos/${memoId}`);
        if (!response.ok) {
          throw new Error(`Failed to fetch memo details: ${response.statusText}`);
        }
        
        const data = await response.json();
        if (data.success) {
          // Navigate to inspection memo page with detailed data
          this.$router.push({ 
            name: 'InspectionMemo', 
            params: { 
              id: memoId,
              memoData: data.memo,
              references: data.references
            } 
          });
        } else {
          throw new Error(data.message || 'Failed to fetch memo details');
        }
      } catch (error) {
        console.error('Error fetching memo details:', error);
        alert('Failed to load memo details. Please try again.');
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
    goToSharedMemos() {
      // Navigate to the shared memos dashboard
      this.$router.push({ name: 'SharedMemoDashboard' });
    },
    shareMemo(memo) {
      this.selectedMemo = memo;
      this.showShareModal = true;
    },
    toggleShareModal() {
      this.showShareModal = !this.showShareModal;
      if (!this.showShareModal) {
        this.emailAddresses = '';
        this.selectedMemo = null;
      }
    },
    sendEmails() {
      if (this.emailAddresses.trim() === '') {
        alert('Please enter at least one email address.');
        return;
      }
      
      const emails = this.emailAddresses.split(',').map(email => email.trim());
      console.log('Sharing memo:', this.selectedMemo, 'to:', emails);
      
      alert(`Memo "${this.selectedMemo.project}" shared successfully with: ${emails.join(', ')}`);
      this.toggleShareModal();
    }
 }
};
</script>

<style scoped>
.memo-dashboard {
  font-family: Arial, sans-serif;
  min-height: 100vh;
  background-color: #f0f0f0;
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

.shared-with-me-button {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 20px;
  padding: 10px 15px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.shared-with-me-button:hover {
  background: #0056b3;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 123, 255, 0.3);
}

.shared-with-me-button svg {
  width: 20px;
  height: 20px;
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

/* New Status-based colors for Memo Filters */
.success, .successfully-completed {
  background-color: #e2fbdc; /* Light Green */
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

.memo-list {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.memo-card {
  position: relative;
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

.memo-assigned {
  font-size: 0.8em;
  color: #666;
  margin-top: 2px;
}

/* Memo Actions */
.memo-actions {
  position: absolute;
  top: 15px;
  right: 15px;
  z-index: 100;
}

.share-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  background-color: #000;
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.share-btn:hover {
  background-color: #333;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.share-btn .icon {
  width: 14px;
  height: 14px;
}

.share-text {
  font-size: 12px;
  font-weight: 500;
}

/* Share Modal Styles */
.share-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.share-modal-content {
  background-color: white;
  border-radius: 10px;
  padding: 30px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  width: 90%;
  max-width: 500px;
}

.share-modal-content h2 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 1.5em;
  text-align: center;
}

.share-modal-content p {
  margin: 0 0 20px 0;
  color: #666;
  text-align: center;
}

.memo-info {
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  border: 1px solid #e9ecef;
}

.memo-info strong {
  color: #333;
}

.email-input {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
  margin-bottom: 20px;
  box-sizing: border-box;
}

.email-input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.modal-actions {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.send-btn {
  padding: 12px 24px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.send-btn:hover {
  background-color: #0056b3;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 123, 255, 0.3);
}

.cancel-btn {
  padding: 12px 24px;
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-btn:hover {
  background-color: #545b62;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(108, 117, 125, 0.3);
}

/* Loading, Error, and Empty States */
.loading-state, .error-state, .empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
  color: #666;
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

.error-icon, .empty-icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.retry-button {
  background: #007bff;
  color: white;
  border: none;
  border-radius: 25px;
  padding: 10px 20px;
  cursor: pointer;
  margin-top: 15px;
  transition: background 0.3s ease;
}

.retry-button:hover {
  background: #0056b3;
}

.empty-subtitle {
  font-size: 0.9em;
  color: #999;
  margin-top: 10px;
}
</style>