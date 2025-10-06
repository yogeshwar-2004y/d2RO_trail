<template>
  <div class="home-page">
    <header class="app-header">
      <div class="logos-container">
        <img src="@/assets/images/aviatrax-logo.png" alt="Aviatrax Logo" class="logo">
        <img src="@/assets/images/vista_logo.png" alt="Vista Logo" class="logo vista-logo">
      </div>
      <div class="header-actions">
        <button class="menu-button" @click="toggleMenu">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="3" y1="6" x2="21" y2="6"></line>
            <line x1="3" y1="12" x2="21" y2="12"></line>
            <line x1="3" y1="18" x2="21" y2="18"></line>
          </svg>
        </button>
        <button class="logout-button" @click="logout">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
            <polyline points="16 17 21 12 16 7"></polyline>
            <line x1="21" y1="12" x2="9" y2="12"></line>
          </svg>
        </button>
      </div>
    </header>
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
    </div>
    
    <!-- News Ticker at the bottom -->
    <NewsTicker 
      height="60px" 
      backgroundColor="#34495e" 
      textColor="#ffffff"
      class="dashboard-news-ticker"
    />
    
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
import NewsTicker from '@/components/NewsTicker.vue'
import VerticalNavBar from '@/components/VerticalNavBar.vue'

export default {
  name: 'HomePageReviewer',
  components: {
    NewsTicker,
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
          console.log('Navigate to profile');
          break;
        case 'settings':
          console.log('Navigate to settings');
          break;
        case 'signature':
          console.log('Navigate to signature');
          break;
        default:
          console.log('Unknown navigation action:', action);
      }
    },
    logout() {
      // Logic to log the user out and redirect to the login page
      // e.g., this.$router.push({ name: 'login' });
      alert('Logging out...');
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
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding: 0 20px;
}

.logo {
  width: 150px; /* Adjust size as needed */
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