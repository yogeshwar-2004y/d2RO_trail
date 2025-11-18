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
                :disabled="isPreparedByVerified"
                required
              />
            </div>
            <div class="form-group">
              <label for="dpName">DP Name:</label>
              <input
                type="text"
                id="dpName"
                v-model="formData.dpName"
                :disabled="isPreparedByVerified"
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
                  :disabled="isPreparedByVerified"
                  required
                />
              </div>
              <div class="form-group">
                <label for="memoRefNo">Memo Ref No:</label>
                <input
                  type="text"
                  id="memoRefNo"
                  v-model="formData.memoRefNo"
                  :disabled="isPreparedByVerified"
                  required
                />
              </div>
              <div class="form-group">
                <label for="lruName">LRU Name:</label>
                <input
                  type="text"
                  id="lruName"
                  v-model="formData.lruName"
                  :disabled="isPreparedByVerified"
                  required
                />
              </div>
              <div class="form-group">
                <label for="inspectionStage">Inspection Stage:</label>
                <input
                  type="text"
                  id="inspectionStage"
                  v-model="formData.inspectionStage"
                  :disabled="isPreparedByVerified"
                  required
                />
              </div>
              <div class="form-group">
                <label for="testVenue">Test Venue:</label>
                <input
                  type="text"
                  id="testVenue"
                  v-model="formData.testVenue"
                  :disabled="isPreparedByVerified"
                  required
                />
              </div>
              <div class="form-group">
                <label for="slNos">SL.NO'S:</label>
                <input
                  type="text"
                  id="slNos"
                  v-model="formData.slNos"
                  :disabled="isPreparedByVerified"
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
                  :disabled="isPreparedByVerified"
                  required
                />
              </div>
              <div class="form-group">
                <label for="dated2">Dated:</label>
                <input
                  type="date"
                  id="dated2"
                  v-model="formData.dated2"
                  :disabled="isPreparedByVerified"
                  required
                />
              </div>
              <div class="form-group">
                <label for="sruName">SRU Name:</label>
                <input
                  type="text"
                  id="sruName"
                  v-model="formData.sruName"
                  :disabled="isPreparedByVerified"
                  required
                />
              </div>
              <div class="form-group">
                <label for="partNo">Part No:</label>
                <input
                  type="text"
                  id="partNo"
                  v-model="formData.partNo"
                  :disabled="isPreparedByVerified"
                  required
                />
              </div>
              <div class="form-group">
                <label for="quantity">Quantity:</label>
                <input
                  type="number"
                  id="quantity"
                  v-model="formData.quantity"
                  :disabled="isPreparedByVerified"
                  required
                />
              </div>
              <div class="form-group">
                <label for="startDate">Start Date:</label>
                <input
                  type="date"
                  id="startDate"
                  v-model="formData.startDate"
                  :disabled="isPreparedByVerified"
                  required
                />
              </div>
              <div class="form-group">
                <label for="endDate">End Date:</label>
                <input
                  type="date"
                  id="endDate"
                  v-model="formData.endDate"
                  :disabled="isPreparedByVerified"
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
                    <select
                      v-model="testCase.testNature"
                      :disabled="isPreparedByVerified"
                    >
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
                    <select
                      v-model="testCase.remarks"
                      :disabled="isPreparedByVerified"
                    >
                      <option value="">Select</option>
                      <option value="OK">OK</option>
                      <option value="NOT OK">NOT OK</option>
                    </select>
                  </td>
                  <td>
                    <input
                      type="file"
                      @change="handleFileUpload($event, 'testCase', index)"
                      :disabled="isPreparedByVerified"
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
            <!-- Prepared By Signature -->
            <div class="signature-item">
              <label>Prepared By:</label>
              <div class="signature-auth-container">
                <div
                  v-if="!canAccessSignatures"
                  class="signature-disabled-message"
                >
                  Signature authentication is only available for QA Reviewer and
                  QA Head.
                </div>
                <div
                  v-else-if="!areAllFieldsFilled"
                  class="signature-disabled-message"
                >
                  Please fill in all form fields (Report Details and Test Cases)
                  before verifying signature.
                </div>
                <div v-else class="signature-inputs">
                  <div class="input-group">
                    <label>Username:</label>
                    <input
                      type="text"
                      v-model="signatures.preparedBy.signatureUsername"
                      placeholder="Enter username..."
                      :disabled="!isPreparedByEnabled"
                    />
                  </div>
                  <div class="input-group">
                    <label>Signature Password:</label>
                    <input
                      type="password"
                      v-model="signatures.preparedBy.signaturePassword"
                      placeholder="Enter signature password..."
                      :disabled="!isPreparedByEnabled"
                    />
                  </div>
                  <button
                    type="button"
                    class="btn btn-verify"
                    @click="
                      verifySignature('preparedBy');
                      $event.target.blur();
                    "
                    :disabled="
                      !isPreparedByEnabled ||
                      !signatures.preparedBy.signatureUsername ||
                      !signatures.preparedBy.signaturePassword
                    "
                  >
                    Verify & Load Signature
                  </button>
                </div>
                <div
                  v-if="signatures.preparedBy.signatureUrl"
                  class="signature-display"
                >
                  <label>Verified Signature:</label>
                  <div class="signature-image-container">
                    <img
                      :src="signatures.preparedBy.signatureUrl"
                      alt="Verified Signature"
                      class="signature-image"
                    />
                    <div class="signature-info">
                      <span class="signature-user">{{
                        signatures.preparedBy.verifiedUserName
                      }}</span>
                      <span class="signature-role"
                        >{{
                          signatures.preparedBy.verifiedUserRole
                        }}
                        Signature</span
                      >
                      <span class="signature-status">✓ Verified</span>
                    </div>
                  </div>
                </div>
                <div
                  v-if="signatures.preparedBy.signatureError"
                  class="signature-error"
                >
                  {{ signatures.preparedBy.signatureError }}
                </div>
              </div>
            </div>

            <!-- Verified By Signature -->
            <div class="signature-item">
              <label>Verified By:</label>
              <div class="signature-auth-container">
                <div
                  v-if="!canAccessSignatures"
                  class="signature-disabled-message"
                >
                  Signature authentication is only available for QA Reviewer and
                  QA Head.
                </div>
                <div
                  v-else-if="!isPreparedByVerified"
                  class="signature-disabled-message"
                >
                  Please complete "Prepared By" signature first.
                </div>
                <div v-else class="signature-inputs">
                  <div class="input-group">
                    <label>Username:</label>
                    <input
                      type="text"
                      v-model="signatures.verifiedBy.signatureUsername"
                      placeholder="Enter username..."
                      :disabled="!isVerifiedByEnabled"
                    />
                  </div>
                  <div class="input-group">
                    <label>Signature Password:</label>
                    <input
                      type="password"
                      v-model="signatures.verifiedBy.signaturePassword"
                      placeholder="Enter signature password..."
                      :disabled="!isVerifiedByEnabled"
                    />
                  </div>
                  <button
                    type="button"
                    class="btn btn-verify"
                    @click="
                      verifySignature('verifiedBy');
                      $event.target.blur();
                    "
                    :disabled="
                      !isVerifiedByEnabled ||
                      !signatures.verifiedBy.signatureUsername ||
                      !signatures.verifiedBy.signaturePassword
                    "
                  >
                    Verify & Load Signature
                  </button>
                </div>
                <div
                  v-if="signatures.verifiedBy.signatureUrl"
                  class="signature-display"
                >
                  <label>Verified Signature:</label>
                  <div class="signature-image-container">
                    <img
                      :src="signatures.verifiedBy.signatureUrl"
                      alt="Verified Signature"
                      class="signature-image"
                    />
                    <div class="signature-info">
                      <span class="signature-user">{{
                        signatures.verifiedBy.verifiedUserName
                      }}</span>
                      <span class="signature-role"
                        >{{
                          signatures.verifiedBy.verifiedUserRole
                        }}
                        Signature</span
                      >
                      <span class="signature-status">✓ Verified</span>
                    </div>
                  </div>
                </div>
                <div
                  v-if="signatures.verifiedBy.signatureError"
                  class="signature-error"
                >
                  {{ signatures.verifiedBy.signatureError }}
                </div>
              </div>
            </div>

            <!-- Approved By Signature -->
            <div class="signature-item">
              <label>Approved By:</label>
              <div class="signature-auth-container">
                <div
                  v-if="!canAccessSignatures"
                  class="signature-disabled-message"
                >
                  Signature authentication is only available for QA Reviewer and
                  QA Head.
                </div>
                <div
                  v-else-if="!isVerifiedByVerified"
                  class="signature-disabled-message"
                >
                  Please complete "Verified By" signature first.
                </div>
                <div v-else class="signature-inputs">
                  <div class="input-group">
                    <label>Username:</label>
                    <input
                      type="text"
                      v-model="signatures.approvedBy.signatureUsername"
                      placeholder="Enter username..."
                      :disabled="!isApprovedByEnabled"
                    />
                  </div>
                  <div class="input-group">
                    <label>Signature Password:</label>
                    <input
                      type="password"
                      v-model="signatures.approvedBy.signaturePassword"
                      placeholder="Enter signature password..."
                      :disabled="!isApprovedByEnabled"
                    />
                  </div>
                  <button
                    type="button"
                    class="btn btn-verify"
                    @click="
                      verifySignature('approvedBy');
                      $event.target.blur();
                    "
                    :disabled="
                      !isApprovedByEnabled ||
                      !signatures.approvedBy.signatureUsername ||
                      !signatures.approvedBy.signaturePassword
                    "
                  >
                    Verify & Load Signature
                  </button>
                </div>
                <div
                  v-if="signatures.approvedBy.signatureUrl"
                  class="signature-display"
                >
                  <label>Verified Signature:</label>
                  <div class="signature-image-container">
                    <img
                      :src="signatures.approvedBy.signatureUrl"
                      alt="Verified Signature"
                      class="signature-image"
                    />
                    <div class="signature-info">
                      <span class="signature-user">{{
                        signatures.approvedBy.verifiedUserName
                      }}</span>
                      <span class="signature-role"
                        >{{
                          signatures.approvedBy.verifiedUserRole
                        }}
                        Signature</span
                      >
                      <span class="signature-status">✓ Verified</span>
                    </div>
                  </div>
                </div>
                <div
                  v-if="signatures.approvedBy.signatureError"
                  class="signature-error"
                >
                  {{ signatures.approvedBy.signatureError }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="form-actions" v-if="!readonly && isApprovedByVerified && !shouldHideSubmitButton">
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
import { userStore } from "@/stores/userStore";

export default {
  name: "CotsScreeningInspectionReport",
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
      reportStatus: null, // Store report status to check if submitted
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
      },
      signatures: {
        preparedBy: {
          signatureUsername: "",
          signaturePassword: "",
          signatureUrl: "",
          verifiedUserName: "",
          verifiedUserRole: "",
          signatureError: "",
        },
        verifiedBy: {
          signatureUsername: "",
          signaturePassword: "",
          signatureUrl: "",
          verifiedUserName: "",
          verifiedUserRole: "",
          signatureError: "",
        },
        approvedBy: {
          signatureUsername: "",
          signaturePassword: "",
          signatureUrl: "",
          verifiedUserName: "",
          verifiedUserRole: "",
          signatureError: "",
        },
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
    areAllFieldsFilled() {
      if (!this.isFormValid) return false;

      for (const testCase of this.formData.testCases) {
        if (!testCase.testNature || !testCase.remarks) {
          return false;
        }
      }

      return true;
    },
    canAccessSignatures() {
      const currentUserRole = userStore.getters.currentUserRole();
      return currentUserRole === 2 || currentUserRole === 3;
    },
    isPreparedByVerified() {
      return !!this.signatures.preparedBy.signatureUrl;
    },
    isVerifiedByVerified() {
      return !!this.signatures.verifiedBy.signatureUrl;
    },
    isApprovedByVerified() {
      return !!this.signatures.approvedBy.signatureUrl;
    },
    isPreparedByEnabled() {
      return this.canAccessSignatures && this.areAllFieldsFilled;
    },
    isVerifiedByEnabled() {
      return this.canAccessSignatures && this.isPreparedByVerified;
    },
    isApprovedByEnabled() {
      return this.canAccessSignatures && this.isVerifiedByVerified;
    },
    shouldHideSubmitButton() {
      // Hide submit button for reviewers and heads after report is submitted
      const currentUserRole = userStore.getters.currentUserRole();
      const isQAReviewer = currentUserRole === 3;
      const isQAHead = currentUserRole === 2;
      
      // For QA Reviewer and QA Head: hide only after submission
      if (isQAReviewer || isQAHead) {
        // Check if report is submitted (status is not 'ASSIGNED')
        return this.reportStatus && this.reportStatus !== "ASSIGNED";
      }
      
      // For all other roles: always hide
      return true;
    },
  },
  mounted() {
    const reportCardId = this.reportId || this.$route.params.reportId;

    if (reportCardId) {
      this.loadReportData(reportCardId);
      this.fetchReportStatus(reportCardId);
    } else {
      // Get parameters from route
      this.lruName = this.$route.params.lruName || "";
      this.projectName = this.$route.params.projectName || "";

      // Set default values
      this.formData.lruName = this.lruName;
      this.formData.projectName = this.projectName;
      this.formData.startDate = this.currentDate;
    }
  },
  methods: {
    handleFileUpload(event, section, index) {
      const file = event.target.files[0];
      if (file) {
        if (section === "testCase") {
          this.formData.testCases[index].fileName = file.name;
        }
      }
    },
    async loadReportData(reportCardId) {
      try {
        const response = await fetch(
          `http://localhost:8000/api/reports/cot-screening/by-report-card/${reportCardId}`
        );

        if (!response.ok) {
          if (response.status === 404) {
            // Report doesn't exist yet, show empty form
            this.lruName = this.$route.params.lruName || "";
            this.projectName = this.$route.params.projectName || "";
            this.formData.lruName = this.lruName;
            this.formData.projectName = this.projectName;
            this.formData.startDate = this.currentDate;
            return;
          }
          throw new Error(
            `Failed to fetch report: ${response.statusText} (${response.status})`
          );
        }

        const result = await response.json();

        if (result.success && result.report) {
          const report = result.report;

          // Map report details
          this.formData.projectName = report.project_name || "";
          this.formData.dpName = report.dp_name || "";
          this.formData.reportRefNo = report.report_ref_no || "";
          this.formData.memoRefNo = report.memo_ref_no || "";
          this.formData.lruName = report.lru_name || "";
          this.formData.inspectionStage = report.inspection_stage || "";
          this.formData.testVenue = report.test_venue || "";
          this.formData.slNos = report.sl_nos || "";
          this.formData.dated1 = report.dated1
            ? report.dated1.split("T")[0]
            : "";
          this.formData.dated2 = report.dated2
            ? report.dated2.split("T")[0]
            : "";
          this.formData.sruName = report.sru_name || "";
          this.formData.partNo = report.part_no || "";
          this.formData.quantity = report.quantity || "";
          this.formData.startDate = report.start_date
            ? report.start_date.split("T")[0]
            : this.currentDate;
          this.formData.endDate = report.end_date
            ? report.end_date.split("T")[0]
            : "";

          this.projectName = report.project_name || "";
          this.lruName = report.lru_name || "";
          this.serialNumber = report.serial_number || this.serialNumber;
          this.inspectionCount =
            report.inspection_count || this.inspectionCount;

          // Map test cases data
          if (this.formData.testCases.length >= 3) {
            this.formData.testCases[0].testNature = report.test_nature1 || "";
            this.formData.testCases[0].remarks = report.rem1 || "";
            this.formData.testCases[0].fileName = report.upload1 || null;

            this.formData.testCases[1].testNature = report.test_nature2 || "";
            this.formData.testCases[1].remarks = report.rem2 || "";
            this.formData.testCases[1].fileName = report.upload2 || null;

            this.formData.testCases[2].testNature = report.test_nature3 || "";
            this.formData.testCases[2].remarks = report.rem3 || "";
            this.formData.testCases[2].fileName = report.upload3 || null;
          }

          // Load signatures
          if (report.prepared_by) {
            this.signatures.preparedBy.signatureUrl = report.prepared_by;
          }
          if (report.verified_by) {
            this.signatures.verifiedBy.signatureUrl = report.verified_by;
          }
          if (report.approved_by) {
            this.signatures.approvedBy.signatureUrl = report.approved_by;
          }
        } else {
          throw new Error(result.message || "Failed to load report data");
        }
      } catch (error) {
        if (
          error.message.includes("404") ||
          error.message.includes("not found")
        ) {
          return;
        }
        alert(`Error loading report data: ${error.message}. Please try again.`);
      }
    },
    async verifySignature(signatureType) {
      const signature = this.signatures[signatureType];

      if (!signature.signatureUsername || !signature.signaturePassword) {
        signature.signatureError =
          "Please enter both username and signature password";
        return;
      }

      try {
        const response = await fetch("http://localhost:8000/api/users/verify-signature", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            username: signature.signatureUsername,
            signature_password: signature.signaturePassword,
          }),
        });

        const data = await response.json();

        if (data.success) {
          signature.signatureUrl = data.signature_url;
          signature.verifiedUserName = data.user_name;
          signature.verifiedUserRole = data.role_name;
          signature.signatureError = "";
          await this.autoSaveReport();
        } else {
          signature.signatureError =
            data.message || "Failed to verify signature";
          signature.signatureUrl = "";
          signature.verifiedUserName = "";
          signature.verifiedUserRole = "";
        }
      } catch (error) {
        signature.signatureError =
          "Error verifying signature: " + error.message;
        signature.signatureUrl = "";
        signature.verifiedUserName = "";
        signature.verifiedUserRole = "";
      }
    },
    prepareSubmissionData() {
      const reportCardId = this.reportId || this.$route.params.reportId;

      return {
        report_card_id: reportCardId,
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

        test_nature1: this.formData.testCases[0]?.testNature || "",
        rem1: this.formData.testCases[0]?.remarks || "",
        upload1: this.formData.testCases[0]?.fileName || "",

        test_nature2: this.formData.testCases[1]?.testNature || "",
        rem2: this.formData.testCases[1]?.remarks || "",
        upload2: this.formData.testCases[1]?.fileName || "",

        test_nature3: this.formData.testCases[2]?.testNature || "",
        rem3: this.formData.testCases[2]?.remarks || "",
        upload3: this.formData.testCases[2]?.fileName || "",

        prepared_by: this.signatures.preparedBy.signatureUrl || "",
        verified_by: this.signatures.verifiedBy.signatureUrl || "",
        approved_by: this.signatures.approvedBy.signatureUrl || "",
      };
    },
    async autoSaveReport() {
      try {
        const reportCardId = this.reportId || this.$route.params.reportId;
        if (!reportCardId) return;

        const userRole = userStore.getters.currentUserRole();
        const submissionData = this.prepareSubmissionData();
        const response = await fetch(`http://localhost:8000/api/reports/cot-screening?user_role=${userRole}`, {
              method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(submissionData),
        });

        const result = await response.json();
        if (!result.success) {
          console.error(`Auto-save failed: ${result.message}`);
        }
      } catch (error) {
        console.error("Error auto-saving report:", error);
      }
    },
    async submitForm() {
      if (!this.isFormValid) {
        alert("Please fill in all required fields.");
        return;
      }

      try {
        const userRole = userStore.getters.currentUserRole();
        const submissionData = this.prepareSubmissionData();
        const response = await fetch(`http://localhost:8000/api/reports/cot-screening?user_role=${userRole}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(submissionData),
        });

        const result = await response.json();

        if (result.success) {
          // Update report status after submission
          const reportCardId = this.reportId || this.$route.params.reportId;
          if (reportCardId) {
            await this.fetchReportStatus(reportCardId);
          }
          alert(
            "COTS Screening inspection report submitted successfully! Notifications have been sent."
          );
        } else {
          alert(`Error: ${result.message}`);
        }
      } catch (error) {
        console.error("Error submitting report:", error);
        alert("Error submitting report. Please try again.");
      }
    },
    async fetchReportStatus(reportCardId) {
      try {
        const response = await fetch(`http://localhost:8000/api/reports/${reportCardId}`);
        if (response.ok) {
          const result = await response.json();
          if (result.success && result.report) {
            this.reportStatus = result.report.status;
          }
        }
      } catch (error) {
        console.error("Error fetching report status:", error);
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
  background: #ebf7fd;
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
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin-top: 1rem;
}

.signature-item {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.signature-item > label {
  font-weight: bold;
  color: #333;
  font-size: 1rem;
  align-self: flex-start;
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
  gap: 15px;
  margin-bottom: 15px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.input-group label {
  font-weight: 600;
  color: #333;
  font-size: 14px;
}

.input-group input {
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.3s ease;
}

.input-group input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.25);
}

.input-group input:disabled {
  background-color: #e9ecef;
  cursor: not-allowed;
  opacity: 0.6;
}

.signature-disabled-message {
  padding: 15px;
  background-color: #fff3cd;
  color: #856404;
  border: 1px solid #ffc107;
  border-radius: 4px;
  font-size: 14px;
  text-align: center;
  font-style: italic;
}

.btn.btn-verify {
  background-color: #667eea;
  color: white;
  border: none !important;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: background-color 0.3s ease;
  align-self: flex-start;
  outline: none !important;
  box-shadow: none !important;
}

.btn.btn-verify:hover:not(:disabled) {
  background-color: #5a6fd8;
  outline: none !important;
  box-shadow: none !important;
}

.btn.btn-verify:focus,
.btn.btn-verify:focus-visible,
.btn.btn-verify:focus-within {
  outline: none !important;
  box-shadow: none !important;
  background-color: #667eea;
  border: none !important;
}

.btn.btn-verify:active:not(:disabled) {
  background-color: #5a6fd8;
  box-shadow: none !important;
  outline: none !important;
  border: none !important;
}

.btn.btn-verify:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
  outline: none !important;
  box-shadow: none !important;
  border: none !important;
}

.signature-display {
  margin-top: 15px;
  padding: 15px;
  background-color: #e8f5e8;
  border: 1px solid #28a745;
  border-radius: 6px;
}

.signature-display label {
  font-weight: 600;
  color: #155724;
  margin-bottom: 10px;
  display: block;
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
  padding: 5px;
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
  color: #666;
  font-size: 12px;
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
  color: #721c24;
  border: 1px solid #f5c6cb;
  border-radius: 4px;
  font-size: 14px;
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
    grid-template-columns: 1fr;
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
