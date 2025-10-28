<template>
  <div v-if="isOpen" class="notifications-overlay" @click="closeOnOverlay">
    <div class="overlay-container" @click.stop>
      <!-- Header -->
      <div class="overlay-header">
        <div class="header-content">
          <h2>Notifications</h2>
          <span v-if="unreadCount > 0" class="unread-badge">{{ unreadCount }} unread</span>
        </div>
        <button class="close-button" @click="close">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>

      <!-- Content -->
      <div class="overlay-content">
        <div v-if="loading" class="loading-state">
          <p>Loading notifications...</p>
        </div>
        
        <div v-else-if="error" class="error-state">
          <p>{{ error }}</p>
          <button @click="fetchNotifications" class="retry-btn">Retry</button>
        </div>
        
        <div v-else-if="notifications.length === 0" class="empty-state">
          <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
            <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
          </svg>
          <p>No notifications</p>
        </div>
        
        <div v-else class="notifications-list">
          <div 
            v-for="notification in notifications" 
            :key="notification.activity_id"
            class="notification-item"
            :class="{ 'unread': !notification.is_read }"
            @click="viewNotification(notification)"
          >
            <div class="notification-icon">
              <svg v-if="!notification.is_read" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
              </svg>
            </div>
            <div class="notification-content">
              <div class="notification-header">
                <h4>{{ notification.activity_performed }}</h4>
                <span class="notification-time">{{ formatTime(notification.timestamp) }}</span>
              </div>
              <p class="notification-details">{{ notification.additional_info }}</p>
              <div class="notification-meta">
                <span class="notification-from">{{ notification.performed_by_name || 'Unknown' }}</span>
                <span v-if="notification.project_name" class="notification-project">{{ notification.project_name }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { userStore } from '@/stores/userStore';

export default {
  name: 'NotificationsOverlay',
  props: {
    isOpen: {
      type: Boolean,
      default: false
    }
  },
  emits: ['close'],
  data() {
    return {
      notifications: [],
      unreadCount: 0,
      loading: false,
      error: null,
      refreshInterval: null
    };
  },
  watch: {
    isOpen(newVal) {
      if (newVal) {
        this.fetchNotifications();
        this.startAutoRefresh();
      } else {
        this.stopAutoRefresh();
      }
    }
  },
  async mounted() {
    if (this.isOpen) {
      await this.fetchNotifications();
      this.startAutoRefresh();
    }
  },
  beforeUnmount() {
    this.stopAutoRefresh();
  },
  methods: {
    async fetchNotifications() {
      this.loading = true;
      this.error = null;
      
      try {
        const currentUser = userStore.getters.currentUser();
        
        if (!currentUser || !currentUser.id) {
          this.error = 'User not logged in';
          return;
        }

        const response = await fetch(`http://localhost:5000/api/notifications/${currentUser.id}?limit=50`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          }
        });

        const data = await response.json();

        if (data.success) {
          this.notifications = data.notifications;
          this.unreadCount = this.notifications.filter(n => !n.is_read).length;
        } else {
          this.error = data.message || 'Failed to fetch notifications';
        }
      } catch (error) {
        console.error('Error fetching notifications:', error);
        this.error = 'Failed to load notifications';
      } finally {
        this.loading = false;
      }
    },
    async viewNotification(notification) {
      // Mark as read when viewed
      if (!notification.is_read) {
        await this.markAsRead(notification.activity_id);
      }
    },
    async markAsRead(notificationId) {
      try {
        const response = await fetch(`http://localhost:5000/api/notifications/${notificationId}/mark-read`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          }
        });

        const data = await response.json();

        if (data.success) {
          const notif = this.notifications.find(n => n.activity_id === notificationId);
          if (notif) {
            notif.is_read = true;
            this.unreadCount--;
          }
        }
      } catch (error) {
        console.error('Error marking notification as read:', error);
      }
    },
    formatTime(timestamp) {
      if (!timestamp) return '';
      const date = new Date(timestamp);
      const now = new Date();
      const diffMs = now - date;
      const diffMins = Math.floor(diffMs / 60000);
      
      if (diffMins < 1) return 'Just now';
      if (diffMins < 60) return `${diffMins}m ago`;
      if (diffMins < 1440) return `${Math.floor(diffMins / 60)}h ago`;
      return date.toLocaleDateString();
    },
    startAutoRefresh() {
      this.refreshInterval = setInterval(this.fetchNotifications, 30000);
    },
    stopAutoRefresh() {
      if (this.refreshInterval) {
        clearInterval(this.refreshInterval);
        this.refreshInterval = null;
      }
    },
    close() {
      this.$emit('close');
    },
    closeOnOverlay(event) {
      if (event.target === event.currentTarget) {
        this.close();
      }
    }
  }
};
</script>

