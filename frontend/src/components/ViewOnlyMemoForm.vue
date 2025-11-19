<template>
  <div class="memo-form">
    <!-- Header -->
    <div class="form-header">
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

      <h1 class="form-title">REQUISITION FOR DGAQA INSPECTION</h1>
      <div class="header-actions">
        <div class="view-only-badge">VIEW ONLY</div>
        <button
          class="download-pdf-btn"
          @click="downloadMemoPDF"
          title="Download PDF"
        >
          <svg
            class="icon download"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path
              d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"
            />
          </svg>
          <span class="download-text">Download PDF</span>
        </button>
      </div>
    </div>

    <!-- Form Content (for PDF generation) -->
    <div class="form-content">
      <!-- Requisition Details Section -->
      <div class="form-card read-only-section">
        <div class="section-header">
          <h2 class="card-title">REQUISITION FOR DGAQA INSPECTION</h2>
        </div>
        <div class="grid-layout">
          <div class="grid-item">
            <span>FROM:</span
            ><input type="text" v-model="formData.from1" readonly />
          </div>
          <div class="grid-item">
            <span>CASCIC Ref No.:</span
            ><input type="text" v-model="formData.casdic" readonly />
          </div>
          <div class="grid-item">
            <span>CASCIC/</span
            ><input type="text" v-model="formData.casdic" readonly />
          </div>
          <div class="grid-item">
            <span>Dated:</span
            ><input type="text" v-model="formData.casdicDate" readonly />
          </div>
          <div class="grid-item">
            <span>TO:</span
            ><input type="text" v-model="formData.from2" readonly />
          </div>
          <div class="grid-item">
            <span>Wing/Proj Ref No.:</span
            ><input type="text" v-model="formData.wingRef" readonly />
          </div>
          <div class="grid-item-full">
            <span>Name & contact No of CASCIC (Designs) coordinator:</span
            ><input type="text" v-model="formData.coordinator" readonly />
          </div>
        </div>
      </div>

      <!-- LRU/SRU Details Section -->
      <div class="form-card read-only-section">
        <div class="section-header">
          <h3 class="section-title">LRU/SRU DETAILS</h3>
        </div>
        <div class="grid-layout two-col">
          <div class="grid-item-half">
            <span>LRU/SRU DETAILS</span
            ><input type="text" v-model="formData.partNo" readonly />
          </div>
          <div class="grid-item-half">
            <span>LRU/SRU Desc:</span
            ><input type="text" v-model="formData.description" readonly />
          </div>
        </div>
        <div class="grid-layout two-col-doc">
          <div class="grid-item">
            <span>Ref Doc</span
            ><input type="text" v-model="formData.refDoc" readonly />
          </div>
          <div class="grid-item">
            <span>Ref No of Document</span
            ><input type="text" v-model="formData.refNo" readonly />
          </div>
          <div class="grid-item">
            <span>ver</span
            ><input type="text" v-model="formData.version" readonly />
          </div>
          <div class="grid-item">
            <span>rev</span
            ><input type="text" v-model="formData.revision" readonly />
          </div>
        </div>
        <div class="grid-layout">
          <div class="grid-item">
            <span>Part No:</span
            ><input type="text" v-model="formData.partNo" readonly />
          </div>
          <div class="grid-item">
            <span>Manufacturer:</span
            ><input type="text" v-model="formData.manufacturer" readonly />
          </div>
          <div class="grid-item">
            <span>Sl.No of units:</span
            ><input type="text" v-model="formData.serialNo" readonly />
          </div>
          <div class="grid-item">
            <span>Drawing no/Rev:</span
            ><input type="text" v-model="formData.drawingRev" readonly />
          </div>
          <div class="grid-item">
            <span>Qty Offered:</span
            ><input type="text" v-model="formData.qtyOffered" readonly />
          </div>
          <div class="grid-item">
            <span>source:</span
            ><input type="text" v-model="formData.source" readonly />
          </div>
        </div>
        <div class="grid-layout two-col">
          <div class="grid-item-half">
            <span>UNIT IDENTIFICATION:</span
            ><input
              type="text"
              v-model="formData.unitIdentification"
              readonly
            />
          </div>
          <div class="grid-item-half">
            <span>MECHANICAL INSPN:</span
            ><input
              type="text"
              v-model="formData.mechanicalInspection"
              readonly
            />
          </div>
        </div>
        <div class="grid-layout two-col">
          <div class="grid-item-half">
            <span>INSPECTION /TEST STAGE OFFERED NOW:</span
            ><input type="text" v-model="formData.testStageOffered" readonly />
          </div>
          <div class="grid-item-half">
            <span>STTE Status:</span
            ><input type="text" v-model="formData.stteStatus" readonly />
          </div>
        </div>
      </div>

      <!-- Testing Details Section - Page break before for PDF -->
      <div class="form-card read-only-section page-break-before">
        <div class="section-header">
          <h3 class="section-title">TESTING DETAILS</h3>
        </div>
        <div class="grid-layout">
          <div class="grid-item-half">
            <span>Above Unit is ready for Testing at venue, dated onwards.</span
            ><input type="text" v-model="formData.venue" readonly />
          </div>
          <div class="grid-item-half">
            <span>Test facility to be used:</span
            ><input type="text" v-model="formData.testFacility" readonly />
          </div>
          <div class="grid-item-half">
            <span>Calibration status OK/Due on:</span
            ><input type="text" v-model="formData.calibrationStatus" readonly />
          </div>
          <div class="grid-item-half">
            <span>SIGNATURE: NAME / DESIGNATION</span
            ><input type="text" v-model="formData.nameDesignation" readonly />
          </div>
          <div class="grid-item-quarter">
            <span>Test cycle / Duration:</span
            ><input
              type="text"
              v-model="formData.testCycleDuration"
              readonly
            /><span>hrs</span>
          </div>
          <div class="grid-item-quarter">
            <span>Func. Check(Initial):</span
            ><input
              type="text"
              v-model="formData.funcCheckInitial"
              readonly
            /><span>date/time</span>
          </div>
          <div class="grid-item-quarter">
            <span>Test Start on:</span
            ><input type="text" v-model="formData.testStartOn" readonly /><span
              >date/time</span
            >
          </div>
          <div class="grid-item-quarter">
            <span>Perf. check (during):</span
            ><input
              type="text"
              v-model="formData.perfCheckDuring"
              readonly
            /><span>date/time</span>
          </div>
          <div class="grid-item-half">
            <span>Test complete on:</span
            ><input
              type="text"
              v-model="formData.testCompleteOn"
              readonly
            /><span>date/time</span>
          </div>
          <div class="grid-item-half">
            <span>Func Check (End):</span
            ><input type="text" v-model="formData.funcCheckEnd" readonly /><span
              >date/time</span
            >
          </div>
        </div>
      </div>

      <!-- Certifications Section -->
      <div class="form-card read-only-section">
        <div class="section-header">
          <h3 class="section-title">CERTIFICATIONS</h3>
        </div>
        <div class="grid-layout one-col-checkbox">
          <p class="checkbox-title">It is certified that :</p>
          <label
            ><input
              type="checkbox"
              v-model="formData.certifications.mechanicalQualityRecords"
              disabled
            />Mechanical Quality Records of all the parts (Raw material TC
            (chemical & mechanical), Dimensional reports, NDT reports, Process
            certificates etc.) & Electrical Quality Records (Components
            Screening report, PCB manufacturing report, process compliance
            reports/ test reports, etc.) were verified thoroughly.</label
          >
          <label
            ><input
              type="checkbox"
              v-model="formData.certifications.cocVerified"
              disabled
            />CoC for SRU, fasteners & standard parts are verified and
            satisfactory</label
          >
          <label
            ><input
              type="checkbox"
              v-model="formData.certifications.sruSerialNoted"
              disabled
            />Sl no of the SRUs are noted down in the respective log book opened
            on _________</label
          >
          <label
            ><input
              type="checkbox"
              v-model="formData.certifications.noDefectInvestigation"
              disabled
            />No Defect investigation is pending against this LRU</label
          >
          <label
            ><input
              type="checkbox"
              v-model="formData.certifications.previousTestStagesCleared"
              disabled
            />All the previous test stages of this LRU/SRU are cleared</label
          >
          <label
            ><input
              type="checkbox"
              v-model="formData.certifications.cascicQAInspected"
              disabled
            />CASCIC QA has physically inspected and accepted the LRU on
            _________</label
          >
          <span class="signature-line">SIGNATURE of Rep, IQA CASCIC</span>
        </div>
      </div>

      <!-- Remarks Section - Page break before for PDF -->
      <div class="form-card page-break-before">
        <div class="section-header">
          <h3 class="section-title">Action taken & remarks by DGAQA</h3>
        </div>
        <div class="grid-layout">
          <div class="readonly-display">{{ formData.remarks }}</div>
          <span class="signature-line right">SIGNATURE OF DGAQA REP..</span>
        </div>
      </div>

      <!-- Approval and Assignment Information (show for all roles when memo is approved) -->
      <div class="form-card" v-if="isMemoApprovedWithReviewer">
        <div class="section-header">
          <h3 class="section-title">APPROVAL AND ASSIGNMENT DETAILS</h3>
        </div>
        <div class="grid-layout">
          <div class="grid-item">
            <label>Date of Test or Review</label>
            <input
              type="text"
              :value="
                formatApprovalDate(
                  memoApprovalStatus.test_date ||
                    memoApprovalStatus.approval_date
                )
              "
              readonly
            />
          </div>
          <div class="grid-item">
            <label>Internal Tester ID</label>
            <input type="text" :value="assignedReviewer.id" readonly />
          </div>
          <div class="grid-item">
            <label>Internal Tester Name</label>
            <input type="text" :value="assignedReviewer.name" readonly />
          </div>
          <div class="grid-item-full">
            <label>Comments</label>
            <input
              type="text"
              :value="memoApprovalStatus.comments || 'No comments provided'"
              readonly
            />
          </div>
          <div class="grid-item">
            <label>Authentication</label>
            <div
              v-if="
                memoApprovalStatus.authentication &&
                isSignatureUrl(memoApprovalStatus.authentication)
              "
              class="signature-display-pdf"
            >
              <img
                :src="getSignatureImageUrl(memoApprovalStatus.authentication)"
                alt="Signature"
                class="signature-image-pdf"
              />
              <span class="signature-line">SIGNATURE</span>
            </div>
            <input
              v-else
              type="text"
              :value="memoApprovalStatus.authentication || 'Not provided'"
              readonly
            />
          </div>
          <div class="grid-item">
            <label>Attachments</label>
            <input
              type="text"
              :value="
                memoApprovalStatus.attachment_path
                  ? 'File attached'
                  : 'No attachments'
              "
              readonly
            />
          </div>
        </div>
      </div>

      <!-- Rejection Information (show for all roles when memo is rejected) -->
      <div class="form-card" v-if="isMemoRejected">
        <div class="section-header">
          <h3 class="section-title">REJECTION DETAILS</h3>
        </div>
        <div class="grid-layout">
          <div class="grid-item">
            <label>Date of Test or Review</label>
            <input
              type="text"
              :value="formatApprovalDate(memoApprovalStatus.approval_date)"
              readonly
            />
          </div>
          <div class="grid-item">
            <label>Internal Tester ID</label>
            <input
              type="text"
              :value="memoApprovalStatus.approved_by"
              readonly
            />
          </div>
          <div class="grid-item">
            <label>Internal Tester Name</label>
            <input type="text" value="QA Head" readonly />
          </div>
          <div class="grid-item-full">
            <label>Comments</label>
            <input
              type="text"
              :value="memoApprovalStatus.comments || 'No comments provided'"
              readonly
            />
          </div>
          <div class="grid-item">
            <label>Authentication</label>
            <div
              v-if="
                memoApprovalStatus.authentication &&
                isSignatureUrl(memoApprovalStatus.authentication)
              "
              class="signature-display-pdf"
            >
              <img
                :src="getSignatureImageUrl(memoApprovalStatus.authentication)"
                alt="Signature"
                class="signature-image-pdf"
              />
              <span class="signature-line">SIGNATURE</span>
            </div>
            <input
              v-else
              type="text"
              :value="memoApprovalStatus.authentication || 'Not provided'"
              readonly
            />
          </div>
          <div class="grid-item">
            <label>Attachments</label>
            <input
              type="text"
              :value="
                memoApprovalStatus.attachment_path
                  ? 'File attached'
                  : 'No attachments'
              "
              readonly
            />
          </div>
        </div>
      </div>
    </div>
    <!-- End Form Content -->

    <!-- QA Head Action Buttons (only show if memo is not processed) - Outside form-content to exclude from PDF -->
    <div
      class="form-section action-buttons"
      v-if="isQAHead && !isMemoProcessed"
    >
      <div class="button-container">
        <button class="btn btn-accept" @click="handleAccept">ACCEPT</button>
        <button class="btn btn-reject" @click="handleReject">REJECT</button>
      </div>
    </div>

    <!-- Accept Confirmation Overlay -->
    <div v-if="showAcceptOverlay" class="overlay">
      <div class="overlay-content approval-form">
        <h3>Memo Approval Form</h3>

        <div class="form-group">
          <label>Memo ID:</label>
          <input
            type="text"
            v-model="approvalForm.memo_id"
            readonly
            class="readonly-input"
          />
        </div>

        <div class="form-group">
          <label>Approval Date:</label>
          <input type="date" v-model="approvalForm.approval_date" required />
        </div>

        <div class="form-group">
          <label>Test Date (Optional):</label>
          <input type="datetime-local" v-model="approvalForm.test_date" />
          <small class="file-info">Optional: Select test date and time</small>
        </div>

        <div class="form-group">
          <label>QA Reviewer: <span class="required-field">*</span></label>
          <select
            v-model="approvalForm.user_id"
            @change="onUserChange"
            required
          >
            <option value="">Select a QA Reviewer</option>
            <option
              v-for="reviewer in qaReviewers"
              :key="reviewer.id"
              :value="reviewer.id"
            >
              {{ reviewer.name }} ({{ reviewer.email }})
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>User ID:</label>
          <input
            type="text"
            v-model="approvalForm.user_id"
            readonly
            class="readonly-input"
          />
        </div>

        <div class="form-group">
          <label>Comments:</label>
          <textarea
            v-model="approvalForm.comments"
            placeholder="Enter your comments..."
            required
          ></textarea>
        </div>

        <div class="form-group">
          <label>Signature Authentication:</label>
          <div class="signature-auth-container">
            <div class="signature-inputs">
              <div class="input-group">
                <label>Username:</label>
                <input
                  type="text"
                  v-model="approvalForm.signatureUsername"
                  placeholder="Enter username..."
                  required
                />
              </div>
              <div class="input-group">
                <label>Signature Password:</label>
                <input
                  type="password"
                  v-model="approvalForm.signaturePassword"
                  placeholder="Enter signature password..."
                  required
                />
              </div>
              <button
                type="button"
                class="btn btn-verify"
                @click="verifySignature('approval')"
                :disabled="
                  !approvalForm.signatureUsername ||
                  !approvalForm.signaturePassword
                "
              >
                Verify & Load Signature
              </button>
            </div>
            <div v-if="approvalForm.signatureUrl" class="signature-display">
              <label>Verified Signature:</label>
              <div class="signature-image-container">
                <img
                  :src="approvalForm.signatureUrl"
                  alt="Verified Signature"
                  class="signature-image"
                />
                <div class="signature-info">
                  <span class="signature-user">{{
                    approvalForm.verifiedUserName
                  }}</span>
                  <span class="signature-role"
                    >{{ approvalForm.verifiedUserRole }} Signature</span
                  >
                  <span class="signature-status">✓ Verified</span>
                </div>
              </div>
            </div>
            <div v-if="approvalForm.signatureError" class="signature-error">
              {{ approvalForm.signatureError }}
            </div>
          </div>
        </div>

        <div class="form-group">
          <label>Attachments (PDF):</label>
          <input type="file" @change="onFileChange" accept=".pdf" />
          <small class="file-info">Optional: Upload PDF attachment</small>
        </div>

        <div class="overlay-buttons">
          <button class="btn btn-confirm" @click="confirmAccept">
            Approve Memo
          </button>
          <button class="btn btn-cancel" @click="cancelAccept">Cancel</button>
        </div>
      </div>
    </div>

    <!-- Reject Confirmation Overlay -->
    <div v-if="showRejectOverlay" class="overlay">
      <div class="overlay-content rejection-form">
        <h3>Memo Rejection Form</h3>

        <div class="form-group">
          <label>Memo ID:</label>
          <input
            type="text"
            v-model="rejectionForm.memo_id"
            readonly
            class="readonly-input"
          />
        </div>

        <div class="form-group">
          <label>Comments:</label>
          <textarea
            v-model="rejectionForm.comments"
            placeholder="Enter rejection comments..."
            required
          ></textarea>
        </div>

        <div class="form-group">
          <label>Signature Authentication:</label>
          <div class="signature-auth-container">
            <div class="signature-inputs">
              <div class="input-group">
                <label>Username:</label>
                <input
                  type="text"
                  v-model="rejectionForm.signatureUsername"
                  placeholder="Enter username..."
                  required
                />
              </div>
              <div class="input-group">
                <label>Signature Password:</label>
                <input
                  type="password"
                  v-model="rejectionForm.signaturePassword"
                  placeholder="Enter signature password..."
                  required
                />
              </div>
              <button
                type="button"
                class="btn btn-verify"
                @click="verifySignature('rejection')"
                :disabled="
                  !rejectionForm.signatureUsername ||
                  !rejectionForm.signaturePassword
                "
              >
                Verify & Load Signature
              </button>
            </div>
            <div v-if="rejectionForm.signatureUrl" class="signature-display">
              <label>Verified Signature:</label>
              <div class="signature-image-container">
                <img
                  :src="rejectionForm.signatureUrl"
                  alt="Verified Signature"
                  class="signature-image"
                />
                <div class="signature-info">
                  <span class="signature-user">{{
                    rejectionForm.verifiedUserName
                  }}</span>
                  <span class="signature-role"
                    >{{ rejectionForm.verifiedUserRole }} Signature</span
                  >
                  <span class="signature-status">✓ Verified</span>
                </div>
              </div>
            </div>
            <div v-if="rejectionForm.signatureError" class="signature-error">
              {{ rejectionForm.signatureError }}
            </div>
          </div>
        </div>

        <div class="form-group">
          <label>Attachments (PDF):</label>
          <input type="file" @change="onRejectionFileChange" accept=".pdf" />
          <small class="file-info">Optional: Upload PDF attachment</small>
        </div>

        <div class="overlay-buttons">
          <button class="btn btn-confirm" @click="confirmReject">
            Reject Memo
          </button>
          <button class="btn btn-cancel" @click="cancelReject">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { userStore } from "@/stores/userStore";
