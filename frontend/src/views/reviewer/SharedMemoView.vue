<template>
  <div class="shared-memo-view-container">
    <header class="app-header">
      <div class="logo-section">
        <svg 
          class="icon arrow-left" 
          viewBox="0 0 24 24" 
          fill="none" 
          stroke="currentColor" 
          stroke-width="2" 
          stroke-linecap="round" 
          stroke-linejoin="round"
          @click="goBack"
        >
          <path d="M19 12H5M12 19l-7-7 7-7"/>
        </svg>
        <span class="logo-text">AVIATRAX</span>
        <span class="memo-id">Shared Memo ID: {{ id }}</span>
        <span class="view-only-indicator">VIEW ONLY</span>
      </div>
      <div class="share-section">
        <button class="share-btn" @click="toggleShareModal">
          <svg class="icon share" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8M16 6l-4-4-4 4M12 2v13"/>
          </svg>
          <span class="share-text">share</span>
        </button>
      </div>
    </header>

    <div class="form-content">
      <div class="form-card">
        <h2 class="card-title">REQUISITION FOR DGAQA INSPECTION</h2>
        <table class="form-table">
          <tr>
            <td class="form-cell">
              <label>From :</label>
              <input type="text" v-model="memoData.from1" readonly />
              <input type="text" v-model="memoData.from2" readonly />
              <input type="text" v-model="memoData.from3" readonly />
            </td>
            <td class="form-cell">
              <label>CASDIC Ref No.:</label>
              <input type="text" v-model="memoData.casdicRefNo" readonly />
            </td>
            <td class="form-cell">
              <label>CASDIC/</label>
              <input type="text" v-model="memoData.casdic" readonly />
            </td>
            <td class="form-cell">
              <label>Dated:</label>
              <input type="text" v-model="memoData.dated" readonly />
            </td>
          </tr>
          <tr>
            <td class="form-cell">
              <label>To :</label>
              <input type="text" v-model="memoData.to1" readonly />
              <input type="text" v-model="memoData.to2" readonly />
            </td>
            <td class="form-cell">
              <label>Thru/: O I/c, WH</label>
            </td>
            <td class="form-cell">
              <label>Wing/Proj Ref No.:</label>
              <input type="text" v-model="memoData.wingProjRefNo" readonly />
            </td>
            <td class="form-cell"></td>
          </tr>
          <tr>
            <td class="form-cell"></td>
            <td class="form-cell" colspan="3">
              <label>Name & contact No of CASDIC (Designs) coordinator:</label>
              <input type="text" v-model="memoData.coordinatorContact" readonly />
            </td>
          </tr>
        </table>
      </div>
      <div class="form-card">
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
                  <input type="text" v-model="memoData.partNo" readonly />
                </div>
                <div class="lru-field">
                  <label>Manufacturer:</label>
                  <input type="text" v-model="memoData.manufacturer" readonly />
                </div>
              </td>
              <td class="desc-cell">
                <span>{{ memoData.lruSruDesc }}</span>
              </td>
              <td class="ref-cell">
                <input type="text" v-model="memoData.refDoc" readonly />
              </td>
              <td class="refno-cell">
                <input type="text" v-model="memoData.refNoDocument" readonly />
              </td>
              <td class="ver-cell">
                <input type="text" v-model="memoData.version" readonly />
              </td>
              <td class="rev-cell">
                <input type="text" v-model="memoData.revision" readonly />
              </td>
            </tr>
            
            <tr>
              <td class="lru-cell">
                <div class="lru-field">
                  <label>Sl.No of units :</label>
                  <input type="text" v-model="memoData.serialNo" readonly />
                </div>
                <div class="lru-field">
                  <label>Drawing no/Rev:</label>
                  <input type="text" v-model="memoData.drawingNoRev" readonly />
                </div>
              </td>
              <td class="desc-cell">
                <span>NA</span>
              </td>
              <td class="ref-cell">
                <input type="text" v-model="memoData.refDoc2" readonly />
              </td>
              <td class="refno-cell">
                <input type="text" v-model="memoData.refNo2" readonly />
              </td>
              <td class="ver-cell">
                <input type="text" v-model="memoData.version2" readonly />
              </td>
              <td class="rev-cell">
                <input type="text" v-model="memoData.revision2" readonly />
              </td>
            </tr>
            
            <tr>
              <td class="lru-cell">
                <div class="lru-field">
                  <label>Qty Offered:</label>
                  <input type="text" v-model="memoData.qtyOffered" readonly />
                </div>
                <div class="lru-field">
                  <label>source :</label>
                  <span>{{ memoData.source }}</span>
                </div>
              </td>
              <td class="desc-cell">
                <span>{{ memoData.description3 }}</span>
              </td>
              <td class="ref-cell">
                <input type="text" v-model="memoData.refDoc3" readonly />
              </td>
              <td class="refno-cell">
                <input type="text" v-model="memoData.refNo3" readonly />
              </td>
              <td class="ver-cell">
                <input type="text" v-model="memoData.version3" readonly />
              </td>
              <td class="rev-cell">
                <input type="text" v-model="memoData.revision3" readonly />
              </td>
            </tr>
            
            <tr>
              <td class="lru-cell">
                <div class="lru-field">
                  <label>UNIT IDENTIFICATION : SOFT / QT / AT / DT / TS / ESS</label>
                </div>
                <div class="lru-field">
                  <label>MECHANICAL INSPN :</label>
                  <input type="text" v-model="memoData.mechanicalInspection" readonly />
                </div>
              </td>
              <td class="desc-cell">
                <span>STAGE / PARTS / ASSY/ FINAL / INSTALL</span>
              </td>
              <td class="ref-cell">
                <input type="text" v-model="memoData.refDoc4" readonly />
              </td>
              <td class="refno-cell">
                <input type="text" v-model="memoData.refNo4" readonly />
              </td>
              <td class="ver-cell">
                <input type="text" v-model="memoData.version4" readonly />
              </td>
              <td class="rev-cell">
                <input type="text" v-model="memoData.revision4" readonly />
              </td>
            </tr>
            
            <tr>
              <td class="lru-cell">
                <div class="lru-field">
                  <label>INSPECTION / TEST STAGE OFFERED NOW:</label>
                  <input type="text" v-model="memoData.inspectionTestStage" readonly />
                </div>
              </td>
              <td class="desc-cell">
                <div class="lru-field">
                  <label>STTE Status:</label>
                  <input type="text" v-model="memoData.stteStatus" readonly />
                </div>
              </td>
              <td class="ref-cell">
                <input type="text" v-model="memoData.refDoc5" readonly />
              </td>
              <td class="refno-cell">
                <input type="text" v-model="memoData.refNo5" readonly />
              </td>
              <td class="ver-cell">
                <input type="text" v-model="memoData.version5" readonly />
              </td>
              <td class="rev-cell">
                <input type="text" v-model="memoData.revision5" readonly />
              </td>
            </tr>
            
            <tr>
              <td class="lru-cell">
                <label>TEST STAGE CLEARED:</label>
                <input type="text" v-model="memoData.testStageCleared" readonly />
              </td>
              <td class="desc-cell"></td>
              <td class="ref-cell">
                <input type="text" v-model="memoData.refDoc6" readonly />
              </td>
              <td class="refno-cell">
                <input type="text" v-model="memoData.refNo6" readonly />
              </td>
              <td class="ver-cell">
                <input type="text" v-model="memoData.version6" readonly />
              </td>
              <td class="rev-cell">
                <input type="text" v-model="memoData.revision6" readonly />
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="form-card">
        <div class="grid-layout">
          <div class="grid-item-half"><span>Above Unit is ready for Testing at venue, dated onwards.</span><input type="text" v-model="memoData.testingVenueDate" readonly /></div>
          <div class="grid-item-half"><span>Test facility to be used:</span><input type="text" v-model="memoData.testFacility" readonly /></div>
          <div class="grid-item-half"><span>Calibration status OK/Due on:</span><input type="text" v-model="memoData.calibrationStatus" readonly /></div>
          <div class="grid-item-half"><span>SIGNATURE: NAME / DESIGNATION</span><input type="text" v-model="memoData.signatureNameDesignation" readonly /></div>
          <div class="grid-item-quarter"><span>Test cycle / Duration:</span><input type="text" v-model="memoData.testCycleDuration" readonly /><span>hrs</span></div>
          <div class="grid-item-quarter"><span>Func. Check(Initial):</span><input type="text" v-model="memoData.funcCheckInitial" readonly /><span>date/time</span></div>
          <div class="grid-item-quarter"><span>Test Start on:</span><input type="text" v-model="memoData.testStartOn" readonly /><span>date/time</span></div>
          <div class="grid-item-quarter"><span>Perf. check (during):</span><input type="text" v-model="memoData.perfCheckDuring" readonly /><span>date/time</span></div>
          <div class="grid-item-half"><span>Test complete on:</span><input type="text" v-model="memoData.testCompleteOn" readonly /><span>date/time</span></div>
          <div class="grid-item-half"><span>Func Check (End):</span><input type="text" v-model="memoData.funcCheckEnd" readonly /><span>date/time</span></div>
        </div>
      </div>
      <div class="form-card">
        <div class="grid-layout one-col-checkbox">
          <p class="checkbox-title">It is certified that :</p>
          <label><input type="checkbox" v-model="memoData.certifications.mechanicalQualityRecords" disabled />Mechanical Quality Records of all the parts (Raw material TC (chemical & mechanical), Dimensional reports, NDT reports, Process certificates etc.) & Electrical Quality Records (Components Screening report, PCB manufacturing report, process compliance reports/ test reports, etc.) were verified thoroughly.</label>
          <label><input type="checkbox" v-model="memoData.certifications.cocVerified" disabled />CoC for SRU, fasteners & standard parts are verified and satisfactory</label>
          <label><input type="checkbox" v-model="memoData.certifications.sruSerialNoted" disabled />Sl no of the SRUs are noted down in the respective log book opened on _________</label>
          <label><input type="checkbox" v-model="memoData.certifications.noDefectInvestigation" disabled />No Defect investigation is pending against this LRU</label>
          <label><input type="checkbox" v-model="memoData.certifications.previousTestStagesCleared" disabled />All the previous test stages of this LRU/SRU are cleared</label>
          <label><input type="checkbox" v-model="memoData.certifications.cascicQAInspected" disabled />CASCIC QA has physically inspected and accepted the LRU on _________</label>
          <span class="signature-line">SIGNATURE of Rep, IQA CASCIC</span>
        </div>
      </div>
      <div class="form-card">
        <div class="grid-layout">
          <p class="remarks-title">Action taken & remarks by DGAQA</p>
          <div class="reviewer-comments-display">
            {{ memoData.reviewerComments || 'No comments provided' }}
          </div>
          <span class="signature-line right">SIGNATURE OF DGAQA REP..</span>
        </div>
      </div>
      <div class="form-card">
        <p class="remarks-title">Test Status</p>
        <div class="grid-layout one-col-checkbox">
          <label><input type="checkbox" v-model="memoData.testStatus.successfullyCompleted" disabled />Successfully completed</label>
          <label><input type="checkbox" v-model="memoData.testStatus.completedWithObservations" disabled />Completed with observations</label>
          <label><input type="checkbox" v-model="memoData.testStatus.testNotConducted" disabled />Test not conducted</label>
          <label><input type="checkbox" v-model="memoData.testStatus.testFailed" disabled />Test failed</label>
        </div>
      </div>
    </div>

    <!-- Share Modal -->
    <div v-if="showShareModal" class="share-modal-overlay" @click="toggleShareModal">
      <div class="share-modal-content" @click.stop>
        <h2>Share via Email</h2>
        <p>Enter email addresses separated by commas.</p>
        <input type="text" v-model="emailAddresses" placeholder="e.g., mail1@example.com, mail2@example.com" class="email-input" />
        <div class="modal-actions">
          <button @click="sendEmails" class="send-btn">Send</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SharedMemoView',
  props: {
    id: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      showShareModal: false,
      emailAddresses: '',
      memoData: {
        from1: 'MED, CASDIC (DARE), Bangalore',
        from2: 'DGAQA cell,',
        from3: 'ORDAQA(ADE), Bangalore',
        casdicRefNo: 'CASDIC/2025/001',
        casdic: 'CASDIC/DES/2025',
        dated: '15-01-2025',
        to1: 'DGAQA Inspection Team',
        to2: '',
        wingProjRefNo: 'WING/PROJ/2025/001',
        coordinatorContact: 'John Smith - +91-9876543210',
        lruSruDetails: 'LRU-001',
        lruSruDesc: 'Flight Control Unit',
        refDoc: 'FCU-SPEC-001',
        refNoDocument: 'DOC/FCU/2025/001',
        version: 'v1.0',
        revision: 'A',
        refDoc2: '',
        refNo2: '',
        version2: '',
        revision2: '',
        description3: '',
        refDoc3: '',
        refNo3: '',
        version3: '',
        revision3: '',
        refDoc4: '',
        refNo4: '',
        version4: '',
        revision4: '',
        refDoc5: '',
        refNo5: '',
        version5: '',
        revision5: '',
        testStageCleared: '',
        refDoc6: '',
        refNo6: '',
        version6: '',
        revision6: '',
        partNo: 'FCU-001-REV-A',
        manufacturer: 'Aviation Systems Ltd.',
        serialNo: 'SN001234567',
        drawingNoRev: 'DRW/FCU/001-REV-A',
        qtyOffered: '2',
        source: 'Manufacturer',
        unitIdentification: 'FCU-001-REV-A-SN001234567',
        mechanicalInspection: 'PASSED',
        inspectionTestStage: 'Final Assembly Test',
        stteStatus: 'READY',
        testingVenueDate: '20-01-2025',
        testFacility: 'Test Lab A',
        calibrationStatus: 'OK',
        signatureNameDesignation: 'Design Engineer',
        testCycleDuration: '24',
        funcCheckInitial: '20-01-2025 09:00',
        testStartOn: '20-01-2025 10:00',
        perfCheckDuring: '20-01-2025 14:00',
        testCompleteOn: '21-01-2025 10:00',
        funcCheckEnd: '21-01-2025 11:00',
        certifications: {
          mechanicalQualityRecords: true,
          cocVerified: true,
          sruSerialNoted: true,
          noDefectInvestigation: true,
          previousTestStagesCleared: true,
          cascicQAInspected: true
        },
        reviewerComments: 'Test completed successfully. All parameters within acceptable limits. Unit approved for next stage.',
        testStatus: {
          successfullyCompleted: true,
          completedWithObservations: false,
          testNotConducted: false,
          testFailed: false
        }
      }
    };
  },
  mounted() {
    this.fetchSharedMemoData();
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    fetchSharedMemoData() {
      // In a real application, you would fetch shared memo data from an API
      console.log('Fetching shared memo data for ID:', this.id);
      // You can replace this with actual API call
      // this.memoData = await api.getSharedMemo(this.id);
    },
    toggleShareModal() {
      this.showShareModal = !this.showShareModal;
      if (!this.showShareModal) {
        this.emailAddresses = '';
      }
    },
    sendEmails() {
      if (this.emailAddresses.trim() === '') {
        alert('Please enter at least one email address.');
        return;
      }
      
      const emails = this.emailAddresses.split(',').map(email => email.trim());
      console.log('Sharing memo to:', emails);
      
      alert(`Memo shared successfully to: ${emails.join(', ')}`);
      this.toggleShareModal();
    }
  }
};
</script>

