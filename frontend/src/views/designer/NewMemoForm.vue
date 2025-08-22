<template>
  <div class="new-memo-form">
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
      <h1 class="form-title">REQUISITION FOR DGAQA INSPECTION</h1>
      
      <!-- General Requisition Information -->
      <div class="form-section">
        <div class="form-row">
          <div class="form-group">
            <label>FROM:</label>
            <input type="text" class="form-input" placeholder="">
            <input type="text" class="form-input" placeholder="">
          </div>
          <div class="form-group">
            <label>CASDIC Ref No.:</label>
            <input type="text" class="form-input" placeholder="">
          </div>
          <div class="form-group">
            <label>CASDIC/</label>
            <input type="text" class="form-input" placeholder="">
          </div>
          <div class="form-group">
            <label>Dated:</label>
            <input type="text" class="form-input" placeholder="">
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>TO:</label>
            <input type="text" class="form-input" placeholder="">
            <input type="text" class="form-input" placeholder="">
          </div>
          <div class="form-group">
            <label>Wing/Proj Ref No.:</label>
            <input type="text" class="form-input" placeholder="">
          </div>
        </div>

        <div class="form-row">
          <div class="form-group full-width">
            <label>Name & contact No of CASDIC (Designs) coordinator:</label>
            <input type="text" class="form-input" placeholder="">
          </div>
        </div>
      </div>

      <hr class="section-divider">

      <!-- LRU/SRU Details -->
      <div class="form-section">
        <div class="section-header">
          <h3>LRU/SRU DETAILS</h3>
          <div class="dropdown-group">
            <label>LRU/SRU Desc:</label>
            <div class="dropdown-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="6,9 12,15 18,9"></polyline>
              </svg>
            </div>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Part No:</label>
            <input type="text" class="form-input" placeholder="">
          </div>
          <div class="form-group">
            <label>Manufacturer:</label>
            <input type="text" class="form-input" placeholder="">
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Sl.No of units:</label>
            <input type="text" class="form-input" placeholder="">
            <div class="dropdown-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="6,9 12,15 18,9"></polyline>
              </svg>
            </div>
          </div>
          <div class="form-group">
            <label>Drawing no /Rev:</label>
            <input type="text" class="form-input" placeholder="">
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Qty Offered:</label>
            <input type="text" class="form-input" placeholder="">
          </div>
          <div class="form-group">
            <label>source:</label>
            <input type="text" class="form-input" placeholder="">
          </div>
        </div>

        <div class="reference-docs">
          <div class="ref-header">
            <span>Ref Doc</span>
            <span>Ref No of Document</span>
            <span>ver</span>
            <span>rev</span>
          </div>
          <div class="ref-rows">
            <div class="ref-row" v-for="i in 5" :key="i">
              <input type="text" class="ref-input" placeholder="">
              <input type="text" class="ref-input" placeholder="">
              <input type="text" class="ref-input" placeholder="">
              <input type="text" class="ref-input" placeholder="">
            </div>
          </div>
        </div>
      </div>

      <hr class="section-divider">

      <!-- Unit Identification & Inspection -->
      <div class="form-section">
        <div class="form-row">
          <div class="form-group">
            <label>UNIT IDENTIFICATION:</label>
            <input type="text" class="form-input" placeholder="">
            <div class="dropdown-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="6,9 12,15 18,9"></polyline>
              </svg>
            </div>
          </div>
          <div class="form-group">
            <label>MECHANICAL INSPN:</label>
            <input type="text" class="form-input" placeholder="">
            <div class="dropdown-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="6,9 12,15 18,9"></polyline>
              </svg>
            </div>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>INSPECTION / TEST STAGE OFFERED NOW :</label>
            <input type="text" class="form-input" placeholder="">
          </div>
          <div class="form-group">
            <label>STTE Status:</label>
            <input type="text" class="form-input" placeholder="">
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
  name: 'NewMemoForm',
  data() {
    return {
      formData: {
        from: ['', ''],
        casdicRef: '',
        casdic: '',
        dated: '',
        to: ['', ''],
        wingProjRef: '',
        coordinator: '',
        partNo: '',
        manufacturer: '',
        units: '',
        drawingNo: '',
        qtyOffered: '',
        source: '',
        unitIdentification: '',
        mechanicalInspn: '',
        inspectionStage: '',
        stteStatus: '',
        referenceDocs: Array(5).fill().map(() => ({ doc: '', refNo: '', ver: '', rev: '' }))
      }
    };
  },
  methods: {
    submitForm() {
      // Handle form submission
      console.log('Form submitted:', this.formData);
      // Navigate back or show success message
      this.$router.go(-1);
    }
  }
};
</script>

<style scoped>
.new-memo-form {
  min-height: 100vh;
  background-color: #f0f0f0;
  padding: 20px;
}

.header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 30px;
}

.back-button {
  background: none;
  border: none;
  cursor: pointer;
  color: #333;
}

.logo {
  width: 150px;
}

.form-container {
  background: white;
  border-radius: 10px;
  padding: 40px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 1200px;
  margin: 0 auto;
}

.form-title {
  text-align: center;
  font-size: 1.8em;
  font-weight: bold;
  text-decoration: underline;
  margin-bottom: 30px;
  color: #333;
}

.form-section {
  margin-bottom: 30px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h3 {
  margin: 0;
  color: #333;
}

.dropdown-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.dropdown-icon {
  cursor: pointer;
  color: #666;
}

.form-row {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  align-items: flex-end;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
  flex: 1;
}

.form-group.full-width {
  flex: 2;
}

.form-group label {
  font-weight: bold;
  color: #333;
  font-size: 0.9em;
}

.form-input {
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.9em;
}

.form-input:focus {
  outline: none;
  border-color: #007bff;
}

.section-divider {
  border: none;
  height: 1px;
  background-color: #ccc;
  margin: 30px 0;
}

.reference-docs {
  margin-top: 20px;
}

.ref-header {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr 1fr;
  gap: 15px;
  margin-bottom: 10px;
  font-weight: bold;
  color: #333;
  font-size: 0.9em;
}

.ref-rows {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.ref-row {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr 1fr;
  gap: 15px;
}

.ref-input {
  padding: 6px 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.8em;
}

.form-actions {
  text-align: right;
  margin-top: 30px;
}

.submit-button {
  background: #007bff;
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: 25px;
  font-weight: bold;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.2s;
}

.submit-button:hover {
  background-color: #0056b3;
}

@media (max-width: 768px) {
  .form-container {
    padding: 20px;
  }
  
  .form-row {
    flex-direction: column;
    gap: 15px;
  }
  
  .ref-header,
  .ref-row {
    grid-template-columns: 1fr;
    gap: 10px;
  }
}
</style>