// Dynamic import for html2pdf to avoid blocking app initialization
let html2pdf;

export default {
  name: "ViewOnlyMemoForm",
  props: {
    id: {
      type: [String, Number],
      required: true,
    },
    memoData: {
      type: Object,
      default: null,
    },
    references: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      showAcceptOverlay: false,
      showRejectOverlay: false,
      qaReviewers: [],
      assignedReviewer: null,
      memoApprovalStatus: null,
      approvalForm: {
        memo_id: null,
        user_id: "",
        user_name: "",
        comments: "",
        authentication: "",
        attachment: null,
        approval_date: "",
        test_date: "",
        // Signature authentication fields
        signatureUsername: "",
        signaturePassword: "",
        signatureUrl: "",
        verifiedUserName: "",
        verifiedUserRole: "",
        signatureError: "",
      },
      rejectionForm: {
        memo_id: null,
        comments: "",
        authentication: "",
        attachment: null,
        // Signature authentication fields
        signatureUsername: "",
        signaturePassword: "",
        signatureUrl: "",
        verifiedUserName: "",
        verifiedUserRole: "",
        signatureError: "",
      },
      formData: {
        // Basic information
        from1: "",
        from2: "",
        from3: "",
        casdic: "",
        casdicDate: "",
        wingRef: "",
        coordinator: "",

        // LRU/SRU Details
        partNo: "",
        manufacturer: "",
        description: "",
        refDoc: "",
        refNo: "",
        version: "",
        revision: "",

        // Additional reference documents
        description2: "",
        refDoc2: "",
        refNo2: "",
        version2: "",
        revision2: "",
        description3: "",
        refDoc3: "",
        refNo3: "",
        version3: "",
        revision3: "",
        description4: "",
        refDoc4: "",
        refNo4: "",
        version4: "",
        revision4: "",
        description5: "",
        refDoc5: "",
        refNo5: "",
        version5: "",
        revision5: "",
        description6: "",
        refDoc6: "",
        refNo6: "",
        version6: "",
        revision6: "",

        // Additional details
        drawingRev: "",
        source: "",
        serialNo: "",
        qtyOffered: "",
        unitIdentification: "",
        mechanicalInspection: "",
        testStageOffered: "",
        testStageCleared: "",
        stteStatus: "",

        // Testing details
        venue: "",
        memoDate: "",
        nameDesignation: "",
        testFacility: "",
        testCycleDuration: "",
        testStartOn: "",
        testCompleteOn: "",
        calibrationStatus: "",
        funcCheckInitial: "",
        perfCheckDuring: "",
        funcCheckEnd: "",

        // Certifications
        certifications: {
          mechanicalQualityRecords: false,
          cocVerified: false,
          sruSerialNoted: false,
          noDefectInvestigation: false,
          previousTestStagesCleared: false,
          cascicQAInspected: false,
        },

        // Remarks
        remarks: "",
      },
    };
  },
  computed: {
    // Get current user role from global store
    currentUserRole() {
      return userStore.getters.currentUserRole();
    },
    // Check if current user is QA Head (role_id = 2)
    isQAHead() {
      return this.currentUserRole === 2;
    },
    // Check if memo is approved and has assigned reviewer
    isMemoApprovedWithReviewer() {
      console.log(
        "approval status:",
        this.memoApprovalStatus,
        "assigned reviewer:",
        this.assignedReviewer,
        "memo status",
        this.memoApprovalStatus
      );
      return (
        this.memoApprovalStatus &&
        this.memoApprovalStatus.status === "accepted" &&
        this.assignedReviewer
      );
    },
    // Check if memo is rejected
    isMemoRejected() {
      return (
        this.memoApprovalStatus && this.memoApprovalStatus.status === "rejected"
      );
    },
    // Check if memo is approved (for hiding buttons)
    isMemoApproved() {
      return (
        this.memoApprovalStatus && this.memoApprovalStatus.status === "accepted"
      );
    },
    // Check if memo has been processed (approved or rejected)
    isMemoProcessed() {
      return (
        this.memoApprovalStatus &&
        (this.memoApprovalStatus.status === "accepted" ||
          this.memoApprovalStatus.status === "rejected")
      );
    },
  },
  async mounted() {
    await this.fetchMemoData();
    await this.fetchQAReviewers();
    await this.fetchMemoApprovalStatus();
  },
  methods: {
    // Check if the authentication field contains a signature URL or path
    isSignatureUrl(authentication) {
      if (!authentication) return false;
      return (
        authentication.includes("http://localhost:8000/api/users/signature/") ||
        authentication.startsWith("/api/users/signature/")
      );
    },
    // Get the full URL for signature image
    getSignatureImageUrl(authentication) {
      if (!authentication) return "";
      if (
        authentication.startsWith("http://") ||
        authentication.startsWith("https://")
      ) {
        return authentication;
      }
      if (authentication.startsWith("/api/users/signature/")) {
        return `http://localhost:8000${authentication}`;
      }
      return authentication;
    },

    async fetchMemoData() {
      try {
        // If memo data is passed as props (from dashboard navigation), use it
        if (this.$route.params.memoData && this.$route.params.references) {
          this.transformAndSetMemoData(
            this.$route.params.memoData,
            this.$route.params.references
          );
          return;
        }

        // Otherwise, fetch from API
        const response = await fetch(
          `http://localhost:8000/api/memos/${this.id}`
        );
        if (!response.ok) {
          throw new Error(
            `Failed to fetch memo details: ${response.statusText}`
          );
        }

        const data = await response.json();
        if (data.success) {
          this.transformAndSetMemoData(data.memo, data.references || []);
          console.log("Fetched memo data:", data.memo, data.references);
          
        } else {
          throw new Error(data.message || "Failed to fetch memo details");
        }
      } catch (error) {
        console.error("Error fetching memo data:", error);
        // Fallback to default data if fetch fails
        console.log("Using default memo data due to fetch error");
      }
    },

    transformAndSetMemoData(backendMemo, references) {
      console.log("Transforming backend memo data:", backendMemo, references);

      // Transform backend memo data to frontend format
      this.formData = {
        // Basic information
        from1: backendMemo.from_person || "",
        from2: backendMemo.to_person || "",
        from3: "ORDAQA(ADE), Bangalore",
        casdic: backendMemo.casdic_ref_no || "",
        casdicDate: this.formatDate(backendMemo.dated),
        wingRef: backendMemo.wing_proj_ref_no || "",
        coordinator: backendMemo.coordinator || "",

        // LRU/SRU Details
        partNo: backendMemo.part_number || "",
        manufacturer: backendMemo.manufacturer || "",
        description: backendMemo.lru_sru_desc || "",
        refDoc: references[0]?.ref_doc || "",
        refNo: references[0]?.ref_no || "",
        version: references[0]?.ver?.toString() || "",
        revision: references[0]?.rev?.toString() || "",

        // Additional reference documents
        description2: "",
        refDoc2: references[1]?.ref_doc || "",
        refNo2: references[1]?.ref_no || "",
        version2: references[1]?.ver?.toString() || "",
        revision2: references[1]?.rev?.toString() || "",
        description3: "",
        refDoc3: references[2]?.ref_doc || "",
        refNo3: references[2]?.ref_no || "",
        version3: references[2]?.ver?.toString() || "",
        revision3: references[2]?.rev?.toString() || "",
        description4: "",
        refDoc4: references[3]?.ref_doc || "",
        refNo4: references[3]?.ref_no || "",
        version4: references[3]?.ver?.toString() || "",
        revision4: references[3]?.rev?.toString() || "",
        description5: "",
        refDoc5: references[4]?.ref_doc || "",
        refNo5: references[4]?.ref_no || "",
        version5: references[4]?.ver?.toString() || "",
        revision5: references[4]?.rev?.toString() || "",
        description6: "",
        refDoc6: references[5]?.ref_doc || "",
        refNo6: references[5]?.ref_no || "",
        version6: references[5]?.ver?.toString() || "",
        revision6: references[5]?.rev?.toString() || "",

        // Additional details
        drawingRev: backendMemo.drawing_no_rev || "",
        source: backendMemo.source || "NA",
        serialNo: this.formatSerialNumbers(backendMemo.slno_units),
        qtyOffered: backendMemo.qty_offered?.toString() || "0",
        // unitIdentification: this.formatUnitIdentification(
        //   backendMemo.unit_identification
        // ),
        unitIdentification: backendMemo.unit_identification || "",
        mechanicalInspection: backendMemo.mechanical_inspn || "",
        testStageOffered: backendMemo.inspn_test_stage_offered || "",
        testStageCleared: backendMemo.test_stage_cleared || "",
        stteStatus: backendMemo.stte_status || "",

        // Testing details
        venue: backendMemo.venue || "",
        memoDate: this.formatDate(backendMemo.memo_date),
        nameDesignation: backendMemo.name_designation || "",
        testFacility: backendMemo.test_facility || "",
        testCycleDuration: backendMemo.test_cycle_duration || "",
        testStartOn: this.formatDateTime(backendMemo.test_start_on),
        testCompleteOn: this.formatDateTime(backendMemo.test_complete_on),
        calibrationStatus: backendMemo.calibration_status || "",
        funcCheckInitial: this.formatDateTime(backendMemo.func_check_initial),
        perfCheckDuring: this.formatDateTime(backendMemo.perf_check_during),
        funcCheckEnd: this.formatDateTime(backendMemo.func_check_end),

        // Certifications
        certifications: {
          mechanicalQualityRecords:
            backendMemo.certified?.includes("a") || false,
          cocVerified: backendMemo.certified?.includes("b") || false,
          sruSerialNoted: backendMemo.certified?.includes("c") || false,
          noDefectInvestigation: backendMemo.certified?.includes("d") || false,
          previousTestStagesCleared:
            backendMemo.certified?.includes("e") || false,
          cascicQAInspected: backendMemo.certified?.includes("f") || false,
        },

        // Remarks
        remarks: backendMemo.remarks || "",
      };
    },

    formatDate(dateString) {
      if (!dateString) return "";
      try {
        const date = new Date(dateString);
        return date
          .toLocaleDateString("en-GB", {
            day: "2-digit",
            month: "2-digit",
            year: "numeric",
          })
          .replace(/\//g, "-");
      } catch {
        return dateString;
      }
    },

    formatDateTime(datetimeString) {
      if (!datetimeString) return "";
      try {
        const date = new Date(datetimeString);
        return date
          .toLocaleString("en-GB", {
            day: "2-digit",
            month: "2-digit",
            year: "numeric",
            hour: "2-digit",
            minute: "2-digit",
          })
          .replace(",", "");
      } catch {
        return datetimeString;
      }
    },

    formatSerialNumbers(serialArray) {
      if (!serialArray || !Array.isArray(serialArray)) return "";
      return serialArray.join(", ");
    },

    // formatUnitIdentification(unitIdArray) {
    //   if (!unitIdArray || !Array.isArray(unitIdArray)) return "";
    //   return unitIdArray.join(", ");
    // },

    // Handle accept button click
    handleAccept() {
      // Set memo_id from props
      this.approvalForm.memo_id = this.id;
      // Set current date as default approval date
      this.approvalForm.approval_date = new Date().toISOString().split("T")[0];
      this.showAcceptOverlay = true;
    },

    // Handle reject button click
    handleReject() {
      this.rejectionForm.memo_id = this.id;
      this.showRejectOverlay = true;
    },

    // Fetch QA reviewers for dropdown
    async fetchQAReviewers() {
      try {
        const response = await fetch(
          "http://localhost:8000/api/available-reviewers"
        );
        const data = await response.json();

        if (data.success) {
          this.qaReviewers = data.reviewers;
        } else {
          console.error("Failed to fetch QA reviewers:", data.message);
        }
      } catch (error) {
        console.error("Error fetching QA reviewers:", error);
      }
    },

    // Fetch memo approval status and assigned reviewer
    async fetchMemoApprovalStatus() {
      try {
        const response = await fetch(
          `http://localhost:8000/api/memos/${this.id}/approval-status`
        );
        const data = await response.json();

        if (data.success) {
          this.memoApprovalStatus = data.approval;
          if (
            data.approval &&
            data.approval.status === "accepted" &&
            data.approval.user_id
          ) {
            // Find the reviewer details from the QA reviewers list
            this.assignedReviewer = this.qaReviewers.find(
              (reviewer) => reviewer.id === data.approval.user_id
            );

            // If not found in the current list, fetch user details
            if (!this.assignedReviewer) {
              await this.fetchReviewerDetails(data.approval.user_id);
            }
          }
        } else {
          console.log("No approval status found for memo:", this.id);
        }
      } catch (error) {
        console.error("Error fetching memo approval status:", error);
      }
    },

    // Fetch reviewer details by user ID
    async fetchReviewerDetails(userId) {
      try {
        const response = await fetch(
          `http://localhost:8000/api/users/${userId}`
        );
        const data = await response.json();

        if (data.success) {
          this.assignedReviewer = {
            id: data.user.user_id,
            name: data.user.name,
            email: data.user.email,
          };
        }
      } catch (error) {
        console.error("Error fetching reviewer details:", error);
      }
    },

    // Handle user selection change
    onUserChange() {
      if (this.approvalForm.user_id) {
        const selectedUser = this.qaReviewers.find(
          (user) => user.id === parseInt(this.approvalForm.user_id)
        );
        if (selectedUser) {
          this.approvalForm.user_name = selectedUser.name;
        }
      } else {
        this.approvalForm.user_name = "";
      }
    },

    // Handle file upload
    onFileChange(event) {
      const file = event.target.files[0];
      if (file && file.type === "application/pdf") {
        this.approvalForm.attachment = file;
      } else {
        alert("Please select a PDF file");
        event.target.value = "";
      }
    },

    // Verify signature credentials
    async verifySignature(formType) {
      const form =
        formType === "approval" ? this.approvalForm : this.rejectionForm;

      if (!form.signatureUsername || !form.signaturePassword) {
        form.signatureError =
          "Please enter both username and signature password";
        return;
      }

      try {
        const response = await fetch("/api/users/verify-signature", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username: form.signatureUsername,
            signature_password: form.signaturePassword,
          }),
        });

        const data = await response.json();
        console.log("DATAAAA Signature verification response:", data);

        if (data.success) {
          form.signatureUrl = data.signature_url;
          form.verifiedUserName = data.user_name;
          form.verifiedUserRole = data.role_name;
          form.authentication = data.signature_url; // Store signature URL as authentication
          form.signatureError = "";
        } else {
          form.signatureError = data.message || "Failed to verify signature";
          form.signatureUrl = "";
          form.verifiedUserName = "";
          form.verifiedUserRole = "";
          form.authentication = "";
        }
      } catch (error) {
        form.signatureError = "Error verifying signature: " + error.message;
        form.signatureUrl = "";
        form.verifiedUserName = "";
        form.verifiedUserRole = "";
        form.authentication = "";
      }
    },

    // Validate approval form
    validateApprovalForm() {
      if (!this.approvalForm.user_id) {
        alert("Please select a QA Reviewer");
        return false;
      }
      if (!this.approvalForm.comments.trim()) {
        alert("Please enter comments");
        return false;
      }
      if (!this.approvalForm.signatureUrl) {
        alert("Please verify your signature before proceeding");
        return false;
      }
      return true;
    },

    // Confirm accept action
    async confirmAccept() {
      if (!this.validateApprovalForm()) {
        return;
      }

      try {
        // Get current user (QA Head) from store
        const currentUser = userStore.getters.currentUser();
        if (!currentUser || !currentUser.id) {
          alert("Error: Could not identify current user. Please log in again.");
          return;
        }

        // Prepare form data for file upload
        const formData = new FormData();
        formData.append("memo_id", this.approvalForm.memo_id);
        formData.append("user_id", this.approvalForm.user_id); // QA Reviewer ID
        formData.append("approved_by", currentUser.id); // QA Head ID (current user)
        formData.append("comments", this.approvalForm.comments);
        formData.append("authentication", this.approvalForm.authentication);
        formData.append("approval_date", this.approvalForm.approval_date);
        formData.append("test_date", this.approvalForm.test_date || ""); // Optional test date
        formData.append("status", "accepted");

        if (this.approvalForm.attachment) {
          formData.append("attachment", this.approvalForm.attachment);
        }

        const response = await fetch(
          `http://localhost:8000/api/memos/${this.approvalForm.memo_id}/approve`,
          {
            method: "POST",
            body: formData,
          }
        );

        const data = await response.json();

        if (data.success) {
          alert("Memo has been accepted successfully!");
          this.showAcceptOverlay = false;
          this.resetApprovalForm();
          // Refresh approval status and reviewer info
          await this.fetchMemoApprovalStatus();
        } else {
          alert(`Error: ${data.message}`);
        }
      } catch (error) {
        console.error("Error accepting memo:", error);
        alert("Error accepting memo. Please try again.");
      }
    },

    // Confirm reject action
    async confirmReject() {
      if (!this.validateRejectionForm()) {
        return;
      }

      try {
        // Get current user (QA Head) from store
        const currentUser = userStore.getters.currentUser();
        if (!currentUser || !currentUser.id) {
          alert("Error: Could not identify current user. Please log in again.");
          return;
        }

        // Prepare form data for file upload
        const formData = new FormData();
        formData.append("memo_id", this.rejectionForm.memo_id);
        formData.append("approved_by", currentUser.id); // QA Head ID (current user)
        formData.append("comments", this.rejectionForm.comments);
        formData.append("authentication", this.rejectionForm.authentication);
        formData.append("status", "rejected");

        if (this.rejectionForm.attachment) {
          formData.append("attachment", this.rejectionForm.attachment);
        }

        const response = await fetch(
          `http://localhost:8000/api/memos/${this.rejectionForm.memo_id}/approve`,
          {
            method: "POST",
            body: formData,
          }
        );

        const data = await response.json();

        if (data.success) {
          alert("Memo has been rejected successfully!");
          this.showRejectOverlay = false;
          this.resetRejectionForm();
          // Refresh approval status
          await this.fetchMemoApprovalStatus();
        } else {
          alert(`Error: ${data.message}`);
        }
      } catch (error) {
        console.error("Error rejecting memo:", error);
        alert("Error rejecting memo. Please try again.");
      }
    },

    // Cancel accept action
    cancelAccept() {
      this.showAcceptOverlay = false;
    },

    // Cancel reject action
    cancelReject() {
      this.showRejectOverlay = false;
    },

    // Validate rejection form
    validateRejectionForm() {
      if (!this.rejectionForm.comments.trim()) {
        alert("Please enter rejection comments");
        return false;
      }
      if (!this.rejectionForm.signatureUrl) {
        alert("Please verify your signature before proceeding");
        return false;
      }
      return true;
    },

    // Handle rejection file change
    onRejectionFileChange(event) {
      const file = event.target.files[0];
      if (file && file.type === "application/pdf") {
        this.rejectionForm.attachment = file;
      } else {
        alert("Please select a PDF file");
        event.target.value = "";
      }
    },

    // Reset rejection form
    resetRejectionForm() {
      this.rejectionForm = {
        memo_id: null,
        comments: "",
        authentication: "",
        attachment: null,
        // Signature authentication fields
        signatureUsername: "",
        signaturePassword: "",
        signatureUrl: "",
        verifiedUserName: "",
        verifiedUserRole: "",
        signatureError: "",
      };
    },

    // Reset approval form
    resetApprovalForm() {
      this.approvalForm = {
        memo_id: null,
        user_id: "",
        user_name: "",
        comments: "",
        authentication: "",
        attachment: null,
        approval_date: "",
        test_date: "",
        // Signature authentication fields
        signatureUsername: "",
        signaturePassword: "",
        signatureUrl: "",
        verifiedUserName: "",
        verifiedUserRole: "",
        signatureError: "",
      };
    },

    // Format approval date for display
    formatApprovalDate(dateString) {
      if (!dateString) return "N/A";
      try {
        const date = new Date(dateString);
        return date.toLocaleString("en-GB", {
          day: "2-digit",
          month: "2-digit",
          year: "numeric",
          hour: "2-digit",
          minute: "2-digit",
        });
      } catch {
        return dateString;
      }
    },

    // Download memo PDF
    async downloadMemoPDF() {
      try {
        // Dynamically import html2pdf to avoid blocking app initialization
        if (!html2pdf) {
          const html2pdfModule = await import("html2pdf.js");
          html2pdf = html2pdfModule.default || html2pdfModule;
        }

        console.log(`Downloading PDF for memo ID: ${this.id}`);

        // Hide Test Status section for PDF (if it exists)
        const testStatusSection = document.querySelector(".exclude-from-pdf");
        let wasHidden = false;
        if (testStatusSection) {
          wasHidden = testStatusSection.style.display === "none";
          testStatusSection.style.display = "none";
        }

        // Ensure page break styles are applied for PDF generation
        const pageBreakElements =
          document.querySelectorAll(".page-break-before");
        pageBreakElements.forEach((element) => {
          element.style.pageBreakBefore = "always";
          element.style.breakBefore = "page";
        });

        // Get the element you want to convert (the main memo content - exclude header/UI)
        const element = document.querySelector(".form-content");

        if (!element) {
          alert("Memo content not found");
          // Restore Test Status section if it was hidden
          if (testStatusSection && !wasHidden) {
            testStatusSection.style.display = "";
          }
          return;
        }

        // Configure options to match the page appearance
        const opt = {
          margin: 0.5,
          filename: `memo_${this.id}_${new Date()
            .toISOString()
            .slice(0, 10)}.pdf`,
          image: { type: "jpeg", quality: 0.98 },
          html2canvas: {
            scale: 2,
            useCORS: true,
            letterRendering: true,
            allowTaint: true,
            windowWidth: element.scrollWidth,
            windowHeight: element.scrollHeight,
          },
          jsPDF: {
            unit: "in",
            format: "a4",
            orientation: "portrait",
          },
        };

        // Generate PDF from HTML
        await html2pdf().set(opt).from(element).save();

        console.log(`PDF downloaded successfully for memo ${this.id}`);

        // Restore Test Status section visibility
        if (testStatusSection && !wasHidden) {
          testStatusSection.style.display = "";
        }
      } catch (error) {
        console.error("Error downloading memo PDF:", error);
        alert(`Error downloading PDF: ${error.message}`);

        // Restore Test Status section visibility on error
        const testStatusSection = document.querySelector(".exclude-from-pdf");
        if (testStatusSection) {
          testStatusSection.style.display = "";
        }
      }
    },
  },
};
</script>

