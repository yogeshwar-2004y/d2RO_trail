<template>
  <div class="report-container">
    <h1 class="report-title">MECHANICAL INSPECTION REPORT</h1>

    <header class="report-header">
      <div class="header-section">
        <label>Project Name:</label>
        <span class="header-value">{{ reportData.projectName }}</span>
      </div>
      <div class="header-section">
        <label>Report No:</label>
        <span class="header-value">{{ reportData.reportNo }}</span>
      </div>
      <div class="header-section">
        <label>Date:</label>
        <span class="header-value">{{ formattedDate }}</span>
      </div>
    </header>

    <hr class="separator" />

    <form class="report-form">
      <section class="form-section">
        <h3 class="section-title">General Details</h3>
        <div class="form-grid">
          <div class="form-field">
            <label for="documentNo">Document No:</label>
            <input type="text" id="documentNo" v-model="reportData.documentNo" class="input-field" />
          </div>
          <div class="form-field">
            <label for="dateOfIssue">Date of Issue:</label>
            <input type="date" id="dateOfIssue" v-model="reportData.dateOfIssue" class="input-field" />
          </div>
          <div class="form-field">
            <label for="issueLevel">Issue Level:</label>
            <input type="text" id="issueLevel" v-model="reportData.issueLevel" class="input-field" />
          </div>
          <div class="form-field">
            <label for="customerName">Customer Name:</label>
            <input type="text" id="customerName" v-model="reportData.customerName" class="input-field" />
          </div>
          <div class="form-field">
            <label for="memoId">Memo ID:</label>
            <input type="text" id="memoId" v-model="reportData.memoId" class="input-field" />
          </div>
          <div class="form-field">
            <label for="productName">Product Name:</label>
            <input type="text" id="productName" v-model="reportData.productName" class="input-field" />
          </div>
          <div class="form-field">
            <label for="dpName">DP Name:</label>
            <input type="text" id="dpName" v-model="reportData.dpName" class="input-field" />
          </div>
          <div class="form-field">
            <label for="skuName">SRU Name:</label>
            <input type="text" id="skuName" v-model="reportData.skuName" class="input-field" />
          </div>
          <div class="form-field">
            <label for="partNo">Part No:</label>
            <input type="text" id="partNo" v-model="reportData.partNo" class="input-field" />
          </div>
          <div class="form-field">
            <label for="slNo">Sl. No:</label>
            <input type="text" id="slNo" v-model="reportData.slNo" class="input-field" />
          </div>
          <div class="form-field">
            <label for="qty">Quantity:</label>
            <input type="text" id="qty" v-model="reportData.qty" class="input-field" />
          </div>
        </div>
      </section>

      <section class="form-section">
        <h3 class="section-title">Test Timeline</h3>
        <div class="form-grid">
          <div class="form-field">
            <label for="testStartedOn">Test Started On:</label>
            <input type="datetime-local" id="testStartedOn" v-model="reportData.testStartedOn" class="input-field" />
          </div>
          <div class="form-field">
            <label for="testEndedOn">Test Ended On:</label>
            <input type="datetime-local" id="testEndedOn" v-model="reportData.testEndedOn" class="input-field" />
          </div>
        </div>
      </section>

      <section class="form-section table-section">
        <h3 class="section-title">Dimensional Checklist</h3>
        <div class="table-container">
          <table class="report-table">
            <thead>
              <tr>
                <th>Sl. No</th>
                <th>Dimension</th>
                <th>Tolerance</th>
                <th>Observed Value</th>
                <th>Instrument Used</th>
                <th>Remarks</th>
                <th class="upload-col">Upload (CoC/Snapshot)</th> </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in dimensionalChecklist" :key="'dim-'+index">
                <td>{{ index + 1 }}</td>
                <td><input type="text" v-model="item.dimension" class="table-input" /></td>
                <td><input type="text" v-model="item.tolerance" class="table-input" /></td>
                <td><input type="text" v-model="item.observedValue" class="table-input" /></td>
                <td><input type="text" v-model="item.instrumentUsed" class="table-input" /></td>
                <td><input type="text" v-model="item.remarks" class="table-input" /></td>
                <td class="upload-cell">
                  <input type="file" :id="'dim-upload-'+index" @change="handleFileUpload($event, item, 'dim')" class="file-input" />
                  <span v-if="item.fileName" class="file-name">{{ item.fileName }}</span>
                </td> </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section class="form-section table-section">
        <h3 class="section-title">Parameter Checklist</h3>
        <div class="table-container">
          <table class="report-table">
            <thead>
              <tr>
                <th>Sl. No</th>
                <th>Parameters</th>
                <th>Allowed / Not Allowed</th>
                <th>Yes/No</th>
                <th>Expected</th>
                <th>Remarks / Observations</th>
                <th class="upload-col">Upload (CoC/Snapshot)</th> </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in parameterChecklist" :key="'param-'+index">
                <td>{{ index + 1 }}</td>
                <td>{{ item.parameter }}</td>
                <td><input type="text" v-model="item.allowed" class="table-input" /></td>
                <td>
                  <div class="toggle-container">
                    <button
                      type="button"
                      :class="{ 'toggle-btn': true, 'active': item.yesNo === 'Yes' }"
                      @click="item.yesNo = 'Yes'"
                    >Yes</button>
                    <button
                      type="button"
                      :class="{ 'toggle-btn': true, 'active': item.yesNo === 'No' }"
                      @click="item.yesNo = 'No'"
                    >No</button>
                  </div>
                </td>
                <td><input type="text" v-model="item.expected" class="table-input" /></td>
                <td><input type="text" v-model="item.remarks" class="table-input" /></td>
                <td class="upload-cell">
                  <input type="file" :id="'param-upload-'+index" @change="handleFileUpload($event, item, 'param')" class="file-input" />
                  <span v-if="item.fileName" class="file-name">{{ item.fileName }}</span>
                </td> </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section class="form-section qa-section">
        <h3 class="section-title">Approval Details</h3>
        <div class="qa-grid">
          <div class="qa-column">
            <label class="qa-label">Prepared By</label>
            <div class="qa-field">
              <label>Signature:</label>
              <input type="text" v-model="approvalDetails.preparedBy.signature" class="input-field" />
            </div>
          </div>
          <div class="qa-column">
            <label class="qa-label">Verified By</label>
            <div class="qa-field">
              <label>Signature:</label>
              <input type="text" v-model="approvalDetails.verifiedBy.signature" class="input-field" />
            </div>
          </div>
          <div class="qa-column">
            <label class="qa-label">Approved By</label>
            <div class="qa-field">
              <label>Signature:</label>
              <input type="text" v-model="approvalDetails.approvedBy.signature" class="input-field" />
            </div>
          </div>
        </div>
      </section>
    </form>
  </div>
