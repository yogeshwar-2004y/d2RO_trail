<template>
  <div class="individual-report-page">
    <!-- Header -->
    <div class="page-header">
      <div class="header-left">
        <button class="back-button" @click="$router.go(-1)">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19 12H5"></path>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
        </button>
        <div class="logos-container">
          <img src="@/assets/images/aviatrax-logo.png" alt="Aviatrax Logo" class="app-logo">
          <img src="@/assets/images/vista_logo.png" alt="Vista Logo" class="app-logo vista-logo">
        </div>
      </div>
      <div class="header-center">
        <h1 class="page-title">INDIVIDUAL REPORT</h1>
      </div>
      <div class="header-right">
        <button class="export-button" @click="exportReport">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="7,10 12,15 17,10"></polyline>
            <line x1="12" y1="15" x2="12" y2="3"></line>
          </svg>
          EXPORT
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Report Header -->
      <div class="report-header">
        <div class="report-title">
          <h2>{{ reportName || 'Report Details' }}</h2>
          <div class="report-meta">
            <span class="report-id">Report ID: {{ reportId }}</span>
            <span class="project-name">Project: {{ projectName }}</span>
          </div>
        </div>
      </div>

      <!-- No Reports Uploaded State -->
      <div class="no-reports-state">
        <div class="empty-icon">📄</div>
        
        <!-- Different messages based on user role -->
        <div v-if="canSelectTemplate" class="template-message">
          <h3>Template not yet chosen</h3>
          <p>Please select a template to proceed with this report.</p>
          
          <!-- Single Choose Template Button for QA Head/Design Head -->
          <div class="template-action">
            <button 
              @click="selectTemplate"
              class="choose-template-btn"
            >
              Choose Template
            </button>
          </div>
        </div>
        
        <div v-else class="report-message">
          <h3>Report not uploaded yet</h3>
          <p>This report is currently empty and needs to be populated with observations and data.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { userStore } from '@/stores/userStore';

export default {
  name: 'IndividualReport',
  data() {
    return {
      reportId: '',
      reportName: '',
      projectName: ''
    };
  },
  computed: {
    canSelectTemplate() {
      // Only QA Head (role_id = 2) and Design Head (role_id = 4) can select templates
      const currentUserRole = userStore.getters.currentUserRole();
      return currentUserRole === 2 || currentUserRole === 4;
    }
  },
  mounted() {
    // Get parameters from route
    this.reportId = this.$route.params.reportId || '';
    this.reportName = this.$route.params.reportName || '';
    this.projectName = this.$route.params.projectName || '';
  },
  methods: {
    selectTemplate() {
      console.log('Choosing template for report:', this.reportId);
      alert(`Choose template for Report ID: ${this.reportId} will be implemented soon!`);
    },
    
    uploadReport() {
      console.log('Uploading report:', this.reportId);
      alert(`Report upload for Report ID: ${this.reportId} will be implemented soon!`);
    },
    
    createReport() {
      console.log('Creating new report for:', this.reportId);
      alert(`Create new report for Report ID: ${this.reportId} will be implemented soon!`);
    },
    
    exportReport() {
      console.log('Exporting report:', this.reportId);
      alert(`Export report for Report ID: ${this.reportId} will be implemented soon!`);
    }
  }
};
</script>

<style scoped>
.individual-report-page {
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

.app-logo {
  width: 120px;
  height: auto;
  filter: brightness(0) invert(1);
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

.header-right {
  display: flex;
  align-items: center;
}

.export-button {
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

.export-button:hover {
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

/* Report Header */
.report-header {
  background: white;
  padding: 25px;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 25px;
}

.report-title h2 {
  color: #2d3748;
  font-size: 1.8em;
  margin: 0 0 15px 0;
  font-weight: 600;
}

.report-meta {
  display: flex;
  gap: 30px;
  flex-wrap: wrap;
}

.report-id,
.project-name {
  color: #4a5568;
  font-size: 1em;
  font-weight: 500;
}

.report-id {
  background: #e2e8f0;
  padding: 8px 15px;
  border-radius: 20px;
}

.project-name {
  background: #f0f4f8;
  padding: 8px 15px;
  border-radius: 20px;
}

/* No Reports State */
.no-reports-state {
  background: white;
  padding: 60px 40px;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 30px;
}

.empty-icon {
  font-size: 5em;
  opacity: 0.6;
}

.no-reports-state h3 {
  color: #ffc107;
  font-size: 2.2em;
  margin: 0;
  font-weight: 600;
}

.template-message h3 {
  color: #007bff;
  font-size: 2.2em;
  margin: 0;
  font-weight: 600;
}

.report-message h3 {
  color: #ffc107;
  font-size: 2.2em;
  margin: 0;
  font-weight: 600;
}

.no-reports-state p {
  color: #6c757d;
  font-size: 1.2em;
  margin: 0;
  max-width: 600px;
  line-height: 1.6;
}

.template-action {
  margin-top: 30px;
}

.choose-template-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 18px 40px;
  border-radius: 10px;
  font-size: 1.3em;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 6px 20px rgba(0, 123, 255, 0.3);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.choose-template-btn:hover {
  background-color: #0056b3;
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 123, 255, 0.4);
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
  
  .report-meta {
    flex-direction: column;
    gap: 10px;
  }
  
  .no-reports-state {
    padding: 40px 20px;
  }
  
  .empty-icon {
    font-size: 4em;
  }
  
  .no-reports-state h3 {
    font-size: 1.8em;
  }
  
  .template-message h3,
  .report-message h3 {
    font-size: 1.8em;
  }
  
  .no-reports-state p {
    font-size: 1.1em;
  }
  
  .choose-template-btn {
    padding: 15px 30px;
    font-size: 1.1em;
    width: 250px;
  }
}
</style>
