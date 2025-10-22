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
          
          <div class="nav-item" @click="navigateToTechSupport">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M9 12l2 2 4-4"></path>
              <path d="M21 12c.552 0 1-.448 1-1V5c0-.552-.448-1-1-1H3c-.552 0-1 .448-1 1v6c0 .552.448 1 1 1h18z"></path>
              <path d="M3 12h18v6c0 .552-.448 1-1 1H4c-.552 0-1-.448-1-1v-6z"></path>
            </svg>
            <span>Tech Support</span>
          </div>
          
          <div class="nav-item signature-item" @click="toggleSignatureSubmenu" :class="{ 'active': showSignatureSubmenu }">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 20h9"></path>
              <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
            </svg>
            <span>Signature</span>
            <svg class="dropdown-arrow" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </div>
          
          <!-- Signature Submenu -->
          <div class="signature-submenu" v-if="showSignatureSubmenu">
            <div class="submenu-item" @click="changeLoginPassword">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                <circle cx="12" cy="16" r="1"></circle>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
              </svg>
              <span>Change Login Password</span>
            </div>
            <div class="submenu-item" @click="changeSignaturePassword">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 20h9"></path>
                <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
              </svg>
              <span>Change Signature Password</span>
            </div>
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
    
    <!-- Password Change Modal -->
    <PasswordChangeModal 
      :isOpen="isPasswordModalOpen"
      :passwordType="passwordType"
      @close="closePasswordModal"
    />
  </div>
</template>

<script>
import { userStore } from '@/stores/userStore'
import PasswordChangeModal from './PasswordChangeModal.vue'

export default {
  name: 'VerticalNavBar',
  components: {
    PasswordChangeModal
  },
  props: {
    isOpen: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      showSignatureSubmenu: false,
      isPasswordModalOpen: false,
      passwordType: 'login'
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
    navigateToTechSupport() {
      // Check if user is admin - if so, go to tech support management, otherwise go to tech support form
      const userRole = userStore.getters.currentUserRole()
      const roleName = userStore.getters.roleName()
      
      if (userRole === 1 || roleName?.toLowerCase() === 'admin') {
        // Admin users go to tech support management page
        this.$emit('navigate', 'tech-support-management')
      } else {
        // Regular users go to their tech support dashboard
        this.$emit('navigate', 'tech-support-user-dashboard')
      }
      this.closeNav()
    },
    toggleSignatureSubmenu() {
      this.showSignatureSubmenu = !this.showSignatureSubmenu
    },
    changeLoginPassword() {
      this.passwordType = 'login'
      this.isPasswordModalOpen = true
    },
    changeSignaturePassword() {
      this.passwordType = 'signature'
      this.isPasswordModalOpen = true
    },
    closePasswordModal() {
      this.isPasswordModalOpen = false
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

.signature-item {
  position: relative;
}

.signature-item.active {
  background-color: #f3f4f6;
}

.dropdown-arrow {
  margin-left: auto;
  color: #6b7280;
  transition: transform 0.2s ease;
}

.signature-item.active .dropdown-arrow {
  transform: rotate(180deg);
  color: #3b82f6;
}

.signature-submenu {
  background-color: #f8fafc;
  border-left: 3px solid #3b82f6;
  margin-left: 20px;
  animation: slideDown 0.2s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.submenu-item {
  display: flex;
  align-items: center;
  padding: 10px 24px 10px 44px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  color: #374151;
  font-size: 0.8rem;
}

.submenu-item:hover {
  background-color: #e5e7eb;
}

.submenu-item svg {
  margin-right: 10px;
  color: #6b7280;
}

.submenu-item span {
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
