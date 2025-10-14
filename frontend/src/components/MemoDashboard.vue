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
      </div>
      <div class="header-right">

        <!-- Shared with Me Button (only for QA Reviewer - role 3) -->
        <button 
          v-if="currentUserRole === 3" 
          class="shared-with-me-button"
          @click="openSharedMemos"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" 
              viewBox="0 0 24 24" fill="none" stroke="currentColor" 
              stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M20 21v-2a4 4 0 0 0-3-3.87"></path>
            <path d="M4 21v-2a4 4 0 0 1 3-3.87"></path>
            <circle cx="12" cy="7" r="4"></circle>
          </svg>
          Shared with Me
        </button>
        
        <!-- Notification Bell (only for QA Head - role 2) -->
        <div 
          v-if="currentUserRole === 2" 
          class="notification-container" 
          @click="openNotifications"
        >
          <div class="notification-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" 
                 viewBox="0 0 24 24" fill="none" stroke="currentColor" 
                 stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
              <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
            </svg>
            <span v-if="unreadNotifications > 0" class="notification-badge">
              {{ unreadNotifications }}
            </span>
          </div>
        </div>

        <!-- Search Box -->
        <div class="search-box">
          <input type="text" v-model="searchQuery" placeholder="Search Projects" class="search-input">
          <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" 
               viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" 
               stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </div>

        <!-- Project Filter -->
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

        <!-- Memo Filter -->
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

        <!-- Submit Memo Button (only for Design Head - role 4, Designer - role 5) -->
        <button 
          v-if="[4, 5].includes(currentUserRole)" 
          class="submit-new-memo-button" 
          @click="submitNewMemo"
        >
          + Submit New Memo
        </button>

      </div>
    </div>
    
    <!-- Memo List -->
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
        @click="viewMemo(memo)"
      >
        <div class="memo-details">
          <div class="memo-project">{{ memo.project }}</div>
          <div class="memo-author">FROM - {{ memo.author }}</div>
        </div>
        <div class="memo-schedule" v-if="memo.assignedDate">
          <div class="memo-assigned">ASSIGNED ON : {{ memo.assignedDate }}</div>
          <div class="memo-scheduled">TEST SCHEDULED ON : {{ memo.scheduledDate }}</div>
        </div>
        <!-- Share button for QA Reviewers -->
        <div v-if="currentUserRole === 3" class="memo-actions">
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
        <p>Select a QA reviewer to share this memo with.</p>
        <div class="memo-info">
          <strong>Project:</strong> {{ selectedMemo?.project }}<br>
          <strong>Author:</strong> {{ selectedMemo?.author }}<br>
          <strong>Memo ID:</strong> {{ selectedMemo?.id }}
        </div>
        <div class="form-group">
          <label for="reviewer-select">Select QA Reviewer:</label>
          <select id="reviewer-select" v-model="selectedReviewerId" class="reviewer-select" @change="onReviewerChange">
            <option value="">Choose a reviewer...</option>
            <option v-for="reviewer in reviewers" :key="reviewer.user_id" :value="reviewer.user_id">
              {{ reviewer.name }} ({{ reviewer.email }})
            </option>
          </select>
        </div>
        <div class="form-group" v-if="selectedReviewerId">
          <label>Selected Reviewer Details:</label>
          <div class="reviewer-details">
            <strong>Username:</strong> {{ getSelectedReviewerName() }}<br>
            <strong>User ID:</strong> {{ selectedReviewerId }}<br>
            <strong>Email:</strong> {{ getSelectedReviewerEmail() }}
          </div>
        </div>
        <div class="modal-actions">
          <button @click="shareMemoWithReviewer" class="send-btn" :disabled="!selectedReviewerId">Share</button>
          <button @click="toggleShareModal" class="cancel-btn">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { userStore } from '@/stores/userStore'

