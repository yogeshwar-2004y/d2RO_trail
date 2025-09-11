<template>
  <div class="activity-logs-page">
    <div class="header">
      <div class="header-left">
        <button class="back-button" @click="$router.go(-1)">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19 12H5"></path>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
        </button>
        <div class="logos-container">
          <img src="@/assets/images/aviatrax-logo.png" alt="Aviatrax Logo" class="logo">
          <img src="@/assets/images/vista_logo.png" alt="Vista Logo" class="logo vista-logo">
        </div>
      </div>
      <div class="header-center">
        <span class="page-title">ACTIVITY LOGS</span>
      </div>
      <div class="header-right">
        <div class="search-box">
          <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          <input type="text" v-model="searchQuery" placeholder="Search Projects" class="search-input">
        </div>
        <button class="icon-button">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M10 20.73l-1.39-1.39C5.39 16.03 3 13.5 3 10a7 7 0 1 1 14 0c0 3.5-2.39 6.03-5.61 9.34l-1.39 1.39z"></path>
            <circle cx="10" cy="10" r="3"></circle>
          </svg>
          <span class="button-label">QUERIES</span>
        </button>
        <button class="icon-button">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="12" y1="12" x2="12" y2="18"></line>
            <polyline points="9 15 12 18 15 15"></polyline>
          </svg>
        </button>
      </div>
    </div>
    
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>ACTIVITY ID</th>
            <th>PROJECT ID</th>
            <th>ACTIVITY PERFORMED</th>
            <th>PERFORMED BY</th>
            <th>TIMESTAMP</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="log in logs" :key="log.activityId">
            <td>{{ log.activityId }}</td>
            <td>{{ log.projectId }}</td>
            <td>{{ log.activityPerformed }}</td>
            <td>{{ log.performedBy }}</td>
            <td>{{ log.timestamp }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ActivityLogs',
  data() {
    return {
      searchQuery: '',
      logs: [
        { activityId: 1, projectId: 'PRJ001', activityPerformed: 'Document Uploaded', performedBy: 'User A', timestamp: '2025-07-15 10:00:00' },
        { activityId: 2, projectId: 'PRJ002', activityPerformed: 'Memo Approved', performedBy: 'User B', timestamp: '2025-07-15 10:15:30' },
        { activityId: 3, projectId: 'PRJ001', activityPerformed: 'Test Assigned', performedBy: 'User C', timestamp: '2025-07-15 11:05:45' },
        { activityId: 4, projectId: 'PRJ003', activityPerformed: 'User Added', performedBy: 'Admin', timestamp: '2025-07-15 11:30:10' },
      ],
    };
  },
};
</script>

<style scoped>
.activity-logs-page {
  font-family: Arial, sans-serif;
  min-height: 100vh;
  background-color: #8f6c6c;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 30px;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 1200px;
  margin-bottom: 30px;
  padding: 20px 0;
  color: #fff;
}

.header-left {
  display: flex;
  align-items: center;
}

.back-button {
  background: none;
  border: none;
  cursor: pointer;
  margin-right: 20px;
  color: #fff;
}

.logo {
  width: 120px;
  margin-right: 20px;
}

.page-title {
  font-size: 1.5em;
  font-weight: bold;
  text-align: center;
  flex-grow: 1;
}

.header-center {
  flex-grow: 1;
  text-align: center;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.search-box {
  position: relative;
}

.search-icon {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #888;
}

.search-input {
  width: 200px;
  padding: 10px 15px;
  padding-left: 40px;
  border: none;
  background-color: #444;
  color: #fff;
  border-radius: 25px;
  outline: none;
}

.icon-button {
  background: none;
  border: none;
  cursor: pointer;
  color: #fff;
  display: flex;
  align-items: center;
  gap: 5px;
}

.table-container {
  width: 100%;
  max-width: 1200px;
  background: #333;
  border-radius: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  padding: 20px;
  color: #fff;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  border: 1px solid #444;
  padding: 15px;
  text-align: left;
}

th {
  background-color: #444;
  font-weight: bold;
}
</style>