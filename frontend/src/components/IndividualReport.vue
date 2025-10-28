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
      </div>
      <div class="header-center">
        <h1 class="page-title">INDIVIDUAL REPORT</h1>
      </div>
      <div class="header-right">
        <button 
          v-if="selectedTemplate && !showTemplateSelection && canDownloadReport" 
          class="export-button" 
          @click="downloadReportPDF"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <line x1="10" y1="9" x2="8" y2="9"></line>
          </svg>
          DOWNLOAD PDF
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

      <!-- Template Selection State -->
      <div v-if="!selectedTemplate" class="no-reports-state">
        <div class="empty-icon">📄</div>
        
        <!-- Design Head can select template -->
        <div v-if="isDesignHead" class="template-message">
          <h3>Template not yet chosen</h3>
          <p>Please select a template to proceed with this report.</p>
          
          <div class="template-action">
            <button 
              @click="selectTemplate"
              class="choose-template-btn"
            >
              Choose Template
            </button>
          </div>
        </div>
        
        <!-- Other roles wait for Design Head to select template -->
        <div v-else class="report-message">
          <h3>Waiting for template selection</h3>
          <p>The Design Head needs to select a template before this report can be accessed.</p>
          
          <!-- Show different messages based on role -->
          <div v-if="isQAReviewer" class="role-message qa-reviewer">
            <div class="role-icon">🔍</div>
            <p><strong>QA Reviewer Access:</strong> Once the Design Head assigns a template, you will be able to fill out and submit this report.</p>
          </div>
          <div v-else-if="isQAHead" class="role-message qa-head">
            <div class="role-icon">👁️</div>
            <p><strong>QA Head - View Only Access:</strong> Once the Design Head assigns a template, you will be able to view this report but cannot edit it.</p>
          </div>
          <div v-else class="role-message other-role">
            <div class="role-icon">👁️</div>
            <p><strong>View-Only Access:</strong> You can view this report once a template is assigned, but only QA Reviewers can edit it.</p>
          </div>
        </div>
      </div>

      <!-- Template Form Display -->
      <div v-else class="template-form-container">
        <!-- Template Header -->
        <div class="template-form-header">
          <div class="template-info">
            <h3>{{ selectedTemplate.displayName }}</h3>
            <p>{{ selectedTemplate.description }}</p>
          </div>
          <div v-if="isDesignHead" class="template-actions">
            <button @click="selectTemplate" class="change-template-btn">
              Change Template
            </button>
          </div>
        </div>

        <!-- Template Form Content -->
        <div class="template-form-content">
          <!-- Role-based access message -->
          <div v-if="!canEditReport && selectedTemplate" class="access-message">
            <div v-if="isQAReviewer" class="access-info qa-reviewer">
              <div class="access-icon">🔍</div>
              <h4>QA Reviewer Access</h4>
              <p>You can edit and submit this report. All fields are enabled for input.</p>
              <p v-if="!isReportSubmitted" class="download-info">
                <strong>Note:</strong> Download PDF will be available after submitting the report.
              </p>
              <p v-else class="download-info success">
                <strong>✓</strong> Report submitted! You can now download the PDF.
              </p>
            </div>
            <div v-else-if="isQAHead" class="access-info qa-head">
              <div class="access-icon">👁️</div>
              <h4>QA Head - View Only Access</h4>
              <p>You can view this report but cannot edit it. Only QA Reviewers can make changes to the report data.</p>
            </div>
            <div v-else class="access-info view-only">
              <div class="access-icon">👁️</div>
              <h4>View-Only Access</h4>
              <p>You can view this report but cannot edit it. Only QA Reviewers can make changes.</p>
            </div>
          </div>
          
          <!-- Dynamic Template Component -->
          <component 
            v-if="currentTemplateComponent"
            :is="currentTemplateComponent"
            :projectName="projectName"
            :reportId="reportId"
            :reportName="reportName"
            :templateId="selectedTemplate.template_id"
            :templateName="selectedTemplate.name"
            :readonly="!canEditReport"
            :isTemplatePreview="false"
            @report-submitted="updateReportStatus"
          />
          
          <!-- Fallback if component not found -->
          <div v-else class="template-error">
            <div class="error-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="15" y1="9" x2="9" y2="15"></line>
                <line x1="9" y1="9" x2="15" y2="15"></line>
              </svg>
            </div>
            <h4>Template Component Not Found</h4>
            <p>The template "{{ selectedTemplate.displayName }}" could not be loaded.</p>
            <button @click="selectTemplate" class="change-template-btn">
              Select Different Template
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Template Selection Overlay -->
    <div v-if="showTemplateOverlay" class="template-overlay" @click="closeOverlay">
      <div class="template-overlay-content" @click.stop>
        <!-- Loading Overlay -->
        <div v-if="loading" class="loading-overlay">
          <div class="loading-spinner"></div>
        </div>
        <div class="template-overlay-header">
          <h2>Choose Report Template</h2>
          <button class="close-btn" @click="closeOverlay">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        
        <div class="template-overlay-body">
          <p class="template-description">Select a template for your report. Each template is designed for specific inspection types.</p>
          
          <div class="templates-grid">
            <div 
              v-for="template in availableTemplates" 
              :key="template.name"
              class="template-card"
              @click="selectTemplateOption(template)"
            >
              <div class="template-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                  <polyline points="14,2 14,8 20,8"></polyline>
                  <line x1="16" y1="13" x2="8" y2="13"></line>
                  <line x1="16" y1="17" x2="8" y2="17"></line>
                  <polyline points="10,9 9,9 8,9"></polyline>
                </svg>
              </div>
              <div class="template-info">
                <h3>{{ template.displayName }}</h3>
                <p>{{ template.description }}</p>
              </div>
              <div class="template-action">
                <button class="select-template-btn">Select</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { userStore } from '@/stores/userStore'
