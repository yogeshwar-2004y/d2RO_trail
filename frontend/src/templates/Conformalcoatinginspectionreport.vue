<template>
  <div class="conformal-coating-inspection-page">
    <!-- Header -->
    <div class="page-header">
      <div class="header-left">
        <button class="back-button" @click="$router.go(-1)">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M19 12H5"></path>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
        </button>
        <div class="logos-container">
          <img
            src="@/assets/images/aviatrax-logo.png"
            alt="Aviatrax Logo"
            class="app-logo"
          />
          <img
            src="@/assets/images/vista_logo.png"
            alt="Vista Logo"
            class="app-logo vista-logo"
          />
        </div>
      </div>
      <div class="header-center">
        <h1 class="page-title">CONFORMAL COATING INSPECTION REPORT</h1>
      </div>
      <div class="header-right">
        <button class="export-button" @click="exportReport">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="7,10 12,15 17,10"></polyline>
            <line x1="12" y1="15" x2="12" y2="3"></line>
          </svg>
          EXPORT
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Form Header -->
      <div class="form-header">
        <div class="document-path">
          CASDIC/{{ projectName }}/{{ lruName }}/SL.{{ serialNumber }}/{{
            inspectionCount
          }}/{{ currentYear }}
        </div>
        <div class="report-date">Date: {{ currentDate }}</div>
      </div>

      <div class="subject-line">
        SUB : Conformal Coating Inspection Report for {{ lruName }}
      </div>

      <!-- Inspection Form -->
      <form @submit.prevent="submitForm" class="inspection-form">
        <div class="report-container">
          <div class="report-info">
            <div>
              <strong>Project Name:</strong>
              <input v-model="projectName" type="text" />
            </div>
            <div>
              <strong>Report Ref No:</strong>
              <input v-model="reportRefNo" type="text" />
            </div>
            <div>
              <strong>DP Name:</strong> <input v-model="dpName" type="text" />
            </div>
            <div>
              <strong>Part No:</strong> <input v-model="partNo" type="text" />
            </div>
            <div>
              <strong>SL No’s:</strong> <input v-model="slNo" type="text" />
            </div>
            <div>
              <strong>End Date:</strong> <input v-model="endDate" type="date" />
            </div>
            <div>
              <strong>SRU Name:</strong> <input v-model="sruName" type="text" />
            </div>
            <div>
              <strong>Start Date:</strong>
              <input v-model="startDate" type="date" />
            </div>
            <div>
              <strong>Inspection Stage:</strong>
              <input v-model="inspectionStage" type="text" />
            </div>
            <div>
              <strong>Test Venue:</strong>
              <input v-model="testVenue" type="text" />
            </div>
          </div>

          <table class="inspection-table">
            <thead>
              <tr>
                <th>SL.NO</th>
                <th>TEST CASES</th>
                <th>EXPECTED</th>
                <th>OBSERVATIONS</th>
                <th>REMARKS (OK/NOT OK)</th>
                <th>UPLOAD</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(test, index) in tests" :key="index">
                <td>{{ index + 1 }}</td>
                <td>{{ test.case }}</td>
                <td>{{ test.expected }}</td>
                <td><input v-model="test.observation" type="text" /></td>
                <td><input v-model="test.remark" type="text" /></td>
                <td><input type="file" /></td>
              </tr>
            </tbody>
          </table>

          <div class="report-footer">
            <div>
              <strong>Prepared By:</strong>
              <input v-model="preparedBy" type="text" />
            </div>
            <div>
              <strong>Verified By:</strong>
              <input v-model="verifiedBy" type="text" />
            </div>
            <div>
              <strong>Approved By:</strong>
              <input v-model="approvedBy" type="text" />
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
  name: "Conformalcoatinginspectionreport",
  data() {
    return {
      projectName: "",
      lruName: "",
      serialNumber: "SL-001",
      inspectionCount: "INS-001",
      currentYear: "2025",
      currentDate: new Date().toISOString().split("T")[0],
      reportRefNo: "",
      dpName: "",
      partNo: "",
      slNo: "",
      endDate: "",
      sruName: "",
      startDate: "",
      inspectionStage: "",
      testVenue: "",
      preparedBy: "",
      verifiedBy: "",
      approvedBy: "",
      overallStatus: "",
      qualityRating: null,
      recommendations: "",
      memoRefNo: "",
      quantity: null,
      dated1: "",
      dated2: "",

      // Test cases remain to define the report structure
      tests: [
        {
          case: "Uncoated patches",
          expected: "Should not be there",
          observation: "",
          remark: "",
        },
        {
          case: "Entrapped air bubbles",
          expected: "Should not be there",
          observation: "",
          remark: "",
        },
        {
          case: "Enclosed foreign particles in the coat",
          expected: "Should not be there",
          observation: "",
          remark: "",
        },
        {
          case: "Residue of masking material",
          expected: "Should not be there",
          observation: "",
          remark: "",
        },
        {
          case: "Discoloration",
          expected: "No recommended",
          observation: "",
          remark: "",
        },
        { case: "Cracks", expected: "No Crimony", observation: "", remark: "" },
        {
          case: "Pin holes and Soft spots",
          expected: "No Damages",
          observation: "",
          remark: "",
        },
        {
          case: "Connectors surrounding and beneath",
          expected: "Should have linear coating",
          observation: "",
          remark: "",
        },
        {
          case: "Conformal coating thickness of 30 to 130 microns for acrylic material as per IPC-CC-830B",
          expected: "30 to 130 microns",
          observation: "",
          remark: "",
        },
      ],
    };
  },
  computed: {
    isFormValid() {
      return (
        this.projectName &&
        this.reportRefNo &&
        this.dpName &&
        this.partNo &&
        this.slNo &&
        this.sruName &&
        this.preparedBy &&
        this.verifiedBy &&
        this.approvedBy
      );
    },
  },
  mounted() {
    // Get parameters from route
    this.lruName = this.$route.params.lruName || "";
    this.projectName = this.$route.params.projectName || "";

    // Set default values
    this.sruName = this.lruName;
    this.projectName = this.projectName;
    this.startDate = this.currentDate;
  },
  methods: {
    async saveDraft() {
      try {
        const reportData = this.prepareReportData();
        const response = await fetch(
          "http://localhost:8000/api/reports/conformal-coating-inspection",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(reportData),
          }
        );

        const result = await response.json();

        if (result.success) {
          alert("Draft saved successfully!");
          console.log("Report saved with ID:", result.report_id);
        } else {
          alert(`Error saving draft: ${result.message}`);
        }
      } catch (error) {
        console.error("Error saving draft:", error);
        alert("Error saving draft. Please try again.");
      }
    },
    resetForm() {
      if (
        confirm(
          "Are you sure you want to reset the form? All data will be lost."
        )
      ) {
        this.projectName = this.$route.params.projectName || "";
        this.lruName = this.$route.params.lruName || "";
        this.reportRefNo = "";
        this.dpName = "";
        this.partNo = "";
        this.slNo = "";
        this.endDate = "";
        this.sruName = this.lruName;
        this.startDate = this.currentDate;
        this.inspectionStage = "";
        this.testVenue = "";
        this.preparedBy = "";
        this.verifiedBy = "";
        this.approvedBy = "";

        // Reset test observations and remarks
        this.tests.forEach((test) => {
          test.observation = "";
          test.remark = "";
        });
      }
    },
    async submitForm() {
      if (this.isFormValid) {
        try {
          const reportData = this.prepareReportData();
          const response = await fetch(
            "http://localhost:8000/api/reports/conformal-coating-inspection",
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify(reportData),
            }
          );

          const result = await response.json();

          if (result.success) {
            alert("Report submitted successfully!");
            console.log("Report submitted with ID:", result.report_id);
            // Optionally redirect or reset form
            this.resetForm();
          } else {
            alert(`Error submitting report: ${result.message}`);
          }
        } catch (error) {
          console.error("Error submitting report:", error);
          alert("Error submitting report. Please try again.");
        }
      } else {
        alert("Please fill in all required fields.");
      }
    },
    prepareReportData() {
      return {
        project_name: this.projectName,
        report_ref_no: this.reportRefNo,
        memo_ref_no: this.memoRefNo || "",
        lru_name: this.lruName,
        sru_name: this.sruName,
        dp_name: this.dpName,
        part_no: this.partNo,
        inspection_stage: this.inspectionStage,
        test_venue: this.testVenue,
        quantity: this.quantity || null,
        sl_nos: this.slNo,
        serial_number: this.serialNumber,
        start_date: this.startDate,
        end_date: this.endDate,
        dated1: this.dated1 || null,
        dated2: this.dated2 || null,
        tests: this.tests.map((test) => ({
          observation: test.observation,
          remark: test.remark,
          upload: test.upload || "",
          expected: test.expected,
        })),
        overall_status: this.overallStatus || "",
        quality_rating: this.qualityRating || null,
        recommendations: this.recommendations || "",
        prepared_by: this.preparedBy,
        verified_by: this.verifiedBy,
        approved_by: this.approvedBy,
      };
    },
    exportReport() {
      try {
        const doc = new jsPDF("p", "mm", "a4");
        const pageWidth = doc.internal.pageSize.getWidth();
        const pageHeight = doc.internal.pageSize.getHeight();
        const margin = 20;
        const contentWidth = pageWidth - 2 * margin;

        let yPosition = margin;

        // Set font styles
        doc.setFont("helvetica");

        // Header
        doc.setFontSize(18);
        doc.setFont("helvetica", "bold");
        doc.text(
          "CONFORMAL COATING INSPECTION REPORT",
          pageWidth / 2,
          yPosition,
          { align: "center" }
        );
        yPosition += 15;

        // Document path and date
        doc.setFontSize(10);
        doc.setFont("helvetica", "normal");
        const documentPath = `CASDIC/${this.projectName || "PROJECT"}/${
          this.lruName || "LRU"
        }/SL.${this.serialNumber || "001"}/${this.inspectionCount || "001"}/${
          this.currentYear || "2025"
        }`;
        doc.text(documentPath, margin, yPosition);

        const dateText = `Date: ${
          this.currentDate || new Date().toLocaleDateString("en-GB")
        }`;
        const dateWidth = doc.getTextWidth(dateText);
        doc.text(dateText, pageWidth - margin - dateWidth, yPosition);
        yPosition += 12;

        // Subject line
        doc.setFontSize(12);
        doc.setFont("helvetica", "bold");
        const subjectText = `SUB: Conformal Coating Inspection Report for ${
          this.lruName || "Unknown LRU"
        }`;
        doc.text(subjectText, pageWidth / 2, yPosition, { align: "center" });
        yPosition += 15;

        // Report details
        doc.setFontSize(10);
        doc.setFont("helvetica", "bold");
        doc.text("Report Details:", margin, yPosition);
        yPosition += 8;

        doc.setFont("helvetica", "normal");
        const details = [
          `Project Name: ${this.projectName || "Not specified"}`,
          `Report Ref No: ${this.reportRefNo || "Not specified"}`,
          `DP Name: ${this.dpName || "Not specified"}`,
          `Part No: ${this.partNo || "Not specified"}`,
          `SL No: ${this.slNo || "Not specified"}`,
          `SRU Name: ${this.sruName || "Not specified"}`,
          `Start Date: ${this.startDate || "Not specified"}`,
          `End Date: ${this.endDate || "Not specified"}`,
          `Inspection Stage: ${this.inspectionStage || "Not specified"}`,
          `Test Venue: ${this.testVenue || "Not specified"}`,
        ];

        details.forEach((detail) => {
          doc.text(detail, margin, yPosition);
          yPosition += 6;
        });

        yPosition += 10;

        // Test results table
        doc.setFont("helvetica", "bold");
        doc.text("Test Results:", margin, yPosition);
        yPosition += 8;

        if (this.tests && this.tests.length > 0) {
          doc.setFontSize(9);
          doc.setFont("helvetica", "bold");

          // Table headers
          doc.text("SL.NO", margin, yPosition);
          doc.text("TEST CASES", margin + 20, yPosition);
          doc.text("EXPECTED", margin + 80, yPosition);
          doc.text("OBSERVATIONS", margin + 120, yPosition);
          doc.text("REMARKS", margin + 160, yPosition);
          yPosition += 6;

          // Table data
          doc.setFont("helvetica", "normal");
          this.tests.forEach((test, index) => {
            doc.text((index + 1).toString(), margin, yPosition);
            doc.text(test.case.substring(0, 25), margin + 20, yPosition);
            doc.text(test.expected.substring(0, 15), margin + 80, yPosition);
            doc.text(
              test.observation.substring(0, 20),
              margin + 120,
              yPosition
            );
            doc.text(test.remark.substring(0, 15), margin + 160, yPosition);
            yPosition += 6;
          });
        }

        yPosition += 15;

        // Signatures
        doc.setFont("helvetica", "bold");
        doc.text("Signatures:", margin, yPosition);
        yPosition += 8;

        doc.setFont("helvetica", "normal");
        doc.text(
          `Prepared By: ${this.preparedBy || "Not specified"}`,
          margin,
          yPosition
        );
        yPosition += 6;
        doc.text(
          `Verified By: ${this.verifiedBy || "Not specified"}`,
          margin,
          yPosition
        );
        yPosition += 6;
        doc.text(
          `Approved By: ${this.approvedBy || "Not specified"}`,
          margin,
          yPosition
        );

        // Save PDF
        const fileName = `Conformal_Coating_Inspection_Report_${
          this.lruName || "Unknown"
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
.conformal-coating-inspection-page {
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

/* Inspection Form */
.inspection-form {
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.report-container {
  max-width: 1200px;
  margin: auto;
  font-family: Arial, sans-serif;
  padding: 20px;
  background: #fff;
}

.report-header-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
  background: #f0f2f5;
  border-radius: 10px;
  border: 1px solid #ddd;
}

.report-header-table td {
  padding: 10px;
  vertical-align: middle;
  text-align: center;
}

.header-logo-cell {
  width: 15%;
  background: #e5e7eb;
}

.header-title-cell {
  width: 70%;
  background: #f0f2f5;
  color: #333;
}

.report-header-table h1 {
  font-size: 22px;
  font-weight: bold;
  margin: 0;
  color: #333;
}

.logo {
  height: 40px;
  width: 80px;
  object-fit: contain;
  background: transparent;
  border-radius: 5px;
}

.report-info {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 20px;
  padding: 10px 0;
  border-bottom: 1px solid #eee;
}

.report-info strong {
  display: inline-block;
  min-width: 100px; /* Aligns the labels */
}

.report-info input[type="text"],
.report-info input[type="date"] {
  border: none;
  border-bottom: 1px solid #ccc;
  padding: 3px 5px;
  width: 70%;
  background-color: transparent;
}

.inspection-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

.inspection-table th,
.inspection-table td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
}

.inspection-table th {
  background: #f3f4f6;
  font-size: 14px;
  color: #333;
}

.inspection-table input[type="text"] {
  width: 95%;
  border: 1px solid #e0e0e0;
  padding: 5px;
  box-sizing: border-box;
}

.inspection-table input[type="file"] {
  font-size: 12px;
}

.report-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 30px;
  padding-top: 15px;
  border-top: 1px dashed #ccc;
}

.report-footer div {
  flex-basis: 30%;
  text-align: center;
  font-size: 14px;
}

.report-footer input[type="text"] {
  border: none;
  border-bottom: 1px solid #000;
  width: 90%;
  margin-top: 10px;
  padding: 5px;
  background-color: transparent;
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

  .form-actions {
    flex-direction: column;
    align-items: center;
  }

  .inspection-table {
    overflow-x: auto;
  }

  .inspection-table table {
    min-width: 600px;
  }
}
</style>
