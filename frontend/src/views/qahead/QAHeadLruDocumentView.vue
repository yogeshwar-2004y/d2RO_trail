<template>
  <div class="lru-document-view">
    <!-- Fixed Navigation Bar -->
    <div class="nav-bar">
      <div class="nav-left">
        <button class="back-button" @click="$router.go(-1)">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19 12H5"></path>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
        </button>
        <img src="@/assets/images/aviatrax-logo.png" alt="Aviatrax Logo" class="logo">
      </div>
      
      <div class="nav-center">
        <button class="nav-button" @click="assignReviewer">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
            <circle cx="9" cy="7" r="4"></circle>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
          </svg>
          ASSIGN REVIEWER
        </button>
        
        <button class="nav-button" @click="viewObservations">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
            <circle cx="12" cy="12" r="3"></circle>
          </svg>
          VIEW OBSERVATIONS
        </button>
        
        <button class="nav-button" @click="trackVersions">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path>
            <rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect>
            <path d="M9 14l2 2 4-4"></path>
          </svg>
          TRACK VERSIONS
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <div class="document-header">
        <h1 class="document-title">{{ lruName }}</h1>
        <p class="project-name">Project: {{ projectName }}</p>
      </div>

      <div class="document-info">
        <div class="info-grid">
          <div class="info-item">
            <label>Document ID:</label>
            <span>{{ lruName }}-001</span>
          </div>
          <div class="info-item">
            <label>Status:</label>
            <span class="status-badge" :class="getStatusClass(lruStatus)">{{ lruStatus }}</span>
          </div>
          <div class="info-item">
            <label>Created Date:</label>
            <span>{{ createdDate }}</span>
          </div>
          <div class="info-item">
            <label>Last Modified:</label>
            <span>{{ lastModified }}</span>
          </div>
        </div>
      </div>

      <div class="document-content">
        <div class="content-section">
          <h3>Document Content</h3>
          <p>This is the main content area for the LRU document. The content will be displayed here based on the selected version.</p>
        </div>
        
        <div class="content-section">
          <h3>Assumptions</h3>
          <ul>
            <li>All function requirements are clearly defined</li>
            <li>Development environment is properly configured</li>
            <li>Necessary resources are available</li>
            <li>Existing ER diagrams are up to date</li>
            <li>Key project stakeholders are identified</li>
          </ul>
        </div>
        
        <div class="content-section">
          <h3>Communication</h3>
          <ul>
            <li>Weekly team meetings</li>
            <li>Bi-weekly stakeholder meetings</li>
            <li>Email updates for critical changes</li>
            <li>Maintenance of a central project documentation repository</li>
          </ul>
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
import QAHeadAssignReviewer from './QAHeadAssignReviewer.vue'

export default {
  name: 'QAHeadLruDocumentView',
  components: {
    QAHeadAssignReviewer
  },
  data() {
    return {
      lruName: '',
      projectName: '',
      lruStatus: '',
      createdDate: '',
      lastModified: '',
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
      ]
    };
  },
  mounted() {
    this.lruName = this.$route.params.lruName || 'Unknown LRU';
    this.projectName = this.$route.params.projectName || 'Unknown Project';
    this.lruStatus = 'Under Review'; // Sample data
    this.createdDate = '2025-01-15'; // Sample data
    this.lastModified = '2025-01-20'; // Sample data
  },
  methods: {
    assignReviewer() {
      this.showAssignReviewerModal = true;
    },
    viewObservations() {
      this.$router.push({ 
        name: 'QAHeadViewObservations', 
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
      // Here you would typically load the selected version content
      alert(`Loading version ${version.version} of ${version.projectId}`);
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
    }
  }
};
</script>

<style scoped>
.lru-document-view {
  min-height: 100vh;
  background-color: #f5f5f5;
}

/* Fixed Navigation Bar */
.nav-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 80px;
  background-color: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 30px;
  z-index: 1000;
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 15px;
}

.back-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  transition: background-color 0.3s ease;
}

.back-button:hover {
  background-color: rgba(0, 0, 0, 0.1);
}

.logo {
  width: 100px; /* Adjust as needed */
  height: auto;
}

.nav-center {
  flex: 1;
  display: flex;
  justify-content: center;
  gap: 20px; /* Adjust as needed */
}

.nav-button {
  display: flex;
  align-items: center;
  gap: 8px;
  background: white;
  border: 1px solid #dee2e6;
  border-radius: 25px;
  padding: 12px 20px;
  font-weight: bold;
  color: #495057;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.nav-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  border-color: #007bff;
}

.nav-button svg {
  color: #6c757d;
}