import html2pdf from 'html2pdf.js';

// Import all template components
import ObservationReport from '@/templates/ObservationReport.vue'
import BarePcbInspectionReport from '@/templates/barepcbinspectionreport.vue'
import Conformalcoatinginspectionreport from '@/templates/Conformalcoatinginspectionreport.vue'
import RawMaterialInspectionReport from '@/templates/RawMaterialInspectionReport.vue'
import CotsScreeningInspectionReport from '@/templates/CotsScreeningInspectionReport.vue'
import AssembledBoardInspectionReport from '@/templates/AssembledBoardInspectionReport.vue'
import KitOfPartInsp from '@/templates/KitOfPartInsp.vue'
import MechanicalInspection from '@/templates/MechanicalInspection.vue'

export default {
  name: 'IndividualReport',
  components: {
    ObservationReport,
    BarePcbInspectionReport,
    Conformalcoatinginspectionreport,
    RawMaterialInspectionReport,
    CotsScreeningInspectionReport,
    AssembledBoardInspectionReport,
    KitOfPartInsp,
    MechanicalInspection
  },
  data() {
    return {
      reportId: '',
      reportName: '',
      projectName: '',
      showTemplateOverlay: false,
      availableTemplates: [
        {
          template_id: 1,
          name: 'Conformalcoatinginspectionreport',
          displayName: 'Conformal Coating Inspection Report',
          description: 'Template for creating conformal coating inspection reports with quality testing criteria',
          component: 'Conformalcoatinginspectionreport'
        },
        {
          template_id: 2,
          name: 'CotsScreeningInspectionReport',
          displayName: 'COTS Screening Inspection Report',
          description: 'Template for creating COTS screening inspection reports with test case validation',
          component: 'CotsScreeningInspectionReport'
        },
        {
          template_id: 3,
          name: 'BarePcbInspectionReport',
          displayName: 'Bare PCB Inspection Report',
          description: 'Template for creating bare PCB inspection reports with comprehensive testing criteria',
          component: 'BarePcbInspectionReport'
        },
        {
          template_id: 4,
          name: 'MechanicalInspection',
          displayName: 'Mechanical Inspection Report',
          description: 'Template for creating mechanical inspection reports with structural testing criteria',
          component: 'MechanicalInspection'
        },
        {
          template_id: 5,
          name: 'AssembledBoardInspectionReport',
          displayName: 'Assembled Board Inspection Report',
          description: 'Template for creating assembled board inspection reports with comprehensive testing criteria',
          component: 'AssembledBoardInspectionReport'
        },
        {
          template_id: 6,
          name: 'RawMaterialInspectionReport',
          displayName: 'Raw Material Inspection Report',
          description: 'Template for creating raw material inspection reports with compliance checking',
          component: 'RawMaterialInspectionReport'
        },
        {
          template_id: 7,
          name: 'KitOfPartInsp',
          displayName: 'Kit of Part Inspection Report',
          description: 'Template for creating kit of part inspection reports with component verification',
          component: 'KitOfPartInsp'
        }
      ],
      selectedTemplate: null,
      loading: false,
      showTemplateSelection: false,
      reportStatus: null
    };
  },
  computed: {
    canSelectTemplate() {
      // Only Design Head (role_id = 4) can select templates
      const currentUserRole = userStore.getters.currentUserRole();
      return currentUserRole === 4;
    },
    
    isDesignHead() {
      const currentUserRole = userStore.getters.currentUserRole();
      return currentUserRole === 4;
    },
    
    isQAReviewer() {
      // QA Reviewer has role_id = 3
      const currentUserRole = userStore.getters.currentUserRole();
      return currentUserRole === 3;
    },
    
    isQAHead() {
      // QA Head has role_id = 2
      const currentUserRole = userStore.getters.currentUserRole();
      return currentUserRole === 2;
    },
    
    canEditReport() {
      // Only QA Reviewer can edit reports when template is assigned
      // QA Head has view-only access
      return this.isQAReviewer && this.selectedTemplate;
    },
    
    isReportSubmitted() {
      // Check if report has been submitted (status is not 'ASSIGNED')
      return this.reportStatus && this.reportStatus !== 'ASSIGNED';
    },
    
    canDownloadReport() {
      // QA Reviewer can download only after submitting the report
      // Other roles with view access can download anytime (if they have access)
      if (this.isQAReviewer) {
        return this.isReportSubmitted;
      }
      // For view-only users, they can download if they have access (but they don't have access anyway)
      return false;
    },
    
    currentTemplateComponent() {
      if (!this.selectedTemplate) return null;
      
      // Map template names to component names
      const componentMap = {
        'ObservationReport': 'ObservationReport',
        'BarePcbInspectionReport': 'BarePcbInspectionReport',
        'Conformalcoatinginspectionreport': 'Conformalcoatinginspectionreport',
        'RawMaterialInspectionReport': 'RawMaterialInspectionReport',
        'CotsScreeningInspectionReport': 'CotsScreeningInspectionReport',
        'AssembledBoardInspectionReport': 'AssembledBoardInspectionReport',
        'KitOfPartInsp': 'KitOfPartInsp',
        'MechanicalInspection': 'MechanicalInspection'
      };
      
      return componentMap[this.selectedTemplate.name] || null;
    }
  },
  mounted() {
    // Get parameters from route
    this.reportId = this.$route.params.reportId || '';
    this.reportName = this.$route.params.reportName || '';
    this.projectName = this.$route.params.projectName || '';
    
    // Load report details to check if template is already selected
    this.loadReportDetails();
  },
  methods: {
    selectTemplate() {
      console.log('Opening template selection overlay for report:', this.reportId);
      this.showTemplateOverlay = true;
      this.showTemplateSelection = true;
    },
    
    closeOverlay() {
      this.showTemplateOverlay = false;
      this.showTemplateSelection = false;
    },
    
    async selectTemplateOption(template) {
      console.log('Selected template:', template.name, 'for report:', this.reportId);
      
      try {
        this.loading = true;
        
        // Update report with selected template_id
        const response = await fetch(`/api/reports/${this.reportId}/template`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            template_id: template.template_id
          })
        });
        
        const result = await response.json();
        
        if (result.success) {
          // Set the selected template
          this.selectedTemplate = template;
          
          // Close the overlay
          this.closeOverlay();
          
          // Show success message
          alert(`Template "${template.displayName}" has been selected successfully!`);
        } else {
          alert(`Error: ${result.message}`);
        }
      } catch (error) {
        console.error('Error selecting template:', error);
        alert('An error occurred while selecting the template. Please try again.');
      } finally {
        this.loading = false;
      }
    },
    
    // Method to update report status (called when report is submitted)
    updateReportStatus(newStatus) {
      this.reportStatus = newStatus;
      console.log('Report status updated to:', newStatus);
    },
    
    async loadReportDetails() {
      if (!this.reportId) return;
      
      try {
        const response = await fetch(`http://localhost:8000/api/reports/${this.reportId}`);
        const result = await response.json();
        
        if (result.success) {
          // Set report status
          this.reportStatus = result.report.status;
          
          // Find the template that matches the template_id
          if (result.report.template_id) {
            const template = this.availableTemplates.find(t => t.template_id === result.report.template_id);
            if (template) {
              this.selectedTemplate = template;
            }
          }
        }
      } catch (error) {
        console.error('Error loading report details:', error);
      }
    },
    
    
    uploadReport() {
      console.log('Uploading report:', this.reportId);
      alert(`Report upload for Report ID: ${this.reportId} will be implemented soon!`);
    },
    
    createReport() {
      console.log('Creating new report for:', this.reportId);
      alert(`Create new report for Report ID: ${this.reportId} will be implemented soon!`);
    },
    
    async downloadReportPDF() {
      try {
        // Get the element you want to convert (the main report content)
      const element = document.querySelector('.template-form-container');
        
        if (!element) {
          alert('Report content not found');
          return;
        }
        
        // Configure options to match the page appearance
        const opt = {
          margin: 0.5,
          filename: `Report_${this.reportId}_${this.reportName?.replace(/[^a-zA-Z0-9]/g, '_') || 'Individual'}_${new Date().toISOString().slice(0, 10)}.pdf`,
          image: { type: 'jpeg', quality: 0.98 },
          html2canvas: { 
            scale: 2,
            useCORS: true,
            letterRendering: true,
            allowTaint: true,
            windowWidth: element.scrollWidth,
            windowHeight: element.scrollHeight
          },
          jsPDF: { 
            unit: 'in', 
            format: 'a4', 
            orientation: 'portrait' 
          }
        };
        
        // Generate PDF from HTML
        await html2pdf().set(opt).from(element).save();
        
        alert("Report PDF downloaded successfully!");
        
      } catch (error) {
        console.error('Error downloading report PDF:', error);
        alert(`Error downloading report PDF: ${error.message || "Unknown error"}. Please try again.`);
      }
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

/* Template Form Container Styles */
.template-form-container {
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.template-form-header {
  background: #f8f9fa;
  padding: 25px 30px;
  border-bottom: 1px solid #e9ecef;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.template-info h3 {
  color: #2d3748;
  font-size: 1.8em;
  font-weight: 600;
  margin: 0 0 8px 0;
}

.template-info p {
  color: #6c757d;
  font-size: 1em;
  margin: 0;
  line-height: 1.5;
}

.template-form-header .template-actions {
  flex-shrink: 0;
}

.template-form-content {
  padding: 0;
}

.template-placeholder {
  text-align: center;
  padding: 40px 20px;
}

.template-icon-large {
  color: #007bff;
  margin: 0 auto 20px auto;
  display: flex;
  justify-content: center;
}

.template-placeholder h4 {
  color: #2d3748;
  font-size: 1.5em;
  font-weight: 600;
  margin: 0 0 15px 0;
}

.template-placeholder p {
  color: #6c757d;
  font-size: 1.1em;
  margin: 0 0 30px 0;
  line-height: 1.6;
}

.template-placeholder .open-template-btn {
  background: #007bff;
  color: white;
  border: none;
  padding: 15px 30px;
  border-radius: 10px;
  font-size: 1.1em;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 123, 255, 0.3);
}

.template-placeholder .open-template-btn:hover {
  background: #0056b3;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 123, 255, 0.4);
}

/* Template Error State */
.template-error {
  text-align: center;
  padding: 40px 20px;
}

.error-icon {
  color: #dc3545;
  margin: 0 auto 20px auto;
  display: flex;
  justify-content: center;
}

.template-error h4 {
  color: #dc3545;
  font-size: 1.5em;
  font-weight: 600;
  margin: 0 0 15px 0;
}

.template-error p {
  color: #6c757d;
  font-size: 1.1em;
  margin: 0 0 30px 0;
  line-height: 1.6;
}

.change-template-btn {
  background: #6c757d;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9em;
}

.change-template-btn:hover {
  background: #5a6268;
  transform: scale(1.05);
}

/* Loading state */
.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1001;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Responsive Design for Template Form */
@media (max-width: 768px) {
  .template-form-header {
    flex-direction: column;
    text-align: center;
    gap: 20px;
    padding: 20px;
  }
  
  .template-form-content {
    padding: 0;
  }
  
  .template-placeholder {
    padding: 30px 15px;
  }
  
  .template-placeholder h4 {
    font-size: 1.3em;
  }
  
  .template-placeholder p {
    font-size: 1em;
  }
  
  .template-placeholder .open-template-btn {
    padding: 12px 25px;
    font-size: 1em;
    width: 100%;
    max-width: 300px;
  }
  
  .change-template-btn {
    padding: 12px 20px;
    font-size: 0.9em;
    width: 100%;
    max-width: 200px;
  }
}

/* Template Overlay Styles */
.template-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
  animation: fadeIn 0.3s ease-out;
}