<style scoped>
/* Scoped styles to prevent them from affecting other components */
:root {
  --background-color: #f0f0f0;
  --card-color: #e0e0e0;
  --text-color: #333;
  --border-color: #999;
  --input-bg: #fff;
  --button-bg: #007bff;
  --button-text: #fff;
}

.memo-form {
  display: flex;
  flex-direction: column;
  height: 100vh;
  font-family: sans-serif;
  color: var(--text-color);
  background-color: var(--background-color);
}

.form-content {
  flex-grow: 1;
  overflow-y: auto;
  padding: 20px;
  box-sizing: border-box;
}

.form-card {
  background-color: var(--card-color, #e0e0e0);
  border: 1px solid var(--border-color, #999);
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 20px;
}

/* Page break for PDF generation */
.page-break-before {
  page-break-before: always;
  break-before: page;
}

.card-title {
  text-align: center;
  margin-top: 0;
  font-size: 1.1em;
}

.grid-layout {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.grid-layout.two-col {
  grid-template-columns: 1fr 1fr;
}

.grid-layout.two-col-doc {
  grid-template-columns: 1fr 1fr 0.5fr 0.5fr;
}

.grid-layout.one-col-checkbox {
  grid-template-columns: 1fr;
}

.grid-layout.one-col-radio {
  grid-template-columns: 1fr;
}

.grid-item {
  display: flex;
  flex-direction: column;
}

.grid-item-half,
.grid-item-quarter {
  display: flex;
  flex-direction: column;
}

.grid-item-full {
  grid-column: 1 / -1;
  display: flex;
  flex-direction: column;
}

.grid-item input,
.grid-item-full input,
.grid-item-half input,
.grid-item-quarter input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #d0d0d0;
  border-radius: 0;
  background-color: #f5f5f5;
  box-sizing: border-box;
  margin-top: 5px;
  font-size: 14px;
  transition: none;
}

.grid-item input:focus,
.grid-item-full input:focus,
.grid-item-half input:focus,
.grid-item-quarter input:focus {
  outline: none;
  border-color: #b0b0b0;
  background-color: #f0f0f0;
  box-shadow: none;
}

.grid-item input[readonly] {
  background-color: #f5f5f5;
  color: #333;
  cursor: default;
  border: 1px solid #d0d0d0;
}

.grid-item input:not([readonly]) {
  background-color: #f5f5f5;
  color: var(--text-color, #333);
  cursor: text;
}

.grid-item span,
.grid-item-full span,
.grid-item-half span,
.grid-item-quarter span {
  font-size: 0.9em;
}

.signature-line {
  display: block;
  text-align: right;
  margin-top: 20px;
  margin-left: auto;
  font-weight: bold;
}

.signature-line.right {
  text-align: right;
}

.one-col-checkbox label {
  display: flex;
  align-items: flex-start;
  margin-bottom: 10px;
  font-size: 0.9em;
  line-height: 1.2;
}

.one-col-checkbox input[type="checkbox"] {
  margin-right: 10px;
  margin-top: 2px;
}

.one-col-checkbox input[type="checkbox"]:not([disabled]) {
  transform: scale(1.2);
  accent-color: #000;
}

.one-col-checkbox input[type="checkbox"][disabled] {
  opacity: 0.6;
  cursor: not-allowed;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #000;
}

.section-title {
  margin: 0;
  color: #000;
  font-size: 1.1em;
  font-weight: bold;
}

.read-only-section {
  border-left: none;
  background-color: #fff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  border: 1px solid var(--border-color, #999);
}

.readonly-display {
  grid-column: 1 / -1;
  padding: 10px;
  background-color: #f5f5f5;
  border: 1px solid #d0d0d0;
  min-height: 50px;
  margin-bottom: 10px;
}

.checkbox-title {
  font-weight: bold;
  margin-bottom: 10px;
}

.form-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #000;
}

.back-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.back-button:hover {
  background-color: #f0f0f0;
}

.form-title {
  text-align: center;
  font-size: 1.5em;
  font-weight: bold;
  margin: 0;
  flex-grow: 1;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 15px;
}

.view-only-badge {
  background: #28a745;
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 0.9em;
  font-weight: bold;
}

.download-pdf-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 123, 255, 0.2);
}

