<template>
  <div class="report-dashboard">
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
      <div class="header-center">
        <div class="page-title">
          <svg class="title-icon" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <line x1="10" y1="9" x2="8" y2="9"></line>
          </svg>
          <span class="title-text">REPORTS</span>
        </div>
      </div>
      <div class="header-right">
        <div class="search-box">
          <input type="text" v-model="searchQuery" placeholder="Search Reports" class="search-input">
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
          <button class="filter-button" @click="toggleReportFilter">
            Filter Reports
          </button>
          <div v-if="showReportFilter" class="filter-panel">
            <div
              v-for="status in reportStatuses"
              :key="status.name"
              class="filter-option"
              :class="[status.color, { 'selected': activeReportFilter === status.name }]"
              @click="selectReportStatus(status.name)"
            >
              {{ status.name }}
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="report-grid">
      <div 
        v-for="report in filteredReports" 
        :key="report.id" 
        class="report-card" 
        :class="report.status.toLowerCase().replace(/ /g, '-')"
        @click="viewReport(report)"
      >
        <div class="card-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
          </svg>
        </div>
        <span class="card-title">{{ report.name }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QAHeadReportDashboard',
  data() {
    return {
      searchQuery: '',
      showProjectFilter: false,
      showReportFilter: false,
      activeProjectFilter: null,
      activeReportFilter: null,
      projects: ['PROJ001', 'PROJ002', 'PROJ003', 'PROJ004', 'PROJ005', 'PROJ006'],
      reportStatuses: [
        { name: 'SUCCESSFULLY COMPLETED', color: 'success' },
        { name: 'ASSIGNED', color: 'assigned' },
        { name: 'TEST NOT CONDUCTED', color: 'not-conducted' },
        { name: 'TEST FAILED', color: 'failed' },
      ],
      reports: [
        { id: 1, project: 'PROJ001', name: 'MEMO-2025-018', status: 'SUCCESSFULLY COMPLETED' },
        { id: 2, project: 'PROJ002', name: 'MEMO002', status: 'ASSIGNED' },
        { id: 3, project: 'PROJ003', name: 'MEMO003', status: 'TEST FAILED' },
        { id: 4, project: 'PROJ001', name: 'MEMO004', status: 'TEST NOT CONDUCTED' },
        { id: 5, project: 'PROJ002', name: 'MEMO005', status: 'SUCCESSFULLY COMPLETED' },
        { id: 6, project: 'PROJ003', name: 'MEMO006', status: 'ASSIGNED' },
        { id: 7, project: 'PROJ004', name: 'MEMO007', status: 'TEST NOT CONDUCTED' },
        { id: 8, project: 'PROJ004', name: 'MEMO008', status: 'TEST FAILED' },
        { id: 9, project: 'PROJ005', name: 'MEMO009', status: 'SUCCESSFULLY COMPLETED' },
        { id: 10, project: 'PROJ005', name: 'MEMO010', status: 'ASSIGNED' },
        { id: 11, project: 'PROJ006', name: 'MEMO011', status: 'TEST NOT CONDUCTED' },
        { id: 12, project: 'PROJ006', name: 'MEMO012', status: 'TEST FAILED' },
        { id: 13, project: 'PROJ001', name: 'MEMO013', status: 'SUCCESSFULLY COMPLETED' },
        { id: 14, project: 'PROJ002', name: 'MEMO014', status: 'ASSIGNED' },
        { id: 15, project: 'PROJ003', name: 'MEMO015', status: 'TEST NOT CONDUCTED' },
        { id: 16, project: 'PROJ004', name: 'MEMO016', status: 'TEST FAILED' },
      ],
    };
  },
  computed: {
    filteredReports() {
      let filtered = this.reports;

      if (this.activeProjectFilter) {
        filtered = filtered.filter(report => report.project === this.activeProjectFilter);
      }

      if (this.activeReportFilter) {
        filtered = filtered.filter(report => report.status === this.activeReportFilter);
      }
      
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(report => report.name.toLowerCase().includes(query));
      }

      return filtered;
    },
  },
  methods: {
    toggleProjectFilter() {
      this.showProjectFilter = !this.showProjectFilter;
      this.showReportFilter = false;
    },
    toggleReportFilter() {
      this.showReportFilter = !this.showReportFilter;
      this.showProjectFilter = false;
    },
    selectProject(project) {
      this.activeProjectFilter = this.activeProjectFilter === project ? null : project;
      this.showProjectFilter = false;
    },
    selectReportStatus(status) {
      this.activeReportFilter = this.activeReportFilter === status ? null : status;
      this.showReportFilter = false;
    },
    viewReport(report) {
      // Navigate to the QAHeadViewObservations form with report data
      this.$router.push({
        name: 'QAHeadViewObservations',
        params: {
          lruName: report.name,
          projectName: report.project,
          reportId: report.id
        }
      });
    }
  }
};
</script>

<style scoped>
.report-dashboard {
  font-family: Arial, sans-serif;
  min-height: 100vh;
  background-color: #f0f0f0;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 30px;
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

.header-center {
  display: flex;
  align-items: center;
  flex-grow: 1;
  justify-content: center;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.title-icon {
  color: #555;
  width: 32px;
  height: 32px;
}

.title-text {
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
  width: 250px;
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
  left: -114px;
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

/* Status-based colors for Report Filters */
.success, .successfully-completed {
  background-color: #e2fbdc;
}
.assigned {
  background-color: #c0f4f9;
}
.not-conducted, .test-not-conducted {
  background-color: #e8d0fd;
}
.failed, .test-failed {
  background-color: #ffc4be;
}

.report-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 20px;
  padding: 30px;
}

.report-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #fff;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  height: 180px;
  text-align: center;
}

.report-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

/* Dynamic card colors based on status */
.report-card.successfully-completed {
  background-color: #e2fbdc;
}
.report-card.assigned {
  background-color: #c0f4f9;
}
.report-card.test-not-conducted {
  background-color: #e8d0fd;
}
.report-card.test-failed {
  background-color: #ffc4be;
}

.card-icon {
  margin-bottom: 10px;
}

.card-icon svg {
  color: #555;
  width: 48px;
  height: 48px;
}

.card-title {
  font-size: 1em;
  font-weight: bold;
  color: #333;
}
</style>