.template-overlay-content {
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  max-width: 900px;
  width: 90%;
  max-height: 80vh;
  overflow: hidden;
  animation: slideIn 0.3s ease-out;
}

.template-overlay-header {
  background: #2d3748;
  color: white;
  padding: 25px 30px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #e2e8f0;
}

.template-overlay-header h2 {
  margin: 0;
  font-size: 1.8em;
  font-weight: 600;
}

.close-btn {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: white;
  cursor: pointer;
  padding: 10px;
  border-radius: 50%;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.1);
}

.template-overlay-body {
  padding: 30px;
  max-height: calc(80vh - 100px);
  overflow-y: auto;
}

.template-description {
  color: #6c757d;
  font-size: 1.1em;
  margin: 0 0 30px 0;
  text-align: center;
  line-height: 1.6;
}

.templates-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
}

.template-card {
  background: #f8f9fa;
  border: 2px solid #e9ecef;
  border-radius: 15px;
  padding: 25px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 20px;
  position: relative;
  overflow: hidden;
}

.template-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(0, 123, 255, 0.05) 0%, rgba(0, 123, 255, 0.1) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.template-card:hover {
  border-color: #007bff;
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 123, 255, 0.2);
}

.template-card:hover::before {
  opacity: 1;
}

.template-icon {
  color: #007bff;
  flex-shrink: 0;
  transition: transform 0.3s ease;
}

