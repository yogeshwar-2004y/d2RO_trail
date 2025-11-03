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
                  <th>DIMENSION <br>(As Per Drawing)</th>
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
                        :placeholder="`Enter ${item.label?.toLowerCase() || 'dimension'}`"
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
                        'ok': item.remarks === 'OK',
                        'not_ok': item.remarks === 'NOT OK'
                      }"
                    >
                      {{ item.remarks || '-' }}
                    </span>
                  </td>
                  <td>
                    <input
                      type="file"
                      :disabled="isPreparedByVerified"
                      @change="handleFileUpload($event, item, 'dim')"
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
                        'ok': item.remarks === 'OK',
                        'not_ok': item.remarks === 'NOT OK'
                      }"
                    >
                      {{ item.remarks || '-' }}
                    </span>
                  </td>
                  <td>
                    <input
                      type="file"
                      :disabled="isPreparedByVerified"
                      @change="handleFileUpload($event, item, 'param')"
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
                <div v-if="!canAccessSignatures" class="signature-disabled-message">
                  Signature authentication is only available for QA Reviewer and QA Head.
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
                    @click="verifySignature('preparedBy')"
                    :disabled="
                      !isPreparedByEnabled ||
                      !signatures.preparedBy.signatureUsername ||
                      !signatures.preparedBy.signaturePassword
                    "
                  >
                    Verify & Load Signature
                  </button>
                </div>
                <div v-if="signatures.preparedBy.signatureUrl" class="signature-display">
                  <label>Verified Signature:</label>
                  <div class="signature-image-container">
                    <img
                      :src="signatures.preparedBy.signatureUrl"
                      alt="Verified Signature"
                      class="signature-image"
                    />
                    <div class="signature-info">
                      <span class="signature-user">{{ signatures.preparedBy.verifiedUserName }}</span>
                      <span class="signature-role">{{ signatures.preparedBy.verifiedUserRole }} Signature</span>
                      <span class="signature-status">✓ Verified</span>
                    </div>
                  </div>
                </div>
                <div v-if="signatures.preparedBy.signatureError" class="signature-error">
                  {{ signatures.preparedBy.signatureError }}
                </div>
              </div>
            </div>

            <!-- Verified By Signature -->
            <div class="signature-item">
              <label>Verified By:</label>
              <div class="signature-auth-container">
                <div v-if="!canAccessSignatures" class="signature-disabled-message">
                  Signature authentication is only available for QA Reviewer and QA Head.
                </div>
                <div v-else-if="!isPreparedByVerified" class="signature-disabled-message">
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
                    @click="verifySignature('verifiedBy')"
                    :disabled="
                      !isVerifiedByEnabled ||
                      !signatures.verifiedBy.signatureUsername ||
                      !signatures.verifiedBy.signaturePassword
                    "
                  >
                    Verify & Load Signature
                  </button>
                </div>
                <div v-if="signatures.verifiedBy.signatureUrl" class="signature-display">
                  <label>Verified Signature:</label>
                  <div class="signature-image-container">
                    <img
                      :src="signatures.verifiedBy.signatureUrl"
                      alt="Verified Signature"
                      class="signature-image"
                    />
                    <div class="signature-info">
                      <span class="signature-user">{{ signatures.verifiedBy.verifiedUserName }}</span>
                      <span class="signature-role">{{ signatures.verifiedBy.verifiedUserRole }} Signature</span>
                      <span class="signature-status">✓ Verified</span>
                    </div>
                  </div>
                </div>
                <div v-if="signatures.verifiedBy.signatureError" class="signature-error">
                  {{ signatures.verifiedBy.signatureError }}
                </div>
              </div>
            </div>

            <!-- Approved By Signature -->
            <div class="signature-item">
              <label>Approved By:</label>
              <div class="signature-auth-container">
                <div v-if="!canAccessSignatures" class="signature-disabled-message">
                  Signature authentication is only available for QA Reviewer and QA Head.
                </div>
                <div v-else-if="!isVerifiedByVerified" class="signature-disabled-message">
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
                    @click="verifySignature('approvedBy')"
                    :disabled="
                      !isApprovedByEnabled ||
                      !signatures.approvedBy.signatureUsername ||
                      !signatures.approvedBy.signaturePassword
                    "
                  >
                    Verify & Load Signature
                  </button>
                </div>
                <div v-if="signatures.approvedBy.signatureUrl" class="signature-display">
                  <label>Verified Signature:</label>
                  <div class="signature-image-container">
                    <img
                      :src="signatures.approvedBy.signatureUrl"
                      alt="Verified Signature"
                      class="signature-image"
                    />
                    <div class="signature-info">
                      <span class="signature-user">{{ signatures.approvedBy.verifiedUserName }}</span>
                      <span class="signature-role">{{ signatures.approvedBy.verifiedUserRole }} Signature</span>
                      <span class="signature-status">✓ Verified</span>
                    </div>
                  </div>
                </div>
                <div v-if="signatures.approvedBy.signatureError" class="signature-error">
                  {{ signatures.approvedBy.signatureError }}
                </div>
              </div>
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

      <!-- Submit Button at Bottom -->
      <!-- <div class="bottom-submit-section" v-if="!readonly">
        <button
          type="button"
          @click="submitForm"
          class="btn btn-primary btn-submit-bottom"
          :disabled="!isFormValid"
        >
          Submit Report
        </button>
      </div> -->
    </div>
  </div>
