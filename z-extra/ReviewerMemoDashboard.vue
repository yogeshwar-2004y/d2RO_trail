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
      <div 
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
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ReviewerMemoDashboard',
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
    openMemo(memoId) {
      // Navigate to the inspection memo page using Vue Router
      this.$router.push({ name: 'InspectionMemo', params: { id: memoId } });
    },
    goToSharedMemos() {
      // Navigate to the shared memos dashboard
      this.$router.push({ name: 'SharedMemoDashboard' });
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
</style>