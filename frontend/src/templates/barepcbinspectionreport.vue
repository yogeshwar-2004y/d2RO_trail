<template>
  <div class="bare-pcb-inspection-page">
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
        <h1 class="page-title">BARE PCB INSPECTION REPORT</h1>
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
      <!-- Form Header -->
      <div class="form-header">
        <div class="document-path">
          CASDIC/{{ projectName }}/{{ lruName }}/SL.{{ serialNumber }}/{{ inspectionCount }}/{{ currentYear }}
        </div>
        <div class="report-date">
          Date: {{ currentDate }}
        </div>
      </div>

      <div class="subject-line">
        SUB : Bare PCB Inspection Report for {{ lruName }}
      </div>

      <!-- Inspection Form -->
      <form @submit.prevent="submitForm" class="inspection-form">
        <!-- Document Details Section -->
        <div class="form-section">
          <h2 class="section-title">Document Details</h2>
          <div class="form-grid">
            <div class="form-group">
              <label for="projectName">Project Name:</label>
              <input type="text" id="projectName" v-model="formData.projectName" required>
            </div>
            <div class="form-group">
              <label for="projectNumber">Project Number:</label>
              <input type="text" id="projectNumber" v-model="formData.projectNumber" required>
            </div>
            <div class="form-group">
              <label for="projectDate">Project Date:</label>
              <input type="date" id="projectDate" v-model="formData.projectDate" required>
            </div>
            <div class="form-group">
              <label for="lruName">LRU Name:</label>
              <input type="text" id="lruName" v-model="formData.lruName" required>
            </div>
            <div class="form-group">
              <label for="lruPartNumber">LRU Part No.:</label>
              <input type="text" id="lruPartNumber" v-model="formData.lruPartNumber" required>
            </div>
            <div class="form-group">
              <label for="serialNumber">Serial Number:</label>
              <input type="text" id="serialNumber" v-model="formData.serialNumber" required>
            </div>
            <div class="form-group">
              <label for="version">Version:</label>
              <input type="text" id="version" v-model="formData.version" required>
            </div>
            <div class="form-group">
              <label for="revision">Revision:</label>
              <input type="text" id="revision" v-model="formData.revision" required>
            </div>
            <div class="form-group">
              <label for="inspectionStage">Inspection Stage:</label>
              <select id="inspectionStage" v-model="formData.inspectionStage" required>
                <option value="">Select Stage</option>
                <option value="Visual Inspection">Visual Inspection</option>
                <option value="Dimensional Check">Dimensional Check</option>
                <option value="Electrical Test">Electrical Test</option>
                <option value="Final Inspection">Final Inspection</option>
              </select>
            </div>
            <div class="form-group">
              <label for="inspectionDate">Date of Inspection:</label>
              <input type="date" id="inspectionDate" v-model="formData.inspectionDate" required>
            </div>
            <div class="form-group">
              <label for="inspectionVenue">Inspection Venue:</label>
              <input type="text" id="inspectionVenue" v-model="formData.inspectionVenue" required>
            </div>
            <div class="form-group">
              <label for="referenceDocument">Reference Document:</label>
              <input type="text" id="referenceDocument" v-model="formData.referenceDocument" required>
            </div>
          </div>
        </div>

        <!-- PCB Details Section -->
        <div class="form-section">
          <h2 class="section-title">PCB Details</h2>
          <div class="form-grid">
            <div class="form-group">
              <label for="pcbType">PCB Type:</label>
              <select id="pcbType" v-model="formData.pcbType" required>
                <option value="">Select Type</option>
                <option value="Single Layer">Single Layer</option>
                <option value="Double Layer">Double Layer</option>
                <option value="Multi Layer">Multi Layer</option>
                <option value="Flexible">Flexible</option>
                <option value="Rigid-Flex">Rigid-Flex</option>
              </select>
            </div>
            <div class="form-group">
              <label for="pcbThickness">PCB Thickness (mm):</label>
              <input type="number" id="pcbThickness" v-model="formData.pcbThickness" step="0.1" required>
            </div>
            <div class="form-group">
              <label for="copperWeight">Copper Weight (oz):</label>
              <input type="number" id="copperWeight" v-model="formData.copperWeight" step="0.1" required>
            </div>
            <div class="form-group">
              <label for="surfaceFinish">Surface Finish:</label>
              <select id="surfaceFinish" v-model="formData.surfaceFinish" required>
                <option value="">Select Finish</option>
                <option value="HASL">HASL (Hot Air Solder Leveling)</option>
                <option value="ENIG">ENIG (Electroless Nickel Immersion Gold)</option>
                <option value="OSP">OSP (Organic Solderability Preservative)</option>
                <option value="Immersion Silver">Immersion Silver</option>
                <option value="Immersion Tin">Immersion Tin</option>
              </select>
            </div>
            <div class="form-group">
              <label for="pcbDimensions">PCB Dimensions (L x W in mm):</label>
              <div class="dimensions-input">
                <input type="number" v-model="formData.pcbLength" placeholder="Length" step="0.1" required>
                <span>x</span>
                <input type="number" v-model="formData.pcbWidth" placeholder="Width" step="0.1" required>
              </div>
            </div>
            <div class="form-group">
              <label for="boardColor">Board Color:</label>
              <select id="boardColor" v-model="formData.boardColor" required>
                <option value="">Select Color</option>
                <option value="Green">Green</option>
                <option value="Blue">Blue</option>
                <option value="Red">Red</option>
                <option value="Black">Black</option>
                <option value="White">White</option>
                <option value="Yellow">Yellow</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Inspection Criteria Section -->
        <div class="form-section">
          <h2 class="section-title">Inspection Criteria</h2>
          <div class="criteria-grid">
            <div class="criteria-item">
              <label>
                <input type="checkbox" v-model="formData.criteria.visualInspection">
                Visual Inspection
              </label>
            </div>
            <div class="criteria-item">
              <label>
                <input type="checkbox" v-model="formData.criteria.dimensionalCheck">
                Dimensional Check
              </label>
            </div>
            <div class="criteria-item">
              <label>
                <input type="checkbox" v-model="formData.criteria.electricalTest">
                Electrical Test
              </label>
            </div>
            <div class="criteria-item">
              <label>
                <input type="checkbox" v-model="formData.criteria.solderabilityTest">
                Solderability Test
              </label>
            </div>
            <div class="criteria-item">
              <label>
                <input type="checkbox" v-model="formData.criteria.cleanlinessCheck">
                Cleanliness Check
              </label>
            </div>
            <div class="criteria-item">
              <label>
                <input type="checkbox" v-model="formData.criteria.markingCheck">
                Marking Check
              </label>
            </div>
          </div>
        </div>

        <!-- Inspection Results Section -->
        <div class="form-section">
          <h2 class="section-title">Inspection Results</h2>
          <div class="results-table">
            <table>
              <thead>
                <tr>
                  <th>SNO</th>
                  <th>Inspection Item</th>
                  <th>Specification</th>
                  <th>Actual Value</th>
                  <th>Status</th>
                  <th>Remarks</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in formData.inspectionItems" :key="index">
                  <td>{{ index + 1 }}</td>
                  <td>
                    <input type="text" v-model="item.item" placeholder="Inspection Item">
                  </td>
                  <td>
                    <input type="text" v-model="item.specification" placeholder="Specification">
                  </td>
                  <td>
                    <input type="text" v-model="item.actualValue" placeholder="Actual Value">
                  </td>
                  <td>
                    <select v-model="item.status">
                      <option value="">Select</option>
                      <option value="Pass">Pass</option>
                      <option value="Fail">Fail</option>
                      <option value="N/A">N/A</option>
                    </select>
                  </td>
                  <td>
                    <input type="text" v-model="item.remarks" placeholder="Remarks">
                  </td>
                </tr>
              </tbody>
            </table>
            <button type="button" @click="addInspectionItem" class="add-item-btn">
              + Add Inspection Item
            </button>
          </div>
        </div>

        <!-- Defects Section -->
        <div class="form-section">
          <h2 class="section-title">Defects Found</h2>
          <div class="defects-table">
            <table>
              <thead>
                <tr>
                  <th>SNO</th>
                  <th>Defect Type</th>
                  <th>Description</th>
                  <th>Severity</th>
                  <th>Location</th>
                  <th>Action Taken</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(defect, index) in formData.defects" :key="index">
                  <td>{{ index + 1 }}</td>
                  <td>
                    <select v-model="defect.type">
                      <option value="">Select Type</option>
                      <option value="Visual">Visual</option>
                      <option value="Dimensional">Dimensional</option>
                      <option value="Electrical">Electrical</option>
                      <option value="Solderability">Solderability</option>
                      <option value="Cleanliness">Cleanliness</option>
                    </select>
                  </td>
                  <td>
                    <textarea v-model="defect.description" placeholder="Defect Description" rows="2"></textarea>
                  </td>
                  <td>
                    <select v-model="defect.severity">
                      <option value="">Select</option>
                      <option value="Critical">Critical</option>
                      <option value="Major">Major</option>
                      <option value="Minor">Minor</option>
                    </select>
                  </td>
                  <td>
                    <input type="text" v-model="defect.location" placeholder="Location">
                  </td>
                  <td>
                    <select v-model="defect.action">
                      <option value="">Select Action</option>
                      <option value="Accept">Accept</option>
                      <option value="Reject">Reject</option>
                      <option value="Rework">Rework</option>
                      <option value="Repair">Repair</option>
                    </select>
                  </td>
                </tr>
              </tbody>
            </table>
            <button type="button" @click="addDefect" class="add-item-btn">
              + Add Defect
            </button>
          </div>
        </div>

        <!-- Overall Assessment Section -->
        <div class="form-section">
          <h2 class="section-title">Overall Assessment</h2>
          <div class="assessment-grid">
            <div class="form-group">
              <label for="overallStatus">Overall Status:</label>
              <select id="overallStatus" v-model="formData.overallStatus" required>
                <option value="">Select Status</option>
                <option value="Pass">Pass</option>
                <option value="Fail">Fail</option>
                <option value="Conditional Pass">Conditional Pass</option>
              </select>
            </div>
            <div class="form-group">
              <label for="qualityRating">Quality Rating (1-10):</label>
              <input type="number" id="qualityRating" v-model="formData.qualityRating" min="1" max="10" required>
            </div>
            <div class="form-group full-width">
              <label for="recommendations">Recommendations:</label>
              <textarea id="recommendations" v-model="formData.recommendations" rows="4" placeholder="Enter recommendations or additional notes"></textarea>
            </div>
          </div>
        </div>

        <!-- Signatures Section -->
        <div class="form-section">
          <h2 class="section-title">Signatures</h2>
          <div class="signatures-grid">
            <div class="signature-item">
              <label>Inspected By:</label>
              <div class="signature-area">
                <input type="text" v-model="formData.inspectedBy" placeholder="Inspector Name" required>
                <input type="date" v-model="formData.inspectionSignatureDate" required>
              </div>
            </div>
            <div class="signature-item">
              <label>Reviewed By:</label>
              <div class="signature-area">
                <input type="text" v-model="formData.reviewedBy" placeholder="Reviewer Name" required>
                <input type="date" v-model="formData.reviewSignatureDate" required>
              </div>
            </div>
            <div class="signature-item">
              <label>Approved By:</label>
              <div class="signature-area">
                <input type="text" v-model="formData.approvedBy" placeholder="Approver Name" required>
                <input type="date" v-model="formData.approvalSignatureDate" required>
              </div>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="form-actions">
          <button type="button" @click="saveDraft" class="btn btn-secondary">
            Save Draft
          </button>
          <button type="button" @click="resetForm" class="btn btn-secondary">
            Reset
          </button>
          <button type="submit" class="btn btn-primary" :disabled="!isFormValid">
            Submit Report
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import jsPDF from 'jspdf';

