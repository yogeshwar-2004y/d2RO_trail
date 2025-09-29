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
        <div class="logos-container">
          <img src="@/assets/images/aviatrax-logo.png" alt="Aviatrax Logo" class="logo">
          <img src="@/assets/images/vista_logo.png" alt="Vista Logo" class="logo vista-logo">
        </div>
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
        <button class="export-all-button" @click="exportAllReports">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="7,10 12,15 17,10"></polyline>
            <line x1="12" y1="15" x2="12" y2="3"></line>
          </svg>
          EXPORT ALL
        </button>
      </div>
    </div>
    
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>Loading reports...</p>
    </div>
    
    <div v-else-if="error" class="error-container">
      <div class="error-message">
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="15" y1="9" x2="9" y2="15"></line>
          <line x1="9" y1="9" x2="15" y2="15"></line>
        </svg>
        <h3>Error Loading Reports</h3>
        <p>{{ error }}</p>
        <button @click="fetchReports" class="retry-button">Retry</button>
      </div>
    </div>
    
    <div v-else class="report-grid">
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
      
      <div v-if="filteredReports.length === 0" class="no-reports">
        <div class="no-reports-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
          </svg>
        </div>
        <h3>No Reports Found</h3>
        <p>No reports match your current filters.</p>
      </div>
    </div>
  </div>
</template>

<script>
import jsPDF from 'jspdf';

