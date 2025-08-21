<template>
  <div class="memo-dashboard">
    <div class="header">
      <div class="header-left">
        <button class="back-button" @click="$router.go(-1)">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19 12H5"></path>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
        </button>
        <img src="@/assets/images/aviatrax-logo.png" alt="AVIATRAX Logo" class="logo">
      </div>
      
      <div class="header-center">
        <button class="submit-memo-button" @click="submitNewMemo">
          <svg class="plus-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="16"></line>
            <line x1="8" y1="12" x2="16" y2="12"></line>
          </svg>
          Submit new MEMO
        </button>
      </div>
      
      <div class="header-right">
        <div class="search-box">
          <input type="text" v-model="searchQuery" placeholder="Search Projects" class="search-input">
          <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </div>
        <div class="filter-dropdown">
          <button class="filter-button" @click="toggleProjectFilter">
            Filter By Projects
          </button>
          <div v-if="showProjectFilter" class="filter-panel">
            <div
              v-for="project in projects"
              :key="project"
              class="filter-option"
              :class="{ 'selected': activeProjectFilter === project }"
              @click="selectProject(project)"
            >
              {{ project }}
            </div>
          </div>
        </div>
        <div class="filter-dropdown">
          <button class="filter-button" @click="toggleMemoFilter">
            Filter Memos
          </button>
          <div v-if="showMemoFilter" class="filter-panel">
            <div
              v-for="status in memoStatuses"
              :key="status.name"
              class="filter-option"
              :class="[status.color, { 'selected': activeMemoFilter === status.name }]"
              @click="selectMemoStatus(status.name)"
            >
              {{ status.name }}
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="memo-list">
      <div v-for="memo in filteredMemos" :key="memo.id" class="memo-card" :class="memo.status.toLowerCase().replace(/ /g, '-')" @click="showMemoDetails(memo)">
        <div class="memo-details">
          <div class="memo-project">{{ memo.project }}</div>
          <div class="memo-author">FROM - AUTHORISING EMP (DESIGN TEAM)</div>
        </div>
        <div class="memo-schedule" v-if="memo.assignedDate">
          <div class="memo-assigned">ASSIGNED ON : {{ memo.assignedDate }}</div>
          <div class="memo-scheduled">TEST SCHEDULED ON : {{ memo.scheduledDate }}</div>
        </div>
      </div>
    </div>

    <!-- Memo Details Modal -->
    <div v-if="showMemoDetails" class="memo-modal-overlay" @click="closeMemoDetails">
      <div class="memo-modal" @click.stop>
        <div class="modal-header">
          <h2>Memo Details - {{ selectedMemo?.project }}</h2>
          <button class="close-button" @click="closeMemoDetails">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        
        <div class="modal-content" v-if="selectedMemo">
          <!-- Basic Memo Info -->
          <div class="memo-info-section">
            <h3>Basic Information</h3>
            <div class="info-grid">
              <div class="info-item">
                <label>Project:</label>
                <span>{{ selectedMemo.project }}</span>
              </div>
              <div class="info-item">
                <label>Status:</label>
                <span>{{ selectedMemo.status }}</span>
              </div>
              <div class="info-item">
                <label>Assigned Date:</label>
                <span>{{ selectedMemo.assignedDate }}</span>
              </div>
              <div class="info-item">
                <label>Scheduled Date:</label>
                <span>{{ selectedMemo.scheduledDate }}</span>
              </div>
            </div>
          </div>

          <!-- Form Data (if available) -->
          <div v-if="selectedMemo.formData" class="form-data-section">
            <h3>DGAQA Inspection Details</h3>
            
            <!-- General Requisition Information -->
            <div class="form-section">
              <h4>General Requisition Information</h4>
              <div class="info-grid">
                <div class="info-item">
                  <label>FROM:</label>
                  <span>{{ selectedMemo.formData.from[0] }} {{ selectedMemo.formData.from[1] }}</span>
                </div>
                <div class="info-item">
                  <label>CASDIC Ref No.:</label>
                  <span>{{ selectedMemo.formData.casdicRef }}</span>
                </div>
                <div class="info-item">
                  <label>CASDIC:</label>
                  <span>{{ selectedMemo.formData.casdic }}</span>
                </div>
                <div class="info-item">
                  <label>Dated:</label>
                  <span>{{ selectedMemo.formData.dated }}</span>
                </div>
                <div class="info-item">
                  <label>TO:</label>
                  <span>{{ selectedMemo.formData.to[0] }} {{ selectedMemo.formData.to[1] }}</span>
                </div>
                <div class="info-item">
                  <label>Wing/Proj Ref No.:</label>
                  <span>{{ selectedMemo.formData.wingProjRef }}</span>
                </div>
                <div class="info-item full-width">
                  <label>Coordinator:</label>
                  <span>{{ selectedMemo.formData.coordinator }}</span>
                </div>
              </div>
            </div>

            <!-- LRU/SRU Details -->
            <div class="form-section">
              <h4>LRU/SRU Details</h4>
              <div class="info-grid">
                <div class="info-item">
                  <label>Part No:</label>
                  <span>{{ selectedMemo.formData.partNo }}</span>
                </div>
                <div class="info-item">
                  <label>Manufacturer:</label>
                  <span>{{ selectedMemo.formData.manufacturer }}</span>
                </div>
                <div class="info-item">
                  <label>Units:</label>
                  <span>{{ selectedMemo.formData.units }}</span>
                </div>
                <div class="info-item">
                  <label>Drawing No/Rev:</label>
                  <span>{{ selectedMemo.formData.drawingNo }}</span>
                </div>
                <div class="info-item">
                  <label>Qty Offered:</label>
                  <span>{{ selectedMemo.formData.qtyOffered }}</span>
                </div>
                <div class="info-item">
                  <label>Source:</label>
                  <span>{{ selectedMemo.formData.source }}</span>
                </div>
              </div>
            </div>

            <!-- Unit Identification -->
            <div class="form-section">
              <h4>Unit Identification & Inspection</h4>
              <div class="info-grid">
                <div class="info-item">
                  <label>Unit Identification:</label>
                  <span>{{ selectedMemo.formData.unitIdentification }}</span>
                </div>
                <div class="info-item">
                  <label>Mechanical Inspection:</label>
                  <span>{{ selectedMemo.formData.mechanicalInspn }}</span>
                </div>
                <div class="info-item">
                  <label>Inspection Stage:</label>
                  <span>{{ selectedMemo.formData.inspectionStage }}</span>
                </div>
                <div class="info-item">
                  <label>STTE Status:</label>
                  <span>{{ selectedMemo.formData.stteStatus }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DesignerMemoPage',
  data() {
    return {
      searchQuery: '',
      showProjectFilter: false,
      showMemoFilter: false,
      activeProjectFilter: null,
      activeMemoFilter: null,
      showMemoDetails: false,
      selectedMemo: null,
      projects: ['PROJ001', 'PROJ002', 'PROJ003', 'PROJ004', 'PROJ005', 'PROJ006'],
      memoStatuses: [
        { name: 'SUCCESSFULLY COMPLETED', color: 'success' },
        { name: 'DISAPPROVED', color: 'disapproved' },
        { name: 'ASSIGNED', color: 'assigned' },
        { name: 'COMPLETED WITH OBSERVATIONS', color: 'observation' },
        { name: 'TEST NOT CONDUCTED', color: 'not-conducted' },
        { name: 'NOT ASSIGNED', color: 'not-assigned' },
      ],
      memos: [
        { id: 1, project: 'PROJ001', author: 'Design Team', assignedDate: '01-07-2025', scheduledDate: '04-07-2025', status: 'NOT ASSIGNED' },
        { id: 2, project: 'PROJ002', author: 'Design Team', assignedDate: '01-07-2025', scheduledDate: '04-07-2025', status: 'ASSIGNED' },
        { id: 3, project: 'PROJ003', author: 'Design Team', assignedDate: null, scheduledDate: null, status: 'NOT ASSIGNED' },
        { id: 4, project: 'PROJ001', author: 'Design Team', assignedDate: '01-07-2025', scheduledDate: '04-07-2025', status: 'SUCCESSFULLY COMPLETED' },
        { id: 5, project: 'PROJ002', author: 'Design Team', assignedDate: '01-07-2025', scheduledDate: '04-07-2025', status: 'DISAPPROVED' },
        { id: 6, project: 'PROJ003', author: 'Design Team', assignedDate: '01-07-2025', scheduledDate: '04-07-2025', status: 'COMPLETED WITH OBSERVATIONS' },
        { id: 7, project: 'PROJ001', author: 'Design Team', assignedDate: '01-07-2025', scheduledDate: '04-07-2025', status: 'TEST NOT CONDUCTED' },
        { id: 8, project: 'PROJ004', author: 'Design Team', assignedDate: '01-07-2025', scheduledDate: '04-07-2025', status: 'SUCCESSFULLY COMPLETED' },
      ],
    };
  },
  mounted() {
    // Check if there's a new memo from the form
    if (this.$route.params.newMemo) {
      try {
        const newMemo = JSON.parse(this.$route.params.newMemo);
        this.addNewMemo(newMemo);
        // Clear the route params
        this.$router.replace({ name: 'DesignerMemo' });
      } catch (error) {
        console.error('Error parsing new memo:', error);
      }
    }
  },
  computed: {
    filteredMemos() {
      let filtered = this.memos;

      if (this.activeProjectFilter) {
        filtered = filtered.filter(memo => memo.project === this.activeProjectFilter);
      }

      if (this.activeMemoFilter) {
        filtered = filtered.filter(memo => memo.status === this.activeMemoFilter);
      }

      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(memo => memo.project.toLowerCase().includes(query));
      }

      return filtered;
    },
  },
  methods: {
    toggleProjectFilter() {
      this.showProjectFilter = !this.showProjectFilter;
      this.showMemoFilter = false;
    },
    toggleMemoFilter() {
      this.showMemoFilter = !this.showMemoFilter;
      this.showProjectFilter = false;
    },
    selectProject(project) {
      this.activeProjectFilter = this.activeProjectFilter === project ? null : project;
      this.showProjectFilter = false;
    },
    selectMemoStatus(status) {
      this.activeMemoFilter = this.activeMemoFilter === status ? null : status;
      this.showMemoFilter = false;
    },
    submitNewMemo() {
      // Navigate to the new memo form
      this.$router.push({ name: 'DesignerNewMemo' });
    },
    addNewMemo(newMemo) {
      // Add the new memo to the beginning of the list
      this.memos.unshift(newMemo);
    },
    showMemoDetails(memo) {
      this.selectedMemo = memo;
      this.showMemoDetails = true;
    },
    closeMemoDetails() {
      this.showMemoDetails = false;
      this.selectedMemo = null;
    }
  }
};
</script>

