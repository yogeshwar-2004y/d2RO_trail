<template>
  <div class="raw-material-inspection-page">
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
        SUB : Raw Material Inspection Report for {{ lruName }}
      </div>

      <!-- Inspection Form -->
      <form @submit.prevent="submitForm" class="inspection-form">
        <div class="report-container">
          <div class="report-info">
            <div>
              <strong>Project Name:</strong>
              <input
                v-model="formData.projectName"
                type="text"
                :disabled="isFormReadonly"
              />
            </div>
            <div>
              <strong>Report Ref No:</strong>
              <input
                v-model="formData.reportRefNo"
                type="text"
                :disabled="isFormReadonly"
              />
            </div>
            <div>
              <strong>Memo Ref No:</strong>
              <input
                v-model="formData.memoRefNo"
                type="text"
                :disabled="isFormReadonly"
              />
            </div>
            <div>
              <strong>LRU Name:</strong>
              <input
                v-model="formData.lruName"
                type="text"
                :disabled="isFormReadonly"
              />
            </div>
            <div>
              <strong>DP Name:</strong>
              <input
                v-model="formData.dpName"
                type="text"
                :disabled="isFormReadonly"
              />
            </div>
            <div>
              <strong>Part No:</strong>
              <input
                v-model="formData.partNo"
                type="text"
                :disabled="isFormReadonly"
              />
            </div>
            <div>
              <strong>SL No's:</strong>
              <input
                v-model="formData.slNos"
                type="text"
                :disabled="isFormReadonly"
              />
            </div>
            <div>
              <strong>End Date:</strong>
              <input
                v-model="formData.endDate"
                type="date"
                :disabled="isFormReadonly"
              />
            </div>
            <div>
              <strong>SRU Name:</strong>
              <input
                v-model="formData.sruName"
                type="text"
                :disabled="isFormReadonly"
              />
            </div>
            <div>
              <strong>Start Date:</strong>
              <input
                v-model="formData.startDate"
                type="date"
                :disabled="isFormReadonly"
              />
            </div>
            <div>
              <strong>Inspection Stage:</strong>
              <input
                v-model="formData.inspectionStage"
                type="text"
                :disabled="isFormReadonly"
              />
            </div>
            <div>
              <strong>Test Venue:</strong>
              <input
                v-model="formData.testVenue"
                type="text"
                :disabled="isFormReadonly"
              />
            </div>
            <div>
              <strong>Quantity:</strong>
              <input
                v-model="formData.quantity"
                type="number"
                :disabled="isFormReadonly"
              />
            </div>
            <div>
              <strong>Dated:</strong>
              <input
                v-model="formData.dated1"
                type="date"
                :disabled="isFormReadonly"
              />
            </div>
            <div>
              <strong>Dated:</strong>
              <input
                v-model="formData.dated2"
                type="date"
                :disabled="isFormReadonly"
              />
            </div>
          </div>

          <table class="inspection-table">
            <thead>
              <tr>
                <th>SL.NO</th>
                <th>CHECK POINTS</th>
                <th>APPLICABILITY (A / NA)</th>
                <th>COMPLIANCE (YES / NO)</th>
                <th>REMARKS (OK / NOT OK)</th>
                <th>UPLOAD</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(checkpoint, index) in formData.checkPoints"
                :key="index"
              >
                <td>{{ index + 1 }}</td>
                <td>{{ checkpoint.description }}</td>
                <td>{{ checkpoint.applicability }}</td>
                <td>
                  <select
                    v-model="checkpoint.compliance"
                    @change="updateRemarks(index)"
                    :disabled="isFormReadonly"
                  >
                    <option value="">Select</option>
                    <option value="YES">YES</option>
                    <option value="NO">NO</option>
                  </select>
                </td>
                <td>
                  <input
                    v-model="checkpoint.remarks"
                    type="text"
                    readonly
                    :disabled="true"
                    class="remarks-readonly"
                  />
                </td>
                <td>
                  <input
                    type="file"
                    :disabled="isFormReadonly"
                    @change="handleFileUpload($event, 'checkpoint', index)"
                  />
                </td>
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
                    :disabled="
                      isFormReadonly ||
                      !areAllFieldsFilled ||
                      !preparedByUsername ||
                      !preparedByPassword
                    "
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
                      <span class="signature-user">{{
                        preparedByVerifiedName
                      }}</span>
                      <span class="signature-role" v-if="preparedByVerifiedRole"
                        >{{ preparedByVerifiedRole }} Signature</span
                      >
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
                    :disabled="
                      !preparedBySignatureUrl ||
                      !verifiedByUsername ||
                      !verifiedByPassword
                    "
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
                      <span class="signature-user">{{
                        verifiedByVerifiedName
                      }}</span>
                      <span class="signature-role" v-if="verifiedByVerifiedRole"
                        >{{ verifiedByVerifiedRole }} Signature</span
                      >
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
                    :disabled="
                      !verifiedBySignatureUrl ||
                      !approvedByUsername ||
                      !approvedByPassword
                    "
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
                      <span class="signature-user">{{
                        approvedByVerifiedName
                      }}</span>
                      <span class="signature-role" v-if="approvedByVerifiedRole"
                        >{{ approvedByVerifiedRole }} Signature</span
                      >
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
        <div
          class="form-actions final-submit"
          v-if="isFormReadonly && approvedBySignatureUrl"
        >
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
  name: "RawMaterialInspectionReport",
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
      formData: {
        projectName: "",
        reportRefNo: "",
        memoRefNo: "",
        lruName: "",
        inspectionStage: "",
        testVenue: "",
        dpName: "",
        dated1: "",
        dated2: "",
        sruName: "",
        quantity: "",
        startDate: "",
        partNo: "",
        slNos: "",
        endDate: "",
        checkPoints: [
          {
            description:
              "Dimensions of the Raw Materials Received as per Certificate",
            applicability: "Applicable",
            compliance: "",
            remarks: "",
          },
          {
            description: "CoC of Raw Materials",
            applicability: "Applicable",
            compliance: "",
            remarks: "",
          },
          {
            description: "Chemical Reports as specified in QAP",
            applicability: "Not Applicable",
            compliance: "",
            remarks: "",
          },
          {
            description: "Tensile Strength",
            applicability: "Applicable",
            compliance: "",
            remarks: "",
          },
          {
            description: "Hardness Test Results as specified in QAP",
            applicability: "Not Applicable",
            compliance: "",
            remarks: "",
          },
          {
            description: "UT Test",
            applicability: "Applicable",
            compliance: "",
            remarks: "",
          },
          {
            description: "Any Other Observations:",
            applicability: "NIL",
            compliance: "",
            remarks: "",
          },
        ],
      },
      overallStatus: "",
      qualityRating: null,
      recommendations: "",
      preparedBy: "",
      preparedByUsername: "",
      preparedByPassword: "",
      preparedBySignatureUrl: "",
      preparedByVerifiedName: "",
      preparedByVerifiedRole: "",
      preparedByError: "",
      verifiedBy: "",
      verifiedByUsername: "",
      verifiedByPassword: "",
      verifiedBySignatureUrl: "",
      verifiedByVerifiedName: "",
      verifiedByVerifiedRole: "",
      verifiedByError: "",
      approvedBy: "",
      approvedByUsername: "",
      approvedByPassword: "",
      approvedBySignatureUrl: "",
      approvedByVerifiedName: "",
      approvedByVerifiedRole: "",
      approvedByError: "",
      approvedByUserId: null,
      preparedByUserId: null,
      reportId: null,  // This will be set to the raw material inspection report ID after saving
      parentReportCardId: null,  // Store the parent report card ID (from props/route) separately
    };
  },
  computed: {
    isFormReadonly() {
      // Form becomes readonly once Prepared By signature is verified
      // This ensures form cannot be changed after Prepared By signature is added
      const hasPreparedBySignature =
        this.preparedBySignatureUrl &&
        this.preparedBySignatureUrl.trim() !== "";

      // Once Prepared By signature exists, form is readonly (reportId will be set by autoSubmitReport)
      // We check for reportId as well to ensure the save was successful
      const hasReportId = this.reportId !== null && this.reportId !== undefined;

      // Form is readonly if Prepared By signature exists and report is saved
      if (hasPreparedBySignature && hasReportId) {
        return true;
      }

      // If Prepared By signature exists but reportId doesn't yet (still saving),
      // still make form readonly to prevent changes during save
      if (hasPreparedBySignature) {
        return true;
      }

      return false;
    },
    isFormValid() {
      return (
        this.formData.projectName &&
        this.formData.reportRefNo &&
        this.formData.memoRefNo &&
        this.formData.lruName &&
        this.formData.dpName &&
        this.formData.sruName &&
        this.formData.partNo
      );
    },
    areAllFieldsFilled() {
      const basicFieldsFilled =
        this.formData.projectName &&
        this.formData.reportRefNo &&
        this.formData.memoRefNo &&
        this.formData.lruName &&
        this.formData.dpName &&
        this.formData.sruName &&
        this.formData.partNo &&
        this.formData.startDate &&
        this.formData.endDate &&
        this.formData.inspectionStage &&
        this.formData.testVenue &&
        this.formData.slNos;

      const allCheckpointsFilled = this.formData.checkPoints.every(
        (checkpoint) => checkpoint.compliance && checkpoint.remarks
      );

      return basicFieldsFilled && allCheckpointsFilled;
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
    this.formData.sruName = this.lruName;

    // Capture the parent report card ID from props or route params
    // This should be stored in report_card_id column in the database
    this.parentReportCardId = 
      this.reportId ||  // From props (parent report card ID)
      this.$route?.params?.reportCardId ||
      this.$route?.params?.report_id ||
      this.$route?.params?.reportId ||
      null;

    // Load existing report data using report_card_id (parent report card ID)
    // The backend will query raw_material_inspection_report table by report_card_id foreign key
    if (this.parentReportCardId) {
      this.$nextTick(() => {
        this.loadReportData();
      });
    }
    
    console.log("Mounted - parentReportCardId:", this.parentReportCardId, "reportId prop:", this.reportId);
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
    updateRemarks(index) {
      const checkpoint = this.formData.checkPoints[index];
      if (!checkpoint.compliance) {
        checkpoint.remarks = "";
        return;
      }

      const applicability = checkpoint.applicability;
      const compliance = checkpoint.compliance;

      // Logic based on applicability and compliance
      if (applicability === "Applicable") {
        // If Applicable and YES -> OK, if NO -> NOT OK
        checkpoint.remarks = compliance === "YES" ? "OK" : "NOT OK";
      } else if (applicability === "Not Applicable") {
        // If Not Applicable and NO -> OK, if YES -> NOT OK
        checkpoint.remarks = compliance === "NO" ? "OK" : "NOT OK";
      } else if (applicability === "NIL") {
        // If NIL and NO -> OK, else NOT OK
        checkpoint.remarks = compliance === "NO" ? "OK" : "NOT OK";
      } else {
        // Default fallback
        checkpoint.remarks = "";
      }
    },
    async saveDraft() {
      try {
        const reportData = this.prepareReportData();
        const response = await fetch(
          "http://localhost:5000/api/reports/raw-material-inspection",
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
        this.formData = {
          projectName: this.projectName,
          lruName: this.lruName,
          reportRefNo: "",
          memoRefNo: "",
          inspectionStage: "",
          testVenue: "",
          dpName: "",
          dated1: "",
          dated2: "",
          sruName: this.lruName,
          quantity: "",
          startDate: this.currentDate,
          partNo: "",
          slNos: "",
          endDate: "",
          checkPoints: [
            {
              description:
                "Dimensions of the Raw Materials Received as per Certificate",
              applicability: "Applicable",
              compliance: "",
              remarks: "",
            },
            {
              description: "CoC of Raw Materials",
              applicability: "Applicable",
              compliance: "",
              remarks: "",
            },
            {
              description: "Chemical Reports as specified in QAP",
              applicability: "Not Applicable",
              compliance: "",
              remarks: "",
            },
            {
              description: "Tensile Strength",
              applicability: "Applicable",
              compliance: "",
              remarks: "",
            },
            {
              description: "Hardness Test Results as specified in QAP",
              applicability: "Not Applicable",
              compliance: "",
              remarks: "",
            },
            {
              description: "UT Test",
              applicability: "Applicable",
              compliance: "",
              remarks: "",
            },
            {
              description: "Any Other Observations:",
              applicability: "NIL",
              compliance: "",
              remarks: "",
            },
          ],
        };
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
          userField: "preparedBy",
        };
      } else if (signatureType === "verified") {
        username = this.verifiedByUsername;
        password = this.verifiedByPassword;
        formData = {
          signatureUrl: "verifiedBySignatureUrl",
          verifiedName: "verifiedByVerifiedName",
          error: "verifiedByError",
          userField: "verifiedBy",
        };
      } else if (signatureType === "approved") {
        username = this.approvedByUsername;
        password = this.approvedByPassword;
        formData = {
          signatureUrl: "approvedBySignatureUrl",
          verifiedName: "approvedByVerifiedName",
          error: "approvedByError",
          userField: "approvedBy",
        };
      }

      if (!username || !password) {
        this[formData.error] =
          "Please enter both username and signature password";
        return;
      }

      try {
        const response = await fetch(
          "http://localhost:5000/api/users/verify-signature",
          {
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
          // Store verified role for display
          if (signatureType === "prepared") {
            this.preparedByVerifiedRole = data.role_name || "";
          } else if (signatureType === "verified") {
            this.verifiedByVerifiedRole = data.role_name || "";
          } else if (signatureType === "approved") {
            this.approvedByVerifiedRole = data.role_name || "";
          }
          this[formData.error] = "";
          this[formData.userField] = data.user_name;

          // Store user_id for activity logging
          if (signatureType === "prepared" && data.user_id) {
            this.preparedByUserId = data.user_id;
          } else if (signatureType === "approved" && data.user_id) {
            this.approvedByUserId = data.user_id;
          }

          if (signatureType === "prepared") {
            // For Prepared By: save to database and make form readonly
            await this.autoSubmitReport();
          } else if (signatureType === "verified") {
            // For Verified By: update database with signature
            await this.updateReportSignature("verified");
          } else if (signatureType === "approved") {
            // For Approved By: update database with signature
            await this.updateReportSignature("approved");
            // Notify QA Heads about approval
            await this.notifyApproval();
          }
        } else {
          this[formData.error] = data.message || "Failed to verify signature";
          this[formData.signatureUrl] = "";
          this[formData.verifiedName] = "";
          if (signatureType === "prepared") {
            this.preparedByVerifiedRole = "";
          } else if (signatureType === "verified") {
            this.verifiedByVerifiedRole = "";
          } else if (signatureType === "approved") {
            this.approvedByVerifiedRole = "";
          }
          this[formData.userField] = "";
        }
      } catch (error) {
        this[formData.error] = "Error verifying signature: " + error.message;
        this[formData.signatureUrl] = "";
        this[formData.verifiedName] = "";
        if (signatureType === "prepared") {
          this.preparedByVerifiedRole = "";
        } else if (signatureType === "verified") {
          this.verifiedByVerifiedRole = "";
        } else if (signatureType === "approved") {
          this.approvedByVerifiedRole = "";
        }
        this[formData.userField] = "";
      }
    },
    async autoSubmitReport() {
      try {
        console.log("Starting autoSubmitReport - saving form data to database...");
        
        // Update all remarks before submitting
        this.formData.checkPoints.forEach((checkpoint, index) => {
          if (checkpoint.compliance) {
            this.updateRemarks(index);
          }
        });

        const reportData = this.prepareReportData();
        console.log("Prepared report data:", reportData);
        
        const response = await fetch(
          "http://localhost:5000/api/reports/raw-material-inspection",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(reportData),
          }
        );

        console.log("API Response status:", response.status, response.statusText);

        if (!response.ok) {
          const errorText = await response.text();
          console.error("API Error Response:", errorText);
          let errorMessage = `Failed to submit report: ${response.status} ${response.statusText}`;
          try {
            const errorData = JSON.parse(errorText);
            errorMessage = errorData.message || errorMessage;
            console.error("Parsed error message:", errorMessage);
          } catch (e) {
            console.error("Could not parse error response:", e);
            errorMessage = errorText || errorMessage;
          }
          throw new Error(errorMessage);
        }

        const result = await response.json();
        console.log("API Response result:", result);

        if (result.success && result.report_id) {
          this.reportId = result.report_id;
          console.log(
            `✓ Report saved to database with ID: ${result.report_id}`
          );
          console.log(`✓ Form is now readonly - inputs cannot be changed`);
          alert(
            `Report saved successfully! Report ID: ${result.report_id}\n\nThe form is now locked. You can proceed with Verified By and Approved By signatures.`
          );
        } else {
          const errorMsg = result.message || "Unknown error occurred";
          console.error("Error submitting report - no success:", errorMsg);
          alert(`Error submitting report: ${errorMsg}`);
          // Don't clear signature if there's an error - allow retry
        }
      } catch (error) {
        console.error("Error auto-submitting report:", error);
        console.error("Error details:", error.message, error.stack);
        alert(`Error submitting report: ${error.message || "Please try again."}`);
        // Clear signature on error so user can retry
        this.preparedBySignatureUrl = "";
        this.preparedByVerifiedName = "";
        this.preparedBy = "";
      }
    },
    async updateReportSignature(signatureType) {
      if (!this.reportId) {
        console.error("Report ID not found. Cannot update signature.");
        alert(
          "Error: Report not found. Please complete the Prepared By signature first."
        );
        return;
      }
      try {
        const updateData = {};
        if (signatureType === "verified") {
          updateData.verified_by = `${this.verifiedBy}|${this.verifiedBySignatureUrl}`;
        } else if (signatureType === "approved") {
          updateData.approved_by = `${this.approvedBy}|${this.approvedBySignatureUrl}`;
        }

        const response = await fetch(
          `http://localhost:5000/api/reports/raw-material-inspection/${this.reportId}`,
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
            console.log(
              `Verified By signature updated in report ID: ${this.reportId}`
            );
            alert("Verified By signature saved successfully!");
          } else if (signatureType === "approved") {
            console.log(
              `Approved By signature updated in report ID: ${this.reportId}`
            );
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
        alert(
          "Error: Report not found. Please complete the Prepared By signature first."
        );
        return;
      }

      if (!this.approvedBySignatureUrl) {
        alert("Please complete the Approved By signature first.");
        return;
      }

      try {
        // Notify QA Heads and log to activity logs
        await this.notifyQAHeads();
        alert(
          "Report submitted successfully! Activity logged and QA Heads have been notified."
        );
        console.log("Report submitted with ID:", this.reportId);
      } catch (error) {
        console.error("Error submitting report:", error);
        alert("Error submitting report. Please try again.");
      }
    },
    async notifyQAHeads() {
      try {
        // Get current user from session/localStorage
        const currentUser = JSON.parse(localStorage.getItem("user") || "{}");
        const reviewerId = currentUser.user_id || null;

        if (!reviewerId) {
          console.error("Reviewer ID not found");
          return;
        }

        // Send notification to backend
        const response = await fetch(
          "http://localhost:5000/api/reports/raw-material-inspection/notify",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              report_id: this.reportId,
              memo_ref_no: this.formData.memoRefNo,
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
    async loadReportData() {
      // Load report data from database using report_card_id (foreign key in raw_material_inspection_report table)
      // The backend will query by report_card_id first, then fallback to report_id
      const reportCardIdToLoad = this.parentReportCardId;

      if (!reportCardIdToLoad) {
        console.log("No report card ID available to load data");
        return;
      }

      try {
        console.log(`Loading raw material inspection report with report_card_id: ${reportCardIdToLoad}`);
        const response = await fetch(
          `http://localhost:5000/api/reports/raw-material-inspection/${reportCardIdToLoad}`,
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
            },
          }
        );

        if (!response.ok) {
          if (response.status === 404) {
            console.log(`Report with report_card_id ${reportCardIdToLoad} not found`);
            return;
          }
          throw new Error(`Failed to fetch report: ${response.statusText}`);
        }

        const result = await response.json();

        if (result.success && result.report) {
          const report = result.report;

          // Set reportId to the raw material inspection report ID from the response
          this.reportId = report.report_id;

          // Map header fields to formData
          this.formData.projectName = report.project_name || "";
          this.formData.reportRefNo = report.report_ref_no || "";
          this.formData.memoRefNo = report.memo_ref_no || "";
          this.formData.lruName = report.lru_name || "";
          this.formData.sruName = report.sru_name || "";
          this.formData.dpName = report.dp_name || "";
          this.formData.partNo = report.part_no || "";
          this.formData.inspectionStage = report.inspection_stage || "";
          this.formData.testVenue = report.test_venue || "";
          this.formData.quantity = report.quantity || null;
          this.formData.slNos = report.sl_nos || "";
          this.serialNumber = report.serial_number || this.serialNumber;
          
          // Update projectName and lruName from loaded data
          if (report.project_name) {
            this.projectName = report.project_name;
          }
          if (report.lru_name) {
            this.lruName = report.lru_name;
          }

          // Format dates
          this.formData.startDate = report.start_date
            ? typeof report.start_date === "string"
              ? report.start_date.split("T")[0]
              : report.start_date
            : "";
          this.formData.endDate = report.end_date
            ? typeof report.end_date === "string"
              ? report.end_date.split("T")[0]
              : report.end_date
            : "";
          this.formData.dated1 = report.dated1
            ? typeof report.dated1 === "string"
              ? report.dated1.split("T")[0]
              : report.dated1
            : "";
          this.formData.dated2 = report.dated2
            ? typeof report.dated2 === "string"
              ? report.dated2.split("T")[0]
              : report.dated2
            : "";

          // Map summary fields
          this.overallStatus = report.overall_status || "";
          this.qualityRating = report.quality_rating || null;
          this.recommendations = report.recommendations || "";

          // Convert applicability from DB format ('A', 'NA') to display format
          const convertApplicability = (applicability) => {
            if (applicability === "A") return "Applicable";
            if (applicability === "NA") return "Not Applicable";
            return applicability || "Applicable";
          };

          // Map checkpoints from database format (applicability1-7, compliance1-7, rem1-7, upload1-7)
          for (let i = 0; i < 7; i++) {
            const index = i + 1;
            if (this.formData.checkPoints[i]) {
              const dbApplicability = report[`applicability${index}`];
              this.formData.checkPoints[i].applicability = convertApplicability(dbApplicability);
              this.formData.checkPoints[i].compliance = report[`compliance${index}`] || "";
              this.formData.checkPoints[i].remarks = report[`rem${index}`] || "";
              this.formData.checkPoints[i].upload = report[`upload${index}`] || "";
              
              // Update remarks based on compliance if needed
              if (this.formData.checkPoints[i].compliance) {
                this.updateRemarks(i);
              }
            }
          }

          // Parse signature fields (format: "name|signature_url")
          if (report.prepared_by) {
            const parts = report.prepared_by.split("|");
            this.preparedBy = parts[0] || "";
            this.preparedBySignatureUrl = parts[1] || "";
            this.preparedByVerifiedName = parts[0] || "";
          }

          if (report.verified_by) {
            const parts = report.verified_by.split("|");
            this.verifiedBy = parts[0] || "";
            this.verifiedBySignatureUrl = parts[1] || "";
            this.verifiedByVerifiedName = parts[0] || "";
          }

          if (report.approved_by) {
            const parts = report.approved_by.split("|");
            this.approvedBy = parts[0] || "";
            this.approvedBySignatureUrl = parts[1] || "";
            this.approvedByVerifiedName = parts[0] || "";
          }

          // Update parent report card ID if available (should already be set)
          if (report.report_card_id) {
            this.parentReportCardId = report.report_card_id;
          }

          console.log("✓ Report data loaded successfully:", report.report_id);
        } else {
          console.error("Failed to load report data:", result.message);
        }
      } catch (error) {
        console.error("Error loading report data:", error);
      }
    },
    async notifyApproval() {
      try {
        if (!this.reportId) {
          console.error(
            "Report ID not found. Cannot send approval notification."
          );
          return;
        }

        if (!this.approvedByUserId) {
          console.error(
            "Approved By User ID not found. Cannot send approval notification."
          );
          return;
        }

        // Send approval notification to backend
        const response = await fetch(
          "http://localhost:5000/api/reports/raw-material-inspection/notify-approval",
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
          console.error(
            "Failed to send approval notification:",
            result.message
          );
        }
      } catch (error) {
        console.error("Error notifying QA Heads about approval:", error);
        // Don't throw error - approval signature should still be saved even if notification fails
      }
    },
    prepareReportData() {
      // Use parentReportCardId which was captured in mounted()
      // This is the parent report card ID (from reports table) that should be stored in report_card_id column
      const reportCardId = this.parentReportCardId;
      
      console.log("Preparing report data - report_card_id:", reportCardId, "parentReportCardId:", this.parentReportCardId);

      // Helper function to convert applicability to database format
      const convertApplicability = (applicability) => {
        if (applicability === "Applicable") return "A";
        if (applicability === "Not Applicable") return "NA";
        if (applicability === "NIL") return "NA"; // Convert NIL to NA for database constraint
        return applicability; // Return as-is if already in correct format
      };

      return {
        report_card_id: reportCardId ? (typeof reportCardId === 'number' ? reportCardId : parseInt(reportCardId)) : null,
        project_name: this.formData.projectName,
        report_ref_no: this.formData.reportRefNo,
        memo_ref_no: this.formData.memoRefNo,
        lru_name: this.formData.lruName,
        sru_name: this.formData.sruName,
        dp_name: this.formData.dpName,
        part_no: this.formData.partNo,
        inspection_stage: this.formData.inspectionStage,
        test_venue: this.formData.testVenue,
        quantity: this.formData.quantity || null,
        sl_nos: this.formData.slNos,
        serial_number: this.serialNumber,
        start_date: this.formData.startDate,
        end_date: this.formData.endDate,
        dated1: this.formData.dated1,
        dated2: this.formData.dated2,
        checkPoints: this.formData.checkPoints.map((checkpoint) => ({
          description: checkpoint.description,
          applicability: convertApplicability(checkpoint.applicability),
          compliance: checkpoint.compliance,
          remarks: checkpoint.remarks,
          upload: checkpoint.upload || "",
        })),
        overall_status: this.overallStatus || "",
        quality_rating: this.qualityRating || null,
        recommendations: this.recommendations || "",
        prepared_by: this.preparedBySignatureUrl
          ? `${this.preparedBy}|${this.preparedBySignatureUrl}`
          : this.preparedBy,
        prepared_by_user_id: this.preparedByUserId || null,  // For activity logging
        verified_by: this.verifiedBySignatureUrl
          ? `${this.verifiedBy}|${this.verifiedBySignatureUrl}`
          : this.verifiedBy,
        approved_by: this.approvedBySignatureUrl
          ? `${this.approvedBy}|${this.approvedBySignatureUrl}`
          : this.approvedBy,
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
        doc.text("RAW MATERIAL INSPECTION REPORT", pageWidth / 2, yPosition, {
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
        const subjectText = `SUB: Raw Material Inspection Report for ${
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
          `Report Ref No: ${this.formData.reportRefNo || "Not specified"}`,
          `Memo Ref No: ${this.formData.memoRefNo || "Not specified"}`,
          `LRU Name: ${this.formData.lruName || "Not specified"}`,
          `DP Name: ${this.formData.dpName || "Not specified"}`,
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

        // Check points table
        doc.setFont("helvetica", "bold");
        doc.text("Check Points:", margin, yPosition);
        yPosition += 8;

        if (this.formData.checkPoints && this.formData.checkPoints.length > 0) {
          doc.setFontSize(9);
          doc.setFont("helvetica", "bold");

          // Table headers
          doc.text("SL.NO", margin, yPosition);
          doc.text("CHECK POINTS", margin + 15, yPosition);
          doc.text("APPLICABILITY", margin + 100, yPosition);
          doc.text("COMPLIANCE", margin + 130, yPosition);
          doc.text("REMARKS", margin + 160, yPosition);
          yPosition += 6;

          // Table data
          doc.setFont("helvetica", "normal");
          this.formData.checkPoints.forEach((checkpoint, index) => {
            doc.text((index + 1).toString(), margin, yPosition);
            doc.text(
              checkpoint.description.substring(0, 30),
              margin + 15,
              yPosition
            );
            doc.text(checkpoint.applicability || "", margin + 100, yPosition);
            doc.text(checkpoint.compliance || "", margin + 130, yPosition);
            doc.text(checkpoint.remarks || "", margin + 160, yPosition);
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
        const fileName = `Raw_Material_Inspection_Report_${
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
.raw-material-inspection-page {
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
  min-width: 100px;
}

.report-info input[type="text"],
.report-info input[type="date"],
.report-info input[type="number"] {
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

.remarks-readonly {
  width: 95%;
  border: 1px solid #e0e0e0;
  padding: 5px;
  box-sizing: border-box;
  background-color: #f5f5f5;
  color: #333;
  cursor: not-allowed;
  font-weight: 500;
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

.signature-role {
  font-weight: 500;
  color: #155724;
  font-size: 12px;
  font-style: italic;
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

  .report-footer {
    flex-direction: column;
    gap: 20px;
  }
}
</style>
