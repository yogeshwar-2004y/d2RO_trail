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
        <div class="logos-container">
          <img src="@/assets/images/aviatrax-logo.png" alt="Aviatrax Logo" class="logo">
          <img src="@/assets/images/vista_logo.png" alt="Vista Logo" class="logo vista-logo">
        </div>
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
      <div 
        v-for="memo in filteredMemos" 
        :key="memo.id" 
        class="memo-card" 
        :class="memo.status.toLowerCase().replace(/ /g, '-')"
        @click="viewMemo(memo)"
      >
        <div class="memo-details">
          <div class="memo-project">{{ memo.project }}</div>
          <div class="memo-author">FROM - AUTHORISING EMP (DESIGN TEAM)</div>
        </div>
        <div class="memo-schedule" v-if="memo.assignedDate">
          <div class="memo-assigned">ASSIGNED ON : {{ memo.assignedDate }}</div>
          <div class="memo-scheduled">TEST SCHEDULED ON : {{ memo.scheduledDate }}</div>
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
      projects: ['PROJ001', 'PROJ002', 'PROJ003', 'PROJ004', 'PROJ005', 'PROJ006'],
      memoStatuses: [
        { name: 'SUCCESSFULLY COMPLETED', color: 'success' },
        { name: 'DISAPPROVED', color: 'disapproved' },
        { name: 'ASSIGNED', color: 'assigned' },
        { name: 'COMPLETED WITH OBSERVATIONS', color: 'observation' },
        { name: 'TEST NOT CONDUCTED', color: 'not-conducted' },
        { name: 'NOT ASSIGNED', color: 'not-assigned' },
      ],
      memos: [
        { id: 1, project: 'PROJ001', author: 'Design Team', assignedDate: '01-07-2025', scheduledDate: '04-07-2025', status: 'NOT ASSIGNED' },
        { id: 2, project: 'PROJ002', author: 'Design Team', assignedDate: '01-07-2025', scheduledDate: '04-07-2025', status: 'ASSIGNED' },
        { id: 3, project: 'PROJ003', author: 'Design Team', assignedDate: null, scheduledDate: null, status: 'NOT ASSIGNED' },
        { id: 4, project: 'PROJ001', author: 'Design Team', assignedDate: '01-07-2025', scheduledDate: '04-07-2025', status: 'SUCCESSFULLY COMPLETED' },
        { id: 5, project: 'PROJ002', author: 'Design Team', assignedDate: '01-07-2025', scheduledDate: '04-07-2025', status: 'DISAPPROVED' },
        { id: 6, project: 'PROJ003', author: 'Design Team', assignedDate: '01-07-2025', scheduledDate: '04-07-2025', status: 'COMPLETED WITH OBSERVATIONS' },
        { id: 7, project: 'PROJ001', author: 'Design Team', assignedDate: '01-07-2025', scheduledDate: '04-07-2025', status: 'TEST NOT CONDUCTED' },
        { id: 8, project: 'PROJ004', author: 'Design Team', assignedDate: '01-07-2025', scheduledDate: '04-07-2025', status: 'SUCCESSFULLY COMPLETED' },
      ],
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
  methods: {
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
      this.$router.push({ name: 'SubmitMemo' });
    },
    viewMemo(memo) {
      this.$router.push({ name: 'MemoForm', params: { memoId: memo.id } });
    },
    openNotifications() {
      this.$router.push({ name: 'QAHeadNotifications' });
    },
    openSharedMemos() {
    this.$router.push({ name: 'SharedMemoDashboard' }); 
    // 👆 replace with the actual route/view you want to navigate to
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

.logo {
  width: 150px;
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

/* Status-based colors */
.success, .successfully-completed { background-color: #e2fbdc; }
.disapproved { background-color: #ffd8d6; }
.assigned { background-color: #d1d8ff; }
.observation, .completed-with-observations { background-color: #fdddfa; }
.not-conducted, .test-not-conducted { background-color: #fdd8d6; }
.not-assigned { background-color: #fff1d6; }

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

</style>
