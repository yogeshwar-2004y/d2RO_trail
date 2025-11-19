<template>
  <div class="view-observations-page">
    <!-- Header -->
    <div class="page-header">
      <div class="header-left">
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
      </div>
      <div class="header-center">
        <h1 class="page-title">IQA OBSERVATION REPORT</h1>
      </div>
      <div class="header-right">
        <button class="export-button" @click="exportReport">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="7,10 12,15 17,10"></polyline>
            <line x1="12" y1="15" x2="12" y2="3"></line>
          </svg>
          Download as PDF
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Report Header -->
      <div class="report-header">
        <div class="document-path">
          CASDIC/{{ projectName }}/{{ lruName }}/SL.{{ serialNumber }}/{{
            observationCount
          }}/{{ currentYear }}
        </div>
        <div class="report-date">Date: {{ currentDate }}</div>
      </div>

      <div class="subject-line">
        SUB : IQA Observation Report for {{ lruName }}
      </div>

      <!-- Read-Only Warning -->
      <div v-if="isReadOnly" class="read-only-warning">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
        </svg>
        <span
          >This report has been submitted and is read-only. You can view the
          data but cannot make changes.</span
        >
      </div>

      <!-- Document Details Grid -->
      <div class="document-details">
        <div class="details-left">
          <div class="detail-item">
            <label>Project Name :</label>
            <span class="readonly-value">{{
              projectName || "Not specified"
            }}</span>
          </div>
          <div class="detail-item">
            <label>LRU Name :</label>
            <span class="readonly-value">{{ lruName || "Not specified" }}</span>
          </div>
          <div class="detail-item">
            <label>LRU Part No. :</label>
            <input
              type="text"
              v-model="lruPartNumber"
              placeholder="Enter LRU Part No."
              class="detail-input"
              :disabled="isReadOnly"
            />
          </div>
          <div class="detail-item">
            <label>Serial Number:</label>
            <input
              type="text"
              v-model="serialNumber"
              placeholder="Enter Serial Number"
              class="detail-input"
              :disabled="isReadOnly"
            />
          </div>
        </div>
        <div class="details-right">
          <div class="detail-item">
            <label>Inspection stage :</label>
            <input
              type="text"
              v-model="inspectionStage"
              placeholder="Enter Inspection stage"
              class="detail-input"
              :disabled="isReadOnly"
            />
          </div>
          <div class="detail-item">
            <label>Date of doc review :</label>
            <input
              type="date"
              v-model="docReviewDate"
              class="detail-input"
              :disabled="isReadOnly"
            />
          </div>
          <div class="detail-item">
            <label>Review venue :</label>
            <input
              type="text"
              v-model="reviewVenue"
              placeholder="Enter Review venue"
              class="detail-input"
              :disabled="isReadOnly"
            />
          </div>
          <div class="detail-item">
            <label>Reference Document:</label>
            <input
              type="text"
              v-model="referenceDocument"
              placeholder="Enter Reference Document"
              class="detail-input"
              :disabled="isReadOnly"
            />
          </div>
        </div>
      </div>

      <!-- Version Selection -->
      <div class="version-selection">
        <h2 class="section-title">Document Version Selection</h2>
        <div class="version-controls">
          <div class="version-dropdown">
            <label for="version-select">Select Document Version:</label>
            <select
              id="version-select"
              v-model="selectedDocumentId"
              @change="onVersionChange"
              class="version-select"
              :disabled="loadingVersions"
            >
              <option value="">
                {{
                  loadingVersions ? "Loading versions..." : "Select a version"
                }}
              </option>
              <option
                v-for="document in availableDocuments"
                :key="document.document_id"
                :value="document.document_id"
              >
                {{ document.document_number }} - {{ document.version }} ({{
                  document.doc_ver
                }}) - {{ document.uploaded_by_name }}
              </option>
            </select>
          </div>
          <div class="version-info" v-if="selectedDocument">
            <span class="version-label">
              Selected: {{ selectedDocument.document_number }} -
              {{ selectedDocument.version }} ({{ selectedDocument.doc_ver }}) -
              Uploaded by {{ selectedDocument.uploaded_by_name }}
            </span>
          </div>
        </div>
      </div>

      <!-- Comments Table -->
      <div class="observations-section">
        <h2 class="section-title">Document Comments & Observations</h2>

        <!-- Loading State -->
        <div v-if="loadingComments" class="loading-container">
          <div class="loading-spinner"></div>
          <p>Loading comments for selected version...</p>
        </div>

        <!-- No Version Selected -->
        <div v-else-if="!selectedDocumentId" class="no-selection">
          <p>
            Please select a document version to view comments and observations.
          </p>
        </div>

        <!-- No Comments -->
        <div v-else-if="documentComments.length === 0" class="no-comments">
          <p>No comments found for the selected version.</p>
        </div>

        <!-- Comments Table -->
        <div v-else class="table-container">
          <table class="observations-table">
            <thead>
              <tr>
                <th>SNO</th>
                <th>Category</th>
                <th>Observations</th>
                <th>Accept/Reject</th>
                <th>Justification</th>
                <th>Reviewer</th>
                <th>Page</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(comment, index) in documentComments"
                :key="comment.id"
              >
                <td>{{ index + 1 }}</td>
                <td>
                  <span
                    class="category-badge"
                    :class="getCategoryClass(comment.section)"
                  >
                    {{
                      comment.section && comment.section.trim() !== ""
                        ? comment.section
                        : "General"
                    }}
                  </span>
                </td>
                <td class="comment-text">
                  {{ comment.description || "No comment" }}
                </td>
                <td>
                  <span
                    class="status-badge"
                    :class="getStatusClass(comment.status)"
                  >
                    {{ comment.status || "Pending" }}
                  </span>
                </td>
                <td class="justification-text">
                  {{ comment.justification || "No justification provided" }}
                </td>
                <td>{{ comment.reviewer_id || "Unknown" }}</td>
                <td>{{ comment.page_no || "N/A" }}</td>
                <td>{{ formatDate(comment.created_at) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Digital Signatures -->
      <div class="signatures-section">
        <h2 class="section-title">Digital Signatures</h2>
        <div class="signatures-grid">
          <!-- Reviewed By Signature -->
          <div class="signature-item">
            <label>Reviewed By:</label>
            <div class="signature-auth-container">
              <div class="signature-inputs">
                <div class="input-group">
                  <label>Username:</label>
                  <input
                    type="text"
                    v-model="reviewedBy.signatureUsername"
                    placeholder="Enter username..."
                    class="signature-input"
                    :disabled="
                      isReadOnly || !reviewedByEnabled || !canAccessSignatures
                    "
                  />
                </div>
                <div class="input-group">
                  <label>Signature Password:</label>
                  <input
                    type="password"
                    v-model="reviewedBy.signaturePassword"
                    placeholder="Enter signature password..."
                    class="signature-input"
                    :disabled="
                      isReadOnly || !reviewedByEnabled || !canAccessSignatures
                    "
                  />
                </div>
                <button
                  type="button"
                  class="btn-verify-signature"
                  @click="verifySignature('reviewed')"
                  :disabled="
                    isReadOnly ||
                    !reviewedByEnabled ||
                    !canAccessSignatures ||
                    !reviewedBy.signatureUsername ||
                    !reviewedBy.signaturePassword
                  "
                >
                  Verify & Load Signature
                </button>
                <div
                  v-if="!canAccessSignatures && !isReadOnly"
                  class="signature-help-text"
                >
                  Signature access is restricted to QA Reviewer, QA Head, and
                  Design Head roles only
                </div>
                <div
                  v-else-if="!reviewedByEnabled && !isReadOnly"
                  class="signature-help-text"
                >
                  Please fill all required fields to enable signature
                  verification
                </div>
              </div>
              <div v-if="reviewedBy.signatureError" class="signature-error">
                {{ reviewedBy.signatureError }}
              </div>
              <div v-if="reviewedBy.signatureUrl" class="signature-display">
                <img
                  :src="reviewedBy.signatureUrl"
                  alt="Reviewed By Signature"
                  class="signature-image"
                />
                <div class="signature-name">
                  {{ reviewedBy.verifiedUserName }}
                </div>
              </div>
              <div v-else class="signature-placeholder">
                <span>No signature loaded</span>
              </div>
              <div class="signature-date">Date: {{ currentDate }}</div>
            </div>
          </div>

          <!-- Approved By Signature -->
          <div class="signature-item">
            <label>Approved By:</label>
            <div class="signature-auth-container">
              <div class="signature-inputs">
                <div class="input-group">
                  <label>Username:</label>
                  <input
                    type="text"
                    v-model="approvedBy.signatureUsername"
                    placeholder="Enter username..."
                    class="signature-input"
                    :disabled="
                      isReadOnly || !approvedByEnabled || !canAccessSignatures
                    "
                  />
                </div>
                <div class="input-group">
                  <label>Signature Password:</label>
                  <input
                    type="password"
                    v-model="approvedBy.signaturePassword"
                    placeholder="Enter signature password..."
                    class="signature-input"
                    :disabled="
                      isReadOnly || !approvedByEnabled || !canAccessSignatures
                    "
                  />
                </div>
                <button
                  type="button"
                  class="btn-verify-signature"
                  @click="verifySignature('approved')"
                  :disabled="
                    isReadOnly ||
                    !approvedByEnabled ||
                    !canAccessSignatures ||
                    !approvedBy.signatureUsername ||
                    !approvedBy.signaturePassword
                  "
                >
                  Verify & Load Signature
                </button>
                <div
                  v-if="!canAccessSignatures && !isReadOnly"
                  class="signature-help-text"
                >
                  Signature access is restricted to QA Reviewer, QA Head, and
                  Design Head roles only
                </div>
                <div
                  v-else-if="!approvedByEnabled && !isReadOnly"
                  class="signature-help-text"
                >
                  <span v-if="!reviewedByVerified"
                    >Please complete "Reviewed By" signature first</span
                  >
                  <span v-else-if="!allFieldsFilled"
                    >Please fill all required fields</span
                  >
                </div>
              </div>
              <div v-if="approvedBy.signatureError" class="signature-error">
                {{ approvedBy.signatureError }}
              </div>
              <div v-if="approvedBy.signatureUrl" class="signature-display">
                <img
                  :src="approvedBy.signatureUrl"
                  alt="Approved By Signature"
                  class="signature-image"
                />
                <div class="signature-name">
                  {{ approvedBy.verifiedUserName }}
                </div>
              </div>
              <div v-else class="signature-placeholder">
                <span>No signature loaded</span>
              </div>
              <div class="signature-date">Date: {{ currentDate }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import jsPDF from "jspdf";
import drdoLogo from "@/assets/images/DRDO_Logo.png";
import aviatraxLogo from "@/assets/images/Aviatrax_Trademark.png";
import { userStore } from "@/stores/userStore";

export default {
  name: "ObservationReport",
  data() {
    return {
      lruName: "",
      projectName: "",
      lruId: null,
      // Properties for document and comment management
      selectedDocumentId: "",
      availableDocuments: [],
      selectedDocument: null,
      documentComments: [],
      loadingComments: false,
      loadingVersions: false,
      // Input fields for user to fill
      serialNumber: "",
      observationCount: "OBS-001",
      currentYear: new Date().getFullYear().toString(),
      currentDate: new Date().toISOString().split("T")[0],
      lruPartNumber: "",
      docReviewDate: new Date().toISOString().split("T")[0],
      reviewVenue: "",
      referenceDocument: "",
      inspectionStage: "Document review/report",
      // Signature authentication data
      reviewedBy: {
        signatureUsername: "",
        signaturePassword: "",
        signatureUrl: "",
        verifiedUserName: "",
        signatureError: "",
        userId: null,
      },
      approvedBy: {
        signatureUsername: "",
        signaturePassword: "",
        signatureUrl: "",
        verifiedUserName: "",
        signatureError: "",
        userId: null,
      },
      reportSubmitted: false,
      // Submitted reports tracking
      submittedReports: [],
      loadingSubmittedReports: false,
      selectedReportId: null,
      showSubmittedReports: false,
    };
  },
  computed: {
    // Check if form should be read-only (when a submitted report is loaded)
    isReadOnly() {
      return this.selectedReportId !== null || this.reportSubmitted;
    },
    // Check if a report already exists for the selected document
    reportExistsForDocument() {
      if (!this.selectedDocumentId) return false;
      return this.submittedReports.some(
        (r) => r.document_id === parseInt(this.selectedDocumentId)
      );
    },
    // Check if all required fields are filled
    allFieldsFilled() {
      return !!(
        this.selectedDocumentId &&
        this.serialNumber &&
        this.lruPartNumber &&
        this.inspectionStage &&
        this.docReviewDate &&
        this.reviewVenue &&
        this.referenceDocument
      );
    },
    // Check if Reviewed By signature is verified
    reviewedByVerified() {
      return !!(
        this.reviewedBy.signatureUrl && this.reviewedBy.verifiedUserName
      );
    },
    // Check if Reviewed By section should be enabled
    reviewedByEnabled() {
      return !this.isReadOnly && this.allFieldsFilled;
    },
    // Check if Approved By section should be enabled
    approvedByEnabled() {
      return (
        !this.isReadOnly && this.allFieldsFilled && this.reviewedByVerified
      );
    },
    // Check if user has permission to access signature features
    canAccessSignatures() {
      const currentUserRole = userStore.getters.currentUserRole();
      // Only QA Reviewer (3), QA Head (2), and Design Head (4) can access signatures
      return (
        currentUserRole === 2 || currentUserRole === 3 || currentUserRole === 4
      );
    },
  },
  mounted() {
    // Get parameters from route
    this.lruName = this.$route.params.lruName || "Unknown LRU";
    this.projectName = this.$route.params.projectName || "Unknown Project";
    this.lruId = this.$route.params.lruId || null;

    console.log("ObservationReport - Route params:", this.$route.params);
    console.log("ObservationReport - Extracted lruId:", this.lruId);

    // Load available documents for the LRU
    if (this.lruId) {
      this.loadAvailableDocuments();
      // Fetch submitted reports for this LRU
      this.fetchSubmittedReports();
    } else {
      console.warn("No LRU ID provided, cannot load documents");
    }
  },
  methods: {
    // Load available documents for the LRU from plan_documents table
    async loadAvailableDocuments() {
      try {
        this.loadingVersions = true;

        console.log("Loading documents for LRU ID:", this.lruId);

        // API call to fetch documents by LRU ID using the existing endpoint
        const response = await fetch(

          `http://localhost:5000/api/lrus/${this.lruId}/plan-documents`
        );
        const data = await response.json();

        if (data.success) {
          this.availableDocuments = data.documents || [];

          // Update LRU and project info from the response
          if (data.lru) {
            this.lruName = data.lru.lru_name || this.lruName;
            this.projectName = data.lru.project_name || this.projectName;
          }

          console.log("Loaded documents:", this.availableDocuments);
          console.log("LRU info:", data.lru);
        } else {
          console.error("Error loading documents:", data.message);
          this.availableDocuments = [];
        }
      } catch (error) {
        console.error("Error fetching documents:", error);
        this.availableDocuments = [];
      } finally {
        this.loadingVersions = false;
      }
    },

    // Load document comments for selected document from document_comments table
    async loadDocumentComments(documentId) {
      if (!documentId) return;

      try {
        this.loadingComments = true;

        // API call to fetch comments for the specific document using the existing endpoint
        const response = await fetch(
          `http://localhost:5000/api/comments?document_id=${documentId}`
          `http://localhost:5000/api/comments?document_id=${documentId}`
        );
        const data = await response.json();

        if (data.success) {
          this.documentComments = data.comments || [];
          console.log("Loaded comments:", this.documentComments);
        } else {
          console.error("Error loading comments:", data.message);
          this.documentComments = [];
        }
      } catch (error) {
        console.error("Error fetching comments:", error);
        this.documentComments = [];
      } finally {
        this.loadingComments = false;
      }
    },

    // Handle document selection change
    async onVersionChange() {
      if (this.selectedDocumentId) {
        this.selectedDocument = this.availableDocuments.find(
          (d) => d.document_id.toString() === this.selectedDocumentId
        );

        // Load comments for the selected document version
        await this.loadDocumentComments(parseInt(this.selectedDocumentId));

        // Refresh submitted reports when document changes
        await this.fetchSubmittedReports();

        // Check if a report exists for this document version
        const reportForDocument = this.submittedReports.find(
          (r) => r.document_id === parseInt(this.selectedDocumentId)
        );

        if (reportForDocument) {
          // Report exists for this version - load the submitted report data
          await this.loadSubmittedReport(reportForDocument.report_id);
        } else {
          // No report exists for this version - clear form and allow editing
          this.clearFormForNewVersion();
        }
      } else {
        this.selectedDocument = null;
        this.documentComments = [];
        // Reset read-only state when no document is selected
        this.selectedReportId = null;
        this.reportSubmitted = false;
        this.clearFormForNewVersion();
      }
    },

    // Clear form fields when switching to a version without submitted report
    clearFormForNewVersion() {
      // Clear all input fields (keep project and LRU name as they are read-only)
      this.serialNumber = "";
      this.observationCount = "OBS-001";
      this.currentYear = new Date().getFullYear().toString();
      this.currentDate = new Date().toISOString().split("T")[0];
      this.lruPartNumber = "";
      this.docReviewDate = new Date().toISOString().split("T")[0];
      this.reviewVenue = "";
      this.referenceDocument = "";
      this.inspectionStage = "Document review/report";

      // Clear signature information
      this.reviewedBy = {
        signatureUsername: "",
        signaturePassword: "",
        signatureUrl: "",
        verifiedUserName: "",
        signatureError: "",
        userId: null,
      };

      this.approvedBy = {
        signatureUsername: "",
        signaturePassword: "",
        signatureUrl: "",
        verifiedUserName: "",
        signatureError: "",
        userId: null,
      };

      // Reset read-only state
      this.selectedReportId = null;
      this.reportSubmitted = false;
    },

    // Get CSS class for category badge based on section
    getCategoryClass(section) {
      if (!section || section.trim() === "") return "category-default";

      const sectionLower = section.toLowerCase();
      if (sectionLower.includes("major") || sectionLower.includes("critical"))
        return "category-major";
      if (sectionLower.includes("minor")) return "category-minor";
      if (sectionLower.includes("general")) return "category-general";
      return "category-default";
    },

    // Get CSS class for status badge
    getStatusClass(status) {
      if (!status) return "status-pending";

      const statusLower = status.toLowerCase();
      if (statusLower.includes("accept") || statusLower.includes("approved"))
        return "status-accepted";
      if (statusLower.includes("reject") || statusLower.includes("rejected"))
        return "status-rejected";
      if (statusLower.includes("pending")) return "status-pending";
      return "status-default";
    },

    // Format date for display
    formatDate(dateString) {
      if (!dateString) return "N/A";

      try {
        const date = new Date(dateString);
        return date.toLocaleDateString("en-GB", {
          day: "2-digit",
          month: "2-digit",
          year: "numeric",
          hour: "2-digit",
          minute: "2-digit",
        });
      } catch (error) {
        return "Invalid Date";
      }
    },

    // Verify signature credentials
    async verifySignature(signatureType) {
      const signature =
        signatureType === "reviewed" ? this.reviewedBy : this.approvedBy;

      if (!signature.signatureUsername || !signature.signaturePassword) {
        signature.signatureError =
          "Please enter both username and signature password";
        return;
      }

      try {
        signature.signatureError = "";
        const response = await fetch(
          "http://localhost:5000/api/users/verify-signature",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              username: signature.signatureUsername,
              signature_password: signature.signaturePassword,
            }),
          }
        );

        const data = await response.json();

        if (data.success) {
          signature.signatureUrl = `http://localhost:5000${data.signature_url}`;
          signature.signatureUrl = `http://localhost:5000${data.signature_url}`;
          signature.verifiedUserName = data.user_name;
          signature.signatureError = "";

          // Store user_id for later use
          if (data.user_id) {
            if (signatureType === "reviewed") {
              this.reviewedBy.userId = data.user_id;
            } else {
              this.approvedBy.userId = data.user_id;
            }
          }

          // Auto-submit report when Approved By is signed
          if (signatureType === "approved") {
            await this.submitIqaObservationReport();
          }
        } else {
          signature.signatureError =
            data.message || "Failed to verify signature";
          signature.signatureUrl = "";
          signature.verifiedUserName = "";
        }
      } catch (error) {
        console.error("Error verifying signature:", error);
        signature.signatureError =
          "Error verifying signature. Please try again.";
        signature.signatureUrl = "";
        signature.verifiedUserName = "";
      }
    },

    // Submit IQA Observation Report
    async submitIqaObservationReport() {
      try {
        // Prevent submission if report is read-only
        if (this.isReadOnly) {
          alert(
            "This report has already been submitted and cannot be modified."
          );
          return;
        }

        // Check if a report already exists for this document
        if (this.reportExistsForDocument) {
          alert(
            "A report has already been submitted for this document version. Please select a different version or load the existing report."
          );
          return;
        }

        // Validate required fields
        if (!this.selectedDocumentId) {
          alert(
            "Please select a document version before submitting the report."
          );
          return;
        }

        if (!this.lruId || !this.projectName || !this.lruName) {
          alert(
            "Missing required information. Please ensure project and LRU data are loaded."
          );
          return;
        }

        // Get current user from localStorage
        const storedUser = localStorage.getItem("user");
        if (!storedUser) {
          alert("User session not found. Please log in again.");
          return;
        }

        const currentUser = JSON.parse(storedUser);
        const createdBy = currentUser.id || currentUser.user_id;

        // Get project_id from API
        let projectId = null;
        try {
          const lruResponse = await fetch(
            `http://localhost:5000/api/lrus/${this.lruId}/metadata`
          );
          const lruData = await lruResponse.json();
          if (lruData.success && lruData.lru && lruData.lru.project_id) {
            projectId = lruData.lru.project_id;
          }
        } catch (error) {
          console.warn("Could not fetch project_id:", error);
        }

        if (!projectId) {
          alert(
            "Could not determine project ID. Please ensure the project is properly loaded."
          );
          return;
        }

        // Prepare report data
        const reportData = {
          project_id: projectId,
          lru_id: this.lruId,
          document_id: parseInt(this.selectedDocumentId),
          observation_count: this.observationCount,
          report_date: this.currentDate,
          current_year: this.currentYear,
          lru_part_number: this.lruPartNumber,
          serial_number: this.serialNumber,
          inspection_stage: this.inspectionStage,
          doc_review_date: this.docReviewDate,
          review_venue: this.reviewVenue,
          reference_document: this.referenceDocument,
          reviewed_by_user_id: this.reviewedBy.userId,
          reviewed_by_signature_path: this.reviewedBy.signatureUrl,
          reviewed_by_verified_name: this.reviewedBy.verifiedUserName,
          approved_by_user_id: this.approvedBy.userId,
          approved_by_signature_path: this.approvedBy.signatureUrl,
          approved_by_verified_name: this.approvedBy.verifiedUserName,
          created_by: createdBy,
        };

        console.log("Submitting IQA Observation Report:", reportData);

        const response = await fetch(
          "http://localhost:5000/api/iqa-observation-reports",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(reportData),
          }
        );

        const data = await response.json();

        if (data.success) {
          this.reportSubmitted = true;
          alert("IQA Observation Report submitted successfully!");
          console.log("Report submitted with ID:", data.report_id);
          // Refresh submitted reports after successful submission
          await this.fetchSubmittedReports();
        } else {
          alert(`Failed to submit report: ${data.message || "Unknown error"}`);
        }
      } catch (error) {
        console.error("Error submitting IQA observation report:", error);
        alert(
          `Error submitting report: ${error.message || "Please try again."}`
        );
      }
    },

    // Fetch submitted IQA observation reports
    async fetchSubmittedReports() {
      try {
        this.loadingSubmittedReports = true;

        // Build query parameters
        const params = new URLSearchParams();
        if (this.projectName) {
          params.append("project_name", this.projectName);
        }
        if (this.lruName) {
          params.append("lru_name", this.lruName);
        }
        if (this.lruId) {
          params.append("lru_id", this.lruId);
        }
        if (this.selectedDocumentId) {
          params.append("document_id", this.selectedDocumentId);
        }

        const response = await fetch(
          `http://localhost:5000/api/iqa-observation-reports?${params.toString()}`
          `http://localhost:5000/api/iqa-observation-reports?${params.toString()}`
        );

        const data = await response.json();

        if (data.success) {
          this.submittedReports = data.reports || [];
          console.log(
            `Fetched ${this.submittedReports.length} submitted reports`
          );

          // If there's a selected document, try to load the most recent report for it
          if (this.selectedDocumentId && this.submittedReports.length > 0) {
            const reportForDocument = this.submittedReports.find(
              (r) => r.document_id === parseInt(this.selectedDocumentId)
            );
            if (reportForDocument && !this.selectedReportId) {
              // Auto-load the most recent report for the selected document
              this.loadSubmittedReport(reportForDocument.report_id);
            }
          }
        } else {
          console.error("Error fetching submitted reports:", data.message);
          this.submittedReports = [];
        }
      } catch (error) {
        console.error("Error fetching submitted reports:", error);
        this.submittedReports = [];
      } finally {
        this.loadingSubmittedReports = false;
      }
    },

    // Load a submitted report's data into the form
    async loadSubmittedReport(reportId) {
      try {
        const report = this.submittedReports.find(
          (r) => r.report_id === reportId
        );
        if (!report) {
          console.error("Report not found:", reportId);
          return;
        }

        // Load the report data into form fields
        this.selectedReportId = reportId;
        this.serialNumber = report.serial_number || "";
        this.observationCount = report.observation_count || "OBS-001";
        this.currentYear =
          report.current_year || new Date().getFullYear().toString();
        this.currentDate =
          report.report_date || new Date().toISOString().split("T")[0];
        this.lruPartNumber = report.lru_part_number || "";
        this.docReviewDate =
          report.doc_review_date || new Date().toISOString().split("T")[0];
        this.reviewVenue = report.review_venue || "";
        this.referenceDocument = report.reference_document || "";
        this.inspectionStage =
          report.inspection_stage || "Document review/report";

        // Load signature information
        if (report.reviewed_by_signature_path) {
          this.reviewedBy.signatureUrl = report.reviewed_by_signature_path;
          this.reviewedBy.verifiedUserName =
            report.reviewed_by_verified_name || "";
          this.reviewedBy.userId = report.reviewed_by_user_id;
        } else {
          // Clear reviewed by signature if not present
          this.reviewedBy.signatureUrl = "";
          this.reviewedBy.verifiedUserName = "";
          this.reviewedBy.userId = null;
        }

        if (report.approved_by_signature_path) {
          this.approvedBy.signatureUrl = report.approved_by_signature_path;
          this.approvedBy.verifiedUserName =
            report.approved_by_verified_name || "";
          this.approvedBy.userId = report.approved_by_user_id;
        } else {
          // Clear approved by signature if not present
          this.approvedBy.signatureUrl = "";
          this.approvedBy.verifiedUserName = "";
          this.approvedBy.userId = null;
        }

        // Ensure document version is selected (should already be set, but just in case)
        if (report.document_id && !this.selectedDocumentId) {
          this.selectedDocumentId = report.document_id.toString();
          await this.loadDocumentComments(report.document_id);
        }

        this.reportSubmitted = true;
        console.log("Loaded submitted report:", report);
      } catch (error) {
        console.error("Error loading submitted report:", error);
      }
    },

    async exportReport() {
      try {
        console.log("Starting PDF export...");

        // Create new PDF document
        const doc = new jsPDF("p", "mm", "a4");
        const pageWidth = doc.internal.pageSize.getWidth();
        const pageHeight = doc.internal.pageSize.getHeight();
        const margin = 20;
        const contentWidth = pageWidth - 2 * margin;

        let yPosition = margin;

        // ===== HEADER WITH LOGOS =====
        const logoHeight = 15; // Height for logos
        const logoY = yPosition;

        // Helper function to load image and convert to base64
        const loadImageAsBase64 = (imagePath) => {
          return new Promise((resolve, reject) => {
            const img = new Image();
            img.crossOrigin = "anonymous";
            img.onload = () => {
              try {
                const canvas = document.createElement("canvas");
                canvas.width = img.width;
                canvas.height = img.height;
                const ctx = canvas.getContext("2d");
                ctx.drawImage(img, 0, 0);
                const base64 = canvas.toDataURL("image/png");
                resolve({ base64, width: img.width, height: img.height });
              } catch (error) {
                reject(error);
              }
            };
            img.onerror = () => reject(new Error("Failed to load image"));
            img.src = imagePath;
          });
        };

        // Load and add DRDO logo (left side)
        try {
          const drdoData = await loadImageAsBase64(drdoLogo);

          // Calculate logo dimensions maintaining aspect ratio
          const maxLogoWidth = 30;
          const maxLogoHeight = logoHeight;
          const aspectRatio = drdoData.width / drdoData.height;
          let logoWidth = maxLogoWidth;
          let logoHeightFinal = logoWidth / aspectRatio;

          if (logoHeightFinal > maxLogoHeight) {
            logoHeightFinal = maxLogoHeight;
            logoWidth = logoHeightFinal * aspectRatio;
          }

          doc.addImage(
            drdoData.base64,
            "PNG",
            margin,
            logoY,
            logoWidth,
            logoHeightFinal
          );
        } catch (error) {
          console.warn("Could not load DRDO logo:", error);
        }

        // Load and add Aviatrax logo (right side)
        try {
          const aviatraxData = await loadImageAsBase64(aviatraxLogo);

          // Calculate logo dimensions maintaining aspect ratio
          const maxLogoWidth = 30;
          const maxLogoHeight = logoHeight;
          const aspectRatio = aviatraxData.width / aviatraxData.height;
          let logoWidth = maxLogoWidth;
          let logoHeightFinal = logoWidth / aspectRatio;

          if (logoHeightFinal > maxLogoHeight) {
            logoHeightFinal = maxLogoHeight;
            logoWidth = logoHeightFinal * aspectRatio;
          }

          // Position on right side
          const logoX = pageWidth - margin - logoWidth;
          doc.addImage(
            aviatraxData.base64,
            "PNG",
            logoX,
            logoY,
            logoWidth,
            logoHeightFinal
          );
        } catch (error) {
          console.warn("Could not load Aviatrax logo:", error);
        }

        // Set font styles
        doc.setFont("helvetica");

        // Main Title - IQA OBSERVATION REPORT (centered between logos)
        // Add more space after logos to prevent overlap
        yPosition = logoY + logoHeight + 8;
        doc.setFontSize(18);
        doc.setFont("helvetica", "bold");
        const titleText = "IQA OBSERVATION REPORT";
        doc.text(titleText, pageWidth / 2, yPosition, {
          align: "center",
        });
        yPosition += 12; // Reduced from 15 to prevent overlap

        // Document path and date on same line
        doc.setFontSize(10);
        doc.setFont("helvetica", "normal");

        // Left side - Document path
        const documentPath = `CASDIC/${this.projectName || "PROJECT"}/${
          this.lruName || "LRU"
        }/SL.${this.serialNumber || "001"}/${this.observationCount || "001"}/${
          this.currentYear || "2025"
        }`;
        doc.text(documentPath, margin, yPosition, { align: "left" });

        // Right side - Date
        const dateText = `Date: ${
          this.currentDate || new Date().toLocaleDateString("en-GB")
        }`;
        doc.text(dateText, pageWidth - margin, yPosition, { align: "right" });
        yPosition += 10; // Reduced from 12 to prevent overlap

        // ===== SUBJECT LINE =====
        doc.setFontSize(12);
        doc.setFont("helvetica", "bold");
        const subjectText = `SUB: IQA Observation Report for ${
          this.lruName || "Unknown LRU"
        }`;
        doc.text(subjectText, pageWidth / 2, yPosition, { align: "center" });
        yPosition += 12; // Reduced from 15 to prevent overlap

        // ===== DOCUMENT VERSION INFO =====
        // Ensure selectedDocument is set if we have selectedDocumentId
        if (!this.selectedDocument && this.selectedDocumentId) {
          this.selectedDocument = this.availableDocuments.find(
            (d) => d.document_id.toString() === this.selectedDocumentId
          );
        }

        if (this.selectedDocument) {
          yPosition += 6;
          doc.setFontSize(10);
          doc.setFont("helvetica", "bold");
          const versionInfo = `Document Version: ${
            this.selectedDocument.document_number || "N/A"
          } - Version ${this.selectedDocument.version || "N/A"}${
            this.selectedDocument.revision
              ? ` (Rev. ${this.selectedDocument.revision})`
              : ""
          }${
            this.selectedDocument.doc_ver
              ? ` - ${this.selectedDocument.doc_ver}`
              : ""
          }`;
          doc.text(versionInfo, pageWidth / 2, yPosition, { align: "center" });
          yPosition += 10;
        } else if (this.selectedDocumentId) {
          // Fallback: try to get document info from availableDocuments
          const docInfo = this.availableDocuments.find(
            (d) => d.document_id.toString() === this.selectedDocumentId
          );
          if (docInfo) {
            yPosition += 6;
            doc.setFontSize(10);
            doc.setFont("helvetica", "bold");
            const versionInfo = `Document Version: ${
              docInfo.document_number || "N/A"
            } - Version ${docInfo.version || "N/A"}${
              docInfo.revision ? ` (Rev. ${docInfo.revision})` : ""
            }${docInfo.doc_ver ? ` - ${docInfo.doc_ver}` : ""}`;
            doc.text(versionInfo, pageWidth / 2, yPosition, {
              align: "center",
            });
            yPosition += 10;
          }
        }

        // ===== DOCUMENT DETAILS SECTION =====
        yPosition += 4; // Add spacing after subject line
        doc.setFontSize(10);

        // Left column details
        const leftColumnX = margin;
        const rightColumnX = margin + contentWidth / 2 + 10;
        const labelWidth = 50; // Fixed width for labels to ensure alignment
        const valueStartX = leftColumnX + labelWidth;
        const rightValueStartX = rightColumnX + labelWidth;

        // Left column - Project details
        const detailsStartY = yPosition;
        let leftColumnY = detailsStartY;

        // Project Name
        doc.setFont("helvetica", "bold");
        doc.text("Project Name :", leftColumnX, leftColumnY);
        doc.setFont("helvetica", "normal");
        doc.text(this.projectName || "Not specified", valueStartX, leftColumnY);
        leftColumnY += 8;

        // LRU Name
        doc.setFont("helvetica", "bold");
        doc.text("LRU Name :", leftColumnX, leftColumnY);
        doc.setFont("helvetica", "normal");
        doc.text(this.lruName || "Not specified", valueStartX, leftColumnY);
        leftColumnY += 8;

        // LRU Part No
        doc.setFont("helvetica", "bold");
        doc.text("LRU Part No. :", leftColumnX, leftColumnY);
        doc.setFont("helvetica", "normal");
        doc.text(
          this.lruPartNumber || "Not specified",
          valueStartX,
          leftColumnY
        );
        leftColumnY += 8;

        // Serial Number
        doc.setFont("helvetica", "bold");
        doc.text("Serial Number :", leftColumnX, leftColumnY);
        doc.setFont("helvetica", "normal");
        doc.text(
          this.serialNumber || "Not specified",
          valueStartX,
          leftColumnY
        );
        leftColumnY += 8;

        // Right column details
        let rightColumnY = detailsStartY;

        // Inspection stage
        doc.setFont("helvetica", "bold");
        doc.text("Inspection stage :", rightColumnX, rightColumnY);
        doc.setFont("helvetica", "normal");
        doc.text(
          this.inspectionStage || "Not specified",
          rightValueStartX,
          rightColumnY
        );
        rightColumnY += 8;

        // Date of doc review
        doc.setFont("helvetica", "bold");
        doc.text("Date of doc review :", rightColumnX, rightColumnY);
        doc.setFont("helvetica", "normal");
        const formattedReviewDate = this.docReviewDate
          ? new Date(this.docReviewDate).toLocaleDateString("en-GB")
          : "Not specified";
        doc.text(formattedReviewDate, rightValueStartX, rightColumnY);
        rightColumnY += 8;

        // Review venue
        doc.setFont("helvetica", "bold");
        doc.text("Review venue :", rightColumnX, rightColumnY);
        doc.setFont("helvetica", "normal");
        doc.text(
          this.reviewVenue || "Not specified",
          rightValueStartX,
          rightColumnY
        );
        rightColumnY += 8;

        // Reference Document
        doc.setFont("helvetica", "bold");
        doc.text("Reference Document :", rightColumnX, rightColumnY);
        doc.setFont("helvetica", "normal");
        doc.text(
          this.referenceDocument || "Not specified",
          rightValueStartX,
          rightColumnY
        );

        // Set yPosition to the maximum of both columns plus spacing
        yPosition = Math.max(leftColumnY, rightColumnY) + 10;

        // ===== OBSERVATIONS SECTION =====
        doc.setFontSize(12);
        doc.setFont("helvetica", "bold");
        doc.text("OBSERVATIONS", pageWidth / 2, yPosition, { align: "center" });
        yPosition += 12;

        // ===== OBSERVATIONS TABLE =====
        // Formal table structure with proper borders and formatting
        const tableStartX = margin;
        const tableEndX = pageWidth - margin;
        const cellPadding = 2;
        const headerHeight = 8;

        // Table column widths (optimized to fit page width: 170mm)
        const snoWidth = 10;
        const categoryWidth = 20;
        const observationWidth = 32;
        const acceptRejectWidth = 22; // Increased to prevent overlap
        const justificationWidth = 26;
        const reviewerWidth = 18;
        const pageWidth_col = 12;
        const dateColWidth = 20;

        // Calculate column start positions
        const colPositions = {
          sno: tableStartX,
          category: tableStartX + snoWidth,
          observation: tableStartX + snoWidth + categoryWidth,
          acceptReject:
            tableStartX + snoWidth + categoryWidth + observationWidth,
          justification:
            tableStartX +
            snoWidth +
            categoryWidth +
            observationWidth +
            acceptRejectWidth,
          reviewer:
            tableStartX +
            snoWidth +
            categoryWidth +
            observationWidth +
            acceptRejectWidth +
            justificationWidth,
          page:
            tableStartX +
            snoWidth +
            categoryWidth +
            observationWidth +
            acceptRejectWidth +
            justificationWidth +
            reviewerWidth,
          date:
            tableStartX +
            snoWidth +
            categoryWidth +
            observationWidth +
            acceptRejectWidth +
            justificationWidth +
            reviewerWidth +
            pageWidth_col,
        };

        // Draw table header box with filled background
        const headerTopY = yPosition - headerHeight + 2;
        const headerBottomY = yPosition + 2;

        // Draw header background (filled rectangle)
        doc.setFillColor(220, 220, 220); // Light gray background
        doc.rect(
          tableStartX,
          headerTopY,
          tableEndX - tableStartX,
          headerHeight,
          "F"
        );

        // Draw header border
        doc.setDrawColor(0, 0, 0);
        doc.setLineWidth(0.5);
        doc.rect(
          tableStartX,
          headerTopY,
          tableEndX - tableStartX,
          headerHeight
        );

        // Table headers with proper alignment and formatting
        doc.setFontSize(8.5); // Slightly smaller font for headers
        doc.setFont("helvetica", "bold");
        doc.setTextColor(0, 0, 0);

        const headerY = headerTopY + headerHeight / 2 + 2;
        doc.text("S.No.", colPositions.sno + snoWidth / 2, headerY, {
          align: "center",
        });
        doc.text(
          "Category",
          colPositions.category + categoryWidth / 2,
          headerY,
          { align: "center" }
        );
        doc.text(
          "Observations",
          colPositions.observation + observationWidth / 2,
          headerY,
          { align: "center" }
        );

        // Accept/Reject header - split into two lines to fit better
        const acceptRejectHeaderX =
          colPositions.acceptReject + acceptRejectWidth / 2;
        const acceptRejectHeaderY1 = headerTopY + 3;
        const acceptRejectHeaderY2 = headerTopY + 6;
        doc.text("Accept/", acceptRejectHeaderX, acceptRejectHeaderY1, {
          align: "center",
        });
        doc.text("Reject", acceptRejectHeaderX, acceptRejectHeaderY2, {
          align: "center",
        });

        doc.text(
          "Justification",
          colPositions.justification + justificationWidth / 2,
          headerY,
          { align: "center" }
        );
        doc.text(
          "Reviewer",
          colPositions.reviewer + reviewerWidth / 2,
          headerY,
          { align: "center" }
        );
        doc.text("Page", colPositions.page + pageWidth_col / 2, headerY, {
          align: "center",
        });
        doc.text("Date", colPositions.date + dateColWidth / 2, headerY, {
          align: "center",
        });

        // Draw vertical lines in header
        doc.setLineWidth(0.3);
        doc.line(
          colPositions.category,
          headerTopY,
          colPositions.category,
          headerBottomY
        );
        doc.line(
          colPositions.observation,
          headerTopY,
          colPositions.observation,
          headerBottomY
        );
        doc.line(
          colPositions.acceptReject,
          headerTopY,
          colPositions.acceptReject,
          headerBottomY
        );
        doc.line(
          colPositions.justification,
          headerTopY,
          colPositions.justification,
          headerBottomY
        );
        doc.line(
          colPositions.reviewer,
          headerTopY,
          colPositions.reviewer,
          headerBottomY
        );
        doc.line(
          colPositions.page,
          headerTopY,
          colPositions.page,
          headerBottomY
        );
        doc.line(
          colPositions.date,
          headerTopY,
          colPositions.date,
          headerBottomY
        );

        yPosition = headerBottomY + 2;

        // Table data rows with formal formatting
        doc.setFont("helvetica", "normal");
        doc.setFontSize(8);
        doc.setTextColor(0, 0, 0);
        doc.setLineWidth(0.3);

        // Safety check - ensure comments array exists and has items
        if (!this.documentComments || this.documentComments.length === 0) {
          // Draw empty table cell
          const emptyRowHeight = 10;
          doc.rect(
            tableStartX,
            yPosition,
            tableEndX - tableStartX,
            emptyRowHeight
          );
          doc.text(
            "No observations available",
            colPositions.observation + observationWidth / 2,
            yPosition + emptyRowHeight / 2 + 2,
            { align: "center" }
          );
          yPosition += emptyRowHeight + 2;
        } else {
          // Limit comments to fit on single page
          const maxComments = Math.min(this.documentComments.length, 8);
          const commentsToShow = this.documentComments.slice(0, maxComments);

          commentsToShow.forEach((comment, index) => {
            const rowStartY = yPosition;
            const cellPadding = 1.5;
            const minRowHeight = 8;

            // Prepare all cell content
            const snoText = (index + 1).toString();

            const categoryText =
              comment.section && comment.section.trim() !== ""
                ? comment.section
                : "General";
            const categoryLines = doc.splitTextToSize(
              categoryText,
              categoryWidth - cellPadding * 2
            );

            const observationText = comment.description || "No comment";
            const observationLines = doc.splitTextToSize(
              observationText,
              observationWidth - cellPadding * 2
            );

            const acceptRejectText = comment.status || "Pending";
            // Ensure Accept/Reject text fits within the column width
            const acceptRejectMaxWidth =
              acceptRejectWidth - cellPadding * 2 - 1;
            const acceptRejectLines = doc.splitTextToSize(
              acceptRejectText,
              acceptRejectMaxWidth
            );

            const justificationText =
              comment.justification || "No justification provided";
            const justificationLines = doc.splitTextToSize(
              justificationText,
              justificationWidth - cellPadding * 2
            );

            const reviewerText = comment.reviewer_id
              ? comment.reviewer_id.toString()
              : "Unknown";
            const reviewerLines = doc.splitTextToSize(
              reviewerText,
              reviewerWidth - cellPadding * 2
            );

            const pageText = comment.page_no
              ? comment.page_no.toString()
              : "N/A";

            const dateText = this.formatDate(comment.created_at) || "N/A";
            const dateLines = doc.splitTextToSize(
              dateText,
              dateColWidth - cellPadding * 2
            );

            // Calculate row height based on the longest text
            const lineHeight = 3.5;
            const maxLines = Math.max(
              observationLines.length,
              justificationLines.length,
              categoryLines.length,
              acceptRejectLines.length,
              reviewerLines.length,
              dateLines.length,
              1
            );
            const rowHeight = Math.max(
              maxLines * lineHeight + cellPadding * 2,
              minRowHeight
            );
            const rowBottomY = rowStartY + rowHeight;

            // Draw row border
            doc.rect(
              tableStartX,
              rowStartY,
              tableEndX - tableStartX,
              rowHeight
            );

            // Draw vertical lines between columns
            doc.line(
              colPositions.category,
              rowStartY,
              colPositions.category,
              rowBottomY
            );
            doc.line(
              colPositions.observation,
              rowStartY,
              colPositions.observation,
              rowBottomY
            );
            doc.line(
              colPositions.acceptReject,
              rowStartY,
              colPositions.acceptReject,
              rowBottomY
            );
            doc.line(
              colPositions.justification,
              rowStartY,
              colPositions.justification,
              rowBottomY
            );
            doc.line(
              colPositions.reviewer,
              rowStartY,
              colPositions.reviewer,
              rowBottomY
            );
            doc.line(
              colPositions.page,
              rowStartY,
              colPositions.page,
              rowBottomY
            );
            doc.line(
              colPositions.date,
              rowStartY,
              colPositions.date,
              rowBottomY
            );

            // Calculate text Y position (top of cell with padding)
            const textStartY = rowStartY + cellPadding + 2;

            // S.No. - centered vertically
            const snoY = rowStartY + rowHeight / 2 + 1;
            doc.text(snoText, colPositions.sno + snoWidth / 2, snoY, {
              align: "center",
            });

            // Category - top aligned, centered horizontally
            doc.text(
              categoryLines,
              colPositions.category + categoryWidth / 2,
              textStartY,
              { align: "center", maxWidth: categoryWidth - cellPadding * 2 }
            );

            // Observations - top aligned, left aligned
            doc.text(
              observationLines,
              colPositions.observation + cellPadding,
              textStartY,
              { align: "left", maxWidth: observationWidth - cellPadding * 2 }
            );

            // Accept/Reject - top aligned, centered horizontally, with proper width constraint
            doc.text(
              acceptRejectLines,
              colPositions.acceptReject + acceptRejectWidth / 2,
              textStartY,
              { align: "center", maxWidth: acceptRejectMaxWidth }
            );

            // Justification - top aligned, left aligned
            doc.text(
              justificationLines,
              colPositions.justification + cellPadding,
              textStartY,
              { align: "left", maxWidth: justificationWidth - cellPadding * 2 }
            );

            // Reviewer - top aligned, centered horizontally
            doc.text(
              reviewerLines,
              colPositions.reviewer + reviewerWidth / 2,
              textStartY,
              { align: "center", maxWidth: reviewerWidth - cellPadding * 2 }
            );

            // Page - centered vertically
            const pageY = rowStartY + rowHeight / 2 + 1;
            doc.text(pageText, colPositions.page + pageWidth_col / 2, pageY, {
              align: "center",
            });

            // Date - top aligned, centered horizontally
            doc.text(
              dateLines,
              colPositions.date + dateColWidth / 2,
              textStartY,
              { align: "center", maxWidth: dateColWidth - cellPadding * 2 }
            );

            yPosition = rowBottomY;
          });

          // Draw final bottom border
          doc.setLineWidth(0.5);
          doc.line(tableStartX, yPosition, tableEndX, yPosition);
          yPosition += 2;

          // Show message if comments were truncated
          if (this.documentComments.length > maxComments) {
            yPosition += 8;
            doc.setFont("helvetica", "italic");
            doc.setFontSize(8);
            doc.text(
              `Note: Showing ${maxComments} of ${this.documentComments.length} comments. Export detailed report for complete list.`,
              margin,
              yPosition
            );
            doc.setFont("helvetica", "normal");
            doc.setFontSize(9);
          }
        }

        yPosition += 15;

        // ===== SIGNATURES SECTION =====
        // Optimize for single page - ensure we have enough space
        if (yPosition > pageHeight - 60) {
          yPosition = pageHeight - 60;
        }

        doc.setFontSize(12);
        doc.setFont("helvetica", "bold");
        doc.text("SIGNATURES", pageWidth / 2, yPosition, { align: "center" });
        yPosition += 15;

        // ===== SIGNATURE AREA =====
        // Create a single horizontal signature box divided into two sections
        const totalSignatureWidth = contentWidth - 20; // Leave some margin
        const signatureHeight = 25;
        const leftSectionWidth = totalSignatureWidth * 0.5; // 50% for left
        const rightSectionWidth = totalSignatureWidth * 0.5; // 50% for right

        const signatureStartX = margin + 10;
        const signatureY = yPosition;

        // Draw the main signature box
        doc.rect(
          signatureStartX,
          signatureY,
          totalSignatureWidth,
          signatureHeight
        );

        // Draw vertical dividing line
        doc.line(
          signatureStartX + leftSectionWidth,
          signatureY,
          signatureStartX + leftSectionWidth,
          signatureY + signatureHeight
        );

        // Load and add Reviewed By signature
        if (this.reviewedBy.signatureUrl) {
          try {
            const reviewedSignatureData = await loadImageAsBase64(
              this.reviewedBy.signatureUrl
            );
            const sigMaxWidth = leftSectionWidth - 10;
            const sigMaxHeight = signatureHeight - 8;
            const sigAspectRatio =
              reviewedSignatureData.width / reviewedSignatureData.height;
            let sigWidth = sigMaxWidth;
            let sigHeight = sigWidth / sigAspectRatio;

            if (sigHeight > sigMaxHeight) {
              sigHeight = sigMaxHeight;
              sigWidth = sigHeight * sigAspectRatio;
            }

            const sigX = signatureStartX + (leftSectionWidth - sigWidth) / 2;
            const sigY = signatureY + (signatureHeight - sigHeight) / 2;

            doc.addImage(
              reviewedSignatureData.base64,
              "PNG",
              sigX,
              sigY,
              sigWidth,
              sigHeight
            );
          } catch (error) {
            console.warn("Could not load Reviewed By signature:", error);
          }
        }

        // Load and add Approved By signature
        if (this.approvedBy.signatureUrl) {
          try {
            const approvedSignatureData = await loadImageAsBase64(
              this.approvedBy.signatureUrl
            );
            const sigMaxWidth = rightSectionWidth - 10;
            const sigMaxHeight = signatureHeight - 8;
            const sigAspectRatio =
              approvedSignatureData.width / approvedSignatureData.height;
            let sigWidth = sigMaxWidth;
            let sigHeight = sigWidth / sigAspectRatio;

            if (sigHeight > sigMaxHeight) {
              sigHeight = sigMaxHeight;
              sigWidth = sigHeight * sigAspectRatio;
            }

            const sigX =
              signatureStartX +
              leftSectionWidth +
              (rightSectionWidth - sigWidth) / 2;
            const sigY = signatureY + (signatureHeight - sigHeight) / 2;

            doc.addImage(
              approvedSignatureData.base64,
              "PNG",
              sigX,
              sigY,
              sigWidth,
              sigHeight
            );
          } catch (error) {
            console.warn("Could not load Approved By signature:", error);
          }
        }

        // Add labels below the signature box
        yPosition += signatureHeight + 8;

        // Left section label
        doc.setFontSize(9);
        doc.setFont("helvetica", "bold");
        doc.text(
          "Reviewed by",
          signatureStartX + leftSectionWidth / 2,
          yPosition,
          { align: "center" }
        );

        // Right section label
        doc.text(
          "Approved by",
          signatureStartX + leftSectionWidth + rightSectionWidth / 2,
          yPosition,
          { align: "center" }
        );

        // Add names below labels
        yPosition += 6;
        doc.setFont("helvetica", "normal");
        doc.setFontSize(8);

        // Reviewed by name
        const reviewedByName =
          this.reviewedBy.verifiedUserName || "Not specified";
        doc.text(
          reviewedByName,
          signatureStartX + leftSectionWidth / 2,
          yPosition,
          { align: "center" }
        );

        // Approved by name
        const approvedByName =
          this.approvedBy.verifiedUserName || "Not specified";
        doc.text(
          approvedByName,
          signatureStartX + leftSectionWidth + rightSectionWidth / 2,
          yPosition,
          { align: "center" }
        );

        // ===== SAVE PDF =====
        const lruNameForFile = this.lruName || "Unknown_LRU";
        const currentDateForFile =
          this.currentDate || new Date().toLocaleDateString("en-GB");
        const fileName = `IQA_Observation_Report_${lruNameForFile}_${currentDateForFile.replace(
          /\//g,
          "-"
        )}.pdf`;
        doc.save(fileName);

        // Show success message
        this.$nextTick(() => {
          alert("Report exported successfully as PDF!");
        });
      } catch (error) {
        console.error("Error exporting PDF:", error);
        this.$nextTick(() => {
          alert(
            `Error exporting PDF: ${
              error.message || "Unknown error"
            }. Please try again.`
          );
        });
      }
    },
  },
};
</script>