<style scoped>
.notifications-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10005;
  padding: 20px;
  animation: fadeIn 0.2s ease;
  margin: 0;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.overlay-container {
  background: white;
  border-radius: 12px;
  width: 100%;
  max-width: 700px;
  max-height: 85vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.overlay-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e2e8f0;
  background: #2d3748;
  color: white;
  border-radius: 12px 12px 0 0;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 15px;
}

.header-content h2 {
  margin: 0;
  font-size: 1.5em;
  font-weight: 600;
}

.unread-badge {
  background: #dc3545;
  color: white;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.9em;
  font-weight: 600;
}

.close-button {
  background: transparent;
  border: none;
  color: white;
  cursor: pointer;
  padding: 8px;
  border-radius: 8px;
  transition: background 0.2s ease;
}

.close-button:hover {
  background: rgba(255, 255, 255, 0.1);
}

.overlay-content {
  flex: 1;
  overflow-y: auto;
  padding: 0;
}

.notifications-list {
  padding: 8px;
  max-height: calc(85vh - 120px);
  overflow-y: auto;
}

.notification-item {
  display: flex;
  gap: 12px;
  padding: 16px;
  border-bottom: 1px solid #e2e8f0;
  cursor: pointer;
  transition: background 0.2s ease;
}

.notification-item:hover {
  background: #f8fafc;
}

.notification-item.unread {
  background: #fff3cd;
  border-left: 4px solid #ffc107;
}

.notification-icon {
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #dc3545;
}

.notification-content {
  flex: 1;
  min-width: 0;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 8px;
}

.notification-header h4 {
  margin: 0;
  color: #2d3748;
  font-size: 1em;
  font-weight: 600;
}

.notification-time {
  color: #999;
  font-size: 0.85em;
  white-space: nowrap;
}

.notification-details {
  margin: 0 0 8px 0;
  color: #666;
  font-size: 0.9em;
  line-height: 1.4;
}

.notification-meta {
  display: flex;
  gap: 12px;
  font-size: 0.85em;
  color: #999;
}

.notification-from {
  font-weight: 500;
}

.notification-project {
  color: #007bff;
}

.loading-state,
.error-state,
.empty-state {
  padding: 60px 24px;
  text-align: center;
  color: #999;
}

.error-state {
  color: #dc3545;
}

.empty-state svg {
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-state p {
  margin: 0;
  font-size: 1.1em;
}

.retry-btn {
  margin-top: 12px;
  padding: 8px 16px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}

.retry-btn:hover {
  background: #0056b3;
}

/* Custom scrollbar */
.overlay-content::-webkit-scrollbar,
.notifications-list::-webkit-scrollbar {
  width: 8px;
}

.overlay-content::-webkit-scrollbar-track,
.notifications-list::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 0 0 12px 12px;
}

.overlay-content::-webkit-scrollbar-thumb,
.notifications-list::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.overlay-content::-webkit-scrollbar-thumb:hover,
.notifications-list::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* Responsive adjustments for mobile */
@media (max-width: 768px) {
  .overlay-container {
    max-width: 95%;
    max-height: 90vh;
    margin: 10px;
  }
  
  .notifications-overlay {
    padding: 10px;
  }
}
</style>

