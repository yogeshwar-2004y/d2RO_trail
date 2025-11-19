<template>
  <div class="inspection-memo-container">
    <header class="app-header"></header>
    <div class="logo-section">
      <div class="logo-left">
        <svg
          class="icon arrow-left"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          @click="goBack"
        >
          <path d="M19 12H5M12 19l-7-7 7-7" />
        </svg>
        <span class="logo-text">AVIATRAX</span>
        <span class="memo-id">Memo ID: {{ id }}</span>
      </div>
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
    <div class="form-content">
      <div class="form-card read-only-section">
        <div class="section-header">
          <h2 class="card-title">REQUISITION FOR DGAQA INSPECTION</h2>
        </div>
        <div class="grid-layout">
          <div class="grid-item">
            <span>FROM:</span
            ><input type="text" v-model="memoData.from" readonly />
          </div>
          <div class="grid-item">
            <span>CASCIC Ref No.:</span
            ><input type="text" v-model="memoData.cascicRefNo" readonly />
          </div>
          <div class="grid-item">
            <span>CASCIC/</span
            ><input type="text" v-model="memoData.cascic" readonly />
          </div>
          <div class="grid-item">
            <span>Dated:</span
            ><input type="text" v-model="memoData.dated" readonly />
          </div>
          <div class="grid-item">
            <span>TO:</span><input type="text" v-model="memoData.to" readonly />
          </div>
          <div class="grid-item">
            <span>Wing/Proj Ref No.:</span
            ><input type="text" v-model="memoData.wingProjRefNo" readonly />
          </div>
          <div class="grid-item-full">
            <span>Name & contact No of CASCIC (Designs) coordinator:</span
            ><input
              type="text"
              v-model="memoData.coordinatorContact"
              readonly
            />
          </div>
        </div>
      </div>
      <div class="form-card read-only-section">
        <div class="section-header">
          <h3 class="section-title">LRU/SRU DETAILS</h3>
        </div>
        <div class="grid-layout two-col">
          <div class="grid-item-half">
            <span>LRU/SRU DETAILS</span
            ><input type="text" v-model="memoData.lruSruDetails" readonly />
          </div>
          <div class="grid-item-half">
            <span>LRU/SRU Desc:</span
            ><input type="text" v-model="memoData.lruSruDesc" readonly />
          </div>
        </div>
        <div class="grid-layout two-col-doc">
          <div class="grid-item">
            <span>Ref Doc</span
            ><input type="text" v-model="memoData.refDoc" readonly />
          </div>
          <div class="grid-item">
            <span>Ref No of Document</span
            ><input type="text" v-model="memoData.refNoDocument" readonly />
          </div>
          <div class="grid-item">
            <span>ver</span
            ><input type="text" v-model="memoData.version" readonly />
          </div>
          <div class="grid-item">
            <span>rev</span
            ><input type="text" v-model="memoData.revision" readonly />
          </div>
        </div>
        <div class="grid-layout">
          <div class="grid-item">
            <span>Part No:</span
            ><input type="text" v-model="memoData.partNo" readonly />
          </div>
          <div class="grid-item">
            <span>Manufacturer:</span
            ><input type="text" v-model="memoData.manufacturer" readonly />
          </div>
          <div class="grid-item">
            <span>Sl.No of units:</span
            ><input type="text" v-model="memoData.serialNo" readonly />
          </div>
          <div class="grid-item">
            <span>Drawing no/Rev:</span
            ><input type="text" v-model="memoData.drawingNoRev" readonly />
          </div>
          <div class="grid-item">
            <span>Qty Offered:</span
            ><input type="text" v-model="memoData.qtyOffered" readonly />
          </div>
          <div class="grid-item">
            <span>source:</span
            ><input type="text" v-model="memoData.source" readonly />
          </div>
        </div>
        <div class="grid-layout two-col">
          <div class="grid-item-half">
            <span>UNIT IDENTIFICATION:</span
            ><input
              type="text"
              v-model="memoData.unitIdentification"
              readonly
            />
          </div>
          <div class="grid-item-half">
            <span>MECHANICAL INSPN:</span
            ><input
              type="text"
              v-model="memoData.mechanicalInspection"
              readonly
            />
          </div>
        </div>
        <div class="grid-layout two-col">
          <div class="grid-item-half">
            <span>INSPECTION /TEST STAGE OFFERED NOW:</span
            ><input
              type="text"
              v-model="memoData.inspectionTestStage"
              readonly
            />
          </div>
          <div class="grid-item-half">
            <span>STTE Status:</span
            ><input type="text" v-model="memoData.stteStatus" readonly />
          </div>
        </div>
      </div>
      <div class="form-card read-only-section">
        <div class="section-header">
          <h3 class="section-title">TESTING DETAILS</h3>
        </div>
        <div class="grid-layout">
          <div class="grid-item-half">
            <span>Above Unit is ready for Testing at venue, dated onwards.</span
            ><input type="text" v-model="memoData.testingVenueDate" readonly />
          </div>
          <div class="grid-item-half">
            <span>Test facility to be used:</span
            ><input type="text" v-model="memoData.testFacility" readonly />
          </div>
          <div class="grid-item-half">
            <span>Calibration status OK/Due on:</span
            ><input type="text" v-model="memoData.calibrationStatus" readonly />
          </div>
          <div class="grid-item-half">
            <span>SIGNATURE: NAME / DESIGNATION</span
            ><input
              type="text"
              v-model="memoData.signatureNameDesignation"
              readonly
            />
          </div>
          <div class="grid-item-quarter">
            <span>Test cycle / Duration:</span
            ><input
              type="text"
              v-model="memoData.testCycleDuration"
              readonly
            /><span>hrs</span>
          </div>
          <div class="grid-item-quarter">
            <span>Func. Check(Initial):</span
            ><input
              type="text"
              v-model="memoData.funcCheckInitial"
              readonly
            /><span>date/time</span>
          </div>
          <div class="grid-item-quarter">
            <span>Test Start on:</span
            ><input type="text" v-model="memoData.testStartOn" readonly /><span
              >date/time</span
            >
          </div>
          <div class="grid-item-quarter">
            <span>Perf. check (during):</span
            ><input
              type="text"
              v-model="memoData.perfCheckDuring"
              readonly
            /><span>date/time</span>
          </div>
          <div class="grid-item-half">
            <span>Test complete on:</span
            ><input
              type="text"
              v-model="memoData.testCompleteOn"
              readonly
            /><span>date/time</span>
          </div>
          <div class="grid-item-half">
            <span>Func Check (End):</span
            ><input type="text" v-model="memoData.funcCheckEnd" readonly /><span
              >date/time</span
            >
          </div>
        </div>
      </div>
      <div class="form-card read-only-section">
        <div class="section-header">
          <h3 class="section-title">CERTIFICATIONS</h3>
        </div>
        <div class="grid-layout one-col-checkbox">
          <p class="checkbox-title">It is certified that :</p>
          <label
            ><input
              type="checkbox"
              v-model="memoData.certifications.mechanicalQualityRecords"
            />Mechanical Quality Records of all the parts (Raw material TC
            (chemical & mechanical), Dimensional reports, NDT reports, Process
            certificates etc.) & Electrical Quality Records (Components
            Screening report, PCB manufacturing report, process compliance
            reports/ test reports, etc.) were verified thoroughly.</label
          >
          <label
            ><input
              type="checkbox"
              v-model="memoData.certifications.cocVerified"
            />CoC for SRU, fasteners & standard parts are verified and
            satisfactory</label
          >
          <label
            ><input
              type="checkbox"
              v-model="memoData.certifications.sruSerialNoted"
            />Sl no of the SRUs are noted down in the respective log book opened
            on _________</label
          >
          <label
            ><input
              type="checkbox"
              v-model="memoData.certifications.noDefectInvestigation"
            />No Defect investigation is pending against this LRU</label
          >
          <label
            ><input
              type="checkbox"
              v-model="memoData.certifications.previousTestStagesCleared"
            />All the previous test stages of this LRU/SRU are cleared</label
          >
          <label
            ><input
              type="checkbox"
              v-model="memoData.certifications.cascicQAInspected"
            />CASCIC QA has physically inspected and accepted the LRU on
            _________</label
          >
          <span class="signature-line">SIGNATURE of Rep, IQA CASCIC</span>
        </div>
      </div>
      <div class="form-card page-break-before">
        <div class="section-header">
          <h3 class="section-title">Action taken & remarks by DGAQA</h3>
        </div>
        <div class="grid-layout">
          <div class="grid-item-full">
            <div class="dgaqa-remarks-text">{{ memoData.dgaqaRemarks }}</div>
            <span class="signature-line right">SIGNATURE OF DGAQA REP..</span>
          </div>
        </div>
      </div>
      <div
        class="form-card editable-section exclude-from-pdf"
        v-if="isQAReviewer"
      >
        <div class="section-header">
          <h3 class="section-title">TEST STATUS</h3>
        </div>
        <div class="grid-layout one-col-radio">
          <label>
            <input
              type="radio"
              value="Successfully completed"
              v-model="memoData.testStatus"
            />
            Successfully completed
          </label>
          <label>
            <input
              type="radio"
              value="Completed with observations"
              v-model="memoData.testStatus"
            />
            Completed with observations
          </label>
          <label>
            <input
              type="radio"
              value="Test not conducted"
              v-model="memoData.testStatus"
            />
            Test not conducted
          </label>
          <label>
            <input
              type="radio"
              value="Test failed"
              v-model="memoData.testStatus"
            />
            Test failed
          </label>
        </div>
      </div>
      <div class="form-card editable-section" v-if="isQAReviewer">
        <div class="section-header">
          <h3 class="section-title">Remarks by QA Reviewer</h3>
          <h3 class="signature-section-label">QA Reviewer Signature</h3>
        </div>
        <div class="grid-layout two-col-signature">
          <div class="grid-item-half">
            <textarea
              v-model="memoData.reviewerComments"
              class="reviewer-comments"
              placeholder="Enter reviewer comments..."
              rows="8"
              :disabled="!isQAReviewer"
            ></textarea>
          </div>
          <!-- QA Reviewer Signature -->
          <div class="grid-item-half signature-item" v-if="isQAReviewer">
            <div class="signature-auth-container">
              <div
                v-if="!canAccessSignatures"
                class="signature-disabled-message"
              >
                Signature authentication is only available for QA Reviewer.
              </div>
              <div
                v-else-if="!signatures.qaReviewer.signatureUrl"
                class="signature-inputs"
              >
                <div class="input-group">
                  <label>Username:</label>
                  <input
                    type="text"
                    v-model="signatures.qaReviewer.signatureUsername"
                    placeholder="Enter username..."
                    :disabled="!isQAReviewerSignatureEnabled || isSubmitted"
                  />
                </div>
                <div class="input-group">
                  <label>Signature Password:</label>
                  <input
                    type="password"
                    v-model="signatures.qaReviewer.signaturePassword"
                    placeholder="Enter signature password..."
                    :disabled="!isQAReviewerSignatureEnabled || isSubmitted"
                  />
                </div>
                <button
                  type="button"
                  class="btn btn-verify"
                  @click="
                    verifySignature('qaReviewer');
                    $event.target.blur();
                  "
                  :disabled="
                    !isQAReviewerSignatureEnabled ||
                    isSubmitted ||
                    !signatures.qaReviewer.signatureUsername ||
                    !signatures.qaReviewer.signaturePassword
                  "
                >
                  Verify & Load Signature
                </button>
              </div>
              <div
                v-if="signatures.qaReviewer.signatureUrl"
                class="signature-display"
              >
                <label>Verified Signature:</label>
                <div class="signature-image-container">
                  <img
                    :src="signatures.qaReviewer.signatureUrl"
                    alt="Verified Signature"
                    class="signature-image"
                  />
                  <div
                    class="signature-info"
                    v-if="
                      signatures.qaReviewer.verifiedUserName ||
                      signatures.qaReviewer.verifiedUserRole
                    "
                  >
                    <span
                      class="signature-user"
                      v-if="signatures.qaReviewer.verifiedUserName"
                      >{{ signatures.qaReviewer.verifiedUserName }}</span
                    >
                    <span
                      class="signature-role"
                      v-if="signatures.qaReviewer.verifiedUserRole"
                      >{{
                        signatures.qaReviewer.verifiedUserRole
                      }}
                      Signature</span
                    >
                    <span class="signature-status">✓ Verified</span>
                  </div>
                  <div class="signature-info" v-else>
                    <span class="signature-status">✓ Signature Verified</span>
                  </div>
                </div>
              </div>
              <div
                v-if="signatures.qaReviewer.signatureError"
                class="signature-error"
              >
                {{ signatures.qaReviewer.signatureError }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- 
<div v-if="showShareModal" class="share-modal-overlay" @click.self="toggleShareModal">
      <div class="share-modal-content">
        <h2>Share via Email</h2>
        <p>Enter email addresses separated by commas.</p>
        <input type="text" v-model="emailAddresses" placeholder="e.g., mail1@example.com, mail2@example.com" class="email-input" />
        <div class="modal-actions">
          <button @click="sendEmails" class="send-btn">Send</button>
        </div>
      </div>
    </div>    
-->

    <!-- Submit Button - Only visible for QA Reviewer -->
    <div class="submit-section" v-if="!isSubmitted && isQAReviewer">
      <button class="submit-button" @click="submitMemo">Submit</button>
    </div>
  </div>
</template>

<script>
import { userStore } from "@/stores/userStore";

export default {
  name: "InspectionMemo",
  props: {
    id: {
      type: [String, Number],
      required: true,
    },
  },
  data() {
    return {
      showShareModal: false,
      emailAddresses: "",
      isSubmitted: false,
      signatures: {
        qaReviewer: {
          signatureUsername: "",
          signaturePassword: "",
          signatureUrl: "",
          verifiedUserName: "",
          verifiedUserRole: "",
          signatureError: "",
        },
      },
      memoData: {
        dgaqaRemarks: "All records verified. Proceed as per plan.",
        from: "CASCIC Design Team",
        cascicRefNo: "CASCIC/2025/001",
        cascic: "CASCIC/DES/2025",
        dated: "15-01-2025",
        to: "DGAQA Inspection Team",
        wingProjRefNo: "WING/PROJ/2025/001",
        coordinatorContact: "Sumith",
        lruSruDetails: "LRU-001",
        lruSruDesc: "Flight Control Unit",
        refDoc: "FCU-SPEC-001",
        refNoDocument: "DOC/FCU/2025/001",
        version: "1.0",
        revision: "A",
        partNo: "FCU-001-REV-A",
        manufacturer: "Aviation Systems Ltd.",
        serialNo: "SN001234567",
        drawingNoRev: "DRW/FCU/001-REV-A",
        qtyOffered: "2",
        source: "Manufacturer",
        unitIdentification: "FCU-001-REV-A-SN001234567",
        mechanicalInspection: "PASSED",
        inspectionTestStage: "Final Assembly Test",
        stteStatus: "READY",
        testingVenueDate: "20-01-2025",
        testFacility: "Test Lab A",
        calibrationStatus: "OK",
        signatureNameDesignation: "Design Engineer",
        testCycleDuration: "24",
        funcCheckInitial: "20-01-2025 09:00",
        testStartOn: "20-01-2025 10:00",
        perfCheckDuring: "20-01-2025 14:00",
        testCompleteOn: "21-01-2025 10:00",
        funcCheckEnd: "21-01-2025 11:00",
        certifications: {
          mechanicalQualityRecords: true,
          cocVerified: true,
          sruSerialNoted: true,
          noDefectInvestigation: true,
          previousTestStagesCleared: true,
          cascicQAInspected: true,
        },
        reviewerComments: "",
        testStatus: "",
      },
    };
  },
  computed: {
    canAccessSignatures() {
      const currentUserRole = userStore.getters.currentUserRole();
      return currentUserRole === 3; // Only QA Reviewer (3)
    },
    isQAReviewerSignatureEnabled() {
      return this.canAccessSignatures;
    },
    isQAReviewer() {
      const currentUserRole = userStore.getters.currentUserRole();
      return currentUserRole === 3; // Only QA Reviewer (3)
    },
  },
  mounted() {
    this.fetchMemoData();
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    async fetchMemoData() {
      try {
        // Check if data was passed via sessionStorage (from dashboard navigation)
        if (this.$route.query.hasData === "true") {
          const storedMemoData = sessionStorage.getItem(`memoData_${this.id}`);
          const storedReferences = sessionStorage.getItem(
            `references_${this.id}`
          );

          if (storedMemoData && storedReferences) {
            const memoData = JSON.parse(storedMemoData);
            const references = JSON.parse(storedReferences);
            this.transformAndSetMemoData(memoData, references);

            // Clean up sessionStorage after use
            sessionStorage.removeItem(`memoData_${this.id}`);
            sessionStorage.removeItem(`references_${this.id}`);
            return;
          }
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
      // Check if memo is already submitted (has a test status set)
      const submittedStatuses = [
        "successfully_completed",
        "test_not_conducted",
        "completed_with_observations",
        "test_failed",
      ];
      this.isSubmitted =
        backendMemo.memo_status &&
        submittedStatuses.includes(backendMemo.memo_status);

      // Transform backend memo data to frontend format
      this.memoData = {
        // Basic memo information
        dgaqaRemarks: backendMemo.remarks || "No remarks provided",
        from: backendMemo.from_person || "CASCIC Design Team",
        cascicRefNo: backendMemo.casdic_ref_no || "",
        cascic: backendMemo.casdic_ref_no || "",
        dated: this.formatDate(backendMemo.dated),
        to: backendMemo.to_person || "DGAQA Inspection Team",
        wingProjRefNo: backendMemo.wing_proj_ref_no || "",
        coordinatorContact: backendMemo.name_designation || "",

        // LRU/SRU Details
        lruSruDetails: backendMemo.part_number || "",
        lruSruDesc: backendMemo.lru_sru_desc || "",
        refDoc: references[0]?.ref_doc || "",
        refNoDocument: references[0]?.ref_no || "",
        version: references[0]?.ver?.toString() || "",
        revision: references[0]?.rev?.toString() || "",
        partNo: backendMemo.part_number || "",
        manufacturer: backendMemo.manufacturer || "",
        serialNo: this.formatSerialNumbers(backendMemo.slno_units),
        drawingNoRev: backendMemo.drawing_no_rev || "",
        qtyOffered: backendMemo.qty_offered?.toString() || "0",
        source: backendMemo.source || "",
        unitIdentification: this.formatUnitIdentification(
          backendMemo.unit_identification
        ),
        mechanicalInspection: backendMemo.mechanical_inspn || "",
        inspectionTestStage: backendMemo.inspn_test_stage_offered || "",
        stteStatus: backendMemo.stte_status || "",

        // Testing Details
        testingVenueDate: this.formatDate(backendMemo.memo_date),
        testFacility: backendMemo.test_facility || "",
        calibrationStatus: backendMemo.calibration_status || "",
        signatureNameDesignation: backendMemo.name_designation || "",
        testCycleDuration: backendMemo.test_cycle_duration || "",
        funcCheckInitial: this.formatDateTime(backendMemo.func_check_initial),
        testStartOn: this.formatDateTime(backendMemo.test_start_on),
        perfCheckDuring: this.formatDateTime(backendMemo.perf_check_during),
        testCompleteOn: this.formatDateTime(backendMemo.test_complete_on),
        funcCheckEnd: this.formatDateTime(backendMemo.func_check_end),

        // Certifications object with all required properties
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

        // Test Status - map from database memo_status to frontend format
        testStatus: this.mapMemoStatusToTestStatus(
          backendMemo.memo_status || ""
        ),

        // Reviewer comments - fetch from database qa_remarks
        reviewerComments: backendMemo.qa_remarks || "",
      };

      // Load signature if it exists
      if (backendMemo.qa_signature) {
        this.signatures.qaReviewer.signatureUrl = backendMemo.qa_signature;
        // Try to extract user info from signature URL or fetch it
        // For now, we'll just set the URL and let the user see the signature
        // You might want to store user name and role separately in the database
      }
    },

    mapMemoStatusToTestStatus(memoStatus) {
      // Map database memo_status to frontend test status format
      const statusMapping = {
        successfully_completed: "Successfully completed",
        test_not_conducted: "Test not conducted",
        completed_with_observations: "Completed with observations",
        test_failed: "Test failed",
      };
      return statusMapping[memoStatus] || "";
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

    /** toggleShareModal() {
      this.showShareModal = !this.showShareModal;
      if (!this.showShareModal) {
        this.emailAddresses = ''; // Clear input on close
      }
    },
    sendEmails() {
      if (this.emailAddresses.trim() === '') {
        alert('Please enter at least one email address.');
        return;
      }
      
      const emails = this.emailAddresses.split(',').map(email => email.trim());
      console.log('Sending memo to:', emails);
      // Here you would add the logic to send the emails, for example, making an API call.
      
      alert(`Memo sent successfully to: ${emails.join(', ')}`);
      this.toggleShareModal(); // Close the modal after "sending"
    },*/
    async submitMemo() {
      // Validate that a test status is selected
      if (!this.memoData.testStatus) {
        alert("Please select a test status.");
        return;
      }

      if (!this.memoData.reviewerComments.trim()) {
        alert("Please provide reviewer comments.");
        return;
      }

      // Validate that signature is verified (only if not already submitted)
      if (!this.isSubmitted && !this.signatures.qaReviewer.signatureUrl) {
        alert("Please verify and load your signature before submitting.");
        return;
      }

      try {
        // Prepare certification data for backend
        const certified = [];
        if (this.memoData.certifications.mechanicalQualityRecords)
          certified.push("a");
        if (this.memoData.certifications.cocVerified) certified.push("b");
        if (this.memoData.certifications.sruSerialNoted) certified.push("c");
        if (this.memoData.certifications.noDefectInvestigation)
          certified.push("d");
        if (this.memoData.certifications.previousTestStagesCleared)
          certified.push("e");
        if (this.memoData.certifications.cascicQAInspected) certified.push("f");

        // Update memo status via API
        const response = await fetch(`/api/memos/${this.id}/status`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            test_status: this.memoData.testStatus,
            reviewer_comments: this.memoData.reviewerComments,
            certified: certified,
            qa_signature: this.signatures.qaReviewer.signatureUrl,
          }),
        });

        if (!response.ok) {
          throw new Error(
            `Failed to update memo status: ${response.statusText}`
          );
        }

        const result = await response.json();
        if (result.success) {
          this.isSubmitted = true; // Hide submit button after successful submission
          alert("Memo status updated successfully!");
          this.goBack(); // Navigate back after successful submission
        } else {
          throw new Error(result.message || "Failed to update memo status");
        }
      } catch (error) {
        console.error("Error updating memo status:", error);
        alert(`Error updating memo status: ${error.message}`);
      }
    },

    // Download memo PDF - Generate clean structured PDF from data
    async downloadMemoPDF() {
      try {
        // Dynamically import jsPDF
        const { jsPDF } = await import("jspdf");

        console.log(`Generating PDF for memo ID: ${this.id}`);

        // Create PDF document
        const doc = new jsPDF("p", "mm", "a4");
        const pageWidth = doc.internal.pageSize.getWidth();
        const pageHeight = doc.internal.pageSize.getHeight();
        const margin = 15;
        const contentWidth = pageWidth - 2 * margin;
        let yPosition = margin;

        // Helper function to check page break and add new page if needed
        const checkPageBreak = (requiredHeight) => {
          if (yPosition + requiredHeight > pageHeight - margin) {
            doc.addPage();
            yPosition = margin;
            return true;
          }
          return false;
        };

        // Helper function to add text with wrapping
        const addWrappedText = (
          text,
          x,
          y,
          maxWidth,
          fontSize = 10,
          fontStyle = "normal"
        ) => {
          doc.setFontSize(fontSize);
          doc.setFont("helvetica", fontStyle);
          const lines = doc.splitTextToSize(text || "", maxWidth);
          doc.text(lines, x, y);
          return lines.length * (fontSize * 0.35); // Approximate line height
        };

        // Helper function to add section header
        const addSectionHeader = (title) => {
          checkPageBreak(15);
          yPosition += 5;
          doc.setFontSize(12);
          doc.setFont("helvetica", "bold");
          doc.text(title, margin, yPosition);
          yPosition += 2;
          // Draw line under header
          doc.setLineWidth(0.5);
          doc.line(margin, yPosition, pageWidth - margin, yPosition);
          yPosition += 8;
        };

        // Helper function to add field (label + value)
        const addField = (label, value, x, width) => {
          const fieldHeight = 8;
          checkPageBreak(fieldHeight);

          doc.setFontSize(9);
          doc.setFont("helvetica", "bold");
          doc.text(label + ":", x, yPosition);

          doc.setFont("helvetica", "normal");
          const valueText = value || "N/A";
          const valueLines = doc.splitTextToSize(valueText, width - 5);
          doc.text(valueLines, x, yPosition + 5);

          yPosition += valueLines.length * 4 + 3;
        };

        // ===== PAGE 1: HEADER AND REQUISITION DETAILS =====
        // Title
        doc.setFontSize(16);
        doc.setFont("helvetica", "bold");
        doc.text("REQUISITION FOR DGAQA INSPECTION", pageWidth / 2, yPosition, {
          align: "center",
        });
        yPosition += 10;

        // Memo ID
        doc.setFontSize(10);
        doc.setFont("helvetica", "normal");
        doc.text(`Memo ID: ${this.id}`, pageWidth - margin, yPosition, {
          align: "right",
        });
        yPosition += 8;

        // Requisition Details Section
        addSectionHeader("REQUISITION DETAILS");

        const leftColX = margin;
        const rightColX = margin + contentWidth / 2;
        const colWidth = contentWidth / 2 - 5;

        addField("FROM", this.memoData.from, leftColX, colWidth);
        addField(
          "CASCIC Ref No.",
          this.memoData.cascicRefNo,
          rightColX,
          colWidth
        );

        addField("CASCIC/", this.memoData.cascic, leftColX, colWidth);
        addField("Dated", this.memoData.dated, rightColX, colWidth);

        addField("TO", this.memoData.to, leftColX, colWidth);
        addField(
          "Wing/Proj Ref No.",
          this.memoData.wingProjRefNo,
          rightColX,
          colWidth
        );

        addField(
          "Name & contact No of CASCIC (Designs) coordinator",
          this.memoData.coordinatorContact,
          leftColX,
          contentWidth
        );

        // LRU/SRU Details Section
        addSectionHeader("LRU/SRU DETAILS");

        addField(
          "LRU/SRU DETAILS",
          this.memoData.lruSruDetails,
          leftColX,
          colWidth
        );
        addField("LRU/SRU Desc", this.memoData.lruSruDesc, rightColX, colWidth);

        addField("Ref Doc", this.memoData.refDoc, leftColX, colWidth);
        addField(
          "Ref No of Document",
          this.memoData.refNoDocument,
          rightColX,
          colWidth
        );

        addField("ver", this.memoData.version, leftColX, colWidth);
        addField("rev", this.memoData.revision, rightColX, colWidth);

        addField("Part No", this.memoData.partNo, leftColX, colWidth);
        addField(
          "Manufacturer",
          this.memoData.manufacturer,
          rightColX,
          colWidth
        );

        addField("Sl.No of units", this.memoData.serialNo, leftColX, colWidth);
        addField(
          "Drawing no/Rev",
          this.memoData.drawingNoRev,
          rightColX,
          colWidth
        );

        addField("Qty Offered", this.memoData.qtyOffered, leftColX, colWidth);
        addField("source", this.memoData.source, rightColX, colWidth);

        addField(
          "UNIT IDENTIFICATION",
          this.memoData.unitIdentification,
          leftColX,
          colWidth
        );
        addField(
          "MECHANICAL INSPN",
          this.memoData.mechanicalInspection,
          rightColX,
          colWidth
        );

        addField(
          "INSPECTION /TEST STAGE OFFERED NOW",
          this.memoData.inspectionTestStage,
          leftColX,
          colWidth
        );
        addField("STTE Status", this.memoData.stteStatus, rightColX, colWidth);

        // Testing Details Section
        addSectionHeader("TESTING DETAILS");

        addField(
          "Above Unit is ready for Testing at venue, dated onwards",
          this.memoData.testingVenueDate,
          leftColX,
          colWidth
        );
        addField(
          "Test facility to be used",
          this.memoData.testFacility,
          rightColX,
          colWidth
        );

        addField(
          "Calibration status OK/Due on",
          this.memoData.calibrationStatus,
          leftColX,
          colWidth
        );
        addField(
          "SIGNATURE: NAME / DESIGNATION",
          this.memoData.signatureNameDesignation,
          rightColX,
          colWidth
        );

        const quarterWidth = contentWidth / 4 - 3;
        addField(
          "Test cycle / Duration",
          this.memoData.testCycleDuration
            ? `${this.memoData.testCycleDuration} hrs`
            : "",
          leftColX,
          quarterWidth
        );
        addField(
          "Func. Check(Initial)",
          this.memoData.funcCheckInitial,
          leftColX + quarterWidth + 3,
          quarterWidth
        );
        addField(
          "Test Start on",
          this.memoData.testStartOn,
          leftColX + (quarterWidth + 3) * 2,
          quarterWidth
        );
        addField(
          "Perf. check (during)",
          this.memoData.perfCheckDuring,
          leftColX + (quarterWidth + 3) * 3,
          quarterWidth
        );

        addField(
          "Test complete on",
          this.memoData.testCompleteOn,
          leftColX,
          colWidth
        );
        addField(
          "Func Check (End)",
          this.memoData.funcCheckEnd,
          rightColX,
          colWidth
        );

        // Certifications Section
        addSectionHeader("CERTIFICATIONS");

        doc.setFontSize(9);
        doc.setFont("helvetica", "normal");
        doc.text("It is certified that :", margin, yPosition);
        yPosition += 6;

        const certifications = this.memoData.certifications || {};
        const certTexts = [
          {
            key: "mechanicalQualityRecords",
            text: "Mechanical Quality Records of all the parts (Raw material TC (chemical & mechanical), Dimensional reports, NDT reports, Process certificates etc.) & Electrical Quality Records (Components Screening report, PCB manufacturing report, process compliance reports/ test reports, etc.) were verified thoroughly.",
          },
          {
            key: "cocVerified",
            text: "CoC for SRU, fasteners & standard parts are verified and satisfactory",
          },
          {
            key: "sruSerialNoted",
            text: "Sl no of the SRUs are noted down in the respective log book opened on _________",
          },
          {
            key: "noDefectInvestigation",
            text: "No Defect investigation is pending against this LRU",
          },
          {
            key: "previousTestStagesCleared",
            text: "All the previous test stages of this LRU/SRU are cleared",
          },
          {
            key: "cascicQAInspected",
            text: "CASCIC QA has physically inspected and accepted the LRU on _________",
          },
        ];

        certTexts.forEach((cert) => {
          checkPageBreak(8);
          // Draw checkbox
          const checkboxSize = 3;
          const isChecked = certifications[cert.key];

          // Draw checkbox border
          doc.setLineWidth(0.5);
          doc.rect(
            margin + 2,
            yPosition - checkboxSize,
            checkboxSize,
            checkboxSize
          );

          // Draw checkmark if checked
          if (isChecked) {
            doc.setLineWidth(0.8);
            doc.line(
              margin + 2.5,
              yPosition - checkboxSize + 1.5,
              margin + 3.5,
              yPosition - checkboxSize + 2.5
            );
            doc.line(
              margin + 3.5,
              yPosition - checkboxSize + 2.5,
              margin + 4.5,
              yPosition - checkboxSize + 0.5
            );
          }

          // Add text next to checkbox
          const text = cert.text;
          const lines = doc.splitTextToSize(text, contentWidth - 15);
          doc.setFontSize(9);
          doc.setFont("helvetica", "normal");
          doc.text(lines, margin + 8, yPosition);
          yPosition += Math.max(lines.length * 4, 6) + 2;
        });

        checkPageBreak(8);
        doc.setFont("helvetica", "bold");
        doc.text("SIGNATURE of Rep, IQA CASCIC", margin, yPosition);
        yPosition += 15;

        // ===== ACTION TAKEN & REMARKS BY DGAQA =====
        checkPageBreak(30);
        addSectionHeader("ACTION TAKEN & REMARKS BY DGAQA");

        // Add remarks text with proper wrapping
        const remarksText = this.memoData.dgaqaRemarks || "No remarks provided";
        doc.setFontSize(10);
        doc.setFont("helvetica", "normal");
        const remarksLines = doc.splitTextToSize(remarksText, contentWidth);
        doc.text(remarksLines, margin, yPosition);
        yPosition += remarksLines.length * 5 + 15;

        // Signature line
        doc.setFont("helvetica", "bold");
        doc.text("SIGNATURE OF DGAQA REP..", pageWidth - margin, yPosition, {
          align: "right",
        });
        yPosition += 15;

        // ===== QA REVIEWER REMARKS (placed after DGAQA section) =====
        if (this.memoData.reviewerComments) {
          checkPageBreak(30);
          addSectionHeader("REMARKS BY QA REVIEWER");

          const reviewerComments = this.memoData.reviewerComments;
          doc.setFontSize(10);
          doc.setFont("helvetica", "normal");
          const commentLines = doc.splitTextToSize(
            reviewerComments,
            contentWidth
          );
          doc.text(commentLines, margin, yPosition);
          yPosition += commentLines.length * 5 + 15;

          // QA Reviewer Signature (if exists)
          if (this.signatures.qaReviewer.signatureUrl) {
            checkPageBreak(30);
            try {
              // Try to add signature image
              const img = new Image();
              img.crossOrigin = "anonymous";
              img.src = this.signatures.qaReviewer.signatureUrl;

              await new Promise((resolve, reject) => {
                img.onload = () => {
                  try {
                    const imgWidth = 50;
                    const imgHeight = (img.height / img.width) * imgWidth;
                    checkPageBreak(imgHeight + 10);
                    doc.addImage(
                      img,
                      "PNG",
                      pageWidth - margin - imgWidth,
                      yPosition,
                      imgWidth,
                      imgHeight
                    );
                    yPosition += imgHeight + 5;
                    doc.setFont("helvetica", "bold");
                    doc.text(
                      "SIGNATURE OF QA REVIEWER",
                      pageWidth - margin,
                      yPosition,
                      { align: "right" }
                    );
                    resolve();
                  } catch (err) {
                    reject(err);
                  }
                };
                img.onerror = reject;
              });
            } catch (err) {
              console.warn("Could not load signature image:", err);
              doc.setFont("helvetica", "bold");
              doc.text(
                "SIGNATURE OF QA REVIEWER",
                pageWidth - margin,
                yPosition,
                { align: "right" }
              );
            }
          } else {
            // Signature line even if no image
            doc.setFont("helvetica", "bold");
            doc.text(
              "SIGNATURE OF QA REVIEWER",
              pageWidth - margin,
              yPosition,
              { align: "right" }
            );
          }
        }

        // Save PDF
        const filename = `memo_${this.id}_${new Date()
          .toISOString()
          .slice(0, 10)}.pdf`;
        doc.save(filename);

        console.log(`PDF generated successfully for memo ${this.id}`);
      } catch (error) {
        console.error("Error generating memo PDF:", error);
        alert(`Error generating PDF: ${error.message}`);
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

.inspection-memo-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  font-family: sans-serif;
  color: var(--text-color);
  background-color: var(--background-color);
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: var(--card-color);
  border-bottom: 1px solid var(--border-color);
}

.logo-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 10px 20px;
}

.logo-left {
  display: flex;
  align-items: center;
}

.logo-section .icon {
  width: 24px;
  height: 24px;
  margin-right: 10px;
  cursor: pointer;
  transition: transform 0.2s;
}

.logo-section .icon:hover {
  transform: scale(1.1);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 15px;
}

.download-pdf-btn {
  display: flex;
  align-items: center;
  gap: 5px;
  margin-right: 25px;
  padding: 8px 13px;
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

.download-pdf-btn .icon {
  width: 16px;
  height: 16px;
}

.download-text {
  font-size: 14px;
  font-weight: 500;
}

.memo-id {
  margin-left: 20px;
  font-size: 0.9em;
  color: #666;
  font-weight: normal;
}

/* removed editable indicator */

.logo-text {
  font-weight: bold;
  font-size: 1.2em;
}

.share-section .share-btn {
  display: flex;
  align-items: center;
  background: none;
  border: none;
  color: var(--text-color);
  font-size: 1em;
  cursor: pointer;
}

.share-section .icon {
  width: 20px;
  height: 20px;
  margin-right: 5px;
}

.form-content {
  flex-grow: 1;
  overflow-y: auto;
  padding: 20px;
  box-sizing: border-box;
}

.form-card {
  background-color: var(--card-color);
  border: 1px solid var(--border-color);
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

.grid-layout.two-col-signature {
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  align-items: start;
  width: 100%;
  box-sizing: border-box;
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
  min-width: 0;
  box-sizing: border-box;
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
  color: var(--text-color);
  cursor: text;
}

.grid-item span,
.grid-item-full span,
.grid-item-half span,
.grid-item-quarter span {
  font-size: 0.9em;
}

.remarks-title {
  font-weight: bold;
  margin-bottom: 5px;
}

.dgaqa-remarks-text {
  padding: 15px 0;
  line-height: 1.8;
  font-size: 14px;
  color: #000;
  white-space: pre-wrap;
  word-wrap: break-word;
  overflow-wrap: break-word;
  margin-bottom: 30px;
  border: none;
  background: transparent;
  min-height: auto;
  max-width: 100%;
  display: block;
}

.signature-line {
  display: block;
  text-align: right;
  margin-top: 20px;
  margin-left: auto;
  font-weight: bold;
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

.one-col-radio label {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  font-size: 0.9em;
  line-height: 1.2;
  cursor: pointer;
}

.one-col-radio input[type="radio"] {
  margin-right: 10px;
  transform: scale(1.2);
  accent-color: #000;
}

.share-modal-overlay {
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

.share-modal-content {
  background-color: white;
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 90%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.share-modal-content h2 {
  margin: 0;
  font-size: 1.5em;
  text-align: center;
}

.share-modal-content p {
  margin: 0;
  font-size: 0.9em;
  color: #666;
}

.email-input {
  width: 100%;
  padding: 10px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  box-sizing: border-box;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
}

.send-btn {
  padding: 10px 20px;
  background-color: #000;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.reviewer-comments {
  width: 100%;
  max-width: 100%;
  padding: 12px;
  border: 1px solid #d0d0d0;
  border-radius: 0;
  background-color: #f5f5f5;
  font-size: 14px;
  font-family: inherit;
  resize: vertical;
  min-height: 250px;
  height: 250px;
  margin: 0;
  transition: none;
  color: var(--text-color);
  box-sizing: border-box;
}

.reviewer-comments:focus {
  outline: none;
  border-color: #b0b0b0;
  background-color: #f0f0f0;
  box-shadow: none;
}

.reviewer-comments::placeholder {
  color: #999;
}

.submit-section {
  display: flex;
  justify-content: flex-end;
  padding: 20px;
  background-color: transparent;
}

.submit-button {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px 30px;
  background-color: #000;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.submit-button:hover {
  background-color: #222;
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.submit-button:active {
  transform: translateY(0);
}

.submit-button svg {
  width: 20px;
  height: 20px;
}

.editable-section {
  border-left: none;
  background-color: #fff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  border: 1px solid var(--border-color);
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

/* remove edit badge + pulse */

.read-only-section {
  border-left: none;
  background-color: #fff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  border: 1px solid var(--border-color);
}

/* remove read-only badge */

.card-title {
  margin: 0;
  color: #000;
  font-size: 1.2em;
  font-weight: bold;
}

/* Signature Styles */
.signature-item {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 0;
  min-width: 0;
  width: 100%;
  box-sizing: border-box;
  min-height: 250px;
}

.signature-section-label {
  font-weight: bold;
  color: #333;
  font-size: 1rem;
  margin-bottom: 10px;
  padding-bottom: 5px;
  margin-right: 28.5rem;
}

.signature-auth-container {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 10px;
  background-color: #f8f9fa;
  margin-top: 0;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
  overflow: hidden;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.signature-inputs {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 15px;
  width: 100%;
  min-width: 0;
  box-sizing: border-box;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
  width: 100%;
  min-width: 0;
  box-sizing: border-box;
}

.input-group label {
  font-weight: 600;
  color: #333;
  font-size: 14px;
}

.input-group input {
  width: 100%;
  max-width: 100%;
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.3s ease;
  box-sizing: border-box;
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
  color: #155724;
  font-size: 12px;
  font-style: italic;
}

.signature-status {
  color: #28a745;
  font-weight: 600;
  font-size: 12px;
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
</style>