export default {
  name: 'BarePcbInspectionReport',
  data() {
    return {
      projectName: '',
      lruName: '',
      serialNumber: 'SL-001',
      inspectionCount: 'INS-001',
      currentYear: '2025',
      currentDate: new Date().toISOString().split('T')[0],
      formData: {
        projectName: '',
        projectNumber: '',
        projectDate: '',
        lruName: '',
        lruPartNumber: '',
        serialNumber: '',
        version: '',
        revision: '',
        inspectionStage: '',
        inspectionDate: '',
        inspectionVenue: '',
        referenceDocument: '',
        pcbType: '',
        pcbThickness: '',
        copperWeight: '',
        surfaceFinish: '',
        pcbLength: '',
        pcbWidth: '',
        boardColor: '',
        criteria: {
          visualInspection: false,
          dimensionalCheck: false,
          electricalTest: false,
          solderabilityTest: false,
          cleanlinessCheck: false,
          markingCheck: false
        },
        inspectionItems: [
          { item: '', specification: '', actualValue: '', status: '', remarks: '' }
        ],
        defects: [
          { type: '', description: '', severity: '', location: '', action: '' }
        ],
        overallStatus: '',
        qualityRating: '',
        recommendations: '',
        inspectedBy: '',
        inspectionSignatureDate: '',
        reviewedBy: '',
        reviewSignatureDate: '',
        approvedBy: '',
        approvalSignatureDate: ''
      }
    };
  },
  computed: {
    isFormValid() {
      return this.formData.projectName &&
             this.formData.projectNumber &&
             this.formData.lruName &&
             this.formData.inspectionStage &&
             this.formData.overallStatus &&
             this.formData.inspectedBy &&
             this.formData.reviewedBy &&
             this.formData.approvedBy;
    }
  },
  mounted() {
    // Get parameters from route
    this.lruName = this.$route.params.lruName || '';
    this.projectName = this.$route.params.projectName || '';
    
    // Set default values
    this.formData.lruName = this.lruName;
    this.formData.projectName = this.projectName;
    this.formData.inspectionDate = this.currentDate;
  },
  methods: {
    addInspectionItem() {
      this.formData.inspectionItems.push({
        item: '',
        specification: '',
        actualValue: '',
        status: '',
        remarks: ''
      });
    },
    addDefect() {
      this.formData.defects.push({
        type: '',
        description: '',
        severity: '',
        location: '',
        action: ''
      });
    },
    saveDraft() {
      console.log('Saving draft:', this.formData);
      alert('Draft saved successfully!');
    },
    resetForm() {
      if (confirm('Are you sure you want to reset the form? All data will be lost.')) {
        this.formData = {
          projectName: this.projectName,
          lruName: this.lruName,
          projectNumber: '',
          projectDate: '',
          lruPartNumber: '',
          serialNumber: '',
          version: '',
          revision: '',
          inspectionStage: '',
          inspectionDate: this.currentDate,
          inspectionVenue: '',
          referenceDocument: '',
          pcbType: '',
          pcbThickness: '',
          copperWeight: '',
          surfaceFinish: '',
          pcbLength: '',
          pcbWidth: '',
          boardColor: '',
          criteria: {
            visualInspection: false,
            dimensionalCheck: false,
            electricalTest: false,
            solderabilityTest: false,
            cleanlinessCheck: false,
            markingCheck: false
          },
          inspectionItems: [
            { item: '', specification: '', actualValue: '', status: '', remarks: '' }
          ],
          defects: [
            { type: '', description: '', severity: '', location: '', action: '' }
          ],
          overallStatus: '',
          qualityRating: '',
          recommendations: '',
          inspectedBy: '',
          inspectionSignatureDate: '',
          reviewedBy: '',
          reviewSignatureDate: '',
          approvedBy: '',
          approvalSignatureDate: ''
        };
      }
    },
    submitForm() {
      if (this.isFormValid) {
        console.log('Submitting form:', this.formData);
        alert('Report submitted successfully!');
        // Here you would typically send the data to your backend API
      } else {
        alert('Please fill in all required fields.');
      }
    },
    exportReport() {
      try {
        const doc = new jsPDF('p', 'mm', 'a4');
        const pageWidth = doc.internal.pageSize.getWidth();
        const pageHeight = doc.internal.pageSize.getHeight();
        const margin = 20;
        const contentWidth = pageWidth - (2 * margin);
        
        let yPosition = margin;
        
        // Set font styles
        doc.setFont('helvetica');
        
        // Header
        doc.setFontSize(18);
        doc.setFont('helvetica', 'bold');
        doc.text('BARE PCB INSPECTION REPORT', pageWidth / 2, yPosition, { align: 'center' });
        yPosition += 15;
        
        // Document path and date
        doc.setFontSize(10);
        doc.setFont('helvetica', 'normal');
        const documentPath = `CASDIC/${this.projectName || 'PROJECT'}/${this.lruName || 'LRU'}/SL.${this.serialNumber || '001'}/${this.inspectionCount || '001'}/${this.currentYear || '2025'}`;
        doc.text(documentPath, margin, yPosition);
        
        const dateText = `Date: ${this.currentDate || new Date().toLocaleDateString('en-GB')}`;
        const dateWidth = doc.getTextWidth(dateText);
        doc.text(dateText, pageWidth - margin - dateWidth, yPosition);
        yPosition += 12;
        
        // Subject line
        doc.setFontSize(12);
        doc.setFont('helvetica', 'bold');
        const subjectText = `SUB: Bare PCB Inspection Report for ${this.lruName || 'Unknown LRU'}`;
        doc.text(subjectText, pageWidth / 2, yPosition, { align: 'center' });
        yPosition += 15;
        
        // Document details
        doc.setFontSize(10);
        doc.setFont('helvetica', 'bold');
        doc.text('Document Details:', margin, yPosition);
        yPosition += 8;
        
        doc.setFont('helvetica', 'normal');
        const details = [
          `Project Name: ${this.formData.projectName || 'Not specified'}`,
          `Project Number: ${this.formData.projectNumber || 'Not specified'}`,
          `LRU Name: ${this.formData.lruName || 'Not specified'}`,
          `Serial Number: ${this.formData.serialNumber || 'Not specified'}`,
          `Inspection Stage: ${this.formData.inspectionStage || 'Not specified'}`,
          `Inspection Date: ${this.formData.inspectionDate || 'Not specified'}`
        ];
        
        details.forEach(detail => {
          doc.text(detail, margin, yPosition);
          yPosition += 6;
        });
        
        yPosition += 10;
        
        // Inspection results
        doc.setFont('helvetica', 'bold');
        doc.text('Inspection Results:', margin, yPosition);
        yPosition += 8;
        
        if (this.formData.inspectionItems && this.formData.inspectionItems.length > 0) {
          doc.setFontSize(9);
          doc.setFont('helvetica', 'bold');
          
          // Table headers
          doc.text('Item', margin, yPosition);
          doc.text('Specification', margin + 40, yPosition);
          doc.text('Actual', margin + 80, yPosition);
          doc.text('Status', margin + 120, yPosition);
          yPosition += 6;
          
          // Table data
          doc.setFont('helvetica', 'normal');
          this.formData.inspectionItems.forEach(item => {
            if (item.item) {
              doc.text(item.item.substring(0, 15), margin, yPosition);
              doc.text(item.specification.substring(0, 15), margin + 40, yPosition);
              doc.text(item.actualValue.substring(0, 15), margin + 80, yPosition);
              doc.text(item.status, margin + 120, yPosition);
              yPosition += 6;
            }
          });
        }
        
        yPosition += 15;
        
        // Overall assessment
        doc.setFontSize(10);
        doc.setFont('helvetica', 'bold');
        doc.text('Overall Assessment:', margin, yPosition);
        yPosition += 8;
        
        doc.setFont('helvetica', 'normal');
        doc.text(`Overall Status: ${this.formData.overallStatus || 'Not specified'}`, margin, yPosition);
        yPosition += 6;
        doc.text(`Quality Rating: ${this.formData.qualityRating || 'Not specified'}/10`, margin, yPosition);
        yPosition += 6;
        
        if (this.formData.recommendations) {
          doc.text('Recommendations:', margin, yPosition);
          yPosition += 6;
          const recommendations = doc.splitTextToSize(this.formData.recommendations, contentWidth - 10);
          doc.text(recommendations, margin, yPosition);
          yPosition += recommendations.length * 4;
        }
        
        yPosition += 15;
        
        // Signatures
        doc.setFont('helvetica', 'bold');
        doc.text('Signatures:', margin, yPosition);
        yPosition += 8;
        
        doc.setFont('helvetica', 'normal');
        doc.text(`Inspected By: ${this.formData.inspectedBy || 'Not specified'}`, margin, yPosition);
        yPosition += 6;
        doc.text(`Reviewed By: ${this.formData.reviewedBy || 'Not specified'}`, margin, yPosition);
        yPosition += 6;
        doc.text(`Approved By: ${this.formData.approvedBy || 'Not specified'}`, margin, yPosition);
        
        // Save PDF
        const fileName = `Bare_PCB_Inspection_Report_${this.lruName || 'Unknown'}_${this.currentDate.replace(/\//g, '-')}.pdf`;
        doc.save(fileName);
        
        alert('Report exported successfully as PDF!');
        
      } catch (error) {
        console.error('Error exporting PDF:', error);
        alert(`Error exporting PDF: ${error.message || 'Unknown error'}. Please try again.`);
      }
    }
  }
};
</script>

