<template>
  <div class="view-observations-page">
    <!-- Header -->
    <div class="page-header">
      <div class="header-left">
        <button class="back-button" @click="$router.go(-1)">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19 12H5"></path>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
        </button>
        <img src="@/assets/images/aviatrax-logo.png" alt="Aviatrax Logo" class="app-logo">
      </div>
      <div class="header-center">
        <h1 class="page-title">IQA OBSERVATION REPORT</h1>
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
        <div class="document-path">
          CASDIC/{{ projectName }}/{{ lruName }}/SL.{{ serialNumber }}/{{ observationCount }}/{{ currentYear }}
        </div>
        <div class="report-date">
          Date: {{ currentDate }}
        </div>
      </div>

      <div class="subject-line">
        SUB : IQA Observation Report for {{ lruName }}
        <span v-if="isVersionSpecific" class="version-info">
          (Version {{ currentVersion }} - Revision {{ reportData.revision }})
        </span>
      </div>

      <!-- Document Details Grid -->
      <div class="document-details">
        <div class="details-left">
          <div class="detail-item">
            <label>Project Name :</label>
            <span>{{ reportData.projectName }}</span>
          </div>
          <div class="detail-item">
            <label>Project Number :</label>
            <span>{{ reportData.projectNumber }}</span>
          </div>
          <div class="detail-item">
            <label>Project Date :</label>
            <span>{{ reportData.projectDate }}</span>
          </div>
          <div class="detail-item">
            <label>LRU Name :</label>
            <span>{{ reportData.lruName }}</span>
          </div>
          <div class="detail-item">
            <label>LRU Part No. :</label>
            <span>{{ lruPartNumber }}</span>
          </div>
          <div class="detail-item">
            <label>Serial Number:</label>
            <span>{{ serialNumber }}</span>
          </div>
        </div>
        <div class="details-right">
          <div class="detail-item">
            <label>Version :</label>
            <span class="version-badge">{{ reportData.version }}</span>
          </div>
          <div class="detail-item">
            <label>Revision :</label>
            <span class="revision-badge">{{ reportData.revision }}</span>
          </div>
          <div class="detail-item">
            <label>Inspection stage :</label>
            <span class="stage-value">Document review/report</span>
          </div>
          <div class="detail-item">
            <label>Date of doc review :</label>
            <span>{{ docReviewDate }}</span>
          </div>
          <div class="detail-item">
            <label>Review venue :</label>
            <span>{{ reviewVenue }}</span>
          </div>
          <div class="detail-item">
            <label>Reference Document:</label>
            <span>{{ referenceDocument }}</span>
          </div>
        </div>
      </div>

      <!-- Observations Table -->
      <div class="observations-section">
        <h2 class="section-title">Observations</h2>
        <div class="table-container">
          <table class="observations-table">
            <thead>
              <tr>
                <th>SNO</th>
                <th>Category (Major/Minor)</th>
                <th>Observations</th>
                <th>Accept/Reject</th>
                <th>Justification</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(observation, index) in reportData.observations" :key="index">
                <td>{{ index + 1 }}</td>
                <td>{{ observation.category }}</td>
                <td>{{ observation.description }}</td>
                <td>{{ observation.status }}</td>
                <td>{{ observation.notes }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <!-- Add New Observation Button -->
        <button class="add-observation-btn" @click="addObservation">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
          Add Observation
        </button>
      </div>

      <!-- Digital Signatures -->
      <div class="signatures-section">
        <h2 class="section-title">Digital Signatures</h2>
        <div class="signatures-grid">
          <div class="signature-item">
            <label>Reviewed By:</label>
            <div class="signature-display">
              <span v-if="reportData.reviewedBy" class="signature-name">{{ reportData.reviewedBy }}</span>
              <span v-else class="no-signature">No signature</span>
            </div>
            <div class="signature-date" v-if="reportData.reviewDate">
              Date: {{ reportData.reviewDate }}
            </div>
          </div>
          
          <div class="signature-item">
            <label>Approved By:</label>
            <div class="signature-display">
              <span v-if="reportData.approvedBy" class="signature-name">{{ reportData.approvedBy }}</span>
              <span v-else class="no-signature">No signature</span>
            </div>
            <div class="signature-date" v-if="reportData.approvalDate">
              Date: {{ reportData.approvalDate }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QAHeadViewObservations',
  data() {
    return {
      lruName: '',
      projectName: '',
      versionId: '',
      currentVersion: '',
      isVersionSpecific: false,
      reportData: {
        projectName: '',
        projectNumber: '',
        projectDate: '',
        version: '',
        revision: '',
        lruName: '',
        observations: [],
        reviewedBy: '',
        approvedBy: '',
        reviewDate: '',
        approvalDate: ''
      },
      // Sample data for non-version-specific view
      serialNumber: 'SL-001',
      observationCount: 'OBS-001',
      currentYear: '2025',
      currentDate: '2025-01-15',
      lruPartNumber: 'LRU-001',
      docReviewDate: '2025-01-15',
      reviewVenue: 'QA Department',
      referenceDocument: 'Technical Specification'
    };
  },
  computed: {
    canSubmit() {
      return this.reportData.observations.length > 0;
    }
  },
  mounted() {
    // Get parameters from route
    this.lruName = this.$route.params.lruName || 'Unknown LRU';
    this.projectName = this.$route.params.projectName || 'Unknown Project';
    this.versionId = this.$route.params.versionId || '';
    
    // Check if this is a version-specific observation view
    if (this.versionId) {
      this.isVersionSpecific = true;
      // Parse version from versionId (e.g., "PRJ-2025-078-A" -> "A")
      const lastDashIndex = this.versionId.lastIndexOf('-');
      if (lastDashIndex !== -1) {
        this.currentVersion = this.versionId.substring(lastDashIndex + 1);
      }
    }
    
    // Load observation data
    this.loadObservationData();
  },
  methods: {
    loadObservationData() {
      // In a real application, this would fetch data from an API
      // For now, we'll use sample data
      if (this.isVersionSpecific) {
        // Load version-specific observation data
        this.loadVersionSpecificData();
      } else {
        // Load general observation data
        this.loadGeneralData();
      }
    },
    
    loadVersionSpecificData() {
      // Sample version-specific observation data
      const versionData = {
        'A': {
          projectName: this.projectName,
          projectNumber: 'PRJ-2025-078',
          projectDate: '2025-01-15',
          version: 'A',
          revision: '1.0',
          lruName: this.lruName,
          observations: [
            {
              observationNumber: 'OBS-001',
              description: 'Initial technical review completed for Version A',
              category: 'Technical Review',
              severity: 'Low',
              status: 'Completed',
              assignedTo: 'John Smith',
              dueDate: '2025-01-20',
              notes: 'All technical requirements met for initial version'
            },
            {
              observationNumber: 'OBS-002',
              description: 'Document formatting needs standardization',
              category: 'Documentation',
              severity: 'Medium',
              status: 'In Progress',
              assignedTo: 'Sarah Johnson',
              dueDate: '2025-01-25',
              notes: 'Working on standardizing document templates'
            }
          ],
          reviewedBy: 'Mike Wilson',
          approvedBy: 'Lisa Brown',
          reviewDate: '2025-01-18',
          approvalDate: '2025-01-20'
        },
        'B': {
          projectName: this.projectName,
          projectNumber: 'PRJ-2025-078',
          projectDate: '2025-01-20',
          version: 'B',
          revision: '2.0',
          lruName: this.lruName,
          observations: [
            {
              observationNumber: 'OBS-003',
              description: 'Technical specifications updated and reviewed',
              category: 'Technical Review',
              severity: 'Medium',
              status: 'Completed',
              assignedTo: 'Engineering Team',
              dueDate: '2025-01-25',
              notes: 'Updated specifications based on feedback'
            },
            {
              observationNumber: 'OBS-004',
              description: 'Quality assurance checklist verification',
              category: 'Quality Assurance',
              severity: 'High',
              status: 'Completed',
              assignedTo: 'QA Team',
              dueDate: '2025-01-28',
              notes: 'All QA requirements verified and documented'
            },
            {
              observationNumber: 'OBS-005',
              description: 'Stakeholder review and approval',
              category: 'Stakeholder Review',
              severity: 'High',
              status: 'In Progress',
              assignedTo: 'Project Manager',
              dueDate: '2025-02-01',
              notes: 'Awaiting final stakeholder approval'
            }
          ],
          reviewedBy: 'Sarah Johnson',
          approvedBy: 'Mike Wilson',
          reviewDate: '2025-01-22',
          approvalDate: '2025-01-25'
        },
        'C': {
          projectName: this.projectName,
          projectNumber: 'PRJ-2025-078',
          projectDate: '2025-01-25',
          version: 'C',
          revision: '3.0',
          lruName: this.lruName,
          observations: [
            {
              observationNumber: 'OBS-006',
              description: 'QA team review completed with corrections',
              category: 'Quality Assurance',
              severity: 'Medium',
              status: 'Completed',
              assignedTo: 'QA Team',
              dueDate: '2025-01-30',
              notes: 'Minor corrections implemented and verified'
            },
            {
              observationNumber: 'OBS-007',
              description: 'Final technical validation',
              category: 'Technical Review',
              severity: 'High',
              status: 'Completed',
              assignedTo: 'Technical Lead',
              dueDate: '2025-02-02',
              notes: 'All technical aspects validated and approved'
            },
            {
              observationNumber: 'OBS-008',
              description: 'Document finalization and formatting',
              category: 'Documentation',
              severity: 'Low',
              status: 'Completed',
              assignedTo: 'Documentation Team',
              dueDate: '2025-02-05',
              notes: 'Final formatting and proofreading completed'
            }
          ],
          reviewedBy: 'Mike Wilson',
          approvedBy: 'Lisa Brown',
          reviewDate: '2025-01-27',
          approvalDate: '2025-01-30'
        },
        'D': {
          projectName: this.projectName,
          projectNumber: 'PRJ-2025-078',
          projectDate: '2025-01-30',
          version: 'D',
          revision: '4.0',
          lruName: this.lruName,
          observations: [
            {
              observationNumber: 'OBS-009',
              description: 'Final review board assessment',
              category: 'Review Board',
              severity: 'High',
              status: 'In Progress',
              assignedTo: 'Review Board',
              dueDate: '2025-02-10',
              notes: 'Final assessment in progress'
            },
            {
              observationNumber: 'OBS-010',
              description: 'Regulatory compliance verification',
              category: 'Compliance',
              severity: 'High',
              status: 'Completed',
              assignedTo: 'Compliance Team',
              dueDate: '2025-02-08',
              notes: 'All regulatory requirements verified'
            },
            {
              observationNumber: 'OBS-011',
              description: 'Final stakeholder sign-off',
              category: 'Stakeholder Review',
              severity: 'Critical',
              status: 'Pending',
              assignedTo: 'Project Director',
              dueDate: '2025-02-15',
              notes: 'Awaiting final stakeholder sign-off'
            }
          ],
          reviewedBy: 'Lisa Brown',
          approvedBy: 'Review Board',
          reviewDate: '2025-02-01',
          approvalDate: 'Pending'
        }
      };
      
      const selectedVersionData = versionData[this.currentVersion] || versionData['A'];
      this.reportData = { ...this.reportData, ...selectedVersionData };
    },
    
    loadGeneralData() {
      // Load general observation data (existing logic)
      this.reportData = {
        projectName: this.projectName,
        projectNumber: 'PRJ-2025-078',
        projectDate: '2025-01-15',
        version: 'General',
        revision: '1.0',
        lruName: this.lruName,
        observations: [
          {
            observationNumber: 'OBS-001',
            description: 'General observation report for LRU document',
            category: 'General Review',
            severity: 'Medium',
            status: 'In Progress',
            assignedTo: 'QA Team',
            dueDate: '2025-01-30',
            notes: 'General observations and recommendations'
          }
        ],
        reviewedBy: '',
        approvedBy: '',
        reviewDate: '',
        approvalDate: ''
      };
    },
    
    addObservation() {
      this.reportData.observations.push({ category: '', description: '', status: '', notes: '' });
    },
    
    saveReport() {
      // Save report logic
      console.log('Saving report:', {
        observations: this.reportData.observations,
        version: this.currentVersion,
        projectName: this.projectName,
        lruName: this.lruName
      });
      alert('Report saved successfully!');
    },
    
    submitReport() {
      // Submit report logic
      console.log('Submitting report:', {
        observations: this.reportData.observations,
        version: this.currentVersion,
        projectName: this.projectName,
        lruName: this.lruName
      });
      alert('Report submitted successfully!');
    },
    
    exportReport() {
      // Export report logic
      console.log('Exporting report:', {
        observations: this.reportData.observations,
        version: this.currentVersion,
        projectName: this.projectName,
        lruName: this.lruName
      });
      alert('Report exported successfully!');
    }
  }
};
</script>

<style scoped>
.view-observations-page {
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
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.document-path {
  font-family: 'Courier New', monospace;
  color: #4a5568;
  font-size: 0.9em;
  background: #f7fafc;
  padding: 10px 15px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.report-date {
  color: #4a5568;
  font-weight: 600;
}

.subject-line {
  font-size: 1.2em;
  font-weight: bold;
  color: #333;
  margin: 20px 0;
  padding: 15px;
  background-color: #f8f9fa;
  border-left: 4px solid #6c757d;
  border-radius: 4px;
}

.version-info {
  font-size: 0.9em;
  color: #6c757d;
  font-weight: normal;
  margin-left: 10px;
}

.version-badge, .revision-badge {
  background-color: #6c757d;
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-weight: bold;
  font-size: 0.9em;
  display: inline-block;
  width: fit-content;
}

.version-badge {
  background-color: #495057;
}

.revision-badge {
  background-color: #6c757d;
}

/* Document Details */
.document-details {
  background: white;
  padding: 25px;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 25px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px solid #e2e8f0;
}

.detail-item:last-child {
  border-bottom: none;
}

.detail-item label {
  font-weight: 600;
  color: #4a5568;
  min-width: 150px;
}

.detail-item span {
  color: #2d3748;
  font-weight: 500;
}

.stage-value {
  color: #4a5568;
  font-weight: 600;
}

/* Observations Section */
.observations-section {
  background: white;
  padding: 25px;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 25px;
}

.section-title {
  color: #2d3748;
  border-bottom: 3px solid #4a5568;
  padding-bottom: 15px;
  margin-bottom: 25px;
  font-size: 1.5em;
  font-weight: 600;
}

.table-container {
  overflow-x: auto;
  margin-bottom: 20px;
}

.observations-table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
}

.observations-table th {
  background: #2d3748;
  color: white;
  padding: 15px;
  text-align: left;
  font-weight: 600;
  font-size: 0.9em;
}

.observations-table td {
  padding: 15px;
  border-bottom: 1px solid #e2e8f0;
  vertical-align: top;
}

.observations-table tr:nth-child(even) {
  background-color: #f8fafc;
}

.observations-table tr:hover {
  background-color: #edf2f7;
}

.category-select,
.status-select {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.9em;
}

.observation-textarea,
.justification-textarea {
  width: 100%;
  min-height: 80px;
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.9em;
  resize: vertical;
  font-family: inherit;
}

.add-observation-btn {
  background: #4a5568;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 12px 20px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 15px rgba(74, 85, 104, 0.3);
}

.add-observation-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(74, 85, 104, 0.4);
}

/* Signatures Section */
.signatures-section {
  background: white;
  padding: 25px;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 25px;
}

.signatures-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}

.signature-item {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.signature-item label {
  font-weight: 600;
  color: #4a5568;
  font-size: 1.1em;
}

.signature-area {
  border: 2px dashed #cbd5e0;
  border-radius: 12px;
  padding: 30px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #f8fafc;
  min-height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.signature-area:hover {
  border-color: #4a5568;
  background: #edf2f7;
}

.signature-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  color: #a0aec0;
}

.signature-display {
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 6px;
  padding: 15px;
  min-height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 10px;
}

.signature-name {
  font-weight: bold;
  color: #333;
  font-size: 1.1em;
}

.no-signature {
  color: #a0aec0;
  font-style: italic;
}

.signature-date {
  font-size: 0.9em;
  color: #6c757d;
  margin-top: 5px;
  text-align: center;
}

/* Action Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
}

.btn-primary {
  background-color: #333;
  color: white;
}

.btn-primary:hover {
  background-color: #555;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background-color: #5a6268;
}

.btn-success {
  background-color: #28a745;
  color: white;
}

.btn-success:hover {
  background-color: #218838;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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
  
  .document-details {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .signatures-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .observations-table {
    font-size: 0.9em;
  }
  
  .observations-table th,
  .observations-table td {
    padding: 10px 8px;
  }
}
</style>
