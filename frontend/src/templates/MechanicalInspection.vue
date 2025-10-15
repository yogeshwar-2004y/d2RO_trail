<template>
  <div class="mechanical-inspection-page">
    <!-- Main Content -->
    <div class="main-content">
      <!-- Form Header -->
      <div class="form-header">
        <div class="document-path">
          CASDIC/{{ reportData.projectName || "Project" }}/{{
            reportData.lruName
          }}/SL.{{ reportData.slNos }}/{{ reportData.reportRefNo }}/{{
            currentYear
          }}
        </div>
        <div class="report-date">Date: {{ formattedDate }}</div>
      </div>

      <div class="subject-line">
        SUB : Mechanical Inspection Report for {{ reportData.lruName }}
      </div>

      <!-- Inspection Form -->
      <form @submit.prevent="submitForm" class="inspection-form">
        <!-- Report Details Section -->
        <div class="form-section">
          <h2 class="section-title">Report Details</h2>
          <div class="general-info-grid">
            <!-- Left Column -->
            <div class="info-column">
              <div class="form-group">
                <label for="projectName">Project Name:</label>
                <input
                  type="text"
                  id="projectName"
                  v-model="reportData.projectName"
                  required
                />
              </div>
              <div class="form-group">
                <label for="reportRefNo">Report Ref No:</label>
                <input
                  type="text"
                  id="reportRefNo"
                  v-model="reportData.reportRefNo"
                  required
                />
              </div>
              <div class="form-group">
                <label for="memoRefNo">Memo Ref No:</label>
                <input
                  type="text"
                  id="memoRefNo"
                  v-model="reportData.memoRefNo"
                />
              </div>
              <div class="form-group">
                <label for="lruName">LRU Name:</label>
                <input
                  type="text"
                  id="lruName"
                  v-model="reportData.lruName"
                  required
                />
              </div>
              <div class="form-group">
                <label for="inspectionStage">Inspection Stage:</label>
                <input
                  type="text"
                  id="inspectionStage"
                  v-model="reportData.inspectionStage"
                />
              </div>
              <div class="form-group">
                <label for="testVenue">Test Venue:</label>
                <input
                  type="text"
                  id="testVenue"
                  v-model="reportData.testVenue"
                />
              </div>
              <div class="form-group">
                <label for="slNos">SL.NO'S:</label>
                <input type="text" id="slNos" v-model="reportData.slNos" />
              </div>
            </div>

            <!-- Right Column -->
            <div class="info-column">
              <div class="form-group">
                <label for="dpName">DP Name:</label>
                <input
                  type="text"
                  id="dpName"
                  v-model="reportData.dpName"
                  required
                />
              </div>
              <div class="form-group">
                <label for="dated1">Dated:</label>
                <input type="date" id="dated1" v-model="reportData.dated1" />
              </div>
              <div class="form-group">
                <label for="dated2">Dated:</label>
                <input type="date" id="dated2" v-model="reportData.dated2" />
              </div>
              <div class="form-group">
                <label for="sruName">SRU Name:</label>
                <input type="text" id="sruName" v-model="reportData.sruName" />
              </div>
              <div class="form-group">
                <label for="partNo">Part No:</label>
                <input
                  type="text"
                  id="partNo"
                  v-model="reportData.partNo"
                  required
                />
              </div>
              <div class="form-group">
                <label for="quantity">Quantity:</label>
                <input
                  type="number"
                  id="quantity"
                  v-model.number="reportData.quantity"
                  min="1"
                  required
                />
              </div>
              <div class="form-group">
                <label for="startDate">Start Date:</label>
                <input
                  type="date"
                  id="startDate"
                  v-model="reportData.startDate"
                />
              </div>
              <div class="form-group">
                <label for="endDate">End Date:</label>
                <input type="date" id="endDate" v-model="reportData.endDate" />
              </div>
            </div>
          </div>
        </div>

        <!-- Dimensional Checklist Section -->
        <div class="form-section">
          <h2 class="section-title">Dimensional Checklist</h2>
          <div class="inspection-table-container">
            <table class="inspection-table">
              <thead>
                <tr>
                  <th>SL NO</th>
                  <th>DIMENSION</th>
                  <th>TOLERANCE</th>
                  <th>OBSERVED VALUE</th>
                  <th>INSTRUMENT USED</th>
                  <th>REMARKS</th>
                  <th>UPLOAD</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(item, index) in dimensionalChecklist"
                  :key="'dim-' + index"
                >
                  <td>{{ index + 1 }}</td>
                  <td>
                    <input
                      type="text"
                      v-model="item.dimension"
                      placeholder="Enter dimension"
                    />
                  </td>
                  <td>
                    <input
                      type="text"
                      v-model="item.tolerance"
                      placeholder="Enter tolerance"
                    />
                  </td>
                  <td>
                    <input
                      type="text"
                      v-model="item.observedValue"
                      placeholder="Enter observed value"
                    />
                  </td>
                  <td>
                    <input
                      type="text"
                      v-model="item.instrumentUsed"
                      placeholder="Enter instrument"
                    />
                  </td>
                  <td>
                    <input
                      type="text"
                      v-model="item.remarks"
                      placeholder="Enter remarks"
                    />
                  </td>
                  <td>
                    <input
                      type="file"
                      @change="handleFileUpload($event, item, 'dim')"
                    />
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Parameter Checklist Section -->
        <div class="form-section">
          <h2 class="section-title">Parameter Checklist</h2>
          <div class="inspection-table-container">
            <table class="inspection-table">
              <thead>
                <tr>
                  <th>SL NO</th>
                  <th>CHECK POINTS</th>
                  <th>EXPECTED</th>
                  <th>COMPLIANCE OBSERVATIONS</th>
                  <th>REMARKS (OK / NOT OK)</th>
                  <th>UPLOAD</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(item, index) in parameterChecklist"
                  :key="'param-' + index"
                >
                  <td>{{ index + 1 }}</td>
                  <td>{{ item.parameter }}</td>
                  <td>
                    <input
                      type="text"
                      v-model="item.expected"
                      readonly
                      class="readonly-input"
                    />
                  </td>
                  <td>
                    <input
                      type="text"
                      v-model="item.complianceObservation"
                      placeholder="Enter compliance observations"
                    />
                  </td>
                  <td>
                    <input
                      type="text"
                      v-model="item.remarks"
                      placeholder="Enter remarks (OK/NOT OK)"
                    />
                  </td>
                  <td>
                    <input
                      type="file"
                      @change="handleFileUpload($event, item, 'param')"
                    />
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Signatures Section -->
        <div class="form-section">
          <h2 class="section-title">Signatures</h2>
          <div class="signatures-layout">
            <div class="signature-item">
              <label>Prepared By:</label>
              <div class="signature-line"></div>
            </div>
            <div class="signature-item">
              <label>Verified By:</label>
              <div class="signature-line"></div>
            </div>
            <div class="signature-item">
              <label>Approved By:</label>
              <div class="signature-line"></div>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="form-actions">
          <button type="button" @click="saveDraft" class="btn btn-secondary">
            Save Draft
          </button>
          <button type="button" @click="resetForm" class="btn btn-secondary">
            Reset
          </button>
          <button
            type="submit"
            class="btn btn-primary"
            :disabled="!isFormValid"
          >
            Submit Report
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import jsPDF from "jspdf";