export default {
  name: 'MemoDashboard',
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
      memos: [],
      loading: true,
      error: null,
      showShareModal: false,
      selectedMemo: null,
      selectedReviewerId: '',
      reviewers: [],
      notifications: [
        { id: 1, project: 'PROJ001', serialNumber: '15,16', lru: 'LRU Name', completedStage: 'stage 1', requiredStage: 'stage3', justification: 'justification', status: 'pending', isRead: false },
        { id: 2, project: 'PROJ002', serialNumber: '17,18', lru: 'LRU Component', completedStage: 'stage 2', requiredStage: 'stage4', justification: 'Technical review required', status: 'pending', isRead: false },
        { id: 3, project: 'PROJ003', serialNumber: '19,20', lru: 'LRU Assembly', completedStage: 'stage 1', requiredStage: 'stage3', justification: 'Quality check needed', status: 'pending', isRead: true },
      ],
    };
  },
  computed: {
    // Get current user role from global store
    currentUserRole() {
      return userStore.getters.currentUserRole()
    },
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
    unreadNotifications() {
      return this.notifications.filter(n => !n.isRead).length;
    }
  },
  async mounted() {
    await this.fetchMemos();
    await this.fetchProjects();
    await this.fetchReviewers();
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

    async viewMemo(memo) {
      try {
        // Fetch detailed memo data from backend
        const response = await fetch(`/api/memos/${memo.id}`);
        if (!response.ok) {
          throw new Error(`Failed to fetch memo details: ${response.statusText}`);
        }
        
        const data = await response.json();
        if (data.success) {
          // Navigate based on user role
          const userRole = userStore.getters.roleName()?.toLowerCase();
          
          if (userRole === 'qa reviewer') {
            // Reviewers use the InspectionMemo component
            this.$router.push({ 
              name: 'InspectionMemo', 
              params: { 
                id: memo.id
              },
              query: {
                hasData: 'true'
              }
            });
            // Store the data in sessionStorage for the component to access
            sessionStorage.setItem(`memoData_${memo.id}`, JSON.stringify(data.memo));
            sessionStorage.setItem(`references_${memo.id}`, JSON.stringify(data.references || []));
          } else {
            // All other roles use the ViewOnlyMemoForm component
            this.$router.push({ 
              name: 'ViewOnlyMemoForm', 
              params: { 
                id: memo.id
              },
              query: {
                hasData: 'true'
              }
            });
            // Store the data in sessionStorage for the component to access
            sessionStorage.setItem(`memoData_${memo.id}`, JSON.stringify(data.memo));
            sessionStorage.setItem(`references_${memo.id}`, JSON.stringify(data.references || []));
          }
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
    submitNewMemo() {
      this.$router.push({ name: 'NewMemoForm' });
    },
    openNotifications() {
      this.$router.push({ name: 'QAHeadNotifications' });
    },
    openSharedMemos() {
      this.$router.push({ name: 'SharedMemoDashboard' }); 
    },
    shareMemo(memo) {
      this.selectedMemo = memo;
      this.showShareModal = true;
    },
    toggleShareModal() {
      this.showShareModal = !this.showShareModal;
      if (!this.showShareModal) {
        this.selectedReviewerId = '';
        this.selectedMemo = null;
      }
    },
    async fetchReviewers() {
      try {
        // Get current user information
        const currentUser = userStore.getters.currentUser();
        if (!currentUser) {
          console.error('No current user found');
          this.reviewers = [];
          return;
        }

        // Build query parameters to exclude current user
        const params = new URLSearchParams();
        params.append('current_user_id', currentUser.id);

        const response = await fetch(`/api/reviewers?${params.toString()}`);
        if (!response.ok) {
          throw new Error(`Failed to fetch reviewers: ${response.statusText}`);
        }
        
        const data = await response.json();
        if (data.success) {
          this.reviewers = data.reviewers;
          console.log(`Fetched ${this.reviewers.length} reviewers (excluding current user)`);
        } else {
          throw new Error(data.message || 'Failed to fetch reviewers');
        }
      } catch (error) {
        console.error('Error fetching reviewers:', error);
        this.reviewers = [];
      }
    },
    onReviewerChange() {
      // This method is called when reviewer selection changes
      // The selectedReviewerId is automatically updated by v-model
      console.log('Selected reviewer ID:', this.selectedReviewerId);
    },
    getSelectedReviewerName() {
      const reviewer = this.reviewers.find(r => r.user_id == this.selectedReviewerId);
      return reviewer ? reviewer.name : '';
    },
    getSelectedReviewerEmail() {
      const reviewer = this.reviewers.find(r => r.user_id == this.selectedReviewerId);
      return reviewer ? reviewer.email : '';
    },
    async shareMemoWithReviewer() {
      if (!this.selectedReviewerId) {
        alert('Please select a reviewer to share with.');
        return;
      }

      try {
        const currentUser = userStore.getters.currentUser();
        if (!currentUser) {
          alert('User not logged in.');
          return;
        }

        // Prepare the sharing data
        const shareData = {
          memo_id: this.selectedMemo.id,
          shared_by: currentUser.id,
          shared_with: parseInt(this.selectedReviewerId)
        };

        console.log('Sharing memo with data:', shareData);

        const response = await fetch('/api/memos/share', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(shareData)
        });

        const data = await response.json();
        if (data.success) {
          const reviewer = this.reviewers.find(r => r.user_id == this.selectedReviewerId);
          alert(`Memo ID ${this.selectedMemo.id} shared successfully with ${reviewer.name} (${reviewer.email})!`);
          this.toggleShareModal();
        } else {
          alert(`Error sharing memo: ${data.message}`);
        }
      } catch (error) {
        console.error('Error sharing memo:', error);
        alert('Error sharing memo. Please try again.');
      }
    }
  }
};
</script>

<style scoped>
/* same styles as before, combining both */
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


.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.notification-container {
  position: relative;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  transition: all 0.3s ease;
}
.notification-container:hover {
  background-color: #f0f0f0;
}
.notification-icon {
  position: relative;
  color: #333;
}
.notification-badge {
  position: absolute;
  top: -8px;
  right: -8px;
  background-color: #ff4757;
  color: white;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  font-size: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
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
  left: -125px;
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

/* Status-based colors */
.success, .successfully-completed { background-color: #e2fbdc; }
.rejected { background-color: #ff4757; color: white; }
.disapproved { background-color: #ffd8d6; }
.assigned { background-color: #d1d8ff; }
.observation, .completed-with-observations { background-color: #fdddfa; }
.not-conducted, .test-not-conducted { background-color: #fdd8d6; }
.not-assigned { background-color: #fff1d6; }
.test-failed { background-color: #ff6b6b; color: white; }

/* Specific status classes for dynamic status values */
.successfully-completed { background-color: #e2fbdc; }
.test-not-conducted { background-color: #fdd8d6; }
.completed-with-observations { background-color: #fdddfa; }
.test-failed { background-color: #ff6b6b; color: white; }

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
.memo-details { flex-grow: 1; }
.memo-project { font-weight: bold; font-size: 1.1em; }
.memo-author { font-size: 0.9em; color: #555; }
.memo-schedule { text-align: right; font-size: 0.9em; color: #555; }

/* New button */
.submit-new-memo-button {
  background: linear-gradient(to right, #a0d9e6, #5cb8de);
  color: white;
  border: none;
  border-radius: 20px;
  padding: 10px 15px;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
  margin-left: 20px;
  white-space: nowrap;
}
.submit-new-memo-button:hover {
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.3);
  transform: translateY(-2px);
}

.shared-with-me-button {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #0066cc;
  color: white;
  border: none;
  border-radius: 25px;
  padding: 10px 18px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}
.shared-with-me-button:hover {
  background: #005bb5;
}
.shared-with-me-button svg {
  stroke: white;
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
  border-top: 4px solid #5cb8de;
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
  background: #5cb8de;
  color: white;
  border: none;
  border-radius: 25px;
  padding: 10px 20px;
  cursor: pointer;
  margin-top: 15px;
  transition: background 0.3s ease;
}

.retry-button:hover {
  background: #4a9bc1;
}

.empty-subtitle {
  font-size: 0.9em;
  color: #999;
  margin-top: 10px;
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
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 123, 255, 0.2);
  margin-right: 300px;
}

.share-btn:hover {
  background-color: #0056b3;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 123, 255, 0.3);
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
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.share-modal-content {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  width: 90%;
  max-width: 500px;
  max-height: 80vh;
  overflow-y: auto;
}

.share-modal-content h2 {
  margin: 0 0 20px 0;
  color: #333;
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

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #333;
}

.reviewer-select {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
  background-color: white;
  box-sizing: border-box;
  cursor: pointer;
}

.reviewer-select:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.reviewer-details {
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  padding: 16px;
  border-radius: 8px;
  border: 1px solid #bae6fd;
  margin-top: 8px;
  font-size: 0.9em;
  line-height: 1.6;
}

.reviewer-details strong {
  color: #0369a1;
  font-weight: 600;
}

.modal-actions {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.send-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.send-btn:hover:not(:disabled) {
  background-color: #0056b3;
  transform: translateY(-1px);
}

.send-btn:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.cancel-btn {
  background-color: #6c757d;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-btn:hover {
  background-color: #5a6268;
  transform: translateY(-1px);
}

</style>
