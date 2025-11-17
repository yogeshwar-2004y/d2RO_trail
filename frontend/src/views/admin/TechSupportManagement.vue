<template>
  <div class="tech-support-management">
    <div class="page-header">
      <button class="back-button" @click="goBack">
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
        <span>Back</span>
      </button>
      <div class="header-content">
        <h1>Tech Support Management</h1>
        <p>Manage and respond to technical support requests</p>
      </div>
    </div>

    <!-- Success Popup Modal -->
    <div
      v-if="showSuccessMessage"
      class="popup-overlay"
      @click="hideSuccessMessage"
    >
      <div class="popup-modal" @click.stop>
        <div class="popup-header">
          <div class="popup-icon">
            <span class="success-checkmark">✓</span>
          </div>
          <h3>Success!</h3>
        </div>
        <div class="popup-body">
          <p>{{ successMessage }}</p>
        </div>
        <div class="popup-footer">
          <button @click="hideSuccessMessage" class="popup-btn">OK</button>
        </div>
      </div>
    </div>

    <div class="filters-section">
      <div class="filter-group">
        <label for="statusFilter">Filter by Status:</label>
        <select
          id="statusFilter"
          v-model="statusFilter"
          @change="filterRequests"
        >
          <option value="">All Statuses</option>
          <option value="pending">Pending</option>
          <option value="in_progress">In Progress</option>
          <option value="resolved">Resolved</option>
          <option value="closed">Closed</option>
          <option value="offline_pending">Offline Pending</option>
        </select>
      </div>
      <div class="filter-group">
        <label for="searchInput">Search:</label>
        <input
          id="searchInput"
          type="text"
          v-model="searchQuery"
          @input="filterRequests"
          placeholder="Search by username, user ID, or issue..."
        />
      </div>
      <div class="export-controls">
        <div class="export-group">
          <label for="exportLimit">Export Limit:</label>
          <select id="exportLimit" v-model="exportLimit">
            <option value="10">10</option>
            <option value="20">20</option>
            <option value="30">30</option>
            <option value="40">40</option>
            <option value="50">50</option>
            <option value="60">60</option>
            <option value="70">70</option>
            <option value="80">80</option>
            <option value="90">90</option>
            <option value="100">100</option>
          </select>
        </div>
        <button @click="exportToPDF" class="export-btn">
          📄 Export to PDF
        </button>
      </div>
    </div>

    <div class="requests-container">
      <div v-if="loading" class="loading">
        <p>Loading tech support requests...</p>
      </div>

      <div v-else>
        <!-- Online Requests Section -->
        <div v-if="filteredRequests.length > 0" class="requests-section">
          <div class="section-header">
            <h3>Online Requests ({{ filteredRequests.length }})</h3>
          </div>
          <div class="requests-list">
            <div
              v-for="request in filteredRequests"
              :key="request.id"
              class="request-card"
              :class="getStatusClass(request.status)"
            >
              <div class="request-header">
                <div class="request-info">
                  <h3>{{ request.username }} (ID: {{ request.user_id }})</h3>
                  <div class="date-info">
                    <span class="submitted-date">
                      <strong>Submitted:</strong>
                      {{ formatDateTime(request.created_at) }}
                    </span>
                    <span
                      v-if="
                        request.updated_at &&
                        request.updated_at !== request.created_at
                      "
                      class="updated-date"
                    >
                      <strong>Last Updated:</strong>
                      {{ formatDateTime(request.updated_at) }}
                    </span>
                    <span
                      v-if="
                        request.status_updated_at &&
                        request.status_updated_at !== request.created_at
                      "
                      class="status-updated-info"
                    >
                      <strong>Status Updated:</strong>
                      {{ formatDateTime(request.status_updated_at) }}
                      <span v-if="request.status_updated_by" class="updated-by">
                        by User ID {{ request.status_updated_by }}
                      </span>
                    </span>
                  </div>
                </div>
                <div class="request-status">
                  <span class="status-badge" :class="request.status">{{
                    request.status.toUpperCase()
                  }}</span>
                </div>
              </div>

              <div class="request-content">
                <div class="issue-date">
                  <strong>Issue Date (User Specified):</strong>
                  {{ formatDateOnly(request.issue_date) }}
                </div>
                <div class="issue-description">
                  <strong>Issue Description:</strong>
                  <p>{{ request.issue_description }}</p>
                </div>
              </div>

              <div class="request-actions">
                <select
                  v-model="request.status"
                  @change="updateStatus(request.id, request.status)"
                  class="status-select"
                >
                  <option value="pending">Pending</option>
                  <option value="in_progress">In Progress</option>
                  <option value="resolved">Resolved</option>
                  <option value="closed">Closed</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <!-- Offline Requests Section -->
        <div v-if="filteredOfflineRequests.length > 0" class="requests-section">
          <div class="section-header">
            <h3>Offline Requests ({{ filteredOfflineRequests.length }})</h3>
            <span class="offline-indicator"
              >⚠️ Stored locally - will sync when backend is available</span
            >
          </div>
          <div class="requests-list">
            <div
              v-for="request in filteredOfflineRequests"
              :key="request.id"
              class="request-card offline-request"
            >
              <div class="request-header">
                <div class="request-info">
                  <h3>{{ request.username }} (ID: {{ request.userId }})</h3>
                  <div class="date-info">
                    <span class="submitted-date">
                      <strong>Stored Locally:</strong>
                      {{ formatDateTime(request.created_at) }}
                    </span>
                    <span
                      v-if="request.submission_attempts > 0"
                      class="attempts-info"
                    >
                      <strong>Sync Attempts:</strong>
                      {{ request.submission_attempts }}
                    </span>
                  </div>
                </div>
                <div class="request-status">
                  <span class="status-badge offline-pending"
                    >OFFLINE PENDING</span
                  >
                </div>
              </div>

              <div class="request-content">
                <div class="issue-date">
                  <strong>Issue Date (User Specified):</strong>
                  {{ formatDateOnly(request.date) }}
                </div>
                <div class="issue-description">
                  <strong>Issue Description:</strong>
                  <p>{{ request.issue }}</p>
                </div>
              </div>

              <div class="request-actions">
                <button
                  @click="syncOfflineRequest(request.id)"
                  class="sync-btn"
                  :disabled="loading"
                >
                  🔄 Sync Now
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- No Requests Message -->
        <div
          v-if="
            filteredRequests.length === 0 &&
            filteredOfflineRequests.length === 0
          "
          class="no-requests"
        >
          <p>No tech support requests found matching your criteria.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { currentUser } from "@/stores/userStore";
