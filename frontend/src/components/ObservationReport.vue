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
          EXPORT
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

      <!-- Document Details Grid -->
      <div class="document-details">
        <div class="details-left">
          <div class="detail-item">
            <label>Project Name :</label>
            <span>{{ projectName }}</span>
          </div>
          <div class="detail-item">
            <label>LRU Name :</label>
            <span>{{ lruName }}</span>
          </div>
          <div class="detail-item">
            <label>LRU Part No. :</label>
            <span>{{ lruPartNumber }}</span>
          </div>
          <div class="detail-item">
            <label>Serial Number:</label>
            <span>{{ serialNumber }}</span>
          </div>
        </div>
        <div class="details-right">
          <div class="detail-item">
            <label>Inspection stage :</label>
            <span class="stage-value">Document review/report</span>
          </div>
          <div class="detail-item">
            <label>Date of doc review :</label>
            <span>{{ docReviewDate }}</span>
          </div>
          <div class="detail-item">
            <label>Review venue :</label>
            <span>{{ reviewVenue }}</span>
          </div>
          <div class="detail-item">
            <label>Reference Document:</label>
            <span>{{ referenceDocument }}</span>
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
          <div class="signature-item">
            <label>Reviewed By:</label>
            <div class="signature-display">
              <span class="signature-name">QA Reviewer</span>
            </div>
            <div class="signature-date">Date: {{ currentDate }}</div>
          </div>

          <div class="signature-item">
            <label>Approved By:</label>
            <div class="signature-display">
              <span class="signature-name">Design Team</span>
            </div>
            <div class="signature-date">Date: {{ currentDate }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import jsPDF from "jspdf";

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
      // Sample data
      serialNumber: "SL-001",
      observationCount: "OBS-001",
      currentYear: "2025",
      currentDate: "2025-01-15",
      lruPartNumber: "LRU-001",
      docReviewDate: "2025-01-15",
      reviewVenue: "QA Department",
      referenceDocument: "Technical Specification",
    };
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
          `http://localhost:8000/api/lrus/${this.lruId}/plan-documents`
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
          `http://localhost:8000/api/comments?document_id=${documentId}`
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
    onVersionChange() {
      if (this.selectedDocumentId) {
        this.selectedDocument = this.availableDocuments.find(
          (d) => d.document_id.toString() === this.selectedDocumentId
        );
        this.loadDocumentComments(this.selectedDocumentId);
      } else {
        this.selectedDocument = null;
        this.documentComments = [];
      }
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

    exportReport() {
      try {
        console.log("Starting PDF export...");

        // Create new PDF document
        const doc = new jsPDF("p", "mm", "a4");
        const pageWidth = doc.internal.pageSize.getWidth();
        const pageHeight = doc.internal.pageSize.getHeight();
        const margin = 20;
        const contentWidth = pageWidth - 2 * margin;

        let yPosition = margin;

        // Set font styles
        doc.setFont("helvetica");

        // ===== HEADER SECTION =====
        // Main Title - IQA OBSERVATION REPORT
        doc.setFontSize(18);
        doc.setFont("helvetica", "bold");
        doc.text("IQA OBSERVATION REPORT", pageWidth / 2, yPosition, {
          align: "center",
        });
        yPosition += 15;

        // Document path and date on same line
        doc.setFontSize(10);
        doc.setFont("helvetica", "normal");

        // Left side - Document path
        const documentPath = `CASDIC/${this.projectName || "PROJECT"}/${
          this.lruName || "LRU"
        }/SL.${this.serialNumber || "001"}/${this.observationCount || "001"}/${
          this.currentYear || "2025"
        }`;
        doc.text(documentPath, margin, yPosition);

        // Right side - Date
        const dateText = `Date: ${
          this.currentDate || new Date().toLocaleDateString("en-GB")
        }`;
        const dateWidth = doc.getTextWidth(dateText);
        doc.text(dateText, pageWidth - margin - dateWidth, yPosition);
        yPosition += 12;

        // ===== SUBJECT LINE =====
        doc.setFontSize(12);
        doc.setFont("helvetica", "bold");
        const subjectText = `SUB: IQA Observation Report for ${
          this.lruName || "Unknown LRU"
        }`;
        doc.text(subjectText, pageWidth / 2, yPosition, { align: "center" });
        yPosition += 15;

        // ===== DOCUMENT DETAILS SECTION =====
        doc.setFontSize(10);

        // Left column details
        const leftColumnX = margin;
        const rightColumnX = margin + contentWidth / 2;
        const labelOffset = 40; // Space after label

        // Left column - Project details
        yPosition = margin + 42;

        // Project Name
        doc.setFont("helvetica", "bold");
        doc.text("Project Name :", leftColumnX, yPosition);
        doc.setFont("helvetica", "normal");
        doc.text(
          this.projectName || "Not specified",
          leftColumnX + labelOffset,
          yPosition
        );
        yPosition += 8;

        // LRU Name
        doc.setFont("helvetica", "bold");
        doc.text("LRU Name :", leftColumnX, yPosition);
        doc.setFont("helvetica", "normal");
        doc.text(
          this.lruName || "Not specified",
          leftColumnX + labelOffset,
          yPosition
        );
        yPosition += 8;

        // LRU Part No
        doc.setFont("helvetica", "bold");
        doc.text("LRU Part No. :", leftColumnX, yPosition);
        doc.setFont("helvetica", "normal");
        doc.text(
          this.lruPartNumber || "Not specified",
          leftColumnX + labelOffset,
          yPosition
        );
        yPosition += 8;

        // Serial Number
        doc.setFont("helvetica", "bold");
        doc.text("Serial Number :", leftColumnX, yPosition);
        doc.setFont("helvetica", "normal");
        doc.text(
          this.serialNumber || "Not specified",
          leftColumnX + labelOffset,
          yPosition
        );
        yPosition += 8;

        // Right column details
        yPosition = margin + 42;

        // Inspection stage
        doc.setFont("helvetica", "bold");
        doc.text("Inspection stage :", rightColumnX, yPosition);
        doc.setFont("helvetica", "normal");
        doc.text(
          "Document review/report",
          rightColumnX + labelOffset,
          yPosition
        );
        yPosition += 8;

        // Date of doc review
        doc.setFont("helvetica", "bold");
        doc.text("Date of doc review :", rightColumnX, yPosition);
        doc.setFont("helvetica", "normal");
        doc.text(
          this.docReviewDate || "Not specified",
          rightColumnX + labelOffset,
          yPosition
        );
        yPosition += 8;

        // Review venue
        doc.setFont("helvetica", "bold");
        doc.text("Review venue :", rightColumnX, yPosition);
        doc.setFont("helvetica", "normal");
        doc.text(
          this.reviewVenue || "Not specified",
          rightColumnX + labelOffset,
          yPosition
        );
        yPosition += 8;

        // Reference Document
        doc.setFont("helvetica", "bold");
        doc.text("Reference Document :", rightColumnX, yPosition);
        doc.setFont("helvetica", "normal");
        doc.text(
          this.referenceDocument || "Not specified",
          rightColumnX + labelOffset,
          yPosition
        );
        yPosition += 15;

        // ===== OBSERVATIONS SECTION =====
        doc.setFontSize(12);
        doc.setFont("helvetica", "bold");
        doc.text("OBSERVATIONS", pageWidth / 2, yPosition, { align: "center" });
        yPosition += 12;

        // ===== OBSERVATIONS TABLE =====
        doc.setFontSize(9);
        doc.setFont("helvetica", "bold");

        // Table column widths and positions (optimized for single page)
        const tableStartX = margin;
        const snoWidth = 12;
        const categoryWidth = 25;
        const observationWidth = 40;
        const acceptRejectWidth = 20;
        const justificationWidth = 30;
        const reviewerWidth = 20;
        const pageWidth_col = 15;
        const dateColWidth = 25;

        // Table headers with proper spacing
        doc.text("SNO", tableStartX, yPosition);
        doc.text("Category", tableStartX + snoWidth, yPosition);
        doc.text(
          "Observations",
          tableStartX + snoWidth + categoryWidth,
          yPosition
        );
        doc.text(
          "Accept/Reject",
          tableStartX + snoWidth + categoryWidth + observationWidth,
          yPosition
        );
        doc.text(
          "Justification",
          tableStartX +
            snoWidth +
            categoryWidth +
            observationWidth +
            acceptRejectWidth,
          yPosition
        );
        doc.text(
          "Reviewer",
          tableStartX +
            snoWidth +
            categoryWidth +
            observationWidth +
            acceptRejectWidth +
            justificationWidth,
          yPosition
        );
        doc.text(
          "Page",
          tableStartX +
            snoWidth +
            categoryWidth +
            observationWidth +
            acceptRejectWidth +
            justificationWidth +
            reviewerWidth,
          yPosition
        );
        doc.text(
          "Date",
          tableStartX +
            snoWidth +
            categoryWidth +
            observationWidth +
            acceptRejectWidth +
            justificationWidth +
            reviewerWidth +
            pageWidth_col,
          yPosition
        );
        yPosition += 6;

        // Draw table header lines
        doc.line(margin, yPosition - 3, pageWidth - margin, yPosition - 3);
        doc.line(margin, yPosition, pageWidth - margin, yPosition);
        yPosition += 4;

        // Table data
        doc.setFont("helvetica", "normal");

        // Safety check - ensure comments array exists and has items
        if (!this.documentComments || this.documentComments.length === 0) {
          doc.text(
            "No comments available",
            tableStartX + snoWidth + categoryWidth,
            yPosition
          );
          yPosition += 15;
        } else {
          // Limit comments to fit on single page
          const maxComments = Math.min(this.documentComments.length, 8);
          const commentsToShow = this.documentComments.slice(0, maxComments);

          commentsToShow.forEach((comment, index) => {
            yPosition += 6;

            // SNO
            doc.text((index + 1).toString(), tableStartX, yPosition);

            // Category (shortened)
            const categoryText = (
              comment.section && comment.section.trim() !== ""
                ? comment.section
                : "General"
            ).substring(0, 15);
            doc.text(categoryText, tableStartX + snoWidth, yPosition);

            // Observations - handle long text with proper wrapping
            const observationText = (
              comment.description || "No comment"
            ).substring(0, 60);
            const observationLines = doc.splitTextToSize(
              observationText,
              observationWidth - 2
            );
            doc.text(
              observationLines,
              tableStartX + snoWidth + categoryWidth,
              yPosition
            );

            // Accept/Reject
            const acceptRejectText = (comment.status || "Pending").substring(
              0,
              15
            );
            doc.text(
              acceptRejectText,
              tableStartX + snoWidth + categoryWidth + observationWidth,
              yPosition
            );

            // Justification - handle long text with proper wrapping
            const justificationText = (
              comment.justification || "No justification provided"
            ).substring(0, 40);
            const justificationLines = doc.splitTextToSize(
              justificationText,
              justificationWidth - 2
            );
            doc.text(
              justificationLines,
              tableStartX +
                snoWidth +
                categoryWidth +
                observationWidth +
                acceptRejectWidth,
              yPosition
            );

            // Reviewer
            const reviewerText = (
              comment.reviewer_id ? comment.reviewer_id.toString() : "Unknown"
            ).substring(0, 15);
            doc.text(
              reviewerText,
              tableStartX +
                snoWidth +
                categoryWidth +
                observationWidth +
                acceptRejectWidth +
                justificationWidth,
              yPosition
            );

            // Page
            const pageText = (
              comment.page_no ? comment.page_no.toString() : "N/A"
            ).substring(0, 10);
            doc.text(
              pageText,
              tableStartX +
                snoWidth +
                categoryWidth +
                observationWidth +
                acceptRejectWidth +
                justificationWidth +
                reviewerWidth,
              yPosition
            );

            // Date
            const dateText = this.formatDate(comment.created_at) || "N/A";
            doc.text(
              dateText.substring(0, 20),
              tableStartX +
                snoWidth +
                categoryWidth +
                observationWidth +
                acceptRejectWidth +
                justificationWidth +
                reviewerWidth +
                pageWidth_col,
              yPosition
            );

            // Calculate row height based on the longest text
            const maxLines = Math.max(
              observationLines.length,
              justificationLines.length,
              1
            );
            yPosition += Math.max(maxLines * 3, 8);
          });

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

        // Add names inside the signature boxes
        yPosition -= 8;
        doc.setFont("helvetica", "normal");
        doc.setFontSize(8);

        // Reviewed by name
        doc.text(
          "QA Reviewer",
          signatureStartX + leftSectionWidth / 2,
          signatureY + signatureHeight / 2 + 2,
          { align: "center" }
        );

        // Approved by name
        doc.text(
          "Design Team",
          signatureStartX + leftSectionWidth + rightSectionWidth / 2,
          signatureY + signatureHeight / 2 + 2,
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
</style>
