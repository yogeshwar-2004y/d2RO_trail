<template>
  <div class="plan-documents-page">
    <!-- Header -->
    <header class="header">
      <div class="header-left">
        <div class="back-arrow" @click="goBack">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="15 18 9 12 15 6"></polyline>
          </svg>
        </div>
        <img src="@/assets/images/aviatrax-logo.png" alt="AVIATRAX Logo" class="logo">
        <div class="page-title">
          <svg class="title-icon" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <line x1="10" y1="9" x2="8" y2="9"></line>
          </svg>
          <span class="title-text">PLAN DOCUMENTS</span>
          <span class="project-id">({{ projectId }})</span>
        </div>
      </div>
      
      <div class="header-right">
        <div class="search-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </div>
        <div class="filter-container">
          <button class="filter-button" @click="toggleFilterDropdown">
            <svg class="filter-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon>
            </svg>
            Filter Documents
          </button>
          
          <!-- Filter Dropdown -->
          <div class="filter-dropdown" v-if="showFilterDropdown">
            <div class="filter-option" v-for="option in filterOptions" :key="option" @click="filterByStatus(option)">
              {{ option }}
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="main-content">
      <div class="lru-grid">
        <div v-for="lru in filteredLrus" :key="lru.id" class="lru-card" :class="lru.status.toLowerCase().replace(/ /g, '-')" @click="selectLru(lru)">
          <div class="lru-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14,2 14,8 20,8"></polyline>
              <line x1="16" y1="13" x2="8" y2="13"></line>
              <line x1="16" y1="17" x2="8" y2="17"></line>
              <polyline points="10,9 9,9 8,9"></polyline>
            </svg>
          </div>
          <div class="lru-label">
            <div class="lru-text">LRU</div>
            <div class="lru-name">{{ lru.name }}</div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: "PlanDocumentsPage",
  props: {
    projectId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      showFilterDropdown: false,
      currentFilter: 'All',
      lrus: [
        { id: 1, name: 'LRU001', status: 'SUCCESSFULLY COMPLETED' },
        { id: 2, name: 'LRU002', status: 'ASSIGNED' },
        { id: 3, name: 'LRU003', status: 'COMPLETED WITH OBSERVATIONS' },
        { id: 4, name: 'LRU004', status: 'TEST NOT CONDUCTED' },
        { id: 5, name: 'LRU005', status: 'TEST FAILED' },
        { id: 6, name: 'LRU006', status: 'SUCCESSFULLY COMPLETED' },
        { id: 7, name: 'LRU007', status: 'ASSIGNED' },
        { id: 8, name: 'LRU008', status: 'COMPLETED WITH OBSERVATIONS' },
        { id: 9, name: 'LRU009', status: 'SUCCESSFULLY COMPLETED' },
        { id: 10, name: 'LRU010', status: 'ASSIGNED' },
        { id: 11, name: 'LRU011', status: 'TEST NOT CONDUCTED' },
        { id: 12, name: 'LRU012', status: 'SUCCESSFULLY COMPLETED' }
      ],
      filterOptions: [
        'All',
        'SUCCESSFULLY COMPLETED',
        'ASSIGNED',
        'COMPLETED WITH OBSERVATIONS',
        'TEST NOT CONDUCTED',
        'TEST FAILED'
      ]
    };
  },
  computed: {
    filteredLrus() {
      if (this.currentFilter === 'All') return this.lrus;
      return this.lrus.filter(lru => lru.status === this.currentFilter);
    }
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    toggleFilterDropdown() {
      this.showFilterDropdown = !this.showFilterDropdown;
    },
    filterByStatus(status) {
      this.currentFilter = status;
      this.showFilterDropdown = false;
    },
    selectLru(lru) {
      console.log('Selected LRU:', lru.name, 'Status:', lru.status);
      // Navigate to LRU details or open LRU
      // this.$router.push({ name: 'LruDetails', params: { id: lru.id } });
    }
  },
  mounted() {
    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.filter-container')) {
        this.showFilterDropdown = false;
      }
    });
  }
};
</script>