import axios from "axios";

export default {
  name: "TechSupportManagement",
  data() {
    return {
      requests: [],
      offlineRequests: [],
      filteredRequests: [],
      filteredOfflineRequests: [],
      loading: true,
      statusFilter: "",
      searchQuery: "",
      showSuccessMessage: false,
      successMessage: "",
      showOfflineRequests: true,
      exportLimit: 50,
    };
  },
  async mounted() {
    // Initialize user store if not already done
    const { initializeUser } = await import("@/stores/userStore");
    initializeUser();
    await this.loadRequests();
    this.loadOfflineRequests();

    // Add keyboard event listener for popup
    document.addEventListener("keydown", this.handleKeydown);
  },

  beforeUnmount() {
    // Remove keyboard event listener
    document.removeEventListener("keydown", this.handleKeydown);
  },
  methods: {
    goBack() {
      // Go back to user activities page or admin dashboard
      this.$router.push("/user-activities");
    },
    async loadRequests() {
      try {
        this.loading = true;
        const response = await fetch("http://127.0.0.1:5000/api/tech-support");
        const data = await response.json();

        if (data.success) {
          this.requests = data.requests;
          this.filteredRequests = [...this.requests];
        } else {
          console.error("Failed to load requests:", data.message);
        }
      } catch (error) {
        console.error("Error loading requests:", error);
      } finally {
        this.loading = false;
      }
    },

    loadOfflineRequests() {
      try {
        const offlineData = JSON.parse(
          localStorage.getItem("tech_support_offline") || "[]"
        );
        this.offlineRequests = offlineData.map((request) => ({
          ...request,
          isOffline: true,
          status: "offline_pending",
        }));
        this.filteredOfflineRequests = [...this.offlineRequests];
        console.log(`Loaded ${this.offlineRequests.length} offline requests`);
      } catch (error) {
        console.error("Error loading offline requests:", error);
        this.offlineRequests = [];
        this.filteredOfflineRequests = [];
      }
    },

    async syncOfflineRequest(requestId) {
      try {
        const request = this.offlineRequests.find((r) => r.id === requestId);
        if (!request) return;

        const requestData = {
          username: request.username,
          userId: request.userId,
          date: request.date,
          issue: request.issue,
        };

        const response = await fetch("http://127.0.0.1:5000/api/tech-support", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(requestData),
          mode: "cors",
        });

        const data = await response.json();

        if (data.success) {
          if (data.duplicate) {
            // Request was already submitted, remove from offline anyway
            this.offlineRequests = this.offlineRequests.filter(
              (r) => r.id !== requestId
            );
            this.filteredOfflineRequests = this.filteredOfflineRequests.filter(
              (r) => r.id !== requestId
            );

            // Update localStorage
            const updatedOffline = JSON.parse(
              localStorage.getItem("tech_support_offline") || "[]"
            );
            const filteredOffline = updatedOffline.filter(
              (r) => r.id !== requestId
            );
            localStorage.setItem(
              "tech_support_offline",
              JSON.stringify(filteredOffline)
            );

            this.showSuccessNotification(
              `Request was already submitted (ID: ${data.existing_request_id}). Removed from offline list.`
            );
          } else {
            // Remove from offline requests
            this.offlineRequests = this.offlineRequests.filter(
              (r) => r.id !== requestId
            );
            this.filteredOfflineRequests = this.filteredOfflineRequests.filter(
              (r) => r.id !== requestId
            );

            // Update localStorage
            const updatedOffline = JSON.parse(
              localStorage.getItem("tech_support_offline") || "[]"
            );
            const filteredOffline = updatedOffline.filter(
              (r) => r.id !== requestId
            );
            localStorage.setItem(
              "tech_support_offline",
              JSON.stringify(filteredOffline)
            );

            this.showSuccessNotification(`Offline request synced successfully`);
          }
          await this.loadRequests(); // Reload online requests
        } else {
          throw new Error(data.message || "Sync failed");
        }
      } catch (error) {
        console.error("Error syncing offline request:", error);
        alert("Failed to sync offline request. Please try again.");
      }
    },

    async exportToPDF() {
      try {
        // Ensure data is loaded before exporting
        if (this.loading) {
          alert("Please wait for data to load before exporting.");
          return;
        }

        // Show loading state
        this.loading = true;

        // Call backend PDF endpoint with limit
        const params = {};
        if (this.exportLimit && this.exportLimit > 0) {
          params.limit = this.exportLimit;
        }

        const response = await axios.get(
          "http://127.0.0.1:5000/api/tech-support/pdf",
          {
            params,
            responseType: "blob",
          }
        );

        // Create blob URL and trigger download
        const blob = new Blob([response.data], { type: "application/pdf" });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = `tech_support_requests_${new Date().toISOString().split("T")[0]}.pdf`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);

        this.showSuccessNotification("Tech support requests exported to PDF successfully");
      } catch (error) {
        console.error("Error exporting to PDF:", error);
        alert("Failed to export PDF. Please try again.");
      } finally {
        this.loading = false;
      }
    },


    async updateStatus(requestId, newStatus) {
      try {
        // Get current admin user ID
        const currentAdmin = currentUser();
        console.log("Current admin user:", currentAdmin); // Debug log

        // Try to get user ID from different possible field names
        const adminUserId =
          currentAdmin?.id || currentAdmin?.user_id || currentAdmin?.userId;

        if (!currentAdmin || !adminUserId) {
          console.error("User object structure:", currentAdmin);
          alert(
            "Unable to identify admin user. Please refresh the page and try again."
          );
          return;
        }

        const response = await fetch(
          `http://127.0.0.1:5000/api/tech-support/${requestId}/status`,
          {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              status: newStatus,
              admin_user_id: adminUserId,
            }),
            mode: "cors",
          }
        );

        const data = await response.json();
        console.log("Status update response:", data); // Debug log

        if (data.success) {
          // Update the local request status
          const request = this.requests.find((r) => r.id === requestId);
          if (request) {
            request.status = newStatus;
            request.status_updated_by = adminUserId;
            request.status_updated_at = new Date().toISOString();
            request.updated_at = new Date().toISOString();
          }
          this.filterRequests();

          // Show success message
          this.showSuccessNotification(
            `Status updated successfully to "${newStatus.toUpperCase()}"`
          );
        } else {
          alert("Failed to update status: " + data.message);
        }
      } catch (error) {
        console.error("Error updating status:", error);
        alert("Error updating status. Please try again.");
      }
    },

    filterRequests() {
      // Filter online requests
      let filtered = [...this.requests];

      // Filter by status
      if (this.statusFilter) {
        filtered = filtered.filter(
          (request) => request.status === this.statusFilter
        );
      }

      // Filter by search query
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(
          (request) =>
            request.username.toLowerCase().includes(query) ||
            request.user_id.toString().includes(query) ||
            request.issue_description.toLowerCase().includes(query)
        );
      }

      this.filteredRequests = filtered;

      // Filter offline requests
      let filteredOffline = [...this.offlineRequests];

      // Filter by status (offline requests are always 'offline_pending')
      if (this.statusFilter && this.statusFilter !== "offline_pending") {
        filteredOffline = [];
      }

      // Filter by search query
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filteredOffline = filteredOffline.filter(
          (request) =>
            request.username.toLowerCase().includes(query) ||
            request.userId.toString().includes(query) ||
            request.issue.toLowerCase().includes(query)
        );
      }

      this.filteredOfflineRequests = filteredOffline;
    },

    formatDateTime(dateString) {
      if (!dateString) return "N/A";
      const date = new Date(dateString);
      // Use local timezone for display
      const formatted = date.toLocaleDateString("en-US", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        hour12: true,
      });
      // Add timezone info
      const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
      return `${formatted} (${timezone})`;
    },

    formatDateOnly(dateString) {
      if (!dateString) return "N/A";
      const date = new Date(dateString);
      // Format as date only (user-specified issue date)
      return date.toLocaleDateString("en-US", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
      });
    },

    getStatusClass(status) {
      return `status-${status}`;
    },

    showSuccessNotification(message) {
      this.successMessage = message;
      this.showSuccessMessage = true;

      // Auto-hide after 4 seconds
      setTimeout(() => {
        this.hideSuccessMessage();
      }, 4000);
    },

    hideSuccessMessage() {
      this.showSuccessMessage = false;
      this.successMessage = "";
    },

    handleKeydown(event) {
      // Close popup on Escape key
      if (event.key === "Escape" && this.showSuccessMessage) {
        this.hideSuccessMessage();
      }
    },
  },
};
</script>

