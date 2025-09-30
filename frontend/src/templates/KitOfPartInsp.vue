<template>
  <div class="inspection-report-container">
    <h1 class="report-title">Kit of Part Inspection Report</h1>
    <form @submit.prevent="handleSubmit" class="report-form">
      
      <section class="header-grid">
        <div class="form-group">
          <label for="project">Project Name</label>
          <input id="project" type="text" v-model="reportData.project" required />
        </div>
        <div class="form-group">
          <label for="dpName">DP Name</label>
          <input id="dpName" type="text" v-model="reportData.dpName" required />
        </div>
        <div class="form-group">
          <label for="reportRefNo">Report Ref No</label>
          <input id="reportRefNo" type="text" v-model="reportData.reportRefNo" required />
        </div>
        <div class="form-group">
          <label for="memoRefNo">Memo Ref No</label>
          <input id="memoRefNo" type="text" v-model="reportData.memoRefNo" />
        </div>
        <div class="form-group">
          <label for="lruName">LRU Name / Part No</label>
          <input id="lruName" type="text" v-model="reportData.lruName" required />
        </div>
        <div class="form-group">
          <label for="sruName">SRU Name</label>
          <input id="sruName" type="text" v-model="reportData.sruName" />
        </div>
        <div class="form-group">
          <label for="partNo">Part No</label>
          <input id="partNo" type="text" v-model="reportData.partNo" />
        </div>
        <div class="form-group">
          <label for="quantity">Quantity</label>
          <input id="quantity" type="number" v-model.number="reportData.quantity" min="1" required />
        </div>
        <div class="form-group">
          <label for="slNos">SL No's</label>
          <input id="slNos" type="text" v-model="reportData.slNos" />
        </div>
        <div class="form-group">
          <label for="testVenue">Test Venue</label>
          <input id="testVenue" type="text" v-model="reportData.testVenue" required />
        </div>
        <div class="form-group">
          <label for="startDate">Start Date/Time</label>
          <input id="startDate" type="datetime-local" v-model="reportData.startDate" required />
        </div>
        <div class="form-group">
          <label for="endDate">End Date/Time</label>
          <input id="endDate" type="datetime-local" v-model="reportData.endDate" required />
        </div>
      </section>

      <section class="results-section">
        <h2>Inspection Results</h2>
        <table class="inspection-table">
          <thead>
            <tr>
              <th>SL.NO.</th>
              <th>TEST CASES</th>
              <th>EXPECTED</th>
              <th class="observations-col">OBSERVATIONS</th>
              <th class="remark-col">REMARKS (OK/NOT OK)</th>
              <th class="upload-col">UPLOAD</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in reportData.inspectionItems" :key="item.slNo">
              <td>{{ item.slNo }}</td>
              <td class="test-case-col">{{ item.testCase }}</td>
              <td class="expected-col">{{ item.expected }}</td>
              <td>
                <textarea 
                  v-model="item.observations" 
                  rows="2" 
                  placeholder="Enter observations here..."
                ></textarea>
              </td>
              <td>
                <div class="radio-group">
                  <label>
                    <input type="radio" :name="'remark-'+item.slNo" value="OK" v-model="item.remarks" required> OK
                  </label>
                  <label>
                    <input type="radio" :name="'remark-'+item.slNo" value="NOT OK" v-model="item.remarks"> NOT OK
                  </label>
                </div>
              </td>
              <td class="upload-cell">
                <input type="file" @change="handleFileUpload($event, item)" />
                <span v-if="item.fileName" class="file-name">{{ item.fileName }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </section>

      <section class="signature-section">
        <div class="signature-block">
          <label for="preparedBy">Prepared By (QA G1 -Team)</label>
          <input id="preparedBy" type="text" v-model="reportData.preparedBy" required />
        </div>
        <div class="signature-block">
          <label for="verifiedBy">Verified By (G1H - QA G)</label>
          <input id="verifiedBy" type="text" v-model="reportData.verifiedBy" required />
        </div>
        <div class="signature-block">
          <label for="approvedBy">Approved By</label>
          <input id="approvedBy" type="text" v-model="reportData.approvedBy" required />
        </div>
      </section>

      <div class="action-buttons">
        <button type="submit" class="btn primary">Submit Report</button>
        <button type="button" class="btn secondary">Save Draft</button>
        <button type="button" class="btn secondary" @click="printReport">Print/Export PDF</button>
      </div>

    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// Define the initial structure and data for the inspection items
const initialInspectionItems = [
  { slNo: 1, testCase: 'Any observation pending from previous KOP stage', expected: 'NIL', observations: '', remarks: '', fileName: null },
  { slNo: 2, testCase: 'CoC verification of components', expected: 'Verified', observations: '', remarks: '', fileName: null },
  { slNo: 3, testCase: 'Quantity as BOM', expected: 'Matching', observations: '', remarks: '', fileName: null },
  { slNo: 4, testCase: 'Quantity as per number of boards to be assembled', expected: 'Matching', observations: '', remarks: '', fileName: null },
  { slNo: 5, testCase: 'Components storage in ESD cover', expected: 'Stored in ESD', observations: '', remarks: '', fileName: null },
  { slNo: 6, testCase: 'All connectors to be fitted with screws before assembly', expected: 'Fitted properly', observations: '', remarks: '', fileName: null },
  { slNo: 7, testCase: 'Any other observations', expected: 'NIL', observations: '', remarks: '', fileName: null },
];

// Reactive state for all form data
const reportData = ref({
  // Header fields
  project: '',
  dpName: '',
  reportRefNo: '',
  memoRefNo: '',
  lruName: '',
  sruName: '',
  partNo: '',
  quantity: null,
  slNos: '',
  testVenue: '',
  startDate: new Date().toISOString().slice(0, 16), // Default to current time
  endDate: new Date().toISOString().slice(0, 16), 

  // Table data
  inspectionItems: initialInspectionItems,

  // Footer/Signature fields
  preparedBy: '',
  verifiedBy: '',
  approvedBy: '',
});

// Method to handle file upload change
const handleFileUpload = (event, item) => {
  const file = event.target.files[0];
  if (file) {
    // Store the file name/reference. In a real app, you'd upload this file
    // and store a file path or ID.
    item.fileName = file.name;
    console.log(`File for item ${item.slNo}: ${file.name}`);
  } else {
    item.fileName = null;
  }
};

// Method to handle form submission
const handleSubmit = () => {
  console.log('Report Submitted:', JSON.parse(JSON.stringify(reportData.value)));
  // In a real application, this is where you would call an API to save the data.
  alert('Inspection Report Submitted!');
};

// Method for printing
const printReport = () => {
  window.print();
};
</script>

<style scoped>
/* BASIC STYLING FOR A CLEAR FORM LAYOUT */
.inspection-report-container {
  max-width: 1200px;
  margin: 20px auto;
  padding: 30px;
  border: 1px solid #ccc;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  font-family: Arial, sans-serif;
  background-color: #fff;
}

.report-title {
  text-align: center;
  margin-bottom: 25px;
  color: #333;
  border-bottom: 2px solid #007bff;
  padding-bottom: 10px;
}

/* HEADER GRID LAYOUT */
.header-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px 20px;
  margin-bottom: 30px;
  padding: 15px;
  border: 1px solid #ddd;
  background-color: #f9f9f9;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #555;
  font-size: 0.9em;
}

