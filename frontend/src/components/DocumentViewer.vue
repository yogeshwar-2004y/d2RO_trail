<template>
  <div class="pdf-viewer-container">
    <!-- Header with document info -->
    <div class="document-header">
      <div class="header-info">
        <h2>{{ lruName || 'Document Viewer' }}</h2>
        <div class="meta-info">
          <span><strong>Project:</strong> {{ projectName || 'N/A' }}</span>
          <span><strong>Document ID:</strong> {{ documentId || 'N/A' }}</span>
          <span><strong>Status:</strong> <span :class="'status-' + (status || 'pending')">{{ status || 'Pending' }}</span></span>
           <!-- <span><strong>Status:</strong> <span :class="getStatusClass(status)">{{ status || 'Pending' }}</span></span> -->
          <span><strong>Created:</strong> {{ formatDate(createdDate) }}</span>
          <span><strong>Modified:</strong> {{ formatDate(lastModifiedDate) }}</span>
        </div>
      </div>
    </div>

    <!-- Action Bar based on user role -->
    <div class="action-bar" v-if="currentUserRole">
      <!-- QA Head Actions -->
      <template v-if="currentUserRole === 'QA Head'">
        <button @click="assignReviewer" class="action-btn">
          Assign Reviewer
        </button>
        <button @click="viewObservations" class="action-btn">
          View Observations
        </button>
        <button @click="trackVersions" class="action-btn">
          Track Versions
        </button>
      </template>

      <!-- Design Head / Designer Actions -->
      <template v-if="currentUserRole === 'Design Head' || currentUserRole === 'Designer'">
        <label for="file-upload" class="upload-btn">
          Upload Document
          <input 
            id="file-upload"
            type="file" 
            accept=".pdf,.docx" 
            @change="handleFileUpload"
            style="display: none"
          />
        </label>
      </template>

      <!-- Admin and QA Reviewer don't need action buttons -->
    </div>

    <!-- Control Bar (shown when document is loaded) -->
    <div class="control-bar" v-if="fileType">
      <div class="controls-left">
        <button @click="zoomOut" class="control-btn">-</button>
        <span class="zoom-level">{{ (zoom * 100).toFixed(0) }}%</span>
        <button @click="zoomIn" class="control-btn">+</button>

        <template v-if="fileType === 'pdf'">
          <button @click="prevPage" :disabled="page <= 1" class="control-btn">← Prev</button>
          <span class="page-info">
            Page 
            <input
              type="number"
              v-model.number="page"
              @keyup.enter="goToPage"
              min="1"
              :max="numPages"
              class="page-input"
            />
            of {{ numPages }}
          </span>
          <button @click="nextPage" :disabled="page >= numPages" class="control-btn">Next →</button>
        </template>
      </div>
      <div class="controls-right">
        <span class="file-name">{{ fileName }}</span>
      </div>
    </div>

    <!-- Main Content Area -->
    <div class="content">
      <!-- Document Container -->
      <div class="document-area">
        <!-- PDF Viewer -->
        <div
          v-if="fileType === 'pdf' && pdfUrl"
          class="doc-container"
          ref="pdfScroll"
          @scroll="onScroll"
        >
          <vue-pdf-embed
            v-for="p in numPages"
            :key="p"
            :source="pdfUrl"
            :page="p"
            :scale="zoom"
            ref="pdfPages"
            class="pdf-page"
          />
        </div>

        <!-- DOCX Viewer -->
        <div
          v-if="fileType === 'docx'"
          v-html="docxHtml"
          class="doc-container docx-content"
          :style="{ fontSize: zoom * 16 + 'px' }"
        ></div>

        <!-- Empty state -->
        <div v-if="!fileType" class="empty-state">
          <div class="empty-icon">📄</div>
          <p class="empty-msg">No document present</p>
          <p class="empty-sub" v-if="canUpload">Please upload a PDF or DOCX file</p>
        </div>
      </div>

      <!-- Simplified Comments Sidebar -->
      <aside class="sidebar">
        <h3>Comments</h3>
        <div class="comments-container">
          <ul class="comments-list" v-if="comments.length > 0">
            <li v-for="(comment, index) in comments" :key="index" class="comment-item">
              <span class="comment-text">{{ comment }}</span>
              <button @click="removeComment(index)" class="remove-btn">×</button>
            </li>
          </ul>
          <p v-else class="no-comments">No comments yet</p>
        </div>
        <div class="add-comment">
          <input
            type="text"
            v-model="newComment"
            placeholder="Add a comment..."
            @keyup.enter="addComment"
            class="comment-input"
          />
          <button @click="addComment" class="comment-btn">Add</button>
        </div>
      </aside>
    </div>

    <!-- Assign Reviewer Modal -->
    <QAHeadAssignReviewer 
      v-if="showAssignReviewerModal"
      :lruName="lruName"
      :projectName="projectName"
      @close="showAssignReviewerModal = false"
    />

    <!-- Track Versions Modal -->
    <div v-if="showTrackVersionsModal" class="track-versions-overlay" @click="closeTrackVersionsModal">
      <div class="track-versions-modal" @click.stop>
        <div class="modal-header">
          <h2>TRACK VERSIONS</h2>
          <button class="close-button" @click="closeTrackVersionsModal">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        
        <div class="modal-content">
          <div class="versions-list">
            <div 
              v-for="version in documentVersions" 
              :key="version.id"
              class="version-item"
              :class="{ 
                'disabled': version.deleted,
                'favorite': version.isFavorite 
              }"
              @click="version.deleted ? null : selectVersion(version)"
            >
              <div class="version-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path>
                  <rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect>
                </svg>
              </div>
              
              <div class="version-info">
                <span class="version-id">{{ version.projectId }} {{ version.version }}</span>
                <span class="version-date">{{ version.date }}</span>
              </div>
              
              <div class="version-actions">
                <button 
                  class="star-button"
                  :class="{ 'starred': version.isFavorite }"
                  @click.stop="toggleFavorite(version)"
                  :disabled="version.deleted"
                >
                  <svg v-if="version.isFavorite" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
                  </svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
                  </svg>
                </button>
                
                <button 
                  class="delete-button"
                  @click.stop="confirmDeleteVersion(version)"
                  :disabled="version.deleted"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="3,6 5,6 21,6"></polyline>
                    <path d="M19,6v14a2,2,0,0,1-2,2H7a2,2,0,0,1-2-2V6m3,0V4a2,2,0,0,1,2-2h4a2,2,0,0,1,2,2V6"></path>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteConfirmModal" class="delete-confirm-overlay" @click="closeDeleteConfirmModal">
      <div class="delete-confirm-modal" @click.stop>
        <div class="modal-header">
          <h3>Confirm Deletion</h3>
          <button class="close-button" @click="closeDeleteConfirmModal">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        
        <div class="modal-content">
          <div class="confirm-message">
            <div class="warning-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                <line x1="12" y1="9" x2="12" y2="13"></line>
                <line x1="12" y1="17" x2="12.01" y2="17"></line>
              </svg>
            </div>
            <h4>Are you sure you want to delete this version?</h4>
            <p>Version: <strong>{{ versionToDelete?.projectId }} {{ versionToDelete?.version }}</strong></p>
            <p class="warning-text">This action cannot be undone. The version will be marked as deleted and will no longer be accessible.</p>
          </div>
          
          <div class="modal-actions">
            <button @click="closeDeleteConfirmModal" class="btn btn-secondary">Cancel</button>
            <button @click="deleteVersion" class="btn btn-danger">Delete Version</button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import VuePdfEmbed from "vue-pdf-embed"