.download-pdf-btn:hover:not(:disabled) {
  background-color: #0056b3;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 123, 255, 0.3);
}

.download-pdf-btn:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
  transform: none;
  box-shadow: 0 2px 4px rgba(108, 117, 125, 0.2);
}

.download-pdf-btn .icon {
  width: 16px;
  height: 16px;
}

.download-text {
  font-size: 14px;
  font-weight: 500;
}

.logos-container {
  display: flex;
  gap: 10px;
}

.logo {
  height: 40px;
}

.form-section {
  margin-bottom: 30px;
  border: 2px solid #000;
  padding: 20px;
}

.form-table {
  width: 100%;
  border-collapse: collapse;
}

.form-cell {
  padding: 10px;
  vertical-align: top;
}

.form-cell label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
  font-size: 0.9em;
}

.form-cell input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.9em;
}

.readonly-field {
  background-color: #f8f9fa;
  color: #6c757d;
  cursor: default;
}

.lru-grid {
  width: 100%;
  border-collapse: collapse;
  border: 2px solid #000;
}

.lru-grid th,
.lru-grid td {
  border: 1px solid #000;
  padding: 10px;
  text-align: center;
  font-weight: bold;
  font-size: 0.9em;
}

.lru-cell {
  width: 20%;
}

.desc-cell {
  width: 25%;
}