<style scoped>
.bare-pcb-inspection-page {
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

/* Form Header */
.form-header {
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

/* Form Sections */
.inspection-form {
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.form-section {
  padding: 30px;
  border-bottom: 1px solid #e2e8f0;
}

.form-section:last-child {
  border-bottom: none;
}

.section-title {
  color: #2d3748;
  border-bottom: 3px solid #4a5568;
  padding-bottom: 15px;
  margin-bottom: 25px;
  font-size: 1.5em;
  font-weight: 600;
}

/* Form Grid */
.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-weight: 600;
  color: #4a5568;
  font-size: 0.9em;
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 12px 15px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.9em;
  transition: all 0.3s ease;
  background: white;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #4a5568;
  box-shadow: 0 0 0 3px rgba(74, 85, 104, 0.1);
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.dimensions-input {
  display: flex;
  align-items: center;
  gap: 10px;
}

.dimensions-input input {
  flex: 1;
}

.dimensions-input span {
  font-weight: bold;
  color: #4a5568;
}

/* Criteria Grid */
.criteria-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.criteria-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.criteria-item label {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  font-weight: 500;
  color: #4a5568;
}

.criteria-item input[type="checkbox"] {
  width: 18px;
  height: 18px;
  accent-color: #4a5568;
}

/* Tables */
.results-table,
.defects-table {
  margin-top: 20px;
}

.results-table table,
.defects-table table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
}

.results-table th,
.defects-table th {
  background: #2d3748;
  color: white;
  padding: 15px 10px;
  text-align: left;
  font-weight: 600;
  font-size: 0.9em;
}

.results-table td,
.defects-table td {
  padding: 10px;
  border-bottom: 1px solid #e2e8f0;
  vertical-align: top;
}

.results-table tr:nth-child(even),
.defects-table tr:nth-child(even) {
  background-color: #f8fafc;
}

.results-table input,
.results-table select,
.results-table textarea,
.defects-table input,
.defects-table select,
.defects-table textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  font-size: 0.9em;
}

.add-item-btn {
  background: #4a5568;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  margin-top: 15px;
  transition: all 0.3s ease;
}

.add-item-btn:hover {
  background: #2d3748;
  transform: translateY(-1px);
}

/* Assessment Grid */
.assessment-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

/* Signatures */
.signatures-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
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
  padding: 20px;
  background: #f8fafc;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.signature-area input {
  padding: 10px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.9em;
}

/* Form Actions */
.form-actions {
  padding: 30px;
  background: #f8fafc;
  display: flex;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
}

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
  font-size: 0.9em;
}

.btn-primary {
  background-color: #2d3748;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #1a202c;
  transform: translateY(-1px);
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background-color: #5a6268;
  transform: translateY(-1px);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
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
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .criteria-grid {
    grid-template-columns: 1fr;
  }
  
  .signatures-grid {
    grid-template-columns: 1fr;
  }
  
  .assessment-grid {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .results-table,
  .defects-table {
    overflow-x: auto;
  }
  
  .results-table table,
  .defects-table table {
    min-width: 600px;
  }
}
</style>