import * as mammoth from "mammoth/mammoth.browser"
import * as pdfjsLib from "pdfjs-dist/legacy/build/pdf"

// Configure pdf.js worker
import pdfjsWorker from "pdfjs-dist/legacy/build/pdf.worker?url"
pdfjsLib.GlobalWorkerOptions.workerSrc = pdfjsWorker

import QAHeadAssignReviewer from "@/views/qahead/QAHeadAssignReviewer.vue"

export default {
  components: { VuePdfEmbed, QAHeadAssignReviewer },
  data() {
    return {
      // Document metadata
      lruName: "LRU-2024-001",
      projectName: "Project Alpha",
      documentId: "DOC-001",
      status: "pending", // pending, approved, rejected, review
      createdDate: new Date('2024-01-15'),
      lastModifiedDate: new Date(),
      
      // User role - this would come from your auth system
      currentUserRole: "QA Head", // "QA Head", "Design Head", "Designer", "Admin", "QA Reviewer"
      
      // Document viewing
      fileType: null,
      pdfUrl: null,
      docxHtml: "",
      page: 1,
      numPages: 0,
      zoom: 1.0,
      fileName: "",

      showAssignReviewerModal: false,
      showTrackVersionsModal: false,
      showDeleteConfirmModal: false,
      versionToDelete: null,
      documentVersions: [
        { 
          id: 1, 
          projectId: 'PRJ-2025-078', 
          version: 'A', 
          date: '2025-01-15', 
          isFavorite: true, 
          deleted: false 
        },
        { 
          id: 2, 
          projectId: 'PRJ-2025-078', 
          version: 'B', 
          date: '2025-01-20', 
          isFavorite: false, 
          deleted: false 
        },
        { 
          id: 3, 
          projectId: 'PRJ-2025-078', 
          version: 'C', 
          date: '2025-01-25', 
          isFavorite: false, 
          deleted: false 
        },
        { 
          id: 4, 
          projectId: 'PRJ-2025-078', 
          version: 'D', 
          date: '2025-01-30', 
          isFavorite: true, 
          deleted: false 
        }
      ],
      
      // Comments
      comments: [],
      newComment: "",
    }
  },
  
  computed: {
    canUpload() {
      return this.currentUserRole === 'Design Head' || this.currentUserRole === 'Designer';
    }
  },
  
  mounted() {
    const { lruId, documentId, projectId } = this.$route.params;
    console.log('Document Viewer initialized:', { lruId, documentId, projectId });
    
    // Load document metadata from server
    // this.loadDocumentMetadata(documentId);
    
    // Load existing document if available
    // this.loadDocumentFromServer(documentId);
  },
  
  methods: {
    // Date formatting
    formatDate(date) {
      if (!date) return 'N/A';
      return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    },

    assignReviewer() {
      this.showAssignReviewerModal = true;
    },
    viewObservations() {
      this.$router.push({ 
        name: 'ObservationReport', 
        params: { 
          lruName: this.lruName,
          projectName: this.projectName
        } 
      });
    },
    trackVersions() {
      this.showTrackVersionsModal = true;
    },
    closeTrackVersionsModal() {
      this.showTrackVersionsModal = false;
    },
    selectVersion(version) {
      console.log('Selected version:', version);
      // Navigate to the document version view page
      this.$router.push({
        name: 'QAHeadDocumentVersionView',
        params: {
          projectName: this.projectName,
          lruName: this.lruName,
          versionId: `${version.projectId}-${version.version}`
        }
      });
    },
    toggleFavorite(version) {
      version.isFavorite = !version.isFavorite;
    },
    confirmDeleteVersion(version) {
      this.versionToDelete = version;
      this.showDeleteConfirmModal = true;
    },
    closeDeleteConfirmModal() {
      this.showDeleteConfirmModal = false;
      this.versionToDelete = null;
    },
    deleteVersion() {
      if (this.versionToDelete) {
        this.versionToDelete.deleted = true;
        this.closeDeleteConfirmModal();
      }
    },
    getStatusClass(status) {
      const statusMap = {
        'Under Review': 'status-under-review',
        'Approved': 'status-approved',
        'Rejected': 'status-rejected',
        'Pending': 'status-pending'
      };
      return statusMap[status] || 'status-default';
    },
    
    // File handling
    handleFileUpload(event) {
      const file = event.target.files?.[0];
      if (!file) return;

      this.fileName = file.name;
      this.clearDocument();

      const fileType = file.type;
      if (fileType === "application/pdf") {
        this.fileType = "pdf";
        this.loadPdf(file);
      } else if (
        fileType === "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
      ) {
        this.fileType = "docx";
        this.loadDocx(file);
      } else {
        alert("Unsupported file type. Please upload a PDF or DOCX file.");
      }
      
      // Update modified date
      this.lastModifiedDate = new Date();
    },

    async loadPdf(file) {
      if (this.pdfUrl) {
        URL.revokeObjectURL(this.pdfUrl);
      }
      this.pdfUrl = URL.createObjectURL(file);
      this.page = 1;

      try {
        const loadingTask = pdfjsLib.getDocument(this.pdfUrl);
        const pdf = await loadingTask.promise;
        this.numPages = pdf.numPages;
      } catch (err) {
        console.error("Failed to load PDF metadata", err);
        alert("Failed to load PDF file.");
      }
    },

    async loadDocx(file) {
      try {
        const arrayBuffer = await file.arrayBuffer();
        const result = await mammoth.convertToHtml({ arrayBuffer });
        this.docxHtml = result.value;
      } catch (err) {
        alert("Failed to render DOCX file.");
        console.error(err);
      }
    },

    // Zoom controls
    zoomIn() {
      if (this.zoom < 2.0) this.zoom += 0.1;
    },
    
    zoomOut() {
      if (this.zoom > 0.3) this.zoom -= 0.1;
    },

    // Page navigation
    goToPage() {
      if (this.page >= 1 && this.page <= this.numPages) {
        this.scrollToPage(this.page);
      } else {
        alert(`Please enter a page between 1 and ${this.numPages}`);
      }
    },
    
    nextPage() {
      if (this.page < this.numPages) {
        this.page++;
        this.scrollToPage(this.page);
      }
    },
    
    prevPage() {
      if (this.page > 1) {
        this.page--;
        this.scrollToPage(this.page);
      }
    },

    scrollToPage(pageNum) {
      this.$nextTick(() => {
        const pageEl = this.$refs.pdfPages?.[pageNum - 1]?.$el;
        if (pageEl) {
          pageEl.scrollIntoView({ behavior: "smooth", block: "start" });
        }
      });
    },

    onScroll() {
      if (this.fileType !== "pdf" || !this.$refs.pdfPages?.length) return;

      let currentPage = 1;
      const containerTop = this.$refs.pdfScroll.scrollTop;

      this.$refs.pdfPages.forEach((page, idx) => {
        const el = page.$el;
        const offset = el.offsetTop - containerTop;
        if (offset <= 50) {
          currentPage = idx + 1;
        }
      });

      this.page = currentPage;
    },

    // Comments
    addComment() {
      if (this.newComment.trim()) {
        this.comments.push(this.newComment.trim());
        this.newComment = "";
      }
    },
    
    removeComment(index) {
      this.comments.splice(index, 1);
    },

    // Cleanup
    clearDocument() {
      if (this.pdfUrl) {
        URL.revokeObjectURL(this.pdfUrl);
      }
      this.pdfUrl = null;
      this.docxHtml = "";
      this.page = 1;
      this.numPages = 0;
      this.zoom = 1.0;
      this.fileType = null;
    },
  },
  
  beforeUnmount() {
    if (this.pdfUrl) {
      URL.revokeObjectURL(this.pdfUrl);
    }
  },
}
</script>

