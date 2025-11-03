<template>
  <div class="conformal-coating-inspection-page">
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
              <input v-model="projectName" type="text" :disabled="isFormReadonly" />
            </div>
            <div>
              <strong>Report Ref No:</strong>
              <input v-model="reportRefNo" type="text" :disabled="isFormReadonly" />
            </div>
            <div>
              <strong>DP Name:</strong> <input v-model="dpName" type="text" :disabled="isFormReadonly" />
            </div>
            <div>
              <strong>Part No:</strong> <input v-model="partNo" type="text" :disabled="isFormReadonly" />
            </div>
            <div>
              <strong>SL No's:</strong> <input v-model="slNo" type="text" :disabled="isFormReadonly" />
            </div>
            <div>
              <strong>End Date:</strong> <input v-model="endDate" type="date" :disabled="isFormReadonly" />
            </div>
            <div>
              <strong>SRU Name:</strong> <input v-model="sruName" type="text" :disabled="isFormReadonly" />
            </div>
            <div>
              <strong>Start Date:</strong>
              <input v-model="startDate" type="date" :disabled="isFormReadonly" />
            </div>
            <div>
              <strong>Inspection Stage:</strong>
              <input v-model="inspectionStage" type="text" :disabled="isFormReadonly" />
            </div>
            <div>
              <strong>Test Venue:</strong>
              <input v-model="testVenue" type="text" :disabled="isFormReadonly" />
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
                <td>
                  <select v-model="test.observation" @change="updateRemark(test)" :disabled="isFormReadonly">
                    <option value="">Select</option>
                    <option v-if="test.case === 'Connectors surrounding and beneath'" value="no damages">no damages</option>
                    <option v-if="test.case === 'Connectors surrounding and beneath'" value="damages present">damages present</option>
                    <option v-if="test.case !== 'Connectors surrounding and beneath'" value="yes">yes</option>
                    <option v-if="test.case !== 'Connectors surrounding and beneath'" value="no">no</option>
                  </select>
                </td>
                <td><input v-model="test.remark" type="text" :disabled="true" readonly /></td>
                <td><input type="file" :disabled="isFormReadonly" /></td>
              </tr>
            </tbody>
          </table>

          <div class="report-footer">
            <div class="signature-section">
              <strong>Prepared By:</strong>
              <div class="signature-auth-container">
                <div class="signature-inputs">
                  <div class="input-group">
                    <label>Username:</label>
                    <input
                      type="text"
                      v-model="preparedByUsername"
                      placeholder="Enter username..."
                      :disabled="isFormReadonly || !areAllFieldsFilled"
                    />
                  </div>
                  <div class="input-group">
                    <label>Signature Password:</label>
                    <input
                      type="password"
                      v-model="preparedByPassword"
                      placeholder="Enter signature password..."
                      :disabled="isFormReadonly || !areAllFieldsFilled"
                    />
                  </div>
                  <button
                    type="button"
                    class="btn btn-verify"
                    @click="verifySignature('prepared')"
                    :disabled="isFormReadonly || !areAllFieldsFilled || !preparedByUsername || !preparedByPassword"
                  >
                    Verify & Load Signature
                  </button>
                </div>
                <div v-if="preparedBySignatureUrl" class="signature-display">
                  <div class="signature-image-container">
                    <img
                      :src="preparedBySignatureUrl"
                      alt="Verified Signature"
                      class="signature-image"
                    />
                    <div class="signature-info">
                      <span class="signature-user">{{ preparedByVerifiedName }}</span>
                      <span class="signature-status">✓ Verified</span>
                    </div>
                  </div>
                </div>
                <div v-if="preparedByError" class="signature-error">
                  {{ preparedByError }}
                </div>
              </div>
            </div>
            <div class="signature-section">
              <strong>Verified By:</strong>
              <div class="signature-auth-container">
                <div class="signature-inputs">
                  <div class="input-group">
                    <label>Username:</label>
                    <input
                      type="text"
                      v-model="verifiedByUsername"
                      placeholder="Enter username..."
                      :disabled="!preparedBySignatureUrl"
                    />
                  </div>
                  <div class="input-group">
                    <label>Signature Password:</label>
                    <input
                      type="password"
                      v-model="verifiedByPassword"
                      placeholder="Enter signature password..."
                      :disabled="!preparedBySignatureUrl"
                    />
                  </div>
                  <button
                    type="button"
                    class="btn btn-verify"
                    @click="verifySignature('verified')"
                    :disabled="!preparedBySignatureUrl || !verifiedByUsername || !verifiedByPassword"
                  >
                    Verify & Load Signature
                  </button>
                </div>
                <div v-if="verifiedBySignatureUrl" class="signature-display">
                  <div class="signature-image-container">
                    <img
                      :src="verifiedBySignatureUrl"
                      alt="Verified Signature"
                      class="signature-image"
                    />
                    <div class="signature-info">
                      <span class="signature-user">{{ verifiedByVerifiedName }}</span>
                      <span class="signature-status">✓ Verified</span>
                    </div>
                  </div>
                </div>
                <div v-if="verifiedByError" class="signature-error">
                  {{ verifiedByError }}
                </div>
              </div>
            </div>
            <div class="signature-section">
              <strong>Approved By:</strong>
              <div class="signature-auth-container">
                <div class="signature-inputs">
                  <div class="input-group">
                    <label>Username:</label>
                    <input
                      type="text"
                      v-model="approvedByUsername"
                      placeholder="Enter username..."
                      :disabled="!verifiedBySignatureUrl"
                    />
                  </div>
                  <div class="input-group">
                    <label>Signature Password:</label>
                    <input
                      type="password"
                      v-model="approvedByPassword"
                      placeholder="Enter signature password..."
                      :disabled="!verifiedBySignatureUrl"
                    />
                  </div>
                  <button
                    type="button"
                    class="btn btn-verify"
                    @click="verifySignature('approved')"
                    :disabled="!verifiedBySignatureUrl || !approvedByUsername || !approvedByPassword"
                  >
                    Verify & Load Signature
                  </button>
                </div>
                <div v-if="approvedBySignatureUrl" class="signature-display">
                  <div class="signature-image-container">
                    <img
                      :src="approvedBySignatureUrl"
                      alt="Verified Signature"
                      class="signature-image"
                    />
                    <div class="signature-info">
                      <span class="signature-user">{{ approvedByVerifiedName }}</span>
                      <span class="signature-status">✓ Verified</span>
                    </div>
                  </div>
                </div>
                <div v-if="approvedByError" class="signature-error">
                  {{ approvedByError }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Submit Button - Enabled only after Approved By signature -->
        <div class="form-actions final-submit" v-if="isFormReadonly && approvedBySignatureUrl">
          <button
            type="button"
            @click="finalSubmitReport"
            class="btn btn-primary btn-submit-final"
            :disabled="!approvedBySignatureUrl || !reportId"
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
  props: {
    readonly: {
      type: Boolean,
      default: false,
    },
    isTemplatePreview: {
      type: Boolean,
      default: false,
    },
    reportId: {
      type: [String, Number],
      default: null,
    },
  },
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
      preparedByUsername: "",
      preparedByPassword: "",
      preparedBySignatureUrl: "",
      preparedByVerifiedName: "",
      preparedByError: "",
      verifiedBy: "",
      verifiedByUsername: "",
      verifiedByPassword: "",
      verifiedBySignatureUrl: "",
      verifiedByVerifiedName: "",
      verifiedByError: "",
      approvedBy: "",
      approvedByUsername: "",
      approvedByPassword: "",
      approvedBySignatureUrl: "",
      approvedByVerifiedName: "",
      approvedByError: "",
      approvedByUserId: null, // Store user_id of the approver
      reportId: null, // Store report ID after initial submission
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
          expected: "no",
          observation: "",
          remark: "",
        },
        {
          case: "Entrapped air bubbles",
          expected: "no",
          observation: "",
          remark: "",
        },
        {
          case: "Enclosed foreign particles in the cracks",
          expected: "no",
          observation: "",
          remark: "",
        },
        {
          case: "Residue of masking material",
          expected: "no",
          observation: "",
          remark: "",
        },
        {
          case: "Dis-coloration",
          expected: "no",
          observation: "",
          remark: "",
        },
        {
          case: "Pin holes and Soft spots",
          expected: "no",
          observation: "",
          remark: "",
        },
        {
          case: "Connectors surrounding and beneath",
          expected: "no damages",
          observation: "",
          remark: "",
        },
        { case: "Uniformity in coating across the board", 
        expected: "yes", 
        observation: "", 
        remark: "" 
        },
        {
          case: "Conformal coating thickness of 30 to 130 microns for acrylic material as per IPC-CC-830B",
          expected: "yes",
          observation: "",
          remark: "",
        },
      ],
    };
  },
  computed: {
    // Form becomes readonly once Prepared By signature is fetched and report is saved
    // Before Prepared By signature: form is ALWAYS fully editable (regardless of readonly prop)
    // After Prepared By signature: form becomes readonly, but Verified/Approved By remain editable
    isFormReadonly() {
      // Before Prepared By signature: form should ALWAYS be editable for initial data entry
      // Check if Prepared By signature has been fetched and report has been saved
      const hasPreparedBySignature = this.preparedBySignatureUrl && this.preparedBySignatureUrl.trim() !== '';
      const hasReportId = this.reportId !== null && this.reportId !== undefined;
      
      // Form is readonly ONLY if BOTH signature exists AND report has been saved
      // Before that point, form is always editable (even if readonly prop is true)
      if (hasPreparedBySignature && hasReportId) {
        return true; // Form is saved with Prepared By signature, make it readonly
      }
      
      // Before Prepared By signature: form is editable regardless of readonly prop
      // (This allows users to fill the form initially even if viewed from read-only context)
      return false;
    },
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
    areAllFieldsFilled() {
      // Check basic form fields
      const basicFieldsFilled = (
        this.projectName &&
        this.reportRefNo &&
        this.dpName &&
        this.partNo &&
        this.slNo &&
        this.sruName &&
        this.startDate &&
        this.endDate &&
        this.inspectionStage &&
        this.testVenue
      );

      // Check if all test observations are filled
      const allObservationsFilled = this.tests.every(
        (test) => test.observation && test.observation.trim() !== ""
      );

      return basicFieldsFilled && allObservationsFilled;
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

    // Load existing report data if reportId is provided (from prop or route)
    const reportIdToLoad = this.reportId || this.$route?.params?.reportId;
    if (reportIdToLoad) {
      // If reportId comes from route, store it in data property
      if (this.$route?.params?.reportId && !this.reportId) {
        this.reportId = reportIdToLoad;
      }
      this.loadReportData();
    }
  },
  watch: {
    reportId: {
      handler(newVal) {
        if (newVal) {
          this.loadReportData();
        }
      },
      immediate: false,
    },
    // Also watch route params for reportId changes
    '$route.params.reportId': {
      handler(newVal) {
        if (newVal) {
          // Store route reportId in data property
          this.reportId = newVal;
          this.loadReportData();
        }
      },
      immediate: false,
    },
  },
  methods: {
    async loadReportData() {
      // Load report data from database when reportId is available
      const reportIdToLoad = this.reportId || this.$route?.params?.reportId;
      
      if (!reportIdToLoad) {
        console.log("No reportId available to load data");
        return;
      }

      try {
        const response = await fetch(
          `http://localhost:5000/api/reports/conformal-coating-inspection/${reportIdToLoad}`,
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
            },
          }
        );

        if (!response.ok) {
          throw new Error(`Failed to fetch report: ${response.statusText}`);
        }

        const result = await response.json();

        if (result.success && result.report) {
          const report = result.report;

          // Set reportId
          this.reportId = report.report_id;

          // Map header fields
          this.projectName = report.project_name || "";
          this.reportRefNo = report.report_ref_no || "";
          this.memoRefNo = report.memo_ref_no || "";
          this.lruName = report.lru_name || "";
          this.sruName = report.sru_name || "";
          this.dpName = report.dp_name || "";
          this.partNo = report.part_no || "";
          this.inspectionStage = report.inspection_stage || "";
          this.testVenue = report.test_venue || "";
          this.quantity = report.quantity || null;
          this.slNo = report.sl_nos || "";
          this.serialNumber = report.serial_number || "";
          this.startDate = report.start_date ? (typeof report.start_date === 'string' ? report.start_date.split('T')[0] : report.start_date) : "";
          this.endDate = report.end_date ? (typeof report.end_date === 'string' ? report.end_date.split('T')[0] : report.end_date) : "";
          this.dated1 = report.dated1 ? (typeof report.dated1 === 'string' ? report.dated1.split('T')[0] : report.dated1) : "";
          this.dated2 = report.dated2 ? (typeof report.dated2 === 'string' ? report.dated2.split('T')[0] : report.dated2) : "";
          this.overallStatus = report.overall_status || "";
          this.qualityRating = report.quality_rating || null;
          this.recommendations = report.recommendations || "";

          // Map test cases (obs1-9, rem1-9, upload1-9, expected1-9)
          for (let i = 1; i <= 9; i++) {
            if (this.tests[i - 1]) {
              this.tests[i - 1].observation = report[`obs${i}`] || "";
              this.tests[i - 1].remark = report[`rem${i}`] || "";
              this.tests[i - 1].upload = report[`upload${i}`] || "";
              this.tests[i - 1].expected = report[`expected${i}`] || this.tests[i - 1].expected;
              
              // Update remark if observation is set (trigger auto-remark update)
              if (this.tests[i - 1].observation) {
                this.updateRemark(this.tests[i - 1]);
              }
            }
          }

          // Parse signature fields (format: "name|signature_url")
          if (report.prepared_by) {
            const preparedParts = report.prepared_by.split("|");
            this.preparedBy = preparedParts[0] || "";
            this.preparedBySignatureUrl = preparedParts[1] || "";
            this.preparedByVerifiedName = preparedParts[0] || "";
          }

          if (report.verified_by) {
            const verifiedParts = report.verified_by.split("|");
            this.verifiedBy = verifiedParts[0] || "";
            this.verifiedBySignatureUrl = verifiedParts[1] || "";
            this.verifiedByVerifiedName = verifiedParts[0] || "";
          }

          if (report.approved_by) {
            const approvedParts = report.approved_by.split("|");
            this.approvedBy = approvedParts[0] || "";
            this.approvedBySignatureUrl = approvedParts[1] || "";
            this.approvedByVerifiedName = approvedParts[0] || "";
          }

          console.log("✓ Report data loaded successfully:", report.report_id);
        } else {
          console.error("Failed to load report data:", result.message);
        }
      } catch (error) {
        console.error("Error loading report data:", error);
      }
    },
    async verifySignature(signatureType) {
      let username, password;
      let formData = {};

      if (signatureType === "prepared") {
        username = this.preparedByUsername;
        password = this.preparedByPassword;
        formData = {
          signatureUrl: "preparedBySignatureUrl",
          verifiedName: "preparedByVerifiedName",
          error: "preparedByError",
          userField: "preparedBy"
        };
      } else if (signatureType === "verified") {
        username = this.verifiedByUsername;
        password = this.verifiedByPassword;
        formData = {
          signatureUrl: "verifiedBySignatureUrl",
          verifiedName: "verifiedByVerifiedName",
          error: "verifiedByError",
          userField: "verifiedBy"
        };
      } else if (signatureType === "approved") {
        username = this.approvedByUsername;
        password = this.approvedByPassword;
        formData = {
          signatureUrl: "approvedBySignatureUrl",
          verifiedName: "approvedByVerifiedName",
          error: "approvedByError",
          userField: "approvedBy"
        };
      }

      if (!username || !password) {
        this[formData.error] = "Please enter both username and signature password";
        return;
      }

      try {
        const response = await fetch("http://localhost:5000/api/users/verify-signature", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username: username,
            signature_password: password,
          }),
        });

        const data = await response.json();

        if (data.success) {
          this[formData.signatureUrl] = data.signature_url;
          this[formData.verifiedName] = data.user_name;
          this[formData.error] = "";
          this[formData.userField] = data.user_name; // Store verified name
          
          // Store user_id for approved signature (needed for notification)
          if (signatureType === "approved" && data.user_id) {
            this.approvedByUserId = data.user_id;
          }
          
          // Handle auto-submission and updates based on signature type
          if (signatureType === "prepared") {
            // Auto-submit when Prepared By signature is fetched
            await this.autoSubmitReport();
          } else if (signatureType === "verified") {
            // Save to DB when Verified By signature is fetched
            await this.updateReportSignature('verified');
          } else if (signatureType === "approved") {
            // Auto-submit when Approved By signature is fetched
            await this.updateReportSignature('approved');
            // Notify QA Heads about approval
            await this.notifyApproval();
          }
        } else {
          this[formData.error] = data.message || "Failed to verify signature";
          this[formData.signatureUrl] = "";
          this[formData.verifiedName] = "";
          this[formData.userField] = "";
        }
      } catch (error) {
        this[formData.error] = "Error verifying signature: " + error.message;
        this[formData.signatureUrl] = "";
        this[formData.verifiedName] = "";
        this[formData.userField] = "";
      }
    },
    updateRemark(test) {
      if (!test.observation) {
        test.remark = "";
        return;
      }
      
      // Compare observation with expected value (case-insensitive)
      const observation = test.observation.toLowerCase().trim();
      const expected = test.expected.toLowerCase().trim();
      
      // Map to database constraint values: "OK" or "NOT OK"
      if (observation === expected) {
        test.remark = "OK";
      } else {
        test.remark = "NOT OK";
      }
    },
    async saveDraft() {
      try {
        const reportData = this.prepareReportData();
        const response = await fetch(
          "http://localhost:5000/api/reports/conformal-coating-inspection",
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
        this.preparedByUsername = "";
        this.preparedByPassword = "";
        this.preparedBySignatureUrl = "";
        this.preparedByVerifiedName = "";
        this.preparedByError = "";
        this.verifiedBy = "";
        this.verifiedByUsername = "";
        this.verifiedByPassword = "";
        this.verifiedBySignatureUrl = "";
        this.verifiedByVerifiedName = "";
        this.verifiedByError = "";
        this.approvedBy = "";
        this.approvedByUsername = "";
        this.approvedByPassword = "";
        this.approvedBySignatureUrl = "";
        this.approvedByVerifiedName = "";
        this.approvedByError = "";
        // Note: reportId is NOT reset here - it should persist until form is explicitly reset

        // Reset test observations and remarks
        this.tests.forEach((test) => {
          test.observation = "";
          test.remark = "";
        });
      }
    },
    async autoSubmitReport() {
      try {
        // Ensure all remarks are updated before submitting
        this.tests.forEach((test) => {
          if (test.observation) {
            this.updateRemark(test);
          }
        });
        
        const reportData = this.prepareReportData();
        const response = await fetch(
          "http://localhost:5000/api/reports/conformal-coating-inspection",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(reportData),
          }
        );

        if (!response.ok) {
          const errorText = await response.text();
          let errorMessage = `Failed to submit report: ${response.status} ${response.statusText}`;
          try {
            const errorData = JSON.parse(errorText);
            errorMessage = errorData.message || errorMessage;
          } catch (e) {
            errorMessage = errorText || errorMessage;
          }
          throw new Error(errorMessage);
        }

        const result = await response.json();

        if (result.success && result.report_id) {
          this.reportId = result.report_id;
          console.log(`✓ Report saved to database with ID: ${result.report_id}`);
          alert(`Report saved successfully! Report ID: ${result.report_id}`);
        } else {
          const errorMsg = result.message || "Unknown error occurred";
          console.error("Error submitting report:", errorMsg);
          alert(`Error submitting report: ${errorMsg}`);
        }
      } catch (error) {
        console.error("Error auto-submitting report:", error);
        alert("Error submitting report. Please try again.");
      }
    },
    async updateReportSignature(signatureType) {
      if (!this.reportId) {
        console.error("Report ID not found. Cannot update signature.");
        alert("Error: Report not found. Please complete the Prepared By signature first.");
        return;
      }

      try {
        const updateData = {};
        if (signatureType === "verified") {
          // Store signature URL in verified_by field (format: "name|signature_url")
          updateData.verified_by = `${this.verifiedBy}|${this.verifiedBySignatureUrl}`;
        } else if (signatureType === "approved") {
          // Store signature URL in approved_by field (format: "name|signature_url")
          updateData.approved_by = `${this.approvedBy}|${this.approvedBySignatureUrl}`;
        }

        if (!this.reportId) {
          console.error("Report ID not found. Cannot update signature.");
          alert("Error: Report not found. Please complete the Prepared By signature first.");
          return;
        }

        // Update the existing record in the database
        const response = await fetch(
          `http://localhost:5000/api/reports/conformal-coating-inspection/${this.reportId}`,
          {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(updateData),
          }
        );

        if (!response.ok) {
          const errorText = await response.text();
          let errorMessage = `Failed to update report: ${response.status} ${response.statusText}`;
          try {
            const errorData = JSON.parse(errorText);
            errorMessage = errorData.message || errorMessage;
          } catch (e) {
            errorMessage = errorText || errorMessage;
          }
          throw new Error(errorMessage);
        }

        const result = await response.json();

        if (result.success) {
          if (signatureType === "verified") {
            console.log(`Verified By signature updated in report ID: ${this.reportId}`);
            alert("Verified By signature saved successfully!");
          } else if (signatureType === "approved") {
            console.log(`Approved By signature updated in report ID: ${this.reportId}`);
            alert("Report finalized successfully!");
          }
        } else {
          alert(`Error updating report: ${result.message}`);
        }
      } catch (error) {
        console.error("Error updating report signature:", error);
        alert("Error updating report. Please try again.");
      }
    },
    async submitForm() {
      // This is the old submit handler - kept for form submission prevention
      // Actual submission happens via finalSubmitReport after Approved By signature
      if (this.isFormValid && this.reportId && this.approvedBySignatureUrl) {
        await this.finalSubmitReport();
      } else {
        if (!this.isFormValid) {
          alert("Please fill in all required fields.");
        } else if (!this.reportId) {
          alert("Please complete the Prepared By signature first.");
        } else if (!this.approvedBySignatureUrl) {
          alert("Please complete the Approved By signature first.");
        }
      }
    },
    async finalSubmitReport() {
      // Final submit button handler - called after Approved By signature is fetched
      if (!this.reportId) {
        alert("Error: Report not found. Please complete the Prepared By signature first.");
        return;
      }
      
      if (!this.approvedBySignatureUrl) {
        alert("Please complete the Approved By signature first.");
        return;
      }
      
      try {
        // Notify QA Heads and log to activity logs
        await this.notifyQAHeads();
        alert("Report submitted successfully! Activity logged and QA Heads have been notified.");
        console.log("Report submitted with ID:", this.reportId);
      } catch (error) {
        console.error("Error submitting report:", error);
        alert("Error submitting report. Please try again.");
      }
    },
    async notifyQAHeads() {
      try {
        // Get current user from session/localStorage
        const currentUser = JSON.parse(localStorage.getItem('user') || '{}');
        const reviewerId = currentUser.user_id || null;
        
        if (!reviewerId) {
          console.error("Reviewer ID not found");
          return;
        }

        // Send notification to backend
        const response = await fetch(
          "http://localhost:5000/api/reports/conformal-coating-inspection/notify",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              report_id: this.reportId,
              memo_ref_no: this.memoRefNo,
              reviewer_id: reviewerId,
            }),
          }
        );

        const result = await response.json();
        if (!result.success) {
          console.error("Failed to send notification:", result.message);
        }
      } catch (error) {
        console.error("Error notifying QA Heads:", error);
        throw error;
      }
    },
    async notifyApproval() {
      try {
        if (!this.reportId) {
          console.error("Report ID not found. Cannot send approval notification.");
          return;
        }

        if (!this.approvedByUserId) {
          console.error("Approved By User ID not found. Cannot send approval notification.");
          return;
        }

        // Send approval notification to backend
        const response = await fetch(
          "http://localhost:5000/api/reports/conformal-coating-inspection/notify-approval",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              report_id: this.reportId,
              approved_by_id: this.approvedByUserId,
            }),
          }
        );

        const result = await response.json();
        if (result.success) {
          console.log("✓ Approval notification sent successfully");
        } else {
          console.error("Failed to send approval notification:", result.message);
        }
      } catch (error) {
        console.error("Error notifying QA Heads about approval:", error);
        // Don't throw error - approval signature should still be saved even if notification fails
      }
    },
    prepareReportData() {
      // Include original_report_id from the reportId prop (which is the reports.report_id)
      const originalReportId = this.reportId || this.savedReportId;
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
        start_date: this.startDate || null,
        end_date: this.endDate || null,
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
        prepared_by: this.preparedBySignatureUrl ? `${this.preparedBy}|${this.preparedBySignatureUrl}` : this.preparedBy,
        verified_by: this.verifiedBySignatureUrl ? `${this.verifiedBy}|${this.verifiedBySignatureUrl}` : this.verifiedBy,
        approved_by: this.approvedBySignatureUrl ? `${this.approvedBy}|${this.approvedBySignatureUrl}` : this.approvedBy,
        report_card_id: originalReportId, // Link to the original report card ID from reports table (preferred field)
        original_report_id: originalReportId, // Backward compatibility
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

.inspection-table select {
  width: 95%;
  border: 1px solid #e0e0e0;
  padding: 5px;
  box-sizing: border-box;
  background-color: white;
  font-size: inherit;
}

.inspection-table input[type="file"] {
  font-size: 12px;
}

.report-footer {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  gap: 20px;
  margin-top: 30px;
  padding-top: 15px;
  border-top: 1px dashed #ccc;
}

.signature-section {
  flex: 1;
  min-width: 0;
}

.signature-section strong {
  display: block;
  margin-bottom: 10px;
  font-size: 14px;
}

.signature-auth-container {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  background-color: #f8f9fa;
  margin-top: 10px;
}

.signature-inputs {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.signature-inputs .input-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.signature-inputs label {
  font-size: 12px;
  font-weight: 600;
  color: #333;
}

.signature-inputs input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
}

.signature-inputs input:disabled {
  background-color: #f0f0f0;
  cursor: not-allowed;
}

.btn-verify {
  background-color: #28a745;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  margin-top: 10px;
}

.btn-verify:hover:not(:disabled) {
  background-color: #218838;
}

.btn-verify:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
  opacity: 0.6;
}

.signature-display {
  margin-top: 15px;
  padding: 15px;
  background-color: #e8f5e8;
  border: 1px solid #28a745;
  border-radius: 6px;
}

.signature-image-container {
  display: flex;
  align-items: center;
  gap: 15px;
  flex-wrap: wrap;
}

.signature-image {
  max-width: 150px;
  max-height: 80px;
  border: 2px solid #28a745;
  border-radius: 4px;
  background-color: white;
  object-fit: contain;
}

.signature-info {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.signature-user {
  font-weight: 600;
  color: #155724;
  font-size: 14px;
}

.signature-status {
  color: #28a745;
  font-size: 12px;
  font-weight: 600;
}

.signature-error {
  margin-top: 10px;
  padding: 10px;
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  border-radius: 4px;
  color: #721c24;
  font-size: 12px;
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

/* Final Submit Button Styling */
.form-actions.final-submit {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 2px solid #4a5568;
  display: flex;
  justify-content: center;
  align-items: center;
}

.btn-submit-final {
  min-width: 200px;
  font-size: 16px;
  font-weight: 600;
  padding: 12px 30px;
  background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
  border: none;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.btn-submit-final:hover:not(:disabled) {
  background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.btn-submit-final:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
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
