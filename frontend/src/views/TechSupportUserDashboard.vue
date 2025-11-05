<template>
  <div class="tech-support-user-dashboard">
    <div class="header">
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
      <h1 class="page-title">My Tech Support Requests</h1>
    </div>

    <div class="dashboard-content">
      <!-- Summary Cards -->
      <div class="summary-cards">
        <div class="summary-card">
          <div class="card-icon pending">
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
              <polyline points="12,6 12,12 16,14"></polyline>
            </svg>
          </div>
          <div class="card-content">
            <h3>{{ statusCounts.pending }}</h3>
            <p>Pending</p>
          </div>
        </div>

        <div class="summary-card">
          <div class="card-icon in-progress">
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
                d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"
              ></path>
              <polyline points="3.27,6.96 12,12.01 20.73,6.96"></polyline>
              <line x1="12" y1="22.08" x2="12" y2="12"></line>
            </svg>
          </div>
          <div class="card-content">
            <h3>{{ statusCounts.in_progress }}</h3>
            <p>In Progress</p>
          </div>
        </div>

        <div class="summary-card">
          <div class="card-icon resolved">
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
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
              <polyline points="22,4 12,14.01 9,11.01"></polyline>
            </svg>
          </div>
          <div class="card-content">
            <h3>{{ statusCounts.resolved }}</h3>
            <p>Resolved</p>
          </div>
        </div>

        <div class="summary-card">
          <div class="card-icon closed">
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
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </div>
          <div class="card-content">
            <h3>{{ statusCounts.closed }}</h3>
            <p>Closed</p>
          </div>
        </div>
      </div>

      <!-- Actions Bar -->
      <div class="actions-bar">
        <button
          @click="refreshRequests"
          class="refresh-btn"
          :disabled="loading"
        >
          <svg
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
            <polyline points="23,4 23,10 17,10"></polyline>
            <polyline points="1,20 1,14 7,14"></polyline>
            <path
              d="M20.49,9A9,9,0,0,0,5.64,5.64L1,10m22,4L18.36,18.36A9,9,0,0,1,3.51,15"
            ></path>
          </svg>
          {{ loading ? "Refreshing..." : "Refresh" }}
        </button>

        <button @click="submitNewRequest" class="new-request-btn">
          <svg
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
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
          Submit New Request
        </button>
      </div>

      <!-- Requests List -->
      <div class="requests-section">
        <h2>Your Tech Support Requests</h2>

        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          <p>Loading your requests...</p>
        </div>

        <div v-else-if="requests.length === 0" class="empty-state">
          <div class="empty-icon">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="64"
              height="64"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M9 12l2 2 4-4"></path>
              <path
                d="M21 12c.552 0 1-.448 1-1V5c0-.552-.448-1-1-1H3c-.552 0-1 .448-1 1v6c0 .552.448 1 1 1h18z"
              ></path>
              <path
                d="M3 12h18v6c0 .552-.448 1-1 1H4c-.552 0-1-.448-1-1v-6z"
              ></path>
            </svg>
          </div>
          <h3>No Tech Support Requests</h3>
          <p>You haven't submitted any tech support requests yet.</p>
          <button @click="submitNewRequest" class="submit-first-btn">
            Submit Your First Request
          </button>
        </div>

        <div v-else class="requests-list">
          <div
            v-for="request in requests"
            :key="request.id"
            class="request-card"
            :class="`status-${request.status}`"
          >
            <div class="request-header">
              <div class="request-id">#{{ request.id }}</div>
              <div class="request-status" :class="`status-${request.status}`">
                {{ formatStatus(request.status) }}
              </div>
            </div>

            <div class="request-content">
              <div class="request-description">
                {{ request.issue_description }}
              </div>

              <div class="request-meta">
                <div class="meta-item">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <rect
                      x="3"
                      y="4"
                      width="18"
                      height="18"
                      rx="2"
                      ry="2"
                    ></rect>
                    <line x1="16" y1="2" x2="16" y2="6"></line>
                    <line x1="8" y1="2" x2="8" y2="6"></line>
                    <line x1="3" y1="10" x2="21" y2="10"></line>
                  </svg>
                  <span>Submitted: {{ formatDate(request.created_at) }}</span>
                </div>

                <div class="meta-item" v-if="request.status_updated_at">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <circle cx="12" cy="12" r="10"></circle>
                    <polyline points="12,6 12,12 16,14"></polyline>
                  </svg>
                  <span
                    >Last Updated:
                    {{ formatDate(request.status_updated_at) }}</span
                  >
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
import { userStore } from "@/stores/userStore";