.ref-cell,
.refno-cell,
.ver-cell,
.rev-cell {
  width: 13.75%;
}

.lru-field {
  margin-bottom: 10px;
}

.lru-field label {
  font-size: 0.8em;
  margin-bottom: 3px;
}

.lru-description-input {
  width: 100%;
  text-align: left;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.checkbox-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.9em;
}

.checkbox-item input[type="checkbox"] {
  width: auto;
}

.remarks-textarea {
  width: 100%;
  height: 100px;
  resize: vertical;
}

.certification h3 {
  margin-bottom: 15px;
  font-size: 1.1em;
}

.testing-details .form-table,
.additional-details .form-table {
  margin-top: 10px;
}

/* Action Buttons Styles */
.action-buttons {
  text-align: center;
  padding: 30px 20px;
  background-color: #f8f9fa;
  border: 2px solid #000;
}

.button-container {
  display: flex;
  gap: 20px;
  justify-content: center;
  align-items: center;
}

.btn {
  padding: 12px 30px;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.btn-accept {
  background-color: #28a745;
  color: white;
  border: 2px solid #28a745;
}

.btn-accept:hover {
  background-color: #218838;
  border-color: #1e7e34;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(40, 167, 69, 0.3);
}

.btn-reject {
  background-color: #dc3545;
  color: white;
  border: 2px solid #dc3545;
}

.btn-reject:hover {
  background-color: #c82333;
  border-color: #bd2130;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(220, 53, 69, 0.3);
}

/* Overlay Styles */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.overlay-content {
  background: white;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  text-align: center;
  max-width: 400px;
  width: 90%;
  height: 60%;
}

.overlay-content h3 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 1.5em;
}

