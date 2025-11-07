<template>
  <div class="notifications-page">
    <!-- Header -->
    <div class="page-header">
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
        <h1 class="page-title">Notifications</h1>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <div v-if="loading" class="loading-message">Loading notifications...</div>
      <div v-else-if="error" class="error-message">
        {{ error }}
        <button @click="fetchNotifications" class="retry-button">Retry</button>
      </div>
      <div v-else-if="notifications.length === 0" class="no-notifications">
        <p>You have no notifications.</p>
      </div>
      <div v-else class="notifications-section">
        <div class="table-container">
          <table class="notifications-table">
            <thead>
              <tr>
                <th>Activity</th>
                <th>Project</th>
                <th>Details</th>
                <th>From</th>
                <th>Timestamp</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="notification in notifications"
                :key="notification.activity_id"
                :class="{ unread: !notification.is_read }"
              >
                <td>{{ notification.activity_performed }}</td>
                <td>{{ notification.project_name || "N/A" }}</td>
                <td class="details-cell">{{ notification.additional_info }}</td>
                <td>{{ notification.performed_by_name || "Unknown" }}</td>
                <td>{{ formatTimestamp(notification.timestamp) }}</td>
                <td>
                  <span
                    class="status-badge"
                    :class="notification.is_read ? 'read' : 'unread'"
                  >
                    {{ notification.is_read ? "Read" : "Unread" }}
                  </span>
                </td>
                <td>
                  <button
                    class="view-button"
                    @click="viewNotification(notification)"
                  >
                    View Details
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Notification Detail Overlay -->
    <div
      v-if="showOverlay && selectedNotification"
      class="overlay"
      @click="closeOverlay"
    >
      <div class="overlay-content" @click.stop>
        <div class="overlay-header">
          <h2>Notification Details</h2>
          <button class="close-button" @click="closeOverlay">×</button>
        </div>

        <div class="overlay-body">
          <div class="form-group">
            <label>Activity Type:</label>
            <input
              type="text"
              :value="selectedNotification.activity_performed"
              readonly
            />
          </div>

          <div class="form-group">
            <label>Project:</label>
            <input
              type="text"
              :value="selectedNotification.project_name || 'N/A'"
              readonly
            />
          </div>

          <div class="form-group">
            <label>From:</label>
            <input
              type="text"
              :value="selectedNotification.performed_by_name || 'Unknown'"
              readonly
            />
          </div>

          <div class="form-group">
            <label>Timestamp:</label>
            <input
              type="text"
              :value="formatTimestamp(selectedNotification.timestamp)"
              readonly
            />
          </div>

          <div class="form-group">
            <label>Details:</label>
            <textarea
              :value="selectedNotification.additional_info"
              readonly
              rows="5"
            ></textarea>
          </div>
        </div>

        <div class="overlay-footer">
          <button class="close-detail-button" @click="closeOverlay">
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { userStore } from "@/stores/userStore";

export default {
  name: "QAHeadNotifications",
  data() {
    return {
      notifications: [],
      loading: false,
      error: null,
      showOverlay: false,
      selectedNotification: null,
    };
  },
  async mounted() {
    await this.fetchNotifications();
  },
  methods: {
    async fetchNotifications() {
      this.loading = true;
      this.error = null;

      try {
        const currentUser = userStore.getters.currentUser();

        if (!currentUser || !currentUser.id) {
          this.error = "User not logged in";
          return;
        }

        const response = await fetch(
          `http://localhost:5000/api/notifications/${currentUser.id}`,
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
            },
          }
        );

        const data = await response.json();

        if (data.success) {
          this.notifications = data.notifications;
        } else {
          this.error = data.message || "Failed to fetch notifications";
        }
      } catch (error) {
        console.error("Error fetching notifications:", error);
        this.error = "Failed to load notifications. Please try again.";
      } finally {
        this.loading = false;
      }
    },
    formatTimestamp(timestamp) {
      if (!timestamp) return "N/A";
      const date = new Date(timestamp);
      return date.toLocaleString();
    },
    async viewNotification(notification) {
      this.selectedNotification = { ...notification };
      this.showOverlay = true;

      // Mark as read if not already read
      if (!notification.is_read) {
        await this.markAsRead(notification.activity_id);
      }
    },
    async markAsRead(notificationId) {
      try {
        const response = await fetch(
          `http://localhost:5000/api/notifications/${notificationId}/mark-read`,
          {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
            },
          }
        );

        const data = await response.json();

        if (data.success) {
          // Update local state
          const notif = this.notifications.find(
            (n) => n.activity_id === notificationId
          );
          if (notif) {
            notif.is_read = true;
          }
        }
      } catch (error) {
        console.error("Error marking notification as read:", error);
      }
    },
    closeOverlay() {
      this.showOverlay = false;
      this.selectedNotification = null;
    },
  },
};
</script>

