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
        <img src="@/assets/images/aviatrax-logo.png" alt="Aviatrax Logo" class="logo">
        <div class="page-title">
          <svg class="title-icon" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <line x1="10" y1="9" x2="8" y2="9"></line>
          </svg>
          <span class="title-text">PLAN DOCUMENTS</span>
        </div>
      </div>
      <div class="header-right">
        <button class="filter-button" @click="toggleFilter">
          <svg class="filter-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon>
          </svg>
          <span class="filter-text">Filter Documents</span>
        </button>
      </div>
    </div>

    <div v-if="showFilter" class="filter-panel">
      <div
        v-for="status in statuses"
        :key="status.name"
        class="filter-option"
        :class="[status.color, { active: activeFilter === status.name }]"
        @click="filterByStatus(status.name)"
      >
        {{ status.name }}
      </div>
    </div>

    <div class="lru-grid">
      <div
        v-for="lru in filteredLrus"
        :key="lru.id"
        class="lru-card"
        :class="lru.status.toLowerCase().replace(/ /g, '-')"
        @click="viewLru(lru.name)"
      >
        <div class="card-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
          </svg>
        </div>
        <span class="card-title">LRU <br> &lt;NAME&gt;</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LruDashboard',
  data() {
    return {
      showFilter: false,
      activeFilter: null,
      statuses: [
        { name: 'Cleared', color: 'cleared-color' },
        { name: 'Disapproved', color: 'disapproved-color' },
        { name: 'Assigned & Returned', color: 'assigned-returned-color' },
        { name: 'Moved to Next Stage', color: 'moved-to-next-stage-color' },
        { name: 'Not Cleared', color: 'not-cleared-color' }
      ],
      lrus: [
        { id: 1, name: 'LRU-001', status: 'Cleared' },
        { id: 2, name: 'LRU-002', status: 'Assigned & Returned' },
        { id: 3, name: 'LRU-003', status: 'Moved to Next Stage' },
        { id: 4, name: 'LRU-004', status: 'Cleared' },
        { id: 5, name: 'LRU-005', status: 'Disapproved' },
        { id: 6, name: 'LRU-006', status: 'Not Cleared' },
        { id: 7, name: 'LRU-007', status: 'Cleared' },
        { id: 8, name: 'LRU-008', status: 'Disapproved' },
        { id: 9, name: 'LRU-009', status: 'Assigned & Returned' },
        { id: 10, name: 'LRU-010', status: 'Cleared' },
        { id: 11, name: 'LRU-011', status: 'Moved to Next Stage' },
        { id: 12, name: 'LRU-012', status: 'Not Cleared' },
        { id: 13, name: 'LRU-013', status: 'Cleared' },
        { id: 14, name: 'LRU-014', status: 'Disapproved' },
        { id: 15, name: 'LRU-015', status: 'Assigned & Returned' },
      ],
    };
  },
  computed: {
    filteredLrus() {
      if (!this.activeFilter) {
        return this.lrus;
      }
      return this.lrus.filter(lru => lru.status === this.activeFilter);
    },
  },
  methods: {
    toggleFilter() {
      this.showFilter = !this.showFilter;
    },
    filterByStatus(status) {
      this.activeFilter = this.activeFilter === status ? null : status;
      this.showFilter = false;
    },
    viewLru(lruName) {
      alert(`Viewing LRU: ${lruName}`);
    },
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

.filter-button {
  display: flex;
  align-items: center;
  gap: 10px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 10px 15px;
  border-radius: 20px;
  background-color: #f0f0f0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.filter-text {
  font-weight: bold;
}

.filter-panel {
  position: absolute;
  top: 90px;
  right: 30px;
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

.filter-option.active {
  border: 2px solid #007bff;
}

/* Status colors based on the image */
.cleared-color, .cleared-color.active {
  background-color: #e2fbdc;
  border-color: #008000;
}
.disapproved-color, .disapproved-color.active {
  background-color: #ffd8d6;
  border-color: #ff0000;
}
.assigned-returned-color, .assigned-returned-color.active {
  background-color: #d1d8ff;
  border-color: #0000ff;
}
.moved-to-next-stage-color, .moved-to-next-stage-color.active {
  background-color: #fdddfa;
  border-color: #800080;
}
.not-cleared-color, .not-cleared-color.active {
  background-color: #fff1d6;
  border-color: #ff8c00;
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
}

/* Dynamic card colors based on status */
.cleared { background-color: #e2fbdc; }
.disapproved { background-color: #ffd8d6; }
.assigned-returned { background-color: #d1d8ff; }
.moved-to-next-stage { background-color: #fdddfa; }
.not-cleared { background-color: #fff1d6; }
</style>