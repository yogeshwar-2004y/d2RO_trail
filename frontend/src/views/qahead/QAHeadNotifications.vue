<template>
  <div class="notifications-page">
    <!-- Header -->
    <div class="page-header">
      <div class="header-left">
        <button class="back-button" @click="$router.go(-1)">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19 12H5"></path>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
        </button>
      </div>
      <div class="header-center">
        <h1 class="page-title">Received Requests</h1>
      </div>
    </div>

         <!-- Main Content -->
     <div class="main-content">
       <!-- Notifications Table -->
      <div class="notifications-section">
        <div class="table-container">
          <table class="notifications-table">
            <thead>
              <tr>
                <th>Project</th>
                <th>Serial Number</th>
                <th>LRU</th>
                <th>Completed Stage</th>
                <th>Required Stage</th>
                <th>Justification</th>
                <th>Status</th>
                <th>Timestamp</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="notification in notifications" :key="notification.id" :class="{ 'unread': !notification.isRead }">
                <td>{{ notification.project }}</td>
                <td>{{ notification.serialNumber }}</td>
                <td>{{ notification.lru }}</td>
                <td>{{ notification.completedStage }}</td>
                <td>{{ notification.requiredStage }}</td>
                <td>{{ notification.justification }}</td>
                <td>
                  <span class="status-badge" :class="notification.status">
                    {{ notification.status }}
                  </span>
                </td>
                <td>{{ formatTimestamp(notification.timestamp) }}</td>
                <td>
                  <button class="view-button" @click="viewNotification(notification)">
                    View
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Notification Detail Overlay -->
    <div v-if="showOverlay" class="overlay" @click="closeOverlay">
      <div class="overlay-content" @click.stop>
        <div class="overlay-header">
          <h2>Project Details</h2>
          <button class="close-button" @click="closeOverlay">×</button>
        </div>
        
        <div class="overlay-body">
          <div class="form-group">
            <label>Project Name:</label>
            <input type="text" v-model="selectedNotification.project" readonly>
          </div>
          
          <div class="form-group">
            <label>Serial Number:</label>
            <input type="text" v-model="selectedNotification.serialNumber" readonly>
          </div>
          
          <div class="form-group">
            <label>LRU:</label>
            <input type="text" v-model="selectedNotification.lru" readonly>
          </div>
          
          <div class="form-group">
            <label>Completed Stage:</label>
            <input type="text" v-model="selectedNotification.completedStage" readonly>
          </div>
          
          <div class="form-group">
            <label>Required Stage:</label>
            <input type="text" v-model="selectedNotification.requiredStage" readonly>
          </div>
          
          <div class="form-group">
            <label>Justification:</label>
            <textarea v-model="selectedNotification.justification" readonly rows="3"></textarea>
          </div>
          
          <div class="form-group">
            <label>Comments:</label>
            <textarea v-model="comments" placeholder="Add your comments here..." rows="4"></textarea>
          </div>
        </div>
        
        <div class="overlay-footer">
          <button class="reject-button" @click="rejectRequest">Reject</button>
          <button class="accept-button" @click="acceptRequest">Accept</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QAHeadNotifications',
  data() {
    return {
      notifications: [
        { 
          id: 1, 
          project: 'PROJ001', 
          serialNumber: '15,16', 
          lru: 'LRU Name', 
          completedStage: 'stage 1', 
          requiredStage: 'stage3', 
          justification: 'justification', 
          status: 'pending',
          isRead: false,
          timestamp: '2025-01-15 10:30:00'
        },
        { 
          id: 2, 
          project: 'PROJ002', 
          serialNumber: '17,18', 
          lru: 'LRU Component', 
          completedStage: 'stage 2', 
          requiredStage: 'stage4', 
          justification: 'Technical review required', 
          status: 'pending',
          isRead: false,
          timestamp: '2025-01-15 09:15:00'
        },
        { 
          id: 3, 
          project: 'PROJ003', 
          serialNumber: '19,20', 
          lru: 'LRU Assembly', 
          completedStage: 'stage 1', 
          requiredStage: 'stage3', 
          justification: 'Quality check needed', 
          status: 'pending',
          isRead: true,
          timestamp: '2025-01-14 16:45:00'
        }
      ],
      showOverlay: false,
      selectedNotification: null,
      comments: ''
    };
  },
  methods: {
    formatTimestamp(timestamp) {
      const date = new Date(timestamp);
      return date.toLocaleString();
    },
    viewNotification(notification) {
      this.selectedNotification = { ...notification };
      this.comments = '';
      this.showOverlay = true;
      // Mark as read
      notification.isRead = true;
      // Update notification count in parent component
      this.$emit('notification-read', notification.id);
    },
    closeOverlay() {
      this.showOverlay = false;
      this.selectedNotification = null;
      this.comments = '';
    },
    acceptRequest() {
      if (this.selectedNotification) {
        this.selectedNotification.status = 'accepted';
        // Update the original notification
        const original = this.notifications.find(n => n.id === this.selectedNotification.id);
        if (original) {
          original.status = 'accepted';
        }
        alert(`Request for ${this.selectedNotification.project} has been accepted. Comments: ${this.comments}`);
        this.closeOverlay();
      }
    },
    rejectRequest() {
      if (this.selectedNotification) {
        this.selectedNotification.status = 'rejected';
        // Update the original notification
        const original = this.notifications.find(n => n.id === this.selectedNotification.id);
        if (original) {
          original.status = 'rejected';
        }
        alert(`Request for ${this.selectedNotification.project} has been rejected. Comments: ${this.comments}`);
        this.closeOverlay();
      }
    }
  }
};
</script>

<style scoped>
.notifications-page {
  min-height: 100vh;
  background: #f5f5f5;
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
  background: white;
  padding: 25px;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
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
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
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
