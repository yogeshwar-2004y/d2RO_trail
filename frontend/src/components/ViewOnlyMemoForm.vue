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
      <div class="view-only-badge">VIEW ONLY</div>
      <div class="logos-container">
        <img src="@/assets/images/aviatrax-logo.png" alt="Aviatrax Logo" class="logo">
        <img src="@/assets/images/vista_logo.png" alt="Vista Logo" class="logo vista-logo">
      </div>
    </div>

    <!-- Requisition Details Section -->
    <div class="form-section requisition-details">
      <table class="form-table">
        <tr>
          <td class="form-cell">
            <label>From :</label>
            <input 
              type="text" 
              v-model="formData.from1" 
              readonly
              class="readonly-field"
            >
          </td>
          <td class="form-cell">
            <label>CASDIC Ref No.:</label>
          </td>
          <td class="form-cell">
            <label>CASDIC/</label>
            <input type="text" v-model="formData.casdic" readonly class="readonly-field">
          </td>
          <td class="form-cell">
            <label>Dated:</label>
            <input type="text" v-model="formData.casdicDate" readonly class="readonly-field">
          </td>
        </tr>
        <tr>
          <td class="form-cell">
            <label>To :</label>
            <input 
              type="text" 
              v-model="formData.from2" 
              readonly
              class="readonly-field"
            >
            <input 
              type="text" 
              v-model="formData.from3" 
              readonly
              class="readonly-field"
            >
          </td>
          <td class="form-cell">
            <label>Thru/: O I/c, WH</label>
          </td>
          <td class="form-cell">
            <label>Wing/Proj Ref No.:</label>
            <input type="text" v-model="formData.wingRef" readonly class="readonly-field">
          </td>
          <td class="form-cell"></td>
        </tr>
        <tr>
          <td class="form-cell"></td>
          <td class="form-cell">
            <label>Name & contact No of CASDIC (Designs) coordinator:</label>
            <input type="text" v-model="formData.coordinator" readonly class="readonly-field">
          </td>
          <td class="form-cell"></td>
          <td class="form-cell"></td>
        </tr>
      </table>
    </div>

    <!-- LRU/SRU Table Section -->
    <div class="form-section lru-table">
      <table class="lru-grid">
        <thead>
          <tr>
            <th class="lru-header" rowspan="2">LRU/SRU DETAILS</th>
            <th class="lru-header" rowspan="2">LRU/SRU Desc</th>
            <th class="ref-header" colspan="4">Ref. Docnt</th>
          </tr>
          <tr>
            <th class="ref-header">Ref Doc</th>
            <th class="ref-header">Ref No of Document</th>
            <th class="ver-header">ver</th>
            <th class="rev-header">rev</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="lru-cell">
              <div class="lru-field">
                <label>Part No:</label>
                <input type="text" v-model="formData.partNo" readonly class="readonly-field">
              </div>
              <div class="lru-field">
                <label>Manufacturer:</label>
                <input type="text" v-model="formData.manufacturer" readonly class="readonly-field">
              </div>
            </td>
            <td class="desc-cell">
              <input type="text" v-model="formData.description" readonly class="readonly-field lru-description-input">
            </td>
            <td class="ref-cell">
              <input type="text" v-model="formData.refDoc" readonly class="readonly-field">
            </td>
            <td class="refno-cell">
              <input type="text" v-model="formData.refNo" readonly class="readonly-field">
            </td>
            <td class="ver-cell">
              <input type="text" v-model="formData.version" readonly class="readonly-field">
            </td>
            <td class="rev-cell">
              <input type="text" v-model="formData.revision" readonly class="readonly-field">
            </td>
          </tr>
          
          <!-- Additional reference rows -->
          <tr v-for="i in 5" :key="i">
            <td class="lru-cell"></td>
            <td class="desc-cell">
              <input type="text" v-model="formData[`description${i+1}`]" readonly class="readonly-field">
            </td>
            <td class="ref-cell">
              <input type="text" v-model="formData[`refDoc${i+1}`]" readonly class="readonly-field">
            </td>
            <td class="refno-cell">
              <input type="text" v-model="formData[`refNo${i+1}`]" readonly class="readonly-field">
            </td>
            <td class="ver-cell">
              <input type="text" v-model="formData[`version${i+1}`]" readonly class="readonly-field">
            </td>
            <td class="rev-cell">
              <input type="text" v-model="formData[`revision${i+1}`]" readonly class="readonly-field">
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Additional Details Section -->
    <div class="form-section additional-details">
      <table class="form-table">
        <tr>
          <td class="form-cell">
            <label>Drawing no/Rev:</label>
            <input type="text" v-model="formData.drawingRev" readonly class="readonly-field">
          </td>
          <td class="form-cell">
            <label>source:</label>
            <input type="text" v-model="formData.source" readonly class="readonly-field">
          </td>
          <td class="form-cell">
            <label>Sl.No of units:</label>
            <input type="text" v-model="formData.serialNo" readonly class="readonly-field">
          </td>
          <td class="form-cell">
            <label>Qty Offered:</label>
            <input type="text" v-model="formData.qtyOffered" readonly class="readonly-field">
          </td>
        </tr>
        <tr>
          <td class="form-cell" colspan="2">
            <label>UNIT IDENTIFICATION:</label>
            <input type="text" v-model="formData.unitIdentification" readonly class="readonly-field">
          </td>
          <td class="form-cell" colspan="2">
            <label>MECHANICAL INSPN:</label>
            <input type="text" v-model="formData.mechanicalInspection" readonly class="readonly-field">
          </td>
        </tr>
        <tr>
          <td class="form-cell" colspan="2">
            <label>INSPECTION /TEST STAGE OFFERED NOW:</label>
            <input type="text" v-model="formData.testStageOffered" readonly class="readonly-field">
          </td>
          <td class="form-cell">
            <label>Test stage cleared:</label>
            <input type="text" v-model="formData.testStageCleared" readonly class="readonly-field">
          </td>
          <td class="form-cell">
            <label>STTE Status:</label>
            <input type="text" v-model="formData.stteStatus" readonly class="readonly-field">
          </td>
        </tr>
      </table>
    </div>

    <!-- Testing Details Section -->
    <div class="form-section testing-details">
      <table class="form-table">
        <tr>
          <td class="form-cell" colspan="2">
            <label>Above Unit is ready for Testing at venue, dated onwards.</label>
            <input type="text" v-model="formData.venue" readonly class="readonly-field">
          </td>
          <td class="form-cell">
            <label>memo date:</label>
            <input type="text" v-model="formData.memoDate" readonly class="readonly-field">
          </td>
          <td class="form-cell">
            <label>Name / designation:</label>
            <input type="text" v-model="formData.nameDesignation" readonly class="readonly-field">
          </td>
        </tr>
        <tr>
          <td class="form-cell">
            <label>Test facility to be used:</label>
            <input type="text" v-model="formData.testFacility" readonly class="readonly-field">
          </td>
          <td class="form-cell">
            <label>Test cycle / Duration:</label>
            <input type="text" v-model="formData.testCycleDuration" readonly class="readonly-field">
          </td>
          <td class="form-cell">
            <label>Test Start on:</label>
            <input type="text" v-model="formData.testStartOn" readonly class="readonly-field">
          </td>
          <td class="form-cell">
            <label>Test complete on:</label>
            <input type="text" v-model="formData.testCompleteOn" readonly class="readonly-field">
          </td>
        </tr>
        <tr>
          <td class="form-cell">
            <label>Calibration status OK/Due on:</label>
            <input type="text" v-model="formData.calibrationStatus" readonly class="readonly-field">
          </td>
          <td class="form-cell">
            <label>Func. Check(Initial):</label>
            <input type="text" v-model="formData.funcCheckInitial" readonly class="readonly-field">
          </td>
          <td class="form-cell">
            <label>Perf. check (during):</label>
            <input type="text" v-model="formData.perfCheckDuring" readonly class="readonly-field">
          </td>
          <td class="form-cell">
            <label>Func Check (End):</label>
            <input type="text" v-model="formData.funcCheckEnd" readonly class="readonly-field">
          </td>
        </tr>
      </table>
    </div>

    <!-- Certification Section -->
    <div class="form-section certification">
      <h3>It is certified that :</h3>
      <div class="checkbox-group">
        <label class="checkbox-item">
          <input type="checkbox" v-model="formData.certifications.mechanicalQualityRecords" disabled>
          <span>Mechanical Quality Records verified thoroughly</span>
        </label>
        <label class="checkbox-item">
          <input type="checkbox" v-model="formData.certifications.cocVerified" disabled>
          <span>CoC for SRU, fasteners & standard parts verified</span>
        </label>
        <label class="checkbox-item">
          <input type="checkbox" v-model="formData.certifications.sruSerialNoted" disabled>
          <span>Sl no of the SRUs noted in log book</span>
        </label>
        <label class="checkbox-item">
          <input type="checkbox" v-model="formData.certifications.noDefectInvestigation" disabled>
          <span>No Defect investigation pending</span>
        </label>
        <label class="checkbox-item">
          <input type="checkbox" v-model="formData.certifications.previousTestStagesCleared" disabled>
          <span>All previous test stages cleared</span>
        </label>
        <label class="checkbox-item">
          <input type="checkbox" v-model="formData.certifications.cascicQAInspected" disabled>
          <span>CASCIC QA has physically inspected and accepted</span>
        </label>
      </div>
    </div>

    <!-- Remarks Section -->
    <div class="form-section remarks">
      <label>Remarks:</label>
      <textarea v-model="formData.remarks" readonly class="readonly-field remarks-textarea"></textarea>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ViewOnlyMemoForm',
  props: {
    id: {
      type: [String, Number],
      required: true
    },
    memoData: {
      type: Object,
      default: null
    },
    references: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      formData: {
        // Basic information
        from1: '',
        from2: '',
        from3: '',
        casdic: '',
        casdicDate: '',
        wingRef: '',
        coordinator: '',
        
        // LRU/SRU Details
        partNo: '',
        manufacturer: '',
        description: '',
        refDoc: '',
        refNo: '',
        version: '',
        revision: '',
        
        // Additional reference documents
        description2: '',
        refDoc2: '',
        refNo2: '',
        version2: '',
        revision2: '',
        description3: '',
        refDoc3: '',
        refNo3: '',
        version3: '',
        revision3: '',
        description4: '',
        refDoc4: '',
        refNo4: '',
        version4: '',
        revision4: '',
        description5: '',
        refDoc5: '',
        refNo5: '',
        version5: '',
        revision5: '',
        description6: '',
        refDoc6: '',
        refNo6: '',
        version6: '',
        revision6: '',
        
        // Additional details
        drawingRev: '',
        source: '',
        serialNo: '',
        qtyOffered: '',
        unitIdentification: '',
        mechanicalInspection: '',
        testStageOffered: '',
        testStageCleared: '',
        stteStatus: '',
        
        // Testing details
        venue: '',
        memoDate: '',
        nameDesignation: '',
        testFacility: '',
        testCycleDuration: '',
        testStartOn: '',
        testCompleteOn: '',
        calibrationStatus: '',
        funcCheckInitial: '',
        perfCheckDuring: '',
        funcCheckEnd: '',
        
        // Certifications
        certifications: {
          mechanicalQualityRecords: false,
          cocVerified: false,
          sruSerialNoted: false,
          noDefectInvestigation: false,
          previousTestStagesCleared: false,
          cascicQAInspected: false,
        },
        
        // Remarks
        remarks: ''
      }
    };
  },
  async mounted() {
    await this.fetchMemoData();
  },
  methods: {
    async fetchMemoData() {
      try {
        // If memo data is passed as props (from dashboard navigation), use it
        if (this.$route.params.memoData && this.$route.params.references) {
          this.transformAndSetMemoData(this.$route.params.memoData, this.$route.params.references);
          return;
        }

        // Otherwise, fetch from API
        const response = await fetch(`/api/memos/${this.id}`);
        if (!response.ok) {
          throw new Error(`Failed to fetch memo details: ${response.statusText}`);
        }

        const data = await response.json();
        if (data.success) {
          this.transformAndSetMemoData(data.memo, data.references || []);
        } else {
          throw new Error(data.message || 'Failed to fetch memo details');
        }
      } catch (error) {
        console.error('Error fetching memo data:', error);
        // Fallback to default data if fetch fails
        console.log('Using default memo data due to fetch error');
      }
    },

    transformAndSetMemoData(backendMemo, references) {
      console.log('Transforming backend memo data:', backendMemo, references);
      
      // Transform backend memo data to frontend format
      this.formData = {
        // Basic information
        from1: backendMemo.from_person || '',
        from2: backendMemo.to_person || '',
        from3: 'ORDAQA(ADE), Bangalore',
        casdic: backendMemo.casdic_ref_no || '',
        casdicDate: this.formatDate(backendMemo.dated),
        wingRef: backendMemo.wing_proj_ref_no || '',
        coordinator: backendMemo.coordinator || '',
        
        // LRU/SRU Details
        partNo: backendMemo.part_number || '',
        manufacturer: backendMemo.manufacturer || '',
        description: backendMemo.lru_sru_desc || '',
        refDoc: references[0]?.ref_doc || '',
        refNo: references[0]?.ref_no || '',
        version: references[0]?.ver?.toString() || '',
        revision: references[0]?.rev?.toString() || '',
        
        // Additional reference documents
        description2: '',
        refDoc2: references[1]?.ref_doc || '',
        refNo2: references[1]?.ref_no || '',
        version2: references[1]?.ver?.toString() || '',
        revision2: references[1]?.rev?.toString() || '',
        description3: '',
        refDoc3: references[2]?.ref_doc || '',
        refNo3: references[2]?.ref_no || '',
        version3: references[2]?.ver?.toString() || '',
        revision3: references[2]?.rev?.toString() || '',
        description4: '',
        refDoc4: references[3]?.ref_doc || '',
        refNo4: references[3]?.ref_no || '',
        version4: references[3]?.ver?.toString() || '',
        revision4: references[3]?.rev?.toString() || '',
        description5: '',
        refDoc5: references[4]?.ref_doc || '',
        refNo5: references[4]?.ref_no || '',
        version5: references[4]?.ver?.toString() || '',
        revision5: references[4]?.rev?.toString() || '',
        description6: '',
        refDoc6: references[5]?.ref_doc || '',
        refNo6: references[5]?.ref_no || '',
        version6: references[5]?.ver?.toString() || '',
        revision6: references[5]?.rev?.toString() || '',
        
        // Additional details
        drawingRev: backendMemo.drawing_no_rev || '',
        source: backendMemo.source || 'NA',
        serialNo: this.formatSerialNumbers(backendMemo.slno_units),
        qtyOffered: backendMemo.qty_offered?.toString() || '0',
        unitIdentification: this.formatUnitIdentification(backendMemo.unit_identification),
        mechanicalInspection: backendMemo.mechanical_inspn || '',
        testStageOffered: backendMemo.inspn_test_stage_offered || '',
        testStageCleared: backendMemo.test_stage_cleared || '',
        stteStatus: backendMemo.stte_status || '',
        
        // Testing details
        venue: backendMemo.venue || '',
        memoDate: this.formatDate(backendMemo.memo_date),
        nameDesignation: backendMemo.name_designation || '',
        testFacility: backendMemo.test_facility || '',
        testCycleDuration: backendMemo.test_cycle_duration || '',
        testStartOn: this.formatDateTime(backendMemo.test_start_on),
        testCompleteOn: this.formatDateTime(backendMemo.test_complete_on),
        calibrationStatus: backendMemo.calibration_status || '',
        funcCheckInitial: this.formatDateTime(backendMemo.func_check_initial),
        perfCheckDuring: this.formatDateTime(backendMemo.perf_check_during),
        funcCheckEnd: this.formatDateTime(backendMemo.func_check_end),
        
        // Certifications
        certifications: {
          mechanicalQualityRecords: backendMemo.certified?.includes('a') || false,
          cocVerified: backendMemo.certified?.includes('b') || false,
          sruSerialNoted: backendMemo.certified?.includes('c') || false,
          noDefectInvestigation: backendMemo.certified?.includes('d') || false,
          previousTestStagesCleared: backendMemo.certified?.includes('e') || false,
          cascicQAInspected: backendMemo.certified?.includes('f') || false,
        },
        
        // Remarks
        remarks: backendMemo.remarks || ''
      };
    },

    formatDate(dateString) {
      if (!dateString) return '';
      try {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-GB', {
          day: '2-digit',
          month: '2-digit',
          year: 'numeric'
        }).replace(/\//g, '-');
      } catch {
        return dateString;
      }
    },

    formatDateTime(datetimeString) {
      if (!datetimeString) return '';
      try {
        const date = new Date(datetimeString);
        return date.toLocaleString('en-GB', {
          day: '2-digit',
          month: '2-digit',
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        }).replace(',', '');
      } catch {
        return datetimeString;
      }
    },

    formatSerialNumbers(serialArray) {
      if (!serialArray || !Array.isArray(serialArray)) return '';
      return serialArray.join(', ');
    },

    formatUnitIdentification(unitIdArray) {
      if (!unitIdArray || !Array.isArray(unitIdArray)) return '';
      return unitIdArray.join(', ');
    }
  }
};
</script>

