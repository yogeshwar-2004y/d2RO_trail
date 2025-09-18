<template>
  <div class="new-memo-form">
    <div class="header">
      <button class="back-button" @click="$router.go(-1)">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M19 12H5"></path>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
      </button>
      <div class="logos-container">
        <img src="@/assets/images/aviatrax-logo.png" alt="AVIATRAX Logo" class="logo">
        <img src="@/assets/images/vista_logo.png" alt="Vista Logo" class="logo vista-logo">
      </div>
    </div>

    <div class="form-container">
      <h1 class="form-title">REQUISITION FOR DGAQA INSPECTION</h1>
      
      <!-- General Requisition Information -->
      <div class="form-section">
        <table class="form-table">
          <tr>
            <td class="form-cell">
              <label>From :</label>
              <input class="locked-input" type="text" value="MED, CASDIC (DARE), Bangalore" disabled>
              <input class="locked-input" type="text" value="DGAQA cell," disabled>
              <input class="locked-input" type="text" value="ORDAQA(ADE), Bangalore" disabled>
            </td>
            <td class="form-cell">
              <label>CASDIC Ref No.:</label>
              <input type="text" v-model="formData.casdicRef" placeholder="">
            </td>
            <td class="form-cell">
              <label>CASDIC/</label>
              <input type="text" v-model="formData.casdic" placeholder="">
            </td>
            <td class="form-cell">
              <label>Dated:</label>
              <input type="date" v-model="formData.casdicDate">
            </td>
          </tr>
          <tr>
            <td class="form-cell">
              <label>To :</label>
              <input class="locked-input" type="text" value="DGAQA cell," disabled>
              <input class="locked-input" type="text" value="ORDAQA(ADE), Bangalore" disabled>
            </td>
            <td class="form-cell">
              <label>Thru/: O I/c, WH</label>
            </td>
            <td class="form-cell">
              <label>Wing/Proj Ref No.:</label>
              <input type="text" v-model="formData.wingRef" placeholder="">
            </td>
            <td class="form-cell"></td>
          </tr>
          <tr>
            <td class="form-cell"></td>
            <td class="form-cell wide-field" colspan="3">
              <label>Name & contact No of CASDIC (Designs) coordinator:</label>
              <input type="text" v-model="formData.coordinator" placeholder="">
            </td>
          </tr>
        </table>
      </div>

      <hr class="section-divider">

      <!-- LRU/SRU Details -->
      <div class="form-section">
        <table class="details-table">
          <thead>
            <tr>
              <th rowspan="2" class="lru-header">LRU / SRU DETAILS</th>
              <th rowspan="2" class="desc-header">LRU / SRU Desc:</th>
              <th rowspan="2" class="ref-doc-header">Ref Doc</th>
              <th rowspan="2" class="ref-no-header">Ref No of Document</th>
              <th class="ver-header">ver</th>
              <th class="rev-header">rev</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="lru-cell">
                <div class="lru-field">
                  <label>Part No:</label>
                  <input type="text" v-model="formData.partNo" placeholder="">
                </div>
                <div class="lru-field">
                  <label>Manufacturer:</label>
                  <input type="text" v-model="formData.manufacturer" placeholder="">
                </div>
              </td>
              <td class="desc-cell">
                <textarea v-model="formData.description" placeholder=""></textarea>
              </td>
              <td class="ref-cell">
                <input type="text" v-model="formData.refDoc" placeholder="">
              </td>
              <td class="refno-cell">
                <input type="text" v-model="formData.refNo" placeholder="">
              </td>
              <td class="ver-cell">
                <input type="text" v-model="formData.version" placeholder="">
              </td>
              <td class="rev-cell">
                <input type="text" v-model="formData.revision" placeholder="">
              </td>
            </tr>
            
            <tr>
              <td class="lru-cell">
                <div class="lru-field">
                  <label>Sl.No of units :</label>
                  <input type="text" v-model="formData.slNo" placeholder="">
                </div>
                <div class="lru-field">
                  <label>Drawing no/Rev:</label>
                  <input type="text" v-model="formData.drawingNo" placeholder="">
                </div>
              </td>
              <td class="desc-cell">
                <span>NA</span>
              </td>
              <td class="ref-cell">
                <input type="text" v-model="formData.refDoc2" placeholder="">
              </td>
              <td class="refno-cell">
                <input type="text" v-model="formData.refNo2" placeholder="">
              </td>
              <td class="ver-cell">
                <input type="text" v-model="formData.version2" placeholder="">
              </td>
              <td class="rev-cell">
                <input type="text" v-model="formData.revision2" placeholder="">
              </td>
            </tr>
            
            <tr>
              <td class="lru-cell">
                <div class="lru-field">
                  <label>Qty Offered:</label>
                  <input type="text" v-model="formData.qtyOffered" placeholder="">
                </div>
                <div class="lru-field">
                  <label>source :</label>
                  <span>NA</span>
                </div>
              </td>
              <td class="desc-cell">
                <textarea v-model="formData.description3" placeholder=""></textarea>
              </td>
              <td class="ref-cell">
                <input type="text" v-model="formData.refDoc3" placeholder="">
              </td>
              <td class="refno-cell">
                <input type="text" v-model="formData.refNo3" placeholder="">
              </td>
              <td class="ver-cell">
                <input type="text" v-model="formData.version3" placeholder="">
              </td>
              <td class="rev-cell">
                <input type="text" v-model="formData.revision3" placeholder="">
              </td>
            </tr>
            
            <tr>
              <td class="lru-cell">
                <div class="lru-field">
                  <label>UNIT IDENTIFICATION : SOFT / QT / AT / DT / TS / ESS</label>
                </div>
                <div class="lru-field">
                  <label>MECHANICAL INSPN :</label>
                  <input type="text" v-model="formData.mechanicalInspn" placeholder="">
                </div>
              </td>
              <td class="desc-cell">
                <span>STAGE / PARTS / ASSY/ FINAL / INSTALL</span>
              </td>
              <td class="ref-cell">
                <input type="text" v-model="formData.refDoc4" placeholder="">
              </td>
              <td class="refno-cell">
                <input type="text" v-model="formData.refNo4" placeholder="">
              </td>
              <td class="ver-cell">
                <input type="text" v-model="formData.version4" placeholder="">
              </td>
              <td class="rev-cell">
                <input type="text" v-model="formData.revision4" placeholder="">
              </td>
            </tr>
            
            <tr>
              <td class="lru-cell">
                <div class="lru-field">
                  <label>INSPECTION / TEST STAGE OFFERED NOW:</label>
                  <input type="text" v-model="formData.inspectionStage" placeholder="">
                </div>
              </td>
              <td class="desc-cell">
                <div class="lru-field">
                  <label>STTE Status:</label>
                  <input type="text" v-model="formData.stteStatus" placeholder="">
                </div>
              </td>
              <td class="ref-cell">
                <input type="text" v-model="formData.refDoc5" placeholder="">
              </td>
              <td class="refno-cell">
                <input type="text" v-model="formData.refNo5" placeholder="">
              </td>
              <td class="ver-cell">
                <input type="text" v-model="formData.version5" placeholder="">
              </td>
              <td class="rev-cell">
                <input type="text" v-model="formData.revision5" placeholder="">
              </td>
            </tr>
            
            <tr>
              <td class="lru-cell">
                <label>TEST STAGE CLEARED:</label>
                <input type="text" v-model="formData.testStageCleared" placeholder="">
              </td>
              <td class="desc-cell"></td>
              <td class="ref-cell">
                <input type="text" v-model="formData.refDoc6" placeholder="">
              </td>
              <td class="refno-cell">
                <input type="text" v-model="formData.refNo6" placeholder="">
              </td>
              <td class="ver-cell">
                <input type="text" v-model="formData.version6" placeholder="">
              </td>
              <td class="rev-cell">
                <input type="text" v-model="formData.revision6" placeholder="">
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <hr class="section-divider">


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
        casdicRef: '',
        casdic: '',
        casdicDate: '',
        wingRef: '',
        coordinator: '',
        partNo: '',
        manufacturer: '',
        description: '',
        refDoc: '',
        refNo: '',
        version: '',
        revision: '',
        slNo: '',
        drawingNo: '',
        refDoc2: '',
        refNo2: '',
        version2: '',
        revision2: '',
        qtyOffered: '',
        description3: '',
        refDoc3: '',
        refNo3: '',
        version3: '',
        revision3: '',
        mechanicalInspn: '',
        refDoc4: '',
        refNo4: '',
        version4: '',
        revision4: '',
        inspectionStage: '',
        stteStatus: '',
        refDoc5: '',
        refNo5: '',
        version5: '',
        revision5: '',
        testStageCleared: '',
        refDoc6: '',
        refNo6: '',
        version6: '',
        revision6: ''
      }
    };
  },
  methods: {
    submitForm() {
      // Create new memo object
      const newMemo = {
        id: Date.now(), // Generate unique ID
        project: this.formData.wingProjRef || 'NEW PROJECT',
        author: 'Design Team',
        assignedDate: this.formData.dated || '01-07-2025',
        scheduledDate: '04-07-2025',
        status: 'NOT ASSIGNED',
        formData: { ...this.formData } // Store all form data
      };

      // Emit event to parent or use router to pass data
      this.$router.push({
        name: 'DesignerMemo',
        params: { newMemo: JSON.stringify(newMemo) }
      });
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

.form-table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid #333;
}

.form-table td, .form-table th {
  border: 1px solid #333;
  padding: 8px;
  vertical-align: top;
}

.form-cell {
  position: relative;
}

.form-cell label {
  font-weight: bold;
  color: #333;
  font-size: 0.9em;
  display: block;
  margin-bottom: 5px;
}

.form-cell input {
  width: 100%;
  padding: 4px 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.9em;
  margin-bottom: 3px;
  box-sizing: border-box;
}

.form-cell input:focus {
  border-color: #80bdff;
  outline: none;
}

.locked-input {
  pointer-events: none;
  background-color: #f1f3f5;
  color: #6c757d;
  border: 1px solid #dee2e6;
  cursor: not-allowed;
}

.form-cell input[readonly] {
  background-color: #e9ecef !important;
  color: #495057 !important;
  cursor: not-allowed;
  border-color: #ced4da;
  pointer-events: none;
  user-select: none;
}

.fixed-text {
  padding: 4px 0px;
  font-size: 0.9em;
  margin-bottom: 3px;
  color: #6c757d;
  cursor: default;
  user-select: none;
  min-height: 20px;
  display: block;
  pointer-events: none;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  outline: none;
  -webkit-touch-callout: none;
  -webkit-tap-highlight-color: transparent;
  font-weight: normal;
  background: none;
  border: none;
}

.details-table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid #333;
}