export default {
  name: "MechanicalInspection",
  props: {
    readonly: {
      type: Boolean,
      default: false
    },
    isTemplatePreview: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      currentYear: "2025",
      reportData: {
        projectName: "",
        reportRefNo: "",
        memoRefNo: "",
        lruName: "",
        inspectionStage: "",
        testVenue: "",
        slNos: "",
        dpName: "",
        dated1: "",
        dated2: "",
        sruName: "",
        partNo: "",
        quantity: null,
        startDate: "",
        endDate: "",
      },
      dimensionalChecklist: [
        {
          dimension: "",
          tolerance: "",
          observedValue: "",
          instrumentUsed: "",
          remarks: "",
          fileName: null,
        },
        {
          dimension: "",
          tolerance: "",
          observedValue: "",
          instrumentUsed: "",
          remarks: "",
          fileName: null,
        },
        {
          dimension: "",
          tolerance: "",
          observedValue: "",
          instrumentUsed: "",
          remarks: "",
          fileName: null,
        },
      ],
      parameterChecklist: [
        {
          parameter: "Burrs",
          complianceObservation: "",
          expected: "Not Expected",
          remarks: "",
          fileName: null,
        },
        {
          parameter: "Damages",
          complianceObservation: "",
          expected: "Not Expected",
          remarks: "",
          fileName: null,
        },
        {
          parameter: "Name Plate",
          complianceObservation: "",
          expected: "As per Drawing",
          remarks: "",
          fileName: null,
        },
        {
          parameter: "Engraving",
          complianceObservation: "",
          expected: "As per Drawing",
          remarks: "",
          fileName: null,
        },
        {
          parameter: "Passivation",
          complianceObservation: "",
          expected: "As per Drawing",
          remarks: "",
          fileName: null,
        },
        {
          parameter: "Chromate",
          complianceObservation: "",
          expected: "As per Drawing",
          remarks: "",
          fileName: null,
        },
        {
          parameter: "Electro-less Nickel plating",
          complianceObservation: "",
          expected: "As per Drawing",
          remarks: "",
          fileName: null,
        },
        {
          parameter: "Fasteners",
          complianceObservation: "",
          expected: "As per Drawing",
          remarks: "",
          fileName: null,
        },
      ],
      currentDate: new Date(),
    };
  },
  computed: {
    formattedDate() {
      return this.currentDate.toISOString().split("T")[0];
    },
    isFormValid() {
      return (
        this.reportData.projectName &&
        this.reportData.reportRefNo &&
        this.reportData.lruName &&
        this.reportData.dpName &&
        this.reportData.partNo &&
        this.reportData.quantity
      );
    },
  },
  mounted() {
    // Get parameters from route
    const projectName = this.$route.params.projectName || "";
    const lruName = this.$route.params.lruName || "";

    // Set default values
    this.reportData.projectName = projectName;
    this.reportData.lruName = lruName;
    this.reportData.startDate = this.formattedDate;
  },
  methods: {
    handleFileUpload(event, item, checklistType) {
      const file = event.target.files[0];
      if (file) {
        item.fileName = file.name;
        console.log(`File uploaded for ${checklistType}:`, file.name);
      }
    },
    saveDraft() {
      console.log("Saving draft:", this.reportData);
      alert("Draft saved successfully!");
    },
    resetForm() {
      if (
        confirm(
          "Are you sure you want to reset the form? All data will be lost."
        )
      ) {
        this.reportData = {
          projectName: this.$route.params.projectName || "",
          reportRefNo: "",
          memoRefNo: "",
          lruName: this.$route.params.lruName || "",
          inspectionStage: "",
          testVenue: "",
          slNos: "",
          dpName: "",
          dated1: "",
          dated2: "",
          sruName: "",
          partNo: "",
          quantity: null,
          startDate: this.formattedDate,
          endDate: "",
        };
        // Reset checklists
        this.dimensionalChecklist.forEach((item) => {
          item.dimension = "";
          item.tolerance = "";
          item.observedValue = "";
          item.instrumentUsed = "";
          item.remarks = "";
          item.fileName = null;
        });
        this.parameterChecklist.forEach((item) => {
          item.complianceObservation = "";
          item.expected =
            item.parameter === "Burrs" || item.parameter === "Damages"
              ? "Not Expected"
              : "As per Drawing";
          item.remarks = "";
          item.fileName = null;
        });
      }
    },
    async submitForm() {
      if (!this.isFormValid) {
        alert("Please fill in all required fields.");
        return;
      }

      try {
        // Prepare data for submission
        const submissionData = {
          // Report Details
          project_name: this.reportData.projectName,
          report_ref_no: this.reportData.reportRefNo,
          memo_ref_no: this.reportData.memoRefNo,
          lru_name: this.reportData.lruName,
          inspection_stage: this.reportData.inspectionStage,
          test_venue: this.reportData.testVenue,
          sl_nos: this.reportData.slNos,
          dp_name: this.reportData.dpName,
          dated1: this.reportData.dated1,
          dated2: this.reportData.dated2,
          sru_name: this.reportData.sruName,
          part_no: this.reportData.partNo,
          quantity: this.reportData.quantity || 0,
          start_date: this.reportData.startDate,
          end_date: this.reportData.endDate,

          // Dimensional Checklist
          dim1_dimension: this.dimensionalChecklist[0].dimension,
          dim1_tolerance: this.dimensionalChecklist[0].tolerance,
          dim1_observed_value: this.dimensionalChecklist[0].observedValue,
          dim1_instrument_used: this.dimensionalChecklist[0].instrumentUsed,
          dim1_remarks: this.dimensionalChecklist[0].remarks,
          dim1_upload: this.dimensionalChecklist[0].fileName,

          dim2_dimension: this.dimensionalChecklist[1].dimension,
          dim2_tolerance: this.dimensionalChecklist[1].tolerance,
          dim2_observed_value: this.dimensionalChecklist[1].observedValue,
          dim2_instrument_used: this.dimensionalChecklist[1].instrumentUsed,
          dim2_remarks: this.dimensionalChecklist[1].remarks,
          dim2_upload: this.dimensionalChecklist[1].fileName,

          dim3_dimension: this.dimensionalChecklist[2].dimension,
          dim3_tolerance: this.dimensionalChecklist[2].tolerance,
          dim3_observed_value: this.dimensionalChecklist[2].observedValue,
          dim3_instrument_used: this.dimensionalChecklist[2].instrumentUsed,
          dim3_remarks: this.dimensionalChecklist[2].remarks,
          dim3_upload: this.dimensionalChecklist[2].fileName,

          // Parameter Checklist
          param1_compliance_observation:
            this.parameterChecklist[0].complianceObservation,
          param1_expected: this.parameterChecklist[0].expected,
          param1_remarks: this.parameterChecklist[0].remarks,
          param1_upload: this.parameterChecklist[0].fileName,

          param2_compliance_observation:
            this.parameterChecklist[1].complianceObservation,
          param2_expected: this.parameterChecklist[1].expected,
          param2_remarks: this.parameterChecklist[1].remarks,
          param2_upload: this.parameterChecklist[1].fileName,

          param3_compliance_observation:
            this.parameterChecklist[2].complianceObservation,
          param3_expected: this.parameterChecklist[2].expected,
          param3_remarks: this.parameterChecklist[2].remarks,
          param3_upload: this.parameterChecklist[2].fileName,

          param4_compliance_observation:
            this.parameterChecklist[3].complianceObservation,
          param4_expected: this.parameterChecklist[3].expected,
          param4_remarks: this.parameterChecklist[3].remarks,
          param4_upload: this.parameterChecklist[3].fileName,

          param5_compliance_observation:
            this.parameterChecklist[4].complianceObservation,
          param5_expected: this.parameterChecklist[4].expected,
          param5_remarks: this.parameterChecklist[4].remarks,
          param5_upload: this.parameterChecklist[4].fileName,

          param6_compliance_observation:
            this.parameterChecklist[5].complianceObservation,
          param6_expected: this.parameterChecklist[5].expected,
          param6_remarks: this.parameterChecklist[5].remarks,
          param6_upload: this.parameterChecklist[5].fileName,

          param7_compliance_observation:
            this.parameterChecklist[6].complianceObservation,
          param7_expected: this.parameterChecklist[6].expected,
          param7_remarks: this.parameterChecklist[6].remarks,
          param7_upload: this.parameterChecklist[6].fileName,

          param8_compliance_observation:
            this.parameterChecklist[7].complianceObservation,
          param8_expected: this.parameterChecklist[7].expected,
          param8_remarks: this.parameterChecklist[7].remarks,
          param8_upload: this.parameterChecklist[7].fileName,

          // Signatures
          prepared_by: "",
          verified_by: "",
          approved_by: "",
        };

        console.log("Submitting mechanical inspection report:", submissionData);

        const response = await fetch(
          "http://localhost:5000/api/mechanical-inspection",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(submissionData),
          }
        );

        const result = await response.json();

        if (result.success) {
          alert("Mechanical inspection report submitted successfully!");
          console.log("Report ID:", result.report_id);
          this.resetForm();
        } else {
          alert(`Error: ${result.message}`);
        }
      } catch (error) {
        console.error("Error submitting report:", error);
        alert("Error submitting report. Please try again.");
      }
    },
    exportReport() {
      console.log("Exporting report...");
      // TODO: Implement PDF export functionality
      alert("Export functionality will be implemented soon!");
    },
  },
};
</script>