<style scoped>
.pdf-viewer-container {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f5f5;
}

/* Header Section */
.document-header {
  background: white;
  border-bottom: 1px solid #e0e0e0;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.header-info h2 {
  margin: 0 0 0.75rem 0;
  color: #333;
  font-size: 1.5rem;
}

.meta-info {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
  color: #666;
  font-size: 0.9rem;
}

.meta-info strong {
  color: #444;
  margin-right: 0.5rem;
}

.status-pending { color: #f59e0b; }
.status-approved { color: #10b981; }
.status-rejected { color: #ef4444; }
.status-review { color: #3b82f6; }

/* Action Bar */
.action-bar {
  background: white;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  gap: 1rem;
}

.action-btn {
  padding: 0.5rem 1rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background 0.2s;
}

.action-btn:hover {
  background: #2563eb;
}

.upload-btn {
  display: inline-block;
  padding: 0.5rem 1rem;
  background: #10b981;
  color: white;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background 0.2s;
}

.upload-btn:hover {
  background: #059669;
}

/* Control Bar */
.control-bar {
  background: #fafafa;
  border-bottom: 1px solid #e0e0e0;
  padding: 0.75rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.controls-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.control-btn {
  padding: 0.25rem 0.75rem;
  background: white;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.control-btn:hover:not(:disabled) {
  background: #f3f4f6;
}

.control-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.zoom-level {
  font-weight: 500;
  color: #4b5563;
  min-width: 50px;
  text-align: center;
}

.page-info {
  color: #4b5563;
  font-size: 0.9rem;
}

.page-input {
  width: 50px;
  padding: 0.25rem;
  margin: 0 0.25rem;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  text-align: center;
}

.file-name {
  color: #6b7280;
  font-size: 0.9rem;
  font-weight: 500;
}

/* Main Content */
.content {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.document-area {
  flex: 1;
  display: flex;
  background: white;
  margin: 1rem;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.doc-container {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
  background: white;
}

.pdf-page {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid #e0e0e0;
  margin-bottom: 1.5rem;
  background: white;
}

.docx-content {
  line-height: 1.6;
  color: #333;
}

.docx-content h1,
.docx-content h2,
.docx-content h3 {
  margin: 1.5rem 0 0.75rem;
  color: #111;
}

.docx-content p {
  margin: 0.75rem 0;
}

/* Empty State */
.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.3;
}

.empty-msg {
  font-size: 1.25rem;
  color: #4b5563;
  margin: 0;
}

.empty-sub {
  font-size: 1rem;
  color: #9ca3af;
  margin-top: 0.5rem;
}

/* Sidebar */
.sidebar {
  width: 300px;
  background: white;
  margin: 1rem 1rem 1rem 0;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
}

.sidebar h3 {
  margin: 0 0 1rem 0;
  color: #333;
  font-size: 1.1rem;
}

.comments-container {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 1rem;
}

.comments-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.comment-item {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 0.75rem;
  margin-bottom: 0.5rem;
  display: flex;
  justify-content: space-between;
  align-items: start;
}

.comment-text {
  flex: 1;
  color: #4b5563;
  font-size: 0.9rem;
  line-height: 1.4;
}

.remove-btn {
  background: transparent;
  border: none;
  color: #ef4444;
  cursor: pointer;
  font-size: 1.25rem;
  line-height: 1;
  padding: 0;
  margin-left: 0.5rem;
  opacity: 0.6;
  transition: opacity 0.2s;
}

.remove-btn:hover {
  opacity: 1;
}

.no-comments {
  color: #9ca3af;
  font-size: 0.9rem;
  text-align: center;
  padding: 2rem 0;
}

.add-comment {
  display: flex;
  gap: 0.5rem;
}

.comment-input {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.9rem;
}

.comment-input:focus {
  outline: none;
  border-color: #3b82f6;
}

.comment-btn {
  padding: 0.5rem 1rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background 0.2s;
}

.comment-btn:hover {
  background: #2563eb;
}

/* Overlay for track versions modal */
.track-versions-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

/* Modal box */
.track-versions-modal {
  background: #fff;
  border-radius: 10px;
  width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 8px 20px rgba(0,0,0,0.25);
  animation: fadeIn 0.2s ease-in-out;
}

/* Modal header */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #eee;
}

.modal-header h2, .modal-header h3 {
  margin: 0;
  font-size: 1.3rem;
  font-weight: bold;
}

.close-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  transition: transform 0.2s ease;
}
.close-button:hover {
  transform: rotate(90deg);
}

/* Content area */
.modal-content {
  padding: 1rem 1.5rem;
}

.versions-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Version card style */
.version-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #f9fafb;
  padding: 0.9rem 1rem;
  border-radius: 8px;
  border-left: 4px solid transparent;
  transition: all 0.2s ease-in-out;
  cursor: pointer;
}

.version-item:hover {
  background: #f3f4f6;
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}

/* Active favorite */
.version-item.favorite {
  border-left: 4px solid #f59e0b; /* yellow accent */
  background: #fffbea;
}

/* Deleted (disabled) style */
.version-item.disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background: #f1f1f1;
}

/* Left section: icon + text */
.version-icon {
  margin-right: 12px;
  flex-shrink: 0;
}

.version-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.version-id {
  font-weight: 600;
  font-size: 0.95rem;
}
.version-date {
  font-size: 0.8rem;
  color: #666;
}

/* Right section: star + delete */
.version-actions {
  display: flex;
  gap: 0.8rem;
  align-items: center;
}

.star-button, .delete-button {
  background: none;
  border: none;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.star-button:hover, .delete-button:hover {
  transform: scale(1.2);
}

/* Star styles */
.star-button svg {
  stroke: #888;
  fill: none;
}
.star-button.starred svg {
  stroke: #f59e0b;
  fill: #f59e0b;
}

/* Delete styles */
.delete-button svg {
  stroke: #d33;
}

/* Delete confirmation modal */
.delete-confirm-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.delete-confirm-modal {
  background: #fff;
  border-radius: 8px;
  width: 450px;
  padding: 1rem 1.5rem;
  box-shadow: 0 8px 20px rgba(0,0,0,0.25);
}

.confirm-message {
  text-align: center;
  padding: 1rem;
}

.warning-icon {
  color: #e63946;
  margin-bottom: 1rem;
}

.warning-text {
  color: #d33;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.8rem;
  margin-top: 1.5rem;
}

.btn {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
}

.btn-secondary {
  background: #e5e7eb;
  border: none;
}
.btn-danger {
  background: #dc2626;
  color: #fff;
  border: none;
}
.btn:hover {
  opacity: 0.9;
}

/* Smooth modal animation */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

</style>