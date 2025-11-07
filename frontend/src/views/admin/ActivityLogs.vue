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
            placeholder="Search Projects"
            class="search-input"
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

    <div class="table-container">
      <div v-if="loading" class="loading-message">Loading activity logs...</div>
      <div v-else-if="error" class="error-message">
        {{ error }}
        <button @click="loadActivityLogs" class="retry-button">Retry</button>
      </div>
      <table v-else>
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
          <tr v-for="log in filteredLogs" :key="log.activity_id">
            <td class="activity-id">{{ log.activity_id || "N/A" }}</td>
            <td class="project-id">{{ extractId(log.additional_info) }}</td>
            <td class="project-name">{{ extractName(log.additional_info) }}</td>
            <td class="activity">{{ log.activity_performed || "N/A" }}</td>
            <td class="performed-by">
              {{ log.user_name || log.performed_by || "Unknown" }}
            </td>
            <td class="timestamp">{{ formatTimestamp(log.timestamp) }}</td>
          </tr>
        </tbody>
      </table>
      <div
        v-if="!loading && !error && filteredLogs.length === 0"
        class="no-data-message"
      >
        No activity logs found.
      </div>
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
        const response = await axios.get(
          "http://localhost:5000/api/activity-logs"
        );

        if (response.data.success) {
          this.logs = response.data.logs;
          this.filteredLogs = [...this.logs];
        } else {
          this.error = "Failed to load activity logs";
        }
      } catch (error) {
        console.error("Error loading activity logs:", error);
        this.error = "Error loading activity logs. Please try again.";
      } finally {
        this.loading = false;
      }
    },

    filterLogs() {
      if (!this.searchQuery.trim()) {
        this.filteredLogs = [...this.logs];
        return;
      }

      const query = this.searchQuery.toLowerCase();
      this.filteredLogs = this.logs.filter(
        (log) =>
          log.activity_performed.toLowerCase().includes(query) ||
          log.user_name?.toLowerCase().includes(query) ||
          log.project_name?.toLowerCase().includes(query) ||
          log.project_id?.toString().includes(query) ||
          log.activity_id?.toString().includes(query) ||
          log.additional_info?.toLowerCase().includes(query)
      );
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
        this.loading = true;
        const response = await axios.get(
          "http://localhost:5000/api/activity-logs/pdf",
          {
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
      } finally {
        this.loading = false;
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
.activity-logs-page {
  font-family: Arial, sans-serif;
  min-height: 100vh;
  background-color: #ebf7fd;
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
  color: #121111;
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
  color: #060505;
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
  color: #050505;
}

.search-input {
  width: 200px;
  padding: 10px 15px;
  padding-left: 40px;
  border: none;
  background-color: #e2e0e0;
  color: #0f0f0f;
  border-radius: 25px;
  outline: none;
}

.icon-button {
  background: none;
  border: none;
  cursor: pointer;
  color: #050505;
  display: flex;
  align-items: center;
  gap: 5px;
}

.table-container {
  width: 100%;
  max-width: 1200px;
  background: #201e1e;
  border-radius: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  padding: 20px;
  color: #060505;
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
}

th {
  background-color: #645656;
  font-weight: bold;
}

.activity-id {
  text-align: center;
  width: 120px;
  font-weight: 600;
  color: #fff;
}

.project-id {
  text-align: center;
  width: 100px;
  color: #fff;
  font-weight: 600;
}

.project-name {
  text-align: left;
  width: 200px;
  color: #fff;
  font-weight: 600;
}

.activity {
  text-align: left;
  width: 250px;
  color: #fff;
  font-weight: 600;
}

.performed-by {
  text-align: left;
  width: 180px;
  color: #fff;
  font-weight: 600;
}

.timestamp {
  text-align: left;
  width: 180px;
  color: #fff;
  font-weight: 600;
}

.loading-message,
.error-message,
.no-data-message {
  text-align: center;
  padding: 40px;
  color: #fff;
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