<style scoped>
.notifications-page {
  min-height: 100vh;
  background: #ebf7fd;
}

/* Header */
.page-header {
  background: #2d3748;
  padding: 20px 30px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 15px;
}

.back-button {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  cursor: pointer;
  padding: 10px;
  border-radius: 50%;
  transition: all 0.3s ease;
  color: white;
}

.back-button:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.05);
}

.app-logo {
  width: 120px;
  height: auto;
  filter: brightness(0) invert(1);
}

.header-center {
  flex: 1;
  text-align: center;
}

.page-title {
  color: white;
  font-size: 2.2em;
  font-weight: 700;
  margin: 0;
  letter-spacing: 2px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

/* Main Content */
.main-content {
  max-width: 1400px;
  margin: 30px auto;
  padding: 0 30px;
}

/* Notifications Section */
.notifications-section {
  background: #ebf7fd;
  padding: 25px;
  border-radius: 15px;
  /* box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); */
}

.table-container {
  overflow-x: auto;
}

.notifications-table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
}

.notifications-table th {
  background: #2d3748;
  color: white;
  padding: 15px;
  text-align: left;
  font-weight: 600;
  font-size: 0.9em;
}

.notifications-table td {
  padding: 15px;
  border-bottom: 1px solid #e2e8f0;
  vertical-align: top;
}

.notifications-table tr:nth-child(even) {
  background-color: #f8fafc;
}

.notifications-table tr:hover {
  background-color: #edf2f7;
}

.notifications-table tr.unread {
  background-color: #fff3cd;
  border-left: 4px solid #ffc107;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-weight: bold;
  font-size: 0.8em;
  text-transform: uppercase;
}

.status-badge.pending {
  background-color: #fff3cd;
  color: #856404;
}

.status-badge.accepted {
  background-color: #d4edda;
  color: #155724;
}

.status-badge.rejected {
  background-color: #f8d7da;
  color: #721c24;
}

.status-badge.unread {
  background-color: #dc3545;
  color: white;
}

.status-badge.read {
  background-color: #5a82a5;
  color: white;
}

.loading-message,
.error-message,
.no-notifications {
  text-align: center;
  padding: 40px;
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  margin: 30px auto;
  max-width: 600px;
}

.loading-message {
  color: #007bff;
  font-size: 1.2em;
}

.error-message {
  color: #dc3545;
  font-size: 1.1em;
}

.no-notifications {
  color: #6c757d;
}

.retry-button {
  margin-top: 15px;
  padding: 10px 20px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.retry-button:hover {
  background: #0056b3;
  transform: translateY(-1px);
}

.details-cell {
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.close-detail-button {
  padding: 12px 24px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.close-detail-button:hover {
  background: #0056b3;
  transform: translateY(-1px);
}

.view-button {
  background: #007bff;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.view-button:hover {
  background: #0056b3;
  transform: translateY(-1px);
}

/* Overlay */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.overlay-content {
  background: white;
  border-radius: 15px;
  width: 30%;
  /* max-width: 600px; */
  max-height: 60vh;
  overflow-y: auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.overlay-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 25px;
  border-bottom: 1px solid #e2e8f0;
}

.overlay-header h2 {
  margin: 0;
  color: #2d3748;
  font-size: 1.5em;
}

.close-button {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.close-button:hover {
  background: #f0f0f0;
  color: #333;
}

.overlay-body {
  padding: 25px;
  margin: 0px;
  /* margin-bottom: 70px; */
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #4a5568;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.3s ease;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.form-group input[readonly] {
  background-color: #f8f9fa;
  color: #6c757d;
}

.overlay-footer {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  padding: 20px 25px;
  border-top: 1px solid #e2e8f0;
}

.accept-button,
.reject-button {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.accept-button {
  background: #28a745;
  color: white;
}

.accept-button:hover {
  background: #218838;
  transform: translateY(-1px);
}

.reject-button {
  background: #dc3545;
  color: white;
}

.reject-button:hover {
  background: #c82333;
  transform: translateY(-1px);
}

/* Responsive Design */
@media (max-width: 768px) {
  .page-header {
    padding: 15px 20px;
    flex-direction: column;
    gap: 15px;
  }

  .page-title {
    font-size: 1.8em;
  }

  .main-content {
    padding: 0 20px;
    margin: 20px auto;
  }

  .overlay-content {
    width: 95%;
    margin: 20px;
  }

  .notifications-table {
    font-size: 0.9em;
  }

  .notifications-table th,
  .notifications-table td {
    padding: 10px 8px;
  }
}
</style>
