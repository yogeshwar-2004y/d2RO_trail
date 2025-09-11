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
        <div class="logos-container">
          <img src="@/assets/images/aviatrax-logo.png" alt="Aviatrax Logo" class="logo">
          <img src="@/assets/images/vista_logo.png" alt="Vista Logo" class="logo vista-logo">
        </div>
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
      <div 
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
export default {
  name: 'SharedMemoDashboard',
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
      sharedMemos: [
        { 
          id: 101, 
          project: 'PROJ001', 
          author: 'Design Team', 
          sharedBy: 'John Doe',
          sharedDate: '10-01-2025',
          assignedDate: '01-07-2025', 
          scheduledDate: '04-07-2025', 
          status: 'SUCCESSFULLY COMPLETED' 
        },
        { 
          id: 102, 
          project: 'PROJ002', 
          author: 'Design Team', 
          sharedBy: 'Jane Smith',
          sharedDate: '12-01-2025',
          assignedDate: '01-07-2025', 
          scheduledDate: '04-07-2025', 
          status: 'COMPLETED WITH OBSERVATIONS' 
        },
        { 
          id: 103, 
          project: 'PROJ003', 
          author: 'Design Team', 
          sharedBy: 'Mike Johnson',
          sharedDate: '15-01-2025',
          assignedDate: null, 
          scheduledDate: null, 
          status: 'NOT ASSIGNED' 
        },
        { 
          id: 104, 
          project: 'PROJ001', 
          author: 'Design Team', 
          sharedBy: 'Sarah Wilson',
          sharedDate: '18-01-2025',
          assignedDate: '01-07-2025', 
          scheduledDate: '04-07-2025', 
          status: 'DISAPPROVED' 
        },
        { 
          id: 105, 
          project: 'PROJ004', 
          author: 'Design Team', 
          sharedBy: 'David Brown',
          sharedDate: '20-01-2025',
          assignedDate: '01-07-2025', 
          scheduledDate: '04-07-2025', 
          status: 'SUCCESSFULLY COMPLETED' 
        },
      ],
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
</style>
