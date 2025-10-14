<template>
  <div class="home-page">
    <!-- Floating Hamburger Menu Button -->
    <button class="floating-menu-button" @click="toggleMenu">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="3" y1="6" x2="21" y2="6"></line>
        <line x1="3" y1="12" x2="21" y2="12"></line>
        <line x1="3" y1="18" x2="21" y2="18"></line>
      </svg>
    </button>
    
    <div class="card-container">
      <div class="card" @click="goToPage('ProjectsDashboard')">
        <div class="card-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <line x1="10" y1="9" x2="8" y2="9"></line>
          </svg>
        </div>
        <div class="card-title">PLAN DOCUMENTS</div>
      </div>
      <div class="card" @click="goToPage('MemoDashboard')">
        <div class="card-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 20h9"></path>
            <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
          </svg>
        </div>
        <div class="card-title">MEMO</div>
      </div>
      <div class="card" @click="goToPage('ReportDashboard')">
        <div class="card-icon">
          <svg xmlns="" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 20h9"></path>
            <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
          </svg>
        </div>
        <div class="card-title">TEST REPORTS</div>
      </div>
      <div class="card" @click="goToPage('UserActivities')">
        <div class="card-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
            <circle cx="9" cy="7" r="4"></circle>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
          </svg>
        </div>
        <div class="card-title">USER ACTIVITIES</div>
      </div>
    </div>
    
    
    <!-- Vertical Navigation Bar -->
    <VerticalNavBar 
      :isOpen="isMenuOpen" 
      @close="closeMenu"
      @navigate="handleNavigation"
      @logout="logout"
    />
  </div>
</template>

<script>
import router from '@/router';

import VerticalNavBar from '@/components/VerticalNavBar.vue'

export default {
  name: 'HomePageAdmin',
  components: {
    VerticalNavBar
  },
  data() {
    return {
      isMenuOpen: false
    }
  },
  methods: {
    goToPage(pageName) {
        if (pageName === 'ProjectsDashboard') {
            this.$router.push({ name: 'ProjectsDashboard' });
        } else if (pageName === 'MemoDashboard') {
            this.$router.push({ name: 'MemoDashboard' });
        } else if (pageName === 'ReportDashboard') {
            this.$router.push({ name: 'ReportDashboard' });
        } else if (pageName === 'UserActivities') {
            this.$router.push({ name: 'UserActivities' });
        }
      // Logic to navigate to the selected page
      // e.g., this.$router.push({ name: pageName });
      // alert(`Navigating to ${pageName}`);
    },
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen;
    },
    closeMenu() {
      this.isMenuOpen = false;
    },
    handleNavigation(action) {
      switch(action) {
        case 'profile':
          // Navigate to profile page
          console.log('Navigate to profile');
          break;
        case 'settings':
          // Navigate to settings page
          console.log('Navigate to settings');
          break;
        case 'change-login-password':
          // Navigate to change login password page
          console.log('Navigate to change login password');
          break;
        case 'change-signature-password':
          // Navigate to change signature password page
          console.log('Navigate to change signature password');
          break;
        default:
          console.log('Unknown navigation action:', action);
      }
    },
    logout() {
      // Logic to log the user out and redirect to the login page
      // e.g., this.$router.push({ name: 'login' });
      // alert('Logging out...');
      this.$router.push({ name: 'login' });
    }
  }
};
</script>

<style scoped>
.home-page {
  background-color: #f0f0f0;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  padding: 20px;
  position: relative; /* For floating menu button */
}

/* Floating Hamburger Menu Button */
.floating-menu-button {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1001;
  background: #162845;
  color: white;
  border: none;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.floating-menu-button:hover {
  background: #51759a;
  transform: scale(1.1);
}

.floating-menu-button svg {
  width: 24px;
  height: 24px;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding: 0 20px;
}




.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.menu-button {
  background: transparent;
  border: none;
  cursor: pointer;
  color: #000;
  padding: 8px;
  border-radius: 6px;
  transition: background-color 0.2s ease;
}

.menu-button:hover {
  background-color: rgba(0, 0, 0, 0.1);
}

.menu-button svg {
  width: 24px;
  height: 24px;
}

.logout-button {
  background: transparent;
  border: none;
  cursor: pointer;
  color: #000;
  padding: 8px;
  border-radius: 6px;
  transition: background-color 0.2s ease;
}

.logout-button:hover {
  background-color: rgba(0, 0, 0, 0.1);
}

.logout-button svg {
  transform: rotate(180deg);
  width: 24px;
  height: 24px;
}

.card-container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-grow: 1;
  gap: 30px;
}

.card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #fff;
  border-radius: 15px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
  width: 220px;
  height: 220px;
  padding: 20px;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.card-icon {
  color: #000;
  margin-bottom: 15px;
}

.card-title {
  font-size: 1.1em;
  font-weight: bold;
  text-align: center;
  color: #333;
}

.dashboard-news-ticker {
  margin-top: auto;
  position: sticky;
  bottom: 0;
}
</style>