.details-table th, .details-table td {
  border: 1px solid #333;
  padding: 8px;
  text-align: left;
  vertical-align: top;
}

.details-table th {
  background-color: #f8f9fa;
  font-weight: bold;
  text-align: center;
}

.lru-header {
  width: 25%;
}

.desc-header {
  width: 25%;
}

.ref-doc-header {
  width: 15%;
}

.ref-no-header {
  width: 20%;
}

.ver-header, .rev-header {
  width: 7.5%;
}

.lru-cell, .desc-cell, .ref-cell, .refno-cell, .ver-cell, .rev-cell {
  vertical-align: top;
}

.lru-field {
  margin-bottom: 10px;
}

.lru-field label {
  font-weight: bold;
  color: #333;
  font-size: 0.8em;
  display: block;
  margin-bottom: 3px;
}

.lru-field input {
  width: 100%;
  padding: 4px 6px;
  border: 1px solid #ccc;
  border-radius: 3px;
  font-size: 0.8em;
  box-sizing: border-box;
}

.desc-cell textarea {
  width: 100%;
  height: 60px;
  padding: 6px;
  border: 1px solid #ccc;
  border-radius: 3px;
  resize: vertical;
  font-size: 0.8em;
  box-sizing: border-box;
}

.desc-cell span {
  color: #666;
  font-size: 0.8em;
  font-style: italic;
}

.ref-cell input, .refno-cell input, .ver-cell input, .rev-cell input {
  width: 100%;
  padding: 4px 6px;
  border: 1px solid #ccc;
  border-radius: 3px;
  text-align: center;
  font-size: 0.8em;
  box-sizing: border-box;
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
