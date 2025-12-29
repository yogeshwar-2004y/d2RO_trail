<template>
  <div class="activity-logs-page">
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
        <span class="page-title">ACTIVITY LOGS</span>
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
            @change="loadActivityLogs"
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
            placeholder="Search Activity Logs"
            class="search-input"
            @input="filterLogs"
          />
        </div>
        <button class="icon-button" @click="goToLoginLogs">
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
            <path d="M9 12l2 2 4-4"></path>
            <path
              d="M21 12c0 4.97-4.03 9-9 9s-9-4.03-9-9 4.03-9 9-9c1.65 0 3.2.45 4.54 1.24"
            ></path>
          </svg>
          <span class="button-label">LOGIN LOGS</span>
        </button>
        <button class="icon-button" @click="downloadPDF">
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
              d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"
            ></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="12" y1="12" x2="12" y2="18"></line>
            <polyline points="9 15 12 18 15 15"></polyline>
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
          <label>Project ID:</label>
          <input
            type="text"
            v-model="searchFilters.projectId"
            placeholder="Enter project ID"
            class="filter-input"
            @input="applyFilters"
          />
        </div>
        <div class="search-field">
          <label>Activity Type:</label>
          <input
            type="text"
            v-model="searchFilters.activityType"
            placeholder="Enter activity type"
            class="filter-input"
            @input="applyFilters"
          />
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

    <div class="table-container">
      <div v-if="loading" class="loading-message">Loading activity logs...</div>
      <div v-else-if="error" class="error-message">
        {{ error }}
        <button @click="loadActivityLogs" class="retry-button">Retry</button>
      </div>
      <table v-if="!loading && !error">
        <thead>
          <tr>
            <th class="activity-id">ACTIVITY ID</th>
            <th class="project-id">PROJECT ID</th>
            <th class="project-name">PROJECT NAME</th>
            <th class="activity">ACTIVITY PERFORMED</th>
            <th class="performed-by">PERFORMED BY</th>
            <th class="timestamp">TIMESTAMP</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="filteredLogs.length === 0">
            <td colspan="6" class="no-data-message">No activity logs found.</td>
          </tr>
          <tr v-for="log in filteredLogs" :key="log.activity_id">
            <td class="activity-id">{{ log.activity_id || "N/A" }}</td>
            <td class="project-id">
              {{ log.project_id || extractId(log.additional_info) || "N/A" }}
            </td>
            <td class="project-name">
              {{
                log.project_name || extractName(log.additional_info) || "N/A"
              }}
            </td>
            <td class="activity">{{ log.activity_performed || "N/A" }}</td>
            <td class="performed-by">
              {{ log.user_name || log.performed_by || "Unknown" }}
            </td>
            <td class="timestamp">{{ formatTimestamp(log.timestamp) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ActivityLogs",
  data() {
    return {
      searchQuery: "",
      logs: [],
      filteredLogs: [],
      loading: false,
      error: null,
      recordLimit: 50, // Default limit of 50 records, can be edited
      showAdvancedSearch: false,
      searchFilters: {
        userName: "",
        activityId: "",
        projectId: "",
        activityType: "",
        dateFrom: "",
        dateTo: "",
      },
    };
  },
  async mounted() {
    await this.loadActivityLogs();
  },
  methods: {
    async loadActivityLogs() {
      this.loading = true;
      this.error = null;

      try {
        const params = {
          limit:
            this.recordLimit && this.recordLimit > 0 ? this.recordLimit : 50,
        };

        const response = await axios.get(
          "/api/activity-logs",
          { params }
        );

        if (response.data.success) {
          this.logs = response.data.logs || [];
          console.log("Raw response data:", response.data);
          console.log("Loaded activity logs:", this.logs.length, "logs");
          console.log("Sample log:", this.logs[0]);
          // Apply any existing filters after loading
          this.applyFilters();
          console.log(
            "Filtered activity logs:",
            this.filteredLogs.length,
            "logs"
          );
        } else {
          this.error = response.data.message || "Failed to load activity logs";
        }
      } catch (error) {
        console.error("Error loading activity logs:", error);
        console.error("Error details:", error.response?.data || error.message);
        this.error = `Error loading activity logs: ${
          error.response?.data?.message || error.message || "Please try again."
        }`;
      } finally {
        this.loading = false;
      }
    },

    filterLogs() {
      this.applyFilters();
    },

    applyFilters() {
      if (!this.logs || this.logs.length === 0) {
        this.filteredLogs = [];
        return;
      }

      let filtered = [...this.logs];

      // Apply simple search query if exists
      if (this.searchQuery.trim()) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(
          (log) =>
            (log.activity_performed?.toLowerCase() || "").includes(query) ||
            (log.user_name?.toLowerCase() || "").includes(query) ||
            (log.project_name?.toLowerCase() || "").includes(query) ||
            (log.project_id?.toString() || "").includes(query) ||
            (log.activity_id?.toString() || "").includes(query) ||
            (log.additional_info?.toLowerCase() || "").includes(query)
        );
      }

      // Apply advanced filters
      if (this.searchFilters.userName.trim()) {
        const userName = this.searchFilters.userName.toLowerCase();
        filtered = filtered.filter((log) =>
          log.user_name?.toLowerCase().includes(userName)
        );
      }

      if (this.searchFilters.activityId.trim()) {
        filtered = filtered.filter((log) =>
          log.activity_id?.toString().includes(this.searchFilters.activityId)
        );
      }

      if (this.searchFilters.projectId.trim()) {
        filtered = filtered.filter((log) =>
          log.project_id?.toString().includes(this.searchFilters.projectId)
        );
      }

      if (this.searchFilters.activityType.trim()) {
        const activityType = this.searchFilters.activityType.toLowerCase();
        filtered = filtered.filter((log) =>
          log.activity_performed?.toLowerCase().includes(activityType)
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
        activityId: "",
        projectId: "",
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

    goToLoginLogs() {
      this.$router.push({ name: "LoginLogs" });
    },

    async downloadPDF() {
      try {
        const params = {};

        // Set limit only if no search filters are applied
        const hasFilters =
          this.searchQuery.trim() ||
          this.searchFilters.userName.trim() ||
          this.searchFilters.activityId.trim() ||
          this.searchFilters.projectId.trim() ||
          this.searchFilters.activityType.trim() ||
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
        if (this.searchFilters.activityId.trim()) {
          params.activity_id = this.searchFilters.activityId.trim();
        }
        if (this.searchFilters.projectId.trim()) {
          params.project_id = this.searchFilters.projectId.trim();
        }
        if (this.searchFilters.activityType.trim()) {
          params.activity_type = this.searchFilters.activityType.trim();
        }
        if (this.searchFilters.dateFrom) {
          params.date_from = this.searchFilters.dateFrom;
        }
        if (this.searchFilters.dateTo) {
          params.date_to = this.searchFilters.dateTo;
        }

        const response = await axios.get(
          "/api/activity-logs/pdf",
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
          `activity_logs_${new Date().toISOString().split("T")[0]}.pdf`
        );
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);

        alert("Activity logs PDF downloaded successfully!");
      } catch (error) {
        console.error("Error downloading PDF:", error);
        alert("Failed to download PDF. Please try again.");
      }
    },

    extractId(additionalInfo) {
      if (!additionalInfo) return "-";

      // Look for pattern "ID:123|" in additional_info
      const idMatch = additionalInfo.match(/ID:([^|]+)\|/);
      return idMatch ? idMatch[1] : "-";
    },

    extractName(additionalInfo) {
      if (!additionalInfo) return "-";

      // Look for pattern "Name:SomeName|" in additional_info
      const nameMatch = additionalInfo.match(/Name:([^|]+)\|/);
      return nameMatch ? nameMatch[1] : "-";
    },
  },

  watch: {
    searchQuery() {
      this.filterLogs();
    },
  },
};
</script>

<style scoped>
/* Advanced Search Panel */
.advanced-search-panel {
  background: white;
  padding: 25px 40px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 10px;
}

.search-fields {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
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
  padding: 12px 18px; /* small button size */
  border-radius: 6px;
  cursor: pointer;
  font-size: 15px;
  font-weight: 500;
  transition: background-color 0.3s ease;
  width: auto; /* keeps it narrow */
  margin-left: 45%; /* optional horizontal spacing from other elements */
  margin-right: 45%; /* optional horizontal spacing from other elements */
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

.activity-logs-page {
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

.table-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  width: 100%;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  border: 1px solid #9f9c9c;
  padding: 15px;
  text-align: left;
  color: #000;
}

th {
  background-color: #34495e;
  font-weight: bold;
  color: #fff;
}

.activity-id {
  text-align: center;
  width: 120px;
  font-weight: 600;
  color: #000;
}

.project-id {
  text-align: center;
  width: 100px;
  color: #000;
  font-weight: 600;
}

.project-name {
  text-align: left;
  width: 200px;
  color: #000;
  font-weight: 600;
}

.activity {
  text-align: left;
  width: 250px;
  color: #000;
  font-weight: 600;
}

.performed-by {
  text-align: left;
  width: 180px;
  color: #000;
  font-weight: 600;
}

.timestamp {
  text-align: left;
  width: 180px;
  color: #000;
  font-weight: 600;
}

.loading-message,
.error-message,
.no-data-message {
  text-align: center;
  padding: 40px;
  color: #000;
  font-size: 1.1em;
}

.error-message {
  color: #ff6b6b;
}

.retry-button {
  margin-top: 10px;
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.retry-button:hover {
  background-color: #0056b3;
}
</style>
