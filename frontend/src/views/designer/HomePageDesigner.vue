<template>
  <div class="designer-home">
    <!-- Floating Hamburger Menu Button -->
    <button class="floating-menu-button" @click="toggleMenu">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="3" y1="6" x2="21" y2="6"></line>
        <line x1="3" y1="12" x2="21" y2="12"></line>
        <line x1="3" y1="18" x2="21" y2="18"></line>
      </svg>
    </button>
    
    <!-- Main Content -->
    <main class="main-content">
      <div class="cards-container">
        <!-- Documents Card -->
        <div class="nav-card" @click="navigateToDocuments">
          <div class="card-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
              <line x1="16" y1="13" x2="8" y2="13"></line>
              <line x1="16" y1="17" x2="8" y2="17"></line>
              <line x1="10" y1="9" x2="8" y2="9"></line>
            </svg>
          </div>
          <div class="card-label">DOCUMENTS</div>
        </div>

        <!-- Memo Card -->
        <div class="nav-card" @click="navigateToMemo">
          <div class="card-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 20h9"></path>
              <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
            </svg>
          </div>
          <div class="card-label">MEMO</div>
        </div>

        <!-- Test Reports Card -->
        <div class="nav-card" @click="navigateToTestReports">
          <div class="card-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 3v18h18"></path>
              <path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3"></path>
            </svg>
          </div>
          <div class="card-label">TEST REPORTS</div>
        </div>
      </div>
    </main>
    
    
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
import VerticalNavBar from '@/components/VerticalNavBar.vue'

export default {
  name: "HomePageDesigner",
  components: {
    VerticalNavBar
  },
  data() {
    return {
      isMenuOpen: false
    }
  },
  methods: {
    navigateToDocuments() {
      // Navigate to documents section
      this.$router.push({ name: 'ProjectsDashboard' });
    },
    navigateToMemo() {
      // Navigate to memo section
      console.log('Navigating to Memo');
      this.$router.push({ name: 'MemoDashboard' });
    },
    navigateToTestReports() {
      // Navigate to the test reports page
      this.$router.push({ name: 'ReportDashboard' });
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
          console.log('Navigate to profile');
          break;
        case 'settings':
          console.log('Navigate to settings');
          break;
        case 'change-login-password':
          console.log('Navigate to change login password');
          break;
        case 'change-signature-password':
          console.log('Navigate to change signature password');
          break;
        default:
          console.log('Unknown navigation action:', action);
      }
    },
    logout() {
      // alert('Logging out...');
      this.$router.push({ name: 'login' });
    }
  }
};
</script>

<style scoped>
.designer-home {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  padding: 20px;
  font-family: Arial, sans-serif;
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

/* Header Styles */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding: 0 20px;
  margin-bottom: 40px;
}

.brand {
  display: flex;
  align-items: center;
}

.logo-image {
  width: 150px;
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

.logout-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  color: #000;
  padding: 8px;
  border-radius: 6px;
  transition: background-color 0.2s ease;
}

.logout-btn:hover {
  background-color: rgba(0, 0, 0, 0.1);
}

.logout-btn svg {
  transform: rotate(180deg);
  width: 24px;
  height: 24px;
}

/* Main Content Styles */
.main-content {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-grow: 1;
  padding: 20px;
}

.cards-container {
  display: flex;
  gap: 40px;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}

/* Navigation Card Styles */
.nav-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #fff;
  border-radius: 20px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  width: 250px;
  height: 250px;
  padding: 30px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.nav-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
  border-color: rgba(0, 0, 0, 0.1);
}

.card-icon {
  color: #000;
  margin-bottom: 20px;
}

.card-label {
  font-size: 1.2em;
  font-weight: bold;
  text-align: center;
  color: #333;
  line-height: 1.3;
}

/* Responsive Design */
@media (max-width: 768px) {
  .cards-container {
    flex-direction: column;
    gap: 30px;
  }
  
  .nav-card {
    width: 220px;
    height: 220px;
  }
}

.dashboard-news-ticker {
  margin-top: auto;
  position: sticky;
  bottom: 0;
}
</style>
