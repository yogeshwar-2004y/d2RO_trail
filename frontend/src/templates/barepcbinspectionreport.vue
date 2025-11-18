<template>
  <div class="bare-pcb-inspection-page">
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
        SUB : Bare PCB Inspection Report for {{ lruName }}
      </div>

      <!-- Inspection Form -->
      <form @submit.prevent="submitForm" class="inspection-form">
        <!-- General Information Section -->
        <div class="form-section">
          <h2 class="section-title">General Information</h2>
          <div class="general-info-grid">
            <!-- Left Column -->
            <div class="info-column">
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
                <label for="slNos">SL.NO's:</label>
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
            <div class="info-column">
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

        <!-- Inspection Checklist Section -->
        <div class="form-section">
          <h2 class="section-title">Inspection Checklist</h2>
          <div class="inspection-table-container">
            <table class="inspection-table">
              <thead>
                <tr>
                  <th>SL NO</th>
                  <th>PARAMETERS TO BE CHECKED</th>
                  <th>OBSERVATION</th>
                  <th>REMARKS (OK/NOT OK)</th>
                  <th>UPLOAD</th>
                </tr>
              </thead>
              <tbody>
                <!-- I. VISUAL INSPECTION -->
                <tr class="section-header">
                  <td colspan="5"><strong>I. VISUAL INSPECTION</strong></td>
                </tr>
                <tr
                  v-for="(item, index) in formData.visualInspection"
                  :key="'visual-' + index"
                >
                  <td>{{ index + 1 }}</td>
                  <td>{{ item.parameter }}</td>
                  <td>
                    <input
                      type="text"
                      v-model="item.observation"
                      :disabled="isPreparedByVerified"
                      placeholder="Enter observation"
                    />
                  </td>
                  <td>
                    <select
                      v-model="item.remarks"
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
                      @change="handleFileUpload($event, 'visual', index)"
                      :disabled="isPreparedByVerified"
                    />
                  </td>
                </tr>

                <!-- II. CONTINUITY CHECKING -->
                <tr class="section-header">
                  <td colspan="5"><strong>II. CONTINUITY CHECKING</strong></td>
                </tr>
                <tr
                  v-for="(item, index) in formData.continuityCheck"
                  :key="'continuity-' + index"
                >
                  <td>{{ index + 1 }}</td>
                  <td>{{ item.parameter }}</td>
                  <td>
                    <input
                      type="text"
                      v-model="item.observation"
                      :disabled="isPreparedByVerified"
                      placeholder="Enter observation"
                    />
                  </td>
                  <td>
                    <select
                      v-model="item.remarks"
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
                      @change="handleFileUpload($event, 'continuity', index)"
                      :disabled="isPreparedByVerified"
                    />
                  </td>
                </tr>

                <!-- III. FABRICATOR & VENDOR QC REPORTS VERIFICATION -->
                <tr class="section-header">
                  <td colspan="5">
                    <strong
                      >III. FABRICATOR & VENDOR QC REPORTS VERIFICATION</strong
                    >
                  </td>
                </tr>
                <tr>
                  <td>1</td>
                  <td class="description-cell">
                    (Fabricator Report shall be as per Mil 551101 (Mil QML
                    31032) Group A & B Certificates for Rigid boards and Mil
                    50884 for Flexi boards (or) IPC 6012 Class 3 DS)
                  </td>
                  <td>
                    <input
                      type="text"
                      v-model="formData.fabricatorReport.observation"
                      :disabled="isPreparedByVerified"
                      placeholder="Enter observation"
                    />
                  </td>
                  <td>
                    <select
                      v-model="formData.fabricatorReport.remarks"
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
                      @change="handleFileUpload($event, 'fabricator', 0)"
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
                  Please fill in all form fields (General Information and
                  Inspection Checklist) before verifying signature.
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
        <div
          class="form-actions"
          v-if="!readonly && isApprovedByVerified && !shouldHideSubmitButton"
        >
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
  name: "BarePcbInspectionReport",
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
        reportRefNo: "",
        memoRefNo: "",
        lruName: "",
        inspectionStage: "",
        testVenue: "",
        dpName: "",
        dated1: "",
        dated2: "",
        sruName: "",
        partNo: "",
        quantity: "",
        slNos: "",
        startDate: "",
        endDate: "",
        visualInspection: [
          {
            parameter: "CHECK FOR BONDING PROBLEM (DELAMINATION)",
            observation: "",
            remarks: "",
          },
          {
            parameter: "CHECK FOR SOLDER MASK OPENINGS",
            observation: "",
            remarks: "",
          },
          {
            parameter: "CHECK FOR BUBBLES ON PCB",
            observation: "",
            remarks: "",
          },
          {
            parameter: "CHECK FOR ANY DAMAGE TO THE PCB",
            observation: "",
            remarks: "",
          },
          {
            parameter: "ALL THROUGH HOLES SHOULD BE CLEAR",
            observation: "",
            remarks: "",
          },
          { parameter: "ALL VIAS TO BE MASKED", observation: "", remarks: "" },
          {
            parameter: "CHECK FOR SILK SCREEN (LEGEND) PRINTING",
            observation: "",
            remarks: "",
          },
          {
            parameter:
              "CHECK FOR PIN NO MARKING ON ICS, CONNECTORS & POLARITY OF DIODES, CAPACITORS etc.",
            observation: "",
            remarks: "",
          },
          {
            parameter: "CHECK FOR TRACKS NEAR MOUNTING HOLES",
            observation: "",
            remarks: "",
          },
          { parameter: "CHECK FOR PCB WARPAGE", observation: "", remarks: "" },
        ],
        continuityCheck: [
          {
            parameter: "CHECK FOR VCC TO GROUND CONTINUITY",
            observation: "",
            remarks: "",
          },
        ],
        fabricatorReport: {
          observation: "",
          remarks: "",
        },
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
        this.formData.reportRefNo &&
        this.formData.memoRefNo &&
        this.formData.lruName &&
        this.formData.dpName &&
        this.formData.sruName &&
        this.formData.partNo
      );
    },
    areAllFieldsFilled() {
      if (!this.isFormValid) return false;

      for (const item of this.formData.visualInspection) {
        if (!item.observation || !item.remarks) {
          return false;
        }
      }

      for (const item of this.formData.continuityCheck) {
        if (!item.observation || !item.remarks) {
          return false;
        }
      }

      if (
        !this.formData.fabricatorReport.observation ||
        !this.formData.fabricatorReport.remarks
      ) {
        return false;
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
        if (section === "visual") {
          this.formData.visualInspection[index].fileName = file.name;
        } else if (section === "continuity") {
          this.formData.continuityCheck[index].fileName = file.name;
        } else if (section === "fabricator") {
          this.formData.fabricatorReport.fileName = file.name;
        }
      }
    },
    async loadReportData(reportCardId) {
      try {
        const response = await fetch(
          `http://localhost:5000/api/reports/bare-pcb-inspection/by-report-card/${reportCardId}`
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
          this.formData.dpName = report.dp_name || "";
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

          // Map visual inspection data (obs1-obs10)
          if (this.formData.visualInspection.length >= 10) {
            for (let i = 0; i < 10; i++) {
              const obsKey = `obs${i + 1}`;
              const remKey = `rem${i + 1}`;
              const uploadKey = `upload${i + 1}`;
              this.formData.visualInspection[i].observation =
                report[obsKey] || "";
              this.formData.visualInspection[i].remarks = report[remKey] || "";
              this.formData.visualInspection[i].fileName =
                report[uploadKey] || null;
            }
          }

          // Map continuity check data (obs11)
          if (this.formData.continuityCheck.length >= 1) {
            this.formData.continuityCheck[0].observation = report.obs11 || "";
            this.formData.continuityCheck[0].remarks = report.rem11 || "";
            this.formData.continuityCheck[0].fileName = report.upload11 || null;
          }

          // Map fabricator report data (obs12)
          this.formData.fabricatorReport.observation = report.obs12 || "";
          this.formData.fabricatorReport.remarks = report.rem12 || "";
          this.formData.fabricatorReport.fileName = report.upload12 || null;

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
        const response = await fetch(
          "http://localhost:5000/api/users/verify-signature",
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              username: signature.signatureUsername,
              signature_password: signature.signaturePassword,
            }),
          }
        );

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
        inspection_count: this.inspectionCount,
        start_date: this.formData.startDate,
        end_date: this.formData.endDate,
        dated1: this.formData.dated1,
        dated2: this.formData.dated2,

        // Visual inspection data (10 items)
        visual_inspection: this.formData.visualInspection,

        // Continuity check data (1 item)
        continuity_check: this.formData.continuityCheck,

        // Fabricator report data
        fabricator_report: this.formData.fabricatorReport,

        prepared_by: this.signatures.preparedBy.signatureUrl || "",
        verified_by: this.signatures.verifiedBy.signatureUrl || "",
        approved_by: this.signatures.approvedBy.signatureUrl || "",
      };
    },
    async autoSaveReport() {
      try {
        const reportCardId = this.reportId || this.$route.params.reportId;
        if (!reportCardId) return;

        const submissionData = this.prepareSubmissionData();
        const response = await fetch(
          "http://localhost:5000/api/reports/bare-pcb-inspection",
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(submissionData),
          }
        );

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
        const submissionData = this.prepareSubmissionData();
        const response = await fetch(
          "http://localhost:5000/api/reports/bare-pcb-inspection",
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(submissionData),
          }
        );

        const result = await response.json();

        if (result.success) {
          // Update report status after submission
          const reportCardId = this.reportId || this.$route.params.reportId;
          if (reportCardId) {
            await this.fetchReportStatus(reportCardId);
          }
          alert(
            "Bare PCB inspection report submitted successfully! Notifications have been sent."
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
        const response = await fetch(
          `http://localhost:5000/api/reports/${reportCardId}`
        );
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
  },
};
</script>

<style scoped>
.bare-pcb-inspection-page {
  min-height: 100vh;
  background: #ebf7fd;
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

.section-header {
  background-color: #f0f4f8 !important;
  font-weight: bold;
  color: #2d3748;
}

.section-header td {
  padding: 12px 8px;
  border-bottom: 2px solid #2d3748;
}

.description-cell {
  font-size: 0.8em;
  line-height: 1.4;
  max-width: 300px;
}

.inspection-table input[type="text"],
.inspection-table select {
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

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* Readonly styles */
input[readonly],
select:disabled,
input:disabled {
  background-color: #f8f9fa;
  color: #6c757d;
  cursor: not-allowed;
  opacity: 0.8;
}

input[readonly]:focus,
select:disabled:focus {
  outline: none;
  box-shadow: none;
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