<style scoped>
.mechanical-inspection-page {
  min-height: 100vh;
  background-color: #f5f5f5;
  font-family: "Arial", sans-serif;
}

.page-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.back-button {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  padding: 0.5rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.back-button:hover {
  background: rgba(255, 255, 255, 0.3);
}

.header-center {
  flex: 1;
  text-align: center;
}

.page-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin: 0;
}

.header-right {
  display: flex;
  align-items: center;
}

.export-button {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.export-button:hover {
  background: rgba(255, 255, 255, 0.3);
}

.main-content {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.form-header {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.document-path {
  font-weight: bold;
  color: #333;
}

.report-date {
  color: #666;
}

.subject-line {
  background: white;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
  font-weight: bold;
  color: #333;
}

.inspection-form {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-section {
  margin-bottom: 2rem;
}

.section-title {
  color: #333;
  border-bottom: 2px solid #667eea;
  padding-bottom: 0.5rem;
  margin-bottom: 1.5rem;
}

.general-info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.info-column {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: bold;
  color: #333;
}

.form-group input {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
}

.inspection-table-container {
  overflow-x: auto;
  margin-top: 1rem;
}

.inspection-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}

.inspection-table th,
.inspection-table td {
  border: 1px solid #ddd;
  padding: 0.75rem;
  text-align: left;
}

.inspection-table th {
  background: #f8f9fa;
  font-weight: bold;
  color: #333;
}

.inspection-table input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.readonly-input {
  background: #f8f9fa;
  color: #666;
}

.signatures-layout {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin-top: 1rem;
}

.signature-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.signature-item label {
  font-weight: bold;
  color: #333;
}

.signature-line {
  height: 2px;
  background: #333;
  margin-top: 2rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #ddd;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.btn-primary {
  background: #667eea;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #5a6fd8;
}

.btn-primary:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
}
</style>
