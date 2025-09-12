<template>
  <div class="lru-dashboard">
    <div class="header">
      <button class="back-button" @click="$router.go(-1)">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M19 12H5"></path>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
      </button>
      <div class="header-center">
        <div class="logos-container">
          <img src="@/assets/images/aviatrax-logo.png" alt="Aviatrax Logo" class="logo">
          <img src="@/assets/images/vista_logo.png" alt="Vista Logo" class="logo vista-logo">
        </div>
        <div class="page-title">
          <svg class="title-icon" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <line x1="10" y1="9" x2="8" y2="9"></line>
          </svg>
          <span class="title-text">{{ projectName }} - LRUs</span>
        </div>
      </div>
      <div class="header-right">
        <div class="filter-dropdown">
          <button class="filter-button" @click="toggleStatusFilter">
            Filter by Status
          </button>
        </div>

        <div class="filter-dropdown">
          <button class="filter-button" @click="toggleStatusFilter">
            Filter by Status
          </button>
        </div>

        <div class="search-box">
          <input type="text" v-model="searchQuery" placeholder="Search LRUs" class="search-input">
          <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </div>
      </div>
      <!-- ✅ Status Filter Overlay -->
      <div v-if="showStatusFilter" class="status-overlay" @click.self="closeStatusFilter">
        <div class="status-panel">
          <h3>Filters</h3>
          <div 
            v-for="status in statuses" 
            :key="status.name" 
            class="status-option" 
            :class="[status.color, { 'selected': activeStatusFilter === status.name }]"
            @click="selectStatus(status.name)"
          >
            {{ status.name }}
          </div>
        </div>
      </div>
      <!-- ✅ Status Filter Overlay -->
      <div v-if="showStatusFilter" class="status-overlay" @click.self="closeStatusFilter">
        <div class="status-panel">
          <h3>Filters</h3>
          <div 
            v-for="status in statuses" 
            :key="status.name" 
            class="status-option" 
            :class="[status.color, { 'selected': activeStatusFilter === status.name }]"
            @click="selectStatus(status.name)"
          >
            {{ status.name }}
          </div>
        </div>
      </div>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>Loading LRUs...</p>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="error-container">
      <p class="error-message">{{ error }}</p>
      <button @click="fetchLrus" class="retry-button">Retry</button>
    </div>

    <!-- LRUs grid -->
    <div v-else class="lru-grid">
      <div v-if="filteredLrus.length === 0" class="no-lrus">
        <p>No LRUs found for this project.</p>
      </div>
      <div v-else v-for="lru in filteredLrus" :key="lru.id" class="lru-card" @click="viewLru(lru)">
        <div class="card-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
          </svg>
        </div>
        <span class="card-title">{{ lru.name }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import { userStore } from '@/stores/userStore'

export default {
  name: 'LruDashboard',
  data() {
    return {
      projectId: null,
      projectName: '',
      searchQuery: '',
      lrus: [],
      loading: true,
      error: null,
      showStatusFilter: false,
      activeStatusFilter: null,
      statuses: [
        { name: 'CLEARED', color: 'cleared' },
        { name: 'DISAPPROVED', color: 'disapproved' },
        { name: 'ASSIGNED & RETURNED', color: 'assigned-returned' },
        { name: 'MOVED TO NEXT STAGE', color: 'moved-next' },
        { name: 'NOT CLEARED', color: 'not-cleared' }
      ]
    };
  },
  computed: {
    // Get current user role from global store
    currentUserRole() {
      return userStore.getters.currentUserRole()
    },
    roleName() {
      return userStore.getters.roleName()
    },
    filteredLrus() {
      let list = this.lrus;

      if (this.activeStatusFilter) {
        list = list.filter(lru => lru.status === this.activeStatusFilter);
      }
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        list = list.filter(lru => lru.name.toLowerCase().includes(query));
      }
      return list;
    }
  },
  async mounted() {
    // Get project ID and name from route params
    this.projectId = parseInt(this.$route.params.projectId);
    this.projectName = this.$route.params.projectName || 'Project';
    
    if (this.projectId) {
      await this.fetchLrus();
    } else {
      this.error = 'Project ID not found';
      this.loading = false;
    }
  },
  methods: {
    toggleStatusFilter() {
      this.showStatusFilter = !this.showStatusFilter;
    },
    closeStatusFilter() {
      this.showStatusFilter = false;
    },
    selectStatus(status) {
      this.activeStatusFilter = this.activeStatusFilter === status ? null : status;
      this.closeStatusFilter();
    },
    async fetchLrus() {
      try {
        this.loading = true;
        this.error = null;
        
        const response = await fetch(`http://localhost:8000/api/projects/${this.projectId}/lrus`);
        const data = await response.json();
        
        if (data.success) {
          this.lrus = data.lrus;
          this.projectName = data.project.name;
        } else {
          this.error = data.message || 'Failed to fetch LRUs';
        }
      } catch (err) {
        console.error('Error fetching LRUs:', err);
        this.error = 'Failed to connect to server. Please check if the backend is running.';
      } finally {
        this.loading = false;
      }
    },
    viewLru(lru) {
      // Navigate to document viewer or LRU detail page
      //alert(`Viewing LRU: ${lru.name}`);
      this.$router.push({ 
        name: 'DocumentViewer', 
        params: { 
          lruId: lru.id, 
          lruName: lru.name,
          projectId: this.projectId
        } 
      });
    },
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString();
    }
  },
};
</script>