<style scoped>
.view-observations-page {
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

/* Report Header */
.report-header {
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

.stage-value {
  color: #4a5568;
  font-weight: 600;
}

/* Document Details */
.document-details {
  background: white;
  padding: 25px;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 25px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px solid #e2e8f0;
}

.detail-item:last-child {
  border-bottom: none;
}

.detail-item label {
  font-weight: 600;
  color: #4a5568;
  min-width: 150px;
}

.detail-item span {
  color: #2d3748;
  font-weight: 500;
}

.detail-item .readonly-value {
  color: #2d3748;
  font-weight: 600;
  padding: 8px 12px;
  background: #f7fafc;
  border-radius: 6px;
  display: inline-block;
  min-width: 150px;
}

.detail-input {
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.95em;
  color: #2d3748;
  width: 100%;
  max-width: 300px;
  transition: border-color 0.3s ease;
}

.detail-input:focus {
  outline: none;
  border-color: #4a5568;
  box-shadow: 0 0 0 3px rgba(74, 85, 104, 0.1);
}

.detail-input[type="date"] {
  cursor: pointer;
}

/* Version Selection Styles */
.version-selection {
  background: white;
  padding: 25px;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 25px;
}

.version-controls {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.version-dropdown {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.version-dropdown label {
  font-weight: 600;
  color: #4a5568;
  font-size: 1.1em;
}

.version-select {
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1em;
  background: white;
  cursor: pointer;
  transition: border-color 0.3s ease;
}

.version-select:focus {
  outline: none;
  border-color: #4a5568;
  box-shadow: 0 0 0 3px rgba(74, 85, 104, 0.1);
}

.version-select:disabled {
  background-color: #f7fafc;
  cursor: not-allowed;
  opacity: 0.6;
}

.version-info {
  padding: 10px 15px;
  background: #f7fafc;
  border-radius: 8px;
  border-left: 4px solid #4a5568;
}

.version-label {
  font-weight: 600;
  color: #2d3748;
}

/* Observations Section */
.observations-section {
  background: white;
  padding: 25px;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 25px;
}

.section-title {
  color: #2d3748;
  border-bottom: 3px solid #4a5568;
  padding-bottom: 15px;
  margin-bottom: 25px;
  font-size: 1.5em;
  font-weight: 600;
}

.table-container {
  overflow-x: auto;
  margin-bottom: 20px;
}

.observations-table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
}

.observations-table th {
  background: #2d3748;
  color: white;
  padding: 15px;
  text-align: left;
  font-weight: 600;
  font-size: 0.9em;
}

.observations-table td {
  padding: 15px;
  border-bottom: 1px solid #e2e8f0;
  vertical-align: top;
}

.observations-table tr:nth-child(even) {
  background-color: #f8fafc;
}

.observations-table tr:hover {
  background-color: #edf2f7;
}

/* Loading and State Styles */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  text-align: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #4a5568;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.no-selection,
.no-comments {
  text-align: center;
  padding: 40px 20px;
  color: #6c757d;
  font-size: 1.1em;
  background: #f8f9fa;
  border-radius: 8px;
  border: 2px dashed #dee2e6;
}

/* Badge Styles */
.category-badge,
.status-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.85em;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.category-major {
  background-color: #dc3545;
  color: white;
}

.category-minor {
  background-color: #ffc107;
  color: #212529;
}

.category-general {
  background-color: #17a2b8;
  color: white;
}

.category-default {
  background-color: #6c757d;
  color: white;
}

.status-accepted {
  background-color: #28a745;
  color: white;
}

.status-rejected {
  background-color: #dc3545;
  color: white;
}

.status-pending {
  background-color: #ffc107;
  color: #212529;
}

.status-default {
  background-color: #6c757d;
  color: white;
}

/* Table Text Styles */
.comment-text,
.justification-text {
  max-width: 300px;
  word-wrap: break-word;
  line-height: 1.4;
}

.comment-text {
  font-style: italic;
  color: #495057;
}

.justification-text {
  color: #6c757d;
}

/* Signatures Section */
.signatures-section {
  background: white;
  padding: 25px;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 25px;
}

.signatures-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}

.signature-item {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.signature-item label {
  font-weight: 600;
  color: #4a5568;
  font-size: 1.1em;
}

.signature-display {
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 6px;
  padding: 15px;
  min-height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 10px;
}

.signature-name {
  font-weight: bold;
  color: #333;
  font-size: 1.1em;
}

.signature-date {
  font-size: 0.9em;
  color: #6c757d;
  margin-top: 5px;
  text-align: center;
}

/* Signature Authentication Styles */
.signature-auth-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
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

.signature-inputs .input-group label {
  font-size: 0.9em;
  font-weight: 600;
  color: #4a5568;
}

.signature-input {
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.9em;
  transition: border-color 0.3s ease;
}

.signature-input:focus {
  outline: none;
  border-color: #4a5568;
  box-shadow: 0 0 0 3px rgba(74, 85, 104, 0.1);
}

.btn-verify-signature {
  padding: 10px 16px;
  background: #4a5568;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.9em;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s ease;
}

.btn-verify-signature:hover:not(:disabled) {
  background: #2d3748;
}

.btn-verify-signature:disabled {
  background: #cbd5e0;
  cursor: not-allowed;
  opacity: 0.6;
}

.signature-error {
  color: #dc3545;
  font-size: 0.85em;
  padding: 8px;
  background: #f8d7da;
  border: 1px solid #f5c6cb;
  border-radius: 4px;
}

.signature-image {
  max-width: 200px;
  max-height: 80px;
  object-fit: contain;
  margin-bottom: 8px;
}

.signature-placeholder {
  padding: 20px;
  background: #f8f9fa;
  border: 2px dashed #dee2e6;
  border-radius: 6px;
  text-align: center;
  color: #6c757d;
  font-size: 0.9em;
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

  .document-details {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .signatures-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .observations-table {
    font-size: 0.9em;
  }

  .observations-table th,
  .observations-table td {
    padding: 10px 8px;
  }

  .version-controls {
    gap: 10px;
  }

  .version-select {
    padding: 10px 12px;
    font-size: 0.9em;
  }

  .comment-text,
  .justification-text {
    max-width: 200px;
    font-size: 0.9em;
  }

  .category-badge,
  .status-badge {
    font-size: 0.75em;
    padding: 3px 8px;
  }
}

/* Submitted Reports Section Styles */
.submitted-reports-section {
  margin: 30px 0;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #dee2e6;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.toggle-button {
  padding: 8px 16px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
  transition: background 0.2s;
}

.toggle-button:hover {
  background: #0056b3;
}

.submitted-reports-list {
  margin-top: 15px;
}

.submitted-reports-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 4px;
  overflow: hidden;
}

.submitted-reports-table thead {
  background: #343a40;
  color: white;
}

.submitted-reports-table th {
  padding: 12px;
  text-align: left;
  font-weight: 600;
  font-size: 0.9em;
}

.submitted-reports-table td {
  padding: 12px;
  border-bottom: 1px solid #dee2e6;
  font-size: 0.9em;
}

.submitted-reports-table tbody tr {
  transition: background 0.2s;
}

.submitted-reports-table tbody tr:hover {
  background: #f8f9fa;
}

.submitted-reports-table tbody tr.selected {
  background: #e7f3ff;
  border-left: 3px solid #007bff;
}

.load-report-btn {
  padding: 6px 12px;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85em;
  transition: background 0.2s;
}

.load-report-btn:hover {
  background: #218838;
}

/* Read-Only Warning Styles */
.read-only-warning {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  background: #fff3cd;
  border: 2px solid #ffc107;
  border-radius: 8px;
  margin: 20px 0;
  color: #856404;
  font-weight: 500;
}

.read-only-warning svg {
  flex-shrink: 0;
  color: #ffc107;
}

.detail-input:disabled,
.signature-input:disabled,
.version-select:disabled {
  background-color: #f7fafc;
  cursor: not-allowed;
  opacity: 0.7;
  color: #6c757d;
}

.btn-verify-signature:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.signature-help-text {
  margin-top: 8px;
  padding: 8px 12px;
  background: #fff3cd;
  border: 1px solid #ffc107;
  border-radius: 4px;
  color: #856404;
  font-size: 0.85em;
  font-style: italic;
}

.signature-input:disabled,
.signature-input[disabled] {
  background-color: #f7fafc;
  cursor: not-allowed;
  opacity: 0.6;
  color: #6c757d;
}
</style>