/* Main Content */
.main-content {
  margin-top: 100px;
  padding: 30px;
  background-color: white;
  min-height: calc(100vh - 100px);
  border-radius: 10px;
  margin-left: 20px;
  margin-right: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.document-header {
  text-align: center;
  margin-bottom: 40px;
  padding-bottom: 20px;
  border-bottom: 2px solid #e9ecef;
}

.document-title {
  font-size: 2.5em;
  color: #333;
  margin-bottom: 10px;
}

.project-name {
  font-size: 1.2em;
  color: #6c757d;
  margin: 0;
}

.document-info {
  margin-bottom: 40px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #007bff;
}

.info-item label {
  font-weight: bold;
  color: #495057;
}

.info-item span {
  color: #6c757d;
}

.status-badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.9em;
  font-weight: bold;
  text-transform: uppercase;
}

.status-badge.status-under-review {
  background-color: #fff3cd;
  color: #856404;
}

.status-badge.status-approved {
  background-color: #d4edda;
  color: #155724;
}

.status-badge.status-rejected {
  background-color: #f8d7da;
  color: #721c24;
}

.status-badge.status-pending {
  background-color: #e2e3e5;
  color: #495057;
}

.document-content {
  margin-top: 40px;
}

.content-section {
  margin-bottom: 40px;
}

.content-section h3 {
  color: #495057;
  border-bottom: 1px solid #dee2e6;
  padding-bottom: 10px;
  margin-bottom: 20px;
}

.content-placeholder {
  background-color: #f8f9fa;
  padding: 30px;
  border-radius: 8px;
  border: 2px dashed #dee2e6;
  text-align: center;
  color: #6c757d;
}

.content-placeholder p {
  margin: 10px 0;
  line-height: 1.6;
}

/* Track Versions Modal */
.track-versions-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1001;
}

.track-versions-modal {
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e9ecef;
  background-color: #f8f9fa;
}

.modal-header h2 {
  margin: 0;
  color: #333;
}

.close-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  transition: background-color 0.3s ease;
}

.close-button:hover {
  background-color: rgba(0, 0, 0, 0.1);
}

.modal-content {
  flex-grow: 1;
  overflow-y: auto;
  padding: 20px;
}

.versions-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.version-item {
  display: flex;
  align-items: center;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
  cursor: pointer;
  transition: all 0.3s ease;
}

.version-item:hover {
  background-color: #e9ecef;
  border-color: #007bff;
}

.version-item.disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background-color: #f0f0f0;
  border-color: #e0e0e0;
}

.version-item.favorite {
  border-left: 4px solid #ffc107; /* Yellow color for favorite */
}

.version-icon {
  margin-right: 15px;
  color: #6c757d;
}

.version-info {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.version-id {
  font-weight: bold;
  color: #333;
  font-size: 1.1em;
}

.version-date {
  font-size: 0.9em;
  color: #6c757d;
  display: block;
}

.version-actions {
  display: flex;
  gap: 10px;
  margin-left: 15px;
}

.star-button, .delete-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  transition: background-color 0.3s ease;
  color: #6c757d;
}

.star-button:hover:not(:disabled), .delete-button:hover:not(:disabled) {
  background-color: #e9ecef;
  color: #007bff; /* Highlight color for hover */
}

.star-button:disabled, .delete-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.star-button.starred {
  color: #ffc107; /* Yellow color for starred */
}

/* Delete Confirmation Modal */
.delete-confirm-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1001;
}

.delete-confirm-modal {
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  width: 90%;
  max-width: 450px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e9ecef;
  background-color: #f8f9fa;
}

.modal-header h3 {
  margin: 0;
  color: #333;
}

.modal-content {
  flex-grow: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.confirm-message {
  margin-bottom: 20px;
}

.warning-icon {
  margin-bottom: 15px;
}

.warning-icon svg {
  color: #dc3545; /* Red color for warning */
  width: 60px;
  height: 60px;
}

.confirm-message h4 {
  color: #333;
  margin-bottom: 10px;
}

.confirm-message p {
  color: #6c757d;
  font-size: 0.9em;
  margin-bottom: 15px;
}

.warning-text {
  color: #dc3545;
  font-weight: bold;
}

.modal-actions {
  display: flex;
  gap: 15px;
  width: 100%;
  padding: 0 20px 20px 20px;
}

.btn {
  flex: 1;
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-secondary {
  background-color: #e9ecef;
  color: #495057;
}

.btn-secondary:hover {
  background-color: #dee2e6;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
}

.btn-danger:hover {
  background-color: #c82333;
}

/* Responsive Design */
@media (max-width: 768px) {
  .nav-bar {
    padding: 0 15px;
  }
  
  .nav-center {
    gap: 10px;
  }
  
  .nav-button {
    padding: 8px 12px;
    font-size: 0.9em;
  }

  .main-content {
    margin: 100px 10px 10px 10px;
    padding: 20px;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }

  .track-versions-modal, .delete-confirm-modal {
    width: 95%;
    max-width: 95%;
  }
}
</style>