<style scoped>
.memo-dashboard {
  font-family: Arial, sans-serif;
  min-height: 100vh;
  background-color: #f0f0f0;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 10;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
  flex: 1;
}

.header-center {
  display: flex;
  justify-content: center;
  align-items: center;
  flex: 1;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
  flex: 1;
  justify-content: flex-end;
}

.back-button {
  background: none;
  border: none;
  cursor: pointer;
}

.logo {
  width: 150px;
}

.header-center {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
}

.submit-memo-button {
  background: #007bff;
  color: #fff;
  border: none;
  border-radius: 25px;
  padding: 10px 20px;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: background-color 0.2s;
}

.submit-memo-button:hover {
  background-color: #0056b3;
}

.plus-icon {
  color: #fff;
}

.search-box {
  position: relative;
}

.search-input {
  padding: 10px 15px;
  padding-left: 40px;
  border: 1px solid #ccc;
  border-radius: 25px;
}

.search-icon {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #888;
}

.filter-dropdown {
  position: relative;
}

.filter-button {
  background: #f0f0f0;
  border: 1px solid #ccc;
  border-radius: 20px;
  padding: 10px 15px;
  font-weight: bold;
  cursor: pointer;
}

.filter-panel {
  position: absolute;
  top: 100%;
  left: 0;
  margin-top: 10px;
  width: 250px;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  padding: 10px;
  z-index: 5;
}

