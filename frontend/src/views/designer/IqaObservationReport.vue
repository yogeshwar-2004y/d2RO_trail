<template>
  <div class="iqa-observation-report">
    <div class="header">
      <button class="back-button" @click="$router.go(-1)">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M19 12H5"></path>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
      </button>
      <img src="@/assets/images/aviatrax-logo.png" alt="AVIATRAX Logo" class="logo">
    </div>

    <div class="form-container">
      <h1 class="form-title">IQA OBSERVATION REPORT</h1>
      
      <!-- Header Information -->
      <div class="header-info">
        <div class="casdic-info">
          <span class="placeholder">CASDIC/project_name/lru_name/sl.no/no_of_observation/year</span>
        </div>
        <div class="date-info">
          <span class="label">Date:</span>
          <input type="text" class="date-input" v-model="formData.date" placeholder="">
        </div>
      </div>

      <div class="subject-line">
        <span class="subject-label">SUB : IQA Observation Report for</span>
        <input type="text" class="document-name-input" v-model="formData.documentName" placeholder="document_name">
      </div>

      <!-- Details Table -->
      <div class="details-table">
        <div class="table-row">
          <div class="table-cell label-cell">
            <span>Project Name :</span>
          </div>
          <div class="table-cell input-cell">
            <input type="text" class="form-input" v-model="formData.projectName" placeholder="">
          </div>
          <div class="table-cell label-cell">
            <span>Inspection stage : Document review/report</span>
          </div>
          <div class="table-cell input-cell">
            <input type="text" class="form-input" v-model="formData.inspectionStage" placeholder="">
          </div>
        </div>

        <div class="table-row">
          <div class="table-cell label-cell">
            <span>LRU Name :</span>
          </div>
          <div class="table-cell input-cell">
            <input type="text" class="form-input" v-model="formData.lruName" placeholder="">
          </div>
          <div class="table-cell label-cell">
            <span>Date of doc review :</span>
          </div>
          <div class="table-cell input-cell">
            <input type="text" class="form-input" v-model="formData.docReviewDate" placeholder="">
          </div>
        </div>

        <div class="table-row">
          <div class="table-cell label-cell">
            <span>LRU Part No. :</span>
          </div>
          <div class="table-cell input-cell">
            <input type="text" class="form-input" v-model="formData.lruPartNo" placeholder="">
          </div>
          <div class="table-cell label-cell">
            <span>Review venue :</span>
          </div>
          <div class="table-cell input-cell">
            <input type="text" class="form-input" v-model="formData.reviewVenue" placeholder="">
          </div>
        </div>

        <div class="table-row">
          <div class="table-cell label-cell">
            <span>Serial Number:</span>
          </div>
          <div class="table-cell input-cell">
            <input type="text" class="form-input" v-model="formData.serialNumber" placeholder="">
          </div>
          <div class="table-cell label-cell">
            <span>Reference Document: name, number, rev&ver, dated</span>
          </div>
          <div class="table-cell input-cell">
            <input type="text" class="form-input" v-model="formData.referenceDocument" placeholder="">
          </div>
        </div>
      </div>

      <!-- Observations Table -->
      <div class="observations-section">
        <h3 class="section-title">Observations</h3>
        <div class="observations-table">
          <div class="table-header">
            <div class="header-cell">SNO</div>
            <div class="header-cell">Category (Major/Minor)</div>
            <div class="header-cell">Observations</div>
            <div class="header-cell">Accept/Reject</div>
            <div class="header-cell">Justification</div>
          </div>
          
          <div v-for="(observation, index) in formData.observations" :key="index" class="table-row observation-row">
            <div class="table-cell">
              <span>{{ index + 1 }}</span>
            </div>
            <div class="table-cell">
              <select v-model="observation.category" class="category-select">
                <option value="">Select</option>
                <option value="Major">Major</option>
                <option value="Minor">Minor</option>
              </select>
            </div>
            <div class="table-cell">
              <textarea v-model="observation.observation" class="observation-textarea" placeholder="Enter observation"></textarea>
            </div>
            <div class="table-cell">
              <select v-model="observation.acceptReject" class="accept-reject-select">
                <option value="">Select</option>
                <option value="Accept">Accept</option>
                <option value="Reject">Reject</option>
              </select>
            </div>
            <div class="table-cell">
              <textarea v-model="observation.justification" class="justification-textarea" placeholder="Enter justification"></textarea>
            </div>
          </div>
        </div>
        
        <button class="add-observation-btn" @click="addObservation">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
          Add Observation
        </button>
      </div>

      <!-- Approval Section -->
      <div class="approval-section">
        <div class="approval-row">
          <div class="approval-item">
            <span class="approval-label">Reviewed by</span>
            <div class="signature-line"></div>
          </div>
          <div class="approval-item">
            <span class="approval-label">Approved by</span>
            <div class="signature-line"></div>
          </div>
        </div>
      </div>

      <div class="form-actions">
        <button class="submit-button" @click="submitForm">SUBMIT</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'IqaObservationReport',
  props: {
    reportId: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      formData: {
        date: '',
        documentName: '',
        projectName: '',
        inspectionStage: '',
        lruName: '',
        docReviewDate: '',
        lruPartNo: '',
        reviewVenue: '',
        serialNumber: '',
        referenceDocument: '',
        observations: [
          { category: '', observation: '', acceptReject: '', justification: '' },
          { category: '', observation: '', acceptReject: '', justification: '' }
        ]
      }
    };
  },
  methods: {
    addObservation() {
      this.formData.observations.push({
        category: '',
        observation: '',
        acceptReject: '',
        justification: ''
      });
    },
    submitForm() {
      // Handle form submission
      console.log('IQA Observation Report submitted:', this.formData);
      // Navigate back or show success message
      this.$router.go(-1);
    }
  }
};
</script>

