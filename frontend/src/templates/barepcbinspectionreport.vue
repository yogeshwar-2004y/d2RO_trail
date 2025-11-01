<template>
  <div class="bare-pcb-inspection-page">
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
        <!-- General Information Section -->
        <div class="form-section">
          <h2 class="section-title">General Information</h2>
          <div class="general-info-grid">
            <!-- Left Column -->
            <div class="info-column">
              <div class="form-group">
                <label for="projectName">Project Name:</label>
                <input type="text" id="projectName" v-model="formData.projectName" :disabled="readonly" required>
              </div>
              <div class="form-group">
                <label for="reportRefNo">Report Ref No:</label>
                <input type="text" id="reportRefNo" v-model="formData.reportRefNo" :disabled="readonly" required>
              </div>
              <div class="form-group">
                <label for="memoRefNo">Memo Ref No:</label>
                <input type="text" id="memoRefNo" v-model="formData.memoRefNo" :disabled="readonly" required>
              </div>
              <div class="form-group">
                <label for="lruName">LRU Name:</label>
                <input type="text" id="lruName" v-model="formData.lruName" :disabled="readonly" required>
              </div>
              <div class="form-group">
                <label for="inspectionStage">Inspection Stage:</label>
                <input type="text" id="inspectionStage" v-model="formData.inspectionStage" :disabled="readonly" required>
              </div>
              <div class="form-group">
                <label for="testVenue">Test Venue:</label>
                <input type="text" id="testVenue" v-model="formData.testVenue" :disabled="readonly" required>
              </div>
              <div class="form-group">
                <label for="slNos">SL.NO's:</label>
                <input type="text" id="slNos" v-model="formData.slNos" :disabled="readonly" required>
              </div>
            </div>
            
            <!-- Right Column -->
            <div class="info-column">
              <div class="form-group">
                <label for="dpName">DP Name:</label>
                <input type="text" id="dpName" v-model="formData.dpName" :disabled="readonly" required>
              </div>
              <div class="form-group">
                <label for="dated1">Dated:</label>
                <input type="date" id="dated1" v-model="formData.dated1" :disabled="readonly" required>
              </div>
              <div class="form-group">
                <label for="dated2">Dated:</label>
                <input type="date" id="dated2" v-model="formData.dated2" :disabled="readonly" required>
              </div>
              <div class="form-group">
                <label for="sruName">SRU Name:</label>
                <input type="text" id="sruName" v-model="formData.sruName" :disabled="readonly" required>
              </div>
              <div class="form-group">
                <label for="partNo">Part No:</label>
                <input type="text" id="partNo" v-model="formData.partNo" :disabled="readonly" required>
              </div>
              <div class="form-group">
                <label for="quantity">Quantity:</label>
                <input type="number" id="quantity" v-model="formData.quantity" :disabled="readonly" required>
              </div>
              <div class="form-group">
                <label for="startDate">Start Date:</label>
                <input type="date" id="startDate" v-model="formData.startDate" :disabled="readonly" required>
              </div>
              <div class="form-group">
                <label for="endDate">End Date:</label>
                <input type="date" id="endDate" v-model="formData.endDate" :disabled="readonly" required>
              </div>
            </div>
          </div>
        </div>

        <!-- Inspection Checklist Section -->
        <div class="form-section">
          <h2 class="section-title">Inspection Checklist</h2>
          <div class="inspection-table-container">
            <table class="inspection-table">
              <thead>
                <tr>
                  <th>SL NO</th>
                  <th>PARAMETERS TO BE CHECKED</th>
                  <th>OBSERVATION</th>
                  <th>REMARKS (OK/NOT OK)</th>
                  <th>UPLOAD</th>
                </tr>
              </thead>
              <tbody>
                <!-- I. VISUAL INSPECTION -->
                <tr class="section-header">
                  <td colspan="5"><strong>I. VISUAL INSPECTION</strong></td>
                </tr>
                <tr v-for="(item, index) in formData.visualInspection" :key="'visual-' + index">
                  <td>{{ index + 1 }}</td>
                  <td>{{ item.parameter }}</td>
                  <td>
                    <input type="text" v-model="item.observation" :disabled="readonly" placeholder="Enter observation">
                  </td>
                  <td>
                    <select v-model="item.remarks" :disabled="readonly">
                      <option value="">Select</option>
                      <option value="OK">OK</option>
                      <option value="NOT OK">NOT OK</option>
                    </select>
                  </td>
                  <td>
                    <input type="file" @change="handleFileUpload($event, 'visual', index)" :disabled="readonly">
                  </td>
                </tr>
                
                <!-- II. CONTINUITY CHECKING -->
                <tr class="section-header">
                  <td colspan="5"><strong>II. CONTINUITY CHECKING</strong></td>
                </tr>
                <tr v-for="(item, index) in formData.continuityCheck" :key="'continuity-' + index">
                  <td>{{ index + 1 }}</td>
                  <td>{{ item.parameter }}</td>
                  <td>
                    <input type="text" v-model="item.observation" :disabled="readonly" placeholder="Enter observation">
                  </td>
                  <td>
                    <select v-model="item.remarks" :disabled="readonly">
                      <option value="">Select</option>
                      <option value="OK">OK</option>
                      <option value="NOT OK">NOT OK</option>
                    </select>
                  </td>
                  <td>
                    <input type="file" @change="handleFileUpload($event, 'continuity', index)" :disabled="readonly">
                  </td>
                </tr>
                
                <!-- III. FABRICATOR & VENDOR QC REPORTS VERIFICATION -->
                <tr class="section-header">
                  <td colspan="5"><strong>III. FABRICATOR & VENDOR QC REPORTS VERIFICATION</strong></td>
                </tr>
                <tr>
                  <td>1</td>
                  <td class="description-cell">
                    (Fabricator Report shall be as per Mil 551101 (Mil QML 31032) Group A & B Certificates for Rigid boards and Mil 50884 for Flexi boards (or) IPC 6012 Class 3 DS)
                  </td>
                  <td>
                    <input type="text" v-model="formData.fabricatorReport.observation" :disabled="readonly" placeholder="Enter observation">
                  </td>
                  <td>
                    <select v-model="formData.fabricatorReport.remarks" :disabled="readonly">
                      <option value="">Select</option>
                      <option value="OK">OK</option>
                      <option value="NOT OK">NOT OK</option>
                    </select>
                  </td>
                  <td>
                    <input type="file" @change="handleFileUpload($event, 'fabricator', 0)" :disabled="readonly">
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Signatures Section -->
        <div class="form-section">
          <h2 class="section-title">Signatures</h2>
          <div class="signatures-layout">
            <div class="signature-item">
              <label>Prepared By:</label>
              <div class="signature-line"></div>
            </div>
            <div class="signature-item">
              <label>Verified By:</label>
              <div class="signature-line"></div>
            </div>
            <div class="signature-item">
              <label>Approved By:</label>
              <div class="signature-line"></div>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="form-actions" v-if="!readonly">
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
  props: {
    readonly: {
      type: Boolean,
      default: false
    },
    isTemplatePreview: {
      type: Boolean,
      default: false
    }
  },
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
        reportRefNo: '',
        memoRefNo: '',
        lruName: '',
        inspectionStage: '',
        testVenue: '',
        dpName: '',
        dated1: '',
        dated2: '',
        sruName: '',
        partNo: '',
        quantity: '',
        slNos: '',
        startDate: '',
        endDate: '',
        visualInspection: [
          { parameter: 'CHECK FOR BONDING PROBLEM (DELAMINATION)', observation: '', remarks: '' },
          { parameter: 'CHECK FOR SOLDER MASK OPENINGS', observation: '', remarks: '' },
          { parameter: 'CHECK FOR BUBBLES ON PCB', observation: '', remarks: '' },
          { parameter: 'CHECK FOR ANY DAMAGE TO THE PCB', observation: '', remarks: '' },
          { parameter: 'ALL THROUGH HOLES SHOULD BE CLEAR', observation: '', remarks: '' },
          { parameter: 'ALL VIAS TO BE MASKED', observation: '', remarks: '' },
          { parameter: 'CHECK FOR SILK SCREEN (LEGEND) PRINTING', observation: '', remarks: '' },
          { parameter: 'CHECK FOR PIN NO MARKING ON ICS, CONNECTORS & POLARITY OF DIODES, CAPACITORS etc.', observation: '', remarks: '' },
          { parameter: 'CHECK FOR TRACKS NEAR MOUNTING HOLES', observation: '', remarks: '' },
          { parameter: 'CHECK FOR PCB WARPAGE', observation: '', remarks: '' }
        ],
        continuityCheck: [
          { parameter: 'CHECK FOR VCC TO GROUND CONTINUITY', observation: '', remarks: '' }
        ],
        fabricatorReport: {
          observation: '',
          remarks: ''
        }
      }
    };
  },
  computed: {
    isFormValid() {
      return this.formData.projectName &&
             this.formData.reportRefNo &&
             this.formData.memoRefNo &&
             this.formData.lruName &&
             this.formData.dpName &&
             this.formData.sruName &&
             this.formData.partNo;
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
    handleFileUpload(event, section, index) {
      const file = event.target.files[0];
      if (file) {
        console.log(`File uploaded for ${section} section, item ${index}:`, file.name);
        // Here you would typically upload the file to your backend
        // For now, we'll just log it
      }
    },
    async saveDraft() {
      try {
        // Prepare the data for draft submission
        const draftData = {
          // Header information
          project_name: this.formData.projectName,
          report_ref_no: this.formData.reportRefNo,
          memo_ref_no: this.formData.memoRefNo,
          lru_name: this.formData.lruName,
          sru_name: this.formData.sruName,
          dp_name: this.formData.dpName,
          part_no: this.formData.partNo,
          inspection_stage: this.formData.inspectionStage,
          test_venue: this.formData.testVenue,
          quantity: this.formData.quantity,
          sl_nos: this.formData.slNos,
          serial_number: this.serialNumber,
          inspection_count: this.inspectionCount,
          start_date: this.formData.startDate,
          end_date: this.formData.endDate,
          dated1: this.formData.dated1,
          dated2: this.formData.dated2,
          
          // Visual inspection data (10 items)
          visual_inspection: this.formData.visualInspection,
          
          // Continuity check data (1 item)
          continuity_check: this.formData.continuityCheck,
          
          // Fabricator report data
          fabricator_report: this.formData.fabricatorReport,
          
          // Draft status
          overall_status: 'DRAFT',
          quality_rating: null,
          recommendations: '',
          prepared_by: '',
          verified_by: '',
          approved_by: ''
        };

        console.log('Saving draft data:', draftData);

        // Send data to backend API
        const response = await fetch('/api/reports/bare-pcb-inspection', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(draftData)
        });

        const result = await response.json();

        if (result.success) {
          alert(`Draft saved successfully! Report ID: ${result.report_id}`);
        } else {
          alert(`Error saving draft: ${result.message}`);
        }
      } catch (error) {
        console.error('Error saving draft:', error);
        alert('Error saving draft. Please try again.');
      }
    },
    resetForm() {
      if (confirm('Are you sure you want to reset the form? All data will be lost.')) {
        this.formData = {
          projectName: this.projectName,
          lruName: this.lruName,
          reportRefNo: '',
          memoRefNo: '',
          inspectionStage: '',
          testVenue: '',
          dpName: '',
          dated1: '',
          dated2: '',
          sruName: this.lruName,
          partNo: '',
          quantity: '',
          slNos: '',
          startDate: this.currentDate,
          endDate: '',
          visualInspection: [
            { parameter: 'CHECK FOR BONDING PROBLEM (DELAMINATION)', observation: '', remarks: '' },
            { parameter: 'CHECK FOR SOLDER MASK OPENINGS', observation: '', remarks: '' },
            { parameter: 'CHECK FOR BUBBLES ON PCB', observation: '', remarks: '' },
            { parameter: 'CHECK FOR ANY DAMAGE TO THE PCB', observation: '', remarks: '' },
            { parameter: 'ALL THROUGH HOLES SHOULD BE CLEAR', observation: '', remarks: '' },
            { parameter: 'ALL VIAS TO BE MASKED', observation: '', remarks: '' },
            { parameter: 'CHECK FOR SILK SCREEN (LEGEND) PRINTING', observation: '', remarks: '' },
            { parameter: 'CHECK FOR PIN NO MARKING ON ICS, CONNECTORS & POLARITY OF DIODES, CAPACITORS etc.', observation: '', remarks: '' },
            { parameter: 'CHECK FOR TRACKS NEAR MOUNTING HOLES', observation: '', remarks: '' },
            { parameter: 'CHECK FOR PCB WARPAGE', observation: '', remarks: '' }
          ],
          continuityCheck: [
            { parameter: 'CHECK FOR VCC TO GROUND CONTINUITY', observation: '', remarks: '' }
          ],
          fabricatorReport: {
            observation: '',
            remarks: ''
          }
        };
      }
    },
    async submitForm() {
      if (this.isFormValid) {
        try {
          // Prepare the data for submission
          const submissionData = {
            // Header information
            project_name: this.formData.projectName,
            report_ref_no: this.formData.reportRefNo,
            memo_ref_no: this.formData.memoRefNo,
            lru_name: this.formData.lruName,
            sru_name: this.formData.sruName,
            dp_name: this.formData.dpName,
            part_no: this.formData.partNo,
            inspection_stage: this.formData.inspectionStage,
            test_venue: this.formData.testVenue,
            quantity: this.formData.quantity,
            sl_nos: this.formData.slNos,
            serial_number: this.serialNumber,
            inspection_count: this.inspectionCount,
            start_date: this.formData.startDate,
            end_date: this.formData.endDate,
            dated1: this.formData.dated1,
            dated2: this.formData.dated2,
            
            // Visual inspection data (10 items)
            visual_inspection: this.formData.visualInspection,
            
            // Continuity check data (1 item)
            continuity_check: this.formData.continuityCheck,
            
            // Fabricator report data
            fabricator_report: this.formData.fabricatorReport,
            
            // Additional fields that might be needed
            overall_status: 'COMPLETED',
            quality_rating: null,
            recommendations: '',
            prepared_by: '',
            verified_by: '',
            approved_by: ''
          };

          console.log('Submitting form data:', submissionData);

          // Send data to backend API
          const response = await fetch('http://localhost:5000/api/reports/bare-pcb-inspection', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(submissionData)
          });

          const result = await response.json();

          if (result.success) {
            alert(`Report submitted successfully! Report ID: ${result.report_id}`);
            // Optionally redirect or reset form
            this.resetForm();
          } else {
            alert(`Error submitting report: ${result.message}`);
          }
        } catch (error) {
          console.error('Error submitting form:', error);
          alert('Error submitting report. Please try again.');
        }
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

/* General Info Grid */
.general-info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}

.info-column {
  display: flex;
  flex-direction: column;
  gap: 15px;
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

/* Inspection Table */
.inspection-table-container {
  margin-top: 20px;
  overflow-x: auto;
}

.inspection-table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
  font-size: 0.9em;
}

.inspection-table th {
  background: #2d3748;
  color: white;
  padding: 12px 8px;
  text-align: left;
  font-weight: 600;
  font-size: 0.85em;
}

.inspection-table td {
  padding: 8px;
  border-bottom: 1px solid #e2e8f0;
  vertical-align: top;
}

.inspection-table tr:nth-child(even) {
  background-color: #f8fafc;
}

.section-header {
  background-color: #f0f4f8 !important;
  font-weight: bold;
  color: #2d3748;
}

.section-header td {
  padding: 12px 8px;
  border-bottom: 2px solid #2d3748;
}

.description-cell {
  font-size: 0.8em;
  line-height: 1.4;
  max-width: 300px;
}

.inspection-table input[type="text"],
.inspection-table select {
  width: 100%;
  padding: 6px;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  font-size: 0.85em;
}

.inspection-table input[type="file"] {
  font-size: 0.8em;
  padding: 4px;
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
.signatures-layout {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-top: 30px;
  padding: 20px 0;
}

.signature-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  flex: 1;
  max-width: 200px;
}

.signature-item label {
  font-weight: 600;
  color: #4a5568;
  font-size: 1em;
  margin-bottom: 5px;
}

.signature-line {
  width: 100%;
  height: 40px;
  border-bottom: 1px solid #333;
  margin-top: 10px;
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

/* Readonly styles */
input[readonly], select:disabled, input:disabled {
  background-color: #f8f9fa;
  color: #6c757d;
  cursor: not-allowed;
  opacity: 0.8;
}

input[readonly]:focus, select:disabled:focus {
  outline: none;
  box-shadow: none;
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
  
  .general-info-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .signatures-layout {
    flex-direction: column;
    align-items: center;
    gap: 20px;
  }
  
  .signature-item {
    max-width: 100%;
  }
  
  .form-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .inspection-table-container {
    overflow-x: auto;
  }
  
  .inspection-table {
    min-width: 800px;
  }
}
</style>