.overlay-content p {
  margin: 0 0 25px 0;
  color: #666;
  font-size: 1.1em;
}

.overlay-buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
}

.btn-confirm {
  background-color: #007bff;
  color: white;
  border: 2px solid #007bff;
  padding: 10px 20px;
  font-size: 14px;
}

.btn-confirm:hover {
  background-color: #0056b3;
  border-color: #004085;
}

.btn-cancel {
  background-color: #6c757d;
  color: white;
  border: 2px solid #6c757d;
  padding: 10px 20px;
  font-size: 14px;
}

.btn-cancel:hover {
  background-color: #545b62;
  border-color: #4e555b;
}

/* Approval Form Styles */
.approval-form {
  max-width: 600px;
  width: 95%;
  max-height: 90vh;
  overflow-y: auto;
}

/* Rejection Form Styles */
.rejection-form {
  max-width: 600px;
  width: 95%;
  max-height: 90vh;
  overflow-y: auto;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #333;
  font-size: 14px;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 2px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  box-sizing: border-box;
  transition: border-color 0.3s ease;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #007bff;
}

.readonly-input {
  background-color: #f8f9fa;
  color: #6c757d;
  cursor: not-allowed;
}

.form-group textarea {
  height: 80px;
  resize: vertical;
}

.file-info {
  display: block;
  margin-top: 5px;
  color: #666;
  font-size: 12px;
  font-style: italic;
}

