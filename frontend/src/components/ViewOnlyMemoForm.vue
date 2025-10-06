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
      <div class="view-only-badge">VIEW ONLY</div>
      <div class="logos-container">
        <img
          src="@/assets/images/aviatrax-logo.png"
          alt="Aviatrax Logo"
          class="logo"
        />
        <img
          src="@/assets/images/vista_logo.png"
          alt="Vista Logo"
          class="logo vista-logo"
        />
      </div>
    </div>

    <!-- Requisition Details Section -->
    <div class="form-section requisition-details">
      <table class="form-table">
        <tr>
          <td class="form-cell">
            <label>From :</label>
            <input
              type="text"
              v-model="formData.from1"
              readonly
              class="readonly-field"
            />
          </td>
          <td class="form-cell">
            <label>CASDIC Ref No.:</label>
          </td>
          <td class="form-cell">
            <label>CASDIC/</label>
            <input
              type="text"
              v-model="formData.casdic"
              readonly
              class="readonly-field"
            />
          </td>
          <td class="form-cell">
            <label>Dated:</label>
            <input
              type="text"
              v-model="formData.casdicDate"
              readonly
              class="readonly-field"
            />
          </td>
        </tr>
        <tr>
          <td class="form-cell">
            <label>To :</label>
            <input
              type="text"
              v-model="formData.from2"
              readonly
              class="readonly-field"
            />
            <input
              type="text"
              v-model="formData.from3"
              readonly
              class="readonly-field"
            />
          </td>
          <td class="form-cell">
            <label>Thru/: O I/c, WH</label>
          </td>
          <td class="form-cell">
            <label>Wing/Proj Ref No.:</label>
            <input
              type="text"
              v-model="formData.wingRef"
              readonly
              class="readonly-field"
            />
          </td>
          <td class="form-cell"></td>
        </tr>
        <tr>
          <td class="form-cell"></td>
          <td class="form-cell">
            <label>Name & contact No of CASDIC (Designs) coordinator:</label>
            <input
              type="text"
              v-model="formData.coordinator"
              readonly
              class="readonly-field"
            />
          </td>
          <td class="form-cell"></td>
          <td class="form-cell"></td>
        </tr>
      </table>
    </div>

    <!-- LRU/SRU Table Section -->
    <div class="form-section lru-table">
      <table class="lru-grid">
        <thead>
          <tr>
            <th class="lru-header" rowspan="2">LRU/SRU DETAILS</th>
            <th class="lru-header" rowspan="2">LRU/SRU Desc</th>
            <th class="ref-header" colspan="4">Ref. Docnt</th>
          </tr>
          <tr>
            <th class="ref-header">Ref Doc</th>
            <th class="ref-header">Ref No of Document</th>
            <th class="ver-header">ver</th>
            <th class="rev-header">rev</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="lru-cell">
              <div class="lru-field">
                <label>Part No:</label>
                <input
                  type="text"
                  v-model="formData.partNo"
                  readonly
                  class="readonly-field"
                />
              </div>
              <div class="lru-field">
                <label>Manufacturer:</label>
                <input
                  type="text"
                  v-model="formData.manufacturer"
                  readonly
                  class="readonly-field"
                />
              </div>
            </td>
            <td class="desc-cell">
              <input
                type="text"
                v-model="formData.description"
                readonly
                class="readonly-field lru-description-input"
              />
            </td>
            <td class="ref-cell">
              <input
                type="text"
                v-model="formData.refDoc"
                readonly
                class="readonly-field"
              />
            </td>
            <td class="refno-cell">
              <input
                type="text"
                v-model="formData.refNo"
                readonly
                class="readonly-field"
              />
            </td>
            <td class="ver-cell">
              <input
                type="text"
                v-model="formData.version"
                readonly
                class="readonly-field"
              />
            </td>
            <td class="rev-cell">
              <input
                type="text"
                v-model="formData.revision"
                readonly
                class="readonly-field"
              />
            </td>
          </tr>

          <!-- Additional reference rows -->
          <tr v-for="i in 5" :key="i">
            <td class="lru-cell"></td>
            <td class="desc-cell">
              <input
                type="text"
                v-model="formData[`description${i + 1}`]"
                readonly
                class="readonly-field"
              />
            </td>
            <td class="ref-cell">
              <input
                type="text"
                v-model="formData[`refDoc${i + 1}`]"
                readonly
                class="readonly-field"
              />
            </td>
            <td class="refno-cell">
              <input
                type="text"
                v-model="formData[`refNo${i + 1}`]"
                readonly
                class="readonly-field"
              />
            </td>
            <td class="ver-cell">
              <input
                type="text"
                v-model="formData[`version${i + 1}`]"
                readonly
                class="readonly-field"
              />
            </td>
            <td class="rev-cell">
              <input
                type="text"
                v-model="formData[`revision${i + 1}`]"
                readonly
                class="readonly-field"
              />
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Additional Details Section -->
    <div class="form-section additional-details">
      <table class="form-table">
        <tr>
          <td class="form-cell">
            <label>Drawing no/Rev:</label>
            <input
              type="text"
              v-model="formData.drawingRev"
              readonly
              class="readonly-field"
            />
          </td>
          <td class="form-cell">
            <label>source:</label>
            <input
              type="text"
              v-model="formData.source"
              readonly
              class="readonly-field"
            />
          </td>
          <td class="form-cell">
            <label>Sl.No of units:</label>
            <input
              type="text"
              v-model="formData.serialNo"
              readonly
              class="readonly-field"
            />
          </td>
          <td class="form-cell">
            <label>Qty Offered:</label>
            <input
              type="text"
              v-model="formData.qtyOffered"
              readonly
              class="readonly-field"
            />
          </td>
        </tr>
        <tr>
          <td class="form-cell" colspan="2">
            <label>UNIT IDENTIFICATION:</label>
            <input
              type="text"
              v-model="formData.unitIdentification"
              readonly
              class="readonly-field"
            />
          </td>
          <td class="form-cell" colspan="2">
            <label>MECHANICAL INSPN:</label>
            <input
              type="text"
              v-model="formData.mechanicalInspection"
              readonly
              class="readonly-field"
            />
          </td>
        </tr>
        <tr>
          <td class="form-cell" colspan="2">
            <label>INSPECTION /TEST STAGE OFFERED NOW:</label>
            <input
              type="text"
              v-model="formData.testStageOffered"
              readonly
              class="readonly-field"
            />
          </td>
          <td class="form-cell">
            <label>Test stage cleared:</label>
            <input
              type="text"
              v-model="formData.testStageCleared"
              readonly
              class="readonly-field"
            />
          </td>
          <td class="form-cell">
            <label>STTE Status:</label>
            <input
              type="text"
              v-model="formData.stteStatus"
              readonly
              class="readonly-field"
            />
          </td>
        </tr>
      </table>
    </div>

    <!-- Testing Details Section -->
    <div class="form-section testing-details">
      <table class="form-table">
        <tr>
          <td class="form-cell" colspan="2">
            <label
              >Above Unit is ready for Testing at venue, dated onwards.</label
            >
            <input
              type="text"
              v-model="formData.venue"
              readonly
              class="readonly-field"
            />
          </td>
          <td class="form-cell">
            <label>memo date:</label>
            <input
              type="text"
              v-model="formData.memoDate"
              readonly
              class="readonly-field"
            />
          </td>
          <td class="form-cell">
            <label>Name / designation:</label>
            <input
              type="text"
              v-model="formData.nameDesignation"
              readonly
              class="readonly-field"
            />
          </td>
        </tr>
        <tr>
          <td class="form-cell">
            <label>Test facility to be used:</label>
            <input
              type="text"
              v-model="formData.testFacility"
              readonly
              class="readonly-field"
            />
          </td>
          <td class="form-cell">
            <label>Test cycle / Duration:</label>
            <input
              type="text"
              v-model="formData.testCycleDuration"
              readonly
              class="readonly-field"
            />
          </td>
          <td class="form-cell">
            <label>Test Start on:</label>
            <input
              type="text"
              v-model="formData.testStartOn"
              readonly
              class="readonly-field"
            />
          </td>
          <td class="form-cell">
            <label>Test complete on:</label>
            <input
              type="text"
              v-model="formData.testCompleteOn"
              readonly
              class="readonly-field"
            />
          </td>
        </tr>
        <tr>
          <td class="form-cell">
            <label>Calibration status OK/Due on:</label>
            <input
              type="text"
              v-model="formData.calibrationStatus"
              readonly
              class="readonly-field"
            />
          </td>
          <td class="form-cell">
            <label>Func. Check(Initial):</label>
            <input
              type="text"
              v-model="formData.funcCheckInitial"
              readonly
              class="readonly-field"
            />
          </td>
          <td class="form-cell">
            <label>Perf. check (during):</label>
            <input
              type="text"
              v-model="formData.perfCheckDuring"
              readonly
              class="readonly-field"
            />
          </td>
          <td class="form-cell">
            <label>Func Check (End):</label>
            <input
              type="text"
              v-model="formData.funcCheckEnd"
              readonly
              class="readonly-field"
            />
          </td>
        </tr>
      </table>
    </div>

    <!-- Certification Section -->
    <div class="form-section certification">
      <h3>It is certified that :</h3>
      <div class="checkbox-group">
        <label class="checkbox-item">
          <input
            type="checkbox"
            v-model="formData.certifications.mechanicalQualityRecords"
            disabled
          />
          <span>Mechanical Quality Records verified thoroughly</span>
        </label>
        <label class="checkbox-item">
          <input
            type="checkbox"
            v-model="formData.certifications.cocVerified"
            disabled
          />
          <span>CoC for SRU, fasteners & standard parts verified</span>
        </label>
        <label class="checkbox-item">
          <input
            type="checkbox"
            v-model="formData.certifications.sruSerialNoted"
            disabled
          />
          <span>Sl no of the SRUs noted in log book</span>
        </label>
        <label class="checkbox-item">
          <input
            type="checkbox"
            v-model="formData.certifications.noDefectInvestigation"
            disabled
          />
          <span>No Defect investigation pending</span>
        </label>
        <label class="checkbox-item">
          <input
            type="checkbox"
            v-model="formData.certifications.previousTestStagesCleared"
            disabled
          />
          <span>All previous test stages cleared</span>
        </label>
        <label class="checkbox-item">
          <input
            type="checkbox"
            v-model="formData.certifications.cascicQAInspected"
            disabled
          />
          <span>CASCIC QA has physically inspected and accepted</span>
        </label>
      </div>
    </div>

    <!-- Remarks Section -->
    <div class="form-section remarks">
      <label>Remarks:</label>
      <textarea
        v-model="formData.remarks"
        readonly
        class="readonly-field remarks-textarea"
      ></textarea>
    </div>

    <!-- QA Head Action Buttons (only show if memo is not processed) -->
    <div
      class="form-section action-buttons"
      v-if="isQAHead && !isMemoProcessed"
    >
      <div class="button-container">
        <button class="btn btn-accept" @click="handleAccept">ACCEPT</button>
        <button class="btn btn-reject" @click="handleReject">REJECT</button>
      </div>
    </div>

    <!-- Assigned Reviewer Information (show for all roles when memo is approved) -->
    <div
      class="form-section reviewer-info-section approved-section"
      v-if="isMemoApprovedWithReviewer"
    >
      <div class="status-badge approved-badge">
        ✓ APPROVED AND ASSIGNED REVIEWER
      </div>
      <h3>Test or Review Details</h3>
      <div class="test-review-grid">
        <div class="test-review-row">
          <div class="test-review-field">
            <label>Date of Test or Review :</label>
            <span class="test-review-value">{{
              formatApprovalDate(
                memoApprovalStatus.test_date || memoApprovalStatus.approval_date
              )
            }}</span>
          </div>
          <div class="test-review-field comments-field">
            <label>Comments :</label>
            <span class="test-review-value comments-value">{{
              memoApprovalStatus.comments || "No comments provided"
            }}</span>
          </div>
        </div>
        <div class="test-review-row">
          <div class="test-review-field">
            <label>Internal Tester ID:</label>
            <span class="test-review-value">{{ assignedReviewer.id }}</span>
          </div>
        </div>
        <div class="test-review-row">
          <div class="test-review-field">
            <label>Internal Tester Name :</label>
            <span class="test-review-value">{{ assignedReviewer.name }}</span>
          </div>
          <div class="test-review-field">
            <label>Authentication</label>
            <span class="test-review-value">{{
              memoApprovalStatus.authentication || "Not provided"
            }}</span>
          </div>
          <div class="test-review-field">
            <label>Attachments</label>
            <span class="test-review-value">{{
              memoApprovalStatus.attachment_path
                ? "File attached"
                : "No attachments"
            }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Rejection Information (show for all roles when memo is rejected) -->
    <div
      class="form-section rejection-info-section rejected-section"
      v-if="isMemoRejected"
    >
      <div class="status-badge rejected-badge">✗ REJECTED</div>
      <h3>Test or Review Details</h3>
      <div class="test-review-grid">
        <div class="test-review-row">
          <div class="test-review-field">
            <label>Date of Test or Review :</label>
            <span class="test-review-value">{{
              formatApprovalDate(memoApprovalStatus.approval_date)
            }}</span>
          </div>
          <div class="test-review-field comments-field">
            <label>Comments :</label>
            <span class="test-review-value comments-value">{{
              memoApprovalStatus.comments || "No comments provided"
            }}</span>
          </div>
        </div>
        <div class="test-review-row">
          <div class="test-review-field">
            <label>Internal Tester ID:</label>
            <span class="test-review-value">{{
              memoApprovalStatus.approved_by
            }}</span>
          </div>
        </div>
        <div class="test-review-row">
          <div class="test-review-field">
            <label>Internal Tester Name :</label>
            <span class="test-review-value">QA Head</span>
          </div>
          <div class="test-review-field">
            <label>Authentication</label>
            <span class="test-review-value">{{
              memoApprovalStatus.authentication || "Not provided"
            }}</span>
          </div>
          <div class="test-review-field">
            <label>Attachments</label>
            <span class="test-review-value">{{
              memoApprovalStatus.attachment_path
                ? "File attached"
                : "No attachments"
            }}</span>
          </div>
        </div>
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
          <label>Authentication:</label>
          <input
            type="text"
            v-model="approvalForm.authentication"
            placeholder="Enter authentication details..."
            required
          />
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
          <label>Authentication:</label>
          <input
            type="text"
            v-model="rejectionForm.authentication"
            placeholder="Enter authentication details..."
            required
          />
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
      },
      rejectionForm: {
        memo_id: null,
        comments: "",
        authentication: "",
        attachment: null,
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
        const response = await fetch(`/api/memos/${this.id}`);
        if (!response.ok) {
          throw new Error(
            `Failed to fetch memo details: ${response.statusText}`
          );
        }

        const data = await response.json();
        if (data.success) {
          this.transformAndSetMemoData(data.memo, data.references || []);
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
        unitIdentification: this.formatUnitIdentification(
          backendMemo.unit_identification
        ),
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

    formatUnitIdentification(unitIdArray) {
      if (!unitIdArray || !Array.isArray(unitIdArray)) return "";
      return unitIdArray.join(", ");
    },

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
          "http://localhost:5000/api/available-reviewers"
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
          `http://localhost:5000/api/memos/${this.id}/approval-status`
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
          `http://localhost:5000/api/users/${userId}`
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
      if (!this.approvalForm.authentication.trim()) {
        alert("Please enter authentication details");
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
          `http://localhost:5000/api/memos/${this.approvalForm.memo_id}/approve`,
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
          `http://localhost:5000/api/memos/${this.rejectionForm.memo_id}/approve`,
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
      if (!this.rejectionForm.authentication.trim()) {
        alert("Please enter authentication details");
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
  },
};
</script>

<style scoped>
.memo-form {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
  background: white;
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

.view-only-badge {
  background: #28a745;
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 0.9em;
  font-weight: bold;
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
</style>