<style scoped>
/* Scoped styles to prevent them from affecting other components */
:root {
  --background-color: #f0f0f0;
  --card-color: #e0e0e0;
  --text-color: #333;
  --border-color: #999;
  --input-bg: #fff;
  --button-bg: #007bff;
  --button-text: #fff;
}

.shared-memo-view-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  font-family: sans-serif;
  color: var(--text-color);
  background-color: var(--background-color);
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: var(--card-color);
  border-bottom: 1px solid var(--border-color);
}

.logo-section {
  display: flex;
  align-items: center;
}

.logo-section .icon {
  width: 24px;
  height: 24px;
  margin-right: 10px;
  cursor: pointer;
  transition: transform 0.2s;
}

.logo-section .icon:hover {
  transform: scale(1.1);
}

.logo-text {
  font-weight: bold;
  font-size: 1.2em;
}

.memo-id {
  margin-left: 20px;
  font-size: 0.9em;
  color: #666;
  font-weight: normal;
}

.view-only-indicator {
  margin-left: 15px;
  background-color: #dc3545;
  color: white;
  font-size: 0.8em;
  font-weight: bold;
  padding: 4px 8px;
  border-radius: 4px;
}

.share-section .share-btn {
  display: flex;
  align-items: center;
  background: none;
  border: none;
  color: var(--text-color);
  font-size: 1em;
  cursor: pointer;
}