.form-group input[type="file"] {
  padding: 5px;
  border: 2px dashed #ddd;
  background-color: #f8f9fa;
  cursor: pointer;
}

.form-group input[type="file"]:hover {
  border-color: #007bff;
  background-color: #e3f2fd;
}

/* Status Badge Styles */
.status-badge {
  display: inline-block;
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: bold;
  font-size: 0.9em;
  text-align: center;
  margin-bottom: 15px;
  width: 100%;
  box-sizing: border-box;
}

.approved-badge {
  background-color: #d4edda;
  color: #155724;
  border: 2px solid #28a745;
}

.rejected-badge {
  background-color: #f8d7da;
  color: #721c24;
  border: 2px solid #dc3545;
}

/* Test Review Details Section Styles */
.reviewer-info-section,
.rejection-info-section {
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 25px;
  margin-top: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Approved Section - Green Theme */
.approved-section {
  background-color: #f0f9f0;
  border: 2px solid #28a745;
}

.approved-section h3 {
  color: #28a745;
}

/* Rejected Section - Red Theme */
.rejected-section {
  background-color: #fdf2f2;
  border: 2px solid #dc3545;
}

.rejected-section h3 {
  color: #dc3545;
}

.reviewer-info-section h3,
.rejection-info-section h3 {
  margin: 0 0 20px 0;
  font-size: 1.3em;
  text-align: center;
  text-decoration: underline;
  border-bottom: 2px solid #e9ecef;
  padding-bottom: 10px;
}

.test-review-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.test-review-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  align-items: start;
}

