<template>
  <div class="test-reports-page">
    <div class="header">
      <div class="header-left">
        <button class="back-button" @click="$router.go(-1)">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19 12H5"></path>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
        </button>
        <div class="brand-section">
          <img src="@/assets/images/aviatrax-logo.png" alt="AVIATRAX Logo" class="logo">
        </div>
      </div>
      
      <div class="header-center">
        <div class="title-section">
          <span class="title-text">REPORT</span>
          <svg class="report-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14,2 14,8 20,8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <polyline points="10,9 9,9 8,9"></polyline>
          </svg>
        </div>
      </div>
      
      <div class="header-right">
        <div class="search-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </div>
        <div class="filter-dropdown">
          <button class="filter-button" @click="toggleProjectFilter">
            <svg class="filter-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polygon points="22,3 2,3 10,12.46 10,19 14,21 14,12.46 22,3"></polygon>
            </svg>
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
            <svg class="filter-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polygon points="22,3 2,3 10,12.46 10,19 14,21 14,12.46 22,3"></polygon>
            </svg>
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
    
    <div class="reports-grid">
      <div 
        v-for="report in filteredReports" 
        :key="report.id" 
        class="report-card"
        :class="report.status.toLowerCase().replace(/ /g, '-')"
        @click="selectReport(report)"
      >
        <div class="report-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14,2 14,8 20,8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <polyline points="10,9 9,9 8,9"></polyline>
          </svg>
        </div>
        <div class="report-label">
          <div class="report-text">MEMO</div>
          <div class="report-number">{{ report.number }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DesignerTestReportsPage',
  data() {
    return {
      showProjectFilter: false,
      showReportFilter: false,
      activeProjectFilter: null,
      activeReportFilter: null,
      projects: ['PROJ001', 'PROJ002', 'PROJ003', 'PROJ004', 'PROJ005', 'PROJ006'],
      reportStatuses: [
        { name: 'SUCCESSFULLY COMPLETED', color: 'successfully-completed' },
        { name: 'ASSIGNED', color: 'assigned' },
        { name: 'COMPLETED WITH OBSERVATIONS', color: 'completed-with-observations' },
        { name: 'TEST NOT CONDUCTED', color: 'test-not-conducted' },
        { name: 'TEST FAILED', color: 'test-failed' },
      ],
      reports: [
        { id: 1, number: '001', status: 'SUCCESSFULLY COMPLETED', project: 'PROJ001' },
        { id: 2, number: '002', status: 'ASSIGNED', project: 'PROJ002' },
        { id: 3, number: '004', status: 'TEST NOT CONDUCTED', project: 'PROJ003' },
        { id: 4, number: '005', status: 'SUCCESSFULLY COMPLETED', project: 'PROJ001' },
        { id: 5, number: '007', status: 'TEST FAILED', project: 'PROJ002' },
        { id: 6, number: '012', status: 'SUCCESSFULLY COMPLETED', project: 'PROJ003' },
        { id: 7, number: '013', status: 'TEST NOT CONDUCTED', project: 'PROJ004' },
        { id: 8, number: '019', status: 'ASSIGNED', project: 'PROJ005' },
        { id: 9, number: '020', status: 'COMPLETED WITH OBSERVATIONS', project: 'PROJ006' },
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
    selectReport(report) {
      // Handle report selection - navigate to report details or open modal
      console.log('Selected report:', report);
      // Example: this.$router.push({ name: 'ReportDetails', params: { reportId: report.id } });
    }
  }
};
</script>

<style scoped>
.test-reports-page {
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
  flex: 1;
}

.back-button {
  background: none;
  border: none;
  cursor: pointer;
  color: #333;
}

.brand-section {
  display: flex;
  align-items: center;
}

.logo {
  width: 150px;
}

.header-center {
  display: flex;
  justify-content: center;
  align-items: center;
  flex: 1;
}

.title-section {
  display: flex;
  align-items: center;
  gap: 10px;
}

.title-text {
  font-weight: bold;
  font-size: 1.1em;
  color: #333;
}

.report-icon {
  color: #333;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
  flex: 1;
  justify-content: flex-end;
}

.search-icon {
  cursor: pointer;
  color: #333;
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
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9em;
}

.filter-icon {
  color: #333;
}

.filter-panel {
  position: absolute;
  top: 100%;
  right: 0;
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

/* Status-based colors for Report Cards */
.successfully-completed {
  background-color: #e2fbdc; /* Light Green */
}
.assigned {
  background-color: #d1d8ff; /* Light Blue */
}
.completed-with-observations {
  background-color: #fdddfa; /* Light Pink */
}
.test-not-conducted {
  background-color: #ffd8d6; /* Light Red/Salmon */
}
.test-failed {
  background-color: #fdd8d6; /* Light Purple */
}

.reports-grid {
  padding: 20px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.report-card {
  border-radius: 15px;
  padding: 30px 20px;
  text-align: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  min-height: 150px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.report-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}

.report-icon {
  margin-bottom: 15px;
  color: #333;
}

.report-label {
  text-align: center;
}

.report-text {
  font-weight: bold;
  font-size: 1.1em;
  color: #333;
  margin-bottom: 5px;
}

.report-number {
  font-weight: bold;
  font-size: 1.3em;
  color: #333;
}

@media (max-width: 768px) {
  .header {
    flex-direction: column;
    gap: 15px;
  }
  
  .header-left,
  .header-center,
  .header-right {
    flex: none;
    width: 100%;
    justify-content: center;
  }
  
  .reports-grid {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 15px;
    padding: 15px;
  }
}
</style>
