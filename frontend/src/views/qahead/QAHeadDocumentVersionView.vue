<template>
  <div class="document-version-view">
    <!-- Header with Back Button and View Observations -->
    <div class="page-header">
      <div class="header-left">
        <button class="back-button" @click="$router.go(-1)">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19 12H5"></path>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
          Back
        </button>
        <div class="document-title">
          <h1>{{ documentVersion.projectId }} {{ documentVersion.version }}</h1>
          <p class="project-name">Project: {{ projectName }}</p>
        </div>
      </div>
      
      <div class="header-right">
        <button class="view-observations-btn" @click="viewObservations">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
            <circle cx="12" cy="12" r="3"></circle>
          </svg>
          VIEW OBSERVATIONS
        </button>
      </div>
    </div>

    <!-- Document Content -->
    <div class="main-content">
      <div class="document-info">
        <div class="info-grid">
          <div class="info-item">
            <label>Document ID:</label>
            <span>{{ documentVersion.projectId }}-{{ documentVersion.version }}</span>
          </div>
          <div class="info-item">
            <label>Version:</label>
            <span class="version-badge">{{ documentVersion.version }}</span>
          </div>
          <div class="info-item">
            <label>Created Date:</label>
            <span>{{ documentVersion.date }}</span>
          </div>
          <div class="info-item">
            <label>Status:</label>
            <span class="status-badge" :class="getStatusClass(documentVersion.status)">
              {{ documentVersion.status }}
            </span>
          </div>
          <div class="info-item">
            <label>Last Modified:</label>
            <span>{{ documentVersion.lastModified }}</span>
          </div>
          <div class="info-item">
            <label>Reviewer:</label>
            <span>{{ documentVersion.reviewer || 'Not Assigned' }}</span>
          </div>
        </div>
      </div>

      <div class="document-content">
        <div class="content-section">
          <h3>Document Content - Version {{ documentVersion.version }}</h3>
          <p>This is the content for version {{ documentVersion.version }} of the document {{ documentVersion.projectId }}.</p>
          <p>The content varies based on the version selected. Each version may contain different updates, corrections, or modifications to the previous version.</p>
        </div>
        
        <div class="content-section">
          <h3>Version History</h3>
          <div class="version-timeline">
            <div class="timeline-item" v-for="(change, index) in documentVersion.changes" :key="index">
              <div class="timeline-date">{{ change.date }}</div>
              <div class="timeline-content">
                <h4>{{ change.title }}</h4>
                <p>{{ change.description }}</p>
                <span class="change-author">By: {{ change.author }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="content-section">
          <h3>Technical Specifications</h3>
          <div class="specs-grid">
            <div class="spec-item">
              <label>Document Type:</label>
              <span>LRU Technical Specification</span>
            </div>
            <div class="spec-item">
              <label>Format:</label>
              <span>PDF/Technical Drawing</span>
            </div>
            <div class="spec-item">
              <label>File Size:</label>
              <span>{{ documentVersion.fileSize || '2.5 MB' }}</span>
            </div>
            <div class="spec-item">
              <label>Pages:</label>
              <span>{{ documentVersion.pages || '15' }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QAHeadDocumentVersionView',
  data() {
    return {
      projectName: '',
      documentVersion: {
        projectId: '',
        version: '',
        date: '',
        status: '',
        lastModified: '',
        reviewer: '',
        fileSize: '',
        pages: '',
        changes: []
      }
    };
  },
  mounted() {
    // Get parameters from route
    this.projectName = this.$route.params.projectName || 'Unknown Project';
    const versionId = this.$route.params.versionId || '';
    
    // Parse version ID (e.g., "PRJ-2025-078-A" -> projectId: "PRJ-2025-078", version: "A")
    if (versionId) {
      const lastDashIndex = versionId.lastIndexOf('-');
      if (lastDashIndex !== -1) {
        this.documentVersion.projectId = versionId.substring(0, lastDashIndex);
        this.documentVersion.version = versionId.substring(lastDashIndex + 1);
      }
    }
    
    // Load document version data
    this.loadDocumentVersion();
  },
  methods: {
    loadDocumentVersion() {
      // In a real application, this would fetch data from an API
      // For now, we'll use sample data based on the version
      const sampleData = this.getSampleVersionData();
      this.documentVersion = { ...this.documentVersion, ...sampleData };
    },
    
    getSampleVersionData() {
      // Sample data for different versions
      const versionData = {
        'A': {
          date: '2025-01-15',
          status: 'Under Review',
          lastModified: '2025-01-15',
          reviewer: 'John Smith',
          fileSize: '2.5 MB',
          pages: '15',
          changes: [
            {
              date: '2025-01-15',
              title: 'Initial Version Created',
              description: 'First draft of the LRU technical specification document',
              author: 'Design Team'
            }
          ]
        },
        'B': {
          date: '2025-01-20',
          status: 'Under Review',
          lastModified: '2025-01-20',
          reviewer: 'Sarah Johnson',
          fileSize: '2.8 MB',
          pages: '16',
          changes: [
            {
              date: '2025-01-20',
              title: 'Technical Specifications Updated',
              description: 'Added detailed technical parameters and requirements',
              author: 'Engineering Team'
            },
            {
              date: '2025-01-18',
              title: 'Initial Version Created',
              description: 'First draft of the LRU technical specification document',
              author: 'Design Team'
            }
          ]
        },
        'C': {
          date: '2025-01-25',
          status: 'Under Review',
          lastModified: '2025-01-25',
          reviewer: 'Mike Wilson',
          fileSize: '3.1 MB',
          pages: '18',
          changes: [
            {
              date: '2025-01-25',
              title: 'Quality Assurance Review',
              description: 'QA team review completed with minor corrections',
              author: 'QA Team'
            },
            {
              date: '2025-01-20',
              title: 'Technical Specifications Updated',
              description: 'Added detailed technical parameters and requirements',
              author: 'Engineering Team'
            },
            {
              date: '2025-01-18',
              title: 'Initial Version Created',
              description: 'First draft of the LRU technical specification document',
              author: 'Design Team'
            }
          ]
        },
        'D': {
          date: '2025-01-30',
          status: 'Under Review',
          lastModified: '2025-01-30',
          reviewer: 'Lisa Brown',
          fileSize: '3.2 MB',
          pages: '19',
          changes: [
            {
              date: '2025-01-30',
              title: 'Final Review Phase',
              description: 'Final review and approval process initiated',
              author: 'Review Board'
            },
            {
              date: '2025-01-25',
              title: 'Quality Assurance Review',
              description: 'QA team review completed with minor corrections',
              author: 'QA Team'
            },
            {
              date: '2025-01-20',
              title: 'Technical Specifications Updated',
              description: 'Added detailed technical parameters and requirements',
              author: 'Engineering Team'
            },
            {
              date: '2025-01-18',
              title: 'Initial Version Created',
              description: 'First draft of the LRU technical specification document',
              author: 'Design Team'
            }
          ]
        }
      };
      
      return versionData[this.documentVersion.version] || versionData['A'];
    },
    
    viewObservations() {
      // Navigate to observations page with version-specific parameters
      this.$router.push({
        name: 'QAHeadViewObservations',
        params: {
          lruName: this.documentVersion.projectId,
          projectName: this.projectName,
          versionId: `${this.documentVersion.projectId}-${this.documentVersion.version}`
        }
      });
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
.document-version-view {
  min-height: 100vh;
  background-color: #f8f9fa;
}

/* Page Header */
.page-header {
  background-color: white;
  border-bottom: 1px solid #e9ecef;
  padding: 20px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.back-button {
  display: flex;
  align-items: center;
  gap: 8px;
  background: none;
  border: 1px solid #dee2e6;
  padding: 10px 15px;
  border-radius: 6px;
  cursor: pointer;
  color: #6c757d;
  transition: all 0.3s ease;
}

.back-button:hover {
  background-color: #f8f9fa;
  border-color: #6c757d;
}

.document-title h1 {
  margin: 0;
  color: #333;
  font-size: 1.8em;
}

.project-name {
  margin: 5px 0 0 0;
  color: #6c757d;
  font-size: 1em;
}

.header-right {
  display: flex;
  align-items: center;
}

.view-observations-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  background-color: #333;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.view-observations-btn:hover {
  background-color: #555;
}

/* Main Content */
.main-content {
  padding: 30px;
  max-width: 1200px;
  margin: 0 auto;
}

.document-info {
  background-color: white;
  border-radius: 8px;
  padding: 25px;
  margin-bottom: 30px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.info-item label {
  font-weight: bold;
  color: #495057;
  font-size: 0.9em;
}

.info-item span {
  color: #333;
  font-size: 1em;
}

.version-badge {
  background-color: #e9ecef;
  color: #495057;
  padding: 4px 12px;
  border-radius: 20px;
  font-weight: bold;
  display: inline-block;
  width: fit-content;
}

.status-badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-weight: bold;
  font-size: 0.9em;
  display: inline-block;
  width: fit-content;
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

/* Document Content */
.document-content {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.content-section {
  background-color: white;
  border-radius: 8px;
  padding: 25px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.content-section h3 {
  color: #333;
  border-bottom: 1px solid #dee2e6;
  padding-bottom: 15px;
  margin-bottom: 20px;
}

.content-section p {
  color: #495057;
  line-height: 1.6;
  margin-bottom: 15px;
}

/* Version Timeline */
.version-timeline {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.timeline-item {
  display: flex;
  gap: 20px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 6px;
  border-left: 4px solid #dee2e6;
}

.timeline-date {
  background-color: #6c757d;
  color: white;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 0.9em;
  font-weight: bold;
  min-width: 100px;
  text-align: center;
}

.timeline-content {
  flex-grow: 1;
}

.timeline-content h4 {
  margin: 0 0 8px 0;
  color: #333;
}

.timeline-content p {
  margin: 0 0 8px 0;
  color: #495057;
}

.change-author {
  font-size: 0.9em;
  color: #6c757d;
  font-style: italic;
}

/* Specs Grid */
.specs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.spec-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.spec-item label {
  font-weight: bold;
  color: #495057;
  font-size: 0.9em;
}

.spec-item span {
  color: #333;
  font-size: 1em;
}

/* Responsive Design */
@media (max-width: 768px) {
  .page-header {
    padding: 15px 20px;
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
  
  .header-left {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .main-content {
    padding: 20px;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .specs-grid {
    grid-template-columns: 1fr;
  }
  
  .timeline-item {
    flex-direction: column;
    gap: 15px;
  }
  
  .timeline-date {
    min-width: auto;
    width: fit-content;
  }
}
</style>