.test-review-row:last-child {
  grid-template-columns: 1fr 1fr 1fr;
}

.test-review-field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.test-review-field.comments-field {
  grid-row: span 2;
}

.test-review-field label {
  font-weight: bold;
  color: #495057;
  font-size: 0.9em;
}

.test-review-value {
  padding: 12px 15px;
  background-color: white;
  border: 1px solid #ced4da;
  border-radius: 4px;
  color: #333;
  min-height: 20px;
  font-size: 0.9em;
}

.test-review-value.comments-value {
  min-height: 60px;
  word-wrap: break-word;
  white-space: pre-wrap;
}

/* Required field indicator */
.required-field {
  color: #dc3545;
  font-weight: bold;
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
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.btn-verify {
  background-color: #007bff;
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
  background-color: #0056b3;
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

/* Responsive design for signature inputs */
@media (max-width: 768px) {
  .signature-inputs {
    gap: 10px;
  }

  .signature-image-container {
    flex-direction: column;
    align-items: flex-start;
  }

  .signature-image {
    max-width: 120px;
    max-height: 60px;
  }
}

/* Signature display in footer */
.signature-display-footer {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
  margin-top: 5px;
}

.signature-image-footer {
  max-width: 120px;
  max-height: 60px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
  padding: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.signature-label {
  font-size: 12px;
  color: #666;
  font-style: italic;
  font-weight: 500;
}

/* Signature display for PDF format */
.signature-display-pdf {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  margin-top: 5px;
  padding: 10px;
  border: 1px solid #d0d0d0;
  background-color: #f5f5f5;
}

.signature-image-pdf {
  max-width: 150px;
  max-height: 60px;
  object-fit: contain;
}

.signature-line {
  font-size: 12px;
  font-weight: bold;
  color: #000;
  text-transform: uppercase;
  letter-spacing: 1px;
  border-top: 1px solid #000;
  padding-top: 5px;
  width: 100%;
  text-align: center;
}

.no-signature {
  color: #666;
  font-style: italic;
}

/* Responsive design for footer signature */
@media (max-width: 768px) {
  .signature-image-footer {
    max-width: 100px;
    max-height: 50px;
  }

  .signature-label {
    font-size: 11px;
  }
}
</style>
