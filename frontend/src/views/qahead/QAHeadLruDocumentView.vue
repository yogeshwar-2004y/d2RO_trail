<template>
  <div class="lru-document-view">
    <!-- Fixed Navigation Bar -->
    <div class="fixed-nav-bar">
      <div class="nav-left">
        <button class="back-button" @click="$router.go(-1)">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19 12H5"></path>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
        </button>
        <img src="@/assets/images/aviatrax-logo.png" alt="Aviatrax Logo" class="app-logo">
      </div>
      
      <div class="nav-center">
        <div class="nav-actions">
          <button class="nav-action-btn assign-reviewer" @click="assignReviewer">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
              <circle cx="9" cy="7" r="4"></circle>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>
            ASSIGN REVIEWER
          </button>
          
          <button class="nav-action-btn view-observations" @click="viewObservations">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="11" cy="11" r="8"></circle>
              <path d="M21 21l-4.35-4.35"></path>
            </svg>
            VIEW OBSERVATIONS
          </button>
          
          <button class="nav-action-btn track-versions" @click="trackVersions">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
              <line x1="16" y1="13" x2="8" y2="13"></line>
              <line x1="16" y1="17" x2="8" y2="17"></line>
              <line x1="10" y1="9" x2="8" y2="9"></line>
            </svg>
            TRACK VERSIONS
          </button>
        </div>
      </div>
      
      <div class="nav-right">
        <!-- Plus button removed -->
      </div>
    </div>

    <!-- Document Content Area -->
    <div class="document-content">
      <div class="document-header">
        <h1 class="document-title">LRU Document: {{ lruName }}</h1>
        <p class="document-subtitle">Project: {{ projectName }}</p>
      </div>
      
      <div class="document-body">
        <div class="document-section">
          <h2>Document Information</h2>
          <div class="info-grid">
            <div class="info-item">
              <label>Document ID:</label>
              <span>{{ lruName }}</span>
            </div>
            <div class="info-item">
              <label>Status:</label>
              <span class="status-badge" :class="lruStatus.toLowerCase().replace(/ /g, '-')">
                {{ lruStatus }}
              </span>
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
        
        <div class="document-section">
          <h2>Document Content</h2>
          <div class="content-placeholder">
            <p>This is where the actual LRU document content would be displayed.</p>
            <p>The document could contain technical specifications, diagrams, requirements, or any other relevant information.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Assign Reviewer Modal -->
    <QAHeadAssignReviewer 
      v-if="showAssignReviewerModal"
      :lru-name="lruName"
      :project-name="projectName"
      @close="showAssignReviewerModal = false"
    />
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
      showAssignReviewerModal: false
    };
  },
  mounted() {
    // Get LRU name and project name from route params
    this.lruName = this.$route.params.lruName || 'Unknown LRU';
    this.projectName = this.$route.params.projectName || 'Unknown Project';
    
    // Set sample data (in real app, this would come from API)
    this.lruStatus = 'Under Review';
    this.createdDate = '2025-01-15';
    this.lastModified = '2025-01-20';
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
      alert(`Tracking versions for LRU: ${this.lruName}`);
      // Implementation for tracking versions
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
.fixed-nav-bar {
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

.app-logo {
  width: 100px; /* Adjust as needed */
  height: auto;
}

.nav-center {
  flex: 1;
  display: flex;
  justify-content: center;
}

.nav-actions {
  display: flex;
  gap: 20px;
}

.nav-action-btn {
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

.nav-action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  border-color: #007bff;
}

.nav-action-btn svg {
  color: #6c757d;
}

.nav-right {
  display: flex;
  align-items: center;
}

/* Document Content Area */
.document-content {
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

.document-subtitle {
  font-size: 1.2em;
  color: #6c757d;
  margin: 0;
}

.document-section {
  margin-bottom: 40px;
}

.document-section h2 {
  color: #495057;
  border-bottom: 1px solid #dee2e6;
  padding-bottom: 10px;
  margin-bottom: 20px;
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

.status-badge.under-review {
  background-color: #fff3cd;
  color: #856404;
}

.status-badge.cleared {
  background-color: #d4edda;
  color: #155724;
}

.status-badge.disapproved {
  background-color: #f8d7da;
  color: #721c24;
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

/* Responsive Design */
@media (max-width: 768px) {
  .fixed-nav-bar {
    padding: 0 15px;
  }
  
  .nav-actions {
    gap: 10px;
  }
  
  .nav-action-btn {
    padding: 8px 12px;
    font-size: 0.9em;
  }
  
  .document-content {
    margin: 100px 10px 10px 10px;
    padding: 20px;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
}
</style>
