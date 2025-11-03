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
            <div class="signature-section">
              <strong>Prepared By (QA G1 -Team):</strong>
              <div class="signature-auth-container">
                <div class="signature-inputs">
                  <div class="input-group">
                    <label>Username:</label>
                    <input
                      type="text"
                      v-model="preparedByUsername"
                      placeholder="Enter username..."
                      :disabled="readonly || !areAllFieldsFilled"
                    />
            </div>
                  <div class="input-group">
                    <label>Signature Password:</label>
                    <input
                      type="password"
                      v-model="preparedByPassword"
                      placeholder="Enter signature password..."
                      :disabled="readonly || !areAllFieldsFilled"
                    />
            </div>
                  <button
                    type="button"
                    class="btn btn-verify"
                    @click="verifySignature('prepared')"
                    :disabled="readonly || !areAllFieldsFilled || !preparedByUsername || !preparedByPassword"
                  >
                    Verify & Load Signature
                  </button>
                 </div>
                 <div v-if="preparedBySignatureUrl && (preparedByVerifiedInSession || readonly)" class="signature-display">
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
              <strong>Verified By (G1H - QA G):</strong>
              <div class="signature-auth-container">
                <div class="signature-inputs">
                  <div class="input-group">
                    <label>Username:</label>
                    <input
                      type="text"
                      v-model="verifiedByUsername"
                      placeholder="Enter username..."
                      :disabled="!preparedBySignatureUrl || readonly"
                    />
                  </div>
                  <div class="input-group">
                    <label>Signature Password:</label>
                    <input
                      type="password"
                      v-model="verifiedByPassword"
                      placeholder="Enter signature password..."
                      :disabled="!preparedBySignatureUrl || readonly"
                    />
                  </div>
                  <button
                    type="button"
                    class="btn btn-verify"
                    @click="verifySignature('verified')"
                    :disabled="!preparedBySignatureUrl || !verifiedByUsername || !verifiedByPassword || readonly"
                  >
                    Verify & Load Signature
                  </button>
                 </div>
                 <div v-if="verifiedBySignatureUrl && (verifiedByVerifiedInSession || readonly)" class="signature-display">
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
                      :disabled="!verifiedBySignatureUrl || readonly"
                    />
                  </div>
                  <div class="input-group">
                    <label>Signature Password:</label>
                    <input
                      type="password"
                      v-model="approvedByPassword"
                      placeholder="Enter signature password..."
                      :disabled="!verifiedBySignatureUrl || readonly"
                    />
                  </div>
                  <button
                    type="button"
                    class="btn btn-verify"
                    @click="verifySignature('approved')"
                    :disabled="!verifiedBySignatureUrl || !approvedByUsername || !approvedByPassword || readonly"
                  >
                    Verify & Load Signature
                  </button>
                 </div>
                 <div v-if="approvedBySignatureUrl && (approvedByVerifiedInSession || readonly)" class="signature-display">
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

        <!-- Action Buttons - Only show before Prepared By signature is verified -->
        <div class="form-actions" v-if="!readonly && !preparedBySignatureUrl">
          <button type="button" @click="saveDraft" class="btn btn-secondary">
            Save Draft
          </button>
          <button type="button" @click="resetForm" class="btn btn-secondary">
            Reset
          </button>
          <button
            type="button"
            class="btn btn-primary"
            :disabled="!isFormValid"
            @click="handleSubmit"
          >
            Fill Report (Signatures Required)
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
    reportId: {
      type: [String, Number],
      default: null,
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
      // Signature verification fields
      preparedByUsername: "",
      preparedByPassword: "",
      preparedBySignatureUrl: "",
      preparedByVerifiedName: "",
      preparedByError: "",
      verifiedByUsername: "",
      verifiedByPassword: "",
      verifiedBySignatureUrl: "",
      verifiedByVerifiedName: "",
      verifiedByError: "",
      approvedByUsername: "",
      approvedByPassword: "",
      approvedBySignatureUrl: "",
      approvedByVerifiedName: "",
      approvedByError: "",
      approvedByUserId: null, // Store user_id of the approver
      savedReportId: null, // Store report ID after submission
      // Track if signatures were verified in current session (not just loaded from DB)
      preparedByVerifiedInSession: false,
      verifiedByVerifiedInSession: false,
      approvedByVerifiedInSession: false,
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
    areAllFieldsFilled() {
      // Check if all required fields are filled
      return (
        this.reportData.projectName &&
        this.reportData.reportRefNo &&
        this.reportData.lruName &&
        this.reportData.dpName &&
        this.reportData.partNo &&
        this.reportData.quantity
      );
    },
    effectiveReportId() {
      // Return the effective report ID (either prop or saved)
      return this.reportId || this.savedReportId;
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

    // Load existing report data if reportId is provided (from prop or route)
    const reportIdToLoad = this.reportId || this.$route?.params?.reportId;
    if (reportIdToLoad) {
      // If reportId comes from route, store it in prop/component
      if (this.$route?.params?.reportId && !this.reportId) {
        // Note: reportId is a prop, so we'll use it directly
      }
      this.loadReportData();
    }
    
    // Compute initial remarks if observations already present
    this.reportData.inspectionItems.forEach((item) => {
      if (item.observations) {
        this.computeRemarkForItem(item);
      }
    });
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
          // Load data when route reportId changes
          this.loadReportData();
        }
      },
      immediate: false,
    },
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
      // This method is now only for validation
      // Actual submission happens when Prepared By signature is verified
      if (!this.isFormValid) {
        alert("Please fill in all required fields.");
        return;
      }
      
      // Just validate and show message that signatures are needed
      alert("Please complete the Prepared By signature to submit the report. The report will be saved to the database when the Prepared By signature is verified.");
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
          this.reportData[formData.userField] = data.user_name; // Store verified name
          
          // Mark signature as verified in current session
          if (signatureType === "prepared") {
            this.preparedByVerifiedInSession = true;
          } else if (signatureType === "verified") {
            this.verifiedByVerifiedInSession = true;
          } else if (signatureType === "approved") {
            this.approvedByVerifiedInSession = true;
          }
          
          // Store user_id for approved signature (needed for notification)
          if (signatureType === "approved" && data.user_id) {
            this.approvedByUserId = data.user_id;
          }
          
          // Handle auto-submission and updates based on signature type
          if (signatureType === "prepared") {
            // CREATE new row when Prepared By signature is verified
            await this.autoSubmitReport();
          } else if (signatureType === "verified") {
            // UPDATE the same row when Verified By signature is fetched
            await this.updateReportSignature('verified');
          } else if (signatureType === "approved") {
            // UPDATE the same row when Approved By signature is fetched
            await this.updateReportSignature('approved');
          }
        } else {
          this[formData.error] = data.message || "Failed to verify signature";
          this[formData.signatureUrl] = "";
          this[formData.verifiedName] = "";
          this.reportData[formData.userField] = "";
        }
      } catch (error) {
        this[formData.error] = "Error verifying signature: " + error.message;
        this[formData.signatureUrl] = "";
        this[formData.verifiedName] = "";
        this.reportData[formData.userField] = "";
      }
    },
    async autoSubmitReport() {
      try {
        // Ensure all remarks are updated before submitting
        this.reportData.inspectionItems.forEach((item) => {
          if (item.observations) {
            this.computeRemarkForItem(item);
          }
        });
        
        const submissionData = this.prepareSubmissionData();
        
        const response = await fetch("http://localhost:5000/api/kit-of-parts", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(submissionData),
        });

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
          this.savedReportId = result.report_id;
          // Also set reportId if it wasn't set (for consistency)
          if (!this.reportId) {
            // Note: reportId is a prop, so we can't directly set it, but savedReportId will work
          }
          console.log(`✓ Report saved to database with ID: ${result.report_id}`);
          alert(`Report saved successfully! Report ID: ${result.report_id}`);
        } else {
          const errorMsg = result.message || "Unknown error occurred";
          console.error("Error submitting report:", errorMsg);
          alert(`Error submitting report: ${errorMsg}`);
        }
      } catch (error) {
        console.error("Error auto-submitting report:", error);
        alert(`Error submitting report: ${error.message}`);
      }
    },
    async updateReportSignature(signatureType) {
      const reportIdToUse = this.savedReportId || this.reportId;
      
      if (!reportIdToUse) {
        console.error("Report ID not found. Cannot update signature.");
        alert("Error: Report not found. Please complete the Prepared By signature first.");
        return;
      }

      try {
        const updateData = {};
        if (signatureType === "verified") {
          // Store signature URL in verified_by_g1h_qa_g field (format: "name|signature_url")
          updateData.verified_by_g1h_qa_g = `${this.reportData.verifiedBy}|${this.verifiedBySignatureUrl}`;
        } else if (signatureType === "approved") {
          // Store signature URL in approved_by field (format: "name|signature_url")
          updateData.approved_by = `${this.reportData.approvedBy}|${this.approvedBySignatureUrl}`;
        }

        // Update the existing record in the database
        const response = await fetch(
          `http://localhost:5000/api/kit-of-parts/${reportIdToUse}`,
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
            console.log(`Verified By signature updated in report ID: ${reportIdToUse}`);
            alert("Verified By signature saved successfully!");
          } else if (signatureType === "approved") {
            console.log(`Approved By signature updated in report ID: ${reportIdToUse}`);
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
    async loadReportData() {
      // Load report data from database when reportId is available
      const reportIdToLoad = this.reportId || this.$route?.params?.reportId;
      
      if (!reportIdToLoad) {
        console.log("No reportId available to load data");
        return;
      }

      try {
        const response = await fetch(
          `http://localhost:5000/api/kit-of-parts/${reportIdToLoad}`,
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

          // Set savedReportId if this is a loaded report
          if (report.report_id) {
            this.savedReportId = report.report_id;
          } else {
            // Fallback to using the reportIdToLoad
            this.savedReportId = reportIdToLoad;
          }

          // Map header fields
          this.reportData.projectName = report.projectName || "";
          this.reportData.reportRefNo = report.reportRefNo || "";
          this.reportData.memoRefNo = report.memoRefNo || "";
          this.reportData.lruName = report.lruName || "";
          this.reportData.sruName = report.sruName || "";
          this.reportData.dpName = report.dpName || "";
          this.reportData.partNo = report.partNo || "";
          this.reportData.inspectionStage = report.inspectionStage || "";
          this.reportData.testVenue = report.testVenue || "";
          this.reportData.quantity = report.quantity || null;
          this.reportData.slNos = report.slNos || "";
          this.reportData.startDate = report.startDate ? (typeof report.startDate === 'string' ? report.startDate.split('T')[0] : report.startDate) : "";
          this.reportData.endDate = report.endDate ? (typeof report.endDate === 'string' ? report.endDate.split('T')[0] : report.endDate) : "";
          this.reportData.dated1 = report.dated1 ? (typeof report.dated1 === 'string' ? report.dated1.split('T')[0] : report.dated1) : "";
          this.reportData.dated2 = report.dated2 ? (typeof report.dated2 === 'string' ? report.dated2.split('T')[0] : report.dated2) : "";

          // Map inspection items (test1-7)
          if (report.inspectionItems && Array.isArray(report.inspectionItems)) {
            for (let i = 0; i < Math.min(report.inspectionItems.length, 7); i++) {
              if (this.reportData.inspectionItems[i]) {
                const item = report.inspectionItems[i];
                this.reportData.inspectionItems[i].observations = item.observations || "";
                this.reportData.inspectionItems[i].remarks = item.remarks || "";
                this.reportData.inspectionItems[i].fileName = item.upload || "";
                
                // Compute remark if observation is set
                if (this.reportData.inspectionItems[i].observations) {
                  this.computeRemarkForItem(this.reportData.inspectionItems[i]);
                }
              }
            }
          }

          // Parse signature fields (format: "name|signature_url")
          // Only load signature URLs if form is readonly (viewing completed report)
          // If form is editable, user must verify signatures again in current session
          if (report.preparedBy) {
            const preparedParts = report.preparedBy.split("|");
            this.reportData.preparedBy = preparedParts[0] || "";
            // Only set signature URL if form is readonly (viewing completed report)
            if (this.readonly) {
              this.preparedBySignatureUrl = preparedParts[1] || "";
              this.preparedByVerifiedName = preparedParts[0] || "";
              // Mark as verified since we're viewing a completed report
              this.preparedByVerifiedInSession = true;
            }
          }

          if (report.verifiedBy) {
            const verifiedParts = report.verifiedBy.split("|");
            this.reportData.verifiedBy = verifiedParts[0] || "";
            // Only set signature URL if form is readonly (viewing completed report)
            if (this.readonly) {
              this.verifiedBySignatureUrl = verifiedParts[1] || "";
              this.verifiedByVerifiedName = verifiedParts[0] || "";
              // Mark as verified since we're viewing a completed report
              this.verifiedByVerifiedInSession = true;
            }
          }

          if (report.approvedBy) {
            const approvedParts = report.approvedBy.split("|");
            this.reportData.approvedBy = approvedParts[0] || "";
            // Only set signature URL if form is readonly (viewing completed report)
            if (this.readonly) {
              this.approvedBySignatureUrl = approvedParts[1] || "";
              this.approvedByVerifiedName = approvedParts[0] || "";
              // Mark as verified since we're viewing a completed report
              this.approvedByVerifiedInSession = true;
            }
          }

          console.log("✓ Report data loaded successfully:", reportIdToLoad);
        } else {
          console.error("Failed to load report data:", result.message);
        }
      } catch (error) {
        console.error("Error loading report data:", error);
      }
    },
    prepareSubmissionData() {
      // Prepare data for submission (reusable method)
      return {
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

        // Signatures (with signature URLs if available)
        preparedBy: this.preparedBySignatureUrl ? `${this.reportData.preparedBy}|${this.preparedBySignatureUrl}` : this.reportData.preparedBy,
        verifiedBy: this.verifiedBySignatureUrl ? `${this.reportData.verifiedBy}|${this.verifiedBySignatureUrl}` : this.reportData.verifiedBy,
        approvedBy: this.approvedBySignatureUrl ? `${this.reportData.approvedBy}|${this.approvedBySignatureUrl}` : this.reportData.approvedBy,
        
        // Link to original report card (if provided as prop)
        // Use report_card_id (preferred) but also support original_report_id for backward compatibility
        report_card_id: this.reportId,
        original_report_id: this.reportId, // Backward compatibility
      };
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
  gap: 20px;
  margin-top: 20px;
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
  transition: background-color 0.2s;
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
  padding: 10px;
  background-color: white;
  border-radius: 4px;
  border: 1px solid #28a745;
}

.signature-image-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.signature-image {
  max-width: 200px;
  max-height: 80px;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 5px;
  background-color: white;
}

.signature-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.signature-user {
  font-weight: 600;
  color: #333;
  font-size: 14px;
}

.signature-status {
  color: #28a745;
  font-size: 12px;
  font-weight: 600;
}

.signature-error {
  color: #dc3545;
  font-size: 12px;
  margin-top: 8px;
  padding: 8px;
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  border-radius: 4px;
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