</template>

<script>
import { userStore } from "@/stores/userStore";

export default {
  name: "MechanicalInspection",
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
    // Check if user is QA Reviewer (role_id = 3) or QA Head (role_id = 2)
    canAccessSignatures() {
      const currentUserRole = userStore.getters.currentUserRole();
      return currentUserRole === 2 || currentUserRole === 3; // QA Head or QA Reviewer
    },
    // Check if Prepared By signature is verified
    isPreparedByVerified() {
      return !!this.signatures.preparedBy.signatureUrl;
    },
    // Check if Verified By signature is verified
    isVerifiedByVerified() {
      return !!this.signatures.verifiedBy.signatureUrl;
    },
    // Prepared By should be enabled if user can access signatures
    isPreparedByEnabled() {
      return this.canAccessSignatures;
    },
    // Verified By should be enabled only after Prepared By is verified
    isVerifiedByEnabled() {
      return this.canAccessSignatures && this.isPreparedByVerified;
    },
    // Approved By should be enabled only after Verified By is verified
    isApprovedByEnabled() {
      return this.canAccessSignatures && this.isVerifiedByVerified;
    },
  },
  mounted() {
    // Get parameters from props (when used in IndividualReport) or route params
    const projectName = this.$route.params.projectName || "";
    const lruName = this.$route.params.lruName || "";
    const reportCardId = this.reportId || this.$route.params.reportId;

    console.log("MechanicalInspection mounted - reportCardId:", reportCardId);

    // If reportCardId is provided, load the report data
    if (reportCardId) {
      this.loadReportData(reportCardId);
    } else {
      // Set default values for new report
      this.reportData.projectName = projectName;
      this.reportData.lruName = lruName;
      this.reportData.startDate = this.formattedDate;
    }
  },
  methods: {
    // Extract numeric value from a string (handles formats like "200 mm", "± 10 mm", "Length : 200 mm")
    extractNumericValue(value, useAbsolute = false) {
      if (!value || typeof value !== 'string') return null;
      
      // Replace ± or +/- with empty string for tolerance values
      // Handles formats like "± 10 mm", "+/- 10 mm", "200 mm", "Length : 200 mm", etc.
      let cleaned = value.replace(/[±]/g, '').replace(/[+/-]/g, ' ').trim();
      
      // Remove common text prefixes like "Length :", "Width :", etc.
      cleaned = cleaned.replace(/^[^0-9-.]*\s*:\s*/i, '').trim();
      
      // Extract the first number (including decimals and negative numbers)
      const match = cleaned.match(/(-?\d+\.?\d*)/);
      if (match) {
        const num = parseFloat(match[1]);
        // Return absolute value if useAbsolute is true (for tolerance), otherwise preserve sign
        return useAbsolute ? Math.abs(num) : num;
      }
      return null;
    },
    
    // Compute remarks based on dimension, tolerance, and observed value
    computeRemarks(item) {
      // Clear remarks if any required field is missing
      if (!item.dimension || !item.tolerance || !item.observedValue) {
        item.remarks = '';
        return;
      }
      
      // Extract values: dimension and observed preserve sign, tolerance always positive
      const dimension = this.extractNumericValue(item.dimension, false);
      const tolerance = this.extractNumericValue(item.tolerance, true); // Always use absolute value for tolerance
      const observed = this.extractNumericValue(item.observedValue, false);
      
      // Check if all values were successfully extracted
      if (dimension === null || tolerance === null || observed === null) {
        item.remarks = '';
        return;
      }
      
      // Calculate the acceptable range
      const minValue = dimension - tolerance;
      const maxValue = dimension + tolerance;
      
      // Check if observed value is within range
      if (observed >= minValue && observed <= maxValue) {
        item.remarks = 'OK';
      } else {
        item.remarks = 'NOT OK';
      }
    },
    
    // Extract value in brackets from expected field (e.g., "(YES)" or "(NO)")
    extractExpectedValue(expected) {
      if (!expected || typeof expected !== 'string') return null;
      
      // Match pattern like "(YES)" or "(NO)"
      const match = expected.match(/\(([^)]+)\)/);
      if (match && match[1]) {
        // Return the value in brackets, trimmed and uppercased
        return match[1].trim().toUpperCase();
      }
      return null;
    },
    
    // Compute remarks for parameter checklist based on compliance observation
    computeParameterRemarks(item) {
      // Clear remarks if compliance observation is not selected
      if (!item.complianceObservation) {
        item.remarks = '';
        return;
      }
      
      // Extract expected value from brackets (e.g., "YES" or "NO" from "(YES)" or "(NO)")
      const expectedValue = this.extractExpectedValue(item.expected);
      
      // If we can't extract expected value, clear remarks
      if (!expectedValue) {
        item.remarks = '';
        return;
      }
      
      // Compare compliance observation with expected value (case-insensitive)
      const complianceValue = item.complianceObservation.toUpperCase();
      
      if (complianceValue === expectedValue) {
        item.remarks = 'OK';
      } else {
        item.remarks = 'NOT OK';
      }
    },
    
    handleFileUpload(event, item, checklistType) {
      const file = event.target.files[0];
      if (file) {
        item.fileName = file.name;
      }
    },
    
    // Load report data from API using report card ID
    async loadReportData(reportCardId) {
      try {
        const url = `http://localhost:5000/api/mechanical-inspection/by-report-card/${reportCardId}`;
        console.log("Loading report data from:", url);
        
        const response = await fetch(url);

        if (!response.ok) {
          const errorText = await response.text();
          console.error("Failed to fetch report. Status:", response.status, "Response:", errorText);
          
          // If report not found (404), it means the form hasn't been submitted yet
          // Show empty form instead of error alert
          if (response.status === 404) {
            console.log("Report not found - showing empty form (report may not have been submitted yet)");
            // Keep default empty form values
            return;
          }
          
          throw new Error(`Failed to fetch report: ${response.statusText} (${response.status})`);
        }

        const result = await response.json();

        if (result.success && result.report) {
          const report = result.report;

          // Map report data
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

          // Map dimensional checklist
          if (this.dimensionalChecklist.length >= 4) {
            // Dimension 1 (Length)
            this.dimensionalChecklist[0].dimension = report.dim1_dimension || "";
            this.dimensionalChecklist[0].tolerance = report.dim1_tolerance || "";
            this.dimensionalChecklist[0].observedValue = report.dim1_observed_value || "";
            this.dimensionalChecklist[0].instrumentUsed = report.dim1_instrument_used || "";
            this.dimensionalChecklist[0].remarks = report.dim1_remarks || "";
            this.dimensionalChecklist[0].fileName = report.dim1_upload || null;

            // Dimension 2 (Width)
            this.dimensionalChecklist[1].dimension = report.dim2_dimension || "";
            this.dimensionalChecklist[1].tolerance = report.dim2_tolerance || "";
            this.dimensionalChecklist[1].observedValue = report.dim2_observed_value || "";
            this.dimensionalChecklist[1].instrumentUsed = report.dim2_instrument_used || "";
            this.dimensionalChecklist[1].remarks = report.dim2_remarks || "";
            this.dimensionalChecklist[1].fileName = report.dim2_upload || null;

            // Dimension 3 (Height)
            this.dimensionalChecklist[2].dimension = report.dim3_dimension || "";
            this.dimensionalChecklist[2].tolerance = report.dim3_tolerance || "";
            this.dimensionalChecklist[2].observedValue = report.dim3_observed_value || "";
            this.dimensionalChecklist[2].instrumentUsed = report.dim3_instrument_used || "";
            this.dimensionalChecklist[2].remarks = report.dim3_remarks || "";
            this.dimensionalChecklist[2].fileName = report.dim3_upload || null;

            // Dimension 4 (Weight)
            this.dimensionalChecklist[3].dimension = report.dim4_dimension || "";
            this.dimensionalChecklist[3].tolerance = report.dim4_tolerance || "";
            this.dimensionalChecklist[3].observedValue = report.dim4_observed_value || "";
            this.dimensionalChecklist[3].instrumentUsed = report.dim4_instrument_used || "";
            this.dimensionalChecklist[3].remarks = report.dim4_remarks || "";
            this.dimensionalChecklist[3].fileName = report.dim4_upload || null;
          }

          // Map parameter checklist
          const paramFields = [
            'param1', 'param2', 'param3', 'param4',
            'param5', 'param6', 'param7', 'param8'
          ];

          paramFields.forEach((paramPrefix, index) => {
            if (index < this.parameterChecklist.length) {
              this.parameterChecklist[index].complianceObservation = 
                report[`${paramPrefix}_compliance_observation`] || "";
              this.parameterChecklist[index].expected = 
                report[`${paramPrefix}_expected`] || this.parameterChecklist[index].expected;
              this.parameterChecklist[index].remarks = 
                report[`${paramPrefix}_remarks`] || "";
              this.parameterChecklist[index].fileName = 
                report[`${paramPrefix}_upload`] || null;
            }
          });

          // Map signatures
          if (report.prepared_by) {
            this.signatures.preparedBy.signatureUrl = report.prepared_by;
          }
          if (report.verified_by) {
            this.signatures.verifiedBy.signatureUrl = report.verified_by;
          }
          if (report.approved_by) {
            this.signatures.approvedBy.signatureUrl = report.approved_by;
          }

          console.log("Report data loaded successfully");
        } else {
          throw new Error(result.message || "Failed to load report data");
        }
      } catch (error) {
        console.error("Error loading report data:", error);
        
        // If report not found (404), it means the form hasn't been submitted yet
        // Show empty form instead of error alert
        if (error.message.includes('404') || error.message.includes('not found')) {
          console.log("Report not found - showing empty form (report may not have been submitted yet)");
          // Keep default empty form values
          return;
        }
        
        alert(`Error loading report data: ${error.message}. Please try again.`);
      }
    },
    
    // Verify signature credentials for prepared/verified/approved by
    async verifySignature(signatureType) {
      const signature = this.signatures[signatureType];

      if (!signature.signatureUsername || !signature.signaturePassword) {
        signature.signatureError =
          "Please enter both username and signature password";
        return;
      }

      try {
        const response = await fetch("http://localhost:5000/api/users/verify-signature", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
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
        } else {
          signature.signatureError = data.message || "Failed to verify signature";
          signature.signatureUrl = "";
          signature.verifiedUserName = "";
          signature.verifiedUserRole = "";
        }
      } catch (error) {
        signature.signatureError = "Error verifying signature: " + error.message;
        signature.signatureUrl = "";
        signature.verifiedUserName = "";
        signature.verifiedUserRole = "";
      }
    },
    saveDraft() {
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
          startDate: this.formattedDate,
          endDate: "",
        };
        // Reset checklists
        this.dimensionalChecklist.forEach((item) => {
          item.dimension = "";
          item.tolerance = "";
          item.observedValue = "";
          item.instrumentUsed = "";
          item.remarks = "";
          item.fileName = null;
        });
        this.parameterChecklist.forEach((item) => {
          item.complianceObservation = "";
          item.expected =
            item.parameter === "Burrs" || item.parameter === "Damages"
              ? "Not Expected (NO)"
              : "As per Drawing (YES)";
          item.remarks = "";
          item.fileName = null;
        });
        // Reset signatures
        this.signatures.preparedBy = {
          signatureUsername: "",
          signaturePassword: "",
          signatureUrl: "",
          verifiedUserName: "",
          verifiedUserRole: "",
          signatureError: "",
        };
        this.signatures.verifiedBy = {
          signatureUsername: "",
          signaturePassword: "",
          signatureUrl: "",
          verifiedUserName: "",
          verifiedUserRole: "",
          signatureError: "",
        };
        this.signatures.approvedBy = {
          signatureUsername: "",
          signaturePassword: "",
          signatureUrl: "",
          verifiedUserName: "",
          verifiedUserRole: "",
          signatureError: "",
        };
      }
    },
    async submitForm() {
      if (!this.isFormValid) {
        alert("Please fill in all required fields.");
        return;
      }

      try {
        // Get report card ID from props or route
        const reportCardId = this.reportId || this.$route.params.reportId;
        
        // Prepare data for submission
        const submissionData = {
          // Link to report card
          report_card_id: reportCardId,
          // Report Details
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

          // Signatures
          prepared_by: this.signatures.preparedBy.signatureUrl || "",
          verified_by: this.signatures.verifiedBy.signatureUrl || "",
          approved_by: this.signatures.approvedBy.signatureUrl || "",
        };

        const response = await fetch(
          "http://localhost:5000/api/mechanical-inspection",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(submissionData),
          }
        );

        const result = await response.json();

        if (result.success) {
          alert("Mechanical inspection report submitted successfully!");
          this.resetForm();
        } else {
          alert(`Error: ${result.message}`);
        }
      } catch (error) {
        console.error("Error submitting report:", error);
        alert("Error submitting report. Please try again.");
      }
    },
  },
};
</script>

<style scoped>
.mechanical-inspection-page {
  min-height: 100vh;
  background-color: #f5f5f5;
  font-family: "Arial", sans-serif;
}

.page-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.back-button {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  padding: 0.5rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.back-button:hover {
  background: rgba(255, 255, 255, 0.3);
}

.header-center {
  flex: 1;
  text-align: center;
}

.page-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin: 0;
}

.header-right {
  display: flex;
  align-items: center;
}

.export-button {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.export-button:hover {
  background: rgba(255, 255, 255, 0.3);
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

.btn-verify {
  background-color: #667eea;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: background-color 0.3s ease;
  align-self: flex-start;
}

.btn-verify:hover:not(:disabled) {
  background-color: #5a6fd8;
}

.btn-verify:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
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
  justify-content: flex-end;
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

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
}

.bottom-submit-section {
  position: sticky;
  bottom: 0;
  background: white;
  padding: 1.5rem 2rem;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
  margin-top: 2rem;
  text-align: center;
  border-top: 1px solid #ddd;
}

.btn-submit-bottom {
  padding: 1rem 3rem;
  font-size: 1.1rem;
  font-weight: 600;
  min-width: 200px;
}
</style>
