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
        <div class="logos-container">
          <img src="@/assets/images/aviatrax-logo.png" alt="Aviatrax Logo" class="app-logo">
          <img src="@/assets/images/vista_logo.png" alt="Vista Logo" class="app-logo vista-logo">
        </div>
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
        <span v-if="isReportSpecific" class="report-info">
          (Report {{ reportData.projectNumber }} - {{ reportData.status || 'Status: Pending' }})
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
import jsPDF from 'jspdf';

export default {
  name: 'ObservationReport',
  data() {
    return {
      lruName: '',
      projectName: '',
      versionId: '',
      reportId: '',
      currentVersion: '',
      isVersionSpecific: false,
      isReportSpecific: false,
      reportData: {
        projectName: '',
        projectNumber: '',
        projectDate: '',
        version: '',
        revision: '',
        lruName: '',
        status: '',
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
    this.reportId = this.$route.params.reportId || '';
    
    // Check if this is a version-specific observation view
    if (this.versionId) {
      this.isVersionSpecific = true;
      // Parse version from versionId (e.g., "PRJ-2025-078-A" -> "A")
      const lastDashIndex = this.versionId.lastIndexOf('-');
      if (lastDashIndex !== -1) {
        this.currentVersion = this.versionId.substring(lastDashIndex + 1);
      }
    }
    
    // Check if this is a report-specific view
    if (this.reportId) {
      this.isReportSpecific = true;
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
      } else if (this.isReportSpecific) {
        // Load report-specific observation data
        this.loadReportSpecificData();
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
        status: 'In Progress',
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
    
    loadReportSpecificData() {
      // Load report-specific observation data based on reportId
      const reportData = {
        '1': {
          projectName: this.projectName,
          projectNumber: 'PRJ-2025-078',
          projectDate: '2025-01-15',
          version: 'A',
          revision: '1.0',
          lruName: this.lruName,
          status: 'SUCCESSFULLY COMPLETED',
          observations: [
            {
              observationNumber: 'OBS-001',
              description: 'Report MEMO-2025-018 successfully completed with all QA requirements met',
              category: 'Quality Assurance',
              severity: 'Low',
              status: 'Completed',
              assignedTo: 'QA Team',
              dueDate: '2025-01-20',
              notes: 'All quality standards verified and documented'
            },
            {
              observationNumber: 'OBS-002',
              description: 'Technical specifications reviewed and approved',
              category: 'Technical Review',
              severity: 'Medium',
              status: 'Completed',
              assignedTo: 'Technical Lead',
              dueDate: '2025-01-25',
              notes: 'Technical requirements fully satisfied'
            }
          ],
          reviewedBy: 'Sarah Johnson',
          approvedBy: 'Mike Wilson',
          reviewDate: '2025-01-18',
          approvalDate: '2025-01-20'
        },
        '2': {
          projectName: this.projectName,
          projectNumber: 'PRJ-2025-079',
          projectDate: '2025-01-18',
          version: 'B',
          revision: '2.0',
          lruName: this.lruName,
          status: 'ASSIGNED',
          observations: [
            {
              observationNumber: 'OBS-003',
              description: 'Report MEMO002 assigned and under review',
              category: 'Assignment',
              severity: 'Medium',
              status: 'In Progress',
              assignedTo: 'QA Team',
              dueDate: '2025-01-30',
              notes: 'Currently being reviewed by assigned team members'
            }
          ],
          reviewedBy: 'John Smith',
          approvedBy: 'Pending',
          reviewDate: '2025-01-22',
          approvalDate: 'Pending'
        },
        '3': {
          projectName: this.projectName,
          projectNumber: 'PRJ-2025-080',
          projectDate: '2025-01-20',
          version: 'C',
          revision: '3.0',
          lruName: this.lruName,
          status: 'TEST FAILED',
          observations: [
            {
              observationNumber: 'OBS-004',
              description: 'Report MEMO003 test failed during execution',
              category: 'Test Execution',
              severity: 'High',
              status: 'Failed',
              assignedTo: 'Test Team',
              dueDate: '2025-01-28',
              notes: 'Test failure analysis in progress, root cause investigation required'
            }
          ],
          reviewedBy: 'Test Lead',
          approvedBy: 'Pending',
          reviewDate: '2025-01-25',
          approvalDate: 'Pending'
        }
      };
      
      // Load data for the specific report, or default to first report if not found
      const selectedReportData = reportData[this.reportId] || reportData['1'];
      this.reportData = { ...this.reportData, ...selectedReportData };
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
      try {
        console.log('Starting PDF export...');
        console.log('Report data:', this.reportData);
        console.log('Component data:', {
          lruName: this.lruName,
          projectName: this.projectName,
          serialNumber: this.serialNumber,
          observationCount: this.observationCount,
          currentYear: this.currentYear,
          currentDate: this.currentDate,
          lruPartNumber: this.lruPartNumber,
          docReviewDate: this.docReviewDate,
          reviewVenue: this.reviewVenue
        });

        // Create new PDF document
        const doc = new jsPDF('p', 'mm', 'a4');
        const pageWidth = doc.internal.pageSize.getWidth();
        const pageHeight = doc.internal.pageSize.getHeight();
        const margin = 20;
        const contentWidth = pageWidth - (2 * margin);
        
        let yPosition = margin;
        
        // Set font styles
        doc.setFont('helvetica');
        
        // ===== HEADER SECTION =====
        // Main Title - IQA OBSERVATION REPORT
        doc.setFontSize(18);
        doc.setFont('helvetica', 'bold');
        doc.text('IQA OBSERVATION REPORT', pageWidth / 2, yPosition, { align: 'center' });
        yPosition += 15;
        
        // Document path and date on same line
        doc.setFontSize(10);
        doc.setFont('helvetica', 'normal');
        
        // Left side - Document path
        const documentPath = `CASDIC/${this.projectName || 'PROJECT'}/${this.lruName || 'LRU'}/SL.${this.serialNumber || '001'}/${this.observationCount || '001'}/${this.currentYear || '2025'}`;
        doc.text(documentPath, margin, yPosition);
        
        // Right side - Date
        const dateText = `Date: ${this.currentDate || new Date().toLocaleDateString('en-GB')}`;
        const dateWidth = doc.getTextWidth(dateText);
        doc.text(dateText, pageWidth - margin - dateWidth, yPosition);
        yPosition += 12;
        
        // ===== SUBJECT LINE =====
        doc.setFontSize(12);
        doc.setFont('helvetica', 'bold');
        const subjectText = `SUB: IQA Observation Report for ${this.lruName || this.reportData.lruName || 'Unknown LRU'}`;
        doc.text(subjectText, pageWidth / 2, yPosition, { align: 'center' });
        yPosition += 15;
        
        // ===== DOCUMENT DETAILS SECTION =====
        doc.setFontSize(10);
        
        // Left column details
        const leftColumnX = margin;
        const rightColumnX = margin + contentWidth / 2;
        const labelOffset = 40; // Space after label
        
        // Left column - Project details
        yPosition = margin + 42;
        
        // Project Name
        doc.setFont('helvetica', 'bold');
        doc.text('Project Name :', leftColumnX, yPosition);
        doc.setFont('helvetica', 'normal');
        doc.text(this.reportData.projectName || this.projectName || 'Not specified', leftColumnX + labelOffset, yPosition);
        yPosition += 8;
        
        // Project Number (if available)
        if (this.reportData.projectNumber) {
          doc.setFont('helvetica', 'bold');
          doc.text('Project Number :', leftColumnX, yPosition);
          doc.setFont('helvetica', 'normal');
          doc.text(this.reportData.projectNumber, leftColumnX + labelOffset, yPosition);
          yPosition += 8;
        }
        
        // Project Date (if available)
        if (this.reportData.projectDate) {
          doc.setFont('helvetica', 'bold');
          doc.text('Project Date :', leftColumnX, yPosition);
          doc.setFont('helvetica', 'normal');
          doc.text(this.reportData.projectDate, leftColumnX + labelOffset, yPosition);
          yPosition += 8;
        }
        
        // LRU Name
        doc.setFont('helvetica', 'bold');
        doc.text('LRU Name :', leftColumnX, yPosition);
        doc.setFont('helvetica', 'normal');
        doc.text(this.reportData.lruName || this.lruName || 'Not specified', leftColumnX + labelOffset, yPosition);
        yPosition += 8;
        
        // LRU Part No
        doc.setFont('helvetica', 'bold');
        doc.text('LRU Part No. :', leftColumnX, yPosition);
        doc.setFont('helvetica', 'normal');
        doc.text(this.lruPartNumber || 'Not specified', leftColumnX + labelOffset, yPosition);
        yPosition += 8;
        
        // Serial Number
        doc.setFont('helvetica', 'bold');
        doc.text('Serial Number :', leftColumnX, yPosition);
        doc.setFont('helvetica', 'normal');
        doc.text(this.serialNumber || 'Not specified', leftColumnX + labelOffset, yPosition);
        yPosition += 8;
        
        // Right column details
        yPosition = margin + 42;
        
        // Version
        if (this.reportData.version) {
          doc.setFont('helvetica', 'bold');
          doc.text('Version :', rightColumnX, yPosition);
          doc.setFont('helvetica', 'normal');
          doc.text(this.reportData.version, rightColumnX + labelOffset, yPosition);
          yPosition += 8;
        }
        
        // Revision
        if (this.reportData.revision) {
          doc.setFont('helvetica', 'bold');
          doc.text('Revision :', rightColumnX, yPosition);
          doc.setFont('helvetica', 'normal');
          doc.text(this.reportData.revision, rightColumnX + labelOffset, yPosition);
          yPosition += 8;
        }
        
        // Inspection stage
        doc.setFont('helvetica', 'bold');
        doc.text('Inspection stage :', rightColumnX, yPosition);
        doc.setFont('helvetica', 'normal');
        doc.text('Document review/report', rightColumnX + labelOffset, yPosition);
        yPosition += 8;
        
        // Date of doc review
        doc.setFont('helvetica', 'bold');
        doc.text('Date of doc review :', rightColumnX, yPosition);
        doc.setFont('helvetica', 'normal');
        doc.text(this.docReviewDate || 'Not specified', rightColumnX + labelOffset, yPosition);
        yPosition += 8;
        
        // Review venue
        doc.setFont('helvetica', 'bold');
        doc.text('Review venue :', rightColumnX, yPosition);
        doc.setFont('helvetica', 'normal');
        doc.text(this.reviewVenue || 'Not specified', rightColumnX + labelOffset, yPosition);
        yPosition += 8;
        
        // Reference Document
        doc.setFont('helvetica', 'bold');
        doc.text('Reference Document :', rightColumnX, yPosition);
        doc.setFont('helvetica', 'normal');
        const revision = this.reportData.revision || 'Not specified';
        const version = this.reportData.version || 'Not specified';
        const projectDate = this.reportData.projectDate || 'Not specified';
        const referenceText = `${this.lruName || 'N/A'}, ${this.lruPartNumber || 'N/A'}, Rev ${revision} & Ver ${version}, dated ${projectDate}`;
        doc.text(referenceText, rightColumnX + labelOffset, yPosition);
        yPosition += 15;
        
        // ===== OBSERVATIONS SECTION =====
        doc.setFontSize(12);
        doc.setFont('helvetica', 'bold');
        doc.text('OBSERVATIONS', pageWidth / 2, yPosition, { align: 'center' });
        yPosition += 12;
        
        // ===== OBSERVATIONS TABLE =====
        doc.setFontSize(9);
        doc.setFont('helvetica', 'bold');
        
        // Table column widths and positions (optimized for single page)
        const tableStartX = margin;
        const snoWidth = 15;
        const categoryWidth = 30;
        const observationWidth = 55;
        const acceptRejectWidth = 25;
        const justificationWidth = 40;
        
        // Table headers with proper spacing
        doc.text('SNO', tableStartX, yPosition);
        doc.text('Category', tableStartX + snoWidth, yPosition);
        doc.text('Observations', tableStartX + snoWidth + categoryWidth, yPosition);
        doc.text('Accept/Reject', tableStartX + snoWidth + categoryWidth + observationWidth, yPosition);
        doc.text('Justification', tableStartX + snoWidth + categoryWidth + observationWidth + acceptRejectWidth, yPosition);
        yPosition += 6;
        
        // Draw table header lines
        doc.line(margin, yPosition - 3, pageWidth - margin, yPosition - 3);
        doc.line(margin, yPosition, pageWidth - margin, yPosition);
        yPosition += 4;
        
        // Table data
        doc.setFont('helvetica', 'normal');
        
        // Safety check - ensure observations array exists and has items
        if (!this.reportData.observations || this.reportData.observations.length === 0) {
          doc.text('No observations available', tableStartX + snoWidth + categoryWidth, yPosition);
          yPosition += 15;
        } else {
          // Limit observations to fit on single page
          const maxObservations = Math.min(this.reportData.observations.length, 8);
          const observationsToShow = this.reportData.observations.slice(0, maxObservations);
          
          observationsToShow.forEach((obs, index) => {
            yPosition += 6;
            
            // SNO
            doc.text((index + 1).toString(), tableStartX, yPosition);
            
            // Category (shortened)
            const categoryText = (obs.category || 'N/A').substring(0, 20);
            doc.text(categoryText, tableStartX + snoWidth, yPosition);
            
            // Observations - handle long text with proper wrapping
            const observationText = (obs.description || obs.observation || 'No observation text').substring(0, 80);
            const observationLines = doc.splitTextToSize(observationText, observationWidth - 2);
            doc.text(observationLines, tableStartX + snoWidth + categoryWidth, yPosition);
            
            // Accept/Reject
            const acceptRejectText = (obs.acceptReject || obs.status || 'Pending').substring(0, 20);
            doc.text(acceptRejectText, tableStartX + snoWidth + categoryWidth + observationWidth, yPosition);
            
            // Justification - handle long text with proper wrapping
            const justificationText = (obs.justification || obs.notes || 'No justification provided').substring(0, 60);
            const justificationLines = doc.splitTextToSize(justificationText, justificationWidth - 2);
            doc.text(justificationLines, tableStartX + snoWidth + categoryWidth + observationWidth + acceptRejectWidth, yPosition);
            
            // Calculate row height based on the longest text
            const maxLines = Math.max(observationLines.length, justificationLines.length, 1);
            yPosition += Math.max(maxLines * 3, 8);
          });
          
          // Show message if observations were truncated
          if (this.reportData.observations.length > maxObservations) {
            yPosition += 8;
            doc.setFont('helvetica', 'italic');
            doc.setFontSize(8);
            doc.text(`Note: Showing ${maxObservations} of ${this.reportData.observations.length} observations. Export detailed report for complete list.`, margin, yPosition);
            doc.setFont('helvetica', 'normal');
            doc.setFontSize(9);
          }
        }
        
        yPosition += 15;
        
        // ===== SIGNATURES SECTION =====
        // Optimize for single page - ensure we have enough space
        if (yPosition > pageHeight - 60) {
          yPosition = pageHeight - 60;
        }
        
        doc.setFontSize(12);
        doc.setFont('helvetica', 'bold');
        doc.text('SIGNATURES', pageWidth / 2, yPosition, { align: 'center' });
        yPosition += 15;
        
        // ===== CORRECTED SIGNATURE AREA =====
        // Create a single horizontal signature box divided into three sections
        const totalSignatureWidth = contentWidth - 20; // Leave some margin
        const signatureHeight = 25;
        const leftSectionWidth = totalSignatureWidth * 0.25; // 25% for left
        const centerSectionWidth = totalSignatureWidth * 0.5; // 50% for center
        const rightSectionWidth = totalSignatureWidth * 0.25; // 25% for right
        
        const signatureStartX = margin + 10;
        const signatureY = yPosition;
        
        // Draw the main signature box
        doc.rect(signatureStartX, signatureY, totalSignatureWidth, signatureHeight);
        
        // Draw vertical dividing lines
        doc.line(signatureStartX + leftSectionWidth, signatureY, signatureStartX + leftSectionWidth, signatureY + signatureHeight);
        doc.line(signatureStartX + leftSectionWidth + centerSectionWidth, signatureY, signatureStartX + leftSectionWidth + centerSectionWidth, signatureY + signatureHeight);
        
        // Add labels below the signature box
        yPosition += signatureHeight + 8;
        
        // Left section label
        doc.setFontSize(9);
        doc.setFont('helvetica', 'bold');
        doc.text('Reviewed by', signatureStartX + (leftSectionWidth / 2), yPosition, { align: 'center' });
        
        // Center section label
        doc.text('Approved by', signatureStartX + leftSectionWidth + (centerSectionWidth / 2), yPosition, { align: 'center' });
        
        // Right section label
        doc.text('Not specified', signatureStartX + leftSectionWidth + centerSectionWidth + (rightSectionWidth / 2), yPosition, { align: 'center' });
        
        // Add names inside the signature boxes
        yPosition -= 8;
        doc.setFont('helvetica', 'normal');
        doc.setFontSize(8);
        
        // Reviewed by name
        const reviewedByName = this.reportData.reviewedBy || 'Not specified';
        doc.text(reviewedByName, signatureStartX + (leftSectionWidth / 2), signatureY + (signatureHeight / 2) + 2, { align: 'center' });
        
        // Approved by name
        const approvedByName = this.reportData.approvedBy || 'Not specified';
        doc.text(approvedByName, signatureStartX + leftSectionWidth + (centerSectionWidth / 2), signatureY + (signatureHeight / 2) + 2, { align: 'center' });
        
        // Right section (Not specified)
        doc.text('Not specified', signatureStartX + leftSectionWidth + centerSectionWidth + (rightSectionWidth / 2), signatureY + (signatureHeight / 2) + 2, { align: 'center' });
        
        // ===== SAVE PDF =====
        const lruNameForFile = this.lruName || this.reportData.lruName || 'Unknown_LRU';
        const currentDateForFile = this.currentDate || new Date().toLocaleDateString('en-GB');
        const fileName = `IQA_Observation_Report_${lruNameForFile}_${currentDateForFile.replace(/\//g, '-')}.pdf`;
        doc.save(fileName);
        
        // Show success message
        this.$nextTick(() => {
          alert('Report exported successfully as PDF!');
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

.report-info {
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
