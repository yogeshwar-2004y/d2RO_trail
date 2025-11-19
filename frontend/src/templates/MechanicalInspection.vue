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
                  :disabled="isPreparedByVerified"
                  required
                />
              </div>
              <div class="form-group">
                <label for="reportRefNo">Report Ref No:</label>
                <input
                  type="text"
                  id="reportRefNo"
                  v-model="reportData.reportRefNo"
                  :disabled="isPreparedByVerified"
                  required
                />
              </div>
              <div class="form-group">
                <label for="memoRefNo">Memo Ref No:</label>
                <input
                  type="text"
                  id="memoRefNo"
                  v-model="reportData.memoRefNo"
                  :disabled="isPreparedByVerified"
                />
              </div>
              <div class="form-group">
                <label for="lruName">LRU Name:</label>
                <input
                  type="text"
                  id="lruName"
                  v-model="reportData.lruName"
                  :disabled="isPreparedByVerified"
                  required
                />
              </div>
              <div class="form-group">
                <label for="inspectionStage">Inspection Stage:</label>
                <input
                  type="text"
                  id="inspectionStage"
                  v-model="reportData.inspectionStage"
                  :disabled="isPreparedByVerified"
                />
              </div>
              <div class="form-group">
                <label for="testVenue">Test Venue:</label>
                <input
                  type="text"
                  id="testVenue"
                  v-model="reportData.testVenue"
                  :disabled="isPreparedByVerified"
                />
              </div>
              <div class="form-group">
                <label for="slNos">SL.NO'S:</label>
                <input
                  type="text"
                  id="slNos"
                  v-model="reportData.slNos"
                  :disabled="isPreparedByVerified"
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
                  v-model="reportData.dpName"
                  :disabled="isPreparedByVerified"
                  required
                />
              </div>
              <div class="form-group">
                <label for="dated1">Dated:</label>
                <input
                  type="date"
                  id="dated1"
                  v-model="reportData.dated1"
                  :disabled="isPreparedByVerified"
                />
              </div>
              <div class="form-group">
                <label for="dated2">Dated:</label>
                <input
                  type="date"
                  id="dated2"
                  v-model="reportData.dated2"
                  :disabled="isPreparedByVerified"
                />
              </div>
              <div class="form-group">
                <label for="sruName">SRU Name:</label>
                <input
                  type="text"
                  id="sruName"
                  v-model="reportData.sruName"
                  :disabled="isPreparedByVerified"
                />
              </div>
              <div class="form-group">
                <label for="partNo">Part No:</label>
                <input
                  type="text"
                  id="partNo"
                  v-model="reportData.partNo"
                  :disabled="isPreparedByVerified"
                  required
                />
              </div>
              <div class="form-group">
                <label for="quantity">Quantity:</label>
                <input
                  type="number"
                  id="quantity"
                  v-model.number="reportData.quantity"
                  :disabled="isPreparedByVerified"
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
                  :disabled="isPreparedByVerified"
                />
              </div>
              <div class="form-group">
                <label for="endDate">End Date:</label>
                <input
                  type="date"
                  id="endDate"
                  v-model="reportData.endDate"
                  :disabled="isPreparedByVerified"
                />
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
                <tr class="table-header">
                  <th>SL NO</th>
                  <th>DIMENSION <br />(As Per Drawing)</th>
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
                    <div class="dimension-input-wrapper">
                      <input
                        type="text"
                        v-model="item.dimension"
                        :placeholder="`Enter ${
                          item.label?.toLowerCase() || 'dimension'
                        }`"
                        class="dimension-input"
                        :disabled="isPreparedByVerified"
                        @input="computeRemarks(item)"
                      />
                      <span class="dimension-unit">{{ item.unit }}</span>
                    </div>
                  </td>
                  <td>
                    <input
                      type="text"
                      v-model="item.tolerance"
                      placeholder="Enter tolerance"
                      :disabled="isPreparedByVerified"
                      @input="computeRemarks(item)"
                    />
                    <span class="dimension-unit">{{ item.unit }}</span>
                  </td>
                  <td>
                    <input
                      type="text"
                      v-model="item.observedValue"
                      placeholder="Enter observed value"
                      :disabled="isPreparedByVerified"
                      @input="computeRemarks(item)"
                    />
                  </td>
                  <td>
                    <input
                      type="text"
                      v-model="item.instrumentUsed"
                      placeholder="Enter instrument"
                      :disabled="isPreparedByVerified"
                    />
                  </td>
                  <td>
                    <span
                      class="remarks-computed"
                      :class="{
                        ok: item.remarks === 'OK',
                        not_ok: item.remarks === 'NOT OK',
                      }"
                    >
                      {{ item.remarks || "-" }}
                    </span>
                  </td>
                  <td>
                    <input
                      type="file"
                      :disabled="isPreparedByVerified"
                      @change="handleFileUpload($event, item)"
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
                    <select
                      v-model="item.complianceObservation"
                      class="compliance-select"
                      :disabled="isPreparedByVerified"
                      @change="computeParameterRemarks(item)"
                    >
                      <option value="">Select...</option>
                      <option value="YES">YES</option>
                      <option value="NO">NO</option>
                    </select>
                  </td>
                  <td>
                    <span
                      class="remarks-computed"
                      :class="{
                        ok: item.remarks === 'OK',
                        not_ok: item.remarks === 'NOT OK',
                      }"
                    >
                      {{ item.remarks || "-" }}
                    </span>
                  </td>
                  <td>
                    <input
                      type="file"
                      :disabled="isPreparedByVerified"
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
                  Please fill in all form fields (Report Details, Dimensional
                  Checklist, and Parameter Checklist) before verifying
                  signature.
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
import jsPDF from "jspdf";

export default {
  name: "MechanicalInspection",
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
          label: "Length",
          dimension: "",
          tolerance: "",
          observedValue: "",
          instrumentUsed: "",
          remarks: "",
          fileName: null,
          unit: "mm",
        },
        {
          label: "Width",
          dimension: "",
          tolerance: "",
          observedValue: "",
          instrumentUsed: "",
          remarks: "",
          fileName: null,
          unit: "mm",
        },
        {
          label: "Height",
          dimension: "",
          tolerance: "",
          observedValue: "",
          instrumentUsed: "",
          remarks: "",
          fileName: null,
          unit: "mm",
        },
        {
          label: "Weight",
          dimension: "",
          tolerance: "",
          observedValue: "",
          instrumentUsed: "",
          remarks: "",
          fileName: null,
          unit: "kg",
        },
      ],
      parameterChecklist: [
        {
          parameter: "Burrs",
          complianceObservation: "",
          expected: "Not Expected (NO)",
          remarks: "",
          fileName: null,
        },
        {
          parameter: "Damages",
          complianceObservation: "",
          expected: "Not Expected (NO)",
          remarks: "",
          fileName: null,
        },
        {
          parameter: "Name Plate",
          complianceObservation: "",
          expected: "As per Drawing (YES)",
          remarks: "",
          fileName: null,
        },
        {
          parameter: "Engraving",
          complianceObservation: "",
          expected: "As per Drawing (YES)",
          remarks: "",
          fileName: null,
        },
        {
          parameter: "Passivation",
          complianceObservation: "",
          expected: "As per Drawing (YES)",
          remarks: "",
          fileName: null,
        },
        {
          parameter: "Chromate",
          complianceObservation: "",
          expected: "As per Drawing (YES)",
          remarks: "",
          fileName: null,
        },
        {
          parameter: "Electro-less Nickel plating",
          complianceObservation: "",
          expected: "As per Drawing (YES)",
          remarks: "",
          fileName: null,
        },
        {
          parameter: "Fasteners",
          complianceObservation: "",
          expected: "As per Drawing (YES)",
          remarks: "",
          fileName: null,
        },
      ],
      currentDate: new Date(),
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
    areAllFieldsFilled() {
      if (!this.isFormValid) return false;

      for (const item of this.dimensionalChecklist) {
        if (
          !item.dimension ||
          !item.tolerance ||
          !item.observedValue ||
          !item.instrumentUsed
        ) {
          return false;
        }
      }

      for (const item of this.parameterChecklist) {
        if (!item.complianceObservation) {
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
      this.reportData.projectName = this.$route.params.projectName || "";
      this.reportData.lruName = this.$route.params.lruName || "";
      this.reportData.startDate = this.formattedDate;
    }
  },
  methods: {
    extractNumericValue(value, useAbsolute = false) {
      if (!value || typeof value !== "string") return null;

      let cleaned = value.replace(/[±]/g, "").replace(/[+/-]/g, " ").trim();
      cleaned = cleaned.replace(/^[^0-9-.]*\s*:\s*/i, "").trim();

      const match = cleaned.match(/(-?\d+\.?\d*)/);
      if (match) {
        const num = parseFloat(match[1]);
        return useAbsolute ? Math.abs(num) : num;
      }
      return null;
    },
    computeRemarks(item) {
      if (!item.dimension || !item.tolerance || !item.observedValue) {
        item.remarks = "";
        return;
      }

      const dimension = this.extractNumericValue(item.dimension, false);
      const tolerance = this.extractNumericValue(item.tolerance, true);
      const observed = this.extractNumericValue(item.observedValue, false);

      if (dimension === null || tolerance === null || observed === null) {
        item.remarks = "";
        return;
      }

      const minValue = dimension - tolerance;
      const maxValue = dimension + tolerance;
      item.remarks =
        observed >= minValue && observed <= maxValue ? "OK" : "NOT OK";
    },
    extractExpectedValue(expected) {
      if (!expected || typeof expected !== "string") return null;

      const match = expected.match(/\(([^)]+)\)/);
      return match && match[1] ? match[1].trim().toUpperCase() : null;
    },

    computeParameterRemarks(item) {
      if (!item.complianceObservation) {
        item.remarks = "";
        return;
      }

      const expectedValue = this.extractExpectedValue(item.expected);
      if (!expectedValue) {
        item.remarks = "";
        return;
      }

      item.remarks =
        item.complianceObservation.toUpperCase() === expectedValue
          ? "OK"
          : "NOT OK";
    },

    handleFileUpload(event, item) {
      const file = event.target.files[0];
      if (file) {
        item.fileName = file.name;
      }
    },

    async loadReportData(reportCardId) {
      try {
        const response = await fetch(
          `http://localhost:8000/api/mechanical-inspection/by-report-card/${reportCardId}`
        );

        if (!response.ok) {
          if (response.status === 404) {
            return;
          }
          throw new Error(
            `Failed to fetch report: ${response.statusText} (${response.status})`
          );
        }

        const result = await response.json();

        if (result.success && result.report) {
          const report = result.report;

          this.reportData = {
            projectName: report.project_name || "",
            reportRefNo: report.report_ref_no || "",
            memoRefNo: report.memo_ref_no || "",
            lruName: report.lru_name || "",
            inspectionStage: report.inspection_stage || "",
            testVenue: report.test_venue || "",
            slNos: report.sl_nos || "",
            dpName: report.dp_name || "",
            dated1: report.dated1 || "",
            dated2: report.dated2 || "",
            sruName: report.sru_name || "",
            partNo: report.part_no || "",
            quantity: report.quantity || null,
            startDate: report.start_date || this.formattedDate,
            endDate: report.end_date || "",
          };

          if (this.dimensionalChecklist.length >= 4) {
            const dimMappings = [
              ["dim1", 0],
              ["dim2", 1],
              ["dim3", 2],
              ["dim4", 3],
            ];

            dimMappings.forEach(([prefix, index]) => {
              this.dimensionalChecklist[index].dimension =
                report[`${prefix}_dimension`] || "";
              this.dimensionalChecklist[index].tolerance =
                report[`${prefix}_tolerance`] || "";
              this.dimensionalChecklist[index].observedValue =
                report[`${prefix}_observed_value`] || "";
              this.dimensionalChecklist[index].instrumentUsed =
                report[`${prefix}_instrument_used`] || "";
              this.dimensionalChecklist[index].remarks =
                report[`${prefix}_remarks`] || "";
              this.dimensionalChecklist[index].fileName =
                report[`${prefix}_upload`] || null;
            });
          }

          const paramFields = [
            "param1",
            "param2",
            "param3",
            "param4",
            "param5",
            "param6",
            "param7",
            "param8",
          ];
          paramFields.forEach((paramPrefix, index) => {
            if (index < this.parameterChecklist.length) {
              this.parameterChecklist[index].complianceObservation =
                report[`${paramPrefix}_compliance_observation`] || "";
              this.parameterChecklist[index].expected =
                report[`${paramPrefix}_expected`] ||
                this.parameterChecklist[index].expected;
              this.parameterChecklist[index].remarks =
                report[`${paramPrefix}_remarks`] || "";
              this.parameterChecklist[index].fileName =
                report[`${paramPrefix}_upload`] || null;
            }
          });

          if (report.prepared_by)
            this.signatures.preparedBy.signatureUrl = report.prepared_by;
          if (report.verified_by)
            this.signatures.verifiedBy.signatureUrl = report.verified_by;
          if (report.approved_by)
            this.signatures.approvedBy.signatureUrl = report.approved_by;
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
          "http://localhost:8000/api/users/verify-signature",
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
        dim4_dimension: this.dimensionalChecklist[3].dimension,
        dim4_tolerance: this.dimensionalChecklist[3].tolerance,
        dim4_observed_value: this.dimensionalChecklist[3].observedValue,
        dim4_instrument_used: this.dimensionalChecklist[3].instrumentUsed,
        dim4_remarks: this.dimensionalChecklist[3].remarks,
        dim4_upload: this.dimensionalChecklist[3].fileName,

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
          "http://localhost:8000/api/mechanical-inspection",
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
          "http://localhost:8000/api/mechanical-inspection",
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
            "Mechanical inspection report submitted successfully! Notifications have been sent."
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
          `http://localhost:8000/api/reports/${reportCardId}`
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
    async exportReport() {
      try {
        // Helper function to convert image URL to base64
        const imageToBase64 = (url) => {
          return new Promise((resolve, reject) => {
            const img = new Image();
            img.crossOrigin = "anonymous";
            img.onload = () => {
              const canvas = document.createElement("canvas");
              canvas.width = img.width;
              canvas.height = img.height;
              const ctx = canvas.getContext("2d");
              ctx.drawImage(img, 0, 0);
              resolve(canvas.toDataURL("image/png"));
            };
            img.onerror = reject;
            img.src = url;
          });
        };

        const doc = new jsPDF("p", "mm", "a4");
        const pageWidth = doc.internal.pageSize.getWidth();
        const pageHeight = doc.internal.pageSize.getHeight();
        const margin = 20;
        const contentWidth = pageWidth - 2 * margin;

        let yPosition = margin;
        let currentPage = 1;

        // Helper function to add new page if needed
        const checkPageBreak = (requiredHeight) => {
          if (yPosition + requiredHeight > pageHeight - margin) {
            doc.addPage();
            currentPage++;
            yPosition = margin;
            return true;
          }
          return false;
        };

        // Helper function to add text with wrapping
        const addText = (
          text,
          x,
          y,
          maxWidth,
          fontSize = 10,
          isBold = false,
          align = "left"
        ) => {
          doc.setFontSize(fontSize);
          doc.setFont("helvetica", isBold ? "bold" : "normal");
          const lines = doc.splitTextToSize(text || "", maxWidth);
          const lineHeight = fontSize * 0.4;
          lines.forEach((line, index) => {
            let xPos = x;
            if (align === "center") {
              const textWidth = doc.getTextWidth(line);
              xPos = x + (maxWidth - textWidth) / 2;
            } else if (align === "right") {
              const textWidth = doc.getTextWidth(line);
              xPos = x + maxWidth - textWidth;
            }
            doc.text(line, xPos, y + index * lineHeight);
          });
          return lines.length * lineHeight;
        };

        // ===== HEADER SECTION =====
        // Load DRDO logo
        let drdoLogoBase64 = null;
        try {
          const drdoLogoUrl = new URL(
            "../assets/images/DRDO.png",
            import.meta.url
          ).href;
          drdoLogoBase64 = await imageToBase64(drdoLogoUrl);
        } catch (e) {
          console.warn("Could not load DRDO logo:", e);
        }

        // Add DRDO logo (left corner)
        let textStartX = margin + 18;
        if (drdoLogoBase64) {
          try {
            doc.addImage(drdoLogoBase64, "PNG", margin, yPosition, 15, 15);
            textStartX = margin + 18;
          } catch (e) {
            console.warn("Could not add DRDO logo:", e);
            textStartX = margin;
          }
        }

        // Add AVIATRAX text (centered)
        doc.setFontSize(14);
        doc.setFont("helvetica", "bold");
        doc.setTextColor(75, 0, 130);
        const aviatraxText = "AVIATRAX™";
        const aviatraxWidth = doc.getTextWidth(aviatraxText);
        doc.text(aviatraxText, (pageWidth - aviatraxWidth) / 2, yPosition + 8);

        // Add Defence Research text below AVIATRAX
        doc.setFontSize(8);
        doc.setFont("helvetica", "normal");
        doc.setTextColor(0, 0, 0);
        const drdoText = "Defence Research and Development Org. (DRDO)";
        const drdoTextWidth = doc.getTextWidth(drdoText);
        doc.text(drdoText, (pageWidth - drdoTextWidth) / 2, yPosition + 12);
        doc.setFont("helvetica", "italic");
        doc.setFontSize(7);
        const centreText =
          "Combat Aircraft Systems Development and Integration Centre";
        const centreTextWidth = doc.getTextWidth(centreText);
        doc.text(centreText, (pageWidth - centreTextWidth) / 2, yPosition + 16);

        // CASDIC path and date
        yPosition += 25;
        doc.setFontSize(9);
        doc.setFont("helvetica", "normal");
        const documentPath = `CASDIC/${
          this.reportData.projectName || "PROJECT"
        }/${this.reportData.lruName || "LRU"}/SL.${
          this.reportData.slNos || "001"
        }/${this.reportData.reportRefNo || "INS-001"}/${this.currentYear}`;
        doc.text(documentPath, margin, yPosition);

        const dateText = `Date: ${
          this.formattedDate || new Date().toLocaleDateString("en-GB")
        }`;
        const dateWidth = doc.getTextWidth(dateText);
        doc.text(dateText, pageWidth - margin - dateWidth, yPosition);
        yPosition += 10;

        // Subject line
        doc.setFontSize(11);
        doc.setFont("helvetica", "bold");
        const subjectText = `SUB: Mechanical Inspection Report for ${
          this.reportData.lruName || "Unknown LRU"
        }`;
        const subjectWidth = doc.getTextWidth(subjectText);
        doc.text(subjectText, (pageWidth - subjectWidth) / 2, yPosition);
        yPosition += 12;

        // ===== REPORT DETAILS SECTION =====
        checkPageBreak(50);
        doc.setFontSize(12);
        doc.setFont("helvetica", "bold");
        doc.text("Report Details", margin, yPosition);
        yPosition += 8;

        doc.setFontSize(10);
        doc.setFont("helvetica", "normal");
        const colWidth = (contentWidth - 10) / 2;
        let leftY = yPosition;
        let rightY = yPosition;

        // Left column fields
        const leftFields = [
          {
            label: "Project Name",
            value: this.reportData.projectName || "N/A",
          },
          {
            label: "Report Ref No",
            value: this.reportData.reportRefNo || "N/A",
          },
          { label: "Memo Ref No", value: this.reportData.memoRefNo || "N/A" },
          { label: "LRU Name", value: this.reportData.lruName || "N/A" },
          {
            label: "Inspection Stage",
            value: this.reportData.inspectionStage || "N/A",
          },
          { label: "Test Venue", value: this.reportData.testVenue || "N/A" },
          { label: "SL.NO'S", value: this.reportData.slNos || "N/A" },
        ];

        // Right column fields
        const rightFields = [
          { label: "DP Name", value: this.reportData.dpName || "N/A" },
          {
            label: "Dated",
            value: this.reportData.dated1
              ? new Date(this.reportData.dated1).toLocaleDateString("en-GB")
              : "dd/mm/yyyy",
          },
          {
            label: "Dated",
            value: this.reportData.dated2
              ? new Date(this.reportData.dated2).toLocaleDateString("en-GB")
              : "dd/mm/yyyy",
          },
          { label: "SRU Name", value: this.reportData.sruName || "N/A" },
          { label: "Part No", value: this.reportData.partNo || "N/A" },
          {
            label: "Quantity",
            value:
              this.reportData.quantity !== null &&
              this.reportData.quantity !== undefined
                ? this.reportData.quantity.toString()
                : "N/A",
          },
          {
            label: "Start Date",
            value: this.reportData.startDate
              ? new Date(this.reportData.startDate).toLocaleDateString("en-GB")
              : "N/A",
          },
          {
            label: "End Date",
            value: this.reportData.endDate
              ? new Date(this.reportData.endDate).toLocaleDateString("en-GB")
              : "N/A",
          },
        ];

        // Print left column
        leftFields.forEach((field) => {
          const text = `${field.label}: ${field.value}`;
          const height = addText(
            text,
            margin,
            leftY,
            colWidth,
            10,
            false,
            "left"
          );
          leftY += height + 3;
        });

        // Print right column
        rightFields.forEach((field) => {
          const text = `${field.label}: ${field.value}`;
          const height = addText(
            text,
            margin + colWidth + 10,
            rightY,
            colWidth,
            10,
            false,
            "left"
          );
          rightY += height + 3;
        });

        yPosition = Math.max(leftY, rightY) + 10;

        // ===== DIMENSIONAL CHECKLIST SECTION =====
        checkPageBreak(40);
        doc.setFontSize(12);
        doc.setFont("helvetica", "bold");
        doc.text("Dimensional Checklist", margin, yPosition);
        yPosition += 10;

        if (this.dimensionalChecklist && this.dimensionalChecklist.length > 0) {
          // Calculate column widths as percentages of contentWidth
          const colWidths = [
            contentWidth * 0.08, // SL.NO
            contentWidth * 0.18, // DIMENSION
            contentWidth * 0.15, // TOLERANCE
            contentWidth * 0.18, // OBSERVED VALUE
            contentWidth * 0.18, // INSTRUMENT USED
            contentWidth * 0.23, // REMARKS
          ];

          // Ensure columns add up exactly to contentWidth
          const totalWidth = colWidths.reduce((sum, width) => sum + width, 0);
          if (Math.abs(totalWidth - contentWidth) > 0.1) {
            const adjustment = (contentWidth - totalWidth) / colWidths.length;
            colWidths.forEach((width, i) => {
              colWidths[i] = width + adjustment;
            });
          }

          const rowHeight = 12;
          const headers = [
            "SL.NO",
            "DIMENSION",
            "TOLERANCE",
            "OBSERVED VALUE",
            "INSTRUMENT USED",
            "REMARKS",
          ];

          // Draw header with borders and background
          doc.setFontSize(9);
          doc.setFont("helvetica", "bold");
          const lineHeight = 4.5;
          const headerHeight = 12;

          let xPos = margin;
          headers.forEach((header, i) => {
            // Draw cell border and background
            doc.setFillColor(240, 240, 240);
            doc.rect(xPos, yPosition - 7, colWidths[i], headerHeight, "FD");

            // Draw header text
            const headerWidth = doc.getTextWidth(header);
            doc.text(
              header,
              xPos + colWidths[i] / 2 - headerWidth / 2,
              yPosition + 2
            );
            xPos += colWidths[i];
          });
          yPosition += headerHeight + 3;

          // Draw rows with borders
          doc.setFont("helvetica", "normal");
          doc.setFontSize(9);
          this.dimensionalChecklist.forEach((item, index) => {
            checkPageBreak(rowHeight + 5);

            const rowData = [
              (index + 1).toString(),
              item.dimension || "",
              item.tolerance || "",
              item.observedValue || "",
              item.instrumentUsed || "",
              item.remarks || "",
            ];

            // Draw cell borders
            doc.setLineWidth(0.1);
            doc.rect(margin, yPosition - 6, contentWidth, rowHeight, "D");

            xPos = margin;
            for (let colIdx = 1; colIdx < colWidths.length; colIdx++) {
              xPos += colWidths[colIdx - 1];
              doc.line(xPos, yPosition - 6, xPos, yPosition - 6 + rowHeight);
            }

            // Draw cell content
            xPos = margin;
            rowData.forEach((text, colIdx) => {
              const textLines = doc.splitTextToSize(
                text || "",
                colWidths[colIdx] - 6
              );
              doc.text(textLines, xPos + 3, yPosition + 3);
              xPos += colWidths[colIdx];
            });

            yPosition += rowHeight + 1;
          });
          yPosition += 5;
        }

        // ===== PARAMETER CHECKLIST SECTION =====
        checkPageBreak(40);
        doc.setFontSize(12);
        doc.setFont("helvetica", "bold");
        doc.text("Parameter Checklist", margin, yPosition);
        yPosition += 10;

        if (this.parameterChecklist && this.parameterChecklist.length > 0) {
          // Calculate column widths as percentages of contentWidth
          const colWidths = [
            contentWidth * 0.08, // SL.NO
            contentWidth * 0.3, // PARAMETER
            contentWidth * 0.25, // EXPECTED
            contentWidth * 0.2, // OBSERVATION
            contentWidth * 0.17, // REMARKS
          ];

          // Ensure columns add up exactly to contentWidth
          const totalWidth = colWidths.reduce((sum, width) => sum + width, 0);
          if (Math.abs(totalWidth - contentWidth) > 0.1) {
            const adjustment = (contentWidth - totalWidth) / colWidths.length;
            colWidths.forEach((width, i) => {
              colWidths[i] = width + adjustment;
            });
          }

          const rowHeight = 12;
          const headers = [
            "SL.NO",
            "PARAMETER",
            "EXPECTED",
            "OBSERVATION",
            "REMARKS",
          ];

          // Draw header with borders and background
          doc.setFontSize(9);
          doc.setFont("helvetica", "bold");
          const headerHeight = 12;

          let xPos = margin;
          headers.forEach((header, i) => {
            // Draw cell border and background
            doc.setFillColor(240, 240, 240);
            doc.rect(xPos, yPosition - 7, colWidths[i], headerHeight, "FD");

            // Draw header text
            const headerWidth = doc.getTextWidth(header);
            doc.text(
              header,
              xPos + colWidths[i] / 2 - headerWidth / 2,
              yPosition + 2
            );
            xPos += colWidths[i];
          });
          yPosition += headerHeight + 3;

          // Draw rows with borders
          doc.setFont("helvetica", "normal");
          doc.setFontSize(9);
          this.parameterChecklist.forEach((item, index) => {
            checkPageBreak(rowHeight + 5);

            const rowData = [
              (index + 1).toString(),
              item.parameter || "",
              item.expected || "",
              item.complianceObservation || "",
              item.remarks || "",
            ];

            // Draw cell borders
            doc.setLineWidth(0.1);
            doc.rect(margin, yPosition - 6, contentWidth, rowHeight, "D");

            xPos = margin;
            for (let colIdx = 1; colIdx < colWidths.length; colIdx++) {
              xPos += colWidths[colIdx - 1];
              doc.line(xPos, yPosition - 6, xPos, yPosition - 6 + rowHeight);
            }

            // Draw cell content
            xPos = margin;
            rowData.forEach((text, colIdx) => {
              const textLines = doc.splitTextToSize(
                text || "",
                colWidths[colIdx] - 6
              );
              doc.text(textLines, xPos + 3, yPosition + 3);
              xPos += colWidths[colIdx];
            });

            yPosition += rowHeight + 1;
          });
          yPosition += 5;
        }

        // ===== SIGNATURES SECTION =====
        checkPageBreak(30);
        doc.setFontSize(12);
        doc.setFont("helvetica", "bold");
        doc.text("Signatures", margin, yPosition);
        yPosition += 8;

        doc.setFontSize(10);
        doc.setFont("helvetica", "normal");

        // Helper to extract name from signature URL
        const getSignatureName = (signatureUrl) => {
          if (!signatureUrl) return "";
          if (signatureUrl.includes("|")) {
            return signatureUrl.split("|")[0];
          }
          return "";
        };

        // Helper to get signature image URL
        const getSignatureImageUrl = (signatureUrl) => {
          if (!signatureUrl) return null;
          if (signatureUrl.includes("|")) {
            const parts = signatureUrl.split("|");
            return parts.length > 1 ? parts[1] : null;
          }
          return signatureUrl.startsWith("http") ? signatureUrl : null;
        };

        const signatures = [
          {
            label: "Prepared By",
            signatureUrl: this.signatures.preparedBy.signatureUrl,
            verifiedName:
              this.signatures.preparedBy.verifiedUserName ||
              getSignatureName(this.signatures.preparedBy.signatureUrl),
          },
          {
            label: "Verified By",
            signatureUrl: this.signatures.verifiedBy.signatureUrl,
            verifiedName:
              this.signatures.verifiedBy.verifiedUserName ||
              getSignatureName(this.signatures.verifiedBy.signatureUrl),
          },
          {
            label: "Approved By",
            signatureUrl: this.signatures.approvedBy.signatureUrl,
            verifiedName:
              this.signatures.approvedBy.verifiedUserName ||
              getSignatureName(this.signatures.approvedBy.signatureUrl),
          },
        ];

        const sigColWidth = contentWidth / 3;
        for (let index = 0; index < signatures.length; index++) {
          const sig = signatures[index];
          const xPos = margin + index * sigColWidth;
          doc.text(`${sig.label}:`, xPos, yPosition);

          const imgUrl = getSignatureImageUrl(sig.signatureUrl);
          if (imgUrl) {
            try {
              const imgBase64 = await imageToBase64(imgUrl);
              doc.addImage(imgBase64, "PNG", xPos, yPosition + 3, 40, 15);
              if (sig.verifiedName) {
                doc.text(sig.verifiedName, xPos, yPosition + 20);
              }
            } catch (e) {
              console.warn(
                `Could not load signature image for ${sig.label}:`,
                e
              );
              doc.text(
                sig.verifiedName || "_________________",
                xPos,
                yPosition + 5
              );
            }
          } else {
            doc.text(
              sig.verifiedName || "_________________",
              xPos,
              yPosition + 5
            );
          }
        }

        // Add page numbers
        const totalPages = doc.internal.getNumberOfPages();
        for (let i = 1; i <= totalPages; i++) {
          doc.setPage(i);
          doc.setFontSize(8);
          doc.setFont("helvetica", "normal");
          const pageText = `Generated on ${new Date().toLocaleString(
            "en-GB"
          )} | Page ${i} of ${totalPages}`;
          doc.text(pageText, pageWidth / 2, pageHeight - 10, {
            align: "center",
          });
        }

        // Save PDF
        const fileName = `Mechanical_Inspection_Report_${
          this.reportData.lruName || "Unknown"
        }_${this.formattedDate.replace(/\//g, "-")}.pdf`;
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
.mechanical-inspection-page {
  min-height: 100vh;
  background-color: #ebf7fd;
  font-family: "Arial", sans-serif;
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

.compliance-select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  background-color: white;
  cursor: pointer;
}

.compliance-select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
}

.remarks-computed {
  display: inline-block;
  padding: 0.5rem;
  font-weight: bold;
  text-align: center;
  min-width: 60px;
  border-radius: 4px;
}

.remarks-computed.ok {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.remarks-computed.not_ok {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.dimension-input-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.dimension-input-wrapper .dimension-input {
  flex: 1;
  margin: 0;
}

.dimension-unit {
  font-weight: 500;
  color: #666;
  white-space: nowrap;
  min-width: 30px;
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
  gap: 1rem;
}

.signature-item > label {
  font-weight: bold;
  color: #333;
  font-size: 1rem;
}

/* Signature Authentication Styles */
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

.input-group input[readonly] {
  background-color: #f8f9fa;
  cursor: not-allowed;
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

.form-actions {
  display: flex;
  justify-content: center;
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
</style>
