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
      </div>

      <!-- Document Details Grid -->
      <div class="document-details">
        <div class="details-left">
          <div class="detail-item">
            <label>Project Name :</label>
            <span>{{ projectName }}</span>
          </div>
          <div class="detail-item">
            <label>LRU Name :</label>
            <span>{{ lruName }}</span>
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
              <tr v-for="(observation, index) in observations" :key="index">
                <td>{{ index + 1 }}</td>
                <td>
                  <select v-model="observation.category" class="category-select">
                    <option value="">Select</option>
                    <option value="Major">Major</option>
                    <option value="Minor">Minor</option>
                  </select>
                </td>
                <td>
                  <textarea 
                    v-model="observation.description" 
                    placeholder="Enter observation details..."
                    class="observation-textarea"
                  ></textarea>
                </td>
                <td>
                  <select v-model="observation.status" class="status-select">
                    <option value="">Select</option>
                    <option value="Accept">Accept</option>
                    <option value="Reject">Reject</option>
                  </select>
                </td>
                <td>
                  <textarea 
                    v-model="observation.justification" 
                    placeholder="Enter justification..."
                    class="justification-textarea"
                  ></textarea>
                </td>
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

      <!-- Signatures Section -->
      <div class="signatures-section">
        <h2 class="section-title">Review & Approval</h2>
        <div class="signatures-grid">
          <div class="signature-item">
            <label>Reviewed by:</label>
            <div class="signature-area" @click="openSignatureModal('reviewer')">
              <div v-if="reviewerSignature" class="signature-display">
                <img :src="reviewerSignature" alt="Reviewer Signature" class="signature-image">
                <span class="signature-name">{{ reviewerName }}</span>
              </div>
              <div v-else class="signature-placeholder">
                <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                  <circle cx="12" cy="7" r="4"></circle>
                </svg>
                <span>Click to sign</span>
              </div>
            </div>
          </div>
          
          <div class="signature-item">
            <label>Approved by:</label>
            <div class="signature-area" @click="openSignatureModal('approver')">
              <div v-if="approverSignature" class="signature-display">
                <img :src="approverSignature" alt="Approver Signature" class="signature-image">
                <span class="signature-name">{{ approverName }}</span>
              </div>
              <div v-else class="signature-placeholder">
                <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                  <circle cx="12" cy="7" r="4"></circle>
                </svg>
                <span>Click to sign</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="action-buttons">
        <button class="btn btn-secondary" @click="$router.go(-1)">Cancel</button>
        <button class="btn btn-primary" @click="saveReport">Save Report</button>
        <button class="btn btn-success" @click="submitReport" :disabled="!canSubmit">Submit Report</button>
      </div>
    </div>

    <!-- Digital Signature Modal -->
    <div v-if="showSignatureModal" class="signature-modal-overlay" @click="closeSignatureModal">
      <div class="signature-modal" @click.stop>
        <div class="modal-header">
          <h3>{{ signatureType === 'reviewer' ? 'Reviewer' : 'Approver' }} Digital Signature</h3>
          <button class="close-button" @click="closeSignatureModal">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        
        <div class="modal-content">
          <div class="signature-form">
            <div class="form-group">
              <label>Name:</label>
              <input 
                type="text" 
                v-model="signatureData.name" 
                :placeholder="`Enter ${signatureType === 'reviewer' ? 'reviewer' : 'approver'} name`"
                class="form-input"
              >
            </div>
            
            <div class="form-group">
              <label>Signature:</label>
              <div class="signature-canvas-container">
                <canvas 
                  ref="signatureCanvas" 
                  class="signature-canvas"
                  @mousedown="startDrawing"
                  @mousemove="draw"
                  @mouseup="stopDrawing"
                  @touchstart="startDrawingTouch"
                  @touchmove="drawTouch"
                  @touchend="stopDrawing"
                ></canvas>
                <div class="canvas-controls">
                  <button type="button" @click="clearSignature" class="clear-btn">Clear</button>
                </div>
              </div>
            </div>
          </div>
          
          <div class="modal-actions">
            <button @click="closeSignatureModal" class="btn btn-secondary">Cancel</button>
            <button @click="saveSignature" class="btn btn-primary" :disabled="!signatureData.name || !hasSignature">Save Signature</button>
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
      currentDate: '',
      currentYear: '',
      serialNumber: '001',
      observationCount: '5',
      lruPartNumber: 'LRU-PART-001',
      docReviewDate: '2025-01-20',
      reviewVenue: 'QA Department',
      referenceDocument: 'REF-DOC-001, Rev 1.0, Dated 2025-01-15',
      observations: [
        { category: '', description: '', status: '', justification: '' },
        { category: '', description: '', status: '', justification: '' },
        { category: '', description: '', status: '', justification: '' },
        { category: '', description: '', status: '', justification: '' },
        { category: '', description: '', status: '', justification: '' }
      ],
      showSignatureModal: false,
      signatureType: '',
      signatureData: {
        name: ''
      },
      reviewerSignature: null,
      reviewerName: '',
      approverSignature: null,
      approverName: '',
      isDrawing: false,
      hasSignature: false
    };
  },
  computed: {
    canSubmit() {
      return this.reviewerSignature && this.approverSignature && 
             this.observations.some(obs => obs.category && obs.description && obs.status);
    }
  },
  mounted() {
    this.initializePage();
    this.setupCanvas();
  },
  methods: {
    initializePage() {
      this.lruName = this.$route.params.lruName || 'Unknown LRU';
      this.projectName = this.$route.params.projectName || 'Unknown Project';
      this.currentDate = new Date().toISOString().split('T')[0];
      this.currentYear = new Date().getFullYear();
    },
    
    setupCanvas() {
      this.$nextTick(() => {
        const canvas = this.$refs.signatureCanvas;
        if (canvas) {
          const ctx = canvas.getContext('2d');
          ctx.strokeStyle = '#2d3748';
          ctx.lineWidth = 2;
          ctx.lineCap = 'round';
        }
      });
    },
    
    addObservation() {
      this.observations.push({ category: '', description: '', status: '', justification: '' });
    },
    
    openSignatureModal(type) {
      this.signatureType = type;
      this.signatureData.name = type === 'reviewer' ? this.reviewerName : this.approverName;
      this.showSignatureModal = true;
      this.$nextTick(() => {
        this.setupCanvas();
      });
    },
    
    closeSignatureModal() {
      this.showSignatureModal = false;
      this.signatureData.name = '';
      this.hasSignature = false;
    },
    
    startDrawing(event) {
      this.isDrawing = true;
      const canvas = this.$refs.signatureCanvas;
      const rect = canvas.getBoundingClientRect();
      const ctx = canvas.getContext('2d');
      ctx.beginPath();
      ctx.moveTo(event.clientX - rect.left, event.clientY - rect.top);
    },
    
    startDrawingTouch(event) {
      event.preventDefault();
      this.isDrawing = true;
      const canvas = this.$refs.signatureCanvas;
      const rect = canvas.getBoundingClientRect();
      const ctx = canvas.getContext('2d');
      const touch = event.touches[0];
      ctx.beginPath();
      ctx.moveTo(touch.clientX - rect.left, touch.clientY - rect.top);
    },
    
    draw(event) {
      if (!this.isDrawing) return;
      const canvas = this.$refs.signatureCanvas;
      const rect = canvas.getBoundingClientRect();
      const ctx = canvas.getContext('2d');
      ctx.lineTo(event.clientX - rect.left, event.clientY - rect.top);
      ctx.stroke();
      this.hasSignature = true;
    },
    
    drawTouch(event) {
      if (!this.isDrawing) return;
      event.preventDefault();
      const canvas = this.$refs.signatureCanvas;
      const rect = canvas.getBoundingClientRect();
      const ctx = canvas.getContext('2d');
      const touch = event.touches[0];
      ctx.lineTo(touch.clientX - rect.left, touch.clientY - rect.top);
      ctx.stroke();
      this.hasSignature = true;
    },
    
    stopDrawing() {
      this.isDrawing = false;
    },
    
    clearSignature() {
      const canvas = this.$refs.signatureCanvas;
      const ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      this.hasSignature = false;
    },
    
    saveSignature() {
      const canvas = this.$refs.signatureCanvas;
      const signatureDataUrl = canvas.toDataURL();
      
      if (this.signatureType === 'reviewer') {
        this.reviewerSignature = signatureDataUrl;
        this.reviewerName = this.signatureData.name;
      } else {
        this.approverSignature = signatureDataUrl;
        this.approverName = this.signatureData.name;
      }
      
      this.closeSignatureModal();
    },
    
    saveReport() {
      // Save report logic
      console.log('Saving report:', {
        observations: this.observations,
        reviewerSignature: this.reviewerSignature,
        approverSignature: this.approverSignature
      });
      alert('Report saved successfully!');
    },
    
    submitReport() {
      if (!this.canSubmit) {
        alert('Please complete all required fields and signatures before submitting.');
        return;
      }
      
      // Submit report logic
      console.log('Submitting report:', {
        observations: this.observations,
        reviewerSignature: this.reviewerSignature,
        approverSignature: this.approverSignature
      });
      alert('Report submitted successfully!');
    },
    
    exportReport() {
      // Export logic - could generate PDF or Excel
      console.log('Exporting report...');
      alert('Report export functionality will be implemented here.');
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
  background: white;
  padding: 20px 25px;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 25px;
  text-align: center;
  font-size: 1.3em;
  font-weight: 600;
  color: #2d3748;
  text-decoration: underline;
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
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.signature-image {
  max-width: 200px;
  max-height: 80px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
}

.signature-name {
  font-weight: 600;
  color: #2d3748;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
  margin-top: 30px;
}

.btn {
  padding: 15px 30px;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1em;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-primary {
  background: #2d3748;
  color: white;
  box-shadow: 0 4px 15px rgba(45, 55, 72, 0.3);
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(45, 55, 72, 0.4);
}

.btn-secondary {
  background: #718096;
  color: white;
  box-shadow: 0 4px 15px rgba(113, 128, 150, 0.3);
}

.btn-secondary:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(113, 128, 150, 0.4);
}

.btn-success {
  background: #4a5568;
  color: white;
  box-shadow: 0 4px 15px rgba(74, 85, 104, 0.3);
}

.btn-success:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(74, 85, 104, 0.4);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* Signature Modal */
.signature-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 3000;
  padding: 20px;
}

.signature-modal {
  background: white;
  border-radius: 20px;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.3);
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 25px 30px;
  background: #2d3748;
  border-radius: 20px 20px 0 0;
  color: white;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.4em;
  font-weight: 600;
}

.close-button {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  transition: all 0.3s ease;
  color: white;
}

.close-button:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.05);
}

.modal-content {
  padding: 30px;
}

.signature-form {
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-weight: 600;
  color: #4a5568;
  margin-bottom: 10px;
}

.form-input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1em;
  transition: border-color 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: #4a5568;
}

.signature-canvas-container {
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  padding: 20px;
  background: #f8fafc;
}

.signature-canvas {
  width: 100%;
  height: 200px;
  border: 1px solid #cbd5e0;
  border-radius: 6px;
  background: white;
  cursor: crosshair;
}

.canvas-controls {
  margin-top: 15px;
  text-align: center;
}

.clear-btn {
  background: #e53e3e;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 8px 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.clear-btn:hover {
  background: #c53030;
  transform: translateY(-1px);
}

.modal-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
  padding-top: 20px;
  border-top: 1px solid #e2e8f0;
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
  
  .action-buttons {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
    justify-content: center;
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