.share-section .icon {
  width: 20px;
  height: 20px;
  margin-right: 5px;
}

.form-content {
  flex-grow: 1;
  overflow-y: auto;
  padding: 20px;
}

.form-card {
  background-color: var(--card-color);
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.card-title {
  text-align: center;
  margin-bottom: 20px;
  font-size: 1.2em;
  font-weight: bold;
}

.grid-layout {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 15px;
}

.grid-layout.two-col {
  grid-template-columns: 1fr 1fr;
}

.grid-layout.two-col-doc {
  grid-template-columns: repeat(4, 1fr);
}

.grid-layout.one-col-checkbox {
  grid-template-columns: 1fr;
}

.grid-item, .grid-item-full, .grid-item-half, .grid-item-quarter {
  display: flex;
  flex-direction: column;
}

.grid-item-full {
  grid-column: 1 / -1;
  display: flex;
  flex-direction: column;
}

.grid-item input, .grid-item-full input, .grid-item-half input, .grid-item-quarter input {
  width: 100%;
  padding: 8px 12px;
  border: 2px solid var(--border-color);
  border-radius: 4px;
  background-color: #f8f9fa;
  box-sizing: border-box;
  margin-top: 5px;
  font-size: 14px;
  color: #6c757d;
  cursor: not-allowed;
}

.grid-item span, .grid-item-full span, .grid-item-half span, .grid-item-quarter span {
  font-size: 0.9em;
}

.remarks-title {
  font-weight: bold;
  margin-bottom: 5px;
}

.reviewer-comments-display {
  width: 100%;
  padding: 12px;
  border: 2px solid var(--border-color);
  border-radius: 4px;
  background-color: #f8f9fa;
  font-size: 14px;
  min-height: 100px;
  margin: 10px 0;
  color: #6c757d;
  white-space: pre-wrap;
}

.signature-line {
  display: block;
  text-align: right;
  margin-top: 20px;
  font-weight: bold;
}

.one-col-checkbox label {
  display: flex;
  align-items: flex-start;
  margin-bottom: 10px;
  font-size: 0.9em;
  line-height: 1.2;
}

.one-col-checkbox input[type="checkbox"] {
  margin-right: 10px;
  margin-top: 2px;
}

.share-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.share-modal-content {
  background-color: white;
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 90%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.share-modal-content h2 {
  margin: 0;
  font-size: 1.5em;
  text-align: center;
}

.share-modal-content p {
  margin: 0;
  font-size: 0.9em;
  color: #666;
}

.email-input {
  width: 100%;
  padding: 10px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  box-sizing: border-box;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
}

.send-btn {
  padding: 10px 20px;
  background-color: var(--button-bg);
  color: var(--button-text);
  border: none;
  border-radius: 4px;
  cursor: pointer;
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
  background-color: #f8f9fa;
  cursor: not-allowed;
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
  background-color: #f8f9fa;
  cursor: not-allowed;
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
  background-color: #f8f9fa;
  cursor: not-allowed;
}
</style>
