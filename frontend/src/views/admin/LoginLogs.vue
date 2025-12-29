<template>
  <div class="login-logs-page">
    <div class="header">
      <div class="header-left">
        <button class="back-button" @click="$router.go(-1)">
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
            <path d="M19 12H5"></path>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
        </button>
      </div>
      <div class="header-center">
        <span class="page-title">LOGIN LOGS</span>
      </div>
      <div class="header-right">
        <div class="limit-input-box">
          <label for="record-limit" class="limit-label">Records Limit:</label>
          <input
            id="record-limit"
            type="number"
            v-model.number="recordLimit"
            min="1"
            class="limit-input"
            @change="refreshLogs"
          />
        </div>
        <div class="search-box">
          <svg
            class="search-icon"
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
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Search Login Logs"
            class="search-input"
            @input="filterLogs"
          />
        </div>
        <button class="icon-button" @click="refreshLogs">
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
            <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"></path>
            <path d="M21 3v5h-5"></path>
            <path
              d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"
            ></path>
            <path d="M3 21v-5h5"></path>
          </svg>
          <span class="button-label">REFRESH</span>
        </button>
        <button class="icon-button" @click="downloadPDF" :disabled="loading">
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
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="7,10 12,15 17,10"></polyline>
            <line x1="12" y1="15" x2="12" y2="3"></line>
          </svg>
          <span class="button-label">DOWNLOAD PDF</span>
        </button>
      </div>
    </div>

    <!-- Advanced Search Panel -->
    <div class="advanced-search-panel" v-if="showAdvancedSearch">
      <div class="search-fields">
        <div class="search-field">
          <label>User Name:</label>
          <input
            type="text"
            v-model="searchFilters.userName"
            placeholder="Enter user name"
            class="filter-input"
            @input="applyFilters"
          />
        </div>
        <div class="search-field">
          <label>User ID:</label>
          <input
            type="text"
            v-model="searchFilters.userId"
            placeholder="Enter user ID"
            class="filter-input"
            @input="applyFilters"
          />
        </div>
        <div class="search-field">
          <label>Activity Type:</label>
          <select
            v-model="searchFilters.activityType"
            class="filter-select"
            @change="applyFilters"
          >
            <option value="">All Activities</option>
            <option value="logged_in">Login</option>
            <option value="logged_out">Logout</option>
            <option value="login_failed">Failed Login</option>
          </select>
        </div>
        <div class="search-field">
          <label>Date From:</label>
          <input
            type="date"
            v-model="searchFilters.dateFrom"
            class="filter-input"
            @change="applyFilters"
          />
        </div>
        <div class="search-field">
          <label>Date To:</label>
          <input
            type="date"
            v-model="searchFilters.dateTo"
            class="filter-input"
            @change="applyFilters"
          />
        </div>
        <div class="search-field">
          <button class="clear-filters-btn" @click="clearFilters">
            Clear Filters
          </button>
        </div>
      </div>
    </div>

    <!-- Toggle Advanced Search Button -->
    <div class="search-toggle-container">
      <button class="toggle-search-btn" @click="toggleAdvancedSearch">
        {{ showAdvancedSearch ? "Hide" : "Show" }} Advanced Search
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>Loading login logs...</p>
    </div>

    <!-- Error State -->
    <div v-if="error" class="error-container">
      <div class="error-message">
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
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="15" y1="9" x2="9" y2="15"></line>
          <line x1="9" y1="9" x2="15" y2="15"></line>
        </svg>
        <p>{{ error }}</p>
        <button @click="loadLoginLogs" class="retry-button">Retry</button>
      </div>
    </div>

    <!-- Login Logs Table -->
    <div v-if="!loading && !error" class="logs-container">
      <div class="table-container">
        <table class="logs-table">
          <thead>
            <tr>
              <th>Serial No.</th>
              <th>User ID</th>
              <th>Activity Performed</th>
              <th>Performed By</th>
              <th>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="log in filteredLogs"
              :key="log.serial_number"
              class="log-row"
              :class="{ 'suspicious-row': log.is_suspicious }"
            >
              <td class="serial-num">{{ log.serial_number }}</td>
              <td class="user-id">
                {{ log.user_id === 0 ? "N/A" : log.user_id }}
              </td>
              <td class="activity">{{ log.activity_performed || "N/A" }}</td>
              <td class="performed-by">{{ log.performed_by_name }}</td>
              <td class="timestamp">{{ formatTimestamp(log.timestamp) }}</td>
            </tr>
          </tbody>
        </table>

        <!-- No Data State -->
        <div v-if="filteredLogs.length === 0" class="no-data">
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
            <path d="M9 12l2 2 4-4"></path>
            <path
              d="M21 12c0 4.97-4.03 9-9 9s-9-4.03-9-9 4.03-9 9-9c1.65 0 3.2.45 4.54 1.24"
            ></path>
          </svg>
          <p>
            {{
              searchQuery
                ? "No login logs match your search criteria"
                : "No login logs found"
            }}
          </p>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="!recordLimit && totalLogs > limit" class="pagination">
        <button
          @click="previousPage"
          :disabled="offset === 0"
          class="page-button"
        >
          Previous
        </button>
        <span class="page-info">
          Showing {{ offset + 1 }} to
          {{ Math.min(offset + limit, totalLogs) }} of {{ totalLogs }} logs
        </span>
        <button
          @click="nextPage"
          :disabled="offset + limit >= totalLogs"
          class="page-button"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "LoginLogs",
  data() {
    return {
      searchQuery: "",
      logs: [],
      filteredLogs: [],
      loading: false,
      error: null,
      totalLogs: 0,
      limit: 50, // Default limit for pagination
      offset: 0,
      recordLimit: 50, // Default limit of 50 records, can be edited
      showAdvancedSearch: false,
      searchFilters: {
        userName: "",
        userId: "",
        activityType: "",
        dateFrom: "",
        dateTo: "",
      },
    };
  },
  async mounted() {
    await this.loadLoginLogs();
  },
  methods: {
    async loadLoginLogs() {
      this.loading = true;
      this.error = null;

      try {
        // If recordLimit is set, use it and reset offset to 0
        // Otherwise use pagination with limit and offset
        const params = {
          limit:
            this.recordLimit && this.recordLimit > 0
              ? this.recordLimit
              : this.limit,
          offset: this.recordLimit && this.recordLimit > 0 ? 0 : this.offset,
        };

        const response = await axios.get(
          "/api/login-logs",
          { params }
        );

        if (response.data.success) {
          this.logs = response.data.logs;
          this.filteredLogs = [...this.logs];
          this.totalLogs = response.data.total;
        } else {
          this.error = "Failed to load login logs";
        }
      } catch (error) {
        console.error("Error loading login logs:", error);
        this.error = "Error loading login logs. Please try again.";
      } finally {
        this.loading = false;
      }
    },

    filterLogs() {
      // Apply both simple search and advanced filters
      this.applyFilters();
    },

    applyFilters() {
      let filtered = [...this.logs];

      // Apply simple search query if exists
      if (this.searchQuery.trim()) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(
          (log) =>
            (log.serial_number?.toString() || "").includes(query) ||
            (log.user_id?.toString() || "").includes(query) ||
            (log.activity_performed?.toLowerCase() || "").includes(query) ||
            (log.performed_by?.toString() || "").includes(query) ||
            (log.performed_by_name?.toLowerCase() || "").includes(query) ||
            (log.user_name?.toLowerCase() || "").includes(query) ||
            (log.user_email?.toLowerCase() || "").includes(query) ||
            (log.suspicion_reason?.toLowerCase() || "").includes(query) ||
            (log.is_suspicious && "suspicious".includes(query)) ||
            this.formatTimestamp(log.timestamp).toLowerCase().includes(query)
        );
      }

      // Apply advanced filters
      if (this.searchFilters.userName.trim()) {
        const userName = this.searchFilters.userName.toLowerCase();
        filtered = filtered.filter(
          (log) =>
            (log.user_name?.toLowerCase() || "").includes(userName) ||
            (log.performed_by_name?.toLowerCase() || "").includes(userName)
        );
      }

      if (this.searchFilters.userId.trim()) {
        const userId = this.searchFilters.userId;
        filtered = filtered.filter(
          (log) =>
            log.user_id?.toString().includes(userId) ||
            log.performed_by?.toString().includes(userId)
        );
      }

      if (this.searchFilters.activityType) {
        filtered = filtered.filter(
          (log) => log.activity_performed === this.searchFilters.activityType
        );
      }

      if (this.searchFilters.dateFrom) {
        const dateFrom = new Date(this.searchFilters.dateFrom);
        dateFrom.setHours(0, 0, 0, 0);
        filtered = filtered.filter((log) => {
          if (!log.timestamp) return false;
          const logDate = new Date(log.timestamp);
          logDate.setHours(0, 0, 0, 0);
          return logDate >= dateFrom;
        });
      }

      if (this.searchFilters.dateTo) {
        const dateTo = new Date(this.searchFilters.dateTo);
        dateTo.setHours(23, 59, 59, 999);
        filtered = filtered.filter((log) => {
          if (!log.timestamp) return false;
          const logDate = new Date(log.timestamp);
          return logDate <= dateTo;
        });
      }

      this.filteredLogs = filtered;
    },

    toggleAdvancedSearch() {
      this.showAdvancedSearch = !this.showAdvancedSearch;
    },

    clearFilters() {
      this.searchQuery = "";
      this.searchFilters = {
        userName: "",
        userId: "",
        activityType: "",
        dateFrom: "",
        dateTo: "",
      };
      this.applyFilters();
    },


    formatTimestamp(timestamp) {
      if (!timestamp) return "N/A";

      try {
        const date = new Date(timestamp);
        return date.toLocaleString("en-US", {
          year: "numeric",
          month: "2-digit",
          day: "2-digit",
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
        });
      } catch (error) {
        return timestamp;
      }
    },

    async downloadPDF() {
      try {
        const params = {};

        // Set limit only if no search filters are applied
        const hasFilters =
          this.searchQuery.trim() ||
          this.searchFilters.userName.trim() ||
          this.searchFilters.userId.trim() ||
          this.searchFilters.activityType ||
          this.searchFilters.dateFrom ||
          this.searchFilters.dateTo;

        if (!hasFilters && this.recordLimit && this.recordLimit > 0) {
          params.limit = this.recordLimit;
        }

        // Include search query if filter is applied
        if (this.searchQuery && this.searchQuery.trim()) {
          params.search = this.searchQuery.trim();
        }

        // Include advanced search filters
        if (this.searchFilters.userName.trim()) {
          params.user_name = this.searchFilters.userName.trim();
        }
        if (this.searchFilters.userId.trim()) {
          params.user_id = this.searchFilters.userId.trim();
        }
        if (this.searchFilters.activityType) {
          params.activity_type = this.searchFilters.activityType;
        }
        if (this.searchFilters.dateFrom) {
          params.date_from = this.searchFilters.dateFrom;
        }
        if (this.searchFilters.dateTo) {
          params.date_to = this.searchFilters.dateTo;
        }

        const response = await axios.get(
          "/api/login-logs/pdf",
          {
            params,
            responseType: "blob",
          }
        );

        // Create blob link to download
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute(
          "download",
          `login_logs_${new Date().toISOString().split("T")[0]}.pdf`
        );
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);

        alert("Login logs PDF downloaded successfully!");
      } catch (error) {
        console.error("Error downloading PDF:", error);
        alert("Failed to download PDF. Please try again.");
      }
    },

    async refreshLogs() {
      this.offset = 0;
      // If recordLimit is set, use it; otherwise use default limit
      if (this.recordLimit && this.recordLimit > 0) {
        this.limit = this.recordLimit;
      } else {
        // Reset to default limit if recordLimit is cleared
        this.limit = 50;
      }
      await this.loadLoginLogs();
    },

    async previousPage() {
      if (this.offset > 0) {
        this.offset -= this.limit;
        await this.loadLoginLogs();
      }
    },

    async nextPage() {
      if (this.offset + this.limit < this.totalLogs) {
        this.offset += this.limit;
        await this.loadLoginLogs();
      }
    },
  },
};
</script>

