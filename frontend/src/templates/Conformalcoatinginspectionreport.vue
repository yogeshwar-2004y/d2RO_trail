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
                    v-model="projectName"
                    :disabled="isFormReadonly"
                    required
                  />
                </div>
                <div class="form-group">
                  <label for="reportRefNo">Report Ref No:</label>
                  <input
                    type="text"
                    id="reportRefNo"
                    v-model="reportRefNo"
                    :disabled="isFormReadonly"
                    required
                  />
                </div>
                <div class="form-group">
                  <label for="memoRefNo">Memo Ref No:</label>
                  <input
                    type="text"
                    id="memoRefNo"
                    v-model="memoRefNo"
                    :disabled="isFormReadonly"
                  />
                </div>
                <div class="form-group">
                  <label for="lruName">LRU Name:</label>
                  <input
                    type="text"
                    id="lruName"
                    v-model="lruName"
                    :disabled="isFormReadonly"
                    required
                  />
                </div>
                <div class="form-group">
                  <label for="inspectionStage">Inspection Stage:</label>
                  <input
                    type="text"
                    id="inspectionStage"
                    v-model="inspectionStage"
                    :disabled="isFormReadonly"
                  />
                </div>
                <div class="form-group">
                  <label for="testVenue">Test Venue:</label>
                  <input
                    type="text"
                    id="testVenue"
                    v-model="testVenue"
                    :disabled="isFormReadonly"
                  />
                </div>
                <div class="form-group">
                  <label for="slNo">SL.NO'S:</label>
                  <input
                    type="text"
                    id="slNo"
                    v-model="slNo"
                    :disabled="isFormReadonly"
                  />
                </div>
              </div>

              <!-- Right Column -->
              <div class="info-column">
                <div class="form-group">
                  <label for="dpName">DP Name:</label>
                  <input
                    type="text"
                    id="dpName"
                    v-model="dpName"
                    :disabled="isFormReadonly"
                    required
                  />
                </div>
                <div class="form-group">
                  <label for="dated1">Dated:</label>
                  <input
                    type="date"
                    id="dated1"
                    v-model="dated1"
                    :disabled="isFormReadonly"
                  />
                </div>
                <div class="form-group">
                  <label for="dated2">Dated:</label>
                  <input
                    type="date"
                    id="dated2"
                    v-model="dated2"
                    :disabled="isFormReadonly"
                  />
                </div>
                <div class="form-group">
                  <label for="sruName">SRU Name:</label>
                  <input
                    type="text"
                    id="sruName"
                    v-model="sruName"
                    :disabled="isFormReadonly"
                  />
                </div>
                <div class="form-group">
                  <label for="partNo">Part No:</label>
                  <input
                    type="text"
                    id="partNo"
                    v-model="partNo"
                    :disabled="isFormReadonly"
                    required
                  />
                </div>
                <div class="form-group">
                  <label for="quantity">Quantity:</label>
                  <input
                    type="number"
                    id="quantity"
                    v-model.number="quantity"
                    :disabled="isFormReadonly"
                    min="1"
                    required
                  />
                </div>
                <div class="form-group">
                  <label for="startDate">Start Date:</label>
                  <input
                    type="date"
                    id="startDate"
                    v-model="startDate"
                    :disabled="isFormReadonly"
                  />
                </div>
                <div class="form-group">
                  <label for="endDate">End Date:</label>
                  <input
                    type="date"
                    id="endDate"
                    v-model="endDate"
                    :disabled="isFormReadonly"
                  />
                </div>
              </div>
            </div>
          </div>
          <!-- Inspection Tests Section -->
          <div class="form-section">
            <h2 class="section-title">Inspection Tests</h2>
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
                  <select
                    v-model="test.observation"
                    @change="updateRemark(test)"
                    :disabled="isFormReadonly"
                  >
                    <option value="">Select</option>
                    <option
                      v-if="test.case === 'Connectors surrounding and beneath'"
                      value="no damages"
                    >
                      no damages
                    </option>
                    <option
                      v-if="test.case === 'Connectors surrounding and beneath'"
                      value="damages present"
                    >
                      damages present
                    </option>
                    <option
                      v-if="test.case !== 'Connectors surrounding and beneath'"
                      value="yes"
                    >
                      yes
                    </option>
                    <option
                      v-if="test.case !== 'Connectors surrounding and beneath'"
                      value="no"
                    >
                      no
                    </option>
                  </select>
                </td>
                <td>
                  <input
                    v-model="test.remark"
                    type="text"
                    :disabled="true"
                    readonly
                  />
                </td>
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
export default {
  name: "Conformalcoatinginspectionreport",
  props: {
    readonly: {
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
      approvedByUserId: null,
      reportId: null,
      memoRefNo: "",
      quantity: null,
      dated1: "",
      dated2: "",
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
        {
          case: "Uniformity in coating across the board",
          expected: "yes",
          observation: "",
          remark: "",
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
    isFormReadonly() {
      const hasPreparedBySignature =
        this.preparedBySignatureUrl &&
        this.preparedBySignatureUrl.trim() !== "";
      const hasReportId = this.reportId !== null && this.reportId !== undefined;

      if (hasPreparedBySignature && hasReportId) {
        return true;
      }

      return false;
    },
    areAllFieldsFilled() {
      const basicFieldsFilled =
        this.projectName &&
        this.reportRefNo &&
        this.dpName &&
        this.partNo &&
        this.slNo &&
        this.sruName &&
        this.startDate &&
        this.endDate &&
        this.inspectionStage &&
        this.testVenue;

      const allObservationsFilled = this.tests.every(
        (test) => test.observation && test.observation.trim() !== ""
      );

      return basicFieldsFilled && allObservationsFilled;
    },
  },
  mounted() {
    this.lruName = this.$route.params.lruName || "";
    this.projectName = this.$route.params.projectName || "";
    this.sruName = this.lruName;
    this.projectName = this.projectName;
    this.startDate = this.currentDate;

    const reportIdToLoad = this.reportId || this.$route?.params?.reportId;
    if (reportIdToLoad) {
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
    "$route.params.reportId": {
      handler(newVal) {
        if (newVal) {
          this.reportId = newVal;
          this.loadReportData();
        }
      },
      immediate: false,
    },
  },
  methods: {
    async loadReportData() {
      const reportIdToLoad = this.reportId || this.$route?.params?.reportId;

      if (!reportIdToLoad) {
        return;
      }

      try {
        const response = await fetch(
          `http://localhost:8000/api/reports/conformal-coating-inspection/${reportIdToLoad}`,
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

          this.reportId = report.report_id;
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
          this.startDate = report.start_date
            ? typeof report.start_date === "string"
              ? report.start_date.split("T")[0]
              : report.start_date
            : "";
          this.endDate = report.end_date
            ? typeof report.end_date === "string"
              ? report.end_date.split("T")[0]
              : report.end_date
            : "";
          this.dated1 = report.dated1
            ? typeof report.dated1 === "string"
              ? report.dated1.split("T")[0]
              : report.dated1
            : "";
          this.dated2 = report.dated2
            ? typeof report.dated2 === "string"
              ? report.dated2.split("T")[0]
              : report.dated2
            : "";

          for (let i = 1; i <= 9; i++) {
            if (this.tests[i - 1]) {
              this.tests[i - 1].observation = report[`obs${i}`] || "";
              this.tests[i - 1].remark = report[`rem${i}`] || "";
              this.tests[i - 1].upload = report[`upload${i}`] || "";
              this.tests[i - 1].expected =
                report[`expected${i}`] || this.tests[i - 1].expected;

              if (this.tests[i - 1].observation) {
                this.updateRemark(this.tests[i - 1]);
              }
            }
          }

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
        }
      } catch (error) {
        // Error loading report data - silently fail
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
          "http://localhost:8000/api/users/verify-signature",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              username: username,
              signature_password: password,
            }),
          }
        );

        const data = await response.json();

        if (data.success) {
          this[formData.signatureUrl] = data.signature_url;
          this[formData.verifiedName] = data.user_name;
          this[formData.error] = "";
          this[formData.userField] = data.user_name;

          if (signatureType === "approved" && data.user_id) {
            this.approvedByUserId = data.user_id;
          }

          if (signatureType === "prepared") {
            await this.autoSubmitReport();
          } else if (signatureType === "verified") {
            await this.updateReportSignature("verified");
          } else if (signatureType === "approved") {
            await this.updateReportSignature("approved");
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

      const observation = test.observation.toLowerCase().trim();
      const expected = test.expected.toLowerCase().trim();

      if (observation === expected) {
        test.remark = "OK";
      } else {
        test.remark = "NOT OK";
      }
    },
    async autoSubmitReport() {
      try {
        this.tests.forEach((test) => {
          if (test.observation) {
            this.updateRemark(test);
          }
        });

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
          alert(`Report saved successfully! Report ID: ${result.report_id}`);
        } else {
          const errorMsg = result.message || "Unknown error occurred";
          alert(`Error submitting report: ${errorMsg}`);
        }
      } catch (error) {
        alert("Error submitting report. Please try again.");
      }
    },
    async updateReportSignature(signatureType) {
      if (!this.reportId) {
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

        if (!this.reportId) {
          alert(
            "Error: Report not found. Please complete the Prepared By signature first."
          );
          return;
        }

        const response = await fetch(
          `http://localhost:8000/api/reports/conformal-coating-inspection/${this.reportId}`,
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
            alert("Verified By signature saved successfully!");
          } else if (signatureType === "approved") {
            alert("Report finalized successfully!");
          }
        } else {
          alert(`Error updating report: ${result.message}`);
        }
      } catch (error) {
        alert("Error updating report. Please try again.");
      }
    },
    async submitForm() {
      if (this.reportId && this.approvedBySignatureUrl) {
        await this.finalSubmitReport();
      } else {
        if (!this.reportId) {
          alert("Please complete the Prepared By signature first.");
        } else if (!this.approvedBySignatureUrl) {
          alert("Please complete the Approved By signature first.");
        }
      }
    },
    async finalSubmitReport() {
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
        await this.notifyQAHeads();
        alert(
          "Report submitted successfully! Activity logged and QA Heads have been notified."
        );
      } catch (error) {
        alert("Error submitting report. Please try again.");
      }
    },
    async notifyQAHeads() {
      try {
        const currentUser = JSON.parse(localStorage.getItem("user") || "{}");
        const reviewerId = currentUser.user_id || null;

        if (!reviewerId) {
          return;
        }

        const response = await fetch(
          "http://localhost:8000/api/reports/conformal-coating-inspection/notify",
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
          throw new Error(result.message);
        }
      } catch (error) {
        throw error;
      }
    },
    async notifyApproval() {
      try {
        if (!this.reportId || !this.approvedByUserId) {
          return;
        }

        const response = await fetch(
          "http://localhost:8000/api/reports/conformal-coating-inspection/notify-approval",
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
        if (!result.success) {
          throw new Error(result.message);
        }
      } catch (error) {
        // Don't throw error - approval signature should still be saved even if notification fails
      }
    },
    prepareReportData() {
      const originalReportId = this.reportId;
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
        prepared_by: this.preparedBySignatureUrl
          ? `${this.preparedBy}|${this.preparedBySignatureUrl}`
          : this.preparedBy,
        verified_by: this.verifiedBySignatureUrl
          ? `${this.verifiedBy}|${this.verifiedBySignatureUrl}`
          : this.verifiedBy,
        approved_by: this.approvedBySignatureUrl
          ? `${this.approvedBy}|${this.approvedBySignatureUrl}`
          : this.approvedBy,
        report_card_id: originalReportId,
        original_report_id: originalReportId,
      };
    },
  },
};
</script>

<style scoped>
.conformal-coating-inspection-page {
  min-height: 100vh;
  background: #f5f5f5;
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

.form-group input:disabled {
  background-color: #e9ecef;
  cursor: not-allowed;
  opacity: 0.6;
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