<style scoped>
.lru-dashboard {
  font-family: Arial, sans-serif;
  min-height: 100vh;
  background-color: #f0f0f0;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 30px;
  background: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 10;
}

.back-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.back-button:hover {
  background-color: #f0f0f0;
}

.header-center {
  display: flex;
  align-items: center;
  gap: 20px;
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
  color: #555;
  width: 32px;
  height: 32px;
}

.title-text {
  font-size: 1.5em;
  font-weight: bold;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 15px;
}

.search-box {
  position: relative;
  width: 250px;
}

.search-input {
  width: 80%;
  padding: 10px 15px;
  padding-right: 40px;
  border: 1px solid #ccc;
  border-radius: 25px;
  font-size: 1em;
  outline: none;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
  position: relative;
  left: -10px;
}

.search-icon {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #888;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #555;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.error-message {
  color: #d32f2f;
  font-size: 1.1em;
  margin-bottom: 20px;
}

.retry-button {
  background-color: #1976d2;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.3s ease;
}

.retry-button:hover {
  background-color: #1565c0;
}

.lru-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 20px;
  padding: 30px;
}

.lru-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #fff;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  height: 180px;
  text-align: center;
}

.lru-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

.card-icon {
  margin-bottom: 10px;
}

.card-icon svg {
  color: #555;
  width: 48px;
  height: 48px;
}

.card-title {
  font-size: 1em;
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

.card-date {
  font-size: 0.8em;
  color: #666;
}

.no-lrus {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 60px 20px;
  text-align: center;
  color: #666;
  font-size: 1.1em;
  grid-column: 1 / -1;
}

/* Filter Button */
.filter-button {
  background: #f0f0f0;
  border: 1px solid #ccc;
  border-radius: 20px;
  padding: 10px 15px;
  font-weight: bold;
  cursor: pointer;
}

/* Overlay */
.status-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.4);
  display: flex;
  justify-content: flex-start;
  align-items: flex-start;
  z-index: 1000;
}

.status-panel {
  background: #fff;
  width: 250;
  padding: 20px;
  border-radius: 10px;
  margin: 50px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.2);
  position: relative;
  right: -960px;
  top: 35px;
}

.status-option {
  padding: 15px;
  margin-bottom: 10px;
  font-weight: bold;
  text-align: center;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s;
}

.status-option:hover {
  transform: scale(1.03);
}

.status-option.selected {
  border: 2px solid #000;
}

/* ✅ Colors (match your screenshot) */
.cleared { background-color: #ccffcc; }        /* light green */
.disapproved { background-color: #ffcccc; }    /* light red */
.assigned-returned { background-color: #ccffff; } /* light cyan */
.moved-next { background-color: #e6ccff; }     /* light purple */
.not-cleared { background-color: #ffddaa; }    /* light orange */

/* Overlay */
.status-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.4);
  display: flex;
  justify-content: flex-start;
  align-items: flex-start;
  z-index: 1000;
}

.status-panel {
  background: #fff;
  width: 250;
  padding: 20px;
  border-radius: 10px;
  margin: 50px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.2);
  position: relative;
  right: -960px;
  top: 35px;
}

.status-option {
  padding: 15px;
  margin-bottom: 10px;
  font-weight: bold;
  text-align: center;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s;
}

.status-option:hover {
  transform: scale(1.03);
}

.status-option.selected {
  border: 2px solid #000;
}

/* ✅ Colors (match your screenshot) */
.cleared { background-color: #ccffcc; }        /* light green */
.disapproved { background-color: #ffcccc; }    /* light red */
.assigned-returned { background-color: #ccffff; } /* light cyan */
.moved-next { background-color: #e6ccff; }     /* light purple */
.not-cleared { background-color: #ffddaa; }    /* light orange */

</style>