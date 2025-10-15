<template>
  <div class="cots-screening-inspection-page">
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
        SUB : COTS Screening Inspection Report for {{ lruName }}
      </div>

      <!-- Inspection Form -->
      <form @submit.prevent="submitForm" class="inspection-form">
        <!-- Header Section -->
        <div class="form-section">
          <div class="header-info-grid">
            <div class="form-group">
              <label for="projectName">Project Name:</label>
              <input
                type="text"
                id="projectName"
                v-model="formData.projectName"
                required
              />
            </div>
            <div class="form-group">
              <label for="dpName">DP Name:</label>
              <input
                type="text"
                id="dpName"
                v-model="formData.dpName"
                required
              />
            </div>
          </div>
        </div>

        <!-- Report Details Section -->
        <div class="form-section">
          <h2 class="section-title">Report Details</h2>
          <div class="report-details-grid">
            <!-- Left Column -->
            <div class="details-column">
              <div class="form-group">
                <label for="reportRefNo">Report Ref No:</label>
                <input
                  type="text"
                  id="reportRefNo"
                  v-model="formData.reportRefNo"
                  required
                />
              </div>
              <div class="form-group">
                <label for="memoRefNo">Memo Ref No:</label>
                <input
                  type="text"
                  id="memoRefNo"
                  v-model="formData.memoRefNo"
                  required
                />
              </div>
              <div class="form-group">
                <label for="lruName">LRU Name:</label>
                <input
                  type="text"
                  id="lruName"
                  v-model="formData.lruName"
                  required
                />
              </div>
              <div class="form-group">
                <label for="inspectionStage">Inspection Stage:</label>
                <input
                  type="text"
                  id="inspectionStage"
                  v-model="formData.inspectionStage"
                  required
                />
              </div>
              <div class="form-group">
                <label for="testVenue">Test Venue:</label>
                <input
                  type="text"
                  id="testVenue"
                  v-model="formData.testVenue"
                  required
                />
              </div>
              <div class="form-group">
                <label for="slNos">SL.NO'S:</label>
                <input
                  type="text"
                  id="slNos"
                  v-model="formData.slNos"
                  required
                />
              </div>
            </div>

            <!-- Right Column -->
            <div class="details-column">
              <div class="form-group">
                <label for="dated1">Dated:</label>
                <input
                  type="date"
                  id="dated1"
                  v-model="formData.dated1"
                  required
                />
              </div>
              <div class="form-group">
                <label for="dated2">Dated:</label>
                <input
                  type="date"
                  id="dated2"
                  v-model="formData.dated2"
                  required
                />
              </div>
              <div class="form-group">
                <label for="sruName">SRU Name:</label>
                <input
                  type="text"
                  id="sruName"
                  v-model="formData.sruName"
                  required
                />
              </div>
              <div class="form-group">
                <label for="partNo">Part No:</label>
                <input
                  type="text"
                  id="partNo"
                  v-model="formData.partNo"
                  required
                />
              </div>
              <div class="form-group">
                <label for="quantity">Quantity:</label>
                <input
                  type="number"
                  id="quantity"
                  v-model="formData.quantity"
                  required
                />
              </div>
              <div class="form-group">
                <label for="startDate">Start Date:</label>
                <input
                  type="date"
                  id="startDate"
                  v-model="formData.startDate"
                  required
                />
              </div>
              <div class="form-group">
                <label for="endDate">End Date:</label>
                <input
                  type="date"
                  id="endDate"
                  v-model="formData.endDate"
                  required
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Test Cases Section -->
        <div class="form-section">
          <h2 class="section-title">Test Cases</h2>
          <div class="test-cases-table-container">
            <table class="test-cases-table">
              <thead>
                <tr>
                  <th>SL.NO:</th>
                  <th>TEST CASES</th>
                  <th>TEST NATURE</th>
                  <th>REMARKS (OK/ NOT OK)</th>
                  <th>UPLOAD</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(testCase, index) in formData.testCases"
                  :key="index"
                >
                  <td>{{ index + 1 }}</td>
                  <td class="test-case-description">
                    {{ testCase.description }}
                  </td>
                  <td>
                    <select v-model="testCase.testNature">
                      <option value="">Select</option>
                      <option value="Passive (Power Off Condition)">
                        Passive (Power Off Condition)
                      </option>
                      <option value="Active (Power On Condition)">
                        Active (Power On Condition)
                      </option>
                    </select>
                  </td>
                  <td>
                    <select v-model="testCase.remarks">
                      <option value="">Select</option>
                      <option value="OK">OK</option>
                      <option value="NOT OK">NOT OK</option>
                    </select>
                  </td>
                  <td>
                    <input
                      type="file"
                      @change="handleFileUpload($event, 'testCase', index)"
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
  name: "CotsScreeningInspectionReport",
  data() {
    return {
      projectName: "",
      lruName: "",
      serialNumber: "SL-001",
      inspectionCount: "INS-001",
      currentYear: "2025",
      currentDate: new Date().toISOString().split("T")[0],
      formData: {
        projectName: "",
        dpName: "",
        reportRefNo: "",
        memoRefNo: "",
        lruName: "",
        inspectionStage: "",
        testVenue: "",
        dated1: "",
        dated2: "",
        sruName: "",
        partNo: "",
        quantity: "",
        slNos: "",
        startDate: "",
        endDate: "",
        testCases: [
          {
            description:
              "High Temperature Storage (Stabilization Bake) Test: Populated PCB Stabilization bake +85°C, 24Hrs.",
            testNature: "Passive (Power Off Condition)",
            remarks: "",
          },
          {
            description:
              "Thermal Shock Test: Populated PCB Thermal shock -40°C, +85°C, Dwell time 30 minutes each, Temperature Transfer time 2 minutes, 10 cycles In Power Off Condition.",
            testNature: "Passive (Power Off Condition)",
            remarks: "",
          },
          {
            description: "Burn-in Test",
            testNature: "Active (Power On Condition)",
            remarks: "",
          },
        ],
        preparedBy: "",
        verifiedBy: "",
        approvedBy: "",
      },
    };
  },
  computed: {
    isFormValid() {
      return (
        this.formData.projectName &&
        this.formData.dpName &&
        this.formData.reportRefNo &&
        this.formData.memoRefNo &&
        this.formData.lruName &&
        this.formData.sruName &&
        this.formData.partNo
      );
    },
  },
  mounted() {
    // Get parameters from route
    this.lruName = this.$route.params.lruName || "";
    this.projectName = this.$route.params.projectName || "";

    // Set default values
    this.formData.lruName = this.lruName;
    this.formData.projectName = this.projectName;
    this.formData.startDate = this.currentDate;
  },
  methods: {
    handleFileUpload(event, section, index) {
      const file = event.target.files[0];
      if (file) {
        console.log(
          `File uploaded for ${section} section, item ${index}:`,
          file.name
        );
        // Here you would typically upload the file to your backend
        // For now, we'll just log it
      }
    },
    saveDraft() {
      console.log("Saving draft:", this.formData);
      alert("Draft saved successfully!");
    },
    resetForm() {
      if (
        confirm(
          "Are you sure you want to reset the form? All data will be lost."
        )
      ) {
        this.formData = {
          projectName: this.projectName,
          dpName: "",
          reportRefNo: "",
          memoRefNo: "",
          lruName: this.lruName,
          inspectionStage: "",
          testVenue: "",
          dated1: "",
          dated2: "",
          sruName: this.lruName,
          partNo: "",
          quantity: "",
          slNos: "",
          startDate: this.currentDate,
          endDate: "",
          testCases: [
            {
              description:
                "High Temperature Storage (Stabilization Bake) Test: Populated PCB Stabilization bake +85°C, 24Hrs.",
              testNature: "Passive (Power Off Condition)",
              remarks: "",
            },
            {
              description:
                "Thermal Shock Test: Populated PCB Thermal shock -40°C, +85°C, Dwell time 30 minutes each, Temperature Transfer time 2 minutes, 10 cycles In Power Off Condition.",
              testNature: "Passive (Power Off Condition)",
              remarks: "",
            },
            {
              description: "Burn-in Test",
              testNature: "Active (Power On Condition)",
              remarks: "",
            },
          ],
          preparedBy: "",
          verifiedBy: "",
          approvedBy: "",
        };
      }
    },
    async submitForm() {
      console.log("🚀 SUBMIT FORM CALLED!");
      console.log("Form valid:", this.isFormValid);
      console.log("Form data:", this.formData);

      if (this.isFormValid) {
        console.log("✅ Form is valid, proceeding with submission...");

        try {
          // Prepare data for backend API
          const apiData = {
            project_name: this.formData.projectName,
            report_ref_no: this.formData.reportRefNo,
            memo_ref_no: this.formData.memoRefNo,
            lru_name: this.formData.lruName,
            sru_name: this.formData.sruName,
            dp_name: this.formData.dpName,
            part_no: this.formData.partNo,
            inspection_stage: this.formData.inspectionStage,
            test_venue: this.formData.testVenue,
            quantity: this.formData.quantity,
            sl_nos: this.formData.slNos,
            serial_number: this.serialNumber,
            start_date: this.formData.startDate,
            end_date: this.formData.endDate,
            dated1: this.formData.dated1,
            dated2: this.formData.dated2,

            // Map test nature fields from testCases
            test_nature1: this.formData.testCases[0]?.testNature || "",
            test_nature2: this.formData.testCases[1]?.testNature || "",
            test_nature3: this.formData.testCases[2]?.testNature || "",

            // Map remarks from testCases (these will be rem1, rem2, rem3)
            rem1: this.formData.testCases[0]?.remarks || "",
            upload1: "", // File upload path would go here

            rem2: this.formData.testCases[1]?.remarks || "",
            upload2: "",

            rem3: this.formData.testCases[2]?.remarks || "",
            upload3: "",

            // Signatories
            prepared_by: this.formData.preparedBy || "",
            verified_by: this.formData.verifiedBy || "",
            approved_by: this.formData.approvedBy || "",
          };

          console.log("📤 Sending data to API:", apiData);
          console.log(
            "🌐 API URL: http://localhost:5000/api/reports/cot-screening?user_role=4"
          );

          // Call the backend API
          const response = await fetch(
            "http://localhost:5000/api/reports/cot-screening?user_role=4",
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify(apiData),
            }
          );

          console.log(
            "📥 Response received:",
            response.status,
            response.statusText
          );

          const result = await response.json();

          if (result.success) {
            alert(
              `Report submitted successfully! Report ID: ${result.report_id}`
            );
            console.log("Report created with ID:", result.report_id);
            // Optionally reset the form or redirect
            this.resetForm();
          } else {
            alert(`Error: ${result.message}`);
            console.error("API Error:", result);
          }
        } catch (error) {
          console.error("Error submitting form:", error);
          alert("Error submitting form. Please try again.");
        }
      } else {
        alert("Please fill in all required fields.");
      }
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
        doc.text("COTS SCREENING INSPECTION REPORT", pageWidth / 2, yPosition, {
          align: "center",
        });
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
        const subjectText = `SUB: COTS Screening Inspection Report for ${
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
          `Project Name: ${this.formData.projectName || "Not specified"}`,
          `DP Name: ${this.formData.dpName || "Not specified"}`,
          `Report Ref No: ${this.formData.reportRefNo || "Not specified"}`,
          `Memo Ref No: ${this.formData.memoRefNo || "Not specified"}`,
          `LRU Name: ${this.formData.lruName || "Not specified"}`,
          `SRU Name: ${this.formData.sruName || "Not specified"}`,
          `Part No: ${this.formData.partNo || "Not specified"}`,
          `Quantity: ${this.formData.quantity || "Not specified"}`,
          `Start Date: ${this.formData.startDate || "Not specified"}`,
          `End Date: ${this.formData.endDate || "Not specified"}`,
        ];

        details.forEach((detail) => {
          doc.text(detail, margin, yPosition);
          yPosition += 6;
        });

        yPosition += 10;

        // Test cases table
        doc.setFont("helvetica", "bold");
        doc.text("Test Cases:", margin, yPosition);
        yPosition += 8;

        if (this.formData.testCases && this.formData.testCases.length > 0) {
          doc.setFontSize(9);
          doc.setFont("helvetica", "bold");

          // Table headers
          doc.text("SL.NO", margin, yPosition);
          doc.text("TEST CASES", margin + 15, yPosition);
          doc.text("TEST NATURE", margin + 100, yPosition);
          doc.text("REMARKS", margin + 160, yPosition);
          yPosition += 6;

          // Table data
          doc.setFont("helvetica", "normal");
          this.formData.testCases.forEach((testCase, index) => {
            doc.text((index + 1).toString(), margin, yPosition);
            doc.text(
              testCase.description.substring(0, 40),
              margin + 15,
              yPosition
            );
            doc.text(testCase.testNature || "", margin + 100, yPosition);
            doc.text(testCase.remarks || "", margin + 160, yPosition);
            yPosition += 6;
          });
        }

        yPosition += 15;

        // Signatures
        doc.setFont("helvetica", "bold");
        doc.text("Signatures:", margin, yPosition);
        yPosition += 8;

        doc.setFont("helvetica", "normal");
        doc.text("Prepared By: _________________", margin, yPosition);
        doc.text("Verified By: _________________", margin + 70, yPosition);
        doc.text("Approved By: _________________", margin + 140, yPosition);

        // Save PDF
        const fileName = `COTS_Screening_Inspection_Report_${
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
.cots-screening-inspection-page {
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

/* Form Sections */
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

/* Header Info Grid */
.header-info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  margin-bottom: 20px;
}

/* Report Details Grid */
.report-details-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}

.details-column {
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

/* Test Cases Table */
.test-cases-table-container {
  margin-top: 20px;
  overflow-x: auto;
}

.test-cases-table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
  font-size: 0.9em;
}

.test-cases-table th {
  background: #2d3748;
  color: white;
  padding: 12px 8px;
  text-align: left;
  font-weight: 600;
  font-size: 0.85em;
}

.test-cases-table td {
  padding: 8px;
  border-bottom: 1px solid #e2e8f0;
  vertical-align: top;
}

.test-cases-table tr:nth-child(even) {
  background-color: #f8fafc;
}

.test-case-description {
  font-size: 0.8em;
  line-height: 1.4;
  max-width: 300px;
}

.test-cases-table input[type="text"],
.test-cases-table select {
  width: 100%;
  padding: 6px;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  font-size: 0.85em;
}

.test-cases-table input[type="file"] {
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

  .header-info-grid,
  .report-details-grid {
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

  .test-cases-table-container {
    overflow-x: auto;
  }

  .test-cases-table {
    min-width: 800px;
  }
}
</style>
