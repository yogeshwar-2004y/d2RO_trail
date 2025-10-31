<template>
  <div class="notification-badge-container">
    <button class="notification-bell" @click="toggleNotifications">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
        <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
      </svg>
      <span v-if="unreadCount > 0" class="badge">{{ unreadCount }}</span>
    </button>
    
    <div v-if="showDropdown" class="notification-dropdown">
      <div class="dropdown-header">
        <h3>Notifications</h3>
        <span v-if="unreadCount > 0" class="unread-count">{{ unreadCount }} unread</span>
      </div>
      <div class="dropdown-content">
        <div v-if="loading" class="loading">Loading...</div>
        <div v-else-if="error" class="error">{{ error }}</div>
        <div v-else-if="notifications.length === 0" class="no-notifications">
          No notifications
        </div>
        <div v-else>
          <div 
            v-for="notification in notifications.slice(0, 5)" 
            :key="notification.activity_id"
            class="notification-item"
            :class="{ 'unread': !notification.is_read }"
            @click="viewNotification(notification)"
          >
            <div class="notification-content">
              <strong>{{ notification.activity_performed }}</strong>
              <p>{{ notification.additional_info }}</p>
              <span class="notification-time">{{ formatTime(notification.timestamp) }}</span>
            </div>
          </div>
          <div v-if="notifications.length > 5" class="view-all">
            <router-link to="/notifications" @click="toggleNotifications">View all notifications</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { userStore } from '@/stores/userStore';

export default {
  name: 'NotificationBadge',
  data() {
    return {
      notifications: [],
      unreadCount: 0,
      loading: false,
      error: null,
      showDropdown: false,
      refreshInterval: null
    };
  },
  async mounted() {
    await this.fetchNotifications();
    // Poll for new notifications every 30 seconds
    this.refreshInterval = setInterval(this.fetchNotifications, 30000);
    
    // Close dropdown when clicking outside
    document.addEventListener('click', this.handleClickOutside);
  },
  beforeUnmount() {
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval);
    }
    document.removeEventListener('click', this.handleClickOutside);
  },
  methods: {
    async fetchNotifications() {
      this.loading = true;
      this.error = null;
      
      try {
        const currentUser = userStore.getters.currentUser();
        
        if (!currentUser || !currentUser.id) {
          return;
        }

        const response = await fetch(`http://localhost:5000/api/notifications/${currentUser.id}?limit=10&unread_only=false`, {
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
    toggleNotifications() {
      this.showDropdown = !this.showDropdown;
      if (this.showDropdown && this.notifications.length === 0) {
        this.fetchNotifications();
      }
    },
    handleClickOutside(event) {
      if (!event.target.closest('.notification-badge-container')) {
        this.showDropdown = false;
      }
    },
    async viewNotification(notification) {
      if (!notification.is_read) {
        await this.markAsRead(notification.activity_id);
      }
      this.$router.push('/notifications');
      this.showDropdown = false;
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
    }
  }
};
</script>

<style scoped>
.notification-badge-container {
  position: relative;
  margin-left: 20px;
}

.notification-bell {
  position: relative;
  background: #2d3748;
  border: none;
  padding: 10px;
  border-radius: 50%;
  cursor: pointer;
  color: white;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.notification-bell:hover {
  background: #1a202c;
  transform: scale(1.1);
}

.badge {
  position: absolute;
  top: 0;
  right: 0;
  background: #dc3545;
  color: white;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: bold;
  transform: translate(30%, -30%);
}

.notification-dropdown {
  position: absolute;
  top: 60px;
  right: 0;
  width: 400px;
  max-height: 500px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  overflow: hidden;
}

.dropdown-header {
  padding: 15px 20px;
  border-bottom: 1px solid #e2e8f0;
  background: #2d3748;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dropdown-header h3 {
  margin: 0;
  font-size: 1.1em;
}

.unread-count {
  font-size: 0.9em;
  background: #dc3545;
  padding: 4px 10px;
  border-radius: 12px;
}

.dropdown-content {
  max-height: 400px;
  overflow-y: auto;
}

.notification-item {
  padding: 15px 20px;
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

.notification-content strong {
  display: block;
  color: #2d3748;
  margin-bottom: 5px;
}

.notification-content p {
  margin: 0;
  color: #666;
  font-size: 0.9em;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.notification-time {
  display: block;
  font-size: 0.8em;
  color: #999;
  margin-top: 5px;
}

.loading,
.error,
.no-notifications {
  padding: 40px 20px;
  text-align: center;
  color: #999;
}

.error {
  color: #dc3545;
}

.view-all {
  padding: 15px;
  text-align: center;
  border-top: 1px solid #e2e8f0;
}

.view-all a {
  color: #007bff;
  text-decoration: none;
  font-weight: 600;
}

.view-all a:hover {
  text-decoration: underline;
}
</style>