</template>

<script>
export default {
  name: 'CombinedReportForm',
  data() {
    return {
      reportData: {
        projectName: 'Example Project X',
        reportNo: 'A-123-B',
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
        { dimension: '', tolerance: '', observedValue: '', instrumentUsed: '', remarks: '', fileName: null }, // ADDED fileName
        { dimension: '', tolerance: '', observedValue: '', instrumentUsed: '', remarks: '', fileName: null }, // ADDED fileName
        { dimension: '', tolerance: '', observedValue: '', instrumentUsed: '', remarks: '', fileName: null }, // ADDED fileName
      ],
      parameterChecklist: [
        { parameter: 'Burrs', allowed: '', yesNo: '', expected: '', remarks: '', fileName: null }, // ADDED fileName
        { parameter: 'Damages', allowed: '', yesNo: '', expected: '', remarks: '', fileName: null }, // ADDED fileName
        { parameter: 'Name Plate', allowed: '', yesNo: '', expected: '', remarks: '', fileName: null }, // ADDED fileName
        { parameter: 'Engraving', allowed: '', yesNo: '', expected: '', remarks: '', fileName: null }, // ADDED fileName
        { parameter: 'Passivation', allowed: '', yesNo: '', expected: '', remarks: '', fileName: null }, // ADDED fileName
        { parameter: 'Chromate', allowed: '', yesNo: '', expected: '', remarks: '', fileName: null }, // ADDED fileName
        { parameter: 'Electro-less Nickel plating', allowed: '', yesNo: '', expected: '', remarks: '', fileName: null }, // ADDED fileName
        { parameter: 'Fasteners', allowed: '', yesNo: '', expected: '', remarks: '', fileName: null }, // ADDED fileName
      ],
      approvalDetails: {
        preparedBy: {
          signature: ''
        },
        verifiedBy: {
          signature: ''
        },
        approvedBy: {
          signature: ''
        }
      },
      currentDate: new Date(),
    };
  },
  computed: {
    formattedDate() {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return this.currentDate.toLocaleDateString(undefined, options);
    },
  },
  methods: {
    // New method to handle file input change
    handleFileUpload(event, item, checklistType) {
      const file = event.target.files[0];
      if (file) {
        // In a real application, you'd upload this file to a server
        // and save the returned URL or file path/ID to 'item.fileReference' or similar.
        // Here, we just store the file name for display purposes.
        item.fileName = file.name;
        console.log(`Uploaded file for ${checklistType} item: ${file.name}`);
      } else {
        item.fileName = null;
      }
    }
  }
};
</script>

<style scoped>
/* Only adding the new/modified styles for the upload feature */

/* Table Styling - New/Modified columns */
.upload-col { 
    width: 15%; 
    white-space: nowrap; 
}

.upload-cell {
    /* Ensures the file input and name stack */
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.file-input {
    /* Basic styling for file input */
    font-size: 0.8em;
    padding: 2px 0;
    width: 100%;
    box-sizing: border-box;
}

.file-name {
    /* Style for showing the uploaded file name */
    display: block;
    font-size: 0.75em;
    color: green;
    margin-top: 5px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

/* Ensure the table inputs/toggles work well with the new column */
.report-table th,
.report-table td {
  padding: 8px 10px; /* Reduced padding slightly for space */
}
</style>