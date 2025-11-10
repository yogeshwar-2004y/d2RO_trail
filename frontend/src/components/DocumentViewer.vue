<template>
  <div class="pdf-viewer-container">
    <!-- Header with document info -->
    <div class="document-header">
      <div class="header-info">
        <h2>{{ lruName || "Document Viewer" }}</h2>
        <div class="meta-info">
          <span><strong>Project:</strong> {{ projectName || "N/A" }}</span>
          <span
            ><strong>Document ID:</strong>
            {{ getCurrentDocumentNumber() || "N/A" }}</span
          >
          <span
            ><strong>Status:</strong>
            <span :class="'status-' + (status || 'pending')">{{
              status || "Pending"
            }}</span></span
          >
          <!-- <span><strong>Status:</strong> <span :class="getStatusClass(status)">{{ status || 'Pending' }}</span></span> -->
          <span><strong>Created:</strong> {{ formatDate(createdDate) }}</span>
          <span
            ><strong>Modified:</strong> {{ formatDate(lastModifiedDate) }}</span
          >
        </div>
      </div>
    </div>

    <!-- Action Bar based on user role -->
    <div class="action-bar" v-if="currentUserRole">
      <!-- QA Head Actions -->
      <template v-if="currentUserRole === 'QA Head'">
        <button
          v-if="!hasAssignedReviewer"
          @click="assignReviewer"
          class="action-btn"
          :disabled="loadingReviewerStatus"
        >
          {{ loadingReviewerStatus ? "Loading..." : "Assign Reviewer" }}
        </button>
        <button
          v-if="hasAssignedReviewer"
          @click="editReviewer"
          class="action-btn action-btn-edit"
          :disabled="loadingReviewerStatus"
        >
          {{ loadingReviewerStatus ? "Loading..." : "Edit Reviewer" }}
        </button>
        <div v-if="hasAssignedReviewer" class="reviewer-info">
          <span class="reviewer-label">Current Reviewer:</span>
          <span class="reviewer-name">{{
            assignedReviewer?.name || "Unknown"
          }}</span>
        </div>
        <button @click="trackVersions" class="action-btn">
          Track Versions
        </button>
      </template>

      <!-- Design Head / Designer Actions -->
      <template
        v-if="
          currentUserRole === 'Design Head' || currentUserRole === 'Designer'
        "
      >
        <div class="upload-section">
          <label
            for="file-upload"
            class="upload-btn"
            :class="{ disabled: !canUploadDocument }"
          >
            Choose Document
            <input
              id="file-upload"
              type="file"
              accept=".pdf,.docx,.doc,.txt,.xlsx,.xls"
              @change="handleFileSelect"
              :disabled="!canUploadDocument"
              style="display: none"
            />
          </label>

          <!-- Upload restriction message -->
          <div v-if="!canUploadDocument" class="upload-restriction-message">
            <div class="restriction-icon">⚠️</div>
            <div class="restriction-text">
              <p><strong>Upload Restricted</strong></p>
              <p v-if="hasAcceptedDocument">
                This document has been accepted as the final version by a
                reviewer. No further uploads are allowed for this LRU.
              </p>
              <p v-else-if="!isLatestDocument">
                You are viewing a previous version of the document. Upload is
                only available for the latest version.
              </p>
              <p v-else-if="hasPendingCommentsInProject">
                There are unacknowledged comments on the latest document. Please
                acknowledge (accept or reject) all comments before uploading the
                next version.
              </p>
              <p v-else-if="allCommentsRejected">
                All comments have been rejected. You need to accept at least one
                comment to upload a revised document.
              </p>
              <p v-else-if="!hasCommentsOnCurrentDocument">
                The latest document is awaiting reviewer comments. Please wait
                for a reviewer to add comments before uploading the next
                version.
              </p>
              <p v-else>
                The latest document is awaiting review. Please wait for reviewer
                comments and acknowledge them before uploading the next version.
              </p>
            </div>
          </div>

          <!-- Upload available message -->
          <div
            v-if="canUploadDocument && existingDocuments.length > 0"
            class="upload-available-message"
          >
            <div class="success-icon">✅</div>
            <div class="success-text">
              <p><strong>Upload Available</strong></p>
              <p>
                All comments have been accepted. You can now upload the next
                version of the document.
              </p>
            </div>
          </div>

          <!-- Delete Latest Document Button -->
          <!-- <div v-if="existingDocuments.length > 0" class="delete-section">
            <button
              @click="deleteLatestDocument"
              class="delete-btn"
              :disabled="isDeleting"
            >
              {{ isDeleting ? "Deleting..." : "🗑️ Delete Latest Document" }}
            </button>
            <div class="delete-warning">
              <p>
                <strong>⚠️ Warning:</strong> This will permanently delete the
                latest document and all its comments.
              </p>
            </div>
          </div> -->

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
                <label>Revision (Auto-assigned):</label>
                <input
                  type="text"
                  v-model="documentDetails.docVer"
                  placeholder="e.g., A"
                  class="form-input"
                  readonly
                  style="background-color: #f3f4f6; cursor: not-allowed"
                />
              </div>
            </div>
            <button
              @click="submitDocument"
              class="submit-btn"
              :disabled="isUploading || !isFormValid"
            >
              {{ isUploading ? "Uploading..." : "Submit Document" }}
            </button>
          </div>
        </div>
      </template>

      <!-- View Observations button - Available for all roles -->
      <button @click="viewObservations" class="action-btn">
        View Observations
      </button>

      <!-- Admin and QA Reviewer don't need action buttons -->
    </div>

    <!-- Control Bar (shown when document is loaded) -->
    <div class="control-bar" v-if="fileType">
      <div class="controls-left">
        <button @click="zoomOut" class="control-btn">-</button>
        <span class="zoom-level">{{ (zoom * 100).toFixed(0) }}%</span>
        <button @click="zoomIn" class="control-btn">+</button>

        <template v-if="fileType === 'pdf'">
          <button @click="prevPage" :disabled="page <= 1" class="control-btn">
            ← Prev
          </button>
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
          <button
            @click="nextPage"
            :disabled="page >= numPages"
            class="control-btn"
          >
            Next →
          </button>
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
              :class="{ 'current-document': isCurrentDocument(doc) }"
              @click="viewDocument(doc)"
            >
              <div class="doc-icon">
                <span v-if="doc.file_path.toLowerCase().includes('.pdf')"
                  >📄</span
                >
                <span v-else-if="doc.file_path.toLowerCase().includes('.docx')"
                  >📝</span
                >
                <span v-else>📄</span>
              </div>
              <div class="doc-info">
                <div class="doc-title">
                  <span class="doc-label">{{ doc.doc_ver || "A" }}</span>
                  {{ doc.document_number }}
                  <span v-if="doc.status === 'accepted'" class="accepted-badge"
                    >✅ ACCEPTED</span
                  >
                  <span v-if="isCurrentDocument(doc)" class="current-badge"
                    >👁️ CURRENTLY VIEWING</span
                  >
                </div>
                <div class="doc-meta">
                  <span class="doc-version"
                    >{{ doc.version }} ({{ doc.revision }})</span
                  >
                  <span class="doc-ver">v{{ doc.doc_ver }}</span>
                </div>
                <div class="doc-details">
                  <span class="uploaded-by">{{ doc.uploaded_by_name }}</span>
                  <span class="upload-date">{{
                    formatDate(doc.upload_date)
                  }}</span>
                </div>
                <div
                  class="doc-status"
                  :class="'status-' + doc.status.replace(' ', '-')"
                >
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
          :class="{ 'annotation-mode': isAnnotationMode }"
          ref="pdfScroll"
          @scroll="onScroll"
          @click="handleDocumentClick"
        >
          <div
            v-for="p in numPages"
            :key="p"
            class="pdf-page-wrapper"
            :data-page="p"
          >
            <vue-pdf-embed
              :source="pdfUrl"
              :page="p"
              :scale="zoom"
              :ref="`pdfPage${p}`"
              class="pdf-page"
            />
            <!-- Annotation overlays for this page -->
            <div class="annotation-overlay" :data-page="p">
              <div
                v-for="annotation in getAnnotationsForPage(p)"
                :key="annotation.id"
                class="annotation-marker"
                :style="{
                  left: annotation.x + '%',
                  top: annotation.y + '%',
                }"
                @click="showAnnotationDetails(annotation)"
                :title="annotation.description"
              >
                <div class="annotation-circle">C</div>
              </div>
            </div>
          </div>
        </div>

        <!-- DOCX Viewer -->
        <div
          v-if="fileType === 'docx'"
          class="doc-container docx-content"
          :class="{ 'annotation-mode': isAnnotationMode }"
          :style="{ transform: `scale(${zoom})`, transformOrigin: 'top left' }"
          @click="handleDocumentClick"
          ref="docxContainer"
        >
          <!-- docx-preview renders content here -->
          <div ref="docxRenderRoot" class="docx-render-root"></div>
          <!-- Annotation overlays for DOCX -->
          <div class="annotation-overlay">
            <div
              v-for="annotation in annotations"
              :key="annotation.id"
              class="annotation-marker"
              :style="{
                left: annotation.x + '%',
                top: annotation.y + '%',
              }"
              @click="showAnnotationDetails(annotation)"
              :title="annotation.description"
            >
              <div class="annotation-circle">C</div>
            </div>
          </div>
        </div>

        <!-- Empty state -->
        <div v-if="!fileType" class="empty-state">
          <div class="empty-icon">📄</div>
          <p class="empty-msg">Select a document to view</p>
          <p class="empty-sub" v-if="canUpload">
            Or upload a new PDF or DOCX file
          </p>
        </div>
      </div>

      <!-- Enhanced Comments Sidebar -->
      <aside class="sidebar" v-if="canViewComments">
        <h3>Comments</h3>
        <div class="comments-container">
          <ul class="comments-list" v-if="comments.length > 0">
            <li
              v-for="(comment, index) in comments"
              :key="index"
              class="comment-item"
              :class="'status-' + (comment.status || 'pending')"
            >
              <button
                v-if="canDeleteComments"
                @click="deleteComment(index)"
                class="delete-btn"
                title="Delete comment"
              >
                🗑️
              </button>
              <div class="comment-header">
                <span class="comment-commented_by"
                  >Reviewer ID: {{ comment.reviewer_id || "Unknown" }}</span
                >
                <span class="comment-date">{{
                  formatDate(comment.created_at)
                }}</span>
                <span
                  v-if="comment.status"
                  class="comment-status"
                  :class="'status-' + comment.status"
                >
                  {{
                    comment.status === "accepted"
                      ? "Accepted"
                      : comment.status === "rejected"
                      ? "Rejected"
                      : comment.status
                  }}
                </span>
              </div>
              <div class="comment-content">
                <div class="comment-meta">
                  <span v-if="comment.page_no"
                    >Page: {{ comment.page_no }}</span
                  >
                  <span v-if="comment.section"
                    >Section: {{ comment.section }}</span
                  >
                </div>
                <p class="comment-text">{{ comment.description }}</p>
                <!-- <div v-if="comment.annotation" class="annotation-info">
                  <span class="annotation-marker">C Annotation</span>
                </div> -->

                <!-- Comment Response Section -->
                <div v-if="comment.justification" class="comment-response">
                  <div class="response-header">
                    {{
                      comment.status === "accepted" ? "Accepted" : "Rejected"
                    }}
                    by Designer ID {{ comment.accepted_by }}
                    <span v-if="comment.accepted_at" class="response-date">{{
                      formatDate(comment.accepted_at)
                    }}</span>
                  </div>
                  <div class="response-content">
                    {{ comment.justification }}
                  </div>
                </div>

                <!-- Action Buttons (only show for pending comments and for designers/design heads) -->
                <div
                  v-if="
                    (comment.status === 'pending' || !comment.status) &&
                    canAcceptRejectComments
                  "
                  class="comment-actions"
                >
                  <button
                    @click="acceptComment(comment)"
                    class="action-btn accept"
                  >
                    ✓ Accept
                  </button>
                  <button
                    @click="rejectComment(comment)"
                    class="action-btn reject"
                  >
                    ✗ Reject
                  </button>
                </div>
              </div>
            </li>
          </ul>
          <p v-else class="no-comments">No comments yet</p>
        </div>

        <!-- Add Comment Button (only for reviewers and only on latest version) -->
        <div class="add-comment-section" v-if="canAddCommentsOnCurrentDocument">
          <div class="button-group">
            <button
              @click="startAnnotationMode"
              class="add-comment-btn"
              v-if="!isAnnotationMode && !showCommentForm"
            >
              Add Comment
            </button>
            <button
              @click="acceptDocument"
              class="accept-document-btn"
              v-if="!isAnnotationMode && !showCommentForm"
            >
              Accept Document
            </button>
          </div>
        </div>

        <!-- Message for reviewers when viewing older versions -->
        <div
          v-if="canAddComments && !isLatestDocument"
          class="comment-restriction-message"
        >
          <div class="restriction-icon">ℹ️</div>
          <div class="restriction-text">
            <p><strong>Comments Not Available</strong></p>
            <p>
              You can only add comments to the latest version of the document.
              Please select the most recent version to add comments.
            </p>
          </div>
        </div>

        <!-- Annotation Mode Indicator (only for reviewers) -->
        <div
          v-if="isAnnotationMode && canAddComments"
          class="annotation-mode-indicator"
        >
          <div class="annotation-instruction">
            <span class="annotation-icon">📍</span>
            <span>Click on the document to place your annotation</span>
            <button @click="cancelAnnotation" class="cancel-annotation-btn">
              Cancel
            </button>
          </div>
        </div>

        <!-- Comment Form Modal - Shows after annotation is placed (only for reviewers) -->
        <div
          v-if="showCommentForm && canAddComments"
          class="comment-form-overlay"
          @click="closeCommentForm"
        >
          <div class="comment-form-container" @click.stop>
            <div class="comment-form-header">
              <h4>Add Comment</h4>
              <button @click="closeCommentForm" class="close-btn">×</button>
            </div>

            <div class="comment-form-body">
              <!-- Document Details Flex Box -->
              <div class="document-details-box">
                <h5>Document Details</h5>
                <div class="details-grid">
                  <div class="detail-item">
                    <span class="detail-label">Document ID:</span>
                    <span class="detail-value">{{
                      commentForm.document_id
                    }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Version:</span>
                    <span class="detail-value">{{ commentForm.version }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Revision:</span>
                    <span class="detail-value">{{ commentForm.revision }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Page:</span>
                    <span class="detail-value">{{ commentForm.page_no }}</span>
                  </div>
                </div>
              </div>

              <!-- Description Input -->
              <div class="form-group">
                <label>Comment Description</label>
                <textarea
                  v-model="commentForm.description"
                  placeholder="Enter your comment description..."
                  rows="4"
                  class="comment-description"
                ></textarea>
              </div>
            </div>

            <div class="comment-form-footer">
              <button @click="closeCommentForm" class="cancel-btn">
                Cancel
              </button>
              <button
                @click="submitComment"
                class="submit-btn"
                :disabled="!commentForm.description.trim()"
              >
                Submit Comment
              </button>
            </div>
          </div>
        </div>
      </aside>
    </div>

    <!-- Delete Confirmation Modal -->
    <div
      v-if="showDeleteConfirm"
      class="delete-confirm-overlay"
      @click="cancelDelete"
    >
      <div class="delete-confirm-modal" @click.stop>
        <div class="delete-confirm-header">
          <h4>Delete Comment</h4>
          <button @click="cancelDelete" class="close-btn">×</button>
        </div>

        <div class="delete-confirm-body">
          <div class="warning-icon">⚠️</div>
          <p>Are you sure you want to delete this comment?</p>
          <div class="comment-preview" v-if="commentToDelete">
            <strong>Comment:</strong>
            <p class="comment-text-preview">
              "{{ commentToDelete.comment.description }}"
            </p>
            <div class="comment-meta-preview">
              <span
                >By: Reviewer ID {{ commentToDelete.comment.reviewer_id }}</span
              >
              <span>Page: {{ commentToDelete.comment.page_no }}</span>
            </div>
          </div>
          <p class="warning-text">This action cannot be undone.</p>
        </div>

        <div class="delete-confirm-footer">
          <button @click="cancelDelete" class="cancel-btn">Cancel</button>
          <button @click="confirmDelete" class="delete-confirm-btn">
            Delete Comment
          </button>
        </div>
      </div>
    </div>

    <!-- Justification Modal -->
    <div
      v-if="showJustificationModal"
      class="justification-overlay"
      @click="cancelJustification"
    >
      <div class="justification-modal" @click.stop>
        <div class="justification-header">
          <h4>
            {{
              justificationAction === "accept"
                ? "Accept Comment"
                : "Reject Comment"
            }}
          </h4>
          <button @click="cancelJustification" class="close-btn">×</button>
        </div>

        <div class="justification-body">
          <div class="comment-preview" v-if="selectedComment">
            <strong>Comment:</strong>
            <p class="comment-text-preview">
              "{{ selectedComment.description }}"
            </p>
            <div class="comment-meta-preview">
              <span>By: Reviewer ID {{ selectedComment.reviewer_id }}</span>
              <span>Page: {{ selectedComment.page_no }}</span>
            </div>
          </div>

          <div class="form-group">
            <label for="justification">Justification *</label>
            <textarea
              id="justification"
              v-model="justificationText"
              placeholder="Please provide justification for your decision..."
              rows="4"
              class="justification-textarea"
              required
            ></textarea>
          </div>
        </div>

        <div class="justification-footer">
          <button @click="cancelJustification" class="cancel-btn">
            Cancel
          </button>
          <button
            @click="confirmJustification"
            class="confirm-btn"
            :class="justificationAction"
            :disabled="!justificationText.trim()"
          >
            {{
              justificationAction === "accept"
                ? "Accept Comment"
                : "Reject Comment"
            }}
          </button>
        </div>
      </div>
    </div>

    <!-- Assign Reviewer Modal -->
    <QAHeadAssignReviewer
      v-if="showAssignReviewerModal"
      :currentLruName="lruName"
      :currentProjectName="projectName"
      :isEditMode="isEditReviewerMode"
      :currentReviewer="assignedReviewer"
      @close="closeReviewerModal"
      @reviewerUpdated="onReviewerUpdated"
    />

    <!-- Track Versions Modal -->
    <div
      v-if="showTrackVersionsModal"
      class="track-versions-overlay"
      @click="closeTrackVersionsModal"
    >
      <div class="track-versions-modal" @click.stop>
        <div class="modal-header">
          <h2>TRACK VERSIONS</h2>
          <button class="close-button" @click="closeTrackVersionsModal">
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
                disabled: version.deleted,
                favorite: version.isFavorite,
              }"
              @click="version.deleted ? null : selectVersion(version)"
            >
              <div class="version-icon">
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
                  <path
                    d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"
                  ></path>
                  <rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect>
                </svg>
              </div>

              <div class="version-info">
                <span class="version-id"
                  >{{ version.projectId }} {{ version.version }}</span
                >
                <span class="version-date">{{ version.date }}</span>
              </div>

              <div class="version-actions">
                <button
                  class="star-button"
                  :class="{ starred: version.isFavorite }"
                  @click.stop="toggleFavorite(version)"
                  :disabled="version.deleted"
                >
                  <svg
                    v-if="version.isFavorite"
                    xmlns="http://www.w3.org/2000/svg"
                    width="20"
                    height="20"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <polygon
                      points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"
                    ></polygon>
                  </svg>
                  <svg
                    v-else
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
                    <polygon
                      points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"
                    ></polygon>
                  </svg>
                </button>

                <button
                  class="delete-button"
                  @click.stop="confirmDeleteVersion(version)"
                  :disabled="version.deleted"
                >
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
                    <polyline points="3,6 5,6 21,6"></polyline>
                    <path
                      d="M19,6v14a2,2,0,0,1-2,2H7a2,2,0,0,1-2-2V6m3,0V4a2,2,0,0,1,2-2h4a2,2,0,0,1,2,2V6"
                    ></path>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div
      v-if="showDeleteConfirmModal"
      class="delete-confirm-overlay"
      @click="closeDeleteConfirmModal"
    >
      <div class="delete-confirm-modal" @click.stop>
        <div class="modal-header">
          <h3>Confirm Deletion</h3>
          <button class="close-button" @click="closeDeleteConfirmModal">
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
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <div class="modal-content">
          <div class="confirm-message">
            <div class="warning-icon">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="48"
                height="48"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <path
                  d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"
                ></path>
                <line x1="12" y1="9" x2="12" y2="13"></line>
                <line x1="12" y1="17" x2="12.01" y2="17"></line>
              </svg>
            </div>
            <h4>Are you sure you want to delete this version?</h4>
            <p>
              Version:
              <strong
                >{{ versionToDelete?.projectId }}
                {{ versionToDelete?.version }}</strong
              >
            </p>
            <p class="warning-text">
              This action cannot be undone. The version will be marked as
              deleted and will no longer be accessible.
            </p>
          </div>

          <div class="modal-actions">
            <button @click="closeDeleteConfirmModal" class="btn btn-secondary">
              Cancel
            </button>
            <button @click="deleteVersion" class="btn btn-danger">
              Delete Version
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import VuePdfEmbed from "vue-pdf-embed";
import * as mammoth from "mammoth/mammoth.browser";
import * as pdfjsLib from "pdfjs-dist/build/pdf";
import { renderAsync as renderDocx } from "docx-preview";

// Configure pdf.js worker
import pdfjsWorker from "pdfjs-dist/build/pdf.worker?url";
pdfjsLib.GlobalWorkerOptions.workerSrc = pdfjsWorker;

import QAHeadAssignReviewer from "@/views/qahead/QAHeadAssignReviewer.vue";
import { userStore } from "@/stores/userStore";

export default {
  components: { VuePdfEmbed, QAHeadAssignReviewer },
  data() {
    return {
      // Document metadata - will be loaded dynamically
      lruName: "",
      projectName: "",
      documentId: null, // Numeric document_id for API calls
      documentNumber: null, // String document_number for display
      status: "pending", // pending, approved, rejected, review
      createdDate: null,
      lastModifiedDate: new Date(),

      // User role - from user store
      currentUserRole: userStore.getters.roleName() || "Guest",

      // Document viewing
      fileType: null,
      pdfUrl: null,
      docxHtml: "", // kept for back-compat; no longer used with docx-preview
      docxRendered: false,
      page: 1,
      numPages: 0,
      zoom: 1.0,
      fileName: "",

      // File upload
      selectedFile: null,
      isUploading: false,
      isDeleting: false,
      documentDetails: {
        lruId: 1,
        documentNumber: "",
        version: "",
        revision: "",
        docVer: "A",
      },

      showAssignReviewerModal: false,
      isEditReviewerMode: false,
      showTrackVersionsModal: false,
      showDeleteConfirmModal: false,
      versionToDelete: null,
      // Document list
      loading: false,
      existingDocuments: [],

      documentVersions: [
        {
          id: 1,
          projectId: "PRJ-2025-078",
          version: "A",
          date: "2025-01-15",
          isFavorite: true,
          deleted: false,
        },
        {
          id: 2,
          projectId: "PRJ-2025-078",
          version: "B",
          date: "2025-01-20",
          isFavorite: false,
          deleted: false,
        },
        {
          id: 3,
          projectId: "PRJ-2025-078",
          version: "C",
          date: "2025-01-25",
          isFavorite: false,
          deleted: false,
        },
        {
          id: 4,
          projectId: "PRJ-2025-078",
          version: "D",
          date: "2025-01-30",
          isFavorite: true,
          deleted: false,
        },
      ],

      // Reviewer assignment
      hasAssignedReviewer: false,
      assignedReviewer: null,
      loadingReviewerStatus: false,

      // Comments
      comments: [],
      allComments: [], // All comments across all documents in the project
      loadingAllComments: false, // Flag to track if we're loading all comments
      newComment: "",
      showCommentForm: false,
      commentForm: {
        document_name: "",
        document_id: "",
        version: "",
        revision: "",
        page_no: 1,
        section: "",
        description: "",
      },

      // Annotations
      annotations: [],
      isAnnotationMode: false,
      currentAnnotation: null,

      // Delete confirmation
      showDeleteConfirm: false,
      commentToDelete: null,

      // Justification modal
      showJustificationModal: false,
      selectedComment: null,
      justificationAction: "accept", // 'accept' or 'reject'
      justificationText: "",
    };
  },

  computed: {
    canUpload() {
      return (
        this.currentUserRole === "Design Head" ||
        this.currentUserRole === "Designer"
      );
    },

    // Helper function to check if a comment is accepted (case-insensitive)
    isCommentAccepted() {
      return (comment) => {
        const status = comment.status?.toString().toLowerCase();
        return status === "accepted";
      };
    },

    // Helper function to check if a comment is pending (not acknowledged)
    isCommentPending() {
      return (comment) => {
        const status = comment.status?.toString().toLowerCase();
        // Only consider comments pending if they haven't been acknowledged (accepted or rejected)
        return !status || status === "pending" || status === "none";
      };
    },

    // Helper function to check if a comment is acknowledged (either accepted or rejected)
    isCommentAcknowledged() {
      return (comment) => {
        const status = comment.status?.toString().toLowerCase();
        return status === "accepted" || status === "rejected";
      };
    },
    isDesigner() {
      return this.currentUserRole === "Designer";
    },
    isDesignHead() {
      return this.currentUserRole === "Design Head";
    },
    isQAHead() {
      return this.currentUserRole === "QA Head";
    },
    isQAAdmin() {
      return this.currentUserRole === "Admin";
    },
    isReviewer() {
      return this.currentUserRole === "QA Reviewer";
    },
    // Role-based permissions for commenting
    canAddComments() {
      return this.currentUserRole === "QA Reviewer";
    },
    canDeleteComments() {
      return this.currentUserRole === "QA Reviewer";
    },
    canAcceptRejectComments() {
      return (
        this.currentUserRole === "Designer" ||
        this.currentUserRole === "Design Head"
      );
    },
    canViewComments() {
      return (
        this.currentUserRole === "Admin" ||
        this.currentUserRole === "QA Head" ||
        this.currentUserRole === "QA Reviewer" ||
        this.currentUserRole === "Design Head" ||
        this.currentUserRole === "Designer"
      );
    },

    // Check if the currently viewed document is the latest version
    isLatestDocument() {
      if (!this.documentId || this.existingDocuments.length === 0) {
        return false;
      }

      // Get the latest document (first in the list, sorted by upload date)
      const latestDocument = this.existingDocuments[0];

      // Check if current document matches the latest document
      return (
        this.documentId === latestDocument.document_id ||
        this.documentNumber === latestDocument.document_number
      );
    },

    // Check if reviewer can add comments (only on latest version)
    canAddCommentsOnCurrentDocument() {
      return this.canAddComments && this.isLatestDocument;
    },
    docContent() {
      return (
        (this.fileType === "pdf" && this.pdfUrl) ||
        (this.fileType === "docx" && this.docxRendered)
      );
    },
    //isFormValid() {
    //return this.commentForm.description.trim();
    isFormValid() {
      return (
        this.documentDetails.documentNumber.trim() !== "" &&
        this.documentDetails.version.trim() !== "" &&
        this.documentDetails.docVer.trim() !== ""
      );
    },

    // Check if any document in this LRU is accepted (final version)
    hasAcceptedDocument() {
      return this.existingDocuments.some((doc) => doc.status === "accepted");
    },

    // Check if user can upload a new document
    canUploadDocument() {
      console.log("=== canUploadDocument DEBUG ===");
      console.log("existingDocuments.length:", this.existingDocuments.length);
      console.log("current document comments (this.comments):", this.comments);
      console.log(
        "current document comments length:",
        this.comments?.length || 0
      );
      console.log("isLatestDocument:", this.isLatestDocument);
      console.log("hasAcceptedDocument:", this.hasAcceptedDocument);

      // If no documents exist, allow upload
      if (this.existingDocuments.length === 0) {
        console.log("No documents exist, allowing upload");
        return true;
      }

      // If any document is already accepted, prevent further uploads
      if (this.hasAcceptedDocument) {
        console.log(
          "Document already accepted as final version - upload disabled"
        );
        return false;
      }

      // Only allow upload for the latest document version
      if (!this.isLatestDocument) {
        console.log("Not the latest document - upload disabled");
        return false;
      }

      // Check if current document has any comments
      if (this.comments && this.comments.length > 0) {
        const pendingComments = this.comments.filter((comment) =>
          this.isCommentPending(comment)
        );

        const acceptedComments = this.comments.filter((comment) =>
          this.isCommentAccepted(comment)
        );

        const rejectedComments = this.comments.filter((comment) => {
          const status = comment.status?.toString().toLowerCase();
          return status === "rejected";
        });

        console.log("Current document comment status breakdown:");
        console.log(`- Accepted: ${acceptedComments.length}`);
        console.log(`- Rejected: ${rejectedComments.length}`);
        console.log(`- Pending: ${pendingComments.length}`);

        // If there are pending comments, disable upload
        if (pendingComments.length > 0) {
          console.log("There are pending comments - upload disabled");
          return false;
        }

        // If all comments are acknowledged, check if at least one is accepted
        if (acceptedComments.length > 0) {
          console.log("At least one comment is accepted - upload enabled");
          return true;
        } else {
          console.log(
            "All comments are rejected - upload disabled (need at least one accepted)"
          );
          return false;
        }
      }

      // If no comments exist on current document, disable upload (waiting for reviewer comments)
      console.log(
        "No comments exist on current document - upload disabled (waiting for reviewer comments)"
      );
      return false;
    },

    // Check if there are pending comments for the current document
    // Note: this.comments is already filtered to current document by loadCommentsFromBackend()
    hasPendingComments() {
      return this.comments.some((comment) => this.isCommentPending(comment));
    },

    // Check if all comments are rejected (no accepted comments)
    allCommentsRejected() {
      if (!this.comments || this.comments.length === 0) {
        return false;
      }

      const acknowledgedComments = this.comments.filter((comment) =>
        this.isCommentAcknowledged(comment)
      );

      const acceptedComments = this.comments.filter((comment) =>
        this.isCommentAccepted(comment)
      );

      // All comments are rejected if all acknowledged comments are rejected (no accepted ones)
      return acknowledgedComments.length > 0 && acceptedComments.length === 0;
    },

    // Check if current document has any comments
    hasCommentsOnCurrentDocument() {
      return this.comments && this.comments.length > 0;
    },

    // Check if there are pending comments across ALL documents in the project
    hasPendingCommentsInProject() {
      console.log("=== hasPendingCommentsInProject DEBUG ===");
      console.log("loadingAllComments:", this.loadingAllComments);
      console.log("allComments:", this.allComments);
      console.log("allComments.length:", this.allComments?.length);
      console.log("existingDocuments.length:", this.existingDocuments.length);
      console.log("Current document comments (this.comments):", this.comments);
      console.log("Current document comments length:", this.comments?.length);

      // If we're still loading comments, don't disable upload yet - wait for loading to complete
      if (this.loadingAllComments) {
        console.log("Still loading comments - allowing upload for now");
        return false; // Don't disable upload while loading
      }

      // If no documents exist, allow upload
      if (this.existingDocuments.length === 0) {
        console.log("No existing documents - allowing upload");
        return false;
      }

      // Check ALL comments across ALL documents in the project (not just latest document)
      if (this.allComments && this.allComments.length > 0) {
        console.log(
          "All comments across project:",
          this.allComments.map((c) => ({
            id: c.id,
            status: c.status,
            doc_id: c.document_id,
            description: c.description?.substring(0, 30),
          }))
        );

        // Check if there are any pending comments across ALL documents
        // Only 'accepted' comments are considered resolved - all others keep upload disabled
        const pendingComments = this.allComments.filter((comment) =>
          this.isCommentPending(comment)
        );

        const acceptedComments = this.allComments.filter((comment) =>
          this.isCommentAccepted(comment)
        );

        const rejectedComments = this.allComments.filter((comment) => {
          const status = comment.status?.toString().toLowerCase();
          return status === "rejected";
        });

        const noneStatusComments = this.allComments.filter((comment) => {
          const status = comment.status?.toString().toLowerCase();
          return !status || status === "none" || status === "null";
        });

        console.log("Comment status breakdown:");
        console.log(`- Accepted: ${acceptedComments.length}`);
        console.log(`- Rejected: ${rejectedComments.length}`);
        console.log(`- None/Null status: ${noneStatusComments.length}`);
        console.log(`- Pending/Other: ${pendingComments.length}`);
        console.log("Pending comments across ALL documents:", pendingComments);

        // Debug individual comment statuses
        console.log("Individual comment statuses:");
        this.allComments.forEach((comment, index) => {
          console.log(`Comment ${index}:`, {
            id: comment.id,
            status: comment.status,
            statusType: typeof comment.status,
            isPending: this.isCommentPending(comment),
            isAccepted: this.isCommentAccepted(comment),
            description: comment.description?.substring(0, 30),
          });
        });

        // If all comments across all documents are acknowledged, check if at least one is accepted
        if (pendingComments.length === 0) {
          // Check if there's at least one accepted comment
          if (acceptedComments.length > 0) {
            console.log(
              "All comments acknowledged and at least one is accepted - allowing upload"
            );
            return false;
          } else {
            console.log(
              "All comments are rejected - upload disabled (need at least one accepted comment)"
            );
            return true;
          }
        }

        console.log(
          "hasPendingCommentsInProject result:",
          pendingComments.length > 0
        );
        return pendingComments.length > 0;
      }

      // If we have documents but no comments loaded yet, check current document comments as fallback
      console.log(
        "Have documents but no allComments loaded - checking current document comments as fallback"
      );

      // Fallback: check current document comments if allComments is not loaded
      if (this.comments && this.comments.length > 0) {
        console.log(
          "Fallback: Checking current document comments:",
          this.comments
        );
        const currentDocPendingComments = this.comments.filter((comment) =>
          this.isCommentPending(comment)
        );
        console.log(
          "Current document pending comments:",
          currentDocPendingComments.length
        );

        if (currentDocPendingComments.length > 0) {
          console.log(
            "Found pending comments in current document - disabling upload"
          );
          return true;
        }
      }

      console.log("No pending comments found - allowing upload");
      return false;
    },

    // Get the label for the current document (A, B, C, etc.)
    getCurrentDocumentLabel() {
      // First, try to find which document has active comments
      if (this.allComments && this.allComments.length > 0) {
        const pendingComments = this.allComments.filter(
          (comment) =>
            comment.status !== "accepted" && comment.status !== "rejected"
        );

        if (pendingComments.length > 0) {
          // Find the document that has the most recent pending comment
          const latestPendingComment = pendingComments.reduce(
            (latest, comment) => {
              const commentDate = new Date(comment.created_at);
              const latestDate = new Date(latest.created_at);
              return commentDate > latestDate ? comment : latest;
            }
          );

          // Find the document that has this comment
          const documentWithComment = this.existingDocuments.find(
            (doc) =>
              doc.document_id == latestPendingComment.document_id ||
              doc.document_number === latestPendingComment.document_id
          );

          if (documentWithComment) {
            console.log("Document with active comment:", documentWithComment);
            return documentWithComment.doc_ver || "Unknown";
          }
        }
      }

      // Fallback to latest document
      const latestDocument = this.getLatestDocument();
      if (!latestDocument) {
        return "A";
      }

      return latestDocument.doc_ver || "A";
    },
  },

  async mounted() {
    const { lruId, documentId, projectId } = this.$route.params;
    console.log("Document Viewer initialized:", {
      lruId,
      documentId,
      projectId,
    });

    // Set the correct LRU ID from route params
    if (lruId) {
      this.documentDetails.lruId = parseInt(lruId);

      // Load all comments FIRST to enable proper upload restrictions
      await this.loadAllCommentsForProject();

      // Then load other data
      this.loadLruMetadata(parseInt(lruId));
      this.loadNextDocVer(parseInt(lruId));
      this.loadDocumentVersions(parseInt(lruId));
      this.loadExistingDocuments(parseInt(lruId));
    }

    // Load existing document if available
    if (documentId && documentId !== "new") {
      this.loadExistingDocument(documentId);
    }

    // Check reviewer assignment status for QA Head
    if (this.currentUserRole === "QA Head") {
      // Add a delay to ensure LRU metadata is loaded first
      setTimeout(() => {
        this.checkReviewerAssignment();
      }, 1000);
    }
  },

  watch: {
    // Watch for changes in allComments to update upload restrictions
    allComments: {
      handler() {
        console.log("allComments changed, re-evaluating upload restrictions");
        // Force reactivity update
        this.$nextTick(() => {
          console.log(
            "Upload restriction after allComments change:",
            this.hasPendingCommentsInProject
          );
        });
      },
      deep: true,
    },
  },

  methods: {
    // Helper method to get the latest uploaded document
    getLatestDocument() {
      if (this.existingDocuments.length === 0) {
        return null;
      }

      // Sort documents by upload date and get the latest
      const sortedDocs = [...this.existingDocuments].sort(
        (a, b) => new Date(b.upload_date) - new Date(a.upload_date)
      );

      return sortedDocs[0];
    },

    // Helper method to check if a specific document has pending comments
    hasPendingCommentsForDocument(documentId) {
      return this.comments.some(
        (comment) =>
          comment.document_id === documentId &&
          (comment.status === "pending" || !comment.status)
      );
    },

    // Helper method to get the current document number for display
    getCurrentDocumentNumber() {
      const currentDoc = this.getCurrentDocument();
      return currentDoc ? currentDoc.document_number : null;
    },

    // Helper method to get the current document being viewed
    getCurrentDocument() {
      // If we have a specific document loaded, return it
      if (this.documentId && this.existingDocuments.length > 0) {
        return this.existingDocuments.find(
          (doc) => doc.document_id === this.documentId
        );
      }

      // Otherwise return the latest document
      return this.getLatestDocument();
    },

    // Check if a specific document is currently being viewed
    isCurrentDocument(doc) {
      if (!this.documentId || !doc) {
        return false;
      }

      // Check if the document matches the currently viewed document
      // Prioritize document_id comparison since it's unique
      return this.documentId === doc.document_id;
    },

    // Load LRU metadata
    async loadLruMetadata(lruId) {
      try {
        console.log(`Attempting to load metadata for LRU ${lruId}...`);
        const response = await fetch(
          `http://localhost:8000/api/lrus/${lruId}/metadata`
        );

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const result = await response.json();
        console.log("API response:", result);

        if (result.success) {
          this.lruName = result.lru.lru_name;
          this.projectName = result.lru.project_name;
          console.log(`✅ Loaded metadata for LRU ${lruId}:`, result.lru);
        } else {
          console.warn("❌ Failed to load LRU metadata:", result.message);
          // Set fallback values
          this.lruName = `LRU-${lruId}`;
          this.projectName = "Unknown Project";
        }
      } catch (error) {
        console.error("❌ Error loading LRU metadata:", error);
        // Set fallback values when API is not available
        this.lruName = `LRU-${lruId}`;
        this.projectName = "Unknown Project";
      }
    },

    // Load next doc_ver for LRU
    async loadNextDocVer(lruId) {
      try {
        console.log(`Attempting to load next doc_ver for LRU ${lruId}...`);
        const response = await fetch(
          `http://localhost:8000/api/plan-documents/next-doc-ver/${lruId}`
        );

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const result = await response.json();
        console.log("Next doc_ver API response:", result);

        if (result.success) {
          this.documentDetails.docVer = result.nextDocVer;
          console.log(`✅ Next doc_ver for LRU ${lruId}: ${result.nextDocVer}`);
        } else {
          // If no documents exist for this LRU, start with A
          this.documentDetails.docVer = "A";
          console.log(
            `⚠️ No existing documents for LRU ${lruId}, starting with doc_ver = A`
          );
        }
      } catch (error) {
        console.error("❌ Error loading next doc_ver:", error);
        // Default to A if there's an error
        this.documentDetails.docVer = "A";
        console.log(`⚠️ Error occurred, defaulting to doc_ver = A`);
      }
    },

    // Load existing documents for LRU
    async loadExistingDocuments(lruId) {
      try {
        this.loading = true;
        console.log(`Loading existing documents for LRU ${lruId}...`);

        const response = await fetch(
          `http://localhost:8000/api/lrus/${lruId}/plan-documents`
        );

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const result = await response.json();
        console.log("Existing documents API response:", result);

        if (result.success) {
          this.existingDocuments = result.documents;
          console.log(
            `✅ Loaded ${this.existingDocuments.length} existing documents for LRU ${lruId}`
          );
        } else {
          console.warn("❌ Failed to load existing documents:", result.message);
          this.existingDocuments = [];
        }
      } catch (error) {
        console.error("❌ Error loading existing documents:", error);
        this.existingDocuments = [];
      } finally {
        this.loading = false;
      }
    },

    // Load document versions for LRU and display the latest one
    async loadDocumentVersions(lruId) {
      try {
        const response = await fetch(
          `http://localhost:8000/api/lrus/${lruId}/plan-documents`
        );
        const result = await response.json();

        if (result.success) {
          // Transform the data to match the expected format
          this.documentVersions = result.documents
            .map((doc) => ({
              id: doc.document_id,
              projectId: `${doc.document_number}`,
              version: doc.version,
              docVer: doc.doc_ver,
              revision: doc.revision,
              date: new Date(doc.upload_date).toLocaleDateString(),
              filePath: doc.file_path,
              originalFilename: doc.original_filename,
              fileSize: doc.file_size,
              isFavorite: false,
              deleted: false,
            }))
            .sort((a, b) => new Date(b.date) - new Date(a.date)); // Sort by date, newest first

          console.log(
            `Loaded ${this.documentVersions.length} document versions for LRU ${lruId}`
          );

          // If there are existing documents, load the latest one
          if (this.documentVersions.length > 0) {
            const latestDoc = this.documentVersions[0];
            this.loadExistingDocument(latestDoc);
          }
        } else {
          console.warn("Failed to load document versions:", result.message);
        }
      } catch (error) {
        console.error("Error loading document versions:", error);
      }
    },

    // View a specific document
    async viewDocument(doc) {
      try {
        console.log("🔍 Viewing document:", doc);
        console.log("📁 File path from DB:", doc.file_path);

        // Extract filename from file_path - handle both Windows (\) and Unix (/) paths
        let filename = doc.file_path.split("\\").pop(); // Handle Windows paths
        filename = filename.split("/").pop(); // Handle Unix paths

        console.log("📄 Extracted filename:", filename);

        const fileUrl = `http://localhost:8000/api/files/plan-documents/${filename}`;
        console.log("🌐 File URL:", fileUrl);

        // Test if file is accessible
        try {
          const testResponse = await fetch(fileUrl, { method: "HEAD" });
          console.log(
            "🔗 File accessibility test:",
            testResponse.status,
            testResponse.statusText
          );

          if (!testResponse.ok) {
            throw new Error(
              `File not accessible: ${testResponse.status} ${testResponse.statusText}`
            );
          }
        } catch (fetchError) {
          console.error("❌ File accessibility test failed:", fetchError);
          alert(
            `Failed to access file: ${filename}. Please check if the file exists in plan_doc_uploads folder.`
          );
          return;
        }

        // Set document metadata
        this.documentId = doc.document_id; // Use actual document_id (integer) instead of document_number
        this.documentNumber = doc.document_number; // Set document_number for display and API calls
        this.status = doc.status;
        this.lastModifiedDate = new Date(doc.upload_date);

        // Clear previous comments and annotations first
        this.comments = [];
        this.annotations = [];

        // Load existing comments and annotations (non-blocking)
        this.loadCommentsFromBackend().catch((err) => {
          console.warn("Comments loading failed (non-critical):", err);
        });

        // Load the file for display based on file extension
        const extension = filename.split(".").pop().toLowerCase();
        console.log("📋 File extension:", extension);

        if (extension === "pdf") {
          this.fileType = "pdf";
          this.fileName = filename;
          console.log("📄 Loading PDF...");
          await this.loadPdfFromUrl(fileUrl);
        } else if (extension === "docx") {
          this.fileType = "docx";
          this.fileName = filename;
          console.log("📝 Loading DOCX...");
          await this.loadDocxFromUrl(fileUrl);
        } else {
          this.fileType = "other";
          this.fileName = filename;
          console.log("📄 Other file type, showing filename only");
        }

        console.log(`✅ Document ${doc.document_number} loaded successfully`);
      } catch (error) {
        console.error("❌ Error viewing document:", error);
        alert(`Failed to load document: ${error.message}`);
      }
    },

    // Load DOCX directly from a URL (docx-preview)
    async loadDocxFromUrl(fileUrl) {
      try {
        this.clearDocument();
        this.fileType = "docx";

        const response = await fetch(fileUrl);
        if (!response.ok) {
          throw new Error(
            `Failed to fetch DOCX: ${response.status} ${response.statusText}`
          );
        }
        const arrayBuffer = await response.arrayBuffer();
        const container = this.$refs.docxRenderRoot || this.$refs.docxContainer;
        if (!container) return;
        container.innerHTML = "";
        await renderDocx(arrayBuffer, container, undefined, {
          inWrapper: true,
          className: "docx-preview-root",
        });
        this.docxRendered = true;
        this.$nextTick(() => {
          this.numPages = 1;
        });
      } catch (err) {
        console.error("❌ Failed to load DOCX from URL:", err);
        alert("Failed to load DOCX file from server.");
      }
    },

    // Load a PDF directly from a URL (used when viewing existing documents)
    async loadPdfFromUrl(fileUrl) {
      try {
        // Reset previous document state and set up for PDF
        this.clearDocument();
        this.fileType = "pdf";
        this.pdfUrl = fileUrl;
        this.page = 1;

        const loadingTask = pdfjsLib.getDocument(this.pdfUrl);
        const pdf = await loadingTask.promise;
        this.numPages = pdf.numPages;
      } catch (err) {
        console.error("Failed to load PDF from URL", err);
        alert("Failed to load PDF file.");
      }
    },

    // Load an existing document either by object or by id/number
    async loadExistingDocument(input) {
      try {
        // If a full document object was passed, delegate to viewDocument
        if (input && typeof input === "object" && input.file_path) {
          await this.viewDocument(input);
          return;
        }

        // Otherwise, fetch list and find by document_number or document_id
        const lruId = this.documentDetails.lruId;
        if (!lruId) {
          console.warn("loadExistingDocument called without LRU ID");
          return;
        }

        const response = await fetch(
          `http://localhost:8000/api/lrus/${lruId}/plan-documents`
        );
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        const data = await response.json();
        if (!data.success) {
          console.warn(
            "Failed to load documents for selecting existing document:",
            data.message
          );
          return;
        }

        const targetIdNum = Number(input);
        const doc = (data.documents || []).find(
          (d) => d.document_number === input || d.document_id === targetIdNum
        );

        if (doc) {
          await this.viewDocument(doc);
        } else {
          console.warn(
            "Requested document not found among existing documents:",
            input
          );
        }
      } catch (err) {
        console.error("Error in loadExistingDocument:", err);
      }
    },

    // Load file from server for display
    /*async loadFileFromServer(filePath, originalFilename) {
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
          console.warn('Requested document not found among existing documents:', input);
        }
      } catch (err) {
        console.error('Error in loadExistingDocument:', err);
      }
    },*/

    // Date formatting
    formatDate(date) {
      if (!date) return "N/A";
      return new Date(date).toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "numeric",
        minute: "numeric",
      });
    },

    // Comment handling
    handleAccept(comment) {
      comment.status = "accepted";
      comment.response = "Comment accepted and changes will be implemented.";
      // TODO: Update on server
    },

    handleReject(comment) {
      this.selectedComment = comment;
      this.showRejectModal = true;
    },

    confirmReject() {
      if (this.selectedComment && this.rejectJustification) {
        this.selectedComment.status = "rejected";
        this.selectedComment.response = this.rejectJustification;
        // TODO: Update on server
        this.cancelReject();
      }
    },

    cancelReject() {
      this.showRejectModal = false;
      this.rejectJustification = "";
      this.selectedComment = null;
    },

    // Accept/Reject Comment Methods
    acceptComment(comment) {
      this.selectedComment = comment;
      this.justificationAction = "accept";
      this.justificationText = "";
      this.showJustificationModal = true;
    },

    rejectComment(comment) {
      this.selectedComment = comment;
      this.justificationAction = "reject";
      this.justificationText = "";
      this.showJustificationModal = true;
    },

    cancelJustification() {
      this.showJustificationModal = false;
      this.selectedComment = null;
      this.justificationText = "";
      this.justificationAction = "accept";
    },

    async acceptDocument() {
      try {
        console.log("Accepting document with ID:", this.documentId);
        console.log("Document number:", this.documentNumber);

        // Show confirmation dialog
        const confirmed = confirm(
          "Are you sure you want to accept this document? This action will mark the document as approved."
        );

        if (!confirmed) {
          return;
        }

        // Make API call to accept the document
        const url = `http://localhost:8000/api/documents/${this.documentId}/accept`;
        console.log("Making request to:", url);

        const response = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        });

        console.log("Response status:", response.status);
        console.log("Response ok:", response.ok);

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          throw new Error(
            errorData.message ||
              `HTTP ${response.status}: ${response.statusText}`
          );
        }

        const result = await response.json();

        // Show success message
        alert(`Document has been accepted successfully! ${result.message}`);

        // Refresh the document data or emit event to parent component
        this.$emit("document-accepted", result);

        // Reload existing documents to show updated status
        await this.loadExistingDocuments(this.documentDetails.lruId);

        // Optionally reload the page or refresh data
        this.$router.go(0); // Reload the current page
      } catch (error) {
        console.error("Error accepting document:", error);
        alert(`Failed to accept document: ${error.message}`);
      }
    },

    async confirmJustification() {
      if (!this.justificationText.trim()) {
        alert("Please provide justification for your decision.");
        return;
      }

      if (!this.selectedComment) {
        alert("No comment selected.");
        return;
      }

      try {
        // Get current user info
        let currentUser = "Anonymous";
        let currentUserId = null;
        try {
          if (userStore && userStore.getters && userStore.getters.userName) {
            currentUser = userStore.getters.userName() || "Anonymous";
          }
          if (userStore && userStore.getters && userStore.getters.currentUser) {
            const user = userStore.getters.currentUser();
            currentUserId = user?.id || user?.user_id || null;
          }
        } catch (error) {
          console.log("Error getting user info:", error);
        }

        const endpoint =
          this.justificationAction === "accept"
            ? `/api/comments/${this.selectedComment.id}/accept`
            : `/api/comments/${this.selectedComment.id}/reject`;

        // Get current document details
        const currentDocument = this.getCurrentDocument();
        const documentDetails = {
          document_id:
            this.selectedComment.document_id || currentDocument?.document_id,
          document_name:
            this.selectedComment.document_name ||
            currentDocument?.document_number,
          document_version:
            this.selectedComment.version || currentDocument?.version,
          document_revision:
            this.selectedComment.revision || currentDocument?.revision,
          document_doc_ver: currentDocument?.doc_ver || "A",
          lru_id: this.documentDetails.lruId,
          project_name: this.projectName,
          lru_name: this.lruName,
        };

        const requestData = {
          justification: this.justificationText,
          accepted_by: currentUserId,
          user_role: this.currentUserRole,
          action: this.justificationAction, // 'accept' or 'reject'
          action_date: new Date().toISOString(),
          ...documentDetails,
        };

        console.log("Sending comment acceptance/rejection data:", requestData);
        console.log("API endpoint:", endpoint);

        const response = await fetch(`http://localhost:8000${endpoint}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(requestData),
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.message || "Failed to update comment");
        }

        const result = await response.json();
        console.log("Comment updated successfully:", result);

        // Reload comments from backend to get updated status
        await this.loadCommentsFromBackend();

        // Reload all comments for the project to update upload restrictions
        await this.loadAllCommentsForProject();

        // Force update of upload restrictions
        this.$forceUpdate();

        // Close modal
        this.cancelJustification();

        // Show success message with upload status
        const action =
          this.justificationAction === "accept" ? "accepted" : "rejected";
        const uploadStatus = this.canUploadDocument
          ? "You can now upload the next version of the document."
          : "Please review and accept all remaining comments before uploading.";
        alert(`Comment ${action} successfully! ${uploadStatus}`);
      } catch (error) {
        console.error("Error updating comment:", error);
        alert(
          `Failed to ${this.justificationAction} comment: ${error.message}`
        );
      }
    },

    scrollToPage(pageNum) {
      if (
        this.fileType === "pdf" &&
        this.$refs.pdfScroll &&
        this.$refs.pdfPages
      ) {
        const targetPage = this.$refs.pdfPages[pageNum - 1];
        if (targetPage && targetPage.$el) {
          targetPage.$el.scrollIntoView({ behavior: "smooth" });
        }
      }
    },

    async assignReviewer() {
      this.isEditReviewerMode = false;
      this.showAssignReviewerModal = true;
    },

    async editReviewer() {
      this.isEditReviewerMode = true;
      this.showAssignReviewerModal = true;
    },

    async checkReviewerAssignment() {
      if (!this.lruName || !this.projectName) {
        return;
      }

      try {
        this.loadingReviewerStatus = true;
        const response = await fetch(
          `http://localhost:8000/api/assigned-reviewer?lru_name=${encodeURIComponent(
            this.lruName
          )}&project_name=${encodeURIComponent(this.projectName)}`
        );
        const data = await response.json();

        if (data.success) {
          this.hasAssignedReviewer = data.has_reviewer;
          this.assignedReviewer = data.reviewer;
        } else {
          console.error("Error checking reviewer assignment:", data.message);
          this.hasAssignedReviewer = false;
          this.assignedReviewer = null;
        }
      } catch (error) {
        console.error("Error checking reviewer assignment:", error);
        this.hasAssignedReviewer = false;
        this.assignedReviewer = null;
      } finally {
        this.loadingReviewerStatus = false;
      }
    },

    closeReviewerModal() {
      this.showAssignReviewerModal = false;
      this.isEditReviewerMode = false;
    },

    onReviewerUpdated() {
      // Refresh reviewer status after assignment/update
      this.checkReviewerAssignment();
      this.closeReviewerModal();
    },
    viewObservations() {
      this.$router.push({
        name: "ObservationReport",
        params: {
          lruId: this.documentDetails.lruId,
          lruName: this.lruName,
          projectId: this.$route.params.projectId,
        },
      });
    },
    trackVersions() {
      this.showTrackVersionsModal = true;
    },
    closeTrackVersionsModal() {
      this.showTrackVersionsModal = false;
    },
    selectVersion(version) {
      console.log("Selected version:", version);
      // Navigate to the document version view page
      this.$router.push({
        name: "QAHeadDocumentVersionView",
        params: {
          projectName: this.projectName,
          lruName: this.lruName,
          versionId: `${version.projectId}-${version.version}`,
        },
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
        "Under Review": "status-under-review",
        Approved: "status-approved",
        Rejected: "status-reject",
        Pending: "status-pending",
      };
      return statusMap[status] || "status-default";
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
        "application/vnd.ms-excel",
      ];

      if (!allowedTypes.includes(fileType)) {
        alert(
          "Unsupported file type. Please upload a PDF, DOCX, DOC, TXT, XLSX, or XLS file."
        );
        return;
      }

      // Validate file size (50MB limit)
      if (file.size > 50 * 1024 * 1024) {
        alert("File too large. Maximum size is 50MB.");
        return;
      }

      this.selectedFile = file;
      this.fileName = file.name;

      // Version will be assigned by backend API during upload

      // Preview the file
      this.clearDocument();
      if (fileType === "application/pdf") {
        this.fileType = "pdf";
        this.loadPdf(file);
      } else if (
        fileType ===
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
      ) {
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
        formData.append("file", this.selectedFile);
        formData.append("lru_id", this.documentDetails.lruId);
        formData.append("document_number", this.documentDetails.documentNumber);
        formData.append("version", this.documentDetails.version);
        formData.append("revision", this.documentDetails.revision);
        formData.append("doc_ver", this.documentDetails.docVer);
        formData.append(
          "uploaded_by",
          userStore.getters.currentUser()?.id ||
            userStore.getters.currentUser()?.user_id ||
            1001
        );

        const response = await fetch(
          "http://localhost:8000/api/plan-documents",
          {
            method: "POST",
            body: formData,
          }
        );

        const result = await response.json();

        if (result.success) {
          alert("Document uploaded successfully!");
          this.selectedFile = null;
          this.$emit("document-uploaded", result);

          // Clear current document state (but preserve comments in database)
          this.clearDocument();
          this.documentId = null;
          this.documentNumber = null;
          this.fileType = null;
          this.fileName = null;

          // Update modified date and reload data
          this.lastModifiedDate = new Date();

          // Reload the next doc_ver, document versions, and existing documents list
          this.loadNextDocVer(this.documentDetails.lruId);
          this.loadDocumentVersions(this.documentDetails.lruId);
          this.loadExistingDocuments(this.documentDetails.lruId);

          // Reload all comments to update upload restrictions
          await this.loadAllCommentsForProject();

          // Auto-view the newly uploaded document to make it active for commenting
          setTimeout(() => {
            if (this.existingDocuments.length > 0) {
              const latestDocument = this.existingDocuments[0]; // Get the most recent document
              this.viewDocument(latestDocument);
            }
          }, 1000); // Small delay to ensure documents are loaded

          // Clear the form
          this.documentDetails.documentNumber = "";
          this.documentDetails.version = "";
          this.documentDetails.revision = "";
        } else {
          alert(`Upload failed: ${result.message}`);
        }
      } catch (error) {
        console.error("Upload error:", error);
        alert("Failed to upload document. Please try again.");
      } finally {
        this.isUploading = false;
      }
    },

    async deleteLatestDocument() {
      if (this.existingDocuments.length === 0) {
        alert("No documents to delete.");
        return;
      }

      const latestDocument = this.existingDocuments[0];
      const confirmMessage = `Are you sure you want to delete the latest document?\n\nDocument: ${latestDocument.document_number}\nVersion: ${latestDocument.version}\n\nThis action cannot be undone and will delete all associated comments.`;

      if (!confirm(confirmMessage)) {
        return;
      }

      this.isDeleting = true;

      try {
        const response = await fetch(
          `http://localhost:8000/api/plan-documents/${latestDocument.document_id}`,
          {
            method: "DELETE",
            headers: {
              "Content-Type": "application/json",
            },
          }
        );

        const result = await response.json();

        if (result.success) {
          alert("Document deleted successfully!");

          // Reload documents and comments
          await this.loadDocuments();
          await this.loadAllCommentsForProject();

          // Clear current PDF if it was the deleted document
          if (
            this.currentDocument &&
            this.currentDocument.document_id === latestDocument.document_id
          ) {
            this.currentDocument = null;
            this.pdfUrl = null;
            this.page = 1;
            this.numPages = 0;
          }
        } else {
          alert(`Failed to delete document: ${result.message}`);
        }
      } catch (error) {
        console.error("Delete error:", error);
        alert("Failed to delete document. Please try again.");
      } finally {
        this.isDeleting = false;
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
        const container = this.$refs.docxRenderRoot || this.$refs.docxContainer;
        if (!container) return;
        container.innerHTML = "";
        await renderDocx(arrayBuffer, container, undefined, {
          inWrapper: true,
          className: "docx-preview-root",
        });
        this.docxRendered = true;
        this.$nextTick(() => {
          this.numPages = 1;
        });
      } catch (err) {
        console.error("Error rendering DOCX with docx-preview:", err);
        alert("Failed to render DOCX file.");
      }
    },

    processDocxHtml(html) {
      console.log("Processing DOCX HTML...");
      try {
        // Create a temporary container
        const temp = document.createElement("div");
        temp.innerHTML = html;

        // Get approximate content per page (A4 size)
        const CHARS_PER_PAGE = 3000; // Rough estimate of characters per page
        const totalContent = temp.textContent;
        const estimatedPages = Math.max(
          Math.ceil(totalContent.length / CHARS_PER_PAGE),
          1
        );
        console.log("Estimated pages:", {
          totalChars: totalContent.length,
          estimatedPages,
        });

        // Initialize result container
        const result = document.createElement("div");
        let pageCount = 0;
        let currentPage = null;
        let currentChars = 0;

        function startNewPage() {
          if (currentPage && currentPage.children.length > 0) {
            result.appendChild(currentPage);
          }
          pageCount++;
          currentPage = document.createElement("div");
          currentPage.className = "page";
          currentPage.setAttribute("data-page", pageCount.toString());
          currentChars = 0;
        }

        // Start first page
        startNewPage();

        // Process each element
        const elements = Array.from(temp.children);
        console.log("Processing elements:", { totalElements: elements.length });

        elements.forEach((element, index) => {
          // Check for explicit page breaks
          const style = window.getComputedStyle(element);
          const hasPageBreak =
            style.pageBreakBefore === "always" ||
            style.pageBreakAfter === "always" ||
            element.tagName === "HR";

          // Force a new page on headings for better content organization
          const isHeading = /^H[1-6]$/.test(element.tagName);
          const elementContent = element.textContent;

          // Start new page if:
          // 1. There's an explicit page break, or
          // 2. Current page has enough content and we're at a good break point, or
          // 3. We're at a heading and current page has some content
          if (
            hasPageBreak ||
            (currentChars > CHARS_PER_PAGE &&
              (isHeading || element.tagName === "P")) ||
            (isHeading && currentChars > CHARS_PER_PAGE * 0.5)
          ) {
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

        console.log("HTML processing complete", {
          actualPages: pageCount,
          estimatedPages,
          finalHtmlLength: result.innerHTML.length,
        });

        // Add page numbers
        result.querySelectorAll(".page").forEach((page, index) => {
          const pageNum = document.createElement("div");
          pageNum.className = "page-number";
          pageNum.textContent = `Page ${index + 1} of ${pageCount}`;
          page.appendChild(pageNum);
        });

        return result.innerHTML;
      } catch (err) {
        console.error("Error in processDocxHtml:", {
          error: err,
          errorName: err.name,
          errorMessage: err.message,
          errorStack: err.stack,
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

    // scrollToPage(pageNum) {
    //   console.log('Attempting to scroll to page:', pageNum, { fileType: this.fileType });

    //   this.$nextTick(() => {
    //     if (this.fileType === 'pdf' && this.$refs.pdfPages) {
    //       const pageEl = this.$refs.pdfPages[pageNum - 1]?.$el;
    //       if (pageEl) {
    //         console.log('Scrolling to PDF page element:', pageEl);
    //         pageEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
    //       } else {
    //         console.warn('PDF page element not found:', { pageNum, totalPages: this.numPages });
    //       }
    //     } else if (this.fileType === 'docx') {
    //       const docContainer = document.querySelector('.docx-content');
    //       if (docContainer) {
    //         const targetPage = docContainer.querySelector(`.page[data-page="${pageNum}"]`);
    //         if (targetPage) {
    //           console.log('Scrolling to DOCX page element:', targetPage);
    //           targetPage.scrollIntoView({ behavior: 'smooth', block: 'start' });
    //         } else {
    //           console.warn('DOCX page element not found:', { pageNum, totalPages: this.numPages });
    //         }
    //       } else {
    //         console.warn('DOCX container not found');
    //       }
    //     }
    //   });
    // },

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

    deleteComment(index) {
      const comment = this.comments[index];
      if (!comment) return;

      // Store comment to delete and show confirmation modal
      this.commentToDelete = { comment, index };
      this.showDeleteConfirm = true;
    },

    confirmDelete() {
      if (!this.commentToDelete) return;

      const { comment, index } = this.commentToDelete;

      // Delete comment from local array
      this.comments.splice(index, 1);

      // If comment has annotation, also delete the annotation
      if (
        comment.annotation &&
        comment.x !== undefined &&
        comment.y !== undefined
      ) {
        this.deleteAnnotationForComment(comment);
      }

      // Delete from backend if comment has an ID
      if (comment.id) {
        this.deleteCommentFromBackend(comment.id);
      }

      console.log("Comment deleted:", comment);
      console.log("Remaining comments:", this.comments.length);

      // Close confirmation modal
      this.showDeleteConfirm = false;
      this.commentToDelete = null;
    },

    cancelDelete() {
      this.showDeleteConfirm = false;
      this.commentToDelete = null;
    },

    deleteAnnotationForComment(comment) {
      // Find and remove the corresponding annotation
      const annotationIndex = this.annotations.findIndex(
        (ann) =>
          ann.description === comment.description &&
          ann.x === comment.x &&
          ann.y === comment.y
      );

      if (annotationIndex !== -1) {
        this.annotations.splice(annotationIndex, 1);
        console.log("Annotation deleted for comment:", comment);
      }
    },

    async deleteCommentFromBackend(commentId) {
      try {
        const response = await fetch(
          `http://localhost:8000/api/comments/${commentId}`,
          {
            method: "DELETE",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              user_role: this.currentUserRole,
            }),
          }
        );

        if (response.ok) {
          console.log("Comment deleted from backend successfully");
        } else {
          console.error("Failed to delete comment from backend");
        }
      } catch (error) {
        console.error("Error deleting comment from backend:", error);
      }
    },

    // Enhanced Comment System
    startAnnotationMode() {
      this.isAnnotationMode = true;
      this.showCommentForm = false;

      // Populate comment form with current document details
      this.commentForm.document_name = this.fileName || "";
      this.commentForm.document_id = this.documentId || "";
      this.commentForm.version =
        this.existingDocuments.find(
          (doc) => doc.document_id === this.documentId
        )?.version || "";
      this.commentForm.revision =
        this.existingDocuments.find(
          (doc) => doc.document_id === this.documentId
        )?.revision || "";
    },

    closeCommentForm() {
      this.showCommentForm = false;
      this.isAnnotationMode = false;
      this.commentForm = {
        document_name: this.fileName || "",
        document_id: this.documentNumber || "",
        version:
          this.existingDocuments.find(
            (doc) => doc.document_id === this.documentId
          )?.version || "",
        revision:
          this.existingDocuments.find(
            (doc) => doc.document_id === this.documentId
          )?.revision || "",
        page_no: this.page || 1,
        section: "",
        description: "",
      };
    },

    cancelAnnotation() {
      this.isAnnotationMode = false;
      this.showCommentForm = false;
    },

    submitComment() {
      console.log("Submit button clicked!");
      console.log("Form data:", this.commentForm);

      // Validate required fields
      if (!this.commentForm.description.trim()) {
        alert("Please enter description");
        return;
      }

      // Get current user info
      let currentUser = "Anonymous";
      let currentUserId = null;
      try {
        if (userStore && userStore.getters && userStore.getters.userName) {
          currentUser = userStore.getters.userName() || "Anonymous";
        }
        if (userStore && userStore.getters && userStore.getters.currentUser) {
          const user = userStore.getters.currentUser();
          currentUserId = user?.id || user?.user_id || null;
        }
      } catch (error) {
        console.log("Error getting user info:", error);
      }
      console.log("Current user:", currentUser, "User ID:", currentUserId);

      // Create comment with annotation data
      const comment = {
        id: Date.now(),
        ...this.commentForm,
        reviewer_id: currentUserId,
        created_at: new Date().toISOString(),
        annotation: !!this.currentAnnotation, // Only true if there's an annotation
      };

      console.log("Created comment object:", comment);

      // Create annotation if we have position data
      if (this.currentAnnotation) {
        const annotation = {
          id: Date.now(),
          x: this.currentAnnotation.x,
          y: this.currentAnnotation.y,
          page: this.currentAnnotation.page,
          description: this.commentForm.description,
          document_id: this.documentNumber,
        };

        this.annotations.push(annotation);
        comment.x = this.currentAnnotation.x;
        comment.y = this.currentAnnotation.y;

        console.log("Annotation created:", annotation);
        console.log("Total annotations:", this.annotations.length);

        // Clear current annotation after creating it
        this.currentAnnotation = null;
      }

      // Add comment to the comments array
      this.comments.push(comment);
      console.log("Comment added to comments array:", comment);
      console.log("Total comments now:", this.comments.length);
      console.log("Comments array:", this.comments);

      // Close the form
      this.closeCommentForm();

      // Save to backend
      this.saveCommentToBackend(comment);

      // Show success message
      console.log("Comment submitted successfully with annotation");
      alert("Comment submitted successfully!");

      // Show user feedback
      this.$nextTick(() => {
        console.log("Comment and annotation added successfully!");
        console.log("Comments in panel:", this.comments);
        console.log("Annotations on document:", this.annotations);
      });
    },

    // Annotation System
    handleDocumentClick(event) {
      if (!this.isAnnotationMode) return;
      // Compute coordinates relative to the correct target
      let x = 0;
      let y = 0;
      let pageNo = 1;

      if (this.fileType === "pdf") {
        // For PDFs, position relative to the clicked page wrapper
        const pageEl = event.target.closest(".pdf-page-wrapper");
        if (!pageEl) return;
        const rect = pageEl.getBoundingClientRect();
        x = ((event.clientX - rect.left) / rect.width) * 100;
        y = ((event.clientY - rect.top) / rect.height) * 100;
        pageNo = Number(pageEl.getAttribute("data-page")) || this.page || 1;
      } else {
        // For DOCX and others, position relative to the container
        const rect = event.currentTarget.getBoundingClientRect();
        x = ((event.clientX - rect.left) / rect.width) * 100;
        y = ((event.clientY - rect.top) / rect.height) * 100;
        pageNo = 1;
      }

      // Update comment form with click position and document details
      this.commentForm.page_no = pageNo;
      this.commentForm.document_name = this.fileName || "";
      this.commentForm.document_id = this.documentNumber || "";
      this.commentForm.version =
        this.existingDocuments.find(
          (doc) => doc.document_id === this.documentId
        )?.version || "";
      this.commentForm.revision =
        this.existingDocuments.find(
          (doc) => doc.document_id === this.documentId
        )?.revision || "";

      // Store annotation position for later use
      this.currentAnnotation = {
        x: x,
        y: y,
        page: pageNo,
      };

      // Exit annotation mode and show comment form
      this.isAnnotationMode = false;
      this.showCommentForm = true;
    },

    getAnnotationsForPage(pageNum) {
      const pageAnnotations = this.annotations.filter(
        (ann) => ann.page === pageNum
      );
      console.log(`Annotations for page ${pageNum}:`, pageAnnotations);
      return pageAnnotations;
    },

    showAnnotationDetails(annotation) {
      // Show annotation details in a tooltip or modal
      alert(`Annotation: ${annotation.description}`);
    },

    async saveCommentToBackend(comment) {
      try {
        // Debug: Log the comment object and component state
        console.log("Comment object:", comment);
        console.log(
          "Component documentId:",
          this.documentId,
          "Type:",
          typeof this.documentId
        );
        console.log(
          "Component documentNumber:",
          this.documentNumber,
          "Type:",
          typeof this.documentNumber
        );
        console.log(
          "Component fileName:",
          this.fileName,
          "Type:",
          typeof this.fileName
        );

        // Ensure document_id is a valid integer
        const documentId = parseInt(this.documentId);
        if (isNaN(documentId)) {
          throw new Error(`Invalid document ID: ${this.documentId}`);
        }

        // Prepare data in the format expected by the backend
        const commentData = {
          document_id: documentId,
          document_name: comment.document_name,
          version: comment.version,
          reviewer_id: comment.reviewer_id,
          page_no: comment.page_no,
          section: comment.section,
          description: comment.description,
          is_annotation: comment.annotation || false,
          user_role: this.currentUserRole,
        };

        // Add annotation position data if it's an annotation
        if (
          comment.annotation &&
          comment.x !== undefined &&
          comment.y !== undefined
        ) {
          commentData.x = comment.x;
          commentData.y = comment.y;
        }

        console.log("Sending comment data to backend:", commentData);
        console.log("Annotation data:", {
          is_annotation: commentData.is_annotation,
          x: commentData.x,
          y: commentData.y,
          page_no: commentData.page_no,
        });

        const response = await fetch("http://localhost:8000/api/comments", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(commentData),
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.message || "Failed to save comment");
        }

        const result = await response.json();
        console.log("Comment saved successfully:", result);

        // Reload comments from backend to get the correct IDs
        await this.loadCommentsFromBackend();

        // Reload all comments for the project to update upload restrictions
        await this.loadAllCommentsForProject();

        // Force update of upload restrictions
        this.$forceUpdate();
      } catch (error) {
        console.error("Error saving comment:", error);
        alert(`Failed to save comment: ${error.message}`);
      }
    },

    async loadCommentsFromBackend() {
      try {
        if (!this.documentId) {
          console.log("No document number available for loading comments");
          return;
        }

        const response = await fetch(
          `http://localhost:8000/api/comments?document_id=${this.documentId}`
        );

        if (response.ok) {
          const data = await response.json();
          this.comments = data.comments || [];
          this.annotations = data.annotations || [];
          console.log(
            `Loaded ${this.comments.length} comments and ${this.annotations.length} annotations`
          );
        } else {
          console.warn(
            `Failed to load comments: ${response.status} ${response.statusText}`
          );
          // Don't show error to user as comments are optional
        }
      } catch (error) {
        console.warn(
          "Error loading comments (optional feature):",
          error.message
        );
        // Don't show error to user as comments are optional
      }
    },

    async loadAllCommentsForProject() {
      try {
        this.loadingAllComments = true;
        console.log(
          "loadAllCommentsForProject called with LRU ID:",
          this.documentDetails.lruId
        );

        if (!this.documentDetails.lruId) {
          console.log("No LRU ID available for loading all comments");
          return;
        }

        // Get all documents for this LRU/project
        const documentsResponse = await fetch(
          `http://localhost:8000/api/lrus/${this.documentDetails.lruId}/plan-documents`
        );
        console.log("Documents response status:", documentsResponse.status);

        if (!documentsResponse.ok) {
          console.warn("Failed to load documents for comment checking");
          return;
        }

        const documentsData = await documentsResponse.json();
        console.log("Documents data:", documentsData);

        if (!documentsData.success || !documentsData.documents) {
          console.warn("No documents found for comment checking");
          return;
        }

        console.log("Found documents:", documentsData.documents.length);

        // Load comments for all documents
        const allComments = [];
        for (const doc of documentsData.documents) {
          console.log("Loading comments for document:", doc.document_id);
          try {
            const commentsResponse = await fetch(
              `http://localhost:8000/api/comments?document_id=${doc.document_id}`
            );
            if (commentsResponse.ok) {
              const commentsData = await commentsResponse.json();
              console.log(
                "Comments data for doc",
                doc.document_id,
                ":",
                commentsData
              );
              if (commentsData.success && commentsData.comments) {
                allComments.push(...commentsData.comments);
                console.log(
                  "Added",
                  commentsData.comments.length,
                  "comments for document",
                  doc.document_id
                );
              }
            }
          } catch (error) {
            console.warn(
              `Failed to load comments for document ${doc.document_id}:`,
              error
            );
          }
        }

        this.allComments = allComments;
        console.log(
          `Loaded ${allComments.length} total comments across all documents in project`
        );
        console.log("All comments:", allComments);

        // Log upload restriction status after loading comments
        const pendingComments = allComments.filter((comment) => {
          const status = comment.status?.toString().toLowerCase();
          return (
            !status ||
            status === "pending" ||
            status === "rejected" ||
            status === "none" ||
            status === "null"
          );
        });
        console.log(
          `Upload restriction status: ${
            pendingComments.length > 0 ? "DISABLED" : "ENABLED"
          } (${pendingComments.length} non-accepted comments)`
        );
      } catch (error) {
        console.warn("Error loading all comments for project:", error.message);
      } finally {
        this.loadingAllComments = false;
      }
    },

    // Debug method - can be called from browser console
    debugUploadStatus() {
      console.log("=== UPLOAD STATUS DEBUG ===");
      console.log("existingDocuments.length:", this.existingDocuments.length);
      console.log("allComments.length:", this.allComments?.length || 0);
      console.log("comments (current doc) length:", this.comments?.length || 0);
      console.log("loadingAllComments:", this.loadingAllComments);
      console.log("canUploadDocument:", this.canUploadDocument);
      console.log(
        "hasPendingCommentsInProject:",
        this.hasPendingCommentsInProject
      );

      if (this.allComments && this.allComments.length > 0) {
        console.log("All comments:", this.allComments);
        const pendingComments = this.allComments.filter((comment) =>
          this.isCommentPending(comment)
        );
        console.log(
          "Pending comments (using isCommentPending):",
          pendingComments
        );
      }

      if (this.comments && this.comments.length > 0) {
        console.log("Current document comments:", this.comments);
        const currentDocPending = this.comments.filter((comment) =>
          this.isCommentPending(comment)
        );
        console.log("Current document pending comments:", currentDocPending);
      }

      console.log("=== END DEBUG ===");
    },

    // Manual reload method - can be called from browser console
    async manualReloadComments() {
      console.log("Manually reloading all comments...");
      await this.loadAllCommentsForProject();
      console.log("Reload complete. Upload status:", this.canUploadDocument);
    },

    // Debug method to check latest document comments specifically
    debugLatestDocumentComments() {
      console.log("=== LATEST DOCUMENT COMMENTS DEBUG ===");

      if (this.existingDocuments.length === 0) {
        console.log("No documents exist");
        return;
      }

      const latestDocument = this.existingDocuments[0];
      console.log("Latest document:", latestDocument);

      if (!this.allComments || this.allComments.length === 0) {
        console.log("No comments loaded");
        return;
      }

      const latestDocumentComments = this.allComments.filter(
        (comment) =>
          comment.document_id == latestDocument.document_id ||
          comment.document_id === latestDocument.document_number
      );

      console.log("Comments for latest document:", latestDocumentComments);

      latestDocumentComments.forEach((comment, index) => {
        console.log(`Comment ${index + 1}:`, {
          id: comment.id,
          document_id: comment.document_id,
          status: comment.status,
          description: comment.description,
          created_at: comment.created_at,
        });
      });

      const pendingComments = latestDocumentComments.filter(
        (comment) =>
          comment.status !== "accepted" && comment.status !== "rejected"
      );

      console.log("Pending comments:", pendingComments);
      console.log("Should upload be enabled:", pendingComments.length === 0);
      console.log("=== END DEBUG ===");
    },

    // Force refresh upload status
    async forceRefreshUploadStatus() {
      console.log("Force refreshing upload status...");
      await this.loadAllCommentsForProject();
      console.log("Current upload status:", this.canUploadDocument);
      console.log(
        "hasPendingCommentsInProject:",
        this.hasPendingCommentsInProject
      );
    },

    // Force enable upload for testing
    forceEnableUpload() {
      console.log("Force enabling upload for testing...");
      this.allComments = []; // Clear all comments to force enable
      console.log("Upload should now be enabled:", this.canUploadDocument);
    },

    // Test method - can be called from browser console
    testCommentAndAnnotation() {
      console.log("Testing comment and annotation functionality...");

      // Create a test comment
      const testComment = {
        id: Date.now(),
        document_name: "test-document.pdf",
        document_id: "TEST-001",
        version: "1.0",
        revision: "A",
        page_no: 1,
        section: "Test Section",
        description: "This is a test comment with annotation",
        commented_by: "Test User",
        created_at: new Date().toISOString(),
        annotation: true,
      };

      // Create a test annotation
      const testAnnotation = {
        id: Date.now(),
        x: 50,
        y: 30,
        page: 1,
        description: "This is a test comment with annotation",
        document_id: "TEST-001",
      };

      this.comments.push(testComment);
      this.annotations.push(testAnnotation);

      console.log("Test comment added:", testComment);
      console.log("Test annotation added:", testAnnotation);
      console.log("Total comments:", this.comments.length);
      console.log("Total annotations:", this.annotations.length);
    },

    // Simple test method to add a comment directly
    addTestComment() {
      const testComment = {
        id: Date.now(),
        document_name: "test-document.pdf",
        document_id: "TEST-001",
        version: "1.0",
        revision: "A",
        page_no: 1,
        section: "Test Section",
        description: "This is a simple test comment",
        commented_by: "Test User",
        created_at: new Date().toISOString(),
        annotation: false,
      };

      this.comments.push(testComment);
      console.log("Simple test comment added:", testComment);
      console.log("Comments array length:", this.comments.length);
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

    // (duplicate removed) loadExistingDocuments is defined earlier
  },

  beforeUnmount() {
    if (this.pdfUrl) {
      URL.revokeObjectURL(this.pdfUrl);
    }
  },
};
</script>

<style scoped>
.pdf-viewer-container {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
    Ubuntu, sans-serif;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f5f5;
}

/* Header Section */
.document-header {
  background: #ebf7fd;
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

.status-pending {
  color: #f59e0b;
}
.status-approved {
  color: #10b981;
}
.status-reject {
  color: #ef4444;
}
.status-review {
  color: #3b82f6;
}

/* Action Bar */
.action-bar {
  background: white;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  justify-content: center; /* Center the items horizontally */
  align-items: center; /* Align items vertically in the center */
  gap: 1rem; /* Space between buttons */
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

.action-btn-edit {
  background-color: #3182ce;
}

.action-btn-edit:hover {
  background-color: #2c5aa0;
}

.action-btn:disabled {
  background-color: #a0aec0;
  cursor: not-allowed;
  opacity: 0.7;
}

.reviewer-info {
  display: flex;
  align-items: center;
  margin-right: 15px;
  padding: 8px 12px;
  background-color: #f7fafc;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
}

.reviewer-label {
  font-weight: 600;
  color: #4a5568;
  margin-right: 8px;
}

.reviewer-name {
  color: #2d3748;
  font-weight: 500;
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

  /* Center horizontally */
  display: block;
  margin: 0 auto;
  text-align: center;
}

.upload-btn:hover {
  background: #059669;
}

.upload-btn.disabled {
  background: #6b7280;
  cursor: not-allowed;
  opacity: 0.6;
}

.upload-btn.disabled:hover {
  background: #6b7280;
}

.delete-section {
  margin-top: 1rem;
  padding: 1rem;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 8px;
}

.delete-btn {
  display: inline-block;
  padding: 0.5rem 1rem;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  text-align: center;
  transition: background-color 0.2s;
}

.delete-btn:hover:not(:disabled) {
  background: #dc2626;
}

.delete-btn:disabled {
  background: #9ca3af;
  cursor: not-allowed;
  opacity: 0.6;
}

.delete-warning {
  margin-top: 0.5rem;
  font-size: 0.75rem;
  color: #dc2626;
}

.upload-restriction-message {
  margin-top: 1rem;
  padding: 1rem;
  background: #fef3c7;
  border: 1px solid #f59e0b;
  border-radius: 0.5rem;
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  /* width: 50%; */
}

.restriction-icon {
  font-size: 1.25rem;
  flex-shrink: 0;
}

.restriction-text p {
  margin: 0;
  font-size: 0.875rem;
  line-height: 1.4;
}

.restriction-text p:first-child {
  font-weight: 600;
  color: #92400e;
}

.restriction-text p:not(:first-child) {
  color: #78350f;
  margin-top: 0.25rem;
}

.upload-available-message {
  margin-top: 1rem;
  padding: 1rem;
  background: #d1fae5;
  border: 1px solid #10b981;
  border-radius: 0.5rem;
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.success-icon {
  font-size: 1.25rem;
  flex-shrink: 0;
}

.success-text p {
  margin: 0;
  font-size: 0.875rem;
  line-height: 1.4;
}

.success-text p:first-child {
  font-weight: 600;
  color: #065f46;
}

.success-text p:not(:first-child) {
  color: #047857;
  margin-top: 0.25rem;
}

.comment-restriction-message {
  margin-top: 1rem;
  padding: 1rem;
  background: #e0f2fe;
  border: 1px solid #0284c7;
  border-radius: 0.5rem;
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.comment-restriction-message .restriction-text p {
  margin: 0;
  font-size: 0.875rem;
  line-height: 1.4;
}

.comment-restriction-message .restriction-text p:first-child {
  font-weight: 600;
  color: #0c4a6e;
}

.comment-restriction-message .restriction-text p:not(:first-child) {
  color: #075985;
  margin-top: 0.25rem;
}

.doc-label {
  display: inline-block;
  background: #3b82f6;
  color: white;
  font-weight: bold;
  padding: 0.125rem 0.375rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  margin-right: 0.5rem;
}

.accepted-badge {
  display: inline-block;
  background: #10b981;
  color: white;
  font-weight: bold;
  padding: 0.125rem 0.375rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  margin-left: 0.5rem;
  animation: pulse 2s infinite;
}

.current-badge {
  display: inline-block;
  background: #3b82f6;
  color: white;
  font-weight: bold;
  padding: 0.125rem 0.375rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  margin-left: 0.5rem;
  animation: pulse 2s infinite;
}

.current-document {
  border: 2px solid #3b82f6 !important;
  background: #eff6ff !important;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15) !important;
}

@keyframes pulse {
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
  100% {
    opacity: 1;
  }
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
  gap: 1rem;
  padding: 1rem;
  min-height: 0; /* Allow container to shrink */
  position: relative; /* For absolute positioning if needed */
  background-color: #ebf7fd;
}

.document-area {
  flex: 3; /* Takes up 3 parts of the 5 total parts */
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  min-height: 0; /* Allow container to shrink */
  overflow: auto; /* Add scroll to document area */
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
  height: 100%;
  background: #f8fafc;
  overflow-y: auto; /* Enable scrolling for DOCX content */
  position: relative; /* Needed so overlay positions correctly */
}

.docx-render-root {
  position: relative;
  z-index: 1;
}

.docx-content .page {
  background: white;
  padding: 2rem;
  margin: 1rem auto;
  max-width: 816px; /* A4 width at 96 DPI */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* Match PDF page shadow */
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

.documents-list-panel {
  background-color: #ebf7fd;
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
  overflow: hidden;
  word-wrap: break-word;
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
  font-weight: 800;
  word-wrap: break-word;
  word-break: break-word;
  overflow-wrap: break-word;
  white-space: pre-wrap;
  max-width: 100%;
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

/* Enhanced Comment System Styles */
.add-comment-section {
  margin-top: 1rem;
}

.button-group {
  display: flex;
  gap: 0.75rem;
}

.add-comment-btn {
  flex: 1;
  padding: 0.75rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background 0.2s;
}

.add-comment-btn:hover {
  background: #2563eb;
}

.accept-document-btn {
  flex: 1;
  padding: 0.75rem;
  background: #10b981;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background 0.2s;
}

.accept-document-btn:hover {
  background: #059669;
}

/* Comment Form Modal */
.comment-form-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.comment-form-container {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  max-height: 65vh;
  overflow-y: auto;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.comment-form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.comment-form-header h4 {
  margin: 0;
  color: #333;
  font-size: 1.25rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6b7280;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #374151;
}

.comment-form-body {
  padding: 1.5rem;
}

.form-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.form-group {
  flex: 1;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #374151;
  font-weight: 500;
  font-size: 0.9rem;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 0.9rem;
  transition: border-color 0.2s;
}

.form-select {
  background-color: white;
  cursor: pointer;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-group input[readonly] {
  background: #f9fafb;
  color: #6b7280;
  cursor: not-allowed;
}

.comment-form-footer {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
  padding: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.cancel-btn,
.annotation-btn,
.submit-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.cancel-btn {
  background: #f3f4f6;
  color: #374151;
}

.cancel-btn:hover {
  background: #e5e7eb;
}

.annotation-btn {
  background: #f59e0b;
  color: white;
}

.annotation-btn:hover {
  background: #d97706;
}

.submit-btn {
  background: #10b981;
  color: white;
}

.submit-btn:hover:not(:disabled) {
  background: #059669;
}

.submit-btn:disabled,
.annotation-btn:disabled {
  background: #d1d5db;
  cursor: not-allowed;
}

/* Enhanced Comment Display */
.comment-item {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 0.75rem;
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  overflow: hidden;
  word-wrap: break-word;
}

.comment-header {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  margin-bottom: 0.5rem;
  padding-right: 2rem; /* Space for delete button */
}

.comment-commented_by {
  font-weight: 600;
  color: #374151;
  font-size: 0.9rem;
}

.comment-date {
  color: #6b7280;
  font-size: 0.8rem;
}

.comment-content {
  margin-bottom: 0.5rem;
  overflow: hidden;
  word-wrap: break-word;
}

.comment-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 0.5rem;
  font-size: 0.8rem;
  color: #6b7280;
}

.comment-text {
  color: #4b5563;
  font-size: 0.9rem;
  line-height: 1.5;
  margin: 0;
  word-wrap: break-word;
  word-break: break-word;
  overflow-wrap: break-word;
  white-space: pre-wrap;
  max-width: 100%;
}

.annotation-info {
  margin-top: 0.5rem;
}

.annotation-marker {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  background: #fef3c7;
  color: #92400e;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
}

/* Delete Button - Absolute Position in Top Right Corner */
.delete-btn {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 0.375rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  z-index: 10;
}

.delete-btn:hover {
  background: #fee2e2;
  border-color: #fca5a5;
  color: #b91c1c;
  transform: scale(1.05);
}

.delete-btn:active {
  transform: scale(0.95);
}

/* Delete Confirmation Modal */
.delete-confirm-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.delete-confirm-modal {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1),
    0 10px 10px -5px rgba(0, 0, 0, 0.04);
  overflow: hidden;
}

.delete-confirm-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  background: #fef2f2;
}

.delete-confirm-header h4 {
  margin: 0;
  color: #dc2626;
  font-size: 1.25rem;
  font-weight: 600;
}

.delete-confirm-body {
  padding: 1.5rem;
  text-align: center;
}

.warning-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.delete-confirm-body p {
  margin: 0 0 1rem 0;
  color: #374151;
  font-size: 1rem;
}

.comment-preview {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1rem;
  margin: 1rem 0;
  text-align: left;
}

.comment-text-preview {
  font-style: italic;
  color: #6b7280;
  margin: 0.5rem 0;
  padding: 0.5rem;
  background: white;
  border-radius: 4px;
  border: 1px solid #e5e7eb;
}

.comment-meta-preview {
  display: flex;
  gap: 1rem;
  font-size: 0.9rem;
  color: #6b7280;
}

.warning-text {
  color: #dc2626;
  font-weight: 500;
  font-size: 0.9rem;
}

.delete-confirm-footer {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
  padding: 1.5rem;
  border-top: 1px solid #e5e7eb;
  background: #f9fafb;
}

.delete-confirm-btn {
  background: #dc2626;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: background 0.2s;
}

.delete-confirm-btn:hover {
  background: #b91c1c;
}

.delete-confirm-btn:active {
  transform: scale(0.98);
}

/* Annotation System Styles */
.pdf-page-wrapper {
  position: relative;
  margin-bottom: 1.5rem;
}

.annotation-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  z-index: 10;
}

.annotation-marker {
  position: absolute;
  pointer-events: all;
  cursor: pointer;
  z-index: 20;
}

.annotation-circle {
  width: 24px;
  height: 24px;
  background: #ef4444;
  border: 2px solid white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: bold;
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  transition: transform 0.2s;
}

.annotation-circle:hover {
  transform: scale(1.2);
}

/* Annotation mode indicator */
.doc-container.annotation-mode {
  cursor: crosshair;
}

.annotation-mode-indicator {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  pointer-events: none;
}

.annotation-instruction {
  background: #3b82f6;
  color: white;
  padding: 1rem 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.9rem;
  font-weight: 500;
}

.annotation-icon {
  font-size: 1.2rem;
}

.cancel-annotation-btn {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
  pointer-events: all;
  transition: background 0.2s;
}

.cancel-annotation-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* Document Details Box */
.document-details-box {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.document-details-box h5 {
  margin: 0 0 1rem 0;
  color: #1e293b;
  font-size: 1rem;
  font-weight: 600;
}

.details-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.detail-label {
  font-size: 0.8rem;
  color: #64748b;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.detail-value {
  font-size: 0.9rem;
  color: #1e293b;
  font-weight: 600;
  padding: 0.5rem;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
}

.comment-description {
  resize: vertical;
  min-height: 100px;
}

/* Overlay for track versions modal */
.track-versions-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
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
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
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

.modal-header h2,
.modal-header h3 {
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
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
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

.star-button,
.delete-button {
  background: none;
  border: none;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.star-button:hover,
.delete-button:hover {
  transform: scale(1.2);
}

/* Comments Section Styles */
.comments-section {
  flex: 2;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
  padding: 1.75rem;
  min-width: 300px;
  max-width: 450px;
  height: calc(100vh - 200px);
  align-self: flex-start;
  position: sticky;
  top: 1rem;
}

.comments-section::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(to right, #3b82f6, #10b981);
  border-radius: 16px 16px 0 0;
}

/* Comments Header */
.comments-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1.25rem;
  border-bottom: 2px solid #f3f4f6;
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
  content: "";
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

/* Comments List */
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
  overflow: hidden;
  word-wrap: break-word;
}

.comment-item:hover {
  background: #f3f4f6;
}

.comment-item.comment-resolved {
  border-left: 4px solid #10b981;
}

/* Comment Components */
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

.comment-commented_by {
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

/* Status Styles */
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

.status-reject {
  background: #fee2e2;
  color: #dc2626;
}

/* Comment Content and Actions */
.comment-content {
  color: #1f2937;
  margin-bottom: 1rem;
  line-height: 1.5;
  overflow: hidden;
  word-wrap: break-word;
}

.comment-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn.accept {
  background: #10b981;
  color: white;
}

.action-btn.reject {
  background: #ef4444;
  color: white;
}

/* Comment Response */
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

/* Modal Styles */
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

/* Animation */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Justification Modal Styles */
.justification-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.justification-modal {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1),
    0 10px 10px -5px rgba(0, 0, 0, 0.04);
  overflow: hidden;
  animation: fadeIn 0.3s ease;
}

.justification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  background: #f8fafc;
}

.justification-header h4 {
  margin: 0;
  color: #1f2937;
  font-size: 1.25rem;
  font-weight: 600;
}

.justification-body {
  padding: 1.5rem;
}

.justification-body .form-group {
  margin-top: 1rem;
}

.justification-body .form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #374151;
  font-weight: 500;
  font-size: 0.9rem;
}

.justification-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.9rem;
  resize: vertical;
  min-height: 100px;
  transition: border-color 0.2s;
}

.justification-textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.justification-footer {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
  padding: 1.5rem;
  border-top: 1px solid #e5e7eb;
  background: #f9fafb;
}

.confirm-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.2s;
}

.confirm-btn.accept {
  background: #10b981;
  color: white;
}

.confirm-btn.accept:hover:not(:disabled) {
  background: #059669;
}

.confirm-btn.reject {
  background: #ef4444;
  color: white;
}

.confirm-btn.reject:hover:not(:disabled) {
  background: #dc2626;
}

.confirm-btn:disabled {
  background: #d1d5db;
  color: #9ca3af;
  cursor: not-allowed;
}

/* Comment Status Styles */
.comment-item.status-accepted {
  border-left: 4px solid #10b981;
  background: #f0fdf4;
}

.comment-item.status-rejected {
  border-left: 4px solid #ef4444;
  background: #fef2f2;
}

.comment-item.status-pending {
  border-left: 4px solid #f59e0b;
  background: #fffbeb;
}

.comment-status {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
  text-transform: capitalize;
}

.status-accepted {
  background: #d1fae5;
  color: #059669;
}

.status-reject {
  background: #fee2e2;
  color: #dc2626;
}

.status-pending {
  background: #fef3c7;
  color: #d97706;
}

/* Comment Actions */
.comment-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.75rem;
}

.action-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 500;
  transition: all 0.2s;
}

.action-btn.accept {
  background: #10b981;
  color: white;
}

.action-btn.accept:hover {
  background: #059669;
}

.action-btn.reject {
  background: #ef4444;
  color: white;
}

.action-btn.reject:hover {
  background: #dc2626;
}

/* Comment Response */
.comment-response {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}

.response-header {
  font-weight: 500;
  color: #4b5563;
  margin-bottom: 0.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.response-date {
  font-size: 0.8rem;
  color: #6b7280;
  font-weight: normal;
}

.response-content {
  color: #6b7280;
  font-size: 0.95rem;
  line-height: 1.5;
  background: #f9fafb;
  padding: 0.75rem;
  border-radius: 4px;
  border: 1px solid #e5e7eb;
}
</style>
ts