.template-card:hover .template-icon {
  transform: scale(1.1);
}

.template-info {
  flex: 1;
  z-index: 1;
  position: relative;
}

.template-info h3 {
  color: #2d3748;
  font-size: 1.3em;
  font-weight: 600;
  margin: 0 0 8px 0;
}

.template-info p {
  color: #6c757d;
  font-size: 0.95em;
  margin: 0;
  line-height: 1.5;
}

.template-action {
  flex-shrink: 0;
  z-index: 1;
  position: relative;
}

.select-template-btn {
  background: #007bff;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9em;
}

.select-template-btn:hover {
  background: #0056b3;
  transform: scale(1.05);
}

/* Animations */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-50px) scale(0.9);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Responsive Design for Overlay */
@media (max-width: 768px) {
  .template-overlay-content {
    width: 95%;
    margin: 20px;
  }
  
  .template-overlay-header {
    padding: 20px;
  }
  
  .template-overlay-header h2 {
    font-size: 1.5em;
  }
  
  .template-overlay-body {
    padding: 20px;
  }
  
  .templates-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  
  .template-card {
    padding: 20px;
    flex-direction: column;
    text-align: center;
    gap: 15px;
  }
  
  .template-info h3 {
    font-size: 1.2em;
  }
  
  .template-info p {
    font-size: 0.9em;
  }
}