<style scoped>
.login-logs-page {
  background-color: #ebf7fd;
  min-height: 100vh;
  padding: 20px;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: white;
  padding: 20px 30px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.header-left {
  display: flex;
  align-items: center;
}

.back-button {
  background: #3498db;
  color: white;
  border: none;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  transition: background-color 0.3s ease;
}

.back-button:hover {
  background: #c0392b;
}

.header-center {
  flex: 1;
  text-align: center;
}

.page-title {
  font-size: 24px;
  font-weight: bold;
  color: #2c3e50;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 15px;
}

.search-box {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 12px;
  color: #7f8c8d;
  z-index: 1;
}

.limit-input-box {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-right: 10px;
}

.limit-label {
  font-size: 14px;
  color: #2c3e50;
  white-space: nowrap;
  font-weight: 500;
}

.limit-input {
  width: 100px;
  padding: 12px 15px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
  text-align: center;
  transition: border-color 0.3s ease;
}

.limit-input:focus {
  outline: none;
  border-color: #3498db;
}

.limit-input::placeholder {
  color: #7f8c8d;
}

.search-input {
  padding: 12px 12px 12px 40px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
  width: 250px;
  transition: border-color 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #3498db;
}

.icon-button {
  background: #3498db;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  transition: background-color 0.3s ease;
}

.icon-button:hover {
  background: #2980b9;
}

.button-label {
  font-size: 14px;
  font-weight: 600;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.error-container {
  display: flex;
  justify-content: center;
  padding: 60px 20px;
}

.error-message {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
  max-width: 400px;
}

.error-message svg {
  color: #e74c3c;
  margin-bottom: 20px;
}

.error-message p {
  color: #7f8c8d;
  margin-bottom: 20px;
}

.retry-button {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.3s ease;
}

.retry-button:hover {
  background: #c0392b;
}

.logs-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.table-container {
  overflow-x: auto;
}

.logs-table {
  width: 100%;
  border-collapse: collapse;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.logs-table th {
  background: #34495e;
  color: white;
  padding: 18px 16px;
  text-align: center;
  font-weight: 600;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border: none;
}

.logs-table td {
  padding: 16px;
  border-bottom: 1px solid #f0f0f0;
  font-size: 14px;
  vertical-align: middle;
}

.log-row:hover {
  background: #f8f9fa;
}

.log-row:last-child td {
  border-bottom: none;
}

.serial-num {
  font-weight: 600;
  color: #2c3e50;
  text-align: center;
  width: 100px;
}

.user-id {
  text-align: center;
  width: 100px;
  color: #7f8c8d;
  font-weight: 500;
}

.activity {
  text-align: left;
  width: 250px;
  color: #000;
  font-weight: 600;
}

.suspicious-row {
  background: #fef9e7 !important;
  border-left: 4px solid #f39c12;
}

.suspicious-row:hover {
  background: #fdf2d9 !important;
}

.performed-by {
  text-align: left;
  width: 200px;
  color: #2c3e50;
  font-weight: 500;
  padding-left: 20px;
}

.timestamp {
  color: #2c3e50;
  font-family: "Courier New", monospace;
  text-align: left;
  width: 200px;
  font-size: 13px;
  padding-left: 20px;
}

.no-data {
  text-align: center;
  padding: 60px 20px;
  color: #7f8c8d;
}

.no-data svg {
  margin-bottom: 20px;
  opacity: 0.5;
}

.no-data p {
  font-size: 16px;
  margin: 0;
}

.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 30px;
  background: #f8f9fa;
  border-top: 1px solid #ecf0f1;
}

.page-button {
  background: #3498db;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.3s ease;
}

.page-button:hover:not(:disabled) {
  background: #2980b9;
}

.page-button:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.page-info {
  color: #7f8c8d;
  font-size: 14px;
  font-weight: 500;
}

/* Advanced Search Panel */
.advanced-search-panel {
  background: white;
  padding: 20px 30px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 10px;
}

.search-fields {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 40px;
  align-items: end;
}

.search-field {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.search-field:last-child {
  grid-column: 1 / -1;
  display: flex;
  justify-content: center;
}

.search-field label {
  font-size: 14px;
  font-weight: 500;
  color: #2c3e50;
}

.filter-input,
.filter-select {
  padding: 10px 12px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.3s ease;
  width: 100%;
}

.filter-input:focus,
.filter-select:focus {
  outline: none;
  border-color: #3498db;
}

.clear-filters-btn {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 12px 18px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 15px;
  font-weight: 500;
  transition: background-color 0.3s ease;
  width: auto;
  margin-left: 45%;
  margin-right: 45%;
}

.clear-filters-btn:hover {
  background: #c0392b;
}

.search-toggle-container {
  margin-bottom: 15px;
  text-align: center;
}

.toggle-search-btn {
  background: #3498db;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.3s ease;
}

.toggle-search-btn:hover {
  background: #2980b9;
}

/* Responsive Design */
@media (max-width: 768px) {
  .header {
    flex-direction: column;
    gap: 20px;
    padding: 20px;
  }

  .header-right {
    width: 100%;
    justify-content: center;
  }

  .search-input {
    width: 200px;
  }

  .logs-table th,
  .logs-table td {
    padding: 12px 8px;
    font-size: 12px;
  }

  .pagination {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
}
</style>
