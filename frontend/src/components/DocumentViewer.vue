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
        <div class="upload-section">
          <label for="file-upload" class="upload-btn">
            Choose Document
            <input 
              id="file-upload"
              type="file" 
              accept=".pdf,.docx,.doc,.txt,.xlsx,.xls" 
              @change="handleFileSelect"
              style="display: none"
            />
          </label>
          
          <!-- Document Details Form - Show when file is selected -->
          <div v-if="selectedFile" class="document-form">
            <div class="form-row">
              <div class="form-group">
                <label>Document Number:</label>
                <input 
                  type="text" 
                  v-model="documentDetails.documentNumber" 
                  placeholder="e.g., DOC-001"
                  class="form-input"
                  required
                />
              </div>
              <div class="form-group">
                <label>Version:</label>
                <input 
                  type="text" 
                  v-model="documentDetails.version" 
                  placeholder="e.g., v1.0"
                  class="form-input"
                  required
                />
              </div>
              <div class="form-group">
                <label>Revision:</label>
                <input 
                  type="text" 
                  v-model="documentDetails.revision" 
                  placeholder="e.g., A"
                  class="form-input"
                  required
                />
              </div>
            </div>
            <button 
              @click="submitDocument" 
              class="submit-btn"
              :disabled="isUploading || !isFormValid"
            >
              {{ isUploading ? 'Uploading...' : 'Submit Document' }}
            </button>
          </div>
        </div>
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
      <!-- Left Panel: Existing Documents List -->
      <div class="documents-list-panel">
        <h3>Uploaded Document Versions</h3>
        <div class="documents-container">
          <div v-if="loading" class="loading-state">
            <p>Loading documents...</p>
          </div>
          <div v-else-if="existingDocuments.length === 0" class="no-documents">
            <div class="no-docs-icon">📋</div>
            <p>No documents uploaded yet</p>
          </div>
          <div v-else class="documents-list">
            <div 
              v-for="doc in existingDocuments" 
              :key="doc.document_id"
              class="document-item"
              @click="viewDocument(doc)"
            >
              <div class="doc-icon">
                <span v-if="doc.file_path.toLowerCase().includes('.pdf')">📄</span>
                <span v-else-if="doc.file_path.toLowerCase().includes('.docx')">📝</span>
                <span v-else>📄</span>
              </div>
              <div class="doc-info">
                <div class="doc-title">{{ doc.document_number }}</div>
                <div class="doc-meta">
                  <span class="doc-version">{{ doc.version }} ({{ doc.revision }})</span>
                  <span class="doc-ver">v{{ doc.doc_ver }}</span>
                </div>
                <div class="doc-details">
                  <span class="uploaded-by">{{ doc.uploaded_by_name }}</span>
                  <span class="upload-date">{{ formatDate(doc.upload_date) }}</span>
                </div>
                <div class="doc-status" :class="'status-' + doc.status.replace(' ', '-')">
                  {{ doc.status }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Panel: Document Viewer -->
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
          <p class="empty-msg">Select a document to view</p>
          <p class="empty-sub" v-if="canUpload">Or upload a new PDF or DOCX file</p>
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
import * as pdfjsLib from "pdfjs-dist/build/pdf"

// Configure pdf.js worker
import pdfjsWorker from "pdfjs-dist/build/pdf.worker?url"
pdfjsLib.GlobalWorkerOptions.workerSrc = pdfjsWorker

import QAHeadAssignReviewer from "@/views/qahead/QAHeadAssignReviewer.vue"
import { userStore } from '@/stores/userStore'

export default {
  components: { VuePdfEmbed, QAHeadAssignReviewer },
  data() {
    return {
      // Document metadata - will be loaded dynamically
      lruName: "",
      projectName: "",
      documentId: "",
      status: "pending", // pending, approved, rejected, review
      createdDate: null,
      lastModifiedDate: new Date(),
      
      // User role - from user store
      currentUserRole: userStore.getters.roleName() || "Guest",
      
      // Document viewing
      fileType: null,
      pdfUrl: null,
      docxHtml: "",
      page: 1,
      numPages: 0,
      zoom: 1.0,
      fileName: "",
      
      // File upload
      selectedFile: null,
      isUploading: false,
      documentDetails: {
        lruId: 1,
        documentNumber: "",
        version: "",
        revision: "",
        docVer: 1
      },

      showAssignReviewerModal: false,
      showTrackVersionsModal: false,
      showDeleteConfirmModal: false,
      versionToDelete: null,
      documentVersions: [], // Will be loaded dynamically
      existingDocuments: [], // List of uploaded documents for this LRU
      loading: false, // Loading state for documents
      
      // Comments
      comments: [],
      newComment: "",
    }
  },
  
  computed: {
    canUpload() {
      return this.currentUserRole === 'Design Head' || this.currentUserRole === 'Designer';
    },
    
    isFormValid() {
      return this.documentDetails.documentNumber.trim() && 
             this.documentDetails.version.trim() && 
             this.documentDetails.revision.trim();
    }
  },
  
  mounted() {
    const { lruId, documentId, projectId } = this.$route.params;
    console.log('Document Viewer initialized:', { lruId, documentId, projectId });
    
    // Set the correct LRU ID from route params
    if (lruId) {
      this.documentDetails.lruId = parseInt(lruId);
      // Load LRU metadata, next doc_ver, document versions, and existing documents
      this.loadLruMetadata(parseInt(lruId));
      this.loadNextDocVer(parseInt(lruId));
      this.loadDocumentVersions(parseInt(lruId));
      this.loadExistingDocuments(parseInt(lruId));
    }
    
    // Load existing document if available
    if (documentId && documentId !== 'new') {
      this.loadExistingDocument(documentId);
    }
  },
  
  methods: {
    // Load LRU metadata
    async loadLruMetadata(lruId) {
      try {
        console.log(`Attempting to load metadata for LRU ${lruId}...`);
        const response = await fetch(`http://localhost:8000/api/lrus/${lruId}/metadata`);
        
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const result = await response.json();
        console.log('API response:', result);
        
        if (result.success) {
          this.lruName = result.lru.lru_name;
          this.projectName = result.lru.project_name;
          console.log(`✅ Loaded metadata for LRU ${lruId}:`, result.lru);
        } else {
          console.warn('❌ Failed to load LRU metadata:', result.message);
          // Set fallback values
          this.lruName = `LRU-${lruId}`;
          this.projectName = "Unknown Project";
        }
      } catch (error) {
        console.error('❌ Error loading LRU metadata:', error);
        // Set fallback values when API is not available
        this.lruName = `LRU-${lruId}`;
        this.projectName = "Unknown Project";
      }
    },

    // Load next doc_ver for LRU
    async loadNextDocVer(lruId) {
      try {
        console.log(`Attempting to load next doc_ver for LRU ${lruId}...`);
        const response = await fetch(`http://localhost:8000/api/plan-documents/next-doc-ver/${lruId}`);
        
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const result = await response.json();
        console.log('Next doc_ver API response:', result);
        
        if (result.success) {
          this.documentDetails.docVer = result.nextDocVer;
          console.log(`✅ Next doc_ver for LRU ${lruId}: ${result.nextDocVer}`);
        } else {
          // If no documents exist for this LRU, start with 1
          this.documentDetails.docVer = 1;
          console.log(`⚠️ No existing documents for LRU ${lruId}, starting with doc_ver = 1`);
        }
      } catch (error) {
        console.error('❌ Error loading next doc_ver:', error);
        // Default to 1 if there's an error
        this.documentDetails.docVer = 1;
        console.log(`⚠️ Error occurred, defaulting to doc_ver = 1`);
      }
    },

    // Load existing documents for LRU  
    async loadExistingDocuments(lruId) {
      try {
        this.loading = true;
        console.log(`Loading existing documents for LRU ${lruId}...`);
        
        const response = await fetch(`http://localhost:8000/api/lrus/${lruId}/plan-documents`);
        
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const result = await response.json();
        console.log('Existing documents API response:', result);
        
        if (result.success) {
          this.existingDocuments = result.documents;
          console.log(`✅ Loaded ${this.existingDocuments.length} existing documents for LRU ${lruId}`);
        } else {
          console.warn('❌ Failed to load existing documents:', result.message);
          this.existingDocuments = [];
        }
      } catch (error) {
        console.error('❌ Error loading existing documents:', error);
        this.existingDocuments = [];
      } finally {
        this.loading = false;
      }
    },

    // Load document versions for LRU (used for track versions modal)
    async loadDocumentVersions(lruId) {
      try {
        const response = await fetch(`http://localhost:8000/api/lrus/${lruId}/plan-documents`);
        const result = await response.json();
        
        if (result.success) {
          // Transform the data to match the expected format for the modal
          this.documentVersions = result.documents.map(doc => ({
            id: doc.document_id,
            projectId: `${doc.document_number}`,
            version: doc.revision,
            date: new Date(doc.upload_date).toLocaleDateString(),
            isFavorite: false, // You can add a favorite flag to your database later
            deleted: false
          }));
          console.log(`Loaded ${this.documentVersions.length} document versions for LRU ${lruId}`);
        } else {
          console.warn('Failed to load document versions:', result.message);
        }
      } catch (error) {
        console.error('Error loading document versions:', error);
      }
    },

    // View a specific document
    async viewDocument(doc) {
      try {
        console.log('🔍 Viewing document:', doc);
        console.log('📁 File path from DB:', doc.file_path);
        
        // Extract filename from file_path - handle both Windows (\) and Unix (/) paths
        let filename = doc.file_path.split('\\').pop(); // Handle Windows paths
        filename = filename.split('/').pop(); // Handle Unix paths
        
        console.log('📄 Extracted filename:', filename);
        
        const fileUrl = `http://localhost:8000/api/files/plan-documents/${filename}`;
        console.log('🌐 File URL:', fileUrl);
        
        // Test if file is accessible
        try {
          const testResponse = await fetch(fileUrl, { method: 'HEAD' });
          console.log('🔗 File accessibility test:', testResponse.status, testResponse.statusText);
          
          if (!testResponse.ok) {
            throw new Error(`File not accessible: ${testResponse.status} ${testResponse.statusText}`);
          }
        } catch (fetchError) {
          console.error('❌ File accessibility test failed:', fetchError);
          alert(`Failed to access file: ${filename}. Please check if the file exists in plan_doc_uploads folder.`);
          return;
        }
        
        // Set document metadata
        this.documentId = doc.document_number;
        this.status = doc.status;
        this.lastModifiedDate = new Date(doc.upload_date);
        
        // Load the file for display based on file extension
        const extension = filename.split('.').pop().toLowerCase();
        console.log('📋 File extension:', extension);
        
        if (extension === 'pdf') {
          this.fileType = 'pdf';
          this.fileName = filename;
          console.log('📄 Loading PDF...');
          await this.loadPdfFromUrl(fileUrl);
        } else if (extension === 'docx') {
          this.fileType = 'docx';
          this.fileName = filename;
          console.log('📝 Loading DOCX...');
          await this.loadDocxFromUrl(fileUrl);
        } else {
          this.fileType = 'other';
          this.fileName = filename;
          console.log('📄 Other file type, showing filename only');
        }
        
        console.log(`✅ Document ${doc.document_number} loaded successfully`);
        
      } catch (error) {
        console.error('❌ Error viewing document:', error);
        alert(`Failed to load document: ${error.message}`);
      }
    },

    // Date formatting
    formatDate(date) {
      if (!date) return 'N/A';
      return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    },

    // Load existing document from server
    async loadExistingDocument(documentId) {
      try {
        const response = await fetch(`http://localhost:8000/api/plan-documents/${documentId}`);
        const result = await response.json();
        
        if (result.success) {
          const doc = result.document;
          this.documentId = doc.document_id;
          this.fileName = doc.original_filename || 'Document';
          this.status = doc.status;
          this.lastModifiedDate = new Date(doc.upload_date);
          
          // Load the file for display
          if (doc.file_path) {
            await this.loadFileFromServer(doc.file_path, doc.original_filename);
          }
        }
      } catch (error) {
        console.error('Error loading document:', error);
      }
    },

    // Load file from server for display
    async loadFileFromServer(filePath, originalFilename) {
      try {
        const filename = filePath.split('/').pop();
        const fileUrl = `http://localhost:8000/api/files/plan-documents/${filename}`;
        
        // Determine file type from extension
        const extension = originalFilename.split('.').pop().toLowerCase();
        
        if (extension === 'pdf') {
          this.fileType = 'pdf';
          this.pdfUrl = fileUrl;
          this.loadPdfFromUrl(fileUrl);
        } else if (extension === 'docx') {
          this.fileType = 'docx';
          this.loadDocxFromUrl(fileUrl);
        } else {
          this.fileType = 'other';
          this.fileName = originalFilename;
        }
      } catch (error) {
        console.error('Error loading file from server:', error);
        alert('Failed to load document from server.');
      }
    },

    // Load PDF from URL
    async loadPdfFromUrl(url) {
      try {
        this.pdfUrl = url;
        this.page = 1;

        const loadingTask = pdfjsLib.getDocument(url);
        const pdf = await loadingTask.promise;
        this.numPages = pdf.numPages;
      } catch (err) {
        console.error("Failed to load PDF from URL", err);
        alert("Failed to load PDF file from server.");
      }
    },

    // Load DOCX from URL
    async loadDocxFromUrl(url) {
      try {
        const response = await fetch(url);
        const arrayBuffer = await response.arrayBuffer();
        const result = await mammoth.convertToHtml({ arrayBuffer });
        this.docxHtml = result.value;
      } catch (err) {
        console.error("Failed to load DOCX from URL", err);
        alert("Failed to load DOCX file from server.");
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
    handleFileSelect(event) {
      const file = event.target.files?.[0];
      if (!file) return;

      // Validate file type
      const fileType = file.type;
      const allowedTypes = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/msword",
        "text/plain",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.ms-excel"
      ];

      if (!allowedTypes.includes(fileType)) {
        alert("Unsupported file type. Please upload a PDF, DOCX, DOC, TXT, XLSX, or XLS file.");
        return;
      }

      // Validate file size (50MB limit)
      if (file.size > 50 * 1024 * 1024) {
        alert("File too large. Maximum size is 50MB.");
        return;
      }

      this.selectedFile = file;
      this.fileName = file.name;
      
      // Preview the file
      this.clearDocument();
      if (fileType === "application/pdf") {
        this.fileType = "pdf";
        this.loadPdf(file);
      } else if (fileType === "application/vnd.openxmlformats-officedocument.wordprocessingml.document") {
        this.fileType = "docx";
        this.loadDocx(file);
      } else {
        this.fileType = "other";
        this.fileName = file.name;
      }
    },

    async submitDocument() {
      if (!this.selectedFile) return;

      this.isUploading = true;

      try {
        const formData = new FormData();
        formData.append('file', this.selectedFile);
        formData.append('lru_id', this.documentDetails.lruId);
        formData.append('document_number', this.documentDetails.documentNumber);
        formData.append('version', this.documentDetails.version);
        formData.append('revision', this.documentDetails.revision);
        formData.append('doc_ver', this.documentDetails.docVer);
        formData.append('uploaded_by', userStore.getters.currentUser()?.id || userStore.getters.currentUser()?.user_id || 1001);

        const response = await fetch('http://localhost:8000/api/plan-documents', {
          method: 'POST',
          body: formData
        });

        const result = await response.json();

        if (result.success) {
          alert('Document uploaded successfully!');
          this.selectedFile = null;
          this.$emit('document-uploaded', result);
          
          // Update modified date and reload data
          this.lastModifiedDate = new Date();
          
          // Reload the next doc_ver, document versions, and existing documents list
          this.loadNextDocVer(this.documentDetails.lruId);
          this.loadDocumentVersions(this.documentDetails.lruId);
          this.loadExistingDocuments(this.documentDetails.lruId);
          
          // Clear the form
          this.documentDetails.documentNumber = "";
          this.documentDetails.version = "";
          this.documentDetails.revision = "";
        } else {
          alert(`Upload failed: ${result.message}`);
        }
      } catch (error) {
        console.error('Upload error:', error);
        alert('Failed to upload document. Please try again.');
      } finally {
        this.isUploading = false;
      }
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

.upload-section {
  display: flex;
  gap: 12px;
  align-items: center;
}

.submit-btn {
  background: #007bff;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
}

.submit-btn:hover:not(:disabled) {
  background: #0056b3;
}

.submit-btn:disabled {
  background: #6c757d;
  cursor: not-allowed;
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

/* Document Form */
.document-form {
  margin-top: 1rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 6px;
  border: 1px solid #e9ecef;
}

.form-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.form-group {
  flex: 1;
  min-width: 150px;
}

.form-group label {
  display: block;
  margin-bottom: 0.25rem;
  font-weight: 500;
  color: #495057;
  font-size: 0.9rem;
}

.form-input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 0.9rem;
  transition: border-color 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.form-input::placeholder {
  color: #6c757d;
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

/* Documents List Panel */
.documents-list-panel {
  width: 350px;
  background: white;
  margin: 1rem 0 1rem 1rem;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.documents-list-panel h3 {
  margin: 0;
  padding: 1rem 1.5rem;
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
  color: #495057;
  font-size: 1.1rem;
  font-weight: 600;
}

.documents-container {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem;
}

.loading-state {
  text-align: center;
  padding: 2rem;
  color: #6c757d;
}

.no-documents {
  text-align: center;
  padding: 3rem 1rem;
  color: #6c757d;
}

.no-docs-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.documents-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.document-item {
  display: flex;
  align-items: flex-start;
  padding: 1rem;
  border: 1px solid #e9ecef;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  background: white;
}

.document-item:hover {
  border-color: #007bff;
  background: #f8f9ff;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 123, 255, 0.1);
}

.doc-icon {
  margin-right: 0.75rem;
  font-size: 1.5rem;
  flex-shrink: 0;
}

.doc-info {
  flex: 1;
  min-width: 0;
}

.doc-title {
  font-weight: 600;
  color: #212529;
  margin-bottom: 0.25rem;
  word-break: break-word;
}

.doc-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.doc-version {
  color: #6c757d;
  font-size: 0.9rem;
}

.doc-ver {
  background: #e9ecef;
  color: #495057;
  padding: 0.125rem 0.375rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
}

.doc-details {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
  font-size: 0.8rem;
  color: #6c757d;
}

.uploaded-by {
  font-weight: 500;
}

.upload-date {
  font-style: italic;
}

.doc-status {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: capitalize;
}

.doc-status.status-not-assigned {
  background: #fff3cd;
  color: #856404;
}

.doc-status.status-assigned-and-returned {
  background: #d1ecf1;
  color: #0c5460;
}

.doc-status.status-cleared {
  background: #d4edda;
  color: #155724;
}

.doc-status.status-disapproved {
  background: #f8d7da;
  color: #721c24;
}

.doc-status.status-moved-to-next-stage {
  background: #cce5ff;
  color: #004085;
}

.doc-status.status-not-cleared {
  background: #f5c6cb;
  color: #721c24;
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