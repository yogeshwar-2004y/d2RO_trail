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
      <div class="card" @click="goToPage('QAHeadProjectsDashboard')">
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
      <div class="card" @click="goToPage('QAHeadMemoDashboard')">
        <div class="card-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 20h9"></path>
            <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
          </svg>
        </div>
        <div class="card-title">MEMO</div>
      </div>
      <div class="card" @click="goToPage('QAHeadReportDashboard')">
        <div class="card-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 3v18h18"></path>
            <path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3"></path>
          </svg>
        </div>
        <div class="card-title">REPORTS</div>
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
import VerticalNavBar from '@/components/VerticalNavBar.vue'

export default {
  name: 'HomePageQAHead',
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
      if (pageName === 'QAHeadProjectsDashboard') {
        this.$router.push({ name: 'ProjectsDashboard' }); //QAHeadProjectsDashboard
      } else if (pageName === 'QAHeadMemoDashboard') {
        this.$router.push({ name: 'MemoDashboard' }); //QAHeadMemoDashboard
      } else if (pageName === 'QAHeadReportDashboard') {
        this.$router.push({ name: 'ReportDashboard' }); //QAHeadReportDashboard
      }
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
        case 'tech-support':
          // Navigate to tech support form page (for regular users)
          this.$router.push({ name: 'TechSupport' });
          break;
        case 'tech-support-management':
          // Navigate to tech support management page (for admin users)
          this.$router.push({ name: 'TechSupportManagement' });
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
      this.$router.push({ name: 'login' });
    }
  }
};
</script>

<style scoped>
.home-page {
  background-color: #f0f0f0;
  height: calc(100vh - 240px); /* Fixed height to prevent scrolling */
  display: flex;
  flex-direction: column;
  justify-content: center; /* Center content vertically */
  align-items: center; /* Center content horizontally */
  padding: 0;
  margin: 0;
  overflow: hidden; /* Prevent any scrolling */
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

.card-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 40px; /* Increased gap for better spacing */
  width: 100%;
  max-width: 900px; /* Limit container width */
}

.card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #fff;
  border-radius: 15px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
  width: 200px; /* Slightly smaller for better fit */
  height: 200px; /* Slightly smaller for better fit */
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
  font-size: 1em;
  font-weight: bold;
  text-align: center;
  color: #333;
  text-transform: uppercase;
  letter-spacing: 1px;
}
</style>