<style scoped>
.plan-documents-page {
  font-family: Arial, sans-serif;
  padding: 20px;
  background-color: white;
  min-height: 100vh;
}

/* Header Styles */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.back-arrow {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.back-arrow:hover {
  background: #e0e0e0;
  transform: scale(1.05);
}

.back-arrow svg {
  color: #333;
}

.logo {
  width: 150px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.title-icon {
  color: #333;
}

.title-text {
  font-size: 1.5em;
  font-weight: bold;
  color: #333;
}

.project-id {
  font-size: 0.8em;
  color: #666;
  margin-left: 10px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.search-icon {
  color: #333;
}

.search-icon svg {
  width: 24px;
  height: 24px;
}

/* Filter Styles */
.filter-container {
  position: relative;
}

.filter-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: #f0f0f0;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  color: #333;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.filter-button:hover {
  background: #e0e0e0;
}

.filter-icon {
  width: 20px;
  height: 20px;
}

.filter-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  min-width: 200px;
}

.filter-option {
  padding: 12px 16px;
  font-weight: bold;
  font-size: 14px;
  cursor: pointer;
  transition: opacity 0.3s ease;
  border-bottom: 1px solid #f0f0f0;
}

.filter-option:last-child {
  border-bottom: none;
}

.filter-option:hover {
  opacity: 0.8;
}

/* Filter Option Colors - Exact from Figma */
.filter-option.cleared {
  background: #90EE90; /* Light Green */
  color: #333;
}

.filter-option.disapproved {
  background: #FFB6C1; /* Light Red/Pink */
  color: #333;
}

.filter-option.assigned-returned {
  background: #87CEEB; /* Light Blue/Cyan */
  color: #333;
}

.filter-option.moved-next {
  background: #DDA0DD; /* Light Purple */
  color: #333;
}

.filter-option.not-cleared {
  background: #FFDAB9; /* Light Orange */
  color: #333;
}

/* Main Content Styles */
.main-content {
  padding: 20px 0;
}

.lru-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

/* LRU Card Styles */
.lru-card {
  background: white;
  border-radius: 15px;
  padding: 30px 20px;
  text-align: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  min-height: 150px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.lru-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}

.lru-icon {
  margin-bottom: 15px;
  color: #333;
}

.lru-label {
  text-align: center;
}

.lru-text {
  font-weight: bold;
  font-size: 1.1em;
  color: #333;
  margin-bottom: 5px;
}

.lru-name {
  font-weight: bold;
  font-size: 1.3em;
  color: #333;
}

/* Status-based colors for LRU Cards - Updated to match Test Reports colors */
.successfully-completed {
  background-color: #e2fbdc; /* Light Green - matches Test Reports */
}

.assigned {
  background-color: #d1d8ff; /* Light Blue - matches Test Reports */
}

.completed-with-observations {
  background-color: #fdddfa; /* Light Pink - matches Test Reports */
}

.test-not-conducted {
  background-color: #ffd8d6; /* Light Red/Salmon - matches Test Reports */
}

.test-failed {
  background-color: #fdddfa; /* Light Pink - matches Test Reports */
}

/* Additional status colors to match Test Reports */
.cleared {
  background-color: #e2fbdc; /* Light Green */
}

.disapproved {
  background-color: #ffd8d6; /* Light Red/Salmon */
}

.pending {
  background-color: #d1d8ff; /* Light Blue */
}

.approved {
  background-color: #e2fbdc; /* Light Green */
}

.review {
  background-color: #fdddfa; /* Light Pink */
}

/* Responsive Design */
@media (max-width: 1024px) {
  .lru-grid {
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 25px;
  }
}

@media (max-width: 768px) {
  .header {
    flex-direction: column;
    gap: 20px;
    align-items: flex-start;
  }
  
  .header-left {
    order: 1;
  }
  
  .header-right {
    order: 2;
    align-self: stretch;
    justify-content: space-between;
  }
  
  .lru-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 20px;
  }
  
  .lru-card {
    padding: 20px 15px;
    height: 180px;
  }
}

@media (max-width: 480px) {
  .lru-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
  }
  
  .lru-card {
    height: 160px;
    padding: 15px 10px;
  }
}
</style>
