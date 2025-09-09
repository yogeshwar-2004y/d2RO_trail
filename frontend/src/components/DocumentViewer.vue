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

      <!-- Comments Section -->
      <div class="comments-section" v-if="docContent && comments.length > 0">
        <div class="comments-header">
          <h3>Comments</h3>
          <span class="comment-count">{{ comments.length }} comments</span>
        </div>
        
        <div class="comments-list">
          <div v-for="comment in comments" 
               :key="comment.id" 
               class="comment-item"
               :class="{ 'comment-resolved': comment.status === 'accepted' }">
            <div class="comment-header">
              <div class="comment-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                </svg>
              </div>
              <div class="comment-info">
                <div class="comment-author">{{ comment.author }}</div>
                <div class="comment-meta">
                  <span class="comment-date">{{ formatDate(comment.date) }}</span>
                  <span class="comment-page" @click="scrollToPage(comment.page)">
                    Page {{ comment.page }}
                  </span>
                </div>
              </div>
              <div class="comment-status" v-if="comment.status" :class="'status-' + comment.status">
                {{ comment.status }}
              </div>
            </div>
            
            <div class="comment-content">
              {{ comment.content }}
            </div>
            
            <div class="comment-actions" v-if="!comment.status && (isDesigner || isDesignHead)">
              <button class="action-btn accept" @click="handleAccept(comment)">
                Accept
              </button>
              <button class="action-btn reject" @click="handleReject(comment)">
                Reject
              </button>
            </div>
            
            <div class="comment-response" v-if="comment.response">
              <div class="response-header">Response:</div>
              <div class="response-content">{{ comment.response }}</div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Reject Comment Modal -->
      <div class="modal" v-if="showRejectModal">
        <div class="modal-content">
          <h3>Reject Comment</h3>
          <textarea 
            v-model="rejectJustification"
            placeholder="Please provide justification for rejecting this comment"
            rows="4"
          ></textarea>
          <div class="modal-actions">
            <button @click="confirmReject">Submit</button>
            <button @click="cancelReject">Cancel</button>
          </div>
        </div>
      </div>
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
import { userStore } from '@/stores/userStore'

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
      comments: [
        {
          id: 1,
          author: 'John Smith (QA Reviewer)',
          date: '2025-09-08',
          page: 1,
          content: 'Section 3.2: The technical specifications for the power supply need to be updated according to the latest standards.',
          status: null,
          response: null
        },
        {
          id: 2,
          author: 'Sarah Wilson (QA Reviewer)',
          date: '2025-09-08',
          page: 2,
          content: 'The maintenance procedures need more detailed steps for troubleshooting common issues.',
          status: 'accepted',
          response: 'Updates will be made in the next revision'
        },
        {
          id: 3,
          author: 'Mike Johnson (QA Reviewer)',
          date: '2025-09-07',
          page: 4,
          content: 'The diagrams in this section need to be updated to match the current hardware configuration.',
          status: 'rejected',
          response: 'Current diagrams are correct according to the latest hardware specifications (Rev 2.1)'
        }
      ],
      showRejectModal: false,
      rejectJustification: '',
      selectedComment: null,
    }
  },
  
  computed: {
    // Get current user role from global store
    currentUserRole() {
      return userStore.getters.roleName() // Using roleName for string comparison
    },
    canUpload() {
      return this.currentUserRole === 'Design Head' || this.currentUserRole === 'Designer';
    },
    isDesigner() {
      return this.currentUserRole === 'Designer';
    },
    isDesignHead() {
      return this.currentUserRole === 'Design Head';
    },
    isQAHead() {
      return this.currentUserRole === 'QA Head';
    },
    isReviewer() {
      return this.currentUserRole === 'Reviewer';
    },
    docContent() {
      return (this.fileType === 'pdf' && this.pdfUrl) || (this.fileType === 'docx' && this.docxHtml);
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
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric'
      });
    },

    // Comment handling
    handleAccept(comment) {
      comment.status = 'accepted';
      comment.response = 'Comment accepted and changes will be implemented.';
      // TODO: Update on server
    },

    handleReject(comment) {
      this.selectedComment = comment;
      this.showRejectModal = true;
    },

    confirmReject() {
      if (this.selectedComment && this.rejectJustification) {
        this.selectedComment.status = 'rejected';
        this.selectedComment.response = this.rejectJustification;
        // TODO: Update on server
        this.cancelReject();
      }
    },

    cancelReject() {
      this.showRejectModal = false;
      this.rejectJustification = '';
      this.selectedComment = null;
    },

    scrollToPage(pageNum) {
      if (this.fileType === 'pdf' && this.$refs.pdfScroll && this.$refs.pdfPages) {
        const targetPage = this.$refs.pdfPages[pageNum - 1];
        if (targetPage && targetPage.$el) {
          targetPage.$el.scrollIntoView({ behavior: 'smooth' });
        }
      }
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
      console.log('Starting DOCX file loading...', { fileName: file.name, fileSize: file.size });
      
      try {
        console.log('Reading file as ArrayBuffer...');
        const arrayBuffer = await file.arrayBuffer();
        console.log('File successfully read as ArrayBuffer');

        console.log('Converting DOCX to HTML with page markers...');
        const options = {
          styleMap: [
            "p[style-name='Page Break'] => div.page-break"
          ]
        };

        // First convert to get the basic HTML
        const result = await mammoth.convertToHtml({ arrayBuffer }, options);
        console.log('Initial HTML conversion complete', { 
          resultLength: result.value.length,
          messages: result.messages 
        });

        // Process the HTML to add page markers
        const processedHtml = this.processDocxHtml(result.value);
        console.log('HTML processing complete', { 
          finalLength: processedHtml.length,
          pageCount: (processedHtml.match(/<div class="page"/g) || []).length 
        });

        // Set the processed HTML
        this.docxHtml = processedHtml;
        
        // Calculate number of pages
        this.$nextTick(() => {
          const pages = document.querySelectorAll('.docx-content .page');
          this.numPages = pages.length || 1;
          console.log('Page calculation complete', { totalPages: this.numPages });
        });

      } catch (err) {
        console.error('Error in loadDocx:', {
          error: err,
          errorName: err.name,
          errorMessage: err.message,
          errorStack: err.stack
        });
        alert("Failed to render DOCX file. Check console for details.");
      }
    },

    processDocxHtml(html) {
      console.log('Processing DOCX HTML...');
      try {
        // Create a temporary container
        const temp = document.createElement('div');
        temp.innerHTML = html;
        
        // Get approximate content per page (A4 size)
        const CHARS_PER_PAGE = 3000; // Rough estimate of characters per page
        const totalContent = temp.textContent;
        const estimatedPages = Math.max(Math.ceil(totalContent.length / CHARS_PER_PAGE), 1);
        console.log('Estimated pages:', { 
          totalChars: totalContent.length, 
          estimatedPages 
        });

        // Initialize result container
        const result = document.createElement('div');
        let pageCount = 0;
        let currentPage = null;
        let currentChars = 0;

        function startNewPage() {
          if (currentPage && currentPage.children.length > 0) {
            result.appendChild(currentPage);
          }
          pageCount++;
          currentPage = document.createElement('div');
          currentPage.className = 'page';
          currentPage.setAttribute('data-page', pageCount.toString());
          currentChars = 0;
        }

        // Start first page
        startNewPage();

        // Process each element
        const elements = Array.from(temp.children);
        console.log('Processing elements:', { totalElements: elements.length });

        elements.forEach((element, index) => {
          // Check for explicit page breaks
          const style = window.getComputedStyle(element);
          const hasPageBreak = style.pageBreakBefore === 'always' || 
                              style.pageBreakAfter === 'always' ||
                              element.tagName === 'HR';

          // Force a new page on headings for better content organization
          const isHeading = /^H[1-6]$/.test(element.tagName);
          const elementContent = element.textContent;
          
          // Start new page if:
          // 1. There's an explicit page break, or
          // 2. Current page has enough content and we're at a good break point, or
          // 3. We're at a heading and current page has some content
          if (hasPageBreak || 
              (currentChars > CHARS_PER_PAGE && (isHeading || element.tagName === 'P')) ||
              (isHeading && currentChars > CHARS_PER_PAGE * 0.5)) {
            startNewPage();
          }

          // Add element to current page
          currentPage.appendChild(element.cloneNode(true));
          currentChars += elementContent.length;
        });

        // Append the last page
        if (currentPage && currentPage.children.length > 0) {
          result.appendChild(currentPage);
        }

        console.log('HTML processing complete', { 
          actualPages: pageCount,
          estimatedPages,
          finalHtmlLength: result.innerHTML.length 
        });

        // Add page numbers
        result.querySelectorAll('.page').forEach((page, index) => {
          const pageNum = document.createElement('div');
          pageNum.className = 'page-number';
          pageNum.textContent = `Page ${index + 1} of ${pageCount}`;
          page.appendChild(pageNum);
        });

        return result.innerHTML;
      } catch (err) {
        console.error('Error in processDocxHtml:', {
          error: err,
          errorName: err.name,
          errorMessage: err.message,
          errorStack: err.stack
        });
        // Return original HTML if processing fails
        return html;
      }
    },

    shouldStartNewPage(pageDiv) {
      // Estimate if current page content exceeds A4 height
      const ESTIMATED_PAGE_HEIGHT = 1056; // A4 height in pixels at 96 DPI
      return pageDiv.offsetHeight > ESTIMATED_PAGE_HEIGHT;
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
      console.log('Attempting to scroll to page:', pageNum, { fileType: this.fileType });
      
      this.$nextTick(() => {
        if (this.fileType === 'pdf' && this.$refs.pdfPages) {
          const pageEl = this.$refs.pdfPages[pageNum - 1]?.$el;
          if (pageEl) {
            console.log('Scrolling to PDF page element:', pageEl);
            pageEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
          } else {
            console.warn('PDF page element not found:', { pageNum, totalPages: this.numPages });
          }
        } else if (this.fileType === 'docx') {
          const docContainer = document.querySelector('.docx-content');
          if (docContainer) {
            const targetPage = docContainer.querySelector(`.page[data-page="${pageNum}"]`);
            if (targetPage) {
              console.log('Scrolling to DOCX page element:', targetPage);
              targetPage.scrollIntoView({ behavior: 'smooth', block: 'start' });
            } else {
              console.warn('DOCX page element not found:', { pageNum, totalPages: this.numPages });
            }
          } else {
            console.warn('DOCX container not found');
          }
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
  justify-content: center; /* Center the items horizontally */
  align-items: center;     /* Align items vertically in the center */
  gap: 1rem;               /* Space between buttons */
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
  text-align: center;
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
  
  /* Center horizontally */
  display: block;
  margin: 0 auto;
  text-align: center;
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
  gap: 1rem;
  padding: 1rem;
}

.document-area {
  flex: 3; /* Takes up 3 parts of the 5 total parts */
  display: flex;
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  min-width: 0; /* Prevents flex child from overflowing */
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
  padding: 1rem;
  width: 100%;
  max-width: 100%;
  background: #f8fafc;
}

.docx-content .page {
  background: white;
  padding: 2rem;
  margin: 1rem auto;
  max-width: 816px; /* A4 width at 96 DPI */
  min-height: 1056px; /* A4 height at 96 DPI */
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  position: relative;
}

.docx-content .page::after {
  content: attr(data-page);
  position: absolute;
  bottom: 0.5rem;
  right: 0.5rem;
  font-size: 0.75rem;
  color: #6b7280;
  background: #f3f4f6;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.docx-content h1,
.docx-content h2,
.docx-content h3 {
  margin: 1.5rem 0 0.75rem;
  color: #111;
}

.docx-content h1 {
  font-size: 1.875rem;
  font-weight: 600;
}

.docx-content h2 {
  font-size: 1.5rem;
  font-weight: 600;
}

.docx-content h3 {
  font-size: 1.25rem;
  font-weight: 600;
}

.docx-content p {
  margin: 0.75rem 0;
  line-height: 1.6;
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
  background: #ffffff;
  border-radius: 12px;
  padding: 1.25rem;
  transition: all 0.2s ease;
  border: 1px solid #e5e7eb;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
}

.comment-item:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
  transform: translateY(-1px);
}

.comment-text {
  flex: 1;
  color: #1f2937;
  font-size: 0.95rem;
  line-height: 1.6;
  margin-bottom: 0.75rem;
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

/* Comments Section Styles */
.comments-section {
  flex: 2; /* Takes up 2 parts of the 5 total parts */
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  overflow-y: auto;
  padding: 1.75rem;
  min-width: 0; /* Prevents flex child from overflowing */
  max-height: calc(100vh - 200px); /* Accounts for header and controls */
  position: relative;
}

.comments-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(to right, #3b82f6, #10b981);
  border-radius: 16px 16px 0 0;
}

.comments-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1.25rem;
  border-bottom: 2px solid #f3f4f6;
  position: relative;
}

.comments-header h3 {
  margin: 0;
  font-size: 1.35rem;
  font-weight: 600;
  color: #111827;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  letter-spacing: -0.025em;
}

.comments-header h3::before {
  content: '';
  display: block;
  width: 4px;
  height: 24px;
  background: #3b82f6;
  border-radius: 4px;
}

.comment-count {
  background: linear-gradient(to right, #dbeafe, #e0f2fe);
  color: #1e40af;
  font-size: 0.875rem;
  font-weight: 600;
  padding: 0.35rem 1rem;
  border-radius: 9999px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.comment-item {
  background: #f9fafb;
  border-radius: 8px;
  padding: 1rem;
  transition: all 0.2s ease;
}

.comment-item:hover {
  background: #f3f4f6;
}

.comment-item.comment-resolved {
  border-left: 4px solid #10b981;
}

.comment-header {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.comment-icon {
  flex-shrink: 0;
  color: #6b7280;
}

.comment-info {
  flex: 1;
}

.comment-author {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.comment-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.85rem;
  color: #6b7280;
}

.comment-page {
  cursor: pointer;
  text-decoration: underline;
}

.comment-status {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
}

.status-accepted {
  background: #d1fae5;
  color: #059669;
}

.status-rejected {
  background: #fee2e2;
  color: #dc2626;
}

.comment-content {
  color: #1f2937;
  margin-bottom: 1rem;
  line-height: 1.5;
}

.comment-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  padding: 0.4rem 1rem;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: opacity 0.2s;
}

.action-btn:hover {
  opacity: 0.9;
}

.action-btn.accept {
  background: #10b981;
  color: white;
}

.action-btn.reject {
  background: #ef4444;
  color: white;
}

.comment-response {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}

.response-header {
  font-weight: 500;
  color: #4b5563;
  margin-bottom: 0.5rem;
}

.response-content {
  color: #6b7280;
  font-size: 0.95rem;
  line-height: 1.5;
}

/* Reject Comment Modal */
.modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  width: 90%;
  max-width: 500px;
  animation: fadeIn 0.3s ease;
}

.modal-content h3 {
  margin: 0 0 1rem 0;
}

.modal-content textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  resize: vertical;
  margin-bottom: 1rem;
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

/* Comments Section Styles */
.comments-section {
  background: #fff;
  border-left: 1px solid #e5e7eb;
  width: 360px;
  height: 100%;
  overflow-y: auto;
  padding: 1rem;
}

.comments-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.comments-header h3 {
  margin: 0;
  font-size: 1.1rem;
}

.comment-count {
  color: #6b7280;
  font-size: 0.9rem;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.comment-item {
  background: #f9fafb;
  border-radius: 8px;
  padding: 1rem;
  transition: all 0.2s ease;
}

.comment-item:hover {
  background: #f3f4f6;
}

.comment-item.comment-resolved {
  border-left: 4px solid #10b981;
}

.comment-header {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.comment-icon {
  flex-shrink: 0;
  color: #6b7280;
}

.comment-info {
  flex: 1;
}

.comment-author {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.comment-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.85rem;
  color: #6b7280;
}

.comment-page {
  cursor: pointer;
  text-decoration: underline;
}

.comment-status {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
}

.status-accepted {
  background: #d1fae5;
  color: #059669;
}

.status-rejected {
  background: #fee2e2;
  color: #dc2626;
}

.comment-content {
  color: #1f2937;
  margin-bottom: 1rem;
  line-height: 1.5;
}

.comment-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  padding: 0.4rem 1rem;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: opacity 0.2s;
}

.action-btn:hover {
  opacity: 0.9;
}

.action-btn.accept {
  background: #10b981;
  color: white;
}

.action-btn.reject {
  background: #ef4444;
  color: white;
}

.comment-response {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}

.response-header {
  font-weight: 500;
  color: #4b5563;
  margin-bottom: 0.5rem;
}

.response-content {
  color: #6b7280;
  font-size: 0.95rem;
  line-height: 1.5;
}

/* Reject Comment Modal */
.modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  width: 90%;
  max-width: 500px;
  animation: fadeIn 0.3s ease;
}

.modal-content h3 {
  margin: 0 0 1rem 0;
}

.modal-content textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  resize: vertical;
  margin-bottom: 1rem;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

.modal-actions button {
  padding: 0.5rem 1.25rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  border: none;
}

.modal-actions button:first-child {
  background: #ef4444;
  color: white;
}

.modal-actions button:last-child {
  background: #e5e7eb;
  color: #1f2937;
}

</style>