export default {
  name: "TechSupportUserDashboard",
  data() {
    return {
      requests: [],
      loading: false,
      error: null,
    };
  },
  computed: {
    statusCounts() {
      const counts = {
        pending: 0,
        in_progress: 0,
        resolved: 0,
        closed: 0,
      };

      this.requests.forEach((request) => {
        if (counts.hasOwnProperty(request.status)) {
          counts[request.status]++;
        }
      });

      return counts;
    },
  },
  async mounted() {
    await this.loadUserRequests();
  },
  methods: {
    async loadUserRequests() {
      try {
        this.loading = true;
        this.error = null;

        const currentUser = userStore.getters.currentUser();
        if (!currentUser || !currentUser.id) {
          this.error = "User information not available";
          return;
        }

        const response = await fetch(
          `http://127.0.0.1:5000/api/tech-support/user/${currentUser.id}`
        );
        const data = await response.json();

        if (data.success) {
          this.requests = data.requests || [];
        } else {
          this.error = data.message || "Failed to load requests";
        }
      } catch (error) {
        console.error("Error loading user requests:", error);
        this.error = "Failed to load requests. Please try again.";
      } finally {
        this.loading = false;
      }
    },

    async refreshRequests() {
      await this.loadUserRequests();
    },

    submitNewRequest() {
      this.$router.push({ name: "TechSupport" });
    },

    formatStatus(status) {
      const statusMap = {
        pending: "Pending",
        in_progress: "In Progress",
        resolved: "Resolved",
        closed: "Closed",
      };
      return statusMap[status] || status;
    },

    formatDate(dateString) {
      if (!dateString) return "N/A";
      const date = new Date(dateString);
      return date.toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    },
  },
};
</script>

<style scoped>
.tech-support-user-dashboard {
  min-height: 100vh;
  background-color: #f5f7fa;
  padding: 20px;
}

.header {
  display: flex;
  align-items: center;
  margin-bottom: 30px;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
}

.back-button {
  background: none;
  border: none;
  cursor: pointer;
  margin-right: 20px;
  padding: 8px;
  border-radius: 8px;
  transition: background-color 0.2s;
}

.back-button:hover {
  background-color: #e9ecef;
}

.page-title {
  font-size: 2rem;
  font-weight: bold;
  color: #2c3e50;
  margin: 0;
}

.dashboard-content {
  max-width: 1200px;
  margin: 0 auto;
}

.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.summary-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 16px;
}

.card-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.card-icon.pending {
  background-color: #f39c12;
}

.card-icon.in-progress {
  background-color: #3498db;
}

.card-icon.resolved {
  background-color: #27ae60;
}

.card-icon.closed {
  background-color: #95a5a6;
}

.card-content h3 {
  font-size: 2rem;
  font-weight: bold;
  margin: 0;
  color: #2c3e50;
}

.card-content p {
  margin: 4px 0 0 0;
  color: #7f8c8d;
  font-weight: 500;
}

.actions-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  gap: 16px;
}

.refresh-btn,
.new-request-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.refresh-btn {
  background-color: #6c757d;
  color: white;
}

.refresh-btn:hover:not(:disabled) {
  background-color: #5a6268;
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.new-request-btn {
  background-color: #007bff;
  color: white;
}

.new-request-btn:hover {
  background-color: #0056b3;
}

.requests-section h2 {
  font-size: 1.5rem;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 20px;
}

.loading-state,
.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.empty-icon {
  color: #bdc3c7;
  margin-bottom: 16px;
}

.empty-state h3 {
  font-size: 1.25rem;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 8px;
}

.empty-state p {
  color: #7f8c8d;
  margin-bottom: 24px;
}

.submit-first-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.submit-first-btn:hover {
  background-color: #0056b3;
}

.requests-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.request-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-left: 4px solid #ddd;
  transition: all 0.2s;
}

.request-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.request-card.status-pending {
  border-left-color: #f39c12;
}

.request-card.status-in_progress {
  border-left-color: #3498db;
}

.request-card.status-resolved {
  border-left-color: #27ae60;
}

.request-card.status-closed {
  border-left-color: #95a5a6;
}

.request-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.request-id {
  font-weight: bold;
  color: #2c3e50;
  font-size: 1.1rem;
}

.request-status {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 500;
  text-transform: uppercase;
}

.request-status.status-pending {
  background-color: #fef3cd;
  color: #856404;
}

.request-status.status-in_progress {
  background-color: #d1ecf1;
  color: #0c5460;
}

.request-status.status-resolved {
  background-color: #d4edda;
  color: #155724;
}

.request-status.status-closed {
  background-color: #e2e3e5;
  color: #383d41;
}

.request-content {
  margin-bottom: 16px;
}

.request-description {
  font-size: 1rem;
  line-height: 1.5;
  color: #2c3e50;
  margin-bottom: 16px;
}

.request-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #7f8c8d;
  font-size: 0.875rem;
}

.meta-item svg {
  color: #bdc3c7;
}

/* Responsive Design */
@media (max-width: 768px) {
  .tech-support-user-dashboard {
    padding: 16px;
  }

  .summary-cards {
    grid-template-columns: 1fr;
  }

  .actions-bar {
    flex-direction: column;
    align-items: stretch;
  }

  .request-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .request-meta {
    flex-direction: column;
    gap: 8px;
  }
}
</style>