export default {
  name: 'QAHeadReportDashboard',
  data() {
    return {
      searchQuery: '',
      showProjectFilter: false,
      showReportFilter: false,
      activeProjectFilter: null,
      activeReportFilter: null,
      projects: [],
      reportStatuses: [
        { name: 'SUCCESSFULLY COMPLETED', color: 'success' },
        { name: 'ASSIGNED', color: 'assigned' },
        { name: 'TEST NOT CONDUCTED', color: 'not-conducted' },
        { name: 'TEST FAILED', color: 'failed' },
      ],
      reports: [],
      loading: true,
      error: null,
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
  async mounted() {
    await this.fetchReports();
    await this.fetchProjects();
  },
  methods: {
    async fetchReports() {
      try {
        this.loading = true;
        const response = await fetch('http://localhost:5000/api/reports');
        
        if (!response.ok) {
          throw new Error(`Failed to fetch reports: ${response.statusText}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
          this.reports = data.reports;
        } else {
          throw new Error(data.message || 'Failed to fetch reports');
        }
      } catch (error) {
        console.error('Error fetching reports:', error);
        this.error = error.message;
      } finally {
        this.loading = false;
      }
    },
    
    async fetchProjects() {
      try {
        const response = await fetch('http://localhost:5000/api/projects');
        
        if (!response.ok) {
          throw new Error(`Failed to fetch projects: ${response.statusText}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
          this.projects = data.projects.map(project => project.name);
        } else {
          throw new Error(data.message || 'Failed to fetch projects');
        }
      } catch (error) {
        console.error('Error fetching projects:', error);
        // Don't set error state for projects as it's not critical
      }
    },
    
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
        name: 'ObservationReport',
        params: {
          lruName: report.name,
          projectName: report.project,
          reportId: report.id
        }
      });
    },
    
    exportAllReports() {
      try {
        // Create new PDF document
        const doc = new jsPDF('p', 'mm', 'a4');
        const pageWidth = doc.internal.pageSize.getWidth();
        const pageHeight = doc.internal.pageSize.getHeight();
        const margin = 20;
        
        let yPosition = margin;
        
        // Set font styles
        doc.setFont('helvetica');
        
        // Header - Reports Summary
        doc.setFontSize(18);
        doc.setFont('helvetica', 'bold');
        doc.text('QA HEAD REPORTS SUMMARY', pageWidth / 2, yPosition, { align: 'center' });
        yPosition += 15;
        
        // Date
        doc.setFontSize(12);
        doc.setFont('helvetica', 'normal');
        const currentDate = new Date().toLocaleDateString('en-GB');
        doc.text(`Generated on: ${currentDate}`, pageWidth / 2, yPosition, { align: 'center' });
        yPosition += 20;
        
        // Filter information
        if (this.activeProjectFilter || this.activeReportFilter) {
          doc.setFontSize(10);
          doc.setFont('helvetica', 'bold');
          doc.text('Applied Filters:', margin, yPosition);
          yPosition += 8;
          
          if (this.activeProjectFilter) {
            doc.setFont('helvetica', 'normal');
            doc.text(`Project: ${this.activeProjectFilter}`, margin + 10, yPosition);
            yPosition += 6;
          }
          
          if (this.activeReportFilter) {
            doc.setFont('helvetica', 'normal');
            doc.text(`Status: ${this.activeReportFilter}`, margin + 10, yPosition);
            yPosition += 6;
          }
          yPosition += 10;
        }
        
        // Reports table
        doc.setFontSize(12);
        doc.setFont('helvetica', 'bold');
        doc.text('REPORTS LIST', pageWidth / 2, yPosition, { align: 'center' });
        yPosition += 15;
        
        // Table headers
        doc.setFontSize(10);
        doc.setFont('helvetica', 'bold');
        const tableStartX = margin;
        const snoWidth = 15;
        const projectWidth = 30;
        const nameWidth = 50;
        const statusWidth = 60;
        
        doc.text('SNO', tableStartX, yPosition);
        doc.text('Project', tableStartX + snoWidth, yPosition);
        doc.text('Report Name', tableStartX + snoWidth + projectWidth, yPosition);
        doc.text('Status', tableStartX + snoWidth + projectWidth + nameWidth, yPosition);
        yPosition += 8;
        
        // Draw table lines
        doc.line(margin, yPosition - 5, pageWidth - margin, yPosition - 5);
        doc.line(margin, yPosition, pageWidth - margin, yPosition);
        
        // Table data
        doc.setFont('helvetica', 'normal');
        this.filteredReports.forEach((report, index) => {
          yPosition += 8;
          
          // Check if we need a new page
          if (yPosition > pageHeight - 40) {
            doc.addPage();
            yPosition = margin + 20;
          }
          
          doc.text((index + 1).toString(), tableStartX, yPosition);
          doc.text(report.project, tableStartX + snoWidth, yPosition);
          doc.text(report.name, tableStartX + snoWidth + projectWidth, yPosition);
          doc.text(report.status, tableStartX + snoWidth + projectWidth + nameWidth, yPosition);
          
          yPosition += 8;
        });
        
        // Summary statistics
        yPosition += 15;
        doc.setFontSize(12);
        doc.setFont('helvetica', 'bold');
        doc.text('SUMMARY STATISTICS', pageWidth / 2, yPosition, { align: 'center' });
        yPosition += 15;
        
        doc.setFontSize(10);
        doc.setFont('helvetica', 'normal');
        
        const totalReports = this.filteredReports.length;
        const statusCounts = {};
        
        this.filteredReports.forEach(report => {
          statusCounts[report.status] = (statusCounts[report.status] || 0) + 1;
        });
        
        doc.text(`Total Reports: ${totalReports}`, margin, yPosition);
        yPosition += 8;
        
        Object.entries(statusCounts).forEach(([status, count]) => {
          doc.text(`${status}: ${count}`, margin + 10, yPosition);
          yPosition += 6;
        });
        
        // Save the PDF
        const fileName = `QA_Head_Reports_Summary_${currentDate.replace(/\//g, '-')}.pdf`;
        doc.save(fileName);
        
        // Show success message
        this.$nextTick(() => {
          alert('Reports summary exported successfully as PDF!');
        });
        
      } catch (error) {
        console.error('Error exporting PDF:', error);
        this.$nextTick(() => {
          alert(`Error exporting PDF: ${error.message || 'Unknown error'}. Please try again.`);
        });
      }
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

.export-all-button {
  background: linear-gradient(135deg, #28a745, #20c997);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 2px 8px rgba(40, 167, 69, 0.3);
}

.export-all-button:hover {
  background: linear-gradient(135deg, #218838, #1ea085);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(40, 167, 69, 0.4);
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

/* Loading, Error, and No Reports States */
.loading-container {
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
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-container {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
}

.error-message {
  text-align: center;
  max-width: 400px;
}

.error-message svg {
  color: #e74c3c;
  margin-bottom: 20px;
}

.error-message h3 {
  color: #e74c3c;
  margin-bottom: 10px;
}

.error-message p {
  color: #666;
  margin-bottom: 20px;
}

.retry-button {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s ease;
}

.retry-button:hover {
  background-color: #2980b9;
}

.no-reports {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
  grid-column: 1 / -1;
}

.no-reports-icon {
  margin-bottom: 20px;
}

.no-reports-icon svg {
  color: #bdc3c7;
}

.no-reports h3 {
  color: #7f8c8d;
  margin-bottom: 10px;
}

.no-reports p {
  color: #95a5a6;
}

/* Responsive Design */
@media (max-width: 768px) {
  .header {
    flex-direction: column;
    gap: 20px;
    padding: 15px 20px;
  }
  
  .header-right {
    flex-direction: column;
    gap: 15px;
    width: 100%;
  }
  
  .search-box {
    width: 100%;
  }
  
  .search-input {
    width: 100%;
  }
  
  .filter-dropdown {
    width: 100%;
  }
  
  .filter-button {
    width: 100%;
    text-align: center;
  }
  
  .export-all-button {
    width: 100%;
    justify-content: center;
  }
  
  .report-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 15px;
    padding: 20px;
  }
  
  .report-card {
    height: 150px;
    padding: 15px;
  }
}
</style>