<style scoped>
.memo-form {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
  background: white;
}

.form-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #000;
}

.back-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.back-button:hover {
  background-color: #f0f0f0;
}

.form-title {
  text-align: center;
  font-size: 1.5em;
  font-weight: bold;
  margin: 0;
  flex-grow: 1;
}

.view-only-badge {
  background: #28a745;
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 0.9em;
  font-weight: bold;
}

.logos-container {
  display: flex;
  gap: 10px;
}

.logo {
  height: 40px;
}

.form-section {
  margin-bottom: 30px;
  border: 2px solid #000;
  padding: 20px;
}

.form-table {
  width: 100%;
  border-collapse: collapse;
}

.form-cell {
  padding: 10px;
  vertical-align: top;
}

.form-cell label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
  font-size: 0.9em;
}

.form-cell input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.9em;
}

.readonly-field {
  background-color: #f8f9fa;
  color: #6c757d;
  cursor: default;
}

.lru-grid {
  width: 100%;
  border-collapse: collapse;
  border: 2px solid #000;
}

.lru-grid th,
.lru-grid td {
  border: 1px solid #000;
  padding: 10px;
  text-align: center;
  font-weight: bold;
  font-size: 0.9em;
}

.lru-cell {
  width: 20%;
}

.desc-cell {
  width: 25%;
}

.ref-cell,
.refno-cell,
.ver-cell,
.rev-cell {
  width: 13.75%;
}

.lru-field {
  margin-bottom: 10px;
}

.lru-field label {
  font-size: 0.8em;
  margin-bottom: 3px;
}

.lru-description-input {
  width: 100%;
  text-align: left;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.checkbox-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.9em;
}

.checkbox-item input[type="checkbox"] {
  width: auto;
}

.remarks-textarea {
  width: 100%;
  height: 100px;
  resize: vertical;
}

.certification h3 {
  margin-bottom: 15px;
  font-size: 1.1em;
}

.testing-details .form-table,
.additional-details .form-table {
  margin-top: 10px;
}
</style>
