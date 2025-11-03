<template>
  <div class="kit-inspection-page">
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
        <div class="report-date">Date: {{ currentDate }}</div>
      </div>

      <div class="subject-line">
        SUB : Kit of Part Inspection Report for {{ reportData.lruName }}
      </div>

      <!-- Inspection Form -->
      <form @submit.prevent="handleSubmit" class="inspection-form">
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
                  :disabled="readonly"
                  required
                />
              </div>
              <div class="form-group">
                <label for="reportRefNo">Report Ref No:</label>
                <input
                  type="text"
                  id="reportRefNo"
                  v-model="reportData.reportRefNo"
                  :disabled="readonly"
                  required
                />
              </div>
              <div class="form-group">
                <label for="memoRefNo">Memo Ref No:</label>
                <input
                  type="text"
                  id="memoRefNo"
                  v-model="reportData.memoRefNo"
                  :disabled="readonly"
                />
              </div>
              <div class="form-group">
                <label for="lruName">LRU Name:</label>
                <input
                  type="text"
                  id="lruName"
                  v-model="reportData.lruName"
                  :disabled="readonly"
                  required
                />
              </div>
              <div class="form-group">
                <label for="inspectionStage">Inspection Stage:</label>
                <input
                  type="text"
                  id="inspectionStage"
                  v-model="reportData.inspectionStage"
                  :disabled="readonly"
                />
              </div>
              <div class="form-group">
                <label for="testVenue">Test Venue:</label>
                <input
                  type="text"
                  id="testVenue"
                  v-model="reportData.testVenue"
                  :disabled="readonly"
                />
              </div>
              <div class="form-group">
                <label for="slNos">SL.NO'S:</label>
                <input type="text" id="slNos" v-model="reportData.slNos" :disabled="readonly" />
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
                  :disabled="readonly"
                  required
                />
              </div>
              <div class="form-group">
                <label for="dated1">Dated:</label>
                <input type="date" id="dated1" v-model="reportData.dated1" :disabled="readonly" />
              </div>
              <div class="form-group">
                <label for="dated2">Dated:</label>
                <input type="date" id="dated2" v-model="reportData.dated2" :disabled="readonly" />
              </div>
              <div class="form-group">
                <label for="sruName">SRU Name:</label>
                <input type="text" id="sruName" v-model="reportData.sruName" :disabled="readonly" />
              </div>
              <div class="form-group">
                <label for="partNo">Part No:</label>
                <input
                  type="text"
                  id="partNo"
                  v-model="reportData.partNo"
                  :disabled="readonly"
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
                  :disabled="readonly"
                />
              </div>
              <div class="form-group">
                <label for="endDate">End Date:</label>
                <input type="date" id="endDate" v-model="reportData.endDate" :disabled="readonly" />
              </div>
            </div>
          </div>
        </div>

        <!-- Inspection Results Section -->
        <div class="form-section">
          <h2 class="section-title">Inspection Results</h2>
          <div class="inspection-table-container">
            <table class="inspection-table">
              <thead>
                <tr>
                  <th>SL NO</th>
                  <th>TEST CASES</th>
                  <th>EXPECTED</th>
                  <th>OBSERVATIONS</th>
                  <th>REMARKS (OK/NOT OK)</th>
                  <th>UPLOAD</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in reportData.inspectionItems" :key="item.slNo">
                  <td>{{ item.slNo }}</td>
                  <td>{{ item.testCase }}</td>
                  <td>{{ item.expected }}</td>
                  <td>
                    <select
                      :disabled="readonly"
                      v-model="item.observations"
                      @change="onObservationChange(item)"
                    >
                      <option value="">Select</option>
                      <option
                        v-for="opt in getObservationOptions(item.slNo)"
                        :key="opt"
                        :value="opt"
                      >
                        {{ opt }}
                      </option>
                    </select>
                  </td>
                  <td>
                    <!-- Remarks are auto-filled and not editable -->
                    <input type="text" :value="item.remarks" disabled />
                  </td>
                  <td>
                    <input
                      type="file"
                      @change="handleFileUpload($event, item)"
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
              <label>Prepared By (QA G1 -Team):</label>
              <div class="signature-line"></div>
            </div>
            <div class="signature-item">
              <label>Verified By (G1H - QA G):</label>
              <div class="signature-line"></div>
            </div>
            <div class="signature-item">
              <label>Approved By:</label>
              <div class="signature-line"></div>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="form-actions" v-if="!readonly">
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
  name: "KitOfPartInsp",
  props: {
    readonly: {
      type: Boolean,
      default: false,
    },
    isTemplatePreview: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      currentYear: "2025",
      currentDate: new Date().toISOString().split("T")[0],
      reportData: {
        // Header fields
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

        // Table data
        inspectionItems: [
          {
            slNo: 1,
            testCase: "Any observation pending from previous KOP stage",
            expected: "NIL",
            observations: "",
            remarks: "",
            fileName: null,
          },
          {
            slNo: 2,
            testCase: "CoC verification of components",
            expected: "Verified",
            observations: "",
            remarks: "",
            fileName: null,
          },
          {
            slNo: 3,
            testCase: "Quantity as BOM",
            expected: "Matching",
            observations: "",
            remarks: "",
            fileName: null,
          },
          {
            slNo: 4,
            testCase: "Quantity as per number of boards to be assembled",
            expected: "Matching",
            observations: "",
            remarks: "",
            fileName: null,
          },
          {
            slNo: 5,
            testCase: "Components storage in ESD cover",
            expected: "Yes",
            observations: "",
            remarks: "",
            fileName: null,
          },
          {
            slNo: 6,
            testCase: "All connectors to be fitted with screws before assembly",
            expected: "Yes",
            observations: "",
            remarks: "",
            fileName: null,
          },
          {
            slNo: 7,
            testCase: "Any other observations",
            expected: "NIL",
            observations: "",
            remarks: "",
            fileName: null,
          },
        ],

        // Footer/Signature fields
        preparedBy: "",
        verifiedBy: "",
        approvedBy: "",
      },
    };
  },
  computed: {
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
    this.reportData.startDate = this.currentDate;
    // Compute initial remarks if observations already present
    this.reportData.inspectionItems.forEach((item) => {
      if (item.observations) {
        this.computeRemarkForItem(item);
      }
    });
  },
  methods: {
    handleFileUpload(event, item) {
      const file = event.target.files[0];
      if (file) {
        item.fileName = file.name;
        console.log(`File for item ${item.slNo}: ${file.name}`);
      } else {
        item.fileName = null;
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
          startDate: this.currentDate,
          endDate: "",
          inspectionItems: [
            {
              slNo: 1,
              testCase: "Any observation pending from previous KOP stage",
              expected: "NIL",
              observations: "",
              remarks: "",
              fileName: null,
            },
            {
              slNo: 2,
              testCase: "CoC verification of components",
              expected: "Verified",
              observations: "",
              remarks: "",
              fileName: null,
            },
            {
              slNo: 3,
              testCase: "Quantity as BOM",
              expected: "Matching",
              observations: "",
              remarks: "",
              fileName: null,
            },
            {
              slNo: 4,
              testCase: "Quantity as per number of boards to be assembled",
              expected: "Matching",
              observations: "",
              remarks: "",
              fileName: null,
            },
            {
              slNo: 5,
              testCase: "Components storage in ESD cover",
              expected: "Stored in ESD",
              observations: "",
              remarks: "",
              fileName: null,
            },
            {
              slNo: 6,
              testCase:
                "All connectors to be fitted with screws before assembly",
              expected: "Fitted properly",
              observations: "",
              remarks: "",
              fileName: null,
            },
            {
              slNo: 7,
              testCase: "Any other observations",
              expected: "NIL",
              observations: "",
              remarks: "",
              fileName: null,
            },
          ],
          preparedBy: "",
          verifiedBy: "",
          approvedBy: "",
        };
      }
    },
    async handleSubmit() {
      if (!this.isFormValid) {
        alert("Please fill in all required fields.");
        return;
      }

      try {
        // Prepare data for submission
        const submissionData = {
          // Report Details
          projectName: this.reportData.projectName,
          reportRefNo: this.reportData.reportRefNo,
          memoRefNo: this.reportData.memoRefNo,
          lruName: this.reportData.lruName,
          inspectionStage: this.reportData.inspectionStage,
          testVenue: this.reportData.testVenue,
          slNos: this.reportData.slNos,
          dpName: this.reportData.dpName,
          dated1: this.reportData.dated1,
          dated2: this.reportData.dated2,
          sruName: this.reportData.sruName,
          partNo: this.reportData.partNo,
          quantity: this.reportData.quantity || 0,
          startDate: this.reportData.startDate,
          endDate: this.reportData.endDate,

          // Test Cases
          test1Observations: this.reportData.inspectionItems[0].observations,
          test1Remarks: this.reportData.inspectionItems[0].remarks,
          test1Upload: this.reportData.inspectionItems[0].fileName,

          test2Observations: this.reportData.inspectionItems[1].observations,
          test2Remarks: this.reportData.inspectionItems[1].remarks,
          test2Upload: this.reportData.inspectionItems[1].fileName,

          test3Observations: this.reportData.inspectionItems[2].observations,
          test3Remarks: this.reportData.inspectionItems[2].remarks,
          test3Upload: this.reportData.inspectionItems[2].fileName,

          test4Observations: this.reportData.inspectionItems[3].observations,
          test4Remarks: this.reportData.inspectionItems[3].remarks,
          test4Upload: this.reportData.inspectionItems[3].fileName,

          test5Observations: this.reportData.inspectionItems[4].observations,
          test5Remarks: this.reportData.inspectionItems[4].remarks,
          test5Upload: this.reportData.inspectionItems[4].fileName,

          test6Observations: this.reportData.inspectionItems[5].observations,
          test6Remarks: this.reportData.inspectionItems[5].remarks,
          test6Upload: this.reportData.inspectionItems[5].fileName,

          test7Observations: this.reportData.inspectionItems[6].observations,
          test7Remarks: this.reportData.inspectionItems[6].remarks,
          test7Upload: this.reportData.inspectionItems[6].fileName,

          // Signatures
          preparedBy: this.reportData.preparedBy,
          verifiedBy: this.reportData.verifiedBy,
          approvedBy: this.reportData.approvedBy,
        };

        console.log(
          "Submitting kit of parts inspection report:",
          submissionData
        );

        const response = await fetch("http://localhost:5000/api/kit-of-parts", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(submissionData),
        });

        const result = await response.json();

        if (result.success) {
          alert("Kit of parts inspection report submitted successfully!");
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
    getObservationOptions(slNo) {
      // Return options based on slNo
      switch (slNo) {
        case 1:
          return ["Nil", "Present"];
        case 2:
          return ["Verified", "Not Verified"];
        case 3:
          return ["Matching", "Not Matching"];
        case 4:
          return ["Matching", "Not Matching"];
        case 5:
          return ["Yes", "No"];
        case 6:
          return ["Yes", "No"];
        case 7:
          return ["Nil", "Yes"];
        default:
          return ["Nil", "Present"];
      }
    },
    onObservationChange(item) {
      // When observation changes, compute remark automatically
      this.computeRemarkForItem(item);
    },
    computeRemarkForItem(item) {
      const expectedNormalized = this.normalizeExpectedForItem(item).toLowerCase();
      const obs = (item.observations || "").toString().trim().toLowerCase();
      if (!obs) {
        item.remarks = "";
        return;
      }
      if (expectedNormalized === obs) {
        item.remarks = "Passed";
      } else {
        item.remarks = "Failed";
      }
    },
    normalizeExpectedForItem(item) {
      // Map expected values to comparable observation values
      const e = (item.expected || "").toString().toLowerCase();
      switch (item.slNo) {
        case 1:
          return e.includes("nil") ? "Nil" : e;
        case 2:
          return e.includes("verif") ? "Verified" : e;
        case 3:
          return e.includes("match") ? "Matching" : e;
        case 4:
          return e.includes("match") ? "Matching" : e;
        case 5:
          // Expected 'Stored in ESD' -> treat as Yes
          return e.includes("stored") || e.includes("yes") ? "Yes" : e;
        case 6:
          // Expected 'Fitted properly' -> treat as Yes
          return e.includes("fitt") || e.includes("yes") ? "Yes" : e;
        case 7:
          return e.includes("nil") ? "Nil" : e;
        default:
          return item.expected || "";
      }
    },
    exportReport() {
      try {
        const doc = new jsPDF("p", "mm", "a4");
        const pageWidth = doc.internal.pageSize.getWidth();
        const pageHeight = doc.internal.pageSize.getHeight();
        const margin = 20;

        let yPosition = margin;

        // Set font styles
        doc.setFont("helvetica");

        // Header
        doc.setFontSize(18);
        doc.setFont("helvetica", "bold");
        doc.text("KIT OF PART INSPECTION REPORT", pageWidth / 2, yPosition, {
          align: "center",
        });
        yPosition += 15;

        // Document path and date
        doc.setFontSize(10);
        doc.setFont("helvetica", "normal");
        const documentPath = `CASDIC/${
          this.reportData.projectName || "PROJECT"
        }/${this.reportData.lruName || "LRU"}/SL.${
          this.reportData.slNos || "001"
        }/${this.reportData.reportRefNo || "001"}/${this.currentYear}`;
        doc.text(documentPath, margin, yPosition);

        const dateText = `Date: ${this.currentDate}`;
        const dateWidth = doc.getTextWidth(dateText);
        doc.text(dateText, pageWidth - margin - dateWidth, yPosition);
        yPosition += 12;

        // Subject line
        doc.setFontSize(12);
        doc.setFont("helvetica", "bold");
        const subjectText = `SUB: Kit of Part Inspection Report for ${
          this.reportData.lruName || "Unknown LRU"
        }`;
        doc.text(subjectText, pageWidth / 2, yPosition, { align: "center" });
        yPosition += 15;

        // Save PDF
        const fileName = `Kit_of_Part_Inspection_Report_${
          this.reportData.lruName || "Unknown"
        }_${this.currentDate.replace(/\//g, "-")}.pdf`;
        doc.save(fileName);

        alert("Report exported successfully as PDF!");
      } catch (error) {
        console.error("Error exporting PDF:", error);
        alert(
          `Error exporting PDF: ${
            error.message || "Unknown error"
          }. Please try again.`
        );
      }
    },
  },
};
</script>

