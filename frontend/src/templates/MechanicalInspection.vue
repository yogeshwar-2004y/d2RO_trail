<template>
    <div class="mechanical-inspection-page">
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
          <h1 class="page-title">MECHANICAL INSPECTION REPORT</h1>
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
            CASDIC/{{ reportData.projectName }}/{{ reportData.productName }}/SL.{{ reportData.slNo }}/{{ reportData.reportNo }}/{{ currentYear }}
          </div>
          <div class="report-date">
            Date: {{ formattedDate }}
          </div>
        </div>
  
        <div class="subject-line">
          SUB : Mechanical Inspection Report for {{ reportData.productName }}
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
                  <input type="text" id="projectName" v-model="reportData.projectName" required>
                </div>
                <div class="form-group">
                  <label for="reportNo">Report No:</label>
                  <input type="text" id="reportNo" v-model="reportData.reportNo" required>
                </div>
                <div class="form-group">
                  <label for="documentNo">Document No:</label>
                  <input type="text" id="documentNo" v-model="reportData.documentNo" required>
                </div>
                <div class="form-group">
                  <label for="dateOfIssue">Date of Issue:</label>
                  <input type="date" id="dateOfIssue" v-model="reportData.dateOfIssue" required>
                </div>
                <div class="form-group">
                  <label for="issueLevel">Issue Level:</label>
                  <input type="text" id="issueLevel" v-model="reportData.issueLevel" required>
                </div>
                <div class="form-group">
                  <label for="customerName">Customer Name:</label>
                  <input type="text" id="customerName" v-model="reportData.customerName" required>
                </div>
              </div>
              
              <!-- Right Column -->
              <div class="info-column">
                <div class="form-group">
                  <label for="memoId">Memo ID:</label>
                  <input type="text" id="memoId" v-model="reportData.memoId" required>
                </div>
                <div class="form-group">
                  <label for="productName">Product Name:</label>
                  <input type="text" id="productName" v-model="reportData.productName" required>
                </div>
                <div class="form-group">
                  <label for="dpName">DP Name:</label>
                  <input type="text" id="dpName" v-model="reportData.dpName" required>
                </div>
                <div class="form-group">
                  <label for="skuName">SRU Name:</label>
                  <input type="text" id="skuName" v-model="reportData.skuName" required>
                </div>
                <div class="form-group">
                  <label for="partNo">Part No:</label>
                  <input type="text" id="partNo" v-model="reportData.partNo" required>
                </div>
                <div class="form-group">
                  <label for="slNo">Sl. No:</label>
                  <input type="text" id="slNo" v-model="reportData.slNo" required>
                </div>
                <div class="form-group">
                  <label for="qty">Quantity:</label>
                  <input type="text" id="qty" v-model="reportData.qty" required>
                </div>
              </div>
            </div>
          </div>
  
          <!-- Test Timeline Section -->
          <div class="form-section">
            <h2 class="section-title">Test Timeline</h2>
            <div class="general-info-grid">
              <div class="info-column">
                <div class="form-group">
                  <label for="testStartedOn">Test Started On:</label>
                  <input type="datetime-local" id="testStartedOn" v-model="reportData.testStartedOn" required>
                </div>
              </div>
              <div class="info-column">
                <div class="form-group">
                  <label for="testEndedOn">Test Ended On:</label>
                  <input type="datetime-local" id="testEndedOn" v-model="reportData.testEndedOn" required>
                </div>
              </div>
            </div>
          </div>
  
          <!-- Dimensional Checklist Section -->
          <div class="form-section">
            <h2 class="section-title">Dimensional Checklist</h2>
            <div class="inspection-table-container">
              <table class="inspection-table">
                <thead>
                  <tr>
                    <th>SL NO</th>
                    <th>DIMENSION</th>
                    <th>TOLERANCE</th>
                    <th>OBSERVED VALUE</th>
                    <th>INSTRUMENT USED</th>
                    <th>REMARKS</th>
                    <th>UPLOAD</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(item, index) in dimensionalChecklist" :key="'dim-'+index">
                    <td>{{ index + 1 }}</td>
                    <td>
                      <input type="text" v-model="item.dimension" placeholder="Enter dimension">
                    </td>
                    <td>
                      <input type="text" v-model="item.tolerance" placeholder="Enter tolerance">
                    </td>
                    <td>
                      <input type="text" v-model="item.observedValue" placeholder="Enter observed value">
                    </td>
                    <td>
                      <input type="text" v-model="item.instrumentUsed" placeholder="Enter instrument">
                    </td>
                    <td>
                      <input type="text" v-model="item.remarks" placeholder="Enter remarks">
                    </td>
                    <td>
                      <input type="file" @change="handleFileUpload($event, item, 'dim')">
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
  
          <!-- Parameter Checklist Section -->
          <div class="form-section">
            <h2 class="section-title">Parameter Checklist</h2>
            <div class="inspection-table-container">
              <table class="inspection-table">
                <thead>
                  <tr>
                    <th>SL NO</th>
                    <th>PARAMETERS</th>
                    <th>ALLOWED / NOT ALLOWED</th>
                    <th>YES/NO</th>
                    <th>EXPECTED</th>
                    <th>REMARKS / OBSERVATIONS</th>
                    <th>UPLOAD</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(item, index) in parameterChecklist" :key="'param-'+index">
                    <td>{{ index + 1 }}</td>
                    <td>{{ item.parameter }}</td>
                    <td>
                      <input type="text" v-model="item.allowed" placeholder="Enter allowed/not allowed">
                    </td>
                    <td>
                      <select v-model="item.yesNo">
                        <option value="">Select</option>
                        <option value="Yes">Yes</option>
                        <option value="No">No</option>
                      </select>
                    </td>
                    <td>
                      <input type="text" v-model="item.expected" placeholder="Enter expected">
                    </td>
                    <td>
                      <input type="text" v-model="item.remarks" placeholder="Enter remarks">
                    </td>
                    <td>
                      <input type="file" @change="handleFileUpload($event, item, 'param')">
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
    name: 'MechanicalInspection',
    data() {
      return {
        currentYear: '2025',
        reportData: {
          projectName: '',
          reportNo: '',
          documentNo: '',
          dateOfIssue: '',
          issueLevel: '',
          customerName: '',
          memoId: '',
          productName: '',
          dpName: '',
          slNo: '',
          skuName: '',
          partNo: '',
          qty: '',
          testStartedOn: '',
          testEndedOn: '',
        },
        dimensionalChecklist: [
          { dimension: '', tolerance: '', observedValue: '', instrumentUsed: '', remarks: '', fileName: null },
          { dimension: '', tolerance: '', observedValue: '', instrumentUsed: '', remarks: '', fileName: null },
          { dimension: '', tolerance: '', observedValue: '', instrumentUsed: '', remarks: '', fileName: null },
        ],
        parameterChecklist: [
          { parameter: 'Burrs', allowed: '', yesNo: '', expected: '', remarks: '', fileName: null },
          { parameter: 'Damages', allowed: '', yesNo: '', expected: '', remarks: '', fileName: null },
          { parameter: 'Name Plate', allowed: '', yesNo: '', expected: '', remarks: '', fileName: null },
          { parameter: 'Engraving', allowed: '', yesNo: '', expected: '', remarks: '', fileName: null },
          { parameter: 'Passivation', allowed: '', yesNo: '', expected: '', remarks: '', fileName: null },
          { parameter: 'Chromate', allowed: '', yesNo: '', expected: '', remarks: '', fileName: null },
          { parameter: 'Electro-less Nickel plating', allowed: '', yesNo: '', expected: '', remarks: '', fileName: null },
          { parameter: 'Fasteners', allowed: '', yesNo: '', expected: '', remarks: '', fileName: null },
        ],
        currentDate: new Date(),
      };
    },
    computed: {
      formattedDate() {
        return this.currentDate.toISOString().split('T')[0];
      },
      isFormValid() {
        return this.reportData.projectName &&
               this.reportData.reportNo &&
               this.reportData.documentNo &&
               this.reportData.productName &&
               this.reportData.dpName &&
               this.reportData.skuName &&
               this.reportData.partNo;
      }
    },
    mounted() {
      // Get parameters from route
      const projectName = this.$route.params.projectName || '';
      const lruName = this.$route.params.lruName || '';
      
      // Set default values
      this.reportData.projectName = projectName;
      this.reportData.productName = lruName;
      this.reportData.dateOfIssue = this.formattedDate;
    },
    methods: {
      handleFileUpload(event, item, checklistType) {
        const file = event.target.files[0];
        if (file) {
          item.fileName = file.name;
          console.log(`Uploaded file for ${checklistType} item: ${file.name}`);
        } else {
          item.fileName = null;
        }
      },
      saveDraft() {
        console.log('Saving draft:', this.reportData);
        alert('Draft saved successfully!');
      },
      resetForm() {
        if (confirm('Are you sure you want to reset the form? All data will be lost.')) {
          this.reportData = {
            projectName: this.$route.params.projectName || '',
            reportNo: '',
            documentNo: '',
            dateOfIssue: this.formattedDate,
            issueLevel: '',
            customerName: '',
            memoId: '',
            productName: this.$route.params.lruName || '',
            dpName: '',
            slNo: '',
            skuName: '',
            partNo: '',
            qty: '',
            testStartedOn: '',
            testEndedOn: '',
          };
          // Reset checklists
          this.dimensionalChecklist.forEach(item => {
            item.dimension = '';
            item.tolerance = '';
            item.observedValue = '';
            item.instrumentUsed = '';
            item.remarks = '';
            item.fileName = null;
          });
          this.parameterChecklist.forEach(item => {
            item.allowed = '';
            item.yesNo = '';
            item.expected = '';
            item.remarks = '';
            item.fileName = null;
          });
        }
      },
      submitForm() {
        if (this.isFormValid) {
          console.log('Submitting form:', this.reportData);
          alert('Report submitted successfully!');
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
          
          let yPosition = margin;
          
          // Set font styles
          doc.setFont('helvetica');
          
          // Header
          doc.setFontSize(18);
          doc.setFont('helvetica', 'bold');
          doc.text('MECHANICAL INSPECTION REPORT', pageWidth / 2, yPosition, { align: 'center' });
          yPosition += 15;
          
          // Document path and date
          doc.setFontSize(10);
          doc.setFont('helvetica', 'normal');
          const documentPath = `CASDIC/${this.reportData.projectName || 'PROJECT'}/${this.reportData.productName || 'PRODUCT'}/SL.${this.reportData.slNo || '001'}/${this.reportData.reportNo || '001'}/${this.currentYear}`;
          doc.text(documentPath, margin, yPosition);
          
          const dateText = `Date: ${this.formattedDate}`;
          const dateWidth = doc.getTextWidth(dateText);
          doc.text(dateText, pageWidth - margin - dateWidth, yPosition);
          yPosition += 12;
          
          // Subject line
          doc.setFontSize(12);
          doc.setFont('helvetica', 'bold');
          const subjectText = `SUB: Mechanical Inspection Report for ${this.reportData.productName || 'Unknown Product'}`;
          doc.text(subjectText, pageWidth / 2, yPosition, { align: 'center' });
          yPosition += 15;
          
          // Save PDF
          const fileName = `Mechanical_Inspection_Report_${this.reportData.productName || 'Unknown'}_${this.formattedDate.replace(/\//g, '-')}.pdf`;
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
  .mechanical-inspection-page {
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