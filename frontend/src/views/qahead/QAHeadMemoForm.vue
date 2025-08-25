<template>
  <div class="memo-form">
    <!-- Header -->
    <div class="form-header">
      <button class="back-button" @click="$router.go(-1)">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M19 12H5"></path>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
      </button>
      <h1 class="form-title">REQUISITION FOR DGAQA INSPECTION</h1>
      <img src="@/assets/images/aviatrax-logo.png" alt="Aviatrax Logo" class="logo">
    </div>

    <!-- Requisition Details Section -->
    <div class="form-section requisition-details">
      <div class="form-grid">
        <div class="form-row">
          <div class="form-field">
            <label>FROM:</label>
            <input type="text" v-model="formData.from" placeholder="Enter sender details">
          </div>
          <div class="form-field">
            <label>CASDIC Ref No.:</label>
            <input type="text" v-model="formData.casdicRef" placeholder="Enter CASDIC reference">
          </div>
          <div class="form-field">
            <label>CASDIC/</label>
            <input type="text" v-model="formData.casdic" placeholder="Enter CASDIC details">
          </div>
          <div class="form-field">
            <label>Dated:</label>
            <input type="date" v-model="formData.casdicDate">
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-field">
            <label>TO:</label>
            <input type="text" v-model="formData.to" placeholder="Enter recipient details">
          </div>
          <div class="form-field">
            <label>Wing/Proj Ref No.:</label>
            <input type="text" v-model="formData.wingRef" placeholder="Enter wing/project reference">
          </div>
          <div class="form-field"></div>
          <div class="form-field"></div>
        </div>
        
        <div class="form-row">
          <div class="form-field"></div>
          <div class="form-field wide-field">
            <label>Name & contact No of CASDIC (Designs) coordinator:</label>
            <input type="text" v-model="formData.coordinator" placeholder="Enter coordinator details">
          </div>
          <div class="form-field"></div>
          <div class="form-field"></div>
        </div>
      </div>
    </div>

    <!-- LRU/SRU Details Section -->
    <div class="form-section lru-details">
      <div class="details-table">
        <div class="table-header">
          <div class="lru-column">LRU/SRU DETAILS</div>
          <div class="desc-column">LRU/SRU Desc:</div>
          <div class="checkbox-column">
            <input type="checkbox" v-model="formData.lruReady" id="lruReady">
            <label for="lruReady"></label>
          </div>
          <div class="ref-column">Ref Doc</div>
          <div class="refno-column">Ref No of Document</div>
          <div class="ver-column">ver</div>
          <div class="rev-column">rev</div>
        </div>
        
        <div class="table-row">
          <div class="lru-column">
            <div class="lru-field">
              <label>Part No:</label>
              <input type="text" v-model="formData.partNo" placeholder="Enter part number">
            </div>
            <div class="lru-field">
              <label>Manufacturer:</label>
              <input type="text" v-model="formData.manufacturer" placeholder="Enter manufacturer">
            </div>
          </div>
          <div class="desc-column">
            <textarea v-model="formData.description" placeholder="Enter LRU/SRU description"></textarea>
          </div>
          <div class="checkbox-column">
            <input type="checkbox" v-model="formData.unitsNoted" id="unitsNoted">
            <label for="unitsNoted"></label>
          </div>
          <div class="ref-column">
            <input type="text" v-model="formData.refDoc" placeholder="Enter reference document">
          </div>
          <div class="refno-column">
            <input type="text" v-model="formData.refNo" placeholder="Enter reference number">
          </div>
          <div class="ver-column">
            <input type="text" v-model="formData.version" placeholder="ver">
          </div>
          <div class="rev-column">
            <input type="text" v-model="formData.revision" placeholder="rev">
          </div>
        </div>
        
        <div class="table-row">
          <div class="lru-column">
            <div class="lru-field">
              <label>Sl.No of units:</label>
              <input type="text" v-model="formData.slNo" placeholder="Enter serial number">
            </div>
            <div class="lru-field">
              <label>Drawing no /Rev:</label>
              <input type="text" v-model="formData.drawingNo" placeholder="Enter drawing number">
            </div>
          </div>
          <div class="desc-column">
            <textarea v-model="formData.description2" placeholder="Additional description"></textarea>
          </div>
          <div class="checkbox-column">
            <input type="checkbox" v-model="formData.unitsNoted2" id="unitsNoted2">
            <label for="unitsNoted2"></label>
          </div>
          <div class="ref-column">
            <input type="text" v-model="formData.refDoc2" placeholder="Enter reference document">
          </div>
          <div class="refno-column">
            <input type="text" v-model="formData.refNo2" placeholder="Enter reference number">
          </div>
          <div class="ver-column">
            <input type="text" v-model="formData.version2" placeholder="ver">
          </div>
          <div class="rev-column">
            <input type="text" v-model="formData.revision2" placeholder="rev">
          </div>
        </div>
        
        <div class="table-row">
          <div class="lru-column">
            <div class="lru-field">
              <label>Qty Offered:</label>
              <input type="text" v-model="formData.qtyOffered" placeholder="Enter quantity">
            </div>
            <div class="lru-field">
              <label>source:</label>
              <input type="text" v-model="formData.source" placeholder="Enter source">
            </div>
          </div>
          <div class="desc-column">
            <textarea v-model="formData.description3" placeholder="Additional description"></textarea>
          </div>
          <div class="checkbox-column">
            <input type="checkbox" v-model="formData.unitsNoted3" id="unitsNoted3">
            <label for="unitsNoted3"></label>
          </div>
          <div class="ref-column">
            <input type="text" v-model="formData.refDoc3" placeholder="Enter reference document">
          </div>
          <div class="refno-column">
            <input type="text" v-model="formData.refNo3" placeholder="Enter reference number">
          </div>
          <div class="ver-column">
            <input type="text" v-model="formData.version3" placeholder="ver">
          </div>
          <div class="rev-column">
            <input type="text" v-model="formData.revision3" placeholder="rev">
          </div>
        </div>
        
        <div class="table-row">
          <div class="lru-column">
            <div class="lru-field">
              <label>UNIT IDENTIFICATION:</label>
              <input type="text" v-model="formData.unitId" placeholder="Enter unit identification">
            </div>
            <div class="lru-field">
              <label>MECHANICAL INSPN:</label>
              <input type="text" v-model="formData.mechanicalInsp" placeholder="Enter mechanical inspection">
            </div>
          </div>
          <div class="desc-column">
            <textarea v-model="formData.description4" placeholder="Additional description"></textarea>
          </div>
          <div class="checkbox-column">
            <input type="checkbox" v-model="formData.unitsNoted4" id="unitsNoted4">
            <label for="unitsNoted4"></label>
          </div>
          <div class="ref-column">
            <input type="text" v-model="formData.refDoc4" placeholder="Enter reference document">
          </div>
          <div class="refno-column">
            <input type="text" v-model="formData.refNo4" placeholder="Enter reference number">
          </div>
          <div class="ver-column">
            <input type="text" v-model="formData.version4" placeholder="ver">
          </div>
          <div class="rev-column">
            <input type="text" v-model="formData.revision4" placeholder="rev">
          </div>
        </div>
      </div>
    </div>

    <!-- Inspection/Test Stage Section -->
    <div class="form-section inspection-stage">
      <div class="stage-header">
        <div class="stage-field">
          <label>INSPECTION / TEST STAGE OFFERED NOW :</label>
          <input type="text" v-model="formData.inspectionStage" placeholder="Enter inspection/test stage">
        </div>
        <div class="stage-field">
          <label>STTE Status:</label>
          <input type="text" v-model="formData.stteStatus" placeholder="Enter STTE status">
        </div>
      </div>
    </div>

    <!-- Test Details Section -->
    <div class="form-section test-details">
      <div class="test-grid">
        <div class="test-column">
          <div class="test-field">
            <label>Above Unit is ready for Testing at</label>
            <input type="text" v-model="formData.testVenue" placeholder="venue, dated">
            <span>onwards.</span>
          </div>
          <div class="test-field">
            <label>SIGNATURE:</label>
            <div class="signature-box"></div>
          </div>
          <div class="test-field">
            <label>NAME / DESIGNATION</label>
            <input type="text" v-model="formData.signatureName" placeholder="Enter name and designation">
          </div>
        </div>
        
        <div class="test-column">
          <div class="test-field">
            <label>Test facility to be used:</label>
            <input type="text" v-model="formData.testFacility" placeholder="Enter test facility">
          </div>
          <div class="test-field">
            <label>Test cycle / Duration:</label>
            <input type="text" v-model="formData.testCycle" placeholder="Enter test cycle">
            <span>hrs</span>
          </div>
          <div class="test-field">
            <label>Test Start on:</label>
            <input type="datetime-local" v-model="formData.testStart">
          </div>
          <div class="test-field">
            <label>Test complete on :</label>
            <input type="datetime-local" v-model="formData.testComplete">
          </div>
        </div>
        
        <div class="test-column">
          <div class="test-field">
            <label>Calibration status OK/Due on :</label>
            <input type="date" v-model="formData.calibrationStatus">
          </div>
          <div class="test-field">
            <label>Func. Check(Initial) :</label>
            <input type="datetime-local" v-model="formData.funcCheckInitial">
          </div>
          <div class="test-field">
            <label>Perf. check (during) :</label>
            <input type="datetime-local" v-model="formData.perfCheckDuring">
          </div>
          <div class="test-field">
            <label>Func Check (end) :</label>
            <input type="datetime-local" v-model="formData.funcCheckEnd">
          </div>
        </div>
      </div>
    </div>

    <!-- Certification Section -->
    <div class="form-section certification">
      <h3>It is certified that :</h3>
      <div class="certification-list">
        <div class="cert-item">
          <input type="checkbox" v-model="formData.cert1" id="cert1">
          <label for="cert1">Mechanical Quality Records of all the parts (Raw material TC (chemical & mechanical), Dimensional reports, NDT reports, Process certificates etc.) & Electrical Quality Records (Components Screening report, PCB manufacturing report, process compliance reports/ test reports, etc.) were verified thoroughly.</label>
        </div>
        <div class="cert-item">
          <input type="checkbox" v-model="formData.cert2" id="cert2">
          <label for="cert2">CoC for SRU, fasteners & standard parts are verified and satisfactory</label>
        </div>
        <div class="cert-item">
          <input type="checkbox" v-model="formData.cert3" id="cert3">
          <label for="cert3">Sl no of the SRUs are noted down in the respective log book opened on</label>
          <input type="text" v-model="formData.logBookDate" placeholder="Enter date">
        </div>
        <div class="cert-item">
          <input type="checkbox" v-model="formData.cert4" id="cert4">
          <label for="cert4">No Defect investigation is pending against this LRU</label>
        </div>
        <div class="cert-item">
          <input type="checkbox" v-model="formData.cert5" id="cert5">
          <label for="cert5">All the previous test stages of this LRU/SRU are cleared</label>
        </div>
        <div class="cert-item">
          <input type="checkbox" v-model="formData.cert6" id="cert6">
          <label for="cert6">CASDIC QA has physically inspected and accepted the LRU on</label>
          <input type="text" v-model="formData.qaInspectionDate" placeholder="Enter date">
        </div>
      </div>
      
      <div class="signature-section">
        <div class="signature-box-large"></div>
        <p>SIGNATURE of Rep, IQA CASDIC</p>
      </div>
    </div>

    <!-- Action Taken Section -->
    <div class="form-section action-taken">
      <h3>Action taken & remarks by DGAQA</h3>
      <p class="instruction">(please use space overleaf for details)</p>
      <div class="remarks-area">
        <textarea v-model="formData.dgaqaRemarks" placeholder="Enter DGAQA remarks and actions taken..."></textarea>
      </div>
      <div class="signature-section">
        <div class="signature-box-large"></div>
        <p>SIGNATURE OF DGAQA REP..</p>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="action-buttons" v-if="memoData.status === 'Not Assigned'">
      <button class="btn btn-accept" @click="acceptMemo">ACCEPT</button>
      <button class="btn btn-reject" @click="rejectMemo">REJECT</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QAHeadMemoForm',
  data() {
    return {
      memoId: '',
      memoData: {
        status: 'Not Assigned'
      },
      formData: {
        from: '',
        casdicRef: '',
        casdic: '',
        casdicDate: '',
        to: '',
        wingRef: '',
        coordinator: '',
        partNo: '',
        manufacturer: '',
        description: '',
        lruReady: false,
        refDoc: '',
        refNo: '',
        version: '',
        revision: '',
        slNo: '',
        drawingNo: '',
        description2: '',
        unitsNoted: false,
        refDoc2: '',
        refNo2: '',
        version2: '',
        revision2: '',
        qtyOffered: '',
        source: '',
        description3: '',
        unitsNoted2: false,
        refDoc3: '',
        refNo3: '',
        version3: '',
        revision3: '',
        unitId: '',
        mechanicalInsp: '',
        description4: '',
        unitsNoted3: false,
        refDoc4: '',
        refNo4: '',
        version4: '',
        revision4: '',
        inspectionStage: '',
        stteStatus: '',
        testVenue: '',
        signatureName: '',
        testFacility: '',
        testCycle: '',
        testStart: '',
        testComplete: '',
        calibrationStatus: '',
        funcCheckInitial: '',
        perfCheckDuring: '',
        funcCheckEnd: '',
        cert1: false,
        cert2: false,
        cert3: false,
        cert4: false,
        cert5: false,
        cert6: false,
        logBookDate: '',
        qaInspectionDate: '',
        dgaqaRemarks: ''
      }
    };
  },
  mounted() {
    this.memoId = this.$route.params.memoId;
    this.loadMemoData();
  },
  methods: {
    loadMemoData() {
      // Simulate loading memo data based on memoId
      // In a real application, this would fetch from an API
      this.memoData = {
        id: this.memoId,
        status: 'Not Assigned',
        title: 'DGAQA Inspection Requisition',
        project: 'PRJ-2025-078',
        date: '2025-01-15'
      };
      
      // Auto-fill some sample data
      this.formData.from = 'CASDIC QA Department';
      this.formData.casdicRef = 'CAS-2025-001';
      this.formData.casdic = 'CASDIC/QA/2025';
      this.formData.casdicDate = '2025-01-15';
      this.formData.to = 'DGAQA Office';
      this.formData.wingRef = 'WING-2025-078';
      this.formData.coordinator = 'John Smith (Designs) - +91-98765-43210';
      this.formData.partNo = 'LRU-001';
      this.formData.manufacturer = 'Aviatrax Industries';
      this.formData.description = 'Main Control Unit for Aircraft Navigation System';
    },
    acceptMemo() {
      alert('Memo accepted successfully!');
      this.$router.go(-1);
    },
    rejectMemo() {
      alert('Memo rejected!');
      this.$router.go(-1);
    }
  }
};
</script>

