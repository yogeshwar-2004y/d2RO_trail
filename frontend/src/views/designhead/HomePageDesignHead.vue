<template>
  <div class="home-page-container">
    <!-- Floating Hamburger Menu Button -->
    <button class="floating-menu-button" @click="toggleMenu">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="3" y1="6" x2="21" y2="6"></line>
        <line x1="3" y1="12" x2="21" y2="12"></line>
        <line x1="3" y1="18" x2="21" y2="18"></line>
      </svg>
    </button>
    
    <div class="card-container">
      <div class="card" @click="goToPage('Documents')">
        <div class="card-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <line x1="10" y1="9" x2="8" y2="9"></line>
          </svg>
        </div>
        <div class="card-title">DOCUMENTS</div>
      </div>
      <div class="card" @click="goToPage('Memo')">
        <div class="card-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 20h9"></path>
            <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
          </svg>
        </div>
        <div class="card-title">MEMO</div>
      </div>
      <div class="card" @click="goToPage('TestReports')">
        <div class="card-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 3v18h18"></path>
            <path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3"></path>
          </svg>
        </div>
        <div class="card-title">TEST REPORTS</div>
      </div>
      <div class="card" @click="goToPage('AssignProject')">
        <div class="card-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
            <circle cx="9" cy="7" r="4"></circle>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
          </svg>
        </div>
        <div class="card-title">ASSIGN PROJECT</div>
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
  name: 'HomePageDesignHead',
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
      if (pageName === 'Documents') {
        this.$router.push({ name: 'ProjectsDashboard' });
      } else if (pageName === 'Memo') {
        this.$router.push({ name: 'MemoDashboard' });
      } else if (pageName === 'TestReports') {
        this.$router.push({ name: 'ReportDashboard' });
      } else if (pageName === 'AssignProject') {
        // alert('Navigating to Assign Project page.');
        this.$router.push({ name: 'ProjectsForAssigning' });
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
      this.$router.push({ name: 'login' });
    }
  }
};
</script>

<style scoped>
.home-page-container {
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
  margin-top: 50px;
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
  gap: 30px; /* Increased gap for better spacing */
  width: 100%;
  max-width: 1000px; /* Increased width for 4 cards horizontally */
}

.card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #fff;
  border-radius: 15px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
  width: 180px; /* Smaller for 4 cards in horizontal layout */
  height: 180px; /* Smaller for 4 cards in horizontal layout */
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
  font-size: 0.9em;
  font-weight: bold;
  text-align: center;
  color: #333;
  text-transform: uppercase;
  letter-spacing: 1px;
}
</style>