<style scoped>
.kit-inspection-page {
  min-height: 100vh;
  background: #f5f5f5;
}

/* Header */
.page-header {
  background: #2d3748;
  padding: 20px 30px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 15px;
}

.back-button {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  cursor: pointer;
  padding: 10px;
  border-radius: 50%;
  transition: all 0.3s ease;
  color: white;
}

.back-button:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.05);
}

.app-logo {
  width: 120px;
  height: auto;
  filter: brightness(0) invert(1);
}

.header-center {
  flex: 1;
  text-align: center;
}

.page-title {
  color: white;
  font-size: 2.2em;
  font-weight: 700;
  margin: 0;
  letter-spacing: 2px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.header-right {
  display: flex;
  align-items: center;
}

.export-button {
  background: rgba(255, 255, 255, 0.95);
  border: none;
  border-radius: 25px;
  padding: 12px 20px;
  font-weight: 600;
  color: #4a5568;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.export-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  background: white;
}

/* Main Content */
.main-content {
  max-width: 1200px;
  margin: 30px auto;
  padding: 0 30px;
}

/* Form Header */
.form-header {
  background: white;
  padding: 25px;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 25px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.document-path {
  font-family: "Courier New", monospace;
  color: #4a5568;
  font-size: 0.9em;
  background: #f7fafc;
  padding: 10px 15px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.report-date {
  color: #4a5568;
  font-weight: 600;
}

.subject-line {
  font-size: 1.2em;
  font-weight: bold;
  color: #333;
  margin: 20px 0;
  padding: 15px;
  background-color: #f8f9fa;
  border-left: 4px solid #6c757d;
  border-radius: 4px;
}

/* Form Sections */
.inspection-form {
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.form-section {
  padding: 30px;
  border-bottom: 1px solid #e2e8f0;
}

.form-section:last-child {
  border-bottom: none;
}

.section-title {
  color: #2d3748;
  border-bottom: 3px solid #4a5568;
  padding-bottom: 15px;
  margin-bottom: 25px;
  font-size: 1.5em;
  font-weight: 600;
}

/* General Info Grid */
.general-info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}

.info-column {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-weight: 600;
  color: #4a5568;
  font-size: 0.9em;
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 12px 15px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.9em;
  transition: all 0.3s ease;
  background: white;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #4a5568;
  box-shadow: 0 0 0 3px rgba(74, 85, 104, 0.1);
}

/* Inspection Table */
.inspection-table-container {
  margin-top: 20px;
  overflow-x: auto;
}

.inspection-table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
  font-size: 0.9em;
}

.inspection-table th {
  background: #2d3748;
  color: white;
  padding: 12px 8px;
  text-align: left;
  font-weight: 600;
  font-size: 0.85em;
}

.inspection-table td {
  padding: 8px;
  border-bottom: 1px solid #e2e8f0;
  vertical-align: top;
}

.inspection-table tr:nth-child(even) {
  background-color: #f8fafc;
}

.inspection-table input[type="text"],
.inspection-table select,
.inspection-table textarea {
  width: 100%;
  padding: 6px;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  font-size: 0.85em;
}

.inspection-table input[type="file"] {
  font-size: 0.8em;
  padding: 4px;
}

/* Signatures */
.signatures-layout {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-top: 30px;
  padding: 20px 0;
}

.signature-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  flex: 1;
  max-width: 200px;
}

.signature-item label {
  font-weight: 600;
  color: #4a5568;
  font-size: 1em;
  margin-bottom: 5px;
}

.signature-line {
  width: 100%;
  height: 40px;
  border-bottom: 1px solid #333;
  margin-top: 10px;
}

/* Form Actions */
.form-actions {
  padding: 30px;
  background: #f8fafc;
  display: flex;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  font-size: 0.9em;
}

.btn-primary {
  background-color: #2d3748;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #1a202c;
  transform: translateY(-1px);
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background-color: #5a6268;
  transform: translateY(-1px);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* Responsive Design */
@media (max-width: 768px) {
  .page-header {
    padding: 15px 20px;
    flex-direction: column;
    gap: 15px;
  }

  .page-title {
    font-size: 1.8em;
  }

  .main-content {
    padding: 0 20px;
    margin: 20px auto;
  }

  .general-info-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .signatures-layout {
    flex-direction: column;
    align-items: center;
    gap: 20px;
  }

  .signature-item {
    max-width: 100%;
  }

  .form-actions {
    flex-direction: column;
    align-items: center;
  }

  .inspection-table-container {
    overflow-x: auto;
  }

  .inspection-table {
    min-width: 800px;
  }
}
</style>