<style scoped>
.iqa-observation-report {
  font-family: Arial, sans-serif;
  min-height: 100vh;
  background-color: #f0f0f0;
}

.header {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px;
  background: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.back-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 5px;
}

.logo {
  width: 150px;
}

.form-container {
  max-width: 1200px;
  margin: 20px auto;
  padding: 30px;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.form-title {
  text-align: center;
  font-size: 2em;
  font-weight: bold;
  margin-bottom: 30px;
  color: #000;
}

.header-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.casdic-info .placeholder {
  color: #888;
  font-style: italic;
}

.date-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.date-info .label {
  font-weight: bold;
}

.date-input {
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 150px;
}

.subject-line {
  text-align: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #000;
}

.subject-label {
  font-weight: bold;
  margin-right: 10px;
}

.document-name-input {
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 200px;
  font-weight: bold;
}

.details-table {
  border: 2px solid #000;
  margin-bottom: 30px;
}

.table-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  border-bottom: 1px solid #000;
}

.table-row:last-child {
  border-bottom: none;
}

.table-cell {
  padding: 15px;
  border-right: 1px solid #000;
  display: flex;
  align-items: center;
}

.table-cell:last-child {
  border-right: none;
}

.label-cell {
  background-color: #f8f9fa;
  font-weight: bold;
  justify-content: flex-start;
}

.input-cell {
  justify-content: center;
}

.form-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 5px;
  text-align: center;
}

.observations-section {
  margin-bottom: 30px;
}

.section-title {
  font-size: 1.5em;
  font-weight: bold;
  margin-bottom: 20px;
  color: #000;
}

.observations-table {
  border: 2px solid #000;
  margin-bottom: 20px;
}

.table-header {
  display: grid;
  grid-template-columns: 0.5fr 1fr 2fr 1fr 1.5fr;
  background-color: #f8f9fa;
  border-bottom: 2px solid #000;
}

.header-cell {
  padding: 15px;
  font-weight: bold;
  text-align: center;
  border-right: 1px solid #000;
}

.header-cell:last-child {
  border-right: none;
}

.observation-row {
  display: grid;
  grid-template-columns: 0.5fr 1fr 2fr 1fr 1.5fr;
  border-bottom: 1px solid #000;
}

.observation-row:last-child {
  border-bottom: none;
}

.observation-row .table-cell {
  padding: 10px;
  border-right: 1px solid #000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.observation-row .table-cell:last-child {
  border-right: none;
}

.category-select, .accept-reject-select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
  text-align: center;
}

.observation-textarea, .justification-textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
  resize: vertical;
  min-height: 60px;
  font-family: inherit;
}

.add-observation-btn {
  background: #007bff;
  color: #fff;
  border: none;
  border-radius: 25px;
  padding: 10px 20px;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 auto;
}

.add-observation-btn:hover {
  background-color: #0056b3;
}

.approval-section {
  margin-bottom: 30px;
}

.approval-row {
  display: flex;
  justify-content: space-between;
  gap: 100px;
}

.approval-item {
  flex: 1;
  text-align: center;
}

.approval-label {
  display: block;
  font-weight: bold;
  margin-bottom: 10px;
  color: #000;
}

.signature-line {
  height: 2px;
  background-color: #000;
  margin-top: 20px;
}

.form-actions {
  text-align: center;
}

.submit-button {
  background: #007bff;
  color: #fff;
  border: none;
  border-radius: 25px;
  padding: 15px 30px;
  font-weight: bold;
  font-size: 1.1em;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: background-color 0.2s;
}

.submit-button:hover {
  background-color: #0056b3;
}

@media (max-width: 768px) {
  .form-container {
    margin: 10px;
    padding: 20px;
  }
  
  .header-info {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
  
  .table-row, .observation-row {
    grid-template-columns: 1fr;
  }
  
  .approval-row {
    flex-direction: column;
    gap: 30px;
  }
}
</style>