<style scoped>
.tech-support-management {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 30px;
  position: relative;
}

.page-header .header-content {
  flex: 1;
  text-align: center;
}

.page-header h1 {
  color: #162845;
  font-size: 2.5rem;
  margin-bottom: 10px;
}

.page-header p {
  color: #666;
  font-size: 1.1rem;
}

.page-header .back-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background-color: #162845;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
}

.page-header .back-button:hover {
  background-color: #0f1d35;
}

.page-header .back-button svg {
  width: 20px;
  height: 20px;
}

/* Success Popup Modal Styles */
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease-out;
}

.popup-modal {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  max-width: 400px;
  width: 90%;
  max-height: 90vh;
  overflow: hidden;
  animation: slideIn 0.3s ease-out;
}

.popup-header {
  background: linear-gradient(135deg, #28a745, #20c997);
  color: white;
  padding: 20px;
  text-align: center;
  position: relative;
}

.popup-icon {
  margin-bottom: 10px;
}

.success-checkmark {
  background: rgba(255, 255, 255, 0.2);
  border: 3px solid white;
  border-radius: 50%;
  width: 60px;
  height: 60px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  font-weight: bold;
  margin: 0 auto;
}

.popup-header h3 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.popup-body {
  padding: 25px 20px;
  text-align: center;
}

.popup-body p {
  margin: 0;
  color: #333;
  font-size: 1.1rem;
  line-height: 1.5;
}

.popup-footer {
  padding: 20px;
  text-align: center;
  background: #f8f9fa;
  border-top: 1px solid #e9ecef;
}

.popup-btn {
  background: #28a745;
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 100px;
}

.popup-btn:hover {
  background: #218838;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(40, 167, 69, 0.3);
}

.popup-btn:active {
  transform: translateY(0);
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: scale(0.8) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.filters-section {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 10px;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.filter-group label {
  font-weight: bold;
  color: #162845;
}

.filter-group select,
.filter-group input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
}

.requests-container {
  min-height: 400px;
}

.loading,
.no-requests {
  text-align: center;
  padding: 40px;
  color: #666;
  font-size: 1.1rem;
}

.requests-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.request-card {
  background: #ebf7fd;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-left: 4px solid #ddd;
  transition: all 0.3s ease;
}

.request-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.request-card.status-pending {
  border-left-color: #ffc107;
}

.request-card.status-in_progress {
  border-left-color: #17a2b8;
}

.request-card.status-resolved {
  border-left-color: #28a745;
}

.request-card.status-closed {
  border-left-color: #6c757d;
}

.request-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.request-info h3 {
  margin: 0 0 10px 0;
  color: #162845;
  font-size: 1.2rem;
}

.date-info {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.submitted-date,
.updated-date {
  color: #666;
  font-size: 0.9rem;
}

.submitted-date strong,
.updated-date strong {
  color: #162845;
}

.updated-date {
  font-style: italic;
  color: #888;
}

.status-updated-info {
  color: #666;
  font-size: 0.9rem;
  background: #e8f4fd;
  padding: 4px 8px;
  border-radius: 4px;
  border-left: 3px solid #17a2b8;
}

.status-updated-info strong {
  color: #17a2b8;
}

.updated-by {
  font-style: italic;
  color: #555;
  margin-left: 5px;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: bold;
  text-transform: uppercase;
}

.status-badge.pending {
  background: #fff3cd;
  color: #856404;
}

.status-badge.in_progress {
  background: #d1ecf1;
  color: #0c5460;
}

.status-badge.resolved {
  background: #d4edda;
  color: #155724;
}

.status-badge.closed {
  background: #e2e3e5;
  color: #383d41;
}

.request-content {
  margin-bottom: 15px;
}

.issue-date {
  margin-bottom: 10px;
  color: #666;
  padding: 8px 12px;
  background: #f8f9fa;
  border-radius: 5px;
  border-left: 3px solid #162845;
}

.issue-date strong {
  color: #162845;
}

.issue-description {
  color: #333;
}

.issue-description p {
  margin: 5px 0 0 0;
  line-height: 1.5;
  white-space: pre-wrap;
}

.request-actions {
  display: flex;
  justify-content: flex-end;
}

.status-select {
  padding: 6px 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background: #fff;
  font-size: 14px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .filters-section {
    flex-direction: column;
    gap: 15px;
  }

  .request-header {
    flex-direction: column;
    gap: 10px;
  }

  .request-actions {
    justify-content: flex-start;
  }

  .popup-modal {
    max-width: 350px;
    width: 95%;
  }

  .popup-header {
    padding: 15px;
  }

  .success-checkmark {
    width: 50px;
    height: 50px;
    font-size: 24px;
  }

  .popup-header h3 {
    font-size: 1.3rem;
  }

  .popup-body {
    padding: 20px 15px;
  }

  .popup-body p {
    font-size: 1rem;
  }

  .popup-footer {
    padding: 15px;
  }

  .popup-btn {
    padding: 10px 25px;
    font-size: 0.9rem;
  }
}

/* Export Controls */
.export-controls {
  display: flex;
  gap: 15px;
  align-items: flex-end;
  margin-left: auto;
}

.export-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.export-group label {
  font-weight: bold;
  color: #162845;
}

.export-group select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background: #fff;
  font-size: 14px;
}

.export-btn {
  background: #28a745;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: background-color 0.3s ease;
}

.export-btn:hover {
  background: #218838;
}

/* Section Headers */
.requests-section {
  margin-bottom: 30px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #e9ecef;
}

.section-header h3 {
  margin: 0;
  color: #162845;
  font-size: 1.3rem;
}

.offline-indicator {
  background: #fff3cd;
  color: #856404;
  padding: 5px 10px;
  border-radius: 15px;
  font-size: 0.85rem;
  font-weight: 500;
}

/* Offline Request Styles */
.offline-request {
  background: #fff9e6;
  border-left: 4px solid #ffc107;
}

.offline-request .request-header h3 {
  color: #856404;
}

.attempts-info {
  color: #856404;
  font-size: 0.9rem;
  font-style: italic;
}

.attempts-info strong {
  color: #6c5b00;
}

.status-badge.offline-pending {
  background: #ffc107;
  color: #212529;
}

.sync-btn {
  background: #17a2b8;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.sync-btn:hover:not(:disabled) {
  background: #138496;
  transform: translateY(-1px);
}

.sync-btn:disabled {
  background: #6c757d;
  cursor: not-allowed;
  transform: none;
}
</style>
