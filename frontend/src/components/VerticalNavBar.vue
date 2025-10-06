<template>
  <div class="vertical-nav-overlay" v-if="isOpen" @click="closeNav">
    <div class="vertical-nav" @click.stop>
      <div class="nav-header">
        <h3>Menu</h3>
        <button class="close-btn" @click="closeNav">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>
      
      <div class="nav-content">
        <div class="user-info">
          <div class="user-avatar">
            <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
          </div>
          <div class="user-details">
            <h4>{{ userInfo.name }}</h4>
            <p>{{ userInfo.role }}</p>
          </div>
        </div>
        
        <nav class="nav-menu">
          <div class="nav-item" @click="navigateToProfile">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
            <span>Profile</span>
          </div>
          
          <div class="nav-item" @click="navigateToSettings">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="3"></circle>
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1 1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
            </svg>
            <span>Settings</span>
          </div>
          
          <div class="nav-item" @click="navigateToSignature">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 20h9"></path>
              <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
            </svg>
            <span>Signature</span>
          </div>
          
          <div class="nav-divider"></div>
          
          <div class="nav-item logout" @click="logout">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
              <polyline points="16 17 21 12 16 7"></polyline>
              <line x1="21" y1="12" x2="9" y2="12"></line>
            </svg>
            <span>Logout</span>
          </div>
        </nav>
      </div>
    </div>
  </div>
</template>

<script>
import { userStore } from '@/stores/userStore'

export default {
  name: 'VerticalNavBar',
  props: {
    isOpen: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    userInfo() {
      return userStore.getters.currentUser() || { name: 'User', role: 'Unknown' }
    }
  },
  methods: {
    closeNav() {
      this.$emit('close')
    },
    navigateToProfile() {
      this.$emit('navigate', 'profile')
      this.closeNav()
    },
    navigateToSettings() {
      this.$emit('navigate', 'settings')
      this.closeNav()
    },
    navigateToSignature() {
      this.$emit('navigate', 'signature')
      this.closeNav()
    },
    logout() {
      this.$emit('logout')
      this.closeNav()
    }
  }
}
</script>

<style scoped>
.vertical-nav-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  display: flex;
  justify-content: flex-end;
  align-items: flex-start;
  padding-top: 20px;
  padding-right: 20px;
}

.vertical-nav {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  width: 320px;
  max-height: 80vh;
  overflow-y: auto;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.nav-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e5e7eb;
}

.nav-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #111827;
}

.close-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 6px;
  color: #6b7280;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background-color: #f3f4f6;
  color: #374151;
}

.nav-content {
  padding: 0;
}

.user-info {
  display: flex;
  align-items: center;
  padding: 20px 24px;
  background-color: #f8fafc;
  border-bottom: 1px solid #e5e7eb;
}

.user-avatar {
  width: 48px;
  height: 48px;
  background-color: #3b82f6;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin-right: 12px;
}

.user-details h4 {
  margin: 0 0 4px 0;
  font-size: 1rem;
  font-weight: 600;
  color: #111827;
}

.user-details p {
  margin: 0;
  font-size: 0.875rem;
  color: #6b7280;
}

.nav-menu {
  padding: 8px 0;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 12px 24px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  color: #374151;
}

.nav-item:hover {
  background-color: #f3f4f6;
}

.nav-item svg {
  margin-right: 12px;
  color: #6b7280;
}

.nav-item span {
  font-size: 0.875rem;
  font-weight: 500;
}

.nav-item.logout {
  color: #dc2626;
}

.nav-item.logout:hover {
  background-color: #fef2f2;
}

.nav-item.logout svg {
  color: #dc2626;
}

.nav-divider {
  height: 1px;
  background-color: #e5e7eb;
  margin: 8px 0;
}

/* Responsive design */
@media (max-width: 480px) {
  .vertical-nav {
    width: 280px;
    margin: 0 10px;
  }
  
  .vertical-nav-overlay {
    padding-right: 10px;
  }
}
</style>