/* Role-based Access Messages */
.role-message {
  margin-top: 20px;
  padding: 20px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 15px;
  animation: fadeIn 0.5s ease-in-out;
}

.role-message.qa-reviewer {
  background: linear-gradient(135deg, #e8f5e8, #f0f8f0);
  border: 2px solid #28a745;
  border-left: 6px solid #28a745;
}

.role-message.qa-head {
  background: linear-gradient(135deg, #e3f2fd, #f3e5f5);
  border: 2px solid #2196f3;
  border-left: 6px solid #2196f3;
}

.role-message.other-role {
  background: linear-gradient(135deg, #fff3cd, #fef9e7);
  border: 2px solid #ffc107;
  border-left: 6px solid #ffc107;
}

.role-icon {
  font-size: 2em;
  flex-shrink: 0;
}

.role-message p {
  margin: 0;
  color: #2d3748;
  font-size: 0.95em;
  line-height: 1.6;
}

.role-message strong {
  color: #1a202c;
  font-weight: 600;
}

/* Access Message in Template Form */
.access-message {
  margin-bottom: 25px;
  padding: 20px;
  border-radius: 12px;
  animation: slideIn 0.6s ease-out;
}

.access-info {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  border-radius: 8px;
}

.access-info.qa-reviewer {
  background: linear-gradient(135deg, #d4edda, #c3e6cb);
  border: 2px solid #28a745;
  border-left: 6px solid #28a745;
}

.access-info.qa-head {
  background: linear-gradient(135deg, #e3f2fd, #f3e5f5);
  border: 2px solid #2196f3;
  border-left: 6px solid #2196f3;
}

.access-info.view-only {
  background: linear-gradient(135deg, #f8d7da, #f5c6cb);
  border: 2px solid #dc3545;
  border-left: 6px solid #dc3545;
}

.access-icon {
  font-size: 1.8em;
  flex-shrink: 0;
}

.access-info h4 {
  margin: 0 0 5px 0;
  color: #1a202c;
  font-size: 1.1em;
  font-weight: 600;
}

.access-info p {
  margin: 0;
  color: #2d3748;
  font-size: 0.9em;
  line-height: 1.5;
}

.download-info {
  margin-top: 8px !important;
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 0.85em !important;
  background: rgba(255, 193, 7, 0.1);
  border-left: 3px solid #ffc107;
}

.download-info.success {
  background: rgba(40, 167, 69, 0.1);
  border-left: 3px solid #28a745;
  color: #155724;
}

/* Responsive Design for Role Messages */
@media (max-width: 768px) {
  .role-message,
  .access-info {
    flex-direction: column;
    text-align: center;
    gap: 10px;
  }
  
  .role-icon,
  .access-icon {
    font-size: 1.5em;
  }
  
  .access-info h4 {
    font-size: 1em;
  }
  
  .role-message p,
  .access-info p {
    font-size: 0.85em;
  }
}
</style>