.form-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

/* TABLE STYLING */
.results-section h2 {
    margin-bottom: 15px;
    color: #007bff;
}

.inspection-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 25px;
}

.inspection-table th, 
.inspection-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
  vertical-align: top;
}

.inspection-table th {
  background-color: #007bff;
  color: white;
  font-weight: bold;
  font-size: 0.9em;
}

.inspection-table td {
    background-color: #fff;
    font-size: 0.85em;
}

.test-case-col { width: 25%; }
.expected-col { width: 10%; }
.observations-col { width: 30%; }
.remark-col { width: 15%; text-align: center; }
.upload-col { width: 10%; }

.inspection-table textarea {
  width: 100%;
  border: 1px solid #ccc;
  box-sizing: border-box;
  resize: vertical;
  min-height: 40px;
}

/* RADIO BUTTONS */
.radio-group {
    display: flex;
    flex-direction: column;
    gap: 5px;
    align-items: flex-start;
}

.radio-group label {
    font-weight: normal;
    font-size: 0.9em;
}

/* FILE UPLOAD */
.upload-cell input[type="file"] {
  max-width: 100%;
  font-size: 0.8em;
}

.file-name {
    display: block;
    font-size: 0.75em;
    color: green;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    margin-top: 5px;
}

/* SIGNATURE SECTION */
.signature-section {
    display: flex;
    justify-content: space-between;
    gap: 30px;
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px dashed #ccc;
}

.signature-block {
    flex: 1;
    text-align: center;
}

.signature-block label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 0.9em;
    color: #333;
}

.signature-block input {
    width: 90%;
    border: none;
    border-bottom: 1px solid #555;
    padding: 5px 0;
    text-align: center;
}

/* ACTION BUTTONS */
.action-buttons {
    text-align: center;
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid #eee;
}

.btn {
    padding: 10px 20px;
    margin: 0 10px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-weight: bold;
    transition: background-color 0.3s;
}

.btn.primary {
    background-color: #007bff;
    color: white;
}

.btn.primary:hover {
    background-color: #0056b3;
}

.btn.secondary {
    background-color: #6c757d;
    color: white;
}

.btn.secondary:hover {
    background-color: #5a6268;
}
</style>