.filter-option {
  padding: 15px;
  margin-bottom: 5px;
  border-radius: 8px;
  font-weight: bold;
  color: #000;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
  text-align: center;
}

.filter-option:hover {
  transform: translateY(-2px);
}

.filter-option.selected {
  border: 2px solid #007bff;
}

/* Status-based colors for Memo Cards - Updated to very light pastel shades */
.success, .successfully-completed {
  background-color: #f5f5dc; /* Very Light Yellow/Beige */
}
.disapproved {
  background-color: #ffe4e1; /* Very Light Red/Salmon */
}
.assigned {
  background-color: #e6f3ff; /* Very Light Blue */
}
.observation, .completed-with-observations {
  background-color: #f0e6ff; /* Very Light Purple */
}
.not-conducted, .test-not-conducted {
  background-color: #ffe6f0; /* Very Light Pink */
}
.not-assigned {
  background-color: #fff2e6; /* Very Light Orange/Peach */
}

.memo-list {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.memo-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  color: #000;
  cursor: pointer;
  transition: all 0.3s ease;
}

.memo-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.memo-details {
  flex-grow: 1;
}

.memo-project {
  font-weight: bold;
  font-size: 1.1em;
}

.memo-author {
  font-size: 0.9em;
  color: #555;
}

.memo-schedule {
  text-align: right;
  font-size: 0.9em;
  color: #555;
}

/* Memo Modal Styles */
.memo-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.memo-modal {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
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
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
  background-color: #f8f9fa;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5em;
}

.close-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 5px;
  color: #888;
}

.close-button:hover {
  color: #333;
}

.modal-content {
  padding: 20px;
  overflow-y: auto;
  flex-grow: 1;
}

.memo-info-section, .form-data-section {
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.memo-info-section h3, .form-data-section h3 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 1.2em;
  color: #333;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
}

.info-item {
  display: flex;
  flex-direction: column;
}

.info-item label {
  font-weight: bold;
  font-size: 0.9em;
  color: #555;
  margin-bottom: 5px;
}

.info-item span {
  font-size: 1em;
  color: #000;
  word-break: break-word;
}

.form-section h4 {
  margin-top: 0;
  margin-bottom: 10px;
  font-size: 1.1em;
  color: #333;
}

.full-width {
  grid-column: 1 / -1; /* Span across all columns */
}
</style>