<style scoped>
.memo-form {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f8f9fa;
  min-height: 100vh;
}

.form-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 30px;
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.back-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  transition: background-color 0.3s ease;
}

.back-button:hover {
  background-color: #e9ecef;
}

.form-title {
  margin: 0;
  font-size: 1.8em;
  font-weight: bold;
  color: #333;
  text-align: center;
  flex-grow: 1;
}

.logo {
  height: 40px;
  width: auto;
}

.form-section {
  background-color: white;
  border-radius: 10px;
  padding: 25px;
  margin-bottom: 25px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.form-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  gap: 20px;
  align-items: end;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-field label {
  font-weight: bold;
  color: #495057;
  font-size: 0.9em;
}

.form-field input {
  padding: 12px 15px;
  border: 1px solid #ced4da;
  border-radius: 8px;
  font-size: 1em;
  color: #495057;
  background-color: #f8f9fa;
  transition: border-color 0.3s ease;
}

.form-field input:focus {
  border-color: #80bdff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
  outline: none;
}

.wide-field {
  grid-column: span 2;
}

.details-table {
  border: 1px solid #dee2e6;
  border-radius: 8px;
  overflow: hidden;
}

.table-header {
  display: grid;
  grid-template-columns: 2fr 2fr 0.5fr 1fr 1fr 0.5fr 0.5fr;
  background-color: #e9ecef;
  padding: 15px;
  font-weight: bold;
  color: #495057;
  text-align: center;
  align-items: center;
}

.table-row {
  display: grid;
  grid-template-columns: 2fr 2fr 0.5fr 1fr 1fr 0.5fr 0.5fr;
  border-top: 1px solid #dee2e6;
  padding: 20px 15px;
  align-items: start;
  gap: 15px;
}

.lru-column {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.lru-field {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.lru-field label {
  font-weight: bold;
  color: #495057;
  font-size: 0.8em;
}

.lru-field input {
  padding: 8px 12px;
  border: 1px solid #ced4da;
  border-radius: 6px;
  font-size: 0.9em;
}

.desc-column textarea {
  width: 100%;
  height: 80px;
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 6px;
  resize: vertical;
  font-size: 0.9em;
}

.checkbox-column {
  display: flex;
  justify-content: center;
  align-items: center;
}

.checkbox-column input[type="checkbox"] {
  width: 20px;
  height: 20px;
  cursor: pointer;
}

.ref-column, .refno-column, .ver-column, .rev-column {
  display: flex;
  justify-content: center;
  align-items: center;
}

.ref-column input, .refno-column input, .ver-column input, .rev-column input {
  width: 100%;
  padding: 8px 10px;
  border: 1px solid #ced4da;
  border-radius: 6px;
  text-align: center;
  font-size: 0.9em;
}

.stage-header {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}

.stage-field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stage-field label {
  font-weight: bold;
  color: #495057;
  font-size: 1em;
}

.stage-field input {
  padding: 15px;
  border: 1px solid #ced4da;
  border-radius: 8px;
  font-size: 1em;
}

.test-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 30px;
}

.test-column {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.test-field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.test-field label {
  font-weight: bold;
  color: #495057;
  font-size: 0.9em;
}

.test-field input {
  padding: 12px 15px;
  border: 1px solid #ced4da;
  border-radius: 8px;
  font-size: 1em;
}

.test-field span {
  color: #6c757d;
  font-size: 0.9em;
}

.signature-box {
  width: 100%;
  height: 60px;
  border: 2px dashed #ced4da;
  border-radius: 8px;
  background-color: #f8f9fa;
}

.signature-box-large {
  width: 200px;
  height: 80px;
  border: 2px dashed #ced4da;
  border-radius: 8px;
  background-color: #f8f9fa;
  margin: 0 auto;
}

.certification h3 {
  color: #333;
  margin-bottom: 20px;
  font-size: 1.3em;
  border-bottom: 2px solid #e9ecef;
  padding-bottom: 10px;
}

.certification-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 30px;
}

.cert-item {
  display: flex;
  align-items: flex-start;
  gap: 15px;
}

.cert-item input[type="checkbox"] {
  width: 20px;
  height: 20px;
  margin-top: 3px;
  cursor: pointer;
}

.cert-item label {
  flex-grow: 1;
  color: #495057;
  line-height: 1.5;
}

.cert-item input[type="text"] {
  width: 150px;
  padding: 8px 12px;
  border: 1px solid #ced4da;
  border-radius: 6px;
  margin-left: 10px;
}

.signature-section {
  text-align: center;
  margin-top: 20px;
}

.signature-section p {
  margin: 10px 0 0 0;
  color: #6c757d;
  font-size: 0.9em;
}

.action-taken h3 {
  color: #333;
  margin-bottom: 15px;
  font-size: 1.3em;
  border-bottom: 2px solid #e9ecef;
  padding-bottom: 10px;
}

.instruction {
  color: #6c757d;
  font-style: italic;
  margin-bottom: 20px;
}

.remarks-area {
  margin-bottom: 30px;
}

.remarks-area textarea {
  width: 100%;
  height: 120px;
  padding: 15px;
  border: 1px solid #ced4da;
  border-radius: 8px;
  resize: vertical;
  font-size: 1em;
  font-family: inherit;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-top: 40px;
}

.btn {
  padding: 15px 40px;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  font-size: 1.1em;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 150px;
}

.btn-accept {
  background: linear-gradient(135deg, #28a745, #20c997);
  color: white;
}

.btn-accept:hover {
  background: linear-gradient(135deg, #218838, #1ea085);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
}

.btn-reject {
  background: linear-gradient(135deg, #dc3545, #e74c3c);
  color: white;
}

.btn-reject:hover {
  background: linear-gradient(135deg, #c82333, #c0392b);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(220, 53, 69, 0.3);
}

@media (max-width: 768px) {
  .form-header {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }
  
  .form-row {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  
  .wide-field {
    grid-column: span 1;
  }
  
  .table-header, .table-row {
    grid-template-columns: 1fr;
    gap: 10px;
  }
  
  .lru-column, .desc-column, .checkbox-column, .ref-column, .refno-column, .ver-column, .rev-column {
    grid-column: span 1;
  }
  
  .stage-header {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .test-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .action-buttons {
    flex-direction: column;
    align-items: center;
    gap: 20px;
  }
  
  .btn {
    width: 100%;
    max-width: 300px;
  }
}
</style>
