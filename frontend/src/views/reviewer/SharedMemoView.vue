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
    </header>

    <div class="form-content">
      <div class="form-card">
        <h2 class="card-title">REQUISITION FOR DGAQA INSPECTION</h2>
        <div class="grid-layout">
          <div class="grid-item"><span>FROM:</span><input type="text" v-model="memoData.from" readonly /></div>
          <div class="grid-item"><span>CASCIC Ref No.:</span><input type="text" v-model="memoData.cascicRefNo" readonly /></div>
          <div class="grid-item"><span>CASCIC/</span><input type="text" v-model="memoData.cascic" readonly /></div>
          <div class="grid-item"><span>Dated:</span><input type="text" v-model="memoData.dated" readonly /></div>
          <div class="grid-item"><span>TO:</span><input type="text" v-model="memoData.to" readonly /></div>
          <div class="grid-item"><span>Wing/Proj Ref No.:</span><input type="text" v-model="memoData.wingProjRefNo" readonly /></div>
          <div class="grid-item-full"><span>Name & contact No of CASCIC (Designs) coordinator:</span><input type="text" v-model="memoData.coordinatorContact" readonly /></div>
        </div>
      </div>
      <div class="form-card">
        <div class="grid-layout two-col">
          <div class="grid-item-half"><span>LRU/SRU DETAILS</span><input type="text" v-model="memoData.lruSruDetails" readonly /></div>
          <div class="grid-item-half"><span>LRU/SRU Desc:</span><input type="text" v-model="memoData.lruSruDesc" readonly /></div>
        </div>
        <div class="grid-layout two-col-doc">
          <div class="grid-item"><span>Ref Doc</span><input type="text" v-model="memoData.refDoc" readonly /></div>
          <div class="grid-item"><span>Ref No of Document</span><input type="text" v-model="memoData.refNoDocument" readonly /></div>
          <div class="grid-item"><span>ver</span><input type="text" v-model="memoData.version" readonly /></div>
          <div class="grid-item"><span>rev</span><input type="text" v-model="memoData.revision" readonly /></div>
        </div>
        <div class="grid-layout">
          <div class="grid-item"><span>Part No:</span><input type="text" v-model="memoData.partNo" readonly /></div>
          <div class="grid-item"><span>Manufacturer:</span><input type="text" v-model="memoData.manufacturer" readonly /></div>
          <div class="grid-item"><span>Sl.No of units:</span><input type="text" v-model="memoData.serialNo" readonly /></div>
          <div class="grid-item"><span>Drawing no/Rev:</span><input type="text" v-model="memoData.drawingNoRev" readonly /></div>
          <div class="grid-item"><span>Qty Offered:</span><input type="text" v-model="memoData.qtyOffered" readonly /></div>
          <div class="grid-item"><span>source:</span><input type="text" v-model="memoData.source" readonly /></div>
        </div>
        <div class="grid-layout two-col">
          <div class="grid-item-half"><span>UNIT IDENTIFICATION:</span><input type="text" v-model="memoData.unitIdentification" readonly /></div>
          <div class="grid-item-half"><span>MECHANICAL INSPN:</span><input type="text" v-model="memoData.mechanicalInspection" readonly /></div>
        </div>
        <div class="grid-layout two-col">
          <div class="grid-item-half"><span>INSPECTION /TEST STAGE OFFERED NOW:</span><input type="text" v-model="memoData.inspectionTestStage" readonly /></div>
          <div class="grid-item-half"><span>STTE Status:</span><input type="text" v-model="memoData.stteStatus" readonly /></div>
        </div>
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
      memoData: {
        from: 'CASCIC Design Team',
        cascicRefNo: 'CASCIC/2025/001',
        cascic: 'CASCIC/DES/2025',
        dated: '15-01-2025',
        to: 'DGAQA Inspection Team',
        wingProjRefNo: 'WING/PROJ/2025/001',
        coordinatorContact: 'John Smith - +91-9876543210',
        lruSruDetails: 'LRU-001',
        lruSruDesc: 'Flight Control Unit',
        refDoc: 'FCU-SPEC-001',
        refNoDocument: 'DOC/FCU/2025/001',
        version: '1.0',
        revision: 'A',
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

